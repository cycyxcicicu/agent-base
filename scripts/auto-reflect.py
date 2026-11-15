#!/usr/bin/env python3
"""scripts/auto-reflect.py

Tự Động Hóa Vòng Lặp Học Hỏi Tri Thức (Autonomous Self-Learning Trigger).
Kết nối chu trình khép kín: Harvest Chat Trajectory -> Harness Reflection -> Knowledge Graph Refresh.

Tính năng:
- Tự động quét các phiên chat gần nhất (Antigravity/Gemini & Claude Code CLI) qua `harvest-chat.py`.
- Tự động gộp các bài học, quyết định kỹ thuật từ `docs/notes/inbox/` vào `docs/PROJECT-NOTES.md` qua `harness-reflect.py --archive`.
- Tái đồng bộ Knowledge Graph và Scoped Context.
- Chạy hoàn toàn idempotent (an toàn, không lặp lại nội dung đã nạp).

Usage:
  python3 scripts/auto-reflect.py
  python3 scripts/auto-reflect.py --limit 10
  python3 scripts/auto-reflect.py --dry-run
"""

from __future__ import annotations

import argparse
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


def run_cmd(args: list[str], dry_run: bool = False) -> int:
    """Thực thi một lệnh python trong subprocess."""
    cmd_str = " ".join(args)
    if dry_run:
        print(f"[DRY-RUN] Sẽ chạy: {cmd_str}")
        return 0

    print(f"==> Chạy: {cmd_str}")
    p = subprocess.run(
        [sys.executable] + args,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(p.stdout)
    return p.returncode


def trigger_learning_cycle(limit: int = 20, dry_run: bool = False) -> int:
    """Kích hoạt chu trình học hỏi và phản tư hoàn chỉnh."""
    print("=" * 60)
    print("KHỞI ĐỘNG CHU TRÌNH HỌC HỎI TỰ TRỊ (AUTONOMOUS LEARNING CYCLE)")
    print("=" * 60)

    # Bước 1: Khai thác chat trajectory
    print("\n--- BƯỚC 1: Khai thác lịch sử hội thoại gần nhất (harvest-chat.py) ---")
    harvest_args = [str(ROOT / "scripts" / "harvest-chat.py"), "--limit", str(limit), "--reflect"]
    code1 = run_cmd(harvest_args, dry_run=dry_run)
    if code1 != 0 and not dry_run:
        print(f"[WARN] harvest-chat trả về mã {code1}, tiếp tục bước phản tư ghi chú...")

    # Bước 2: Phản tư kinh nghiệm và lưu trữ ghi chú
    print("\n--- BƯỚC 2: Phản tư bài học & Archive ghi chú đã gộp (harness-reflect.py) ---")
    reflect_args = [str(ROOT / "scripts" / "harness-reflect.py"), "--archive"]
    if dry_run:
        reflect_args.append("--dry-run")
    code2 = run_cmd(reflect_args, dry_run=dry_run)
    if code2 != 0 and not dry_run:
        print(f"[ERROR] harness-reflect trả về mã lỗi {code2}")
        return code2

    print("\n" + "=" * 60)
    print("[THÀNH CÔNG] Chu trình học hỏi đã hoàn tất. Tri thức mới đã nạp vào hệ thống.")
    print("=" * 60)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="auto-reflect: Tự động hóa chu trình học hỏi tri thức và phản tư kinh nghiệm"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Số lượng phiên chat tối đa cần quét (mặc định: 20)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Xem trước các bước sẽ thực hiện mà không ghi đè dữ liệu",
    )

    args = parser.parse_args()
    return trigger_learning_cycle(limit=args.limit, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
