import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Module sẽ cài đặt
from agent_core.verification.repro import (
    run_repro_harness,
    run_verify_mode,
    ReproResult,
)


class TestVerifyReproContract(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.evidence_root = Path(self.tmp_dir) / "evidence"
        self.evidence_root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_reproduced_when_bug_occurs_both_times_after_reset(self):
        # Kịch bản lỗi: Luôn trả exit 1
        recipe = {
            "name": "repro-always-fail",
            "command": ["python", "-c", "import sys; sys.exit(1)"],
            "expected_bug_exit_code": 1,
            "reset_action": "noop",
        }
        res = run_repro_harness(recipe, evidence_root=self.evidence_root)
        self.assertEqual(res.verdict, "reproduced")
        self.assertEqual(res.run_count, 2)
        self.assertTrue(res.proof_path.is_file())

    def test_not_reproduced_when_bug_does_not_occur(self):
        # Kịch bản bình thường: Luôn trả exit 0
        recipe = {
            "name": "repro-always-pass",
            "command": ["python", "-c", "import sys; sys.exit(0)"],
            "expected_bug_exit_code": 1,
            "reset_action": "noop",
        }
        res = run_repro_harness(recipe, evidence_root=self.evidence_root)
        self.assertEqual(res.verdict, "not_reproduced")
        self.assertEqual(res.run_count, 2)

    def test_inconclusive_when_results_flaky(self):
        # Lần 1 fail, lần 2 pass -> flaky -> inconclusive
        # Mô phỏng bằng counter file
        counter_file = Path(self.tmp_dir) / "counter.txt"
        counter_file.write_text("0", encoding="utf-8")
        script = f"""
from pathlib import Path
p = Path(r'{counter_file}')
val = int(p.read_text())
p.write_text(str(val + 1))
import sys
sys.exit(1 if val == 0 else 0)
"""
        recipe = {
            "name": "repro-flaky",
            "command": ["python", "-c", script],
            "expected_bug_exit_code": 1,
            "reset_action": "noop",  # không reset counter khiến lần 2 khác lần 1
        }
        res = run_repro_harness(recipe, evidence_root=self.evidence_root)
        self.assertEqual(res.verdict, "inconclusive")

    def test_verify_mode_baseline_fails_and_patch_passes(self):
        # Chế độ verify: baseline thấy lỗi 2/2, sau khi patch hết lỗi 0/2 -> verify PASS
        flag_file = Path(self.tmp_dir) / "patched.flag"

        test_script = f"""
from pathlib import Path
import sys
flag = Path(r'{flag_file}')
# Nếu chưa patched -> exit 1 (bug), nếu patched -> exit 0 (clean)
sys.exit(0 if flag.is_file() else 1)
"""
        def patch_action():
            flag_file.write_text("patched", encoding="utf-8")

        recipe = {
            "name": "verify-fix",
            "command": ["python", "-c", test_script],
            "expected_bug_exit_code": 1,
            "reset_action": "noop",
        }
        v_res = run_verify_mode(recipe, patch_fn=patch_action, evidence_root=self.evidence_root)
        self.assertEqual(v_res.verdict, "pass")
        self.assertTrue(v_res.baseline_reproduced)
        self.assertTrue(v_res.patch_clean)


if __name__ == "__main__":
    unittest.main()
