"""agent_core.workflow.diff_utils

Tiện ích dùng chung cho các cổng kiểm tự động (`hard-check.py`, `glossary-check.py`, `task-gate.py`, `security-hook.py`):
- Khớp glob đường dẫn POSIX (`*`, `**`, `?`).
- Thu thập danh sách file và dòng thêm/xóa trên git diff (bao gồm cả thay đổi chưa commit trong worktree).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

SKIP_DIRS = {
    ".git",
    "node_modules",
    "build",
    "dist",
    "target",
    "__pycache__",
    "graphify-out",
    ".venv",
    "venv",
    ".next",
    "coverage",
}
DEFAULT_MAX_FILE_BYTES = 1_000_000


def glob_to_regex(glob_str: str) -> str:
    """Chuyển glob đường dẫn (`*`, `**`, `?`) sang regex neo đầu cuối."""
    g = glob_str.replace("\\", "/")
    out: List[str] = []
    i, n = 0, len(g)
    while i < n:
        c = g[i]
        if c == "*":
            if i + 1 < n and g[i + 1] == "*":
                if i + 2 < n and g[i + 2] == "/":
                    out.append("(?:.*/)?")
                    i += 3
                    continue
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(c))
        i += 1
    return "^" + "".join(out) + "$"


def matches(path: str, globs: Iterable[str]) -> bool:
    """Kiểm tra đường dẫn POSIX có khớp ít nhất một glob trong danh sách hay không."""
    norm = path.replace("\\", "/").lstrip("./")
    return any(re.match(glob_to_regex(g), norm) for g in globs)


def git_output(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "-c", "core.quotepath=false", *args],
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    )


def verify_git_ref(root: Path, ref: str) -> None:
    try:
        git_output(root, "rev-parse", "--verify", f"{ref}^{{commit}}")
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as exc:
        raise ValueError(f"git ref không hợp lệ '{ref}': {exc}")


def collect_changed_files(root: Path, changed_against: str) -> List[str]:
    """Liệt kê file thêm/sửa đổi so với `changed_against` (gồm cả diff chưa commit và untracked)."""
    verify_git_ref(root, changed_against)
    names = set(git_output(root, "diff", "--name-only", "--diff-filter=ACMR", "--no-renames", f"{changed_against}...HEAD").splitlines())
    names.update(git_output(root, "diff", "--name-only", "--diff-filter=ACMR", "--no-renames").splitlines())
    names.update(git_output(root, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "--no-renames").splitlines())
    names.update(git_output(root, "ls-files", "--others", "--exclude-standard").splitlines())
    return sorted({n.strip().replace("\\", "/") for n in names if n.strip()})


def parse_unified_diff_lines(diff_text: str) -> Tuple[Dict[str, Dict[int, str]], Dict[str, List[Tuple[int, str]]]]:
    """Tách các dòng mới thêm (`+`) và các dòng vừa xóa (`-`) từ `git diff -U0`."""
    added: Dict[str, Dict[int, str]] = {}
    removed: Dict[str, List[Tuple[int, str]]] = {}
    cur_file: Optional[str] = None
    old_line = 0
    new_line = 0

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            cur_file = line[6:].strip().replace("\\", "/")
            added.setdefault(cur_file, {})
            removed.setdefault(cur_file, [])
            continue
        if line.startswith("+++ "):
            cur_file = None
            continue
        if line.startswith("--- "):
            continue
        if cur_file is None:
            continue
        if line.startswith("@@"):
            m = re.search(r"-(\d+)(?:,\d+)?\s+\+(\d+)(?:,\d+)?", line)
            if m:
                old_line = int(m.group(1))
                new_line = int(m.group(2))
            continue
        if line.startswith("+") and not line.startswith("+++"):
            added[cur_file][new_line] = line[1:]
            new_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed[cur_file].append((old_line, line[1:]))
            old_line += 1

    return added, removed


def collect_changed_line_diffs(
    root: Path,
    changed_against: Optional[str] = None,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
) -> Tuple[Dict[str, List[Tuple[int, str]]], Dict[str, List[Tuple[int, str]]]]:
    """Thu thập dòng thêm mới và dòng bị xóa trên git diff + untracked files.
    Nếu `changed_against` được truyền, kiểm tra ref hợp lệ và bao gồm `<ref>...HEAD` + working tree.
    Nếu `changed_against` là None, chỉ lấy thay đổi chưa commit + staged + untracked (nếu là git repo).
    """
    diff_specs = [
        ("diff", "--unified=0", "--no-color", "--no-renames"),
        ("diff", "--cached", "--unified=0", "--no-color", "--no-renames"),
    ]
    if changed_against:
        verify_git_ref(root, changed_against)
        diff_specs.insert(0, ("diff", "--unified=0", "--no-color", "--no-renames", f"{changed_against}...HEAD"))

    added_map: Dict[str, Dict[int, str]] = {}
    removed_map: Dict[str, List[Tuple[int, str]]] = {}

    for args in diff_specs:
        try:
            out = git_output(root, *args)
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            continue
        a_part, r_part = parse_unified_diff_lines(out)
        for fpath, rows in a_part.items():
            added_map.setdefault(fpath, {}).update(rows)
        for fpath, rrows in r_part.items():
            removed_map.setdefault(fpath, []).extend(rrows)

    try:
        untracked_out = git_output(root, "ls-files", "--others", "--exclude-standard")
        for raw_u in untracked_out.splitlines():
            rel = raw_u.strip().replace("\\", "/")
            if not rel:
                continue
            p = root / rel
            if p.is_file() and p.stat().st_size <= max_file_bytes:
                lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
                added_map[rel] = dict(enumerate(lines, 1))
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        pass

    added_sorted = {f: sorted(rows.items()) for f, rows in sorted(added_map.items()) if rows}
    removed_clean = {f: rows for f, rows in sorted(removed_map.items()) if rows}
    return added_sorted, removed_clean

