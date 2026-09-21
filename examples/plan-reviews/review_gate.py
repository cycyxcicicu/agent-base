#!/usr/bin/env python3
"""
Plan & Task Gate Auditor (Adapted from gstack plan-eng-review & plan-ceo-review)
Quét và đánh giá chất lượng phản biện của Implementation Plan hoặc Task Card.
"""

import sys
import re
import argparse
from pathlib import Path

# Đảm bảo mã hóa UTF-8 trên Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REQUIRED_CHECKS = [
    {
        "id": "ENG-01",
        "name": "Đánh giá Bán kính ảnh hưởng (Blast Radius)",
        "patterns": [r"blast[_\s-]?radius", r"bán kính ảnh hưởng", r"phạm vi ảnh hưởng"],
        "weight": 20
    },
    {
        "id": "ENG-02",
        "name": "Kế hoạch Hoàn tác (Rollback Strategy)",
        "patterns": [r"rollback", r"hoàn tác", r"kế hoạch rút lui"],
        "weight": 20
    },
    {
        "id": "ENG-03",
        "name": "Quy chuẩn Cắt dọc (Vertical Slice / Tracer-Bullet)",
        "patterns": [r"vertical[_\s-]?slice", r"tracer[_\s-]?bullet", r"cắt dọc", r"end-to-end"],
        "weight": 20
    },
    {
        "id": "ENG-04",
        "name": "Tiêu chí Nghiệm thu Đo lường được (Acceptance Criteria)",
        "patterns": [r"acceptance criteria", r"tiêu chí nghiệm thu", r"tiêu chuẩn hoàn thành"],
        "weight": 20
    },
    {
        "id": "ENG-05",
        "name": "Xác thực Đồ thị Phụ thuộc (Blocked By declaration)",
        "patterns": [r"blocked[_\s-]?by", r"phụ thuộc vào", r"điều kiện tiên quyết"],
        "weight": 20
    }
]

def audit_file(file_path: Path):
    print(f"\n🔍 Đang thẩm định chất lượng Kế hoạch / Phiếu công việc: {file_path.name}\n")
    if not file_path.exists():
        print(f"❌ File không tồn tại: {file_path}")
        sys.exit(1)

    content = file_path.read_text(encoding='utf-8', errors='ignore')
    total_score = 0
    max_score = sum(c["weight"] for c in REQUIRED_CHECKS)

    print("| Mã kiểm tra | Nội dung tiêu chí | Kết quả thẩm định | Trọng số |")
    print("|---|---|---|---|")

    for check in REQUIRED_CHECKS:
        found = False
        for p in check["patterns"]:
            if re.search(p, content, re.IGNORECASE):
                found = True
                break
        
        if found:
            total_score += check["weight"]
            print(f"| {check['id']} | {check['name']} | ✅ ĐẠT TIÊU CHUẨN | +{check['weight']} |")
        else:
            print(f"| {check['id']} | {check['name']} | ⚠️ THIẾU SÓT | 0 |")

    score_pct = (total_score / max_score) * 100
    print("\n--------------------------------------------------")
    print(f"📊 ĐIỂM CHẤT LƯỢNG KẾ HOẠCH (PLAN QUALITY SCORE): {total_score}/{max_score} ({score_pct:.1f}%)")

    if score_pct >= 80:
        print("🎉 KẾ HOẠCH ĐẠT TIÊU CHUẨN PHÊ DUYỆT (PASSED)! Sẵn sàng bước vào pha Coding.\n")
        return 0
    else:
        print("❌ KẾ HOẠCH CHƯA ĐẠT! Cần bổ sung các mục thiếu trước khi bắt đầu code.\n")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Auditor kế hoạch và phiếu task theo chuẩn gstack")
    parser.add_argument("file", help="Đường dẫn tới file markdown cần kiểm tra")
    args = parser.parse_args()

    sys.exit(audit_file(Path(args.file)))

if __name__ == "__main__":
    main()
