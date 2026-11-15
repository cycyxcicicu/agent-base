#!/usr/bin/env python3
"""tests/test_safe_exec.py

Unit test cho công cụ scripts/safe-exec.py (nén và gọt output thông minh chống Context Rot).
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("safe_exec", str(ROOT / "scripts" / "safe-exec.py"))
safe_exec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(safe_exec)


class TestSafeExec(unittest.TestCase):
    def test_short_output_not_compressed(self):
        lines = [f"line {i}" for i in range(15)]
        compressed, folded = safe_exec.compress_output(lines, max_lines=30)
        self.assertEqual(compressed, lines)
        self.assertEqual(folded, 0)

    def test_long_output_folded_correctly(self):
        lines = [f"info line {i}" for i in range(100)]
        compressed, folded = safe_exec.compress_output(lines, max_lines=20, head_count=5, tail_count=5)
        self.assertLessEqual(len(compressed), 20)
        self.assertGreater(folded, 0)
        has_fold_notice = any("... [gập" in l for l in compressed)
        self.assertTrue(has_fold_notice)
        self.assertEqual(compressed[0], "info line 0")
        self.assertEqual(compressed[-1], "info line 99")

    def test_error_and_traceback_preservation(self):
        lines = [f"setup step {i}" for i in range(50)]
        lines.append("Traceback (most recent call last):")
        lines.append('  File "app.py", line 42, in test_something')
        lines.append("AssertionError: expected True but got False")
        for i in range(50):
            lines.append(f"teardown step {i}")
        lines.append("Ran 1 test in 0.05s - FAILED (failures=1)")

        compressed, folded = safe_exec.compress_output(lines, max_lines=30)
        compressed_text = "\n".join(compressed)

        self.assertIn("AssertionError", compressed_text)
        self.assertIn("Traceback", compressed_text)
        self.assertIn("FAILED", compressed_text)

    def test_error_line_detection(self):
        self.assertTrue(safe_exec.is_error_or_summary_line("Exception: Database connection refused"))
        self.assertTrue(safe_exec.is_error_or_summary_line("ERROR: Failed to compile module"))
        self.assertTrue(safe_exec.is_error_or_summary_line("FAILED (failures=2, errors=1)"))
        self.assertTrue(safe_exec.is_error_or_summary_line("BUILD FAILURE"))
        self.assertFalse(safe_exec.is_error_or_summary_line("Downloading package version 1.2.3..."))
        self.assertFalse(safe_exec.is_error_or_summary_line("Scanning dependencies"))

    def test_execute_command_success(self):
        res = safe_exec.execute_command("echo 'hello world'", max_lines=10)
        self.assertEqual(res["exit_code"], 0)
        self.assertIn("hello world", res["output"])
        self.assertEqual(res["timed_out"], False)

    def test_execute_command_failure_exit_code(self):
        res = safe_exec.execute_command("python3 -c 'import sys; sys.exit(42)'", max_lines=10)
        self.assertEqual(res["exit_code"], 42)


if __name__ == "__main__":
    unittest.main()
