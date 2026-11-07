"""Kiểm thử quy ước đặt tên task có nghĩa: file T-<số>-<slug>.md, cảnh báo tên vô nghĩa, merge-gate và worktree nhận slug."""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent_core.workflow.task_discovery import parse_task_frontmatter  # noqa: E402


def load_script(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CARD = "---\nid: {id}\nstatus: todo\nscope_edit:\n  - src/**\nscope_deny:\n  - AGENTS.md\n---\n# {id}: {title}\n"


class TestSlugFromFilename(unittest.TestCase):
    def test_slug_comes_from_the_file_name(self):
        meta = parse_task_frontmatter(CARD.format(id="T-12", title="Chuẩn hóa tên task"),
                                      Path("tasks/E1/T-12-docs-chuan-hoa-ten-task.md"))
        self.assertEqual(meta["slug"], "docs-chuan-hoa-ten-task")
        self.assertEqual(meta["title"], "Chuẩn hóa tên task")

    def test_subtask_slug(self):
        meta = parse_task_frontmatter(CARD.format(id="T-12.1", title="Viết kiểm tra"), Path("T-12.1-test-viet-kiem-tra.md"))
        self.assertEqual(meta["slug"], "test-viet-kiem-tra")

    def test_bare_id_file_has_no_slug(self):
        meta = parse_task_frontmatter(CARD.format(id="T-5", title="Việc cũ"), Path("tasks/T-5.md"))
        self.assertEqual(meta["slug"], "")


class TestNameWarnings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = load_script("task_board", "task-board.py")

    def card(self, **kw):
        base = {"id": "T-1", "file": "tasks/E1/T-1-feat-them-cot-an-hien.md", "slug": "feat-them-cot-an-hien",
                "title": "Thêm cột ẩn hiện", "is_example": False}
        base.update(kw)
        return base

    def test_good_name_has_no_warning(self):
        self.assertEqual(self.board.name_warnings([self.card()]), [])

    def test_bare_id_file_is_warned(self):
        w = self.board.name_warnings([self.card(file="tasks/E1/T-1.md", slug="")])
        self.assertTrue(any("chỉ có mã" in x for x in w), w)

    def test_bad_slug_is_warned(self):
        w = self.board.name_warnings([self.card(slug="Them_Cot")])
        self.assertTrue(any("slug" in x for x in w), w)
        w = self.board.name_warnings([self.card(slug="a" * 41)])
        self.assertTrue(any("tối đa 40" in x for x in w), w)

    def test_slug_must_start_with_a_task_type(self):
        w = self.board.name_warnings([self.card(slug="them-cot-an-hien")])
        self.assertTrue(any("loại việc" in x for x in w), w)
        for good in ("fix-loi-xuat-excel", "feat-them-cot", "docs-chuan-hoa-ten-task", "refactor-tach-service", "hotfix-sua-gap"):
            self.assertEqual(self.board.name_warnings([self.card(slug=good)]), [], good)

    def test_missing_or_code_title_is_warned(self):
        for title in ("", "T-1 gì đó"):
            w = self.board.name_warnings([self.card(title=title)])
            self.assertTrue(any("tiêu đề" in x for x in w), (title, w))

    def test_example_cards_are_skipped(self):
        self.assertEqual(self.board.name_warnings([self.card(file="tasks/T-1.md", slug="", title="", is_example=True)]), [])


class TestMergeGateAcceptsSlugCard(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="gate-name-"))
        self.addCleanup(shutil.rmtree, str(self.repo), True)
        for args in (["init", "-q", "-b", "develop"], ["config", "user.email", "t@example.com"], ["config", "user.name", "Human"],
                     ["config", "core.autocrlf", "false"]):
            self.git(*args)
        self.write("AGENTS.md", "# rules\n")
        self.write("src/a.py", "print(1)\n")
        self.write("tasks/E1-x/T-1-them-cot-an-hien.md", CARD.format(id="T-1", title="Thêm cột ẩn hiện"))
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")

    def git(self, *args):
        r = subprocess.run(["git", *args], cwd=self.repo, capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            raise AssertionError(r.stderr)

    def write(self, rel, text):
        p = self.repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="")

    def gate(self):
        gate = Path(os.environ.get("MERGE_GATE_SCRIPT", str(ROOT / "scripts" / "merge-gate.py")))
        return subprocess.run([sys.executable, str(gate), "--branch", "feature/1-them-cot-an-hien", "--card",
                               "tasks/E1-x/T-1-them-cot-an-hien.md", "--base", "develop"],
                              cwd=self.repo, capture_output=True, text=True, encoding="utf-8")

    def test_card_and_note_with_slug_are_allowed_besides_scope_files(self):
        self.git("checkout", "-q", "-b", "feature/1-them-cot-an-hien")
        self.write("src/a.py", "print(2)\n")
        self.write("tasks/E1-x/T-1-them-cot-an-hien.md",
                   CARD.format(id="T-1", title="Thêm cột ẩn hiện") + "\n## Nhật ký phiên\n- xong\n")
        self.write("docs/notes/inbox/T-1-them-cot-an-hien-dev.md",
                   "không có lưu ý\n- Skill đã chọn & áp dụng: springboot-patterns\n- Checklist đã tuân thủ: controller\n- Tra cứu mã nguồn (XERJ/AST): PASS\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "change")
        r = self.gate()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_file_outside_scope_still_fails(self):
        self.git("checkout", "-q", "-b", "feature/1-them-cot-an-hien")
        self.write("AGENTS.md", "# changed\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "change")
        self.assertNotEqual(self.gate().returncode, 0)


if __name__ == "__main__":
    unittest.main()
