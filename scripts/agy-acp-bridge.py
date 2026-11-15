#!/usr/bin/env python3
"""
scripts/agy-acp-bridge.py
AI chỉ đạo điều khiển `agy acp --sandbox` (Antigravity Agent Control Protocol) làm việc.
Tự động cấp quyền file/lệnh theo chính sách an toàn, hỗ trợ phiên sống (multi-turn) và kiểm toán.
Chạy với thư viện chuẩn Python 3.9+, không dependency ngoài.

Usage:
  python3 scripts/agy-acp-bridge.py run --dir <repo> --task-file <brief.md> \\
      [--allow-write PATH ...] [--allow-cmd REGEX ...] [--model M] \\
      [--session ID] [--worktree --seed PATH --apply] [--timeout SEC] [--report-dir DIR]
"""

from __future__ import annotations

import argparse
import errno
import fnmatch
import importlib.util
import json
import os
import queue
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Nạp agy-bridge.py để tái sử dụng các hàm hạ tầng
BRIDGE_PY = Path(__file__).resolve().parent / "agy-bridge.py"
spec = importlib.util.spec_from_file_location("agy_bridge", str(BRIDGE_PY))
if not spec or not spec.loader:
    raise RuntimeError(f"Không thể nạp agy-bridge từ {BRIDGE_PY}")
agy_bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agy_bridge)

get_lock_file = agy_bridge.get_lock_file
get_git_status = agy_bridge.get_git_status
get_git_head = agy_bridge.get_git_head
get_git_branch = agy_bridge.get_git_branch
get_file_fingerprint = agy_bridge.get_file_fingerprint
snapshot_repo_state = agy_bridge.snapshot_repo_state
copy_path_into_worktree = agy_bridge.copy_path_into_worktree
map_allow_write_to_worktree = agy_bridge.map_allow_write_to_worktree
calculate_changed_files = agy_bridge.calculate_changed_files
get_all_changed_files = agy_bridge.get_all_changed_files
check_violations = agy_bridge.check_violations
check_quota_error = agy_bridge.check_quota_error
parse_agy_json = agy_bridge.parse_agy_json
QUOTA_KEYWORDS = agy_bridge.QUOTA_KEYWORDS
redact_secrets = agy_bridge.redact_secrets
sanitize_task_slug = agy_bridge.sanitize_task_slug
is_ignored_cache_file = agy_bridge.is_ignored_cache_file


def as_dict(x: any) -> dict:
    """Helper đảm bảo trả về dict khi nhận dữ liệu JSON-RPC (Requirement 8, P6c-M01)."""
    return x if isinstance(x, dict) else {}


def as_str(x: any) -> str:
    """Helper đảm bảo trả về str khi nhận dữ liệu JSON-RPC (Requirement 8, P6c-M01)."""
    return x if isinstance(x, str) else ""

ACP_FIXED_PROMPT_PREFIX = (
    "LUẬT CỨNG BẮT BUỘC:\n"
    "1. Cấm chạy các lệnh: git push (mọi biến thể), send-email, remote đổi đích; git config ghi; git ngoài phạm vi repo/worktree. Khi không dùng worktree cấm: reset --hard, clean, stash, restore, checkout/switch đổi nhánh, commit --amend. Message commit chỉ mô tả thay đổi, không thêm thông tin công cụ AI hay Co-Authored-By.\n"
    "2. Tuyệt đối không đọc, in hay commit file bí mật (.env*, token, khóa, mật khẩu).\n"
    "3. Tuân thủ toàn bộ quy định trong AGENTS.md.\n"
    "4. Chỉ ghi vào đường dẫn được cho phép (--allow-write).\n"
    "5. Chỉ dừng hỏi khi thiếu dữ kiện nghiệp vụ, không phải khi bị từ chối một lệnh. Không tự ý suy đoán.\n"
    "6. Đọc/tìm file thì ưu tiên công cụ tích hợp (view_file, list_dir, grep_search, find_by_name), KHÔNG cần quyền lệnh; chỉ dùng shell khi bắt buộc.\n"
    "7. Nếu một lệnh shell bị từ chối: KHÔNG dừng. Dùng công cụ tích hợp hoặc cách khác để vẫn hoàn thành việc; chỉ dừng khi việc bắt buộc thực sự không làm được, và khi đó nêu rõ lệnh nào gây ra.\n\n"
    "TASK BRIEF:\n"
)
FIXED_PROMPT_PREFIX = ACP_FIXED_PROMPT_PREFIX

FORBIDDEN_READ_PATTERNS = [
    ".env*",
    "*.pem",
    "*.key",
    "id_rsa*",
    "*credentials*",
    "*secret*",
    ".git/config",
]

GIT_MAIN_BRANCHES = {"main", "master", "develop"}


def is_secret_file_name(name_or_path: str) -> bool:
    norm = name_or_path.replace("\\", "/").strip().lower()
    name = Path(norm).name
    if norm.startswith("~/.ssh") or norm.startswith("~/.netrc") or norm.startswith("~/.aws"):
        return True
    if "$home/.ssh" in norm or "$home/.netrc" in norm or "$home/.aws" in norm:
        return True
    if norm == ".git/config" or norm.endswith("/.git/config"):
        return True
    if name.startswith(".env") or name == ".env" or name.startswith(".e*"):
        return True
    if name.startswith("id_rsa"):
        return True
    if name.endswith(".pem") or name.endswith(".key") or name.endswith("*.k*"):
        return True
    if "credential" in name or "secret" in name:
        return True
    return False


def extract_inner_subcommands(text: str) -> list[str]:
    subcmds = []
    for m in re.finditer(r"\$\((.+?)\)", text):
        subcmds.append(m.group(1).strip())
    for m in re.finditer(r"<\((.+?)\)", text):
        subcmds.append(m.group(1).strip())
    for m in re.finditer(r">\((.+?)\)", text):
        subcmds.append(m.group(1).strip())
    for m in re.finditer(r"`(.+?)`", text):
        subcmds.append(m.group(1).strip())
    return subcmds


def sanitize_outer_subcommands(text: str) -> str:
    s = re.sub(r"\$\((.+?)\)", " DUMMY_ARG ", text)
    s = re.sub(r"<\((.+?)\)", " DUMMY_ARG ", s)
    s = re.sub(r">\((.+?)\)", " DUMMY_ARG ", s)
    s = re.sub(r"`(.+?)`", " DUMMY_ARG ", s)
    return s


PIPED_OR_CHAINED_SHELL_COMMANDS = {
    "sh",
    "bash",
    "zsh",
    "dash",
    "eval",
    "source",
    ".",
    "xargs",
}


def extract_cmd_name(argv: list[str]) -> tuple[str, list[str]]:
    """
    Rút trích tên lệnh thực thi từ argv:
    - Bỏ qua ./ ở đầu
    - Xử lý env (kể cả cờ -i, -u, -S, VAR=val)
    - Trả về (base_name, remaining_args)
    - Với lệnh '.' (dot/source) trả về ('.', remaining_args)
    """
    if not argv:
        return "", []

    idx = 0
    cmd_raw = argv[idx]
    if cmd_raw.startswith("./"):
        cmd_raw = cmd_raw[2:]
    cmd_base = Path(cmd_raw).name.lower()

    if cmd_base == "env":
        idx += 1
        while idx < len(argv):
            arg = argv[idx]
            if arg in ("-u", "--unset"):
                idx += 2
                continue
            if arg.startswith("-u"):
                idx += 1
                continue
            if arg in ("-i", "--ignore-environment", "-0", "--null", "-v", "--verbose"):
                idx += 1
                continue
            if arg == "-S" or arg.startswith("-S"):
                idx += 1
                continue
            if arg.startswith("-"):
                idx += 1
                continue
            if "=" in arg and not arg.startswith("="):
                # FOO=bar
                idx += 1
                continue
            break
        if idx >= len(argv):
            return "env", []
        cmd_raw = argv[idx]
        if cmd_raw.startswith("./"):
            cmd_raw = cmd_raw[2:]
        if cmd_raw == ".":
            return ".", argv[idx + 1:]
        return Path(cmd_raw).name.lower(), argv[idx + 1:]

    if cmd_raw == ".":
        return ".", argv[1:]
    return Path(cmd_raw).name.lower(), argv[1:]


def check_single_segment_argv(
    argv: list[str],
    effective_dir: Path,
    is_worktree: bool = False,
    allow_cmd: list[str] | None = None,
    raw_seg_str: str = "",
) -> tuple[bool, str]:
    if not argv:
        return True, ""

    base_name, remaining_args = extract_cmd_name(argv)
    effective_argv = [base_name] + remaining_args

    # 1. HỦY DIỆT / HỆ THỐNG / MẠNG (HARD-DENY)
    if base_name == "rm":
        for a in effective_argv[1:]:
            if a.startswith("-"):
                if re.search(r"^-(?:[a-zA-Z]*[rfRF][a-zA-Z]*|-[a-zA-Z-]*(?:recursive|force))$", a):
                    return False, f"Lệnh cấm: rm với cờ hủy diệt {a}"

    if base_name in ("rmdir", "shred", "dd", "mkfs"):
        return False, f"Lệnh cấm: {base_name}"

    if base_name in ("sudo", "su"):
        return False, f"Lệnh cấm đặc quyền: {base_name}"

    if base_name == "chmod":
        for a in effective_argv[1:]:
            if a == "-R" or a.startswith("-R") or (a.startswith("-") and not a.startswith("--") and "R" in a) or a == "--recursive":
                return False, "Lệnh cấm: chmod -R"

    if base_name == "chown":
        return False, "Lệnh cấm: chown"

    if base_name in ("kill", "pkill"):
        return False, f"Lệnh cấm: {base_name}"

    if base_name in ("curl", "wget", "nc", "ssh", "scp", "ftp"):
        return False, f"Lệnh cấm mạng: {base_name}"

    if base_name in ("brew", "docker", "kubectl"):
        return False, f"Lệnh cấm hệ thống: {base_name}"

    if base_name in ("eval", "exec", "source", "."):
        return False, f"Lệnh cấm shell: {base_name}"

    if base_name in ("bash", "sh", "zsh", "dash"):
        for a in effective_argv[1:]:
            if a == "-c" or a.startswith("-c"):
                return False, f"Lệnh cấm shell: {base_name} -c"

    if base_name == "xargs":
        return False, "Lệnh cấm: xargs"

    if "--dangerously-skip-permissions" in argv or "--dangerously-skip-permissions" in effective_argv:
        return False, "Cờ cấm: --dangerously-skip-permissions"

    # Soft-deny: npm / pip install (cho phép qua allow_cmd)
    if base_name == "npm" and any(a.lower() in ("install", "i", "ci") for a in argv[1:]):
        if not (allow_cmd and any(re.search(pat, raw_seg_str) for pat in allow_cmd)):
            return False, "Lệnh cấm: npm install (chỉ cho phép khi có trong --allow-cmd)"

    if base_name in ("pip", "pip3") and any(a.lower() in ("install",) for a in argv[1:]):
        if not (allow_cmd and any(re.search(pat, raw_seg_str) for pat in allow_cmd)):
            return False, f"Lệnh cấm: {base_name} install (chỉ cho phép khi có trong --allow-cmd)"

    # Python -c và script trong repo
    if base_name in ("python", "python3") or base_name.startswith("python3.") or base_name.startswith("python2"):
        for a in argv[1:]:
            if a == "-c" or a.startswith("-c") or (a.startswith("-") and not a.startswith("--") and "c" in a):
                return False, "Lệnh cấm: python -c"
        if not any(a == "-m" for a in argv[1:]):
            script_args = [a for a in argv[1:] if not a.startswith("-")]
            if script_args:
                script_path = script_args[0]
                if script_path.startswith("/") or ".." in Path(script_path).parts or ".." in script_path:
                    return False, f"python3 chỉ chấp nhận script trong repo với đường dẫn tương đối sạch: {script_path}"

    # Node -e / --eval và script file
    if base_name == "node" or base_name.startswith("node"):
        for a in argv[1:]:
            if a == "-e" or a.startswith("-e") or a.startswith("--eval") or (a.startswith("-") and not a.startswith("--") and "e" in a):
                return False, "Lệnh cấm: node -e / --eval"
        script_args = [a for a in argv[1:] if not a.startswith("-")]
        if script_args:
            script_path = script_args[0]
            if script_path.startswith("/") or ".." in Path(script_path).parts or ".." in script_path:
                return False, f"node chỉ chấp nhận script trong repo với đường dẫn tương đối sạch: {script_path}"

    # Find -delete / -exec / -ok / -fprint / -fls
    if base_name == "find":
        for a in argv[1:]:
            if (
                a in ("-delete", "-exec", "-execdir", "-ok")
                or a.startswith("-exec")
                or a.startswith("-fprint")
                or a.startswith("-fls")
            ):
                return False, f"Lệnh cấm: find với cờ {a}"

    # Sed -i / --in-place / 1e
    if base_name == "sed":
        for a in argv[1:]:
            if a == "-i" or a.startswith("-i") or a == "--in-place" or a.startswith("--in-place"):
                return False, "Lệnh cấm: sed -i / --in-place"
            if re.search(r"^\d*e\b", a) or a == "e":
                return False, "Lệnh cấm: sed e command"

    # Awk system / getline
    if base_name == "awk":
        for a in argv[1:]:
            if "system(" in a or "system (" in a:
                return False, "Lệnh cấm: awk với system() gọi shell ngoài"
            if "getline" in a:
                return False, "Lệnh cấm: awk với getline"

    # Đọc file bí mật qua lệnh đọc: cat, head, tail, rg, grep, sed, awk
    if base_name in ("cat", "head", "tail", "rg", "grep", "sed", "awk"):
        for a in argv[1:]:
            if a.startswith("-"):
                if a == "--files":
                    continue
                continue
            if is_secret_file_name(a):
                return False, f"Từ chối đọc file bí mật / nhạy cảm: {a}"
            if a.startswith("/") or a.startswith(".."):
                try:
                    p = Path(a)
                    if p.is_absolute():
                        p_res = p.resolve()
                    else:
                        p_res = (effective_dir / p).resolve()
                    if not p_res.is_relative_to(effective_dir.resolve()):
                        return False, f"Từ chối đọc đường dẫn ngoài phạm vi làm việc: {a}"
                except Exception:
                    pass

    # 2. GIT COMMANDS
    if base_name == "git":
        idx = 1
        subcmd = ""
        while idx < len(argv):
            arg = argv[idx]
            arg_l = arg.lower()
            if arg == "-c" or arg.startswith("-c"):
                return False, f"Lệnh cấm: git {arg}"
            if arg_l.startswith("--exec-path") or arg_l.startswith("--git-dir") or arg_l.startswith("--work-tree") or arg_l.startswith("--namespace") or arg_l.startswith("--config-env"):
                return False, f"Lệnh cấm: git {arg}"
            if arg == "-C":
                idx += 1
                if idx < len(argv):
                    target_dir = argv[idx]
                    p = Path(target_dir)
                    if not p.is_absolute():
                        p = (effective_dir / p).resolve()
                    else:
                        p = p.resolve()
                    try:
                        if not p.is_relative_to(effective_dir.resolve()):
                            return False, f"Lệnh cấm: git -C trỏ ngoài phạm vi làm việc: {target_dir}"
                    except Exception:
                        return False, f"Lệnh cấm: git -C trỏ ngoài phạm vi làm việc: {target_dir}"
                idx += 1
                continue
            if arg.startswith("-C"):
                target_dir = arg[2:]
                if target_dir.startswith("="):
                    target_dir = target_dir[1:]
                p = Path(target_dir)
                if not p.is_absolute():
                    p = (effective_dir / p).resolve()
                else:
                    p = p.resolve()
                try:
                    if not p.is_relative_to(effective_dir.resolve()):
                        return False, f"Lệnh cấm: git -C trỏ ngoài phạm vi làm việc: {target_dir}"
                except Exception:
                    return False, f"Lệnh cấm: git -C trỏ ngoài phạm vi làm việc: {target_dir}"
                idx += 1
                continue
            if arg.startswith("-"):
                idx += 1
                continue
            subcmd = arg_l
            break

        if not subcmd:
            return True, "git command"

        subcmd_args = argv[idx + 1:]

        if "--no-verify" in subcmd_args or "-n" in subcmd_args:
            if subcmd == "commit" and "-n" in subcmd_args:
                return False, "Lệnh cấm: git commit --no-verify (-n)"
            if "--no-verify" in subcmd_args:
                return False, "Lệnh cấm: git --no-verify"

        if subcmd in ("show", "cat-file", "diff", "log"):
            for a in subcmd_args:
                if a.startswith("--output="):
                    out_target = a.split("=", 1)[1].strip("'\"")
                    if out_target.startswith("/") or ".." in out_target:
                        try:
                            p = Path(out_target)
                            p_res = p.resolve() if p.is_absolute() else (effective_dir / p).resolve()
                            if not p_res.is_relative_to(effective_dir.resolve()):
                                return False, f"Lệnh cấm: git {subcmd} --output trỏ ngoài phạm vi làm việc: {out_target}"
                        except Exception:
                            return False, f"Lệnh cấm: git {subcmd} --output trỏ ngoài phạm vi làm việc: {out_target}"
                elif a == "-o" or a.startswith("-o"):
                    pass
                if ":" in a:
                    _, path_part = a.split(":", 1)
                    if is_secret_file_name(path_part):
                        return False, f"Từ chối đọc file bí mật qua git {subcmd}: {a}"
                elif is_secret_file_name(a):
                    return False, f"Từ chối đọc file bí mật qua git {subcmd}: {a}"

        # Group 1: git ĐẨY (PUSH / REMOTE WRITE / CONFIG WRITE) - CẤM Ở MỌI CHẾ ĐỘ
        if subcmd == "push":
            return False, "Lệnh cấm: git push (mọi biến thể)"

        if subcmd == "send-email":
            return False, "Lệnh cấm: git send-email"

        if subcmd == "remote":
            for a in subcmd_args:
                if a.lower() in ("add", "set-url", "remove", "rm", "rename"):
                    return False, f"Lệnh cấm: git remote {a}"

        if subcmd == "config":
            for a in subcmd_args:
                if a.lower() in ("--global", "--system", "--add", "--unset", "--unset-all"):
                    return False, f"Lệnh cấm: git config {a}"
            non_flags = [a for a in subcmd_args if not a.startswith("-")]
            if len(non_flags) >= 2:
                return False, "Lệnh cấm: git config ghi giá trị"

        if subcmd == "branch":
            has_del_or_force = any(re.search(r"^-(?:[a-zA-Z]*[dDmMcCfF][a-zA-Z]*|-[a-zA-Z-]*(?:delete|move|copy|force))$", a) for a in subcmd_args)
            if has_del_or_force:
                for a in subcmd_args:
                    if not a.startswith("-"):
                        branch_name = a.lower()
                        if branch_name in GIT_MAIN_BRANCHES or branch_name.startswith("release/"):
                            return False, f"Lệnh cấm: không được xóa hoặc đổi tên nhánh chính: {a}"

        # Group 2: git LẤY VỀ (FETCH / PULL / CLONE / LS-REMOTE)
        if subcmd == "fetch":
            return True, "git fetch được phép"

        if subcmd == "ls-remote":
            return True, "git ls-remote được phép"

        if subcmd == "submodule":
            return True, "git submodule được phép"

        if subcmd == "clone":
            non_flags = [a for a in subcmd_args if not a.startswith("-")]
            if len(non_flags) >= 2:
                dest_dir = non_flags[1]
                p = Path(dest_dir)
                if not p.is_absolute():
                    p = (effective_dir / p).resolve()
                else:
                    p = p.resolve()
                try:
                    if not p.is_relative_to(effective_dir.resolve()):
                        return False, f"Lệnh cấm: git clone ra ngoài phạm vi làm việc: {dest_dir}"
                except Exception:
                    return False, f"Lệnh cấm: git clone ra ngoài phạm vi làm việc: {dest_dir}"
            return True, "git clone được phép"

        if subcmd == "pull":
            if is_worktree:
                return True, "git pull trong worktree được phép"
            else:
                if "--ff-only" in subcmd_args:
                    return True, "git pull --ff-only được phép"
                else:
                    return False, "Khi không dùng worktree, git pull chỉ được phép khi có --ff-only. Gợi ý: dùng git fetch rồi git merge --ff-only."

        # Group 3: git GHI CỤC BỘ
        if not is_worktree:
            if subcmd == "reset" and any(a == "--hard" for a in subcmd_args):
                return False, "Khi không dùng worktree, cấm git reset --hard"
            if subcmd == "clean":
                return False, "Khi không dùng worktree, cấm git clean"
            if subcmd == "checkout":
                if "--" in subcmd_args or "." in subcmd_args:
                    return False, "Khi không dùng worktree, cấm git checkout -- / git checkout ."
                non_flags = [a for a in subcmd_args if not a.startswith("-")]
                if non_flags:
                    return False, f"Khi không dùng worktree, cấm git checkout đổi nhánh: {non_flags[0]}"
            if subcmd == "switch":
                return False, "Khi không dùng worktree, cấm git switch đổi nhánh"
            if subcmd == "restore":
                return False, "Khi không dùng worktree, cấm git restore"
            if subcmd == "stash":
                if any(a.lower() in ("list", "show") for a in subcmd_args):
                    return True, "git stash list/show được phép"
                return False, "Khi không dùng worktree, cấm git stash"
            if subcmd == "add":
                if any(a in ("-A", "--all", ".", "-f", "--force", "-u", "--update") for a in subcmd_args):
                    return False, "Khi không dùng worktree, cấm git add -A/--all/./-f/-u (phải add từng đường dẫn cụ thể)"
            if subcmd == "commit" and any(a == "--amend" for a in subcmd_args):
                return False, "Khi không dùng worktree, cấm git commit --amend"
            if subcmd == "rebase":
                return False, "Khi không dùng worktree, cấm git rebase"
            if subcmd == "branch":
                has_del = any(re.search(r"^-(?:[a-zA-Z]*[dDmMcCfF][a-zA-Z]*|-[a-zA-Z-]*(?:delete|move|copy|force))$", a) for a in subcmd_args)
                if has_del:
                    return False, "Khi không dùng worktree, cấm git branch xóa/đổi tên"

        return True, f"git {subcmd} được phép"

    return True, f"Lệnh được phép mặc định: {base_name}"


def check_command_permission(
    cmd_str: str,
    allow_cmd: list[str] | None,
    effective_dir: Path,
    is_worktree: bool = False,
) -> tuple[bool, bool, str]:
    clean_cmd = cmd_str.strip()
    if not clean_cmd:
        return False, False, "Lệnh rỗng"

    if "\x00" in cmd_str:
        return False, False, "Chứa ký tự null byte không an toàn"

    if any(ord(c) < 32 and c not in "\t\n\r" for c in cmd_str):
        return False, False, "Chứa ký tự điều khiển không in được"

    if any(c in cmd_str for c in ("\u00a0", "—", "–")):
        return False, False, "Chứa ký tự unicode lạ (khoảng trắng giả hoặc gạch ngang)"

    if re.search(r"[a-zA-Z0-9_-]''[a-zA-Z0-9_-]|''|\"\"|[a-zA-Z0-9_-]\"\"[a-zA-Z0-9_-]", clean_cmd):
        return False, False, f"Chứa chuỗi nháy rỗng hoặc nối nháy liền kề: {clean_cmd}"

    if re.search(r"-['\"][a-zA-Z]", clean_cmd):
        return False, False, f"Nháy làm thay đổi token cờ: {clean_cmd}"

    # 1. Trích xuất và kiểm tra các lệnh con trong $(...), <(...), >(...), `...`
    inner_cmds = extract_inner_subcommands(clean_cmd)
    for ic in inner_cmds:
        allowed, _, reason = check_command_permission(
            ic, allow_cmd=allow_cmd, effective_dir=effective_dir, is_worktree=is_worktree
        )
        if not allowed:
            return False, False, f"Lệnh con trong subshell bị từ chối: {reason}"

    sanitized_cmd = sanitize_outer_subcommands(clean_cmd)

    # 2. Tách đoạn theo compound operators: &&, ||, |, ;, &, \n, \r
    placeholder = "___FD_REDIR_2GT1___"
    masked = re.sub(r"2>&1", placeholder, sanitized_cmd)
    split_pattern = r"(&&|\|\||[|;&\n\r])"
    tokens = re.split(split_pattern, masked)

    segments_with_op: list[tuple[str | None, str]] = []
    current_op = None
    for tok in tokens:
        if re.fullmatch(split_pattern, tok):
            current_op = tok.strip() or tok
        else:
            seg_str = tok.strip()
            if seg_str:
                segments_with_op.append((current_op, seg_str))
                current_op = None

    if not segments_with_op:
        return False, False, "Lệnh rỗng"

    for op, raw_seg in segments_with_op:
        seg = raw_seg.replace(placeholder, "2>&1")

        # 3. Kiểm tra chuyển hướng >, >>, tee ra ngoài scope
        clean_seg_for_redir = re.sub(r"(?:1|2|&)?\s*>{1,2}\s*/dev/null", " ", seg)
        clean_seg_for_redir = re.sub(r"<\s*/dev/null", " ", clean_seg_for_redir)
        clean_seg_for_redir = re.sub(r"2>&1", " ", clean_seg_for_redir)

        redir_matches = re.findall(r"(?:1|2|&)?\s*>{1,2}\s*(\S+)", clean_seg_for_redir)
        for target in redir_matches:
            target_clean = target.strip("'\"")
            if target_clean == "/dev/null":
                continue
            if target_clean.startswith("/") or ".." in target_clean:
                try:
                    p = Path(target_clean)
                    if p.is_absolute():
                        p_res = p.resolve()
                    else:
                        p_res = (effective_dir / p).resolve()
                    if not p_res.is_relative_to(effective_dir.resolve()):
                        return False, False, f"Chuyển hướng ghi ra ngoài phạm vi làm việc: > {target}"
                except Exception:
                    return False, False, f"Chuyển hướng ghi ra ngoài phạm vi làm việc: > {target}"

        clean_seg = re.sub(r"(?:1|2|&)?\s*>{1,2}\s*\S+", " ", seg)
        clean_seg = re.sub(r"<\s*\S+", " ", clean_seg)
        clean_seg = re.sub(r"2>&1", " ", clean_seg).strip()
        if not clean_seg:
            continue

        try:
            argv = shlex.split(clean_seg)
        except ValueError as exc:
            return False, False, f"Lỗi cú pháp lệnh: {exc}"

        if not argv:
            continue

        # Việc 1: Chặn khi một đoạn sau | (hoặc &&, ;) có lệnh đầu là sh, bash, zsh, dash, eval, source, ., xargs
        if op in ("|", "&&", ";", "||", "&", "\n", "\r"):
            cmd_name, _ = extract_cmd_name(argv)
            if cmd_name in PIPED_OR_CHAINED_SHELL_COMMANDS:
                return False, False, f"Lệnh cấm: thực thi vỏ bọc shell/eval/xargs sau '{op}': {cmd_name}"

        if argv[0].lower() == "tee":
            for a in argv[1:]:
                if not a.startswith("-"):
                    if a.startswith("/") or ".." in a:
                        try:
                            p = Path(a)
                            p_res = p.resolve() if p.is_absolute() else (effective_dir / p).resolve()
                            if not p_res.is_relative_to(effective_dir.resolve()):
                                return False, False, f"Lệnh tee ghi ra ngoài phạm vi làm việc: {a}"
                        except Exception:
                            return False, False, f"Lệnh tee ghi ra ngoài phạm vi làm việc: {a}"

        if argv[0].startswith("\\"):
            argv[0] = argv[0][1:]

        allowed, reason = check_single_segment_argv(
            argv=argv,
            effective_dir=effective_dir,
            is_worktree=is_worktree,
            allow_cmd=allow_cmd,
            raw_seg_str=seg,
        )
        if not allowed:
            return False, False, reason

    return True, False, "Lệnh được phép"


def check_file_permission(
    path_str: str,
    effective_dir: Path,
    effective_allow_write: list[str] | None,
) -> tuple[bool, str]:
    """
    Kiểm tra quyền ghi/sửa file (P6f-C02):
    Cho phép nếu nằm trong hoặc bằng một đường dẫn trong effective_allow_write.
    Từ chối symlink file, symlink thư mục trung gian, đường dẫn chứa .., và đường dẫn ngoài phạm vi.
    """
    if not path_str or not path_str.strip():
        return False, "Từ chối ghi file: đường dẫn rỗng"

    if not effective_allow_write:
        return False, f"Từ chối ghi file: danh sách allow-write rỗng ({path_str})"

    p_str = path_str.strip()
    p = Path(p_str)
    if ".." in p.parts:
        return False, f"Từ chối ghi qua đường dẫn chứa ..: {path_str}"

    eff_resolved = effective_dir.resolve()
    if not p.is_absolute():
        p_raw = eff_resolved / p
    else:
        p_raw = p

    # 1. Từ chối nếu file đã là symlink
    if p_raw.is_symlink():
        return False, f"Từ chối ghi vào file là symlink: {path_str}"

    # 2. Kiểm tra mọi thư mục trung gian của đường dẫn gốc chưa resolve (P6f-C02)
    curr = eff_resolved
    for part in p.parent.parts:
        if part in (".", "", "/"):
            continue
        curr = curr / part
        if curr.is_symlink():
            return False, f"Từ chối ghi qua symlink thư mục trung gian: {path_str} (tại {curr})"

    try:
        p_resolved = p_raw.resolve()
    except Exception:
        return False, f"Đường dẫn không hợp lệ: {path_str}"

    try:
        if not p_resolved.is_relative_to(eff_resolved):
            return False, f"Từ chối ghi ngoài phạm vi làm việc: {path_str}"
    except (ValueError, AttributeError):
        return False, f"Từ chối ghi ngoài phạm vi làm việc: {path_str}"

    # 3. Lọc effective_allow_write: bỏ qua symlink hoặc resolve ra ngoài/bằng gốc repo
    valid_allowed: list[Path] = []
    for allowed in effective_allow_write:
        a_path = Path(allowed)
        if not a_path.is_absolute():
            a_raw = eff_resolved / a_path
        else:
            a_raw = a_path

        if a_raw.is_symlink():
            continue
        curr_a = eff_resolved
        has_sym_a = False
        for part in a_path.parent.parts:
            if part in (".", "", "/"):
                continue
            curr_a = curr_a / part
            if curr_a.is_symlink():
                has_sym_a = True
                break
        if has_sym_a:
            continue
        try:
            a_resolved = a_raw.resolve()
            if a_resolved == eff_resolved:
                continue
            if not a_resolved.is_relative_to(eff_resolved):
                continue
            valid_allowed.append(a_resolved)
        except Exception:
            continue

    if not valid_allowed:
        return False, f"Danh sách allow-write không có mục hợp lệ nào ({path_str})"

    for a_resolved in valid_allowed:
        if p_resolved == a_resolved:
            return True, f"Khớp chính xác allow-write: {path_str}"
        try:
            if p_resolved.is_relative_to(a_resolved):
                return True, f"Nằm trong thư mục allow-write: {path_str}"
        except (ValueError, AttributeError):
            pass

    return False, f"Nằm ngoài phạm vi allow-write: {path_str}"


def check_read_permission(path_str: str, effective_dir: Path) -> tuple[bool, str]:
    """Kiểm tra quyền đọc file (kind == 'read') (P6f-C02).
    Từ chối đường dẫn rỗng, kiểm tra .. và tên bí mật trước và sau resolve,
    từ chối symlink thư mục trung gian, và từ chối ngoài effective_dir.
    """
    if not path_str or not path_str.strip():
        return False, "Từ chối đọc file: đường dẫn rỗng"

    p_str = path_str.strip()
    p = Path(p_str)
    if ".." in p.parts:
        return False, f"Từ chối đọc qua đường dẫn chứa ..: {path_str}"

    if is_secret_file_name(p_str):
        return False, f"Từ chối đọc file bí mật / nhạy cảm: {path_str}"

    eff_resolved = effective_dir.resolve()

    if not p.is_absolute():
        p_raw = eff_resolved / p
    else:
        p_raw = p

    # Kiểm tra symlink trung gian
    curr = eff_resolved
    for part in p.parent.parts:
        if part in (".", "", "/"):
            continue
        curr = curr / part
        if curr.is_symlink():
            return False, f"Từ chối đọc qua symlink thư mục trung gian: {path_str} (tại {curr})"

    try:
        p_resolved = p_raw.resolve()
    except Exception:
        return False, f"Đường dẫn không hợp lệ: {path_str}"

    try:
        if not p_resolved.is_relative_to(eff_resolved):
            return False, f"Từ chối đọc file nằm ngoài thư mục làm việc: {path_str}"
    except (ValueError, AttributeError):
        return False, f"Từ chối đọc file nằm ngoài thư mục làm việc: {path_str}"

    for check_p in (p, p_raw, p_resolved):
        if is_secret_file_name(str(check_p)):
            return False, f"Từ chối đọc file bí mật / nhạy cảm: {path_str}"

    return True, "Read action allowed"


def extract_permission_info(params: dict) -> tuple[str, str, str, str]:
    """Rút trích (kind, tool_name, path_str, cmd_str) từ params của session/request_permission."""
    tool_call = as_dict(params.get("toolCall"))
    kind = as_str(tool_call.get("kind"))
    tool_name = as_str(tool_call.get("name"))
    args_map = as_dict(tool_call.get("args"))
    locs = tool_call.get("locations")
    loc_path = ""
    if isinstance(locs, list) and locs and isinstance(locs[0], dict):
        loc_path = as_str(locs[0].get("path"))

    path_str = (
        as_str(args_map.get("Path"))
        or as_str(args_map.get("path"))
        or as_str(args_map.get("file_path"))
        or as_str(args_map.get("dir"))
        or as_str(args_map.get("DirectoryPath"))
        or as_str(args_map.get("SearchPath"))
        or as_str(args_map.get("TargetFile"))
        or as_str(args_map.get("AbsolutePath"))
        or as_str(args_map.get("loc_path"))
        or loc_path
        or ""
    )
    cmd_str = (
        as_str(args_map.get("CommandLine"))
        or as_str(args_map.get("command"))
        or as_str(args_map.get("cmd"))
        or ""
    )
    return kind, tool_name, path_str, cmd_str


def dispatch_request_permission(
    params: dict,
    effective_dir: Path,
    effective_allow_write: list[str] | None,
    allow_cmd: list[str] | None,
    is_worktree: bool = False,
) -> tuple[bool, bool, str, str, str, str]:
    """
    Xử lý điều hướng quyền cho session/request_permission.
    Trả về: (allowed, is_needs_human, reason, target, perm_kind, tool_name)
    """
    kind, tool_name, path_str, cmd_str = extract_permission_info(params)
    tool_call = as_dict(params.get("toolCall"))
    args_map = as_dict(tool_call.get("args"))

    if kind == "edit" or tool_name in ("write_file", "edit_file"):
        target = path_str
        allowed, reason = check_file_permission(
            path_str=path_str,
            effective_dir=effective_dir,
            effective_allow_write=effective_allow_write,
        )
        return allowed, False, reason, target, "edit", tool_name
    elif kind == "execute" or tool_name == "run_command" or cmd_str:
        target = cmd_str
        allowed, is_needs_human, reason = check_command_permission(
            cmd_str=cmd_str,
            allow_cmd=allow_cmd,
            effective_dir=effective_dir,
            is_worktree=is_worktree,
        )
        return allowed, is_needs_human, reason, target, "execute", tool_name
    elif kind == "read" or tool_name in ("read_file", "list_dir", "view_file") or path_str:
        target = path_str or str(args_map)
        allowed, reason = check_read_permission(
            path_str=path_str,
            effective_dir=effective_dir,
        )
        return allowed, False, reason, target, "read", tool_name
    else:
        target = f"{tool_name}: {args_map}"
        reason = f"Công cụ được phép mặc định: {tool_name}"
        return True, False, reason, target, kind or tool_name, tool_name


def apply_worktree_changes(
    wt_dir: Path,
    repo_dir: Path,
    changed_files: list[str],
    allowed_resolved: list[Path],
) -> int:
    """Sao chép thay đổi hợp lệ từ worktree về repo gốc (--apply)."""
    applied = 0
    for f in changed_files:
        if is_ignored_cache_file(f):
            continue
        src_f = wt_dir / f
        dst_f = repo_dir / f
        if src_f.is_file() and not src_f.is_symlink():
            dst_f.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_f, dst_f, follow_symlinks=False)
            applied += 1
        elif not src_f.exists() and dst_f.exists():
            if dst_f.is_file() and not dst_f.is_symlink():
                dst_f.unlink()
                applied += 1
    return applied


class ACPController:
    """Điều khiển tiến trình `agy acp --sandbox` qua JSON-RPC stdio."""

    def __init__(self, agy_bin: str, cwd: Path, timeout: float = 1800.0):
        self.agy_bin = agy_bin
        self.cwd = cwd
        self.timeout = timeout
        self.proc: subprocess.Popen | None = None
        self.msg_queue: queue.Queue = queue.Queue()
        self.stderr_lines: list[str] = []
        self.req_id_counter = 0
        self.reader_thread: threading.Thread | None = None
        self.err_thread: threading.Thread | None = None

    def start(self):
        cmd = [sys.executable, "-u", self.agy_bin] if self.agy_bin.endswith(".py") else [self.agy_bin]
        cmd.extend(["acp", "--sandbox"])
        popen_kwargs = {
            "cwd": str(self.cwd),
            "stdin": subprocess.PIPE,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
            "bufsize": 1,
        }
        if sys.platform != "win32":
            popen_kwargs["start_new_session"] = True
        self.proc = subprocess.Popen(
            cmd,
            **popen_kwargs,
        )
        self.reader_thread = threading.Thread(target=self._stdout_worker, daemon=True)
        self.err_thread = threading.Thread(target=self._stderr_worker, daemon=True)
        self.reader_thread.start()
        self.err_thread.start()

    def _stdout_worker(self):
        try:
            if not self.proc or not self.proc.stdout:
                return
            for line in iter(self.proc.stdout.readline, ""):
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    data = json.loads(line_str)
                    if data is not None and isinstance(data, dict):
                        self.msg_queue.put(data)
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            self.msg_queue.put(None)

    def _stderr_worker(self):
        try:
            if not self.proc or not self.proc.stderr:
                return
            for line in iter(self.proc.stderr.readline, ""):
                self.stderr_lines.append(line)
        except Exception:
            pass

    def next_id(self) -> int:
        self.req_id_counter += 1
        return self.req_id_counter

    def send_raw(self, obj: dict):
        if not self.proc or not self.proc.stdin:
            return
        line = json.dumps(obj, ensure_ascii=False)
        try:
            self.proc.stdin.write(line + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

    def send_request(self, method: str, params: dict | None = None) -> int:
        rid = self.next_id()
        msg = {"jsonrpc": "2.0", "id": rid, "method": method}
        if params is not None:
            msg["params"] = params
        self.send_raw(msg)
        return rid

    def send_response(self, req_id, result: dict):
        msg = {"jsonrpc": "2.0", "id": req_id, "result": result}
        self.send_raw(msg)

    def read_message(self, timeout: float | None = None):
        try:
            return self.msg_queue.get(timeout=timeout)
        except queue.Empty:
            return "TIMEOUT"

    def close(self):
        if self.proc:
            try:
                if hasattr(os, "getpgid") and hasattr(signal, "SIGTERM"):
                    pgid = os.getpgid(self.proc.pid)
                    os.killpg(pgid, signal.SIGTERM)
                else:
                    self.proc.terminate()
            except Exception:
                try:
                    self.proc.terminate()
                except Exception:
                    pass
            try:
                self.proc.wait(timeout=3)
            except Exception:
                try:
                    if hasattr(os, "getpgid") and hasattr(signal, "SIGKILL"):
                        pgid = os.getpgid(self.proc.pid)
                        os.killpg(pgid, signal.SIGKILL)
                    else:
                        self.proc.kill()
                except Exception:
                    try:
                        self.proc.kill()
                    except Exception:
                        pass
                try:
                    self.proc.wait(timeout=2)
                except Exception:
                    pass
            self.proc = None



def find_matching_quota_keyword(text: str) -> str | None:
    t = text.lower()
    for kw in QUOTA_KEYWORDS:
        if kw == "429":
            if re.search(r"\b429\b", t):
                return kw
        else:
            if kw in t:
                return kw
    return None


def detect_error_and_suspected_quota(
    prompt_result: dict | None,
    prompt_error: any,
    stderr_acc: str,
    response_text: str,
    timed_out: bool,
    timeout_val: float,
    stop_reason: str = "",
) -> dict | None:
    """
    Phát hiện lỗi phiên và nghi quota, lưu nguyên văn lỗi (cắt tối đa 2000 ký tự)
    và nguồn phát hiện (trường nào, sự kiện nào, từ khóa khớp).
    QUÉT TỪ KHÓA QUOTA CHỈ TRÊN TRƯỜNG LỖI / STDERR / JSON-RPC ERROR,
    KHÔNG quét trên response_text của lượt end_turn thành công.
    """
    # 1. Ưu tiên kiểm tra timeout đầu tiên (P6e-M02)
    if timed_out:
        return {
            "raw_message": f"Phiên làm việc vượt quá thời gian tối đa {timeout_val}s",
            "source_field": "timeout",
            "source_event": "session/prompt (timeout)",
            "matched_keyword": None,
            "is_suspected_quota": False,
        }

    if prompt_error:
        if isinstance(prompt_error, (dict, list)):
            raw = json.dumps(prompt_error, ensure_ascii=False)
        else:
            raw = str(prompt_error)
        raw_cut = raw[:2000]
        kw = find_matching_quota_keyword(raw)
        return {
            "raw_message": raw_cut,
            "source_field": "prompt_result['error']",
            "source_event": "session/prompt (JSON-RPC error)",
            "matched_keyword": kw,
            "is_suspected_quota": kw is not None,
        }

    is_successful_end_turn = (
        stop_reason == "end_turn"
        and not timed_out
        and not prompt_error
        and (prompt_result is not None)
    )

    # Chỉ xét stderr khi lượt lỗi / không có kết quả (Requirement 10, P6c-M03)
    if not is_successful_end_turn and stderr_acc.strip():
        raw_cut = stderr_acc.strip()[:2000]
        kw = find_matching_quota_keyword(raw_cut)
        if kw:
            return {
                "raw_message": raw_cut,
                "source_field": "stderr",
                "source_event": "process_stderr",
                "matched_keyword": kw,
                "is_suspected_quota": True,
            }

    # P6g-Việc 3: stopReason='max_tokens', 'cancelled', 'end_turn' không được quét từ khóa quota trên response_text hay stopReason.
    # Chỉ quét từ khóa quota trong trường lỗi thật (error.message, mã HTTP 429, RESOURCE_EXHAUSTED), không quét stopReason hay văn bản chat.
    if stop_reason and stop_reason != "end_turn":
        return {
            "raw_message": f"stopReason='{stop_reason}'" + (f": {response_text[:500]}" if response_text else ""),
            "source_field": "prompt_result['result']['stopReason']",
            "source_event": "session/prompt (result)",
            "matched_keyword": None,
            "is_suspected_quota": False,
        }

    return None


def run_quota_probe(
    agy_bin: str,
    model: str,
    cwd: Path,
    timeout: float = 120.0,
) -> tuple[bool, str, dict | None]:
    """
    Chạy lượt thăm dò nhỏ để xác nhận quota (P6e-M03):
    agy -p "Trả lời đúng một từ: pong." --model <model> --output-format json --sandbox
    Trả về: (is_success, raw_output_or_error, parsed_json)
    Thành công khi parsed_json có status == "SUCCESS" và có response.
    """
    base_cmd = [sys.executable, "-u", agy_bin] if agy_bin.endswith(".py") else [agy_bin]
    cmd = base_cmd + [
        "-p",
        "Trả lời đúng một từ: pong.",
        "--model",
        model,
        "--output-format",
        "json",
        "--sandbox",
    ]
    proc = None
    try:
        popen_kwargs = {
            "cwd": str(cwd),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
        }
        if sys.platform != "win32":
            popen_kwargs["start_new_session"] = True
        proc = subprocess.Popen(
            cmd,
            **popen_kwargs,
        )
        try:
            stdout_data, stderr_data = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                if hasattr(os, "getpgid") and hasattr(signal, "SIGTERM"):
                    pgid = os.getpgid(proc.pid)
                    os.killpg(pgid, signal.SIGTERM)
                else:
                    proc.terminate()
            except Exception:
                try:
                    proc.terminate()
                except Exception:
                    pass
            try:
                stdout_data, stderr_data = proc.communicate(timeout=3.0)
            except Exception:
                try:
                    if hasattr(os, "getpgid") and hasattr(signal, "SIGKILL"):
                        pgid = os.getpgid(proc.pid)
                        os.killpg(pgid, signal.SIGKILL)
                    else:
                        proc.kill()
                except Exception:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                stdout_data, stderr_data = "", ""
            return False, f"Thăm dò quota timeout sau {timeout}s", None

        parsed = parse_agy_json(stdout_data)
        if parsed and parsed.get("status") == "SUCCESS" and parsed.get("response"):
            return True, stdout_data.strip(), parsed

        err_msg = ""
        if parsed and parsed.get("error"):
            err_msg = str(parsed.get("error"))
        elif stderr_data.strip():
            err_msg = stderr_data.strip()
        elif stdout_data.strip():
            err_msg = stdout_data.strip()
        else:
            err_msg = f"Probe exited with code {proc.returncode}"
        return False, err_msg, parsed
    except Exception as exc:
        return False, f"Không chạy được thăm dò: {exc}", None


def write_acp_report(
    report_file: Path,
    repo_dir: Path,
    task_file: str,
    final_status: str,
    final_model: str,
    final_session_id: str,
    final_tokens: int,
    denied_count: int,
    audit_log: list[dict],
    needs_human_commands: list[str],
    changed_files: list[str],
    violations: list[str],
    quota_error_msg: str | None = None,
    worktree_dir: Path | None = None,
    worktree_branch: str | None = None,
    applied_count: int | None = None,
    apply_conflict: bool = False,
    conflict_files: list[str] | None = None,
    agent_response: str = "",
    autocont_count: int = 0,
    unapplied_count: int = 0,
    error_details: dict | None = None,
    commits_count: int = 0,
    head_short: str = "",
    head_warn_msg: str | None = None,
) -> None:
    report_file.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# AGY ACP Bridge Report: {Path(task_file).name}",
        "",
        f"- Thời gian: {datetime.now().isoformat()}",
        f"- Thư mục repo: {repo_dir}",
    ]
    if worktree_branch:
        lines.append(f"- Git Branch: `{worktree_branch}`")
    if worktree_dir:
        lines.append(f"- Git Worktree: {worktree_dir} (branch `{worktree_branch}`)")
    if commits_count > 0:
        lines.append(f"- Commits: {commits_count} (head `{head_short}`)")
    lines.extend([
        f"- Task file: {task_file}",
        f"- Trạng thái: {final_status}",
        f"- Model: {final_model}",
        f"- Session ID: {final_session_id}",
        f"- Tổng tokens: {final_tokens}",
        f"- Yêu cầu quyền bị từ chối: {denied_count}",
        f"- Số lần tự tiếp tục (auto-continue): {autocont_count}",
        "",
    ])

    if head_warn_msg:
        lines.extend([
            f"> **CẢNH BÁO GIT**: {head_warn_msg}",
            "",
        ])

    if error_details:
        raw_msg = error_details.get("raw_message", "")
        src_field = error_details.get("source_field", "")
        src_event = error_details.get("source_event", "")
        kw = error_details.get("matched_keyword")
        probe_succ = error_details.get("probe_succeeded", False)
        probe_run = error_details.get("probe_run", False)
        probe_det = error_details.get("probe_details", "")

        if probe_succ:
            lines.extend([
                "## Cảnh báo lỗi & Kết quả xác minh Quota",
                f"> **KẾT QUẢ XÁC MINH**: nghi quota nhưng thăm dò thành công; lỗi nguyên văn: {raw_msg}",
                f"> - Nguồn phát hiện: sự kiện `{src_event}`, trường `{src_field}`, từ khóa khớp: `{kw}`",
                "> - Lỗi nguyên văn:",
                f"> ```\n> {raw_msg}\n> ```",
                "> - Thăm dò qua `agy -p`: Thành công (`status` SUCCESS và có phản hồi). Xác định KHÔNG phải lỗi hết hạn mức.",
                "",
            ])
        elif final_status == "quota" or error_details.get("is_suspected_quota"):
            lines.extend([
                "## Cảnh báo Quota (Hết hạn mức)",
                "> **CẢNH BÁO QUOTA**: Hết hạn mức tài khoản, hãy đổi tài khoản `agy` rồi chạy lại.",
                f"> - Nguồn phát hiện: sự kiện `{src_event}`, trường `{src_field}`, từ khóa khớp: `{kw}`",
                "> - Lỗi nguyên văn:",
                f"> ```\n> {raw_msg}\n> ```",
            ])
            if probe_run:
                lines.append(f"> - Kết quả thăm dò qua `agy -p`: Thất bại ({probe_det})")
            else:
                lines.append("> - Thăm dò qua `agy -p`: Đã tắt (--no-quota-probe)")
            lines.append("")
        else:
            lines.extend([
                "## Thông tin lỗi phiên (Session Error)",
                f"> - Nguồn phát hiện: sự kiện `{src_event}`, trường `{src_field}`",
                "> - Lỗi nguyên văn:",
                f"> ```\n> {raw_msg}\n> ```",
                "",
            ])
    elif quota_error_msg:
        lines.extend([
            "> **CẢNH BÁO QUOTA**: Hết hạn mức tài khoản, hãy đổi tài khoản `agy` rồi chạy lại.",
            "> Lỗi nguyên văn:",
            f"> ```\n> {quota_error_msg}\n> ```",
            "",
        ])

    if needs_human_commands:
        lines.extend([
            "## Cảnh báo quyền lệnh (NEEDS-HUMAN)",
            "> Các lệnh sau đã bị từ chối tự động vì không nằm trong danh sách an toàn mặc định.",
            "> Để cho phép chạy các lệnh này ở lượt tiếp theo, hãy bổ sung vào tham số `--allow-cmd`:",
            "",
        ])
        for cmd in set(needs_human_commands):
            lines.append(f"- Lệnh bị từ chối:")
            lines.append(f"  ```bash\n  {cmd}\n  ```")
        lines.append("")

    if worktree_dir and unapplied_count > 0:
        lines.extend([
            "## Tệp chưa áp dụng từ Worktree (Unapplied Changes)",
            f"- Phiên kết thúc với trạng thái `{final_status}` nên các thay đổi chưa được tự động chép về repo gốc.",
            f"- Tổng số file hợp lệ đã ghi trong worktree: {unapplied_count} file",
            f"- Thư mục worktree: `{worktree_dir}`",
            f"- Nhánh worktree: `{worktree_branch}`",
            "",
            "### Gợi ý cách chép về repo gốc thủ công (--apply thủ công):",
        ])
        for f in changed_files:
            src_f = worktree_dir / f
            dst_f = repo_dir / f
            lines.append(f"- File trong worktree: `{src_f}` -> Repo gốc: `{dst_f}`")
        lines.extend([
            "",
            "```bash",
            "# Lệnh sao chép thủ công các file từ worktree sang repo gốc:",
        ])
        for f in changed_files:
            src_f = worktree_dir / f
            dst_f = repo_dir / f
            lines.append(f'cp "{src_f}" "{dst_f}"')
        lines.extend([
            "```",
            "",
        ])
    elif worktree_dir and applied_count is not None and applied_count > 0:
        lines.extend([
            "## Kết quả áp dụng Worktree (--apply)",
            f"- Đã áp dụng về repo gốc: {applied_count} file",
            "",
        ])
    elif worktree_dir and not apply_conflict:
        lines.extend([
            "## Worktree độc lập",
            f"- Thư mục: `{worktree_dir}`",
            f"- Nhánh: `{worktree_branch}`",
            f"- Để xem chi tiết: `git -C {worktree_dir} status`",
            "",
        ])

    if apply_conflict and conflict_files:
        lines.extend([
            "## Xung đột khi áp dụng (--apply CONFLICT)",
            "Từ chối áp dụng vì các file đích ở repo gốc đã bị sửa đổi sau thời điểm tạo worktree:",
        ])
        for cf in conflict_files:
            lines.append(f"  - `CONFLICT`: `{cf}`")
        lines.append("")

    lines.extend([
        "## Nhật ký kiểm toán quyền (Permission Audit Log)",
        f"- Tổng số yêu cầu quyền nhận được: {len(audit_log)}",
        "",
        "| ID | Tool | Kind | Quyết định | Nhãn | Mục tiêu | Lý do |",
        "|---|---|---|---|---|---|---|",
    ])
    if audit_log:
        for entry in audit_log:
            tool = entry.get("tool", "")
            kind = entry.get("kind", "")
            decision = entry.get("decision", "")
            if kind == "auto_continue":
                label = "AUTO-CONTINUE"
            else:
                label = "NEEDS-HUMAN" if entry.get("needs_human") else ("ALLOW" if decision == "allow" else "DENY")
            target = entry.get("target", "").replace("|", "\\|").replace("\n", " ")
            if len(target) > 60:
                target = target[:57] + "..."
            reason = entry.get("reason", "").replace("|", "\\|")
            lines.append(f"| {entry.get('id')} | {tool} | {kind} | {decision} | {label} | `{target}` | {reason} |")
    else:
        lines.append("| - | - | - | - | - | (Không có yêu cầu quyền nào) | - |")
    lines.append("")

    lines.extend([
        "## Danh sách file thay đổi",
        f"- Tổng số: {len(changed_files)} file",
    ])
    if changed_files:
        for f in changed_files:
            lines.append(f"  - `{f}`")
    else:
        lines.append("  (Không có file nào thay đổi)")
    lines.append("")

    lines.extend([
        "## Vi phạm (VIOLATION)",
    ])
    if violations:
        for v in violations:
            if v == "commit detected":
                lines.append("  - `VIOLATION`: commit detected (HEAD thay đổi)")
            else:
                lines.append(f"  - `VIOLATION`: `{v}` nằm ngoài phạm vi `--allow-write`")
    else:
        lines.append("  (Không có vi phạm)")
    lines.append("")

    if agent_response:
        lines.extend([
            "## Phản hồi của Agent",
            "```",
            agent_response.strip(),
            "```",
            "",
        ])

    report_content = redact_secrets("\n".join(lines))
    report_file.write_text(report_content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if argv and argv[0] not in ("run", "-h", "--help"):
        argv = ["run"] + argv

    parser = argparse.ArgumentParser(
        description="Điều khiển agy acp (Antigravity Agent Control Protocol) qua phiên sống."
    )
    subparsers = parser.add_subparsers(dest="subcommand")
    run_parser = subparsers.add_parser("run", help="Thực thi task qua agy acp")

    run_parser.add_argument("--dir", required=True, help="Thư mục repo")
    run_parser.add_argument("--task-file", required=True, help="File brief/nhiệm vụ (.md)")
    run_parser.add_argument(
        "--model",
        default="gemini-3.8-flash-medium",
        help="Model sử dụng (mặc định: gemini-3.8-flash-medium)",
    )
    run_parser.add_argument(
        "--session",
        default=None,
        help="ID phiên trước đó để tiếp tục bằng session/load",
    )
    run_parser.add_argument(
        "--allow-write",
        nargs="*",
        action="extend",
        default=None,
        help="Đường dẫn file hoặc thư mục cho phép ghi",
    )
    run_parser.add_argument(
        "--allow-cmd",
        nargs="*",
        action="extend",
        default=None,
        help="Regex hoặc tên lệnh cho phép thực thi",
    )
    run_parser.add_argument(
        "--timeout",
        type=float,
        default=1800.0,
        help="Thời gian tối đa tính bằng giây (mặc định 1800s)",
    )
    run_parser.add_argument(
        "--report-dir",
        default=None,
        help="Thư mục ghi báo cáo",
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ in kế hoạch JSON trên 1 dòng và thoát 0",
    )
    run_parser.add_argument(
        "--worktree",
        action="store_true",
        help="Chạy agy trong git worktree riêng",
    )
    run_parser.add_argument(
        "--worktrees-dir",
        default="~/Documents/worktrees/agy",
        help="Thư mục chứa các worktree",
    )
    run_parser.add_argument(
        "--seed",
        nargs="*",
        action="extend",
        default=None,
        help="File sao chép vào worktree trước khi chạy",
    )
    run_parser.add_argument(
        "--apply",
        action="store_true",
        help="Áp dụng thay đổi từ worktree về repo gốc khi thành công",
    )
    run_parser.add_argument(
        "--max-auto-continue",
        type=int,
        default=3,
        help="Số lần tối đa tự gửi session/prompt tiếp tục khi bị từ chối lệnh mà chưa ghi file (mặc định 3)",
    )
    run_parser.add_argument(
        "--no-quota-probe",
        action="store_true",
        help="Tắt thăm dò quota bằng agy -p khi phát hiện nghi quota",
    )

    args = parser.parse_args(argv)
    if args.subcommand != "run":
        parser.print_help(sys.stderr)
        return 1

    repo_dir = Path(args.dir).resolve()
    if not repo_dir.exists():
        sys.stderr.write(f"Lỗi: Thư mục repo không tồn tại: {args.dir}\n")
        return 1

    task_file_path = Path(args.task_file)
    if not task_file_path.is_absolute():
        if not task_file_path.exists() and (repo_dir / task_file_path).exists():
            task_file_path = repo_dir / task_file_path
        else:
            task_file_path = task_file_path.resolve()

    if not task_file_path.exists():
        sys.stderr.write(f"Lỗi: File task không tồn tại: {args.task_file}\n")
        return 1

    try:
        task_content = task_file_path.read_text(encoding="utf-8")
    except Exception as exc:
        sys.stderr.write(f"Lỗi: Không đọc được file task {task_file_path}: {exc}\n")
        return 1

    prompt = FIXED_PROMPT_PREFIX + task_content
    allow_write = args.allow_write or []
    allow_cmd = args.allow_cmd or []

    # Check glob and validate allow_write (Requirement 6, P6c-C02)
    repo_resolved = repo_dir.resolve()
    for p in allow_write:
        if "*" in p:
            sys.stderr.write(f"Lỗi: Không được dùng glob '*' trong --allow-write: {p}\n")
            return 1
        p_obj = Path(p)
        if ".." in p_obj.parts:
            sys.stderr.write(f"Lỗi: Đường dẫn --allow-write chứa '..': {p}\n")
            return 2
        raw_p = p_obj if p_obj.is_absolute() else (repo_resolved / p_obj)
        if raw_p.is_symlink():
            sys.stderr.write(f"Lỗi: Đường dẫn --allow-write là symlink: {p}\n")
            return 2
        # Duyệt từng thành phần cha chưa resolve (P6f-C02)
        if p_obj.is_absolute():
            try:
                p_rel = p_obj.relative_to(repo_resolved)
            except ValueError:
                sys.stderr.write(f"Lỗi: Đường dẫn --allow-write nằm ngoài thư mục repo: {p}\n")
                return 2
        else:
            p_rel = p_obj
        curr = repo_resolved
        has_sym = False
        for part in p_rel.parent.parts:
            if part in (".", ""):
                continue
            curr = curr / part
            if curr.is_symlink():
                has_sym = True
                break
        if has_sym:
            sys.stderr.write(f"Lỗi: Thư mục cha của --allow-write là symlink: {p}\n")
            return 2
        try:
            res_p = raw_p.resolve()
        except Exception:
            sys.stderr.write(f"Lỗi: Đường dẫn --allow-write không hợp lệ: {p}\n")
            return 2
        if res_p == repo_resolved:
            sys.stderr.write(f"Lỗi: Đường dẫn --allow-write trùng gốc repo: {p}\n")
            return 2
        try:
            if not res_p.is_relative_to(repo_resolved):
                sys.stderr.write(f"Lỗi: Đường dẫn --allow-write nằm ngoài thư mục repo: {p}\n")
                return 2
        except (ValueError, AttributeError):
            sys.stderr.write(f"Lỗi: Đường dẫn --allow-write nằm ngoài thư mục repo: {p}\n")
            return 2

    task_slug = sanitize_task_slug(task_file_path.stem)
    now_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    repo_sanitized = re.sub(r"[^\w\-.]", "_", repo_dir.name or "repo")
    worktrees_root = Path(os.path.expanduser(args.worktrees_dir or "~/Documents/worktrees/agy")).resolve()
    wt_branch = f"agy/{task_slug}-{now_timestamp}"
    wt_dir = worktrees_root / f"{repo_sanitized}-{task_slug}-{now_timestamp}"

    effective_allow_write = (
        map_allow_write_to_worktree(allow_write, repo_dir, wt_dir)
        if args.worktree
        else allow_write
    )

    # Dry-run
    if args.dry_run:
        plan = {
            "argv": [os.environ.get("AGY_BIN", "agy"), "acp", "--sandbox"],
            "model": args.model,
            "session": args.session,
            "policy": {
                "allow_write": effective_allow_write,
                "allow_cmd": allow_cmd,
            },
            "worktree": str(wt_dir) if args.worktree else None,
            "branch": wt_branch if args.worktree else None,
        }
        print(json.dumps(plan, ensure_ascii=False))
        return 0

    if args.report_dir:
        report_dir = Path(args.report_dir).resolve()
    else:
        tmp = os.environ.get("TMPDIR") or tempfile.gettempdir()
        report_dir = Path(tmp) / "agy-acp-bridge"
    report_dir.mkdir(parents=True, exist_ok=True)

    # Khóa thư mục repo
    lock_file = get_lock_file(report_dir, repo_dir)
    lock_acquired = False
    try:
        fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(f"pid={os.getpid()}\ndir={repo_dir}\ntime={datetime.now().isoformat()}\n")
        lock_acquired = True
    except FileExistsError:
        # Kiểm tra tiến trình cũ còn sống không để dọn khóa chết (stale lock, P6e-M02)
        stale = False
        try:
            st = lock_file.stat()
            if st.st_size == 0:
                if (time.time() - st.st_mtime) > 10.0:
                    stale = True
            else:
                content = lock_file.read_text(encoding="utf-8")
                m = re.search(r"pid=(\d+)", content)
                if m:
                    pid = int(m.group(1))
                    try:
                        if sys.platform == "win32":
                            import ctypes
                            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
                            SYNCHRONIZE = 0x00100000
                            h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE, False, pid)
                            if h:
                                exit_code = ctypes.c_ulong()
                                if ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(exit_code)):
                                    stale = (exit_code.value != 259)
                                else:
                                    stale = False
                                ctypes.windll.kernel32.CloseHandle(h)
                            else:
                                stale = True
                        else:
                            os.kill(pid, 0)
                    except ProcessLookupError:
                        stale = True
                    except PermissionError:
                        stale = False
                    except OSError as e:
                        if getattr(e, "errno", None) == errno.ESRCH:
                            stale = True
                        else:
                            stale = False
                elif (time.time() - st.st_mtime) > 10.0:
                    stale = True
        except Exception:
            pass
        if stale:
            try:
                trash_lock = lock_file.with_name(f"{lock_file.name}.stale.{os.getpid()}.{time.time()}")
                os.rename(lock_file, trash_lock)
                try:
                    trash_lock.unlink()
                except Exception:
                    pass
                fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(f"pid={os.getpid()}\ndir={repo_dir}\ntime={datetime.now().isoformat()}\n")
                lock_acquired = True
            except Exception:
                sys.stderr.write(f"Lỗi: Thư mục {repo_dir} đang bị khóa bởi {lock_file}\n")
                return 4
        else:
            sys.stderr.write(f"Lỗi: Thư mục {repo_dir} đang bị khóa bởi {lock_file}\n")
            return 4
    except Exception as exc:
        sys.stderr.write(f"Lỗi khi tạo file khóa {lock_file}: {exc}\n")
        return 4

    controller: ACPController | None = None
    try:
        effective_dir = repo_dir
        repo_baseline_snapshot: dict[str, str] = {}

        if args.worktree:
            worktrees_root.mkdir(parents=True, exist_ok=True)
            repo_baseline_snapshot = snapshot_repo_state(repo_dir)

            wt_add_cmd = [
                "git",
                "-C",
                str(repo_dir),
                "worktree",
                "add",
                "-b",
                wt_branch,
                str(wt_dir),
                "HEAD",
            ]
            wt_res = subprocess.run(wt_add_cmd, capture_output=True, text=True)
            if wt_res.returncode != 0:
                err_text = (wt_res.stderr.strip() or wt_res.stdout.strip() or "git worktree add failed").splitlines()[0]
                print("STATUS: fail worktree-create-failed")
                print("FILES: 0 changed []")
                print(f"REPORT: worktree create error: {err_text}")
                return 6

            effective_dir = wt_dir

            seed_files = args.seed or []
            for s in seed_files:
                try:
                    copy_path_into_worktree(Path(s), repo_dir, wt_dir, is_seed=True)
                except ValueError as exc:
                    sys.stderr.write(f"Lỗi --seed: {exc}\n")
                    print("STATUS: fail worktree-copy-failed")
                    print("FILES: 0 changed []")
                    print(f"REPORT: worktree copy error: {exc}")
                    return 6

            try:
                copy_path_into_worktree(task_file_path, repo_dir, wt_dir, is_seed=False)
            except ValueError as exc:
                sys.stderr.write(f"Lỗi task file: {exc}\n")
                print("STATUS: fail worktree-copy-failed")
                print("FILES: 0 changed []")
                print(f"REPORT: worktree copy error: {exc}")
                return 6

        initial_status = get_git_status(effective_dir)
        initial_fp = {f: get_file_fingerprint(effective_dir, f) for f in initial_status}
        initial_head = get_git_head(effective_dir)
        head_before = initial_head

        agy_bin = os.environ.get("AGY_BIN", "agy")
        controller = ACPController(agy_bin=agy_bin, cwd=effective_dir, timeout=args.timeout)

        try:
            controller.start()
        except FileNotFoundError:
            sys.stderr.write(f"Lỗi: Binary không tìm thấy: {agy_bin}\n")
            print("STATUS: fail session=none tokens=0 denied=0")
            print("FILES: 0 changed []")
            print(f"REPORT: Binary not found: {agy_bin}")
            return 2

        # 1. initialize
        init_id = controller.send_request("initialize", {
            "protocolVersion": 1,
            "clientInfo": {"name": "agy-acp-bridge", "version": "1.0"},
        })
        init_res = None
        step_deadline = time.time() + 10.0
        while time.time() < step_deadline:
            rem = max(0.1, step_deadline - time.time())
            msg = controller.read_message(timeout=rem)
            if msg == "TIMEOUT" or msg is None:
                break
            if msg.get("id") == init_id:
                init_res = msg
                break

        if not init_res or "result" not in init_res:
            controller.close()
            print("STATUS: fail session=none tokens=0 denied=0")
            print("FILES: 0 changed []")
            print("REPORT: initialize failed")
            return 2

        # 2. session/new hoặc session/load
        session_id = args.session
        if session_id:
            load_id = controller.send_request("session/load", {
                "sessionId": session_id,
                "cwd": str(effective_dir),
                "mcpServers": [],
            })
            load_res = None
            step_deadline = time.time() + 10.0
            while time.time() < step_deadline:
                rem = max(0.1, step_deadline - time.time())
                msg = controller.read_message(timeout=rem)
                if msg == "TIMEOUT" or msg is None:
                    break
                if msg.get("id") == load_id:
                    load_res = msg
                    break
            if not load_res or "result" not in load_res:
                controller.close()
                print(f"STATUS: fail session={session_id} tokens=0 denied=0")
                print("FILES: 0 changed []")
                print(f"REPORT: session/load failed for {session_id}")
                return 2
        else:
            new_id = controller.send_request("session/new", {
                "cwd": str(effective_dir),
                "mcpServers": [],
            })
            new_res = None
            step_deadline = time.time() + 10.0
            while time.time() < step_deadline:
                rem = max(0.1, step_deadline - time.time())
                msg = controller.read_message(timeout=rem)
                if msg == "TIMEOUT" or msg is None:
                    break
                if msg.get("id") == new_id:
                    new_res = msg
                    break
            if not new_res or not isinstance(new_res.get("result"), dict):
                controller.close()
                print("STATUS: fail session=none tokens=0 denied=0")
                print("FILES: 0 changed []")
                print("REPORT: session/new failed")
                return 2
            session_id = as_str(as_dict(new_res.get("result")).get("sessionId")) or "none"

        # 3. session/set_model
        if args.model:
            model_id = controller.send_request("session/set_model", {
                "sessionId": session_id,
                "modelId": args.model,
            })
            step_deadline = time.time() + 10.0
            while time.time() < step_deadline:
                rem = max(0.1, step_deadline - time.time())
                msg = controller.read_message(timeout=rem)
                if msg == "TIMEOUT" or msg is None:
                    break
                if msg.get("id") == model_id:
                    break

        # 4. session/prompt loop (hỗ trợ tự tiếp tục khi bị từ chối lệnh)
        audit_log: list[dict] = []
        needs_human_commands: list[str] = []
        agent_chunks: list[str] = []
        denied_count = 0
        final_tokens = 0
        total_allowed_writes = 0
        autocont_count = 0
        current_prompt = prompt
        last_turn_had_denial = False
        last_turn_had_denied_cmd = False
        prompt_result: dict | None = None
        prompt_error = None
        stop_reason = ""
        timed_out = False
        quota_detected = False
        quota_err_msg = ""
        start_time = time.time()

        autocont_recovered = False
        total_exec_denied_count = 0
        turns_count = 0
        turns_with_denial_count = 0
        while True:
            # P6d-C03: đặt lại stop_reason, turn_prompt_result, prompt_error ở ĐẦU mỗi lượt
            turns_count += 1
            stop_reason = ""
            turn_prompt_result = None
            prompt_error = None

            prompt_id = controller.send_request("session/prompt", {
                "sessionId": session_id,
                "prompt": [{"type": "text", "text": current_prompt}],
            })

            turn_denied_commands: list[str] = []
            turn_allowed_writes = 0
            turn_denied_count = 0
            turn_tokens = 0

            while True:
                remaining = args.timeout - (time.time() - start_time)
                if remaining <= 0:
                    timed_out = True
                    # Gửi session/cancel
                    controller.send_request("session/cancel", {"sessionId": session_id})
                    cancel_wait = 5.0
                    while cancel_wait > 0:
                        t0 = time.time()
                        m = controller.read_message(timeout=1.0)
                        cancel_wait -= (time.time() - t0)
                        if m is None:
                            break
                        if m == "TIMEOUT":
                            continue
                        if isinstance(m, dict):
                            m_method = as_str(m.get("method"))
                            if m_method == "session/request_permission":
                                req_id = m.get("id")
                                controller.send_response(req_id, {"outcome": {"optionId": "deny"}})
                            elif m_method == "session/update":
                                update_obj = as_dict(as_dict(m.get("params")).get("update"))
                                if as_str(update_obj.get("sessionUpdate")) == "usage_update":
                                    usage = as_dict(update_obj.get("usage"))
                                    t = usage.get("totalTokens", usage.get("total_tokens", turn_tokens))
                                    if isinstance(t, int):
                                        turn_tokens = t
                            elif m.get("id") == prompt_id:
                                turn_prompt_result = m
                                break
                    break

                msg = controller.read_message(timeout=min(remaining, 1.0))
                if msg == "TIMEOUT":
                    continue
                if msg is None:
                    # Process đóng pipe
                    break

                if not isinstance(msg, dict):
                    continue

                m_method = as_str(msg.get("method"))

                # Xử lý xin quyền session/request_permission
                if m_method == "session/request_permission":
                    req_id = msg.get("id")
                    params = as_dict(msg.get("params"))
                    allowed, is_needs_human, reason, target, perm_kind, tool_name = dispatch_request_permission(
                        params=params,
                        effective_dir=effective_dir,
                        effective_allow_write=effective_allow_write,
                        allow_cmd=allow_cmd,
                        is_worktree=bool(args.worktree),
                    )

                    if perm_kind == "edit":
                        if allowed:
                            turn_allowed_writes += 1
                            total_allowed_writes += 1
                    elif perm_kind == "execute":
                        if not allowed:
                            turn_denied_commands.append(target)
                            total_exec_denied_count += 1
                        if is_needs_human:
                            needs_human_commands.append(target)
                    elif perm_kind == "read":
                        pass

                    decision = "allow" if allowed else "deny"
                    if not allowed:
                        turn_denied_count += 1
                        denied_count += 1

                    audit_log.append({
                        "id": req_id,
                        "tool": tool_name,
                        "kind": perm_kind,
                        "target": target,
                        "decision": decision,
                        "needs_human": is_needs_human,
                        "reason": reason,
                        "time": datetime.now().isoformat(),
                    })

                    controller.send_response(req_id, {"outcome": {"optionId": decision}})

                elif m_method == "session/update":
                    update_obj = as_dict(as_dict(msg.get("params")).get("update"))
                    session_update = as_str(update_obj.get("sessionUpdate"))
                    if session_update == "agent_message_chunk":
                        chunk_text = as_str(as_dict(update_obj.get("content")).get("text"))
                        if chunk_text:
                            agent_chunks.append(chunk_text)
                    elif session_update == "usage_update":
                        usage = as_dict(update_obj.get("usage"))
                        t = usage.get("totalTokens", usage.get("total_tokens", turn_tokens))
                        if isinstance(t, int):
                            turn_tokens = t

                elif msg.get("id") == prompt_id:
                    turn_prompt_result = msg
                    break

            prompt_result = turn_prompt_result
            if prompt_result:
                if "result" in prompt_result:
                    r = as_dict(prompt_result.get("result"))
                    stop_reason = as_str(r.get("stopReason"))
                    usage = as_dict(r.get("usage"))
                    t = usage.get("totalTokens", usage.get("total_tokens", turn_tokens))
                    if isinstance(t, int):
                        turn_tokens = t
                    elif str(t).isdigit():
                        turn_tokens = int(t)
                if "error" in prompt_result:
                    prompt_error = prompt_result["error"]
            else:
                stop_reason = ""
                if not timed_out:
                    prompt_error = {"message": "prompt_result is None (crash or closed pipe)"}

            final_tokens += turn_tokens
            last_turn_had_denied_cmd = bool(turn_denied_commands)
            if last_turn_had_denied_cmd:
                turns_with_denial_count += 1
            if autocont_count > 0 and turn_allowed_writes > 0 and not turn_denied_commands:
                autocont_recovered = True

            # Kiểm tra xem lượt này có lỗi hoặc nghi quota không
            turn_stderr = "".join(controller.stderr_lines)
            turn_agent = "".join(agent_chunks)
            turn_error_info = detect_error_and_suspected_quota(
                prompt_result=prompt_result,
                prompt_error=prompt_error,
                stderr_acc=turn_stderr,
                response_text=turn_agent,
                timed_out=timed_out,
                timeout_val=args.timeout,
                stop_reason=stop_reason,
            )
            if turn_error_info and turn_error_info.get("is_suspected_quota"):
                quota_detected = True

            # Kiểm tra xem có tự tiếp tục khi bị từ chối lệnh không
            should_continue = False
            if (
                not timed_out
                and not prompt_error
                and not quota_detected
                and stop_reason == "end_turn"
                and turn_denied_commands
                and turn_allowed_writes == 0
                and autocont_count < args.max_auto_continue
            ):
                should_continue = True

            if should_continue:
                autocont_count += 1
                denied_cmd = turn_denied_commands[-1]
                continue_msg = (
                    f"Lệnh `{denied_cmd}` bị từ chối. "
                    "Hãy dùng công cụ tích hợp (view_file, list_dir, grep_search) "
                    "hoặc cách khác và tiếp tục làm hết việc theo brief."
                )
                audit_log.append({
                    "id": f"autocont-{autocont_count}",
                    "tool": "bridge",
                    "kind": "auto_continue",
                    "target": denied_cmd,
                    "decision": "continue",
                    "needs_human": False,
                    "reason": f"Tự tiếp tục lượt {autocont_count}: Lệnh bị từ chối và chưa có file nào được ghi",
                    "time": datetime.now().isoformat(),
                })
                current_prompt = continue_msg
                continue
            else:
                break

        controller.close()

        # Kiểm tra kết quả prompt
        response_text = "".join(agent_chunks)
        stderr_acc = "".join(controller.stderr_lines)

        final_error_info = detect_error_and_suspected_quota(
            prompt_result=prompt_result,
            prompt_error=prompt_error,
            stderr_acc=stderr_acc,
            response_text=response_text,
            timed_out=timed_out,
            timeout_val=args.timeout,
            stop_reason=stop_reason,
        )

        quota_confirmed = False
        probe_succeeded = False
        probe_run = False
        probe_details = ""

        if final_error_info and final_error_info.get("is_suspected_quota"):
            if args.no_quota_probe:
                quota_confirmed = True
                probe_details = "Thăm dò quota bị tắt (--no-quota-probe)"
            else:
                probe_run = True
                probe_ok, probe_out_or_err, probe_parsed = run_quota_probe(
                    agy_bin=agy_bin,
                    model=args.model,
                    cwd=effective_dir,
                    timeout=120.0,
                )
                if probe_ok:
                    probe_succeeded = True
                    quota_confirmed = False
                    probe_details = "Thăm dò quota thành công (pong)"
                else:
                    quota_confirmed = True
                    probe_details = f"Thăm dò quota thất bại: {probe_out_or_err[:200]}"

            final_error_info["probe_run"] = probe_run
            final_error_info["probe_succeeded"] = probe_succeeded
            final_error_info["probe_details"] = probe_details

        success_turn = (
            (stop_reason == "end_turn")
            and (prompt_result is not None)
            and not timed_out
            and not prompt_error
            and not quota_confirmed
        )

        # Chụp trạng thái Git sau lượt (P6f)
        head_after = get_git_head(effective_dir)
        branch_after = get_git_branch(effective_dir)
        commits_count = 0
        head_short = head_after[:7] if head_after else ""
        head_is_ancestor = True
        head_rewritten_warn = False
        head_warn_msg = None

        if initial_head and head_after and initial_head != head_after:
            mb_res = subprocess.run(
                ["git", "-C", str(effective_dir), "merge-base", "--is-ancestor", initial_head, head_after],
                capture_output=True,
            )
            if mb_res.returncode == 0:
                head_is_ancestor = True
                cnt_res = subprocess.run(
                    ["git", "-C", str(effective_dir), "rev-list", "--count", f"{initial_head}..{head_after}"],
                    capture_output=True,
                    text=True,
                )
                if cnt_res.returncode == 0 and cnt_res.stdout.strip().isdigit():
                    commits_count = int(cnt_res.stdout.strip())
                else:
                    commits_count = 1
            else:
                head_is_ancestor = False
                head_rewritten_warn = True
                head_warn_msg = f"HEAD đổi sang {head_short} nhưng không phải hậu duệ của {initial_head[:7]}. Dùng 'git reflog' để khôi phục commit cũ nếu cần."

        branch_invalid = False
        if args.worktree:
            if branch_after != wt_branch or not head_is_ancestor:
                branch_invalid = True

        overall_changed_files = get_all_changed_files(effective_dir, initial_head, initial_status, initial_fp)
        violations = check_violations(effective_dir, overall_changed_files, effective_allow_write)

        apply_conflict = False
        conflict_files: list[str] = []
        applied_count = 0

        # Xử lý --apply nếu dùng worktree (chỉ áp dụng khi thành công hoàn toàn, không xung đột/lỗi nhánh)
        if (
            args.worktree
            and args.apply
            and success_turn
            and not violations
            and not quota_confirmed
            and not branch_invalid
            and not head_rewritten_warn
        ):
            curr_repo_snapshot = snapshot_repo_state(repo_dir)
            repo_resolved = repo_dir.resolve()
            allowed_resolved = []
            for p in (args.allow_write or []):
                p_obj = Path(p)
                raw_p = p_obj if p_obj.is_absolute() else (repo_resolved / p_obj)
                if raw_p.is_symlink():
                    continue
                curr = raw_p.parent
                has_sym = False
                while curr != repo_dir and curr.resolve() != repo_resolved and curr != curr.parent:
                    if curr.is_symlink():
                        has_sym = True
                        break
                    curr = curr.parent
                if has_sym:
                    continue
                try:
                    res_p = raw_p.resolve()
                except Exception:
                    continue
                if res_p == repo_resolved:
                    continue
                try:
                    if not res_p.is_relative_to(repo_resolved):
                        continue
                except (ValueError, AttributeError):
                    continue
                allowed_resolved.append(res_p)

            for f in overall_changed_files:
                if is_ignored_cache_file(f):
                    continue
                src_f = wt_dir / f
                dst_f = repo_dir / f

                # Check conflict with baseline snapshot
                orig_hash = repo_baseline_snapshot.get(f)
                curr_hash = curr_repo_snapshot.get(f)
                if orig_hash != curr_hash:
                    conflict_files.append(f)
                    continue

                # Từ chối symlink
                if src_f.is_symlink() or dst_f.is_symlink():
                    conflict_files.append(f)
                    continue

                # Từ chối đích ngoài --allow-write
                dst_resolved = dst_f.resolve()
                is_in_allow_write = False
                for a in allowed_resolved:
                    if dst_resolved == a:
                        is_in_allow_write = True
                        break
                    try:
                        if dst_resolved.is_relative_to(a):
                            is_in_allow_write = True
                            break
                    except (ValueError, AttributeError):
                        pass
                if not is_in_allow_write:
                    conflict_files.append(f)
                    continue

            if conflict_files:
                apply_conflict = True
            else:
                applied_files = [f for f in overall_changed_files if not is_ignored_cache_file(f)]
                applied_count = apply_worktree_changes(wt_dir, repo_dir, applied_files, allowed_resolved)

        # Quyết định exit_code và status_word
        all_turns_had_denied_cmds = (turns_count > 0 and turns_with_denial_count == turns_count)
        has_changed_files = bool(overall_changed_files)
        if not has_changed_files or last_turn_had_denied_cmd:
            autocont_recovered = False

        if quota_confirmed:
            exit_code = 7
            status_word = "quota"
        elif violations:
            exit_code = 3
            status_word = "fail"
        elif apply_conflict:
            exit_code = 5
            status_word = "fail"
        elif not success_turn or branch_invalid:
            exit_code = 2
            status_word = "fail"
        elif head_rewritten_warn:
            exit_code = 0
            status_word = "warn"
        elif bool(needs_human_commands):
            exit_code = 0
            status_word = "warn"
        # Việc 2: Khi lượt cuối (hoặc tất cả các lượt) có lệnh bị từ chối và không có file nào được ghi/đổi, STATUS phải là warn (exit 0)
        elif (last_turn_had_denied_cmd or all_turns_had_denied_cmds or total_exec_denied_count > 0) and not has_changed_files:
            exit_code = 0
            status_word = "warn"
        elif last_turn_had_denied_cmd:
            exit_code = 0
            status_word = "warn"
        elif total_exec_denied_count > 0 and not autocont_recovered:
            exit_code = 0
            status_word = "warn"
        else:
            exit_code = 0
            status_word = "ok"

        has_unapplied = bool(
            args.worktree
            and status_word in ("fail", "quota")
            and overall_changed_files
            and not violations
        )
        unapplied_count = len(overall_changed_files) if has_unapplied else 0

        # Đường dẫn báo cáo
        timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_file = report_dir / f"{timestamp_str}-{task_slug}.md"
        if report_file.exists():
            report_file = report_dir / f"{timestamp_str}-{datetime.now().strftime('%f')}-{task_slug}.md"

        write_acp_report(
            report_file=report_file,
            repo_dir=repo_dir,
            task_file=args.task_file,
            final_status=status_word,
            final_model=args.model,
            final_session_id=session_id,
            final_tokens=final_tokens,
            denied_count=denied_count,
            audit_log=audit_log,
            needs_human_commands=needs_human_commands,
            changed_files=overall_changed_files,
            violations=violations,
            quota_error_msg=final_error_info.get("raw_message") if quota_confirmed else None,
            worktree_dir=wt_dir if args.worktree else None,
            worktree_branch=wt_branch if args.worktree else None,
            applied_count=applied_count if (args.worktree and args.apply and not apply_conflict and status_word in ("ok", "warn")) else None,
            apply_conflict=apply_conflict,
            conflict_files=conflict_files,
            agent_response=response_text,
            autocont_count=autocont_count,
            unapplied_count=unapplied_count,
            error_details=final_error_info,
            commits_count=commits_count,
            head_short=head_short,
            head_warn_msg=head_warn_msg,
        )

        # In ĐÚNG 3 dòng stdout
        line1 = f"STATUS: {status_word} session={session_id} tokens={final_tokens} denied={denied_count}"
        if autocont_count > 0:
            line1 += f" autocont={autocont_count}"
        if status_word == "quota":
            line1 += " DOI-TAI-KHOAN-AGY"

        files_preview = ", ".join(overall_changed_files[:5])
        if len(overall_changed_files) > 5:
            files_preview += ", ..."
        line2 = f"FILES: {len(overall_changed_files)} changed [{files_preview}]"
        if commits_count > 0:
            line2 += f" commits={commits_count} head={head_short}"
        if violations:
            viols_preview = ", ".join(violations[:5])
            if len(violations) > 5:
                viols_preview += ", ..."
            line2 += f" [VIOLATION: {viols_preview}]"
        if apply_conflict:
            conf_preview = ", ".join(conflict_files[:5])
            if len(conflict_files) > 5:
                conf_preview += ", ..."
            line2 += f" [CONFLICT: {conf_preview}]"
        if args.worktree:
            line2 += f" wt={wt_dir}"
            if args.apply and not apply_conflict and status_word in ("ok", "warn"):
                line2 += f" applied={applied_count}"
            elif has_unapplied:
                line2 += f" unapplied={unapplied_count}"

        line3 = f"REPORT: {report_file.resolve()}"

        print(line1)
        print(line2)
        print(line3)

        return exit_code

    finally:
        if controller is not None:
            controller.close()
        if lock_acquired and lock_file.exists():
            try:
                lock_file.unlink()
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main())
