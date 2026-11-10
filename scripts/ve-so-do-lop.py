#!/usr/bin/env python3
"""Giữ tên cũ cho tương thích. Dùng scripts/ve-so-do.py (mọi loại sơ đồ: class, flow, sequence, erd).

  python3 scripts/ve-so-do-lop.py <spec.json> [--check-only]   # tương đương ve-so-do.py, mặc định type = class
  python3 scripts/ve-so-do-lop.py --mau                         # tương đương ve-so-do.py --mau class
"""
import subprocess
import sys
from pathlib import Path

args = sys.argv[1:]
if args[:1] == ["--mau"]:
    args = ["--mau", "class"]
sys.exit(subprocess.call([sys.executable, str(Path(__file__).with_name("ve-so-do.py"))] + args))
