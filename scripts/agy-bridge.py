#!/usr/bin/env python3
"""
scripts/agy-bridge.py
AI chỉ đạo điều khiển `agy` (Antigravity CLI) làm việc.
Chạy với thư viện chuẩn Python 3.9+, không dependency ngoài.

Usage:
  python3 scripts/agy-bridge.py run --dir <repo> --task-file <brief.md> \
      [--models M1,M2] [--allow-write PATH ...] [--allow-cmd NAME ...] \
      [--report-dir DIR] [--conversation ID] [--dry-run] [--allow-git] \
      [--worktree] [--worktrees-dir DIR] [--seed PATH ...] [--apply]
"""

from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FIXED_PROMPT_PREFIX = (
    "LUẬT CỨNG BẮT BUỘC:\n"
    "1. Cấm chạy các lệnh: git push (mọi biến thể), send-email, remote đổi đích; git config ghi; git ngoài phạm vi repo/worktree. Khi không dùng worktree cấm: reset --hard, clean, stash, restore, checkout/switch đổi nhánh, commit --amend. Message commit chỉ mô tả thay đổi, không thêm thông tin công cụ AI hay Co-Authored-By.\n"
    "2. Tuyệt đối không đọc, in hay commit file bí mật (.env*, token, khóa, mật khẩu).\n"
    "3. Tuân thủ toàn bộ quy định trong AGENTS.md.\n"
    "4. Chỉ ghi vào đường dẫn được cho phép (--allow-write).\n"
    "5. Dừng hỏi ngay khi thiếu dữ kiện, không tự ý suy đoán.\n\n"
    "TASK BRIEF:\n"
)

QUOTA_KEYWORDS = ("quota", "exhausted", "rate limit", "429", "usage limit", "billing")


def redact_secrets(text: str) -> str:
    """Che các giá trị bí mật (token, api_key, private key) trong văn bản báo cáo."""
    if not text:
        return ""
    # Redact OpenAI / Anthropic / general API keys (sk-...)
    res = re.sub(r"\bsk-[a-zA-Z0-9_\-]{16,}\b", "[REDACTED_SECRET]", text)
    # Redact GitHub tokens (ghp_..., gho_...)
    res = re.sub(r"\b(?:ghp|gho)_[a-zA-Z0-9]{20,}\b", "[REDACTED_SECRET]", res)
    # Redact AWS keys
    res = re.sub(r"\bAKIA[0-9A-Z]{16}\b", "[REDACTED_SECRET]", res)
    # Redact token=..., password=..., secret=..., api_key=...
    res = re.sub(
        r"(?i)\b(api[_\-]?key|token|secret|password|passwd|private[_\-]?key)(\s*[:=]\s*['\"]?)([^\s'\"&]+)(['\"]?)",
        r"\1\2[REDACTED_SECRET]\4",
        res,
    )
    # Redact Bearer ...
    res = re.sub(r"(?i)\b(bearer\s+)[a-zA-Z0-9\-_.~+/]+=*", r"\1[REDACTED_SECRET]", res)
    # Redact PEM private keys
    res = re.sub(
        r"-----BEGIN [A-Z ]+ PRIVATE KEY-----[\s\S]*?-----END [A-Z ]+ PRIVATE KEY-----",
        "[REDACTED_PRIVATE_KEY]",
        res,
    )
    return res


def sanitize_task_slug(raw_stem: str, max_len: int = 50) -> str:
    """Làm sạch task_slug: không .., không bắt đầu bằng ., độ dài tối đa."""
    slug = re.sub(r"[^\w\-]", "_", raw_stem)
    slug = re.sub(r"_{2,}", "_", slug)
    slug = slug.strip("._")
    if not slug:
        slug = "task"
    return slug[:max_len]


def is_ignored_cache_file(path_str: str) -> bool:
    """Chỉ bỏ qua đúng mẫu __pycache__/<tên>.cpython-<số>.pyc (P6f-C02).
    Mọi đường dẫn khác trong __pycache__/.pytest_cache hoặc .pyc ở chỗ khác -> VIOLATION."""
    norm = str(path_str).replace("\\", "/")
    p = Path(norm)
    if p.parent.name == "__pycache__":
        if re.match(r"^[\w\-.]+\.cpython-\d+(?:\.opt-\d+)?\.pyc$", p.name):
            return True
    return False


def calculate_total_tokens(attempts: list[dict]) -> int:
    """Tính tổng token từ danh sách các lượt chạy (hỗ trợ cả total_tokens và totalTokens)."""
    total = 0
    for a in attempts:
        usage = a.get("usage")
        if isinstance(usage, dict):
            tok = usage.get("total_tokens") or usage.get("totalTokens") or 0
            if isinstance(tok, int):
                total += tok
    return total


def parse_agy_json(stdout_text: str) -> dict | None:
    text = stdout_text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
    return None


def classify_denied_actions(denied_actions: list | None) -> tuple[list, list]:
    """
    Phân loại denied_actions:
    - soft_denials: action == 'command' (từ chối lệnh, không leo thang model)
    - hard_denials: mọi action khác (ví dụ write_file, từ chối cứng, leo thang model)
    """
    if not denied_actions:
        return [], []
    soft = []
    hard = []
    for item in denied_actions:
        action = item.get("action") if isinstance(item, dict) else str(item)
        if action == "command":
            soft.append(item)
        else:
            hard.append(item)
    return soft, hard


def check_quota_error(
    exit_code: int,
    stdout_text: str,
    stderr_text: str,
    parsed_json: dict | None,
) -> tuple[bool, str]:
    """
    Phát hiện hết hạn mức / rate limit theo từ khóa không phân biệt hoa thường.
    Chỉ kiểm tra khi mã thoát khác 0, hoặc status khác SUCCESS, hoặc có trường error.
    Chỉ quét trường error, stderr (không bao giờ trên response của lượt thành công).
    Từ khóa 429 phải khớp nguyên từ (\b429\b).
    """
    status = parsed_json.get("status", "") if parsed_json else ""
    has_error = bool(parsed_json and parsed_json.get("error"))
    if exit_code == 0 and status == "SUCCESS" and not has_error:
        return False, ""

    texts = []
    if parsed_json and parsed_json.get("error"):
        texts.append(str(parsed_json["error"]))
    if stderr_text:
        texts.append(stderr_text)
    if stdout_text and not parsed_json:
        texts.append(stdout_text)

    combined = " ".join(texts).lower()
    for kw in QUOTA_KEYWORDS:
        matched = False
        if kw == "429":
            if re.search(r"\b429\b", combined):
                matched = True
        else:
            if kw in combined:
                matched = True
        if matched:
            raw_err = ""
            if parsed_json and parsed_json.get("error"):
                raw_err = str(parsed_json["error"])
            elif stderr_text.strip():
                raw_err = stderr_text.strip()
            elif stdout_text.strip() and not parsed_json:
                raw_err = stdout_text.strip()
            else:
                raw_err = f"Lỗi khớp từ khóa hạn mức: '{kw}'"
            return True, raw_err
    return False, ""


def get_lock_file(report_dir: Path, repo_dir: Path) -> Path:
    repo_resolved = repo_dir.resolve()
    dir_hash = hashlib.sha256(str(repo_resolved).encode("utf-8")).hexdigest()[:12]
    sanitized_name = re.sub(r"[^\w\-.]", "_", repo_resolved.name or "repo")
    # Khóa theo thư mục repo dùng chung cho cả hai bridge, không phụ thuộc report_dir
    lock_dir = Path(tempfile.gettempdir()) / "agy-locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    return lock_dir / f"agy-{sanitized_name}-{dir_hash}.lock"


def get_git_status(repo_dir: Path) -> dict[str, str]:
    try:
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignored"],
            capture_output=True,
        )
        if res.returncode != 0:
            return {}
        raw = res.stdout.decode("utf-8", errors="replace")
        tokens = raw.split("\0")
        files_status = {}
        i = 0
        while i < len(tokens):
            item = tokens[i]
            if not item:
                i += 1
                continue
            if len(item) < 3:
                i += 1
                continue
            status_code = item[:2]
            entry = item[3:]
            files_status[entry] = status_code
            if status_code.startswith("R") or status_code.startswith("C"):
                i += 1
                if i < len(tokens) and tokens[i]:
                    orig_entry = tokens[i]
                    files_status[orig_entry] = status_code
            i += 1
        return files_status
    except Exception:
        return {}


def get_git_head(repo_dir: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""


def get_git_branch(repo_dir: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""


def get_all_changed_files(
    repo_dir: Path,
    initial_head: str | None = None,
    initial_status: dict[str, str] | None = None,
    initial_fp: dict[str, tuple[int, int, str]] | None = None,
) -> list[str]:
    """Hợp nhất git diff từ initial_head và git status (untracked-files=all) (Requirement 6)."""
    changed = set()
    # 1. git diff --name-status -z initial_head
    if initial_head:
        try:
            res = subprocess.run(
                ["git", "-C", str(repo_dir), "diff", "--name-status", "-z", initial_head],
                capture_output=True,
            )
            if res.returncode == 0:
                raw = res.stdout.decode("utf-8", errors="replace")
                tokens = raw.split("\0")
                i = 0
                while i < len(tokens):
                    item = tokens[i]
                    if not item:
                        i += 1
                        continue
                    status_code = item
                    i += 1
                    if i < len(tokens) and tokens[i]:
                        changed.add(tokens[i])
                        if status_code.startswith("R") or status_code.startswith("C"):
                            i += 1
                            if i < len(tokens) and tokens[i]:
                                changed.add(tokens[i])
                    i += 1
        except Exception:
            pass

    # 2. Thay đổi chưa commit trong working tree
    curr_status = get_git_status(repo_dir)
    curr_fp = {f: get_file_fingerprint(repo_dir, f) for f in curr_status}
    if initial_status is not None and initial_fp is not None:
        wt_changed = calculate_changed_files(initial_status, initial_fp, curr_status, curr_fp)
        changed.update(wt_changed)
    else:
        for entry in curr_status:
            changed.add(entry)

    # Lọc bỏ .agy-task/ nếu có
    res_list = [f for f in changed if not f.startswith(".agy-task/") and f != ".agy-task"]
    return sorted(res_list)


def get_file_fingerprint(repo_dir: Path, rel_path: str) -> tuple[int, int, str]:
    p = repo_dir / rel_path
    if p.is_symlink():
        try:
            st = p.lstat()
            target = os.readlink(p)
            return (st.st_size, st.st_mtime_ns, f"symlink:{target}")
        except OSError:
            return (0, 0, "")
    if not p.exists() or p.is_dir():
        return (0, 0, "")
    try:
        st = p.stat()
        if st.st_size < 1024 * 1024:
            content_hash = hashlib.sha256(p.read_bytes()).hexdigest()
        else:
            content_hash = f"{st.st_mtime_ns}:{st.st_size}"
        return (st.st_size, st.st_mtime_ns, content_hash)
    except OSError:
        return (0, 0, "")


def snapshot_repo_state(repo_dir: Path) -> dict[str, str]:
    """Chụp trạng thái băm mọi file trong repo gốc (trừ .git) để kiểm tra conflict khi apply."""
    snapshot = {}
    repo_resolved = repo_dir.resolve()
    for root, dirs, files in os.walk(repo_resolved):
        if ".git" in dirs:
            dirs.remove(".git")
        rel_root = Path(root).relative_to(repo_resolved)
        for f in files:
            p = Path(root) / f
            rel = str(rel_root / f) if str(rel_root) != "." else f
            try:
                st = p.stat()
                if st.st_size < 1024 * 1024 * 10:
                    snapshot[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
                else:
                    snapshot[rel] = f"{st.st_mtime_ns}:{st.st_size}"
            except OSError:
                pass
    return snapshot


def copy_path_into_worktree(src_path: Path, repo_dir: Path, worktree_dir: Path, is_seed: bool = False) -> None:
    repo_resolved = repo_dir.resolve()
    wt_resolved = worktree_dir.resolve()
    if not src_path.is_absolute():
        raw_src = repo_resolved / src_path
    else:
        raw_src = src_path
    if not raw_src.exists() and not raw_src.is_symlink():
        return

    # Từ chối nếu là gốc repo hoặc .git
    try:
        resolved_src = raw_src.resolve()
    except Exception:
        resolved_src = raw_src

    if resolved_src == repo_resolved or str(src_path).strip() in (".", "") or resolved_src.name == ".git":
        raise ValueError(f"Không được seed gốc repo hoặc .git: {src_path}")

    if not is_seed:
        # Task file ngoài repo hoặc trong repo: chép NỘI DUNG vào .agy-task/<tên> (P6f-M01)
        rel = Path(".agy-task") / raw_src.name
        dest = worktree_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.is_symlink() or dest.exists():
            dest.unlink()
        if not resolved_src.is_file():
            raise ValueError(f"Task-file không tồn tại hoặc không phải file: {src_path}")
        shutil.copy2(resolved_src, dest, follow_symlinks=True)
        return

    # is_seed == True
    try:
        rel = raw_src.relative_to(repo_resolved)
    except ValueError:
        raise ValueError(f"Đường dẫn ngoài repo: {src_path}")

    if ".git" in rel.parts:
        raise ValueError(f"Không được seed .git: {src_path}")

    dest = worktree_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Xử lý symlink cho seed (P6f-M01): tạo symlink tương đối trỏ trong worktree
    if raw_src.is_symlink():
        target = raw_src.resolve()
        try:
            if not target.is_relative_to(repo_resolved):
                raise ValueError(f"Symlink trỏ ra ngoài repo: {src_path}")
        except (ValueError, AttributeError):
            raise ValueError(f"Symlink trỏ ra ngoài repo: {src_path}")
        if dest.is_symlink() or dest.exists():
            dest.unlink()
        target_rel = target.relative_to(repo_resolved)
        wt_target = worktree_dir / target_rel
        rel_link = os.path.relpath(wt_target, dest.parent)
        os.symlink(rel_link, dest)
        return

    if resolved_src.is_dir():
        def _ignore_external_symlinks(directory, contents):
            ignored = []
            dir_path = Path(directory)
            for name in contents:
                item = dir_path / name
                if item.is_symlink():
                    try:
                        target = item.resolve()
                        if not target.is_relative_to(repo_resolved):
                            ignored.append(name)
                    except Exception:
                        ignored.append(name)
            return ignored

        shutil.copytree(
            resolved_src,
            dest,
            dirs_exist_ok=True,
            symlinks=True,
            ignore=_ignore_external_symlinks,
        )
        for root_p, dirs, files in os.walk(dest):
            for f_name in files + dirs:
                p_item = Path(root_p) / f_name
                if p_item.is_symlink():
                    try:
                        target = p_item.resolve()
                        if not target.is_relative_to(repo_resolved) and not target.is_relative_to(wt_resolved):
                            p_item.unlink()
                        elif target.is_relative_to(repo_resolved):
                            target_rel = target.relative_to(repo_resolved)
                            wt_target = worktree_dir / target_rel
                            rel_link = os.path.relpath(wt_target, p_item.parent)
                            p_item.unlink()
                            os.symlink(rel_link, p_item)
                    except Exception:
                        pass
    else:
        shutil.copy2(resolved_src, dest, follow_symlinks=False)


def map_allow_write_to_worktree(
    allow_write: list[str],
    repo_dir: Path,
    worktree_dir: Path,
) -> list[str]:
    repo_resolved = repo_dir.resolve()
    worktree_resolved = worktree_dir.resolve()
    mapped = []
    for p in allow_write:
        p_obj = Path(p)
        if not p_obj.is_absolute():
            resolved = (repo_resolved / p_obj).resolve()
        else:
            resolved = p_obj.resolve()
        try:
            rel = resolved.relative_to(repo_resolved)
            mapped.append(str(worktree_resolved / rel))
        except ValueError:
            mapped.append(p)
    return mapped


def calculate_changed_files(
    status_before: dict[str, str],
    fp_before: dict[str, tuple[int, int, str]],
    status_after: dict[str, str],
    fp_after: dict[str, tuple[int, int, str]],
) -> list[str]:
    changed = []
    for f in status_after:
        if f not in status_before:
            changed.append(f)
        elif status_after[f] != status_before[f] or fp_after.get(f) != fp_before.get(f):
            changed.append(f)
    for f in status_before:
        if f not in status_after and f not in changed:
            changed.append(f)
    return sorted(changed)


def check_violations(repo_dir: Path, changed_files: list[str], allow_write: list[str]) -> list[str]:
    # Requirement 12: bỏ qua cache files
    effective_changed = [f for f in changed_files if not is_ignored_cache_file(f)]
    if not allow_write:
        return sorted(effective_changed)

    allowed_resolved: list[Path] = []
    repo_resolved = repo_dir.resolve()
    for p in allow_write:
        path_obj = Path(p)
        if not path_obj.is_absolute():
            path_obj = (repo_resolved / path_obj)
        # Requirement 6: Nếu mục allow_write là symlink hoặc resolve ra ngoài repo hoặc bằng gốc repo: bỏ qua
        if path_obj.is_symlink():
            continue
        try:
            res = path_obj.resolve()
            if res == repo_resolved or not res.is_relative_to(repo_resolved):
                continue
            allowed_resolved.append(res)
        except Exception:
            continue

    if not allowed_resolved:
        return sorted(effective_changed)

    violations = []
    for f in effective_changed:
        f_path = repo_dir / f
        # Từ chối symlink trong worktree trỏ ra ngoài hoặc vào file khác
        if f_path.is_symlink():
            violations.append(f)
            continue

        # Từ chối đường dẫn chứa .. hoặc symlink thành phần cha (P6f-C02)
        if ".." in Path(f).parts:
            violations.append(f)
            continue
        curr = repo_dir
        has_symlink_parent = False
        for part in Path(f).parent.parts:
            if part in (".", ""):
                continue
            curr = curr / part
            if curr.is_symlink():
                has_symlink_parent = True
                break
        if has_symlink_parent:
            violations.append(f)
            continue

        try:
            f_resolved = f_path.resolve()
        except Exception:
            violations.append(f)
            continue

        allowed = False
        for allowed_path in allowed_resolved:
            if f_resolved == allowed_path:
                allowed = True
                break
            try:
                if f_resolved.is_relative_to(allowed_path):
                    lexical_parent = (repo_resolved / f).parent.resolve()
                    if lexical_parent == allowed_path or lexical_parent.is_relative_to(allowed_path):
                        allowed = True
                        break
            except (ValueError, AttributeError):
                pass
        if not allowed:
            violations.append(f)
    return sorted(violations)


def build_agy_argv(
    agy_bin: str,
    prompt: str,
    model: str,
    repo_dir: str,
    settings_json: str,
    conversation_id: str | None = None,
) -> list[str]:
    cmd = [
        agy_bin,
        "-p",
        prompt,
        "--model",
        model,
        "--sandbox",
        "--output-format",
        "json",
        "--add-dir",
        repo_dir,
        "--settings",
        settings_json,
    ]
    if conversation_id:
        cmd.extend(["--conversation", conversation_id])
    return cmd


def write_report(
    report_file: Path,
    repo_dir: Path,
    task_file: str,
    final_status: str,
    final_model: str,
    final_conv_id: str,
    final_tokens: int,
    attempts: list[dict],
    changed_files: list[str],
    violations: list[str],
    cmd_denied: bool = False,
    quota_error_msg: str | None = None,
    worktree_dir: Path | None = None,
    worktree_branch: str | None = None,
    applied_count: int | None = None,
    apply_conflict: bool = False,
    conflict_files: list[str] | None = None,
    commits_count: int = 0,
    head_short: str = "",
    head_warn_msg: str | None = None,
) -> None:
    report_file.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# AGY Bridge Report: {Path(task_file).name}",
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
        f"- Conversation ID: {final_conv_id}",
        f"- Tổng tokens: {final_tokens}",
        f"- Models đã thử: {', '.join(a['model'] for a in attempts)}",
        "",
    ])

    if head_warn_msg:
        lines.extend([
            f"> **CẢNH BÁO GIT**: {head_warn_msg}",
            "",
        ])

    if quota_error_msg:
        lines.extend([
            "> **CẢNH BÁO QUOTA**: Hết hạn mức tài khoản, hãy đổi tài khoản `agy` rồi chạy lại.",
            "> Lỗi nguyên văn:",
            f"> ```\n> {quota_error_msg}\n> ```",
            "",
        ])

    if cmd_denied:
        lines.extend([
            "> Cảnh báo: thiếu quyền chạy lệnh, không phải lỗi model; kiểm tra `--allow-cmd` và lệnh bằng chứng trong brief.",
            "",
        ])

    if worktree_dir and applied_count is not None:
        lines.extend([
            f"## Kết quả áp dụng Worktree (--apply)",
            f"- Đã áp dụng về repo gốc: {applied_count} file",
            "",
        ])
    elif worktree_dir and not apply_conflict:
        lines.extend([
            f"## Worktree độc lập",
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
        "## Các lượt thực thi (Attempts)",
        "",
    ])
    for i, a in enumerate(attempts, 1):
        lines.extend([
            f"### Lượt {i}: Model `{a['model']}`",
            f"- Mã thoát (exit code): {a['exit_code']}",
            f"- Status: {a.get('status', 'UNKNOWN')}",
            f"- Usage: `{json.dumps(a.get('usage', {}))}`",
            f"- Denied actions: `{json.dumps(a.get('denied_actions', []))}`",
            f"- Files thay đổi trong lượt: {', '.join(a.get('turn_changed_files', [])) or 'Không có'}",
            "",
            "#### Response nguyên văn",
            "```",
            a.get("response", "").strip(),
            "```",
            "",
        ])
    lines.extend([
        "## Danh sách file thay đổi",
        f"- Tổng số: {len(changed_files)} file",
    ])
    if changed_files:
        for f in changed_files:
            lines.append(f"  - `{f}`")
    else:
        lines.append("  (Không có file nào thay đổi)")
    lines.extend([
        "",
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
    report_content = redact_secrets("\n".join(lines))
    report_file.write_text(report_content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # Support invocation without 'run' subcommand
    if argv and argv[0] not in ("run", "-h", "--help"):
        argv = ["run"] + argv

    parser = argparse.ArgumentParser(
        description="AI chỉ đạo điều khiển agy (Antigravity CLI) làm việc."
    )
    subparsers = parser.add_subparsers(dest="subcommand")
    run_parser = subparsers.add_parser("run", help="Thực thi task qua agy")

    run_parser.add_argument("--dir", required=True, help="Thư mục repo")
    run_parser.add_argument("--task-file", required=True, help="File brief/nhiệm vụ (.md)")
    run_parser.add_argument(
        "--models",
        default="gemini-3.8-flash-medium,gemini-3.8-flash-high",
        help="Thang model, ngăn cách bởi dấu phẩy",
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
        help="Tên lệnh cho phép thực thi (không còn hạn chế lệnh ở chế độ mặc định)",
    )
    run_parser.add_argument(
        "--report-dir",
        default=None,
        help="Thư mục ghi báo cáo (mặc định: $TMPDIR/agy-bridge)",
    )
    run_parser.add_argument(
        "--conversation",
        default=None,
        help="ID phiên trước đó để tiếp tục",
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ in lệnh argv sẽ chạy (JSON 1 dòng) và thoát 0",
    )
    run_parser.add_argument(
        "--allow-git",
        action="store_true",
        help="Cho phép lệnh git khi có --allow-cmd git",
    )
    run_parser.add_argument(
        "--worktree",
        action="store_true",
        help="Chạy agy trong git worktree riêng để cách ly thay đổi",
    )
    run_parser.add_argument(
        "--worktrees-dir",
        default="~/Documents/worktrees/agy",
        help="Thư mục chứa các worktree (mặc định: ~/Documents/worktrees/agy)",
    )
    run_parser.add_argument(
        "--seed",
        nargs="*",
        action="extend",
        default=None,
        help="Đường dẫn file trong repo gốc cần sao chép vào worktree trước khi chạy",
    )
    run_parser.add_argument(
        "--apply",
        action="store_true",
        help="Áp dụng thay đổi từ worktree về repo gốc khi thành công",
    )
    run_parser.add_argument(
        "--timeout",
        type=float,
        default=1800.0,
        help="Thời gian tối đa (giây) cho mỗi lệnh agy (mặc định: 1800.0)",
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

    # Normalize models list
    models = []
    if isinstance(args.models, str):
        models = [m.strip() for m in args.models.split(",") if m.strip()]
    elif isinstance(args.models, list):
        for item in args.models:
            for m in item.split(","):
                if m.strip():
                    models.append(m.strip())
    if not models:
        models = ["gemini-3.8-flash-medium", "gemini-3.8-flash-high"]

    allow_write = args.allow_write or []
    allow_cmd = args.allow_cmd or []

    # Check git permission
    for c in allow_cmd:
        parts = c.strip().split()
        if parts and parts[0] == "git" and not args.allow_git:
            sys.stderr.write("Lỗi: --allow-cmd chứa 'git' nhưng thiếu cờ --allow-git\n")
            return 1

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

    # Plan worktree if requested
    task_slug = sanitize_task_slug(task_file_path.stem)
    now_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    repo_sanitized = re.sub(r"[^\w\-.]", "_", repo_dir.name or "repo")
    worktrees_root = Path(os.path.expanduser(args.worktrees_dir or "~/Documents/worktrees/agy")).resolve()
    wt_branch = f"agy/{task_slug}-{now_timestamp}"
    wt_dir = worktrees_root / f"{repo_sanitized}-{task_slug}-{now_timestamp}"

    # Dry-run handling
    if args.dry_run:
        if args.worktree:
            mapped_aw = map_allow_write_to_worktree(allow_write, repo_dir, wt_dir)
            plan = {
                "worktree": str(wt_dir),
                "branch": wt_branch,
                "allow_write": mapped_aw,
            }
            print(json.dumps(plan, ensure_ascii=False))
            return 0
        else:
            allow_rules = [f"write_file({p})" for p in allow_write]
            for c in allow_cmd:
                allow_rules.append(f"command({c})")
            settings_json = json.dumps({"permissions": {"allow": allow_rules}}, ensure_ascii=False)
            agy_bin = os.environ.get("AGY_BIN", "agy")
            cmd = build_agy_argv(
                agy_bin=agy_bin,
                prompt=prompt,
                model=models[0],
                repo_dir=str(args.dir),
                settings_json=settings_json,
                conversation_id=args.conversation,
            )
            dry_run_cmd = list(cmd)
            if "-p" in dry_run_cmd:
                p_idx = dry_run_cmd.index("-p") + 1
                if p_idx < len(dry_run_cmd):
                    orig_p = dry_run_cmd[p_idx]
                    dry_run_cmd[p_idx] = f"{orig_p[:200]}...[{len(orig_p)} ký tự]"
            print(json.dumps(dry_run_cmd, ensure_ascii=False))
            return 0

    # Report directory
    if args.report_dir:
        report_dir = Path(args.report_dir).resolve()
    else:
        tmp = os.environ.get("TMPDIR") or tempfile.gettempdir()
        report_dir = Path(tmp) / "agy-bridge"

    report_dir.mkdir(parents=True, exist_ok=True)

    # Acquire lock on root repo_dir
    lock_file = get_lock_file(report_dir, repo_dir)
    lock_acquired = False
    try:
        fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(f"pid={os.getpid()}\ndir={repo_dir}\ntime={datetime.now().isoformat()}\n")
        lock_acquired = True
    except FileExistsError:
        # Kiểm tra tiến trình cũ còn sống không để dọn khóa chết (stale lock)
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

    try:
        # Create worktree if requested
        effective_dir = repo_dir
        effective_allow_write = allow_write
        repo_baseline_snapshot: dict[str, str] = {}

        if args.worktree:
            worktrees_root.mkdir(parents=True, exist_ok=True)
            # Baseline snapshot of repo_dir before worktree
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
            effective_allow_write = map_allow_write_to_worktree(allow_write, repo_dir, wt_dir)

            # Copy seed files before initial git status snapshot
            seed_files = args.seed or []
            try:
                for s in seed_files:
                    copy_path_into_worktree(Path(s), repo_dir, wt_dir, is_seed=True)
                # Copy task-file into worktree if not present
                copy_path_into_worktree(task_file_path, repo_dir, wt_dir, is_seed=False)
            except ValueError as exc:
                sys.stderr.write(f"Lỗi seed hoặc task-file: {exc}\n")
                print(f"STATUS: fail model={models[0]} conv=none tokens=0")
                print("FILES: 0 changed []")
                print(f"REPORT: Lỗi seed hoặc task-file: {exc}")
                return 6

        # Build settings JSON for agy
        allow_rules = [f"write_file({p})" for p in effective_allow_write]
        for c in allow_cmd:
            allow_rules.append(f"command({c})")
        settings_json = json.dumps({"permissions": {"allow": allow_rules}}, ensure_ascii=False)

        # Initial status and head in effective_dir
        initial_status = get_git_status(effective_dir)
        initial_fp = {f: get_file_fingerprint(effective_dir, f) for f in initial_status}
        initial_head = get_git_head(effective_dir)
        initial_branch = get_git_branch(effective_dir)

        agy_bin = os.environ.get("AGY_BIN", "agy")
        current_conv_id = args.conversation
        final_conv_id = args.conversation or "none"
        final_model = models[0]
        final_status = "fail"
        final_tokens = 0
        attempts: list[dict] = []
        success_turn = False
        is_warn = False
        quota_detected = False
        quota_err_msg = ""

        for model in models:
            final_model = model
            status_before = get_git_status(effective_dir)
            fp_before = {f: get_file_fingerprint(effective_dir, f) for f in status_before}
            head_before = get_git_head(effective_dir)

            cmd = build_agy_argv(
                agy_bin=agy_bin,
                prompt=prompt,
                model=model,
                repo_dir=str(effective_dir),
                settings_json=settings_json,
                conversation_id=current_conv_id,
            )

            try:
                popen_cmd = list(cmd)
                if popen_cmd and popen_cmd[0].endswith(".py"):
                    popen_cmd = [sys.executable] + popen_cmd
                popen_kwargs = {
                    "cwd": effective_dir,
                    "stdin": subprocess.PIPE,
                    "stdout": subprocess.PIPE,
                    "stderr": subprocess.PIPE,
                    "text": True,
                }
                if sys.platform != "win32":
                    popen_kwargs["start_new_session"] = True
                proc = subprocess.Popen(
                    popen_cmd,
                    **popen_kwargs,
                )
                stdout_text, stderr_text = proc.communicate(timeout=args.timeout)
                exit_code = proc.returncode
            except subprocess.TimeoutExpired:
                exit_code = 124
                stdout_text = ""
                stderr_text = f"Phiên làm việc vượt quá thời gian tối đa {args.timeout}s"
                try:
                    if hasattr(os, "getpgid") and hasattr(signal, "SIGTERM"):
                        pgid = os.getpgid(proc.pid)
                        os.killpg(pgid, signal.SIGTERM)
                    else:
                        proc.terminate()
                except Exception:
                    pass
                try:
                    proc.wait(timeout=3)
                except Exception:
                    try:
                        if hasattr(os, "getpgid") and hasattr(signal, "SIGKILL"):
                            pgid = os.getpgid(proc.pid)
                            os.killpg(pgid, signal.SIGKILL)
                        else:
                            proc.kill()
                    except Exception:
                        pass
                    try:
                        proc.wait(timeout=2)
                    except Exception:
                        pass
            except FileNotFoundError:
                exit_code = 127
                stdout_text = ""
                stderr_text = f"Binary không tìm thấy: {agy_bin}"

            status_after = get_git_status(effective_dir)
            fp_after = {f: get_file_fingerprint(effective_dir, f) for f in status_after}
            head_after = get_git_head(effective_dir)
            turn_changed = calculate_changed_files(status_before, fp_before, status_after, fp_after)

            parsed_json = parse_agy_json(stdout_text)
            status_str = parsed_json.get("status") if parsed_json else "ERROR"
            denied_actions = (parsed_json.get("denied_actions") or []) if parsed_json else []
            conv_id = parsed_json.get("conversation_id") if parsed_json else None
            if conv_id:
                current_conv_id = conv_id
                final_conv_id = conv_id

            usage = parsed_json.get("usage", {}) if parsed_json else {}
            response_text = parsed_json.get("response", "") if parsed_json else stderr_text

            attempt_record = {
                "model": model,
                "exit_code": exit_code,
                "status": status_str,
                "usage": usage,
                "denied_actions": denied_actions,
                "turn_changed_files": turn_changed,
                "response": response_text,
            }
            attempts.append(attempt_record)

            # Check Quota Error
            is_quota, q_err = check_quota_error(exit_code, stdout_text, stderr_text, parsed_json)
            if is_quota:
                quota_detected = True
                quota_err_msg = q_err
                break

            soft_denials, hard_denials = classify_denied_actions(denied_actions)

            is_failed = False
            if exit_code != 0:
                is_failed = True
            elif not parsed_json:
                is_failed = True
            elif status_str != "SUCCESS":
                is_failed = True
            elif bool(hard_denials):
                is_failed = True

            if not is_failed:
                success_turn = True
                if bool(soft_denials):
                    is_warn = True
                    final_status = "warn"
                else:
                    final_status = "ok"
                break

        # Calculate final tokens sum
        final_tokens = calculate_total_tokens(attempts)

        # Final git status check and commit calculation (Requirement 6)
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

        has_changed_files = bool(overall_changed_files)
        last_attempt_had_denials = False
        all_attempts_had_denials = False
        if attempts:
            last_attempt = attempts[-1]
            s_last, h_last = classify_denied_actions(last_attempt.get("denied_actions"))
            last_attempt_had_denials = bool(s_last or h_last)
            all_attempts_had_denials = all(bool(classify_denied_actions(a.get("denied_actions"))[0] or classify_denied_actions(a.get("denied_actions"))[1]) for a in attempts)

        bridge_warn = bool(is_warn or head_rewritten_warn or ((last_attempt_had_denials or all_attempts_had_denials) and not has_changed_files))

        # Exit code determination
        if quota_detected:
            exit_code = 7
            status_word = "quota"
            line1 = f"STATUS: quota model={final_model} conv={final_conv_id} tokens={final_tokens} DOI-TAI-KHOAN-AGY"
        elif violations:
            exit_code = 3
            status_word = "fail"
            line1 = f"STATUS: fail model={final_model} conv={final_conv_id} tokens={final_tokens}"
        elif not success_turn or branch_invalid:
            exit_code = 2
            status_word = "fail"
            line1 = f"STATUS: fail model={final_model} conv={final_conv_id} tokens={final_tokens}"
        elif args.worktree and args.apply:
            # Check for conflict in target files in repo_dir
            curr_repo_snapshot = snapshot_repo_state(repo_dir)
            repo_resolved = repo_dir.resolve()
            allowed_resolved = []
            for p in (allow_write or []):
                p_obj = Path(p)
                raw_p = p_obj if p_obj.is_absolute() else (repo_resolved / p_obj)
                if raw_p.is_symlink():
                    continue
                try:
                    res_p = raw_p.resolve()
                    if res_p == repo_resolved or not res_p.is_relative_to(repo_resolved):
                        continue
                    allowed_resolved.append(res_p)
                except Exception:
                    continue

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
                exit_code = 5
                status_word = "fail"
                line1 = f"STATUS: fail model={final_model} conv={final_conv_id} tokens={final_tokens}"
            else:
                # Safe to copy/delete files from worktree to repo_dir (P6f-M01)
                applied_files = [f for f in overall_changed_files if not is_ignored_cache_file(f)]
                actual_applied = 0
                for f in applied_files:
                    src_f = wt_dir / f
                    dst_f = repo_dir / f
                    if src_f.is_file() and not src_f.is_symlink():
                        dst_f.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_f, dst_f, follow_symlinks=False)
                        actual_applied += 1
                    elif not src_f.exists() and dst_f.exists():
                        if dst_f.is_file() and not dst_f.is_symlink():
                            dst_f.unlink()
                            actual_applied += 1
                applied_count = actual_applied
                if bridge_warn:
                    exit_code = 0
                    status_word = "warn"
                    line1 = f"STATUS: {status_word} model={final_model} conv={final_conv_id} tokens={final_tokens} cmd-denied"
                else:
                    exit_code = 0
                    status_word = "ok"
                    line1 = f"STATUS: {status_word} model={final_model} conv={final_conv_id} tokens={final_tokens}"
        elif bridge_warn:
            exit_code = 0
            status_word = "warn"
            line1 = f"STATUS: {status_word} model={final_model} conv={final_conv_id} tokens={final_tokens} cmd-denied"
        else:
            exit_code = 0
            status_word = "ok"
            line1 = f"STATUS: {status_word} model={final_model} conv={final_conv_id} tokens={final_tokens}"

        # Generate report path
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_file = report_dir / f"{timestamp}-{task_slug}.md"
        if report_file.exists():
            report_file = report_dir / f"{timestamp}-{datetime.now().strftime('%f')}-{task_slug}.md"

        write_report(
            report_file=report_file,
            repo_dir=repo_dir,
            task_file=args.task_file,
            final_status=status_word,
            final_model=final_model,
            final_conv_id=final_conv_id,
            final_tokens=final_tokens,
            attempts=attempts,
            changed_files=overall_changed_files,
            violations=violations,
            cmd_denied=(status_word == "warn"),
            quota_error_msg=quota_err_msg if quota_detected else None,
            worktree_dir=wt_dir if args.worktree else None,
            worktree_branch=(branch_after or wt_branch) if args.worktree else (branch_after or None),
            applied_count=applied_count if (args.worktree and args.apply and not apply_conflict) else None,
            apply_conflict=apply_conflict,
            conflict_files=conflict_files,
            commits_count=commits_count,
            head_short=head_short,
            head_warn_msg=head_warn_msg,
        )

        # Output exactly 3 lines to stdout
        files_preview = ", ".join(overall_changed_files[:5])
        if len(overall_changed_files) > 5:
            files_preview += ", ..."
        commit_info = f" commits={commits_count} head={head_short}" if commits_count > 0 else ""
        line2 = f"FILES: {len(overall_changed_files)} changed [{files_preview}]{commit_info}"
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
            if args.apply:
                line2 += f" applied={applied_count}"

        line3 = f"REPORT: {report_file.resolve()}"

        print(line1)
        print(line2)
        print(line3)

        return exit_code

    finally:
        if lock_acquired and lock_file.exists():
            try:
                lock_file.unlink()
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main())
