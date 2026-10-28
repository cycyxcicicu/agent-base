import os
import shutil
import tempfile
import unittest
from pathlib import Path
import subprocess
import sys


class TestTaskBoardDiscovery(unittest.TestCase):
    def test_task_board_runs_cleanly(self):
        # Chạy scripts/task-board.py trên repo thật
        cmd = [sys.executable, "scripts/task-board.py"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0, f"task-board.py failed with: {res.stderr}")
        self.assertIn("0 lỗi", res.stdout)


if __name__ == "__main__":
    unittest.main()
