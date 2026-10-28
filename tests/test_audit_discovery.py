import os
import shutil
import tempfile
import unittest
from pathlib import Path
import subprocess
import sys


class TestAuditDiscovery(unittest.TestCase):
    def test_card_audit_runs_cleanly(self):
        cmd = [sys.executable, "scripts/card-audit.py"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0, f"card-audit.py failed with: {res.stderr}")
        self.assertIn("0 lỗi", res.stdout)

    def test_next_py_runs_cleanly(self):
        cmd = [sys.executable, "scripts/next.py"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0, f"next.py failed with: {res.stderr}")
        self.assertIn("CẦN NGHIỆM THU", res.stdout)


if __name__ == "__main__":
    unittest.main()
