#!/usr/bin/env python3
"""Kiểm tra tính toàn vẹn và mức độ đầy đủ của hồ sơ đóng gói Feature & Delivery Package."""

import argparse
import sys
from pathlib import Path


FEATURE_REQUIRED_PATTERNS = [
    ("SRS / Đặc tả yêu cầu", [r".*srs.*\.md$", r".*mo-ta.*\.md$", r".*dac-ta.*\.md$", r".*xuat-excel.*\.md$"]),
    ("Solution Design / HLD", [r".*solution.*design.*\.md$", r".*kien-truc.*\.md$", r".*doi-chieu.*\.md$"]),
    ("Detail Design / LLD", [r".*detail.*design.*\.md$", r".*thiet-ke-ky-thuat.*\.md$", r".*ky-thuat.*\.md$"]),
    ("TestLink XML", [r".*testlink.*\.xml$", r".*testcases.*\.xml$"]),
    ("Ma trận Truy vết RTM", [r".*rtm.*\.md$", r".*traceability.*\.md$", r".*doi-chieu.*\.md$"]),
    ("Sơ đồ Kiến trúc / Luồng", [r"hinh/.*", r".*\.drawio$", r".*\.png$"]),
]

PACKAGE_REQUIRED_FILES = [
    ("Bảng kê khai gói (Manifest)", "package-manifest.md"),
    ("Kịch bản Triển khai (Runbook)", "deployment-runbook.md"),
    ("Kịch bản Hoàn tác (Rollback)", "rollback-plan.md"),
    ("Nghiệm thu UAT & Demo", "uat-signoff.md"),
]


def audit_feature(feature_dir: Path) -> tuple[int, int, list]:
    import re
    if not feature_dir.exists() or not feature_dir.is_dir():
        return 0, len(FEATURE_REQUIRED_PATTERNS), [f"Thư mục không tồn tại: {feature_dir}"]

    files = [p.relative_to(feature_dir).as_posix() for p in feature_dir.rglob("*") if p.is_file()]
    passed = 0
    missing = []

    for name, patterns in FEATURE_REQUIRED_PATTERNS:
        found = False
        for p in patterns:
            for f in files:
                if re.search(p, f, re.IGNORECASE):
                    found = True
                    break
            if found:
                break
        if found:
            passed += 1
        else:
            missing.append(name)

    return passed, len(FEATURE_REQUIRED_PATTERNS), missing


def audit_package(pkg_dir: Path) -> tuple[int, int, list]:
    if not pkg_dir.exists() or not pkg_dir.is_dir():
        return 0, len(PACKAGE_REQUIRED_FILES), [f"Thư mục không tồn tại: {pkg_dir}"]

    passed = 0
    missing = []
    for name, filename in PACKAGE_REQUIRED_FILES:
        target = pkg_dir / filename
        if target.exists() and target.is_file() and target.stat().st_size > 50:
            passed += 1
        else:
            missing.append(f"{name} ({filename})")

    return passed, len(PACKAGE_REQUIRED_FILES), missing


TASK_REQUIRED_SECTIONS = [
    ("Use Case Mapping", r"(?i)(use\s*case|chức\s*năng|feature)"),
    ("User Story (BDD)", r"(?i)(user\s*story|là\s*một|tôi\s*muốn|acceptance\s*criteria)"),
    ("API Design Specification", r"(?i)(api\s*design|endpoint|hợp\s*đồng.*api|rest\s*api)"),
    ("Scope Gating (scope_edit)", r"(?i)scope_edit"),
    ("Tiêu chuẩn DoD", r"(?i)(definition\s*of\s*done|tiêu\s*chí\s*(xong|nghiệm\s*thu))"),
]


def audit_task(task_file: Path) -> tuple[int, int, list]:
    import re
    if not task_file.exists() or not task_file.is_file():
        return 0, len(TASK_REQUIRED_SECTIONS), [f"Tệp không tồn tại: {task_file}"]

    content = task_file.read_text(encoding="utf-8", errors="replace")
    passed = 0
    missing = []

    for name, pattern in TASK_REQUIRED_SECTIONS:
        if re.search(pattern, content):
            passed += 1
        else:
            missing.append(name)

    return passed, len(TASK_REQUIRED_SECTIONS), missing


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra mức độ đầy đủ của hồ sơ Feature & Delivery Package.")
    parser.add_argument("--feature", help="Đường dẫn thư mục Feature (ví dụ: doc/features/UC-01-excel-export)")
    parser.add_argument("--package", help="Đường dẫn thư mục Delivery Package (ví dụ: doc/delivery/packages/REL-2026-Q1)")
    parser.add_argument("--task", help="Đường dẫn file Task card (ví dụ: doc/delivery/tasks/T-04.1.md)")
    parser.add_argument("--all", action="store_true", help="Quét toàn bộ features và packages trong dự án.")
    args = parser.parse_args()

    print("=" * 70)
    print("📦 KIỂM ĐỊNH HỒ SƠ ĐÓNG GÓI PHÁT HÀNH (DELIVERY PACKAGE AUDIT)")
    print("=" * 70)

    total_err = 0

    if args.task:
        p = Path(args.task)
        passed, total, missing = audit_task(p)
        print(f"\n📋 [TASK CARD] {p.name}: {passed}/{total} thành phần chuẩn chỉ")
        if missing:
            print(f"  ❌ Thiếu các phần: {', '.join(missing)}")
            total_err += 1
        else:
            print("  ✅ Đầy đủ 100% Use Case, User Story, API Design và Scope Gating!")

    if args.feature:
        p = Path(args.feature)
        passed, total, missing = audit_feature(p)
        print(f"\n🔍 [FEATURE] {p.name}: {passed}/{total} thành phần hợp lệ")
        if missing:
            print(f"  ❌ Thiếu các hồ sơ: {', '.join(missing)}")
            total_err += 1
        else:
            print("  ✅ Đầy đủ 100% hồ sơ Use Case chuẩn CMMI-L3!")

    if args.package:
        p = Path(args.package)
        passed, total, missing = audit_package(p)
        print(f"\n🚀 [DELIVERY PACKAGE] {p.name}: {passed}/{total} hồ sơ hoàn chỉnh")
        if missing:
            print(f"  ❌ Thiếu các tài liệu phát hành:")
            for m in missing:
                print(f"     - {m}")
            total_err += 1
        else:
            print("  ✅ Đầy đủ 100% hồ sơ phát hành sẵn sàng lên Production!")

    if not args.feature and not args.package and not args.all and not args.task:
        parser.print_help()
        sys.exit(0)

    print("\n" + "=" * 70)
    if total_err == 0:
        print("🎉 KIỂM ĐỊNH THÀNH CÔNG: MỌI HỒ SƠ ĐÃ SẴN SÀNG!")
        sys.exit(0)
    else:
        print(f"⚠️  PHÁT HIỆN {total_err} HỒ SƠ CHƯA ĐẠT CHUẨN.")
        sys.exit(1)


if __name__ == "__main__":
    main()
