"""Tests for scripts/check-skills.py: SKILL.md size warning and broken internal links.

Run: python -m unittest discover -s tests -p "test_check_skills.py" -v
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-skills.py"
SKILL_NAME = "demo-skill"


def front_matter():
    return f"---\nname: {SKILL_NAME}\ndescription: Demo skill used by the unit tests.\n---\n"


class CheckSkillsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.skill = self.root / SKILL_NAME
        self.skill.mkdir()

    def write_skill(self, body):
        skill_md = self.skill / "SKILL.md"
        skill_md.write_bytes((front_matter() + body).encode("utf-8"))
        return skill_md

    def run_check(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--path", str(self.skill)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(self.root),
        )

    def test_valid_skill_passes(self):
        self.write_skill("# Demo\n\nNothing to resolve here.\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_skill_over_line_limit_warns_without_failing(self):
        header_lines = front_matter().count("\n")
        body_lines = 501 - header_lines
        self.write_skill("\n".join(f"line {i + 1}" for i in range(body_lines)) + "\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN", result.stdout)
        self.assertIn("501", result.stdout)
        self.assertIn("500", result.stdout)

    def test_broken_internal_link_fails(self):
        self.write_skill("# Demo\n\nSee [notes](references/missing.md) for details.\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("BROKEN LINK", result.stdout)
        self.assertIn("references/missing.md", result.stdout)

    def test_links_inside_code_fences_and_inline_code_are_ignored(self):
        self.write_skill(
            "# Demo\n\n"
            "```markdown\n"
            "[table](references/fenced-missing.md)\n"
            "```\n\n"
            "~~~\n"
            "[tilde](references/tilde-missing.md)\n"
            "~~~\n\n"
            "Inline sample: `[inline](references/inline-missing.md)` is only an example.\n"
        )
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("BROKEN LINK", result.stdout)

    def test_existing_internal_link_passes(self):
        (self.skill / "references").mkdir()
        (self.skill / "references" / "notes.md").write_bytes(b"# Notes\n")
        self.write_skill(
            '# Demo\n\nSee [notes](references/notes.md "Notes title") and [top](#demo).\n'
        )
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
