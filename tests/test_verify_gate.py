"""Kiểm thử scripts/verify-gate.py (trusted Stop hook + 3-in-1 bundle)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "verify-gate.py"


class TestVerifyGate(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="verifygate-")
        self.addCleanup(self._tmp.cleanup)
        self.ws = Path(self._tmp.name) / "proj"
        self.ws.mkdir()
        self.trust_file = Path(self._tmp.name) / "trust.tsv"

    def test_untrusted_command_fails_open_and_trusted_command_blocks_with_exit_2_on_failure(self):
        claude = self.ws / "CLAUDE.md"
        claude.write_text("# Demo\n<!-- agentbase:verify: python3 -c 'import sys; sys.exit(1)' -->\n", encoding="utf-8")

        # Chưa trust -> Stop hook trả 0 (không tự chạy lệnh chưa duyệt)
        r_untrusted = subprocess.run(
            [sys.executable, str(SCRIPT), "hook", "--root", str(self.ws), "--trust-file", str(self.trust_file)],
            input=json.dumps({"cwd": str(self.ws)}),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r_untrusted.returncode, 0)

        # Trust lệnh thất bại -> Stop hook chặn exit 2
        r_trust = subprocess.run(
            [sys.executable, str(SCRIPT), "--trust", "--root", str(self.ws), "--trust-file", str(self.trust_file)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(r_trust.returncode, 0, r_trust.stdout + r_trust.stderr)

        r_fail = subprocess.run(
            [sys.executable, str(SCRIPT), "hook", "--root", str(self.ws), "--trust-file", str(self.trust_file)],
            input=json.dumps({"cwd": str(self.ws)}),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r_fail.returncode, 2)
        self.assertIn("thất bại", r_fail.stderr)

        # Đổi lệnh sang thành công mà chưa trust lại -> tự vô hiệu trust cũ (trả 0), sau đó trust lại -> PASS 0
        claude.write_text("# Demo\n<!-- agentbase:verify: python3 --version -->\n", encoding="utf-8")
        subprocess.run(
            [sys.executable, str(SCRIPT), "--trust", "--root", str(self.ws), "--trust-file", str(self.trust_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        r_ok = subprocess.run(
            [sys.executable, str(SCRIPT), "hook", "--root", str(self.ws), "--trust-file", str(self.trust_file)],
            input=json.dumps({"cwd": str(self.ws)}),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r_ok.returncode, 0)


if __name__ == "__main__":
    unittest.main()

