#!/usr/bin/env python3
"""
scripts/setup-skills.py
Trợ lý Khởi Tạo & Thiết Lập Kỹ Năng Cho Dự Án Mới (Interactive Setup Wizard)
Chạy chế độ tương tác hỏi đáp của scripts/fetch-skills.py.
"""
import sys
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
fetch_script = root / "scripts" / "fetch-skills.py"

if __name__ == "__main__":
    cmd = [sys.executable, str(fetch_script), "--interactive"] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))
