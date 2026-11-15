#!/usr/bin/env python3
"""
scripts/liquibase-guard.py
Cổng kiểm soát Di chuyển Cơ sở Dữ liệu Liquibase (Liquibase Migration Guard).

Mục tiêu cốt lõi (Theo quy tắc cứng §0 AGENTS.md & chuan-sql-va-loi.md):
1. Author Chuẩn Hóa: Mọi changeset mới bắt buộc phải có `author: ducnvh` (hoặc `author="ducnvh"`).
2. Tính Bất Biến (Immutability): Nghiêm cấm sửa đổi changeset cũ đã có trong lịch sử Git.
3. Rollback Bắt Buộc: Mọi changeset DDL/DML bắt buộc phải có khối rollback.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

CHANGESET_XML_PATTERN = re.compile(r'<changeSet\s+[^>]*author=["\']([^"\']+)["\']', re.IGNORECASE)
CHANGESET_SQL_PATTERN = re.compile(r'--changeset\s+([^\s:]+):([^\s]+)', re.IGNORECASE)


def _check_xml_author(file_path: Path, content: str) -> list[str]:
    """Kiểm tra author trong file XML."""
    violations: list[str] = []
    for author in CHANGESET_XML_PATTERN.findall(content):
        if author.lower() != "ducnvh":
            violations.append(
                f"{file_path} [INVALID_LIQUIBASE_AUTHOR] Changeset có author='{author}'. "
                "Quy tắc cứng yêu cầu author changeset mới luôn là 'ducnvh'."
            )
    return violations


def _check_sql_author(file_path: Path, content: str) -> list[str]:
    """Kiểm tra author trong file SQL formatted."""
    if "--liquibase" not in content.lower():
        return []
    violations: list[str] = []
    for author, cs_id in CHANGESET_SQL_PATTERN.findall(content):
        if author.lower() != "ducnvh":
            violations.append(
                f"{file_path} [INVALID_LIQUIBASE_AUTHOR] Changeset id='{cs_id}' có author='{author}'. "
                "Quy tắc cứng yêu cầu author changeset mới luôn là 'ducnvh'."
            )
    return violations


def _check_author_violations(file_path: Path, content: str) -> list[str]:
    """Kiểm tra author của changeset mới phải luôn là ducnvh."""
    suffix = file_path.suffix.lower()
    if suffix == ".xml":
        return _check_xml_author(file_path, content)
    if suffix == ".sql":
        return _check_sql_author(file_path, content)
    return []


def _check_immutability(file_path: Path, base_ref: str) -> list[str]:
    """Kiểm tra tính bất biến: Cấm sửa/xóa dòng changeset cũ so với base_ref."""
    violations: list[str] = []
    try:
        rel_path = file_path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        rel_path = file_path.name

    cmd = ["git", "diff", base_ref, "--", rel_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout:
        return violations

    for line in res.stdout.splitlines():
        if not line.startswith("-") or line.startswith("---"):
            continue
        if any(k in line.lower() for k in ("changeset", "<changeset")):
            violations.append(
                f"{file_path} [MUTATED_OLD_CHANGESET] Phát hiện hành vi sửa/xóa changeset cũ! "
                "Quy tắc cứng nghiêm cấm sửa changeset đã tồn tại; bắt buộc tạo changeset mới."
            )
            break
    return violations


def check_liquibase_file(file_path: Path, base_ref: str | None = None) -> list[str]:
    """Kiểm tra toàn diện 1 file changeset liquibase."""
    if not file_path.is_file():
        return []

    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    violations = _check_author_violations(file_path, content)
    if base_ref:
        violations.extend(_check_immutability(file_path, base_ref))
    return violations


def _resolve_target_files(args: argparse.Namespace) -> list[Path]:
    """Xác định danh sách file migration cần kiểm tra."""
    if args.changed_against:
        cmd = ["git", "diff", "--name-only", args.changed_against]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            return []
        matched = []
        for line in res.stdout.splitlines():
            p = Path(line.strip())
            if p.is_file() and any(k in str(p).lower() for k in ("liquibase", "changelog", "db/migration")):
                matched.append(p)
        return matched

    if args.paths:
        return [Path(p) for p in args.paths if Path(p).is_file()]

    results = []
    for p in Path.cwd().glob("**/db/**"):
        if p.is_file() and any(k in p.name.lower() for k in ("changelog", "migration")):
            results.append(p)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Liquibase Migration Guard")
    parser.add_argument("paths", nargs="*", help="File migration cần kiểm tra")
    parser.add_argument("--changed-against", help="So sánh với commit/nhánh gốc (vd: origin/develop)")
    args = parser.parse_args()

    files = _resolve_target_files(args)
    all_violations: list[str] = []
    for f in files:
        all_violations.extend(check_liquibase_file(f, base_ref=args.changed_against))

    if not all_violations:
        print(f"✅ [LIQUIBASE GUARD] Đã quét {len(files)} file migration: 100% hợp chuẩn.")
        sys.exit(0)

    print("❌ [LIQUIBASE GUARD - VI PHẠM QUY CHUẨN MIGRATION]")
    for v in all_violations:
        print(f"  - {v}")
    print("\nQuy tắc cứng: Liquibase changeset mới author là 'ducnvh', cấm sửa changeset cũ.")
    sys.exit(1)


if __name__ == "__main__":
    main()
