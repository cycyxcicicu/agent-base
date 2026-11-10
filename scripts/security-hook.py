#!/usr/bin/env python3
"""
scripts/security-hook.py
Claude Code PreToolUse Security Guard.

Chặn cứng:
1. Các lệnh shell vi phạm AGENTS.md (grep, rg, git grep, find mã nguồn).
2. Các lệnh git nguy hiểm hoặc mẹo lách luật (git\\t, git  , "git", command git,
   & git, g`it, $(git ...)) ở tầng token, tránh false-positive lên `git status` / `git -C ... log`.
Khi vi phạm: exit code 2 + stderr thông báo lỗi để Claude Code hủy bỏ tool call.
"""
import json
import os
import re
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from agent_core.workflow.diff_utils import matches as _glob_matches  # noqa: E402

PLAN_ALLOWED_GLOBS = (
    "doc/**",
    "docs/**",
    "tasks/**",
    "**/*.md",
    "**/*.spec.json",
    "**/*.drawio",
    "**/*.xml",
    "**/*.xlsx",
    "**/*.docx",
)
SCOPE_FILENAME = ".agentbase-scope.json"

BLOCKED_CODE_EXTS = (
    ".java", ".ts", ".tsx", ".js", ".jsx",
    ".py", ".go", ".rs", ".kt", ".swift",
    ".cs", ".php", ".c", ".cpp", ".h", ".vue",
)

_WRAPPERS = {"sudo", "env", "command", "nohup", "time"}
_OBFUSCATING_WRAPPERS = {"command", "env"}

_GIT_GLOBAL_VAL_FLAGS = {
    "-C", "-c", "--git-dir", "--work-tree", "--namespace",
    "--exec-path", "--super-prefix", "--config-env", "--list-cmds",
}

_DANGEROUS_GIT_C_PREFIXES = (
    "alias.", "core.hookspath", "core.sshcommand", "core.editor", "core.pager",
    "core.fsmonitor", "core.askpass", "credential.", "include.", "includeif.",
    "url.", "protocol.", "http.", "user.", "author.", "committer.",
    "commit.gpgsign", "gpg.", "diff.external", "sequence.editor", "pager.",
)

_HARD_DENIED_GIT_SUBCMDS = {
    "reset", "clean", "init", "clone", "filter-branch", "filter-repo",
    "update-ref", "gc", "prune", "replace", "sparse-checkout",
    "bisect", "maintenance", "config",
}

_ALWAYS_ASK_GIT_SUBCMDS = {"add", "commit", "push"}
_MUTATING_GIT_SUBCMDS = {
    "pull", "merge", "rebase", "checkout", "switch", "restore",
    "cherry-pick", "revert", "rm", "mv", "apply", "am",
}
_PROTECTED_BRANCH_NAMES = {"main", "master", "develop"}


def _extract_subshells_and_split(cmd: str) -> list[tuple[str, bool]]:
    """Tách chuỗi shell theo toán tử không nằm trong ngoặc (&&, ||, ;, |, &, newline)
    và đệ quy trích xuất biểu thức $(...) / `...` ngoài ngoặc đơn."""
    out: list[tuple[str, bool]] = []
    _scan_shell(cmd, False, out)
    return out


def _scan_shell(text: str, in_subshell: bool, out: list[tuple[str, bool]]) -> None:
    buf: list[str] = []
    in_single = False
    in_double = False
    i = 0
    n = len(text)

    def _flush():
        seg = "".join(buf).strip()
        buf.clear()
        if seg:
            out.append((seg, in_subshell))

    while i < n:
        ch = text[i]
        if ch == "\\" and not in_single and i + 1 < n:
            buf.append(ch)
            buf.append(text[i + 1])
            i += 2
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            buf.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            buf.append(ch)
            i += 1
            continue

        # Subshell $(...) ngoài ngoặc đơn (kể cả trong ngoặc kép)
        if not in_single and text.startswith("$(", i):
            depth = 1
            j = i + 2
            s_q = False
            d_q = False
            while j < n and depth > 0:
                c = text[j]
                if c == "\\" and not s_q and j + 1 < n:
                    j += 2
                    continue
                if c == "'" and not d_q:
                    s_q = not s_q
                elif c == '"' and not s_q:
                    d_q = not d_q
                elif not s_q and not d_q:
                    if c == "(":
                        depth += 1
                    elif c == ")":
                        depth -= 1
                j += 1
            if depth == 0:
                inner = text[i + 2:j - 1]
                _scan_shell(inner, True, out)
                buf.append(text[i:j])
                i = j
                continue

        # Backtick command substitution `...` ngoài ngoặc đơn (cần đủ cặp mở/đóng)
        if not in_single and ch == "`":
            j = i + 1
            closed = False
            while j < n:
                if text[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if text[j] == "`":
                    closed = True
                    break
                j += 1
            if closed:
                inner = text[i + 1:j]
                _scan_shell(inner, True, out)
                buf.append(text[i:j + 1])
                i = j + 1
                continue

        if not in_single and not in_double:
            if text.startswith("&&", i) or text.startswith("||", i):
                _flush()
                i += 2
                continue
            if ch in (";", "|", "\n", "\r"):
                _flush()
                i += 1
                continue
            if ch == "&" and (i == 0 or text[i - 1] not in "<>") and not text.startswith("&>", i):
                # Giữ lại `&` nếu đứng đầu (toán tử gọi PowerShell `& git`) sau khi tách vế trước đó
                if "".join(buf).strip():
                    _flush()
                buf.append(ch)
                i += 1
                continue

        buf.append(ch)
        i += 1

    _flush()


def _tokenize_segment(seg: str) -> list[tuple[str, str, str]]:
    """Trả về [(norm_word, raw_word, preceding_ws), ...]. Bỏ ngoặc nhưng giữ `raw_word` để nhận biết mẹo bọc."""
    tokens: list[tuple[str, str, str]] = []
    i = 0
    n = len(seg)
    while i < n:
        ws_start = i
        while i < n and seg[i] in " \t\r\n":
            i += 1
        ws = seg[ws_start:i]
        if i >= n:
            break
        raw_start = i
        norm_chars: list[str] = []
        in_single = False
        in_double = False
        while i < n:
            ch = seg[i]
            if not in_single and not in_double and ch in " \t\r\n":
                break
            if ch == "'" and not in_double:
                in_single = not in_single
                i += 1
                continue
            if ch == '"' and not in_single:
                in_double = not in_double
                i += 1
                continue
            if ch == "\\" and not in_single and not in_double and i + 1 < n and seg[i + 1] in ("'", '"', " "):
                norm_chars.append(seg[i + 1])
                i += 2
                continue
            norm_chars.append(ch)
            i += 1
        tokens.append(("".join(norm_chars), seg[raw_start:i], ws))
    return tokens


_PY_EXE_RE = re.compile(r"^(python(?:\d+(?:\.\d+)*)?|py)(?:\.exe)?$", re.I)
_ENV_ASSIGN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$")


def _normalize_git_exe(word: str) -> str:
    """Chuẩn hóa tên thực thi git (bỏ dấu backtick PowerShell như g`it -> git)."""
    return os.path.basename(word.replace("`", "").replace("\\", "/")).lower()


def _is_inline_python_violation(tokens: list[tuple[str, str, str]], py_idx: int) -> tuple[bool, str]:
    """Chặn python/python3 -c, heredoc (`<<`), hoặc đọc script inline qua stdin (`-`) theo AGENTS.md."""
    args = [t[0] for t in tokens[py_idx + 1:]]
    i = 0
    while i < len(args):
        tok = args[i]
        if tok == "-m" or (tok.startswith("-m") and not tok.startswith("--") and len(tok) > 2):
            return False, ""
        if tok in ("-W", "-X", "--check-hash-based-pycs"):
            i += 2
            continue
        if tok in ("-c", "--command") or (
            tok.startswith("-") and not tok.startswith("--") and "c" in tok[1:]
        ):
            return True, (
                "[SECURITY GATE - VI PHẠM AGENTS.md] Lệnh Python inline (`-c`) bị chặn cứng!\n"
                "Cấm tự chế one-liner Python để duyệt/sửa mã nguồn; hãy dùng MCP xerj, `safe-search.py`, `read_file`, `Edit` hoặc công cụ chuẩn."
            )
        if tok == "-" or tok.startswith("<<"):
            return True, (
                "[SECURITY GATE - VI PHẠM AGENTS.md] Chạy Python inline qua stdin/heredoc (`-` / `<<`) bị chặn cứng!\n"
                "Cấm vá code hoặc quét mã nguồn bằng heredoc Python; hãy dùng `Edit`/`Write` hoặc script chính thức."
            )
        if tok.startswith("-"):
            i += 1
            continue
        # Gặp đường dẫn file .py đầu tiên -> hợp lệ (ví dụ safe-search.py, worktree-manager.py)
        return False, ""
    return False, ""


def _is_git_protected_ref(arg: str) -> bool:
    low = arg.lower()
    if low.startswith(":"):
        return True
    if any(low.startswith(p) for p in ("refs/heads/main", "refs/heads/master", "refs/heads/develop", "refs/heads/release/")):
        return True
    if ":" in low:
        rhs = low.split(":", 1)[1]
        if rhs in _PROTECTED_BRANCH_NAMES or rhs.startswith("release/"):
            return True
    return low in _PROTECTED_BRANCH_NAMES or low.startswith("release/")


def _is_git_write_or_hard_denied(
    tokens: list[tuple[str, str, str]], git_idx: int, in_subshell: bool, is_cmd_obfuscated: bool
) -> tuple[bool, str]:
    norms = [t[0] for t in tokens]
    all_after = norms[git_idx + 1:]

    # 1. Cấm --no-verify hoặc -c / --config-env cấu hình khóa nguy hiểm ở bất kỳ vị trí global/subcommand nào
    sub_idx = git_idx + 1
    has_ws_evasion_before_subcmd = False
    while sub_idx < len(tokens) and norms[sub_idx].startswith("-"):
        flag = norms[sub_idx]
        gap = tokens[sub_idx][2]
        if "\t" in gap or "  " in gap:
            has_ws_evasion_before_subcmd = True
        if flag == "-c" and sub_idx + 1 < len(tokens):
            cfg_key = norms[sub_idx + 1].split("=", 1)[0].lower()
            if any(cfg_key.startswith(p) for p in _DANGEROUS_GIT_C_PREFIXES):
                return True, f"[SECURITY GATE] Cờ 'git -c {cfg_key}' bị chặn cứng theo AGENTS.md."
            sub_idx += 2
            continue
        if flag.startswith("-c") and len(flag) > 2:
            cfg_key = flag[2:].split("=", 1)[0].lower()
            if any(cfg_key.startswith(p) for p in _DANGEROUS_GIT_C_PREFIXES):
                return True, f"[SECURITY GATE] Cờ 'git -c {cfg_key}' bị chặn cứng theo AGENTS.md."
            sub_idx += 1
            continue
        if flag == "--config-env" or flag.startswith("--config-env="):
            return True, "[SECURITY GATE] Cờ '--config-env' của git bị chặn cứng theo AGENTS.md."
        if flag in _GIT_GLOBAL_VAL_FLAGS:
            sub_idx += 2
            continue
        sub_idx += 1

    if sub_idx >= len(tokens):
        return False, ""

    if "\t" in tokens[sub_idx][2] or "  " in tokens[sub_idx][2]:
        has_ws_evasion_before_subcmd = True

    subcmd = norms[sub_idx].lower()
    args = norms[sub_idx + 1:]

    if subcmd == "grep":
        return True, (
            "[SECURITY GATE - VI PHẠM AGENTS.md] Lệnh 'git grep' bị chặn cứng!\n"
            "Quy tắc AGENTS.md nghiêm cấm quét mã nguồn bằng grep.\n"
            "-> BẮT BUỘC dùng MCP xerj_def, xerj_search (kèm prefix dự án) hoặc graphify."
        )

    if "--no-verify" in all_after:
        return True, "[SECURITY GATE] Cờ '--no-verify' bị chặn cứng theo AGENTS.md."

    if subcmd in _HARD_DENIED_GIT_SUBCMDS:
        return True, f"[SECURITY GATE] Lệnh 'git {subcmd}' bị chặn cứng theo AGENTS.md."

    args_low = [a.lower() for a in args]
    if subcmd == "reflog" and any(a in ("expire", "delete") for a in args_low):
        return True, "[SECURITY GATE] Lệnh 'git reflog expire/delete' bị chặn cứng."
    if subcmd == "notes" and any(a in ("add", "remove") for a in args_low):
        return True, "[SECURITY GATE] Lệnh 'git notes add/remove' bị chặn cứng."
    if subcmd == "submodule" and any(a in ("add", "update") for a in args_low):
        return True, "[SECURITY GATE] Lệnh 'git submodule add/update' bị chặn cứng."
    if subcmd == "branch" and ("-D" in args or "--delete" in args_low):
        return True, "[SECURITY GATE] Xóa nhánh bằng 'git branch -D/--delete' bị chặn cứng."
    if subcmd == "tag" and any(a in ("-d", "-f", "--force", "--delete") for a in args_low):
        return True, "[SECURITY GATE] Thao tác xóa/ép tag bị chặn cứng."
    if subcmd == "stash" and any(a in ("drop", "clear") for a in args_low):
        return True, "[SECURITY GATE] Lệnh 'git stash drop/clear' bị chặn cứng."
    if subcmd == "worktree" and any(a in ("prune", "lock", "unlock") for a in args_low):
        return True, "[SECURITY GATE] Lệnh 'git worktree prune/lock/unlock' bị chặn cứng."
    if subcmd == "remote" and any(a in ("add", "remove", "set-url", "rename") for a in args_low):
        return True, "[SECURITY GATE] Thay đổi remote git bị chặn cứng theo AGENTS.md."
    if subcmd == "checkout" and "-B" in args:
        return True, "[SECURITY GATE] Lệnh 'git checkout -B' bị chặn cứng."
    if subcmd == "switch" and "-C" in args:
        return True, "[SECURITY GATE] Lệnh 'git switch -C' bị chặn cứng."
    if subcmd == "add" and any(a in ("-A", "--all", ".", "-f", "--force") for a in args):
        return True, "[SECURITY GATE] 'git add -A / . / -f' bị chặn cứng; chỉ add từng đường dẫn cụ thể."
    if subcmd == "commit" and any(
        a in ("--amend", "-n", "--author", "--reset-author", "--no-gpg-sign") or a.startswith("--author=")
        for a in args_low
    ):
        return True, "[SECURITY GATE] Cờ sửa lịch sử / giả danh tính trên 'git commit' bị chặn cứng."
    if subcmd == "push":
        if any(
            a in ("--force", "-f", "--force-with-lease", "--delete", "-d", "--mirror", "--all", "--tags", "--prune")
            for a in args_low
        ):
            return True, "[SECURITY GATE] Lệnh 'git push' ép/xóa/hàng loạt bị chặn cứng."
        pos_args = [a for a in args if not a.startswith("-")]
        if any(_is_git_protected_ref(a) for a in pos_args):
            return True, "[SECURITY GATE] Push lên nhánh chung (main/master/develop/release/*) hoặc xóa ref bị chặn cứng."

    # Chặn các dạng lách luật (tab, 2 dấu cách, "git", command git, & git, g`it, $(git ...)) khi gọi lệnh ghi git
    evaded = is_cmd_obfuscated or has_ws_evasion_before_subcmd or in_subshell
    if not evaded:
        return False, ""

    is_mutating_combo = (
        subcmd in _ALWAYS_ASK_GIT_SUBCMDS
        or subcmd in _MUTATING_GIT_SUBCMDS
        or (subcmd == "stash" and any(a in ("push", "pop", "apply", "branch") for a in args_low))
        or (subcmd == "worktree" and any(a in ("add", "remove", "move") for a in args_low))
        or (subcmd == "branch" and not any(a in ("--list", "-l", "-a", "--all", "-v", "-vv", "--show-current", "-r", "--remotes") for a in args_low) and bool([a for a in args if not a.startswith("-")] or any(a in ("-d", "-m", "-M", "-c", "-C", "--move", "--copy") for a in args)))
        or (subcmd == "tag" and any(a in ("-a", "-m") or a.startswith("-m") for a in args_low))
    )
    if is_mutating_combo:
        return True, (
            f"[SECURITY GATE] Phát hiện dạng gọi lệnh ghi 'git {subcmd}' không chuẩn "
            "(tab/nhiều dấu cách/bọc ngoặc/wrapper/subshell) — bị chặn để tránh lách quy tắc kiểm soát."
        )

    return False, ""


def check_command_violation(cmd: str) -> tuple[bool, str]:
    if not cmd or not cmd.strip():
        return False, ""

    for seg, in_subshell in _extract_subshells_and_split(cmd):
        tokens = _tokenize_segment(seg)
        if not tokens:
            continue

        idx = 0
        has_ps_call_op = False
        used_obfuscating_wrapper = False
        if tokens[0][0] == "&":
            has_ps_call_op = True
            idx = 1

        while idx < len(tokens):
            raw_tok = tokens[idx][0]
            if _ENV_ASSIGN_RE.match(raw_tok):
                idx += 1
                continue
            base = os.path.basename(raw_tok.replace("\\", "/")).lower()
            if base in _WRAPPERS:
                if base in _OBFUSCATING_WRAPPERS:
                    used_obfuscating_wrapper = True
                idx += 1
                while base == "env" and idx < len(tokens) and "=" in tokens[idx][0] and not tokens[idx][0].startswith("-"):
                    idx += 1
                continue
            break

        if idx >= len(tokens):
            continue

        norm_cmd, raw_cmd, _ = tokens[idx]
        first = os.path.basename(norm_cmd.replace("\\", "/")).lower()

        # 1. Chặn grep, egrep, fgrep, rg
        if first in ("grep", "egrep", "fgrep", "rg"):
            return True, (
                f"[SECURITY GATE - VI PHẠM AGENTS.md] Lệnh '{first}' bị chặn cứng!\n"
                "Quy tắc AGENTS.md nghiêm cấm dùng grep/rg để dò tìm mã nguồn (chống tràn context).\n"
                "-> BẮT BUỘC dùng MCP xerj_def, xerj_search (kèm prefix dự án) hoặc graphify."
            )

        # 2. Chặn find quét file mã nguồn
        if first == "find":
            for ext in BLOCKED_CODE_EXTS:
                if f"*{ext}" in seg:
                    return True, (
                        f"[SECURITY GATE - VI PHẠM AGENTS.md] Lệnh 'find' quét file mã nguồn ({ext}) bị chặn!\n"
                        "-> BẮT BUỘC dùng MCP xerj_def, xerj_search (kèm prefix dự án) hoặc graphify."
                    )

        # 3. Chặn python/python3 -c và heredoc/stdin inline script (bảo vệ cả khi nối && hoặc đặt VAR=...)
        if _PY_EXE_RE.match(first):
            blocked, msg = _is_inline_python_violation(tokens, idx)
            if blocked:
                return True, msg

        # 4. Kiểm tra lệnh git (bao gồm git.exe, "git", 'git', g`it, command git, /usr/bin/git, & git, git\t, git  )
        git_exe = _normalize_git_exe(norm_cmd)
        if git_exe in ("git", "git.exe"):
            is_cmd_obfuscated = (
                has_ps_call_op
                or used_obfuscating_wrapper
                or any(ch in raw_cmd for ch in ('"', "'", "`", "/", "\\"))
            )
            blocked, msg = _is_git_write_or_hard_denied(tokens, idx, in_subshell, is_cmd_obfuscated)
            if blocked:
                return True, msg

    return False, ""


def _find_scope_file(target: Path, cwd: str | None = None) -> Path | None:
    env_scope = os.environ.get("AGENTBASE_SCOPE_FILE", "").strip()
    if env_scope:
        p = Path(os.path.expanduser(env_scope)).resolve()
        return p if p.exists() else None
    seen: set[Path] = set()
    search_bases = [target.parent]
    if cwd:
        search_bases.append(Path(os.path.expanduser(cwd)).resolve())
    for base in search_bases:
        for cand_dir in (base, *list(base.parents[:6])):
            if cand_dir in seen:
                continue
            seen.add(cand_dir)
            cand = cand_dir / SCOPE_FILENAME
            if cand.exists():
                return cand
    return None


def check_file_edit_violation(file_path: str, cwd: str | None = None) -> tuple[bool, str]:
    """Kiểm tra khóa phạm vi Edit/Write (.agentbase-scope.json) — fail-open khi không bật, fail-closed khi bật."""
    if not file_path or not file_path.strip():
        return False, ""
    base_dir = Path(os.path.expanduser(cwd)).resolve() if cwd else Path.cwd().resolve()
    raw_target = Path(os.path.expanduser(file_path))
    target = raw_target.resolve() if raw_target.is_absolute() else (base_dir / raw_target).resolve()

    scope_file = _find_scope_file(target, cwd=str(base_dir))
    if not scope_file:
        return False, ""

    if target == scope_file.resolve():
        return True, (
            "[SCOPE LOCK] Không được tự sửa file khóa phạm vi .agentbase-scope.json qua Edit/Write.\n"
            "-> Dùng `python3 scripts/task-gate.py set-scope` khi chuyển pha hoặc được duyệt."
        )

    try:
        cfg = json.loads(scope_file.read_text(encoding="utf-8"))
        if not isinstance(cfg, dict):
            raise ValueError("scope config must be a JSON object")
    except Exception as exc:
        return True, f"[SCOPE LOCK] File {scope_file} bị lỗi định dạng ({exc}) — chặn sửa file theo nguyên tắc fail-closed."

    mode = str(cfg.get("mode", "")).strip().lower()
    scope_root = scope_file.parent.resolve()
    try:
        rel = target.relative_to(scope_root).as_posix()
        inside_root = True
    except ValueError:
        rel = target.as_posix()
        inside_root = False

    if mode == "plan":
        check_path = rel if inside_root else target.name
        if not (_glob_matches(check_path, PLAN_ALLOWED_GLOBS) or "/doc/" in target.as_posix() or "/docs/" in target.as_posix() or "/tasks/" in target.as_posix()):
            return True, (
                f"[CHALLENGE / PLAN GATE] Đang ở pha 'plan' — CẤM sửa mã nguồn ({target.name})!\n"
                "Hãy hoàn tất Phản biện 3 phương án + Thiết kế/AC trước khi mở khóa sang pha `implement`."
            )
        return False, ""

    if mode == "implement":
        card_path = str(cfg.get("card_path") or "").strip()
        if inside_root and card_path and rel == card_path.lstrip("./"):
            return False, ""
        if _glob_matches(rel, ("doc/notes/inbox/**", "docs/notes/inbox/**")) or "/notes/inbox/" in target.as_posix():
            return False, ""

        scope_deny = [str(x) for x in (cfg.get("scope_deny") or []) if str(x).strip()]
        scope_edit = [str(x) for x in (cfg.get("scope_edit") or []) if str(x).strip()]

        if not inside_root:
            return True, (
                f"[SCOPE LOCK] File '{target}' nằm ngoài thư mục worktree/dự án đang khóa ({scope_root}).\n"
                "-> Chỉ sửa trong phạm vi `scope_edit` của Task Card hoặc gỡ khóa bằng `task-gate.py clear-scope`."
            )
        if scope_deny and _glob_matches(rel, scope_deny):
            return True, f"[SCOPE LOCK] File '{rel}' nằm trong danh sách cấm `scope_deny` của Task Card."
        if scope_edit and not _glob_matches(rel, scope_edit):
            return True, (
                f"[SCOPE LOCK] File '{rel}' nằm ngoài `scope_edit` của Task Card ({', '.join(scope_edit[:5])}).\n"
                "-> Ghi đề xuất mở rộng vào card thay vì tự ý sửa file ngoài phạm vi."
            )

    return False, ""


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            sys.exit(0)

        payload = json.loads(raw_input)

        # Claude Code PreToolUse payload format
        tool_name = payload.get("tool_name") or payload.get("tool") or payload.get("name") or ""
        tool_input = payload.get("tool_input") or payload.get("input") or {}
        cwd = payload.get("cwd")

        if tool_name in ("Bash", "bash", "execute_command", "terminal", "PowerShell"):
            command = tool_input.get("command") or tool_input.get("CommandLine") or ""
            is_violation, reason = check_command_violation(command)
            if is_violation:
                sys.stderr.write(f"\n{reason}\n\n")
                sys.stderr.flush()
                sys.exit(2)
        elif tool_name in ("Edit", "Write", "MultiEdit", "NotebookEdit", "edit_file", "write_file", "replace_file_content", "write_to_file"):
            target_path = (
                tool_input.get("file_path")
                or tool_input.get("notebook_path")
                or tool_input.get("path")
                or tool_input.get("TargetFile")
                or ""
            )
            is_violation, reason = check_file_edit_violation(str(target_path), cwd=cwd)
            if is_violation:
                sys.stderr.write(f"\n{reason}\n\n")
                sys.stderr.flush()
                sys.exit(2)

    except Exception:
        # Khi có lỗi phân tích JSON, không chặn tiến trình bình thường
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
