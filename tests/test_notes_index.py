"""Tests for scripts/notes-index.py: sinh INDEX từ hộp thư ghi chú.

Mọi ca chạy script qua subprocess với `sys.executable --root=<tempdir>`,
không bao giờ đụng `docs/notes/` thật.

Run: python -m unittest discover -s tests -p "test_notes_index.py" -v
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "notes-index.py"
TIMEOUT = 60


def run(root, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), f"--root={root}", *args],
        capture_output=True, text=True, timeout=TIMEOUT, encoding="utf-8", env=env,
    )


def write_note(inbox, name, body):
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / name).write_text(body, encoding="utf-8")


class NotesIndexTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.inbox = self.root / "docs" / "notes" / "inbox"
        self.index = self.root / "docs" / "notes" / "INDEX.md"

    def tearDown(self):
        self._tmp.cleanup()

    def test_generates_row_per_note_with_summary(self):
        write_note(self.inbox, "T-01-dev.md", "> summary: mot dieu can biet\n\nTask: T-01\n")
        write_note(self.inbox, "T-02-qa.md", "# Sub: T-02.1\n> summary: qa nghiem thu\n")
        proc = run(self.root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        text = self.index.read_text(encoding="utf-8")
        self.assertIn("`docs/notes/inbox/T-01-dev.md` | T-01 | mot dieu can biet", text)
        self.assertIn("`docs/notes/inbox/T-02-qa.md` | T-02 | qa nghiem thu", text)

    def test_frontmatter_summary_also_accepted(self):
        write_note(self.inbox, "T-03-dev.md", "---\nsummary: tu frontmatter\n---\n\nnoi dung\n")
        run(self.root)
        self.assertIn("| T-03 | tu frontmatter |", self.index.read_text(encoding="utf-8"))

    def test_missing_summary_flagged_by_check(self):
        write_note(self.inbox, "T-04-dev.md", "Task: T-04 khong co summary\n")
        run(self.root)
        proc = run(self.root, "--check")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("T-04-dev.md", proc.stdout)

    def test_idempotent_and_check_passes(self):
        write_note(self.inbox, "T-05-dev.md", "> summary: du dung\n")
        first = run(self.root)
        second = run(self.root)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(second.returncode, 0)
        check = run(self.root, "--check")
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_stale_index_fails_check(self):
        write_note(self.inbox, "T-06-dev.md", "> summary: note dau\n")
        run(self.root)
        write_note(self.inbox, "T-07-dev.md", "> summary: note moi chua vao index\n")
        proc = run(self.root, "--check")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("INDEX.md", proc.stdout)

    def test_empty_inbox_renders_placeholder(self):
        proc = run(self.root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("| — | — |", self.index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
