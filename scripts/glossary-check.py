#!/usr/bin/env python3
"""
scripts/glossary-check.py

Kiểm tra tính nhất quán thuật ngữ nghiệp vụ & UI (Domain Glossary / Banned-Terms Guard)
theo cấu hình JSON (chuyển thể cơ chế `gstack-banned-terms` sang Python thuần cho multi-repo).

Mặc định tìm GLOSSARY.json theo thứ tự:
  1. --glossary <path>
  2. doc/architecture/GLOSSARY.json
  3. doc/GLOSSARY.json
  4. docs/GLOSSARY.json

Khi dùng --changed-against <ref>: chỉ quét các dòng THÊM MỚI / SỬA ĐỔI (gồm cả diff
đã commit trên nhánh, staged, unstaged và file mới untracked) để không bị đỏ bởi code cũ.

Exit codes:
  0: Đạt (hoặc chưa cấu hình GLOSSARY.json)
  1: Phát hiện dùng thuật ngữ sai chuẩn / từ cấm
  2: Lỗi cấu hình JSON hoặc git ref
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.workflow.diff_utils import (  # noqa: E402
    DEFAULT_MAX_FILE_BYTES as MAX_FILE_BYTES,
    SKIP_DIRS,
    collect_changed_line_diffs,
    git_output,
    matches,
)

DEFAULT_CANDIDATES = (
    "doc/architecture/GLOSSARY.json",
    "doc.workspace/architecture/GLOSSARY.json",
    "doc/GLOSSARY.json",
    "doc.workspace/GLOSSARY.json",
    "docs/GLOSSARY.json",
)


def resolve_glossary_path(root: Path, cli_arg: str | None) -> Path | None:
    if cli_arg:
        p = Path(cli_arg)
        return p if p.is_absolute() else (root / p)
    for rel in DEFAULT_CANDIDATES:
        cand = root / rel
        if cand.is_file():
            return cand
    return None


def load_glossary(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: không đọc được JSON ({exc})")

    if not isinstance(data, dict) or not isinstance(data.get("terms"), list):
        raise ValueError(f"{path}: cần JSON object có khóa 'terms' là danh sách")

    global_exclude = data.get("exclude", [])
    if not isinstance(global_exclude, list) or not all(isinstance(x, str) for x in global_exclude):
        raise ValueError(f"{path}: 'exclude' phải là danh sách chuỗi glob")

    seen_ids: set[str] = set()
    rules = []
    for idx, item in enumerate(data["terms"], 1):
        where = f"{path}: terms[{idx}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where}: mỗi phần tử phải là object")
        rid = str(item.get("id") or f"term-{idx}").strip()
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", rid):
            raise ValueError(f"{where}: id '{rid}' chỉ được dùng chữ thường, số và '-'")
        if rid in seen_ids:
            raise ValueError(f"{where}: id '{rid}' bị trùng")
        seen_ids.add(rid)

        preferred = item.get("preferred")
        forbidden = item.get("forbidden")
        if not isinstance(preferred, str) or not preferred.strip():
            raise ValueError(f"{where} ({rid}): thiếu 'preferred'")
        if not isinstance(forbidden, list) or not forbidden or not all(isinstance(x, str) and x.strip() for x in forbidden):
            raise ValueError(f"{where} ({rid}): 'forbidden' phải là danh sách chuỗi không rỗng")

        include = item.get("include", ["**"])
        exclude = item.get("exclude", [])
        if not isinstance(include, list) or not include or not all(isinstance(x, str) for x in include):
            raise ValueError(f"{where} ({rid}): 'include' phải là danh sách glob không rỗng")
        if not isinstance(exclude, list) or not all(isinstance(x, str) for x in exclude):
            raise ValueError(f"{where} ({rid}): 'exclude' phải là danh sách chuỗi glob")

        case_sensitive = bool(item.get("case_sensitive", False))
        whole_word = bool(item.get("whole_word", True))
        flags = 0 if case_sensitive else re.IGNORECASE

        patterns = []
        for raw_term in forbidden:
            esc = re.escape(raw_term.strip())
            pat_str = rf"(?<!\w){esc}(?!\w)" if whole_word else esc
            patterns.append((raw_term.strip(), re.compile(pat_str, flags)))

        rules.append({
            "id": rid,
            "preferred": preferred.strip(),
            "patterns": patterns,
            "include": include,
            "exclude": list(global_exclude) + list(exclude),
            "reason": str(item.get("reason") or "").strip(),
            "severity": item.get("severity", "error") if item.get("severity") in ("error", "warn") else "error",
        })

    return {"exclude": global_exclude, "rules": rules}


def collect_target_lines(root: Path, changed_against: str | None, files_csv: str | None) -> dict[str, list[tuple[int, str]]]:
    """Thu thập {(đường_dẫn): [(số_dòng, nội_dung), ...]} cần kiểm tra."""
    if files_csv:
        result: dict[str, list[tuple[int, str]]] = {}
        for raw in files_csv.split(","):
            rel = raw.strip().replace("\\", "/")
            if not rel:
                continue
            p = root / rel
            if p.is_file() and p.stat().st_size <= MAX_FILE_BYTES:
                text = p.read_text(encoding="utf-8", errors="ignore").splitlines()
                result[rel] = list(enumerate(text, 1))
        return result

    if changed_against:
        added_sorted, _ = collect_changed_line_diffs(root, changed_against, max_file_bytes=MAX_FILE_BYTES)
        return added_sorted

    # Quét toàn bộ repo nếu không truyền --changed-against hoặc --files
    files: list[str] = []
    try:
        tracked = git_output(root, "ls-files", "-co", "--exclude-standard")
        files = sorted({x.strip().replace("\\", "/") for x in tracked.splitlines() if x.strip()})
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        for p in root.rglob("*"):
            if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS):
                files.append(p.relative_to(root).as_posix())
        files.sort()

    result = {}
    for rel in files:
        p = root / rel
        if p.is_file() and p.stat().st_size <= MAX_FILE_BYTES:
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
            result[rel] = list(enumerate(lines, 1))
    return result


def scan_glossary(root: Path, glossary: dict, target_lines: dict[str, list[tuple[int, str]]]):
    """Quét vi phạm thuật ngữ. Trả về (findings, ignored_count)."""
    findings = []
    ignored = 0
    rules = glossary["rules"]

    for rel, lines_with_no in target_lines.items():
        applicable = [r for r in rules if matches(rel, r["include"]) and not matches(rel, r["exclude"])]
        if not applicable:
            continue

        # Đọc thêm dòng ngay trước trên đĩa để kiểm tra comment `glossary-ignore: <id> <lý do>`
        disk_lines: list[str] | None = None
        full_p = root / rel
        if full_p.is_file() and full_p.stat().st_size <= MAX_FILE_BYTES:
            try:
                disk_lines = full_p.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                disk_lines = None

        for line_no, text in lines_with_no:
            for rule in applicable:
                ignore_re = re.compile(r"glossary-ignore:\s*" + re.escape(rule["id"]) + r"\s+\S{3,}")
                prev_line = disk_lines[line_no - 2] if (disk_lines and 2 <= line_no <= len(disk_lines) + 1) else ""
                for forbidden_term, regex in rule["patterns"]:
                    if regex.search(text):
                        if ignore_re.search(text) or (prev_line and ignore_re.search(prev_line)):
                            ignored += 1
                        else:
                            findings.append({
                                "file": rel,
                                "line": line_no,
                                "id": rule["id"],
                                "severity": rule["severity"],
                                "forbidden": forbidden_term,
                                "preferred": rule["preferred"],
                                "reason": rule["reason"],
                            })
                        break
    return findings, ignored


def main() -> int:
    ap = argparse.ArgumentParser(description="Kiểm tra thuật ngữ chuẩn theo GLOSSARY.json.")
    ap.add_argument("--root", default=".", help="Thư mục gốc dự án hoặc worktree")
    ap.add_argument("--glossary", default=None, help="Đường dẫn file GLOSSARY.json")
    ap.add_argument("--changed-against", metavar="REF", help="Chỉ quét dòng mới thêm/sửa so với REF (vd: develop)")
    ap.add_argument("--files", default=None, help="Danh sách file (ngăn cách dấu phẩy) cần quét")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    glossary_path = resolve_glossary_path(root, args.glossary)
    if not glossary_path or not glossary_path.is_file():
        print("[INFO] Chưa cấu hình GLOSSARY.json — bỏ qua kiểm tra thuật ngữ.")
        return 0

    try:
        glossary = load_glossary(glossary_path)
        targets = collect_target_lines(root, args.changed_against, args.files)
    except ValueError as exc:
        print(f"LỖI: {exc}")
        return 2

    findings, ignored = scan_glossary(root, glossary, targets)
    for f in findings:
        lvl = "LỖI" if f["severity"] == "error" else "cảnh báo"
        why = f" ({f['reason']})" if f["reason"] else ""
        print(f"{f['file']}:{f['line']}: [{f['id']}] {lvl}: dùng '{f['forbidden']}' -> chuẩn là '{f['preferred']}'{why}")

    errors = sum(1 for f in findings if f["severity"] == "error")
    print(f"Thuật ngữ Glossary: {len(glossary['rules'])} mục, quét {len(targets)} file; {errors} lỗi, {len(findings) - errors} cảnh báo, {ignored} bỏ qua có lý do.")
    if errors:
        print("FAIL: Sửa thuật ngữ về đúng chuẩn Domain Glossary, hoặc thêm `glossary-ignore: <id> <lý do>` nếu dùng có chủ đích.")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
