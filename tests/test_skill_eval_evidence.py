"""Kiểm thử v2 cho agent_core/eval/skill_eval.py:
Khung eval có bằng chứng (evidence-based), chấm mù (blind judging),
chặn lỗi nghiêm trọng (critical fail) không bị điểm trung bình che.
"""
import math
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent_core.eval.skill_eval import (
    EvalTask,
    Rubric,
    RubricItem,
    run_matrix,
    run_matrix_with_evidence,
    EvidenceRequest,
    EvidenceCollector,
    SanitizedBundle,
    CellResult,
)

RUBRIC = Rubric("test-skill", [
    RubricItem("correctness", "Độ chính xác", 2.0),
    RubricItem("safety", "An toàn", 1.0),
])

TASKS = [
    EvalTask("task-1", "Giải quyết vấn đề A"),
    EvalTask("task-2", "Giải quyết vấn đề B"),
]


class TestSkillEvalEvidence(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="eval-evidence-test-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.evidence_root = self.tmp / "evidence"
        self.evidence_root.mkdir()

    def test_cleanup_before_judge_eliminated_in_v2(self):
        """Artifacts và trace được collector thu thập TRƯỚC khi sandbox bị xóa.
        Judge nhận được bundle chứa artifact hợp lệ dù sandbox đã bị dọn."""
        collected_artifacts = []

        def runner(model, skill, prompt, sandbox):
            artifact_file = sandbox / "output_artifact.txt"
            artifact_file.write_text("DỮ LIỆU BẰNG CHỨNG QUAN TRỌNG", encoding="utf-8")
            return "DONE WITH ARTIFACT"

        def judge(judge_model, rubric, task, bundle):
            self.assertIsInstance(bundle, SanitizedBundle)
            self.assertIn("output_artifact.txt", bundle.artifacts)
            artifact_path = bundle.artifacts["output_artifact.txt"]
            self.assertTrue(artifact_path.exists())
            collected_artifacts.append(artifact_path.read_text(encoding="utf-8"))
            return {"correctness": 10.0, "safety": 10.0}

        collector = EvidenceCollector(allowlist=["output_artifact.txt"])
        req = EvidenceRequest(
            skill_text="my skill",
            tasks=[TASKS[0]],
            models=["model-alpha"],
            judge_model="judge-omega",
            rubric=RUBRIC,
            evidence_root=self.evidence_root,
            allow_same_family=True,
        )

        res = run_matrix_with_evidence(req, runner, judge, collector)
        self.assertEqual(len(collected_artifacts), 1)
        self.assertEqual(collected_artifacts[0], "DỮ LIỆU BẰNG CHỨNG QUAN TRỌNG")
        self.assertTrue(res.passed_v2(target=10.0))

    def test_blind_bundle_sanitization(self):
        """Judge nhận SanitizedBundle: không có tên model thật, không lộ provider,
        thay bằng mã mù ngẫu nhiên (blind_id)."""
        seen_bundles = []

        def runner(model, skill, prompt, sandbox):
            return f"Kết quả từ model {model}"

        def judge(judge_model, rubric, task, bundle):
            seen_bundles.append(bundle)
            return {"correctness": 9.0, "safety": 9.0}

        req = EvidenceRequest(
            skill_text="skill text",
            tasks=[TASKS[0]],
            models=["anthropic/claude-3-opus", "openai/gpt-4o"],
            judge_model="google/gemini-1.5-pro",
            rubric=RUBRIC,
            evidence_root=self.evidence_root,
            allow_same_family=True,
        )

        res = run_matrix_with_evidence(req, runner, judge)
        self.assertEqual(len(seen_bundles), 2)
        for b in seen_bundles:
            self.assertTrue(b.blind_id.startswith("candidate_"))
            self.assertNotIn("claude", b.blind_id)
            self.assertNotIn("gpt", b.blind_id)
            self.assertNotIn("anthropic", b.blind_id)
            self.assertNotIn("openai", b.blind_id)

    def test_critical_fail_on_forbidden_access_or_fabricated_proof(self):
        """Thoát đường dẫn (path escape) hoặc ghi chỗ cấm bị bắt ở pha deterministic assertions
        và đánh dấu critical fail; passed_v2 phải False dù judge cho 10 điểm."""
        def runner(model, skill, prompt, sandbox):
            # Tạo file escape mô phỏng
            return {
                "output": "Đã cố tình đọc ghi ngoài sandbox",
                "path_escapes": ["../../etc/passwd"],
                "forbidden_writes": ["/root/.ssh/id_rsa"],
            }

        def judge(judge_model, rubric, task, bundle):
            return {"correctness": 10.0, "safety": 10.0}

        req = EvidenceRequest(
            skill_text="skill text",
            tasks=[TASKS[0]],
            models=["model-alpha"],
            judge_model="judge-omega",
            rubric=RUBRIC,
            evidence_root=self.evidence_root,
            allow_same_family=True,
        )

        res = run_matrix_with_evidence(req, runner, judge)
        self.assertGreater(res.critical_fails, 0)
        self.assertFalse(res.passed_v2(target=5.0))

    def test_nan_or_out_of_range_or_timeout_fails(self):
        """Điểm NaN hoặc ngoài khoảng [0, 10] không được ép thành pass."""
        def runner(model, skill, prompt, sandbox):
            return "Output"

        def judge_nan(judge_model, rubric, task, bundle):
            return {"correctness": float("nan"), "safety": 8.0}

        req = EvidenceRequest(
            skill_text="skill text",
            tasks=[TASKS[0]],
            models=["model-alpha"],
            judge_model="judge-omega",
            rubric=RUBRIC,
            evidence_root=self.evidence_root,
            allow_same_family=True,
        )

        res = run_matrix_with_evidence(req, runner, judge_nan)
        self.assertFalse(res.passed_v2(target=5.0))
        self.assertGreater(res.inconclusive_count, 0)

    def test_case_min_score_prevents_high_mean_from_masking_failures(self):
        """Một case điểm kém (dưới case_min_score) khiến passed_v2 = False dù mean >= target."""
        def runner(model, skill, prompt, sandbox):
            return "Output"

        def judge(judge_model, rubric, task, bundle):
            if task.name == "task-1":
                return {"correctness": 10.0, "safety": 10.0}  # 10.0
            else:
                return {"correctness": 4.0, "safety": 4.0}    # 4.0

        req = EvidenceRequest(
            skill_text="skill text",
            tasks=TASKS,
            models=["model-alpha"],
            judge_model="judge-omega",
            rubric=RUBRIC,
            evidence_root=self.evidence_root,
            allow_same_family=True,
            case_min_score=6.0,
            target=6.0,  # Mean = (10 + 4) / 2 = 7.0 >= 6.0
        )

        res = run_matrix_with_evidence(req, runner, judge)
        self.assertEqual(res.per_model()["model-alpha"], 7.0)
        # Mean đạt target 6.0, nhưng task-2 điểm 4.0 < case_min_score 6.0 -> passed_v2 phải False!
        self.assertFalse(res.passed_v2(target=6.0, case_min_score=6.0))

    def test_backward_compatibility_run_matrix_legacy(self):
        """run_matrix cũ vẫn hoạt động bình thường, giữ nguyên cấu trúc."""
        def runner(model, skill, prompt, sandbox):
            return "GOOD OUTPUT"

        def judge(judge_model, rubric, task, output):
            return {"correctness": 10.0, "safety": 10.0}

        res = run_matrix("skill", TASKS, ["m1"], "judgeX", RUBRIC, runner, judge, self.tmp, allow_same_family=True)
        self.assertEqual(res.per_model()["m1"], 10.0)
        self.assertTrue(res.passed(10.0))


if __name__ == "__main__":
    unittest.main()
