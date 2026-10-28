#!/usr/bin/env python3
"""
scripts/task-claim-check.py
CLI Kiểm tra điều kiện nhận task (Claim Check) theo 5 tiêu chí: G0, SEQ, DoR, BLK, PLAN.
Cung cấp chẩn đoán cố vấn độc lập trước khi bắt đầu thực thi task.

Mã thoát (Exit codes):
  0: PASS (Đủ điều kiện nhận việc)
  1: BLOCKED (Ít nhất một tiêu chí bị chặn)
  2: Lỗi tham số / tệp không tồn tại

Usage:
  python scripts/task-claim-check.py --card tasks/<epic>/T-xx.md [--format json]
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

from agent_core.workflow.claim_check import check_task_claim


def main():
    parser = argparse.ArgumentParser(description="CLI Kiểm tra điều kiện nhận việc (Task Claim Check)")
    parser.add_argument("--card", required=True, help="Đường dẫn tới file task card cần kiểm tra")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    args = parser.parse_args()

    card_path = Path(args.card)
    if not card_path.is_file():
        # Thử ghép với ROOT nếu đường dẫn tương đối
        card_path = ROOT / args.card
        if not card_path.is_file():
            sys.stderr.write(f"Lỗi: Không tìm thấy task card tại: {args.card}\n")
            sys.exit(2)

    try:
        result = check_task_claim(card_path, tasks_root=ROOT / "tasks")
    except Exception as e:
        sys.stderr.write(f"Lỗi khi kiểm tra card: {str(e)}\n")
        sys.exit(2)

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        status_icon = "✅ PASS" if result.verdict == "PASS" else "⛔ BLOCKED"
        print(f"\n=======================================================")
        print(f"KẾT QUẢ KIỂM TRA ĐIỀU KIỆN NHẬN TASK: [{result.card_id}] {status_icon}")
        print(f"=======================================================")
        print(f"📢 {result.advisory_notice}\n")

        for code, info in result.checks.items():
            icon = "✅" if info["pass"] else "❌"
            print(f"  {icon} [{code}] {info['message']}")
        print()

    sys.exit(0 if result.verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
