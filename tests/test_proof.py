import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

# Module sẽ cài đặt
from agent_core.verification.proof import (
    validate_proof_bundle,
    ProofBundle,
    CommandRecord,
    ArtifactRecord,
    AssertionRecord,
    TraceRecord,
)


class TestProofContract(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def _sample_valid_proof_dict(self) -> dict:
        return {
            "schema_version": 1,
            "run_id": "run-20261028-001",
            "scenario_id": "bootstrap-clean",
            "phase": "final",
            "started_at": "2026-10-28T00:00:00Z",
            "ended_at": "2026-10-28T00:00:10Z",
            "result": "pass",
            "repo_revision": "abc1234567890abcdef1234567890abcdef12345678",
            "dirty_input_manifest": [],
            "input_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "tool_versions": {"python": "3.11.4"},
            "commands": [
                {
                    "sequence": 1,
                    "argv": ["python", "-m", "unittest"],
                    "cwd_rel": ".",
                    "timeout_sec": 30,
                    "exit_code": 0,
                    "duration_ms": 150,
                    "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                }
            ],
            "assertions": [
                {
                    "id": "assert-1",
                    "expected": "0 errors",
                    "observed": "0 errors",
                    "passed": True,
                }
            ],
            "artifacts": [],
            "trace": [
                {
                    "sequence": 1,
                    "actor": "dev",
                    "action": "run_command",
                    "target": "python -m unittest",
                    "result": "exit_0",
                    "timestamp": "2026-10-28T00:00:01Z",
                    "capture": "observed",
                }
            ],
            "cleanup": {"performed": True, "clean": True, "errors": []},
            "limitations": ["Chạy trong môi trường isolated fixture"],
        }

    def test_valid_proof_passes_validation(self):
        data = self._sample_valid_proof_dict()
        errors = validate_proof_bundle(data)
        self.assertEqual(len(errors), 0, f"Validation errors: {errors}")

    def test_invalid_phase_enum_fails(self):
        data = self._sample_valid_proof_dict()
        data["phase"] = "unknown_phase"  # Chỉ cho phép 'baseline' hoặc 'final'
        errors = validate_proof_bundle(data)
        self.assertTrue(any("phase" in err for err in errors))

    def test_invalid_result_enum_fails(self):
        data = self._sample_valid_proof_dict()
        data["result"] = "maybe"  # Chỉ cho phép pass, fail, inconclusive, skipped
        errors = validate_proof_bundle(data)
        self.assertTrue(any("result" in err for err in errors))

    def test_extra_properties_rejected(self):
        data = self._sample_valid_proof_dict()
        data["unauthorized_secret_field"] = "evil"
        errors = validate_proof_bundle(data)
        self.assertTrue(any("additionalProperties" in err or "unauthorized_secret_field" in err for err in errors))

    def test_path_escape_in_artifact_fails(self):
        data = self._sample_valid_proof_dict()
        data["artifacts"] = [
            {
                "path_rel": "../outside.txt",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "byte_count": 0,
                "media_type": "text/plain",
            }
        ]
        errors = validate_proof_bundle(data)
        self.assertTrue(any("outside.txt" in err or "escape" in err.lower() for err in errors))


    def test_proof_check_detects_modified_artifact_and_missing_file(self):
        import subprocess
        import sys
        import hashlib

        # Tạo một proof bundle hợp lệ kèm artifact
        run_dir = Path(self.tmp_dir) / "run-001"
        run_dir.mkdir()

        art_file = run_dir / "output.txt"
        content = b"original output content"
        art_file.write_bytes(content)
        art_sha = hashlib.sha256(content).hexdigest()

        data = self._sample_valid_proof_dict()
        data["artifacts"] = [
            {
                "path_rel": "output.txt",
                "sha256": art_sha,
                "byte_count": len(content),
                "media_type": "text/plain",
            }
        ]
        proof_json = run_dir / "proof.json"
        proof_json.write_text(json.dumps(data), encoding="utf-8")

        # 1. Chạy proof-check -> exit 0
        cmd = [sys.executable, "scripts/proof-check.py", "--bundle", str(proof_json)]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0)

        # 2. Sửa 1 byte của artifact -> exit 1
        art_file.write_bytes(b"modified output content")
        res_mod = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res_mod.returncode, 1)
        self.assertIn("Sai lệch băm SHA256", res_mod.stdout)

        # 3. Xóa artifact -> exit 1
        art_file.unlink()
        res_del = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res_del.returncode, 1)
        self.assertIn("Thiếu tệp artifact", res_del.stdout)


if __name__ == "__main__":
    unittest.main()
