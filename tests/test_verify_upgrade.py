import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Module sẽ cài đặt
from agent_core.verification.upgrade import run_upgrade_verification
from agent_core.verification.proof import validate_proof_bundle


class TestVerifyUpgrade(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.evidence_root = Path(self.tmp_dir) / "evidence"
        self.evidence_root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_upgrade_verification_scenarios(self):
        proof_path = run_upgrade_verification(
            evidence_root=self.evidence_root,
            keep_fixture=False,
        )
        self.assertTrue(proof_path.is_file(), f"Proof file not found: {proof_path}")

        data = json.loads(proof_path.read_text(encoding="utf-8"))
        errors = validate_proof_bundle(data)
        self.assertEqual(len(errors), 0, f"Proof errors: {errors}")

        self.assertEqual(data["scenario_id"], "upgrade-flow")
        self.assertEqual(data["result"], "pass")

        # Kiểm tra đủ 4 assertions: preserve, conflict, dry-run, idempotent
        assertion_ids = [a["id"] for a in data["assertions"]]
        self.assertIn("assert-preserve-customization", assertion_ids)
        self.assertIn("assert-report-conflicts", assertion_ids)
        self.assertIn("assert-dry-run-safe", assertion_ids)
        self.assertIn("assert-idempotent-rerun", assertion_ids)


if __name__ == "__main__":
    unittest.main()
