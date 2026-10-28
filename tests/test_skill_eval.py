"""Kiểm thử agent_core/eval/skill_eval.py bằng runner/judge/improver giả (không gọi model nào).
Viết bằng unittest (CI chạy `python -m unittest discover -s tests`, không cài pytest)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent_core.eval.skill_eval import (  # noqa: E402
    EvalTask, Rubric, RubricItem, check_judge_independent, draft_rubric, extract_json, hill_climb, make_sandbox,
    model_family, render_report, run_matrix, weighted_score,
)

RUBRIC = Rubric("demo", [RubricItem("a", "tiêu chí a", 2.0), RubricItem("b", "tiêu chí b", 1.0)])
TASKS = [EvalTask("t1", "việc 1"), EvalTask("t2", "việc 2")]


def judge_by_marker(judge_model, rubric, task, output):
    good = "GOOD" in output
    return {"a": 10 if good else 4, "b": 10 if good else 6}


class SkillEvalCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix='skill-eval-test-')
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)


class TestCore(SkillEvalCase):
    def test_model_family(self):
        self.assertEqual(model_family("anthropic/claude-sonnet-5"), "claude")
        self.assertEqual(model_family("gpt-5.1"), "gpt")
        self.assertEqual(model_family("9router/gemini-2-pro"), "gemini")

    def test_judge_must_be_independent(self):
        with self.assertRaises(ValueError):
            check_judge_independent(["claude-a", "gpt-b"], "claude-a")
        with self.assertRaises(ValueError):
            check_judge_independent(["claude-a"], "claude-z")  # cùng họ
        check_judge_independent(["claude-a", "gpt-b"], "gemini-c")
        check_judge_independent(["claude-a"], "claude-z", allow_same_family=True)

    def test_weighted_score_and_missing_item(self):
        self.assertEqual(weighted_score(RUBRIC, {"a": 10, "b": 4}), 8.0)
        with self.assertRaises(ValueError):
            weighted_score(RUBRIC, {"a": 10})

    def test_sandbox_names_are_random_and_neutral(self):
        names = {make_sandbox(self.tmp).name for _ in range(5)}
        self.assertEqual(len(names), 5)
        self.assertTrue(all("eval" not in n and "test" not in n for n in names))

    def test_matrix_scores_each_model_and_cleans_sandbox(self):
        seen = []

        def runner(model, skill, prompt, sandbox):
            seen.append(sandbox)
            self.assertTrue(sandbox.is_dir())
            return "GOOD" if model == "m1" else "bad"

        res = run_matrix("skill", TASKS, ["m1", "m2"], "judgeX", RUBRIC, runner, judge_by_marker, self.tmp)
        self.assertEqual(res.per_model(), {"m1": 10.0, "m2": 4.67})
        self.assertFalse(res.passed(10.0))
        self.assertEqual(res.min_model_score(), 4.67)
        self.assertTrue(all(not p.exists() for p in seen), "sandbox phải được dọn sau mỗi lượt")

    def _evaluate(self, text):
        return run_matrix(text, TASKS, ["m1"], "judgeX", RUBRIC, lambda m, s, p, sb: s, judge_by_marker, self.tmp)

    def test_hill_climb_keeps_better_and_stops_at_target(self):
        out = hill_climb("bad", self._evaluate, lambda text, report: text + " GOOD", RUBRIC, target=10.0, max_rounds=5)
        self.assertTrue(out.reached_target)
        self.assertIn("GOOD", out.best_text)
        self.assertLess(out.history[0], out.history[-1])

    def test_hill_climb_never_keeps_worse_and_respects_patience(self):
        out = hill_climb("GOOD but not perfect", self._evaluate, lambda t, r: "worse", RUBRIC,
                         target=10.0, max_rounds=10, patience=2)
        self.assertEqual(out.best_text, "GOOD but not perfect")
        self.assertLessEqual(out.rounds, 4, "phải dừng sau 2 vòng liền không cải thiện")


class TestCli(SkillEvalCase):
    def setUp(self):
        super().setUp()
        t = self.tmp
        (t / "SKILL.md").write_text("# s\n", encoding="utf-8")
        (t / "rubric.json").write_text('{"skill":"s","items":[{"id":"a","description":"d","weight":1}]}', encoding="utf-8")
        (t / "tasks.json").write_text('[{"name":"t","prompt":"p"}]', encoding="utf-8")
        (t / "runner.py").write_text("print('GOOD')\n", encoding="utf-8")
        (t / "judge.py").write_text(
            "import json,sys\nr=json.load(open(sys.argv[1],encoding='utf-8'))\n"
            "print(json.dumps({'scores':{i['id']:10 for i in r['items']}}))\n", encoding="utf-8")

    def cli(self, action, *extra):
        cmd = [sys.executable, str(ROOT / "scripts" / "skill-eval.py"), action,
               "--skill", str(self.tmp / "SKILL.md"), "--rubric", str(self.tmp / "rubric.json"),
               "--tasks", str(self.tmp / "tasks.json"), *extra]
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    def test_plan_rejects_same_family_judge(self):
        r = self.cli("plan", "--models", "claude-a", "--judge", "claude-z")
        self.assertEqual(r.returncode, 2)
        self.assertIn("cùng họ", r.stdout)

    def test_run_end_to_end_with_external_commands(self):
        py = Path(sys.executable).as_posix()
        r = self.cli("run", "--models", "claude-a,gpt-b", "--judge", "gemini-c",
                     "--runner-cmd", f"{py} {(self.tmp / 'runner.py').as_posix()}",
                     "--judge-cmd", f"{py} {(self.tmp / 'judge.py').as_posix()} {{rubric_file}}", "--target", "10")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Đạt mục tiêu: có", r.stdout)
        self.assertEqual((self.tmp / "SKILL.md").read_text(encoding="utf-8"), "# s\n", "không được ghi đè SKILL.md")


class TestStabilityAndRubric(SkillEvalCase):
    def test_spread_weakest_and_report_warning(self):
        def runner(model, skill, prompt, sandbox):
            return "GOOD" if model == "m1" else "bad"

        res = run_matrix("s", TASKS, ["m1", "m2"], "judgeX", RUBRIC, runner, judge_by_marker, self.tmp)
        self.assertEqual(res.weakest_model(), "m2")
        self.assertEqual(res.spread(), 5.33)
        report = render_report(res, RUBRIC, 10.0, "judgeX")
        self.assertIn("Model yếu nhất: `m2`", report)
        self.assertIn("chưa ổn định giữa các model", report)

    def test_extract_json_handles_fences_and_prose(self):
        self.assertEqual(extract_json('Đây:\n```json\n{"a": 1}\n```\nxong'), {"a": 1})
        with self.assertRaises(ValueError):
            extract_json("không có json")

    def test_draft_rubric_uses_folder_name_and_checks_size(self):
        raw = 'nháp:\n' + json.dumps({"skill": "model-tu-ghi", "items": [
            {"id": "a", "description": "x"}, {"id": "b", "description": "y", "weight": 2}, {"id": "c", "description": "z"}]})
        rub = draft_rubric("ten-thu-muc", raw)
        self.assertEqual(rub.skill, "ten-thu-muc")
        self.assertEqual([i.weight for i in rub.items], [1.0, 2.0, 1.0])
        with self.assertRaises(ValueError):  # chỉ 1 tiêu chí
            draft_rubric("s", json.dumps({"items": [{"id": "a", "description": "x"}]}))
        with self.assertRaises(ValueError):  # trùng mã
            draft_rubric("s", json.dumps({"items": [{"id": "a", "description": "x"}] * 3}))


class TestExamplesAndDisguise(SkillEvalCase):
    EX = ROOT / "examples" / "skill-eval"

    def py(self, name):
        # Đường dẫn có dấu cách (ví dụ "D:/OneDrive - x/...") phải nằm trong nháy kép vì lệnh được tách bằng shlex
        return f'"{Path(sys.executable).as_posix()}" "{(self.EX / name).as_posix()}"'

    def run_cli(self, *argv):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "skill-eval.py"), *argv],
                              capture_output=True, text=True, encoding="utf-8")

    def test_example_files_are_valid(self):
        rub = Rubric.from_json((self.EX / "rubric.example.json").read_text(encoding="utf-8"))
        self.assertEqual(len(rub.items), 2)
        tasks = json.loads((self.EX / "tasks.example.json").read_text(encoding="utf-8"))
        self.assertEqual(len(tasks), 2)

    def test_example_hill_climb_reaches_target_without_touching_original(self):
        skill = self.tmp / "SKILL.example.md"
        skill.write_text((self.EX / "SKILL.example.md").read_text(encoding="utf-8"), encoding="utf-8")
        original = skill.read_text(encoding="utf-8")
        r = self.run_cli("run", "--skill", str(skill), "--rubric", str(self.EX / "rubric.example.json"),
                         "--tasks", str(self.EX / "tasks.example.json"), "--models", "claude-a,gpt-b", "--judge", "gemini-c",
                         "--runner-cmd", self.py("demo_runner.py") + " {model} {skill_file} {prompt_file}",
                         "--judge-cmd", self.py("demo_judge.py") + " {rubric_file} {task_file} {output_file}",
                         "--improver-cmd", self.py("demo_improver.py") + " {skill_file} {report_file}", "--target", "10")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Đạt mục tiêu: có", r.stdout)
        self.assertEqual(skill.read_text(encoding="utf-8"), original, "không được sửa skill gốc")
        best = self.tmp / "SKILL.example.best.md"
        self.assertTrue(best.is_file())
        self.assertIn("file:dòng", best.read_text(encoding="utf-8"))

    def test_readme_style_relative_paths_work_from_project_root(self):
        """Lệnh trong README dùng đường dẫn tương đối; runner chạy trong thư mục tạm nên script phải đổi sang đường dẫn tuyệt đối."""
        py = f'"{Path(sys.executable).as_posix()}"'
        r = subprocess.run(
            [sys.executable, "scripts/skill-eval.py", "run", "--skill", "examples/skill-eval/SKILL.example.md",
             "--rubric", "examples/skill-eval/rubric.example.json", "--tasks", "examples/skill-eval/tasks.example.json",
             "--models", "claude-a,gpt-b", "--judge", "gemini-c",
             "--runner-cmd", py + " examples/skill-eval/demo_runner.py {model} {skill_file} {prompt_file}",
             "--judge-cmd", py + " examples/skill-eval/demo_judge.py {rubric_file} {task_file} {output_file}",
             "--improver-cmd", py + " examples/skill-eval/demo_improver.py {skill_file} {report_file}", "--target", "10"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        best = ROOT / "examples" / "skill-eval" / "SKILL.example.best.md"
        self.addCleanup(lambda: best.unlink() if best.exists() else None)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Đạt mục tiêu: có", r.stdout)

    def test_rubric_action_writes_draft_named_after_folder(self):
        folder = self.tmp / "my-skill"
        folder.mkdir()
        (folder / "SKILL.md").write_text("# s\n", encoding="utf-8")
        out = self.tmp / "draft.json"
        r = self.run_cli("rubric", "--skill", str(folder / "SKILL.md"), "--out", str(out),
                         "--rubric-cmd", self.py("demo_rubric.py") + " {skill_file}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["skill"], "my-skill")
        self.assertEqual(len(data["items"]), 3)
        self.assertIn("BẢN NHÁP", r.stdout)

    def test_agent_under_test_never_sees_eval_in_paths(self):
        record = self.tmp / "argv.txt"
        probe = self.tmp / "probe.py"
        probe.write_text(
            "import sys\nopen(sys.argv[1], 'w', encoding='utf-8').write('\\n'.join(sys.argv[2:]))\nprint('GOOD')\n",
            encoding="utf-8")
        (self.tmp / "SKILL.md").write_text("# s\n", encoding="utf-8")
        py = Path(sys.executable).as_posix()
        r = self.run_cli("run", "--skill", str(self.tmp / "SKILL.md"), "--rubric", str(self.EX / "rubric.example.json"),
                         "--tasks", str(self.EX / "tasks.example.json"), "--models", "claude-a", "--judge", "gemini-c",
                         "--runner-cmd", f'"{py}" "{probe.as_posix()}" "{record.as_posix()}" {{skill_file}} {{prompt_file}} {{sandbox}}',
                         "--judge-cmd", self.py("demo_judge.py") + " {rubric_file} {task_file} {output_file}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for p in record.read_text(encoding="utf-8").splitlines():
            path = Path(p)
            for part in (path.name.lower(), path.parent.name.lower()):
                for word in ("eval", "test", "skill"):
                    self.assertNotIn(word, part, f"lộ '{word}' trong đường dẫn agent nhìn thấy: {p}")


class TestCommandTemplate(unittest.TestCase):
    """Hồi quy: dấu {} trong đường dẫn lệnh không được bị hiểu là placeholder."""

    @classmethod
    def setUpClass(cls):
        import importlib.util
        spec = importlib.util.spec_from_file_location("skill_eval_cli", ROOT / "scripts" / "skill-eval.py")
        cls.cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.cli)

    def test_known_placeholder_is_filled(self):
        self.assertEqual(self.cli._fill("{model}", {"model": "gpt-5"}), "gpt-5")

    def test_literal_braces_in_path_are_kept(self):
        path = r"C:\Temp\sandbox.{3a6989c8-9c48-4fb5-948b-913e5142d8bb}\AC\runner.py"
        self.assertEqual(self.cli._fill(path, {"model": "m"}), path)

    def test_mixed_path_and_placeholder(self):
        out = self.cli._fill(r"C:\sandbox.{UUID}\{prompt_file}", {"prompt_file": "p.txt"})
        self.assertEqual(out, r"C:\sandbox.{UUID}\p.txt")


if __name__ == "__main__":
    unittest.main()
