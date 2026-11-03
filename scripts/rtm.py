#!/usr/bin/env python3
"""
scripts/rtm.py
CLI Sinh và kiểm tra tính toàn vẹn của Ma trận truy vết yêu cầu (Function_RTM).
Tuân thủ đặc tả T-11 §7 và các yêu cầu R-08, R-09.

Mã thoát (Exit codes):
  0: Thành công (sinh file thành công hoặc --check hoàn toàn sạch 100%)
  1: Phát hiện thiếu sót truy vết khi bật --check
  2: Lỗi tham số / thư mục đầu vào

Usage:
  python scripts/rtm.py                            # Sinh build/rtm/RTM.md
  python scripts/rtm.py --check                    # Kiểm tra độ bao phủ truy vết
  python scripts/rtm.py --output docs/RTM.md       # Xuất ra đường dẫn tùy chỉnh
"""

from __future__ import annotations
import argparse
import json
import os
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

from agent_core.workflow.rtm import generate_rtm, check_rtm


def main():
    parser = argparse.ArgumentParser(description="CLI Ma trận truy vết yêu cầu phần mềm (Function_RTM)")
    parser.add_argument("--req-dir", default=str(ROOT / "docs" / "requirements"), help="Thư mục chứa tài liệu R-xxx")
    parser.add_argument("--tasks-dir", default=str(ROOT / "tasks"), help="Thư mục chứa task cards")
    parser.add_argument("--output", default=str(ROOT / "build" / "rtm" / "RTM.md"), help="Đường dẫn tệp RTM.md đầu ra")
    parser.add_argument("--check", action="store_true", help="Kiểm tra thiếu sót truy vết và trả mã thoát 1 nếu có lỗi")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    args = parser.parse_args()

    req_dir = Path(args.req_dir)
    tasks_dir = Path(args.tasks_dir)
    output_path = Path(args.output)

    if not req_dir.is_dir():
        sys.stderr.write(f"Lỗi: Thư mục yêu cầu không tồn tại: {req_dir}\n")
        sys.exit(2)
    if not tasks_dir.is_dir():
        sys.stderr.write(f"Lỗi: Thư mục task không tồn tại: {tasks_dir}\n")
        sys.exit(2)

    # Sinh RTM
    out_dir = output_path.parent
    report = generate_rtm(req_dir, tasks_dir, out_dir)

    # Nếu tên file khác RTM.md mặc định, đổi tên sang output_path
    generated_file = out_dir / "RTM.md"
    if generated_file.resolve() != output_path.resolve():
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if generated_file.is_file():
            os.replace(generated_file, output_path)

    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"✅ Đã sinh Ma trận truy vết RTM tại: {output_path}")
        print(f"📊 Thống kê: {len(report.entries)} yêu cầu R-xxx được liên kết.")
        if report.issues:
            print(f"⚠️ Phát hiện {len(report.issues)} điểm thiếu sót truy vết:")
            for iss in report.issues:
                print(f"  - [{iss['type']}] {iss['message']}")
        else:
            print("🎉 100% Yêu cầu đã được liên kết đầy đủ với task và test!")

    if args.check and not report.is_clean:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
