import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Module sẽ cài đặt
from agent_core.verification.bootstrap import run_bootstrap_verification
from agent_core.verification.proof import validate_proof_bundle


class TestVerifyBootstrap(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.evidence_root = Path(self.tmp_dir) / "evidence"
        self.evidence_root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_bootstrap_verification_runs_in_isolated_fixture(self):
        # Chạy recipe bootstrap
        proof_path = run_bootstrap_verification(
            evidence_root=self.evidence_root,
            keep_fixture=False,
        )
        self.assertTrue(proof_path.is_file(), f"Proof file not found: {proof_path}")

        # Thẩm định proof
        data = json.loads(proof_path.read_text(encoding="utf-8"))
        errors = validate_proof_bundle(data)
        self.assertEqual(len(errors), 0, f"Proof errors: {errors}")

        self.assertEqual(data["scenario_id"], "bootstrap-clean")
        self.assertEqual(data["result"], "pass")
        self.assertTrue(data["cleanup"]["performed"])
        self.assertTrue(data["cleanup"]["clean"])

        # Kiểm tra commands được ghi nhận
        self.assertGreaterEqual(len(data["commands"]), 1)
        # Kiểm tra trace được ghi nhận
        self.assertGreaterEqual(len(data["trace"]), 1)


if __name__ == "__main__":
    unittest.main()
