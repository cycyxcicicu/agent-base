#!/usr/bin/env python3
"""tests/test_trace_logger.py

Unit test cho công cụ scripts/trace-logger.py (Observability & Session Telemetry).
"""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("trace_logger", str(ROOT / "scripts" / "trace-logger.py"))
trace_logger = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(trace_logger)


class TestTraceLogger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.orig_trace_dir = trace_logger.TRACE_DIR
        trace_logger.TRACE_DIR = Path(self.temp_dir)

    def tearDown(self):
        trace_logger.TRACE_DIR = self.orig_trace_dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_log_and_summarize_session(self):
        sid = "TEST-SESSION-01"
        trace_logger.append_event(sid, "SESSION_START", {"task": "T-10", "agent": "dev"})
        trace_logger.append_event(sid, "TOOL_CALL", {"tool": "safe-exec", "status": "OK", "duration": 0.5})
        trace_logger.append_event(sid, "TOOL_CALL", {"tool": "xerj_search", "status": "OK", "duration": 0.2})
        trace_logger.append_event(sid, "TOOL_CALL", {"tool": "bad_tool", "status": "FAIL", "duration": 0.1})
        trace_logger.append_event(sid, "GATE_CHECK", {"status": "PASS"})
        trace_logger.append_event(sid, "SESSION_END", {"final_status": "SUCCESS"})

        summ = trace_logger.get_session_summary(sid)
        self.assertEqual(summ["session_id"], sid)
        self.assertEqual(summ["tool_calls"], 3)
        self.assertEqual(summ["tool_failures"], 1)
        self.assertEqual(summ["gates_passed"], 1)
        self.assertAlmostEqual(summ["tool_success_rate"], 66.7, places=1)
        self.assertEqual(len(summ["hotspots"]), 3)
        self.assertEqual(summ["hotspots"][0]["tool"], "safe-exec")


if __name__ == "__main__":
    unittest.main()
