#!/usr/bin/env python3
"""scripts/refresh.py

Chạy một lệnh thay cho bốn bước sinh lại mà CI bắt buộc, để khỏi nhớ tay:

  1. sync-adapters.py            vai trò, AGENTS.md -> GEMINI.md, CODEX.md, .kilo/, .claude/, ...
  2. build-knowledge-catalog.py  mã băm của các file đăng ký trong catalog tri thức (và nút mới)
  3. task-board.py               tasks/BOARD.md từ các task card
  4. notes-index.py              docs/notes/INDEX.md từ hộp thư ghi chú

Dùng:
  python scripts/refresh.py           sinh lại tất cả (ghi file)
  python scripts/refresh.py --check   chỉ kiểm, không ghi gì; mã thoát 1 nếu có bước lệch

Chỉ dùng thư viện chuẩn. Dừng ở bước đầu tiên lỗi.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

# (tên, lệnh ghi file, lệnh chỉ kiểm)
STEPS = [
    ("adapters", ["scripts/sync-adapters.py"], ["scripts/sync-adapters.py", "--check"]),
    ("catalog", ["scripts/build-knowledge-catalog.py"],
     ["scripts/knowledge.py", "validate", "--root", ".", "--manifest", "agents/knowledge/knowledge-manifest.json"]),
    ("task-board", ["scripts/task-board.py"], ["scripts/task-board.py", "--check"]),
    ("notes-index", ["scripts/notes-index.py"], ["scripts/notes-index.py", "--check"]),
]


def run(args):
    return subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description="Sinh lại hoặc kiểm các file sinh tự động mà CI yêu cầu.")
    parser.add_argument("--check", action="store_true", help="Chỉ kiểm, không ghi file")
    args = parser.parse_args()

    failed = []
    for name, write_cmd, check_cmd in STEPS:
        proc = run(check_cmd if args.check else write_cmd)
        tail = (proc.stdout.strip().splitlines() or [""])[-1]
        status = "OK " if proc.returncode == 0 else "LỖI"
        print(f"[{status}] {name}: {tail}")
        if proc.returncode != 0:
            failed.append(name)
            print(proc.stdout[-800:] + proc.stderr[-800:])
            if not args.check:
                break
    if failed:
        print(f"Bước lỗi hoặc lệch: {', '.join(failed)}")
        sys.exit(1)
    print("Tất cả đã khớp." if args.check else "Đã sinh lại tất cả.")


if __name__ == "__main__":
    main()
