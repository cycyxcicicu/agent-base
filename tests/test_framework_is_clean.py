"""Giữ bộ khung sạch: dữ liệu chạy của dự án không được nằm trong repo agent-base (tests/ không được copy sang dự án)."""

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Dữ liệu chạy của một dự án. Ngoại lệ là file mẫu hoặc file khung.
PROJECT_DATA = [
    r"^docs/notes/inbox/(?!\.gitkeep$).+",
    r"^docs/notes/archive/.+",
    r"^docs/proposals/PRP-.+",
    r"^tasks/BOARD\.md$",
    r"^tasks/E[^/]+/.+",
    r"^scratch/.+",
    r"^\.local/.+",
]


class TestFrameworkIsClean(unittest.TestCase):
    def test_no_project_runtime_data_is_tracked(self):
        try:
            out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("không phải git repo")
        offenders = [f for f in out.splitlines() if any(re.match(p, f) for p in PROJECT_DATA)]
        self.assertEqual(offenders, [], f"Dữ liệu dự án nằm trong repo khung: {offenders[:10]}")


if __name__ == "__main__":
    unittest.main()
