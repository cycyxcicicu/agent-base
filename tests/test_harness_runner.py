import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestHarnessRunner(unittest.TestCase):
    def test_harness_runner_status(self):
        cmd = [sys.executable, str(ROOT / "scripts" / "harness-runner.py"), "--status"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("HARNESS² ENGINE STATUS", res.stdout)
        self.assertIn("SẴN SÀNG THỰC THI", res.stdout)

    def test_harness_runner_probe(self):
        cmd = [sys.executable, str(ROOT / "scripts" / "harness-runner.py"), "--probe", "--task", "T-TEST"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("TASK-LEVEL PROBING", res.stdout)
        self.assertIn("Propose – Probe – Compose", res.stdout)


if __name__ == "__main__":
    unittest.main()
