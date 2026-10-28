"""Kiểm thử CLI scripts/skill-eval.py với cờ --evidence-mode và --evidence-root."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestSkillEvalCliEvidence(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="cli-evidence-test-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        (self.tmp / "SKILL.md").write_text("# Test Skill\n", encoding="utf-8")
        (self.tmp / "rubric.json").write_text(
            json.dumps({"skill": "test", "items": [{"id": "c1", "description": "d", "weight": 1}]}),
            encoding="utf-8",
        )
        (self.tmp / "tasks.json").write_text(
            json.dumps([{"name": "t1", "prompt": "p1"}, {"name": "t2", "prompt": "p2"}]),
            encoding="utf-8",
        )
        # Runner script tạo artifact trong sandbox
        (self.tmp / "runner.py").write_text(
            "import os, sys\n"
            "with open('artifact.txt', 'w', encoding='utf-8') as f:\n"
            "    f.write('artifact from runner')\n"
            "print('RUNNER SUCCESS')\n",
            encoding="utf-8",
        )
        # Judge script
        (self.tmp / "judge.py").write_text(
            "import json, sys\n"
            "r = json.load(open(sys.argv[1], encoding='utf-8'))\n"
            "print(json.dumps({'scores': {i['id']: 10.0 for i in r['items']}}))\n",
            encoding="utf-8",
        )

    def test_cli_evidence_mode_collects_artifacts_and_reports_v2(self):
        evidence_dir = self.tmp / "evidence_out"
        report_file = self.tmp / "report.md"
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "skill-eval.py"),
            "run",
            "--skill", str(self.tmp / "SKILL.md"),
            "--rubric", str(self.tmp / "rubric.json"),
            "--tasks", str(self.tmp / "tasks.json"),
            "--models", "dummy/model-a",
            "--judge", "other/judge-b",
            "--runner-cmd", f'"{sys.executable}" "{self.tmp / "runner.py"}"',
            "--judge-cmd", f'"{sys.executable}" "{self.tmp / "judge.py"}" {{rubric_file}}',
            "--evidence-mode",
            "--evidence-root", str(evidence_dir),
            "--case-min-score", "8.0",
            "--out", str(report_file),
            "--allow-same-family",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", cwd=str(self.tmp))
        self.assertEqual(proc.returncode, 0, f"CLI thất bại: {proc.stderr}")
        self.assertIn("[Evidence Mode v2]", proc.stdout)
        self.assertIn("Critical Fails: 0", proc.stdout)
        self.assertIn("Inconclusive Cases: 0", proc.stdout)
        self.assertIn("Đạt mục tiêu v2: có", proc.stdout)

        # Kiểm tra evidence_dir có chứa artifacts đã được thu thập
        collected = list(evidence_dir.rglob("artifact.txt"))
        self.assertGreaterEqual(len(collected), 2, "Artifact phải được thu thập cho cả 2 task trước khi dọn sandbox")
        self.assertTrue(report_file.exists())


if __name__ == "__main__":
    unittest.main()
