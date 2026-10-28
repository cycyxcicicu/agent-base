#!/usr/bin/env python3
"""
scripts/generate-dashboard.py
Điểm vào mỏng: sinh bảng điều khiển trực quan vào build/viewer/ (mở build/viewer/index.html trên trình duyệt).
Mã nằm ở tools/viewer/dashboard/ (collect.py: thu thập dữ liệu, render.py: dựng site), giao diện ở tools/viewer/assets/.
Tự thích ứng với mọi dự án theo khung AGENTS.md (PROJECT.md, tasks/EPICS.md, tasks/**/T-*.md, docs/).

Cách dùng:
  python scripts/generate-dashboard.py
"""

import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools' / 'viewer'))

from dashboard.render import main  # noqa: E402

if __name__ == '__main__':
    sys.exit(main())
