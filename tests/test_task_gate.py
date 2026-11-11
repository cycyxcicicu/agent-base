"""Kiểm thử scripts/task-gate.py (Checklist AC, RH-1/RH-4/RH-10 Gate Integrity & Scope Lock)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "task-gate.py"


class TestTaskGate(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="taskgate-")
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def _write(self, rel: str, text: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def _git(self, *args: str):
        r = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)

    def _run(self, *args: str):
        r = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr

    def test_strict_ac_and_challenge_enforcement(self):
        card = self._write("doc/features/UC-06/tasks/T-UC06.4.md", """# Task T-UC06.4

## Tiêu chí nghiệm thu
- [x] AC-01: Lọc nhân viên theo phòng ban
- [ ] AC-02: Lọc theo quyền IAM
""")
        code, out = self._run("audit", "--root", str(self.root), "--card", str(card), "--strict-ac", "--require-challenge")
        self.assertEqual(code, 1, out)
        self.assertIn("AC-INCOMPLETE", out)
        self.assertIn("AC-02", out)
        self.assertIn("MISSING-CHALLENGE", out)

        card.write_text("""# Task T-UC06.4
Phương án A / Phương án B / Phương án C (Khuyến nghị): Lọc batch 1000, fallback 502.
- [x] AC-01: Lọc nhân viên theo phòng ban
- [x] AC-02: Lọc theo quyền IAM
""", encoding="utf-8")
        code2, out2 = self._run("audit", "--root", str(self.root), "--card", str(card), "--strict-ac", "--require-challenge")
        self.assertEqual(code2, 0, out2)
        self.assertIn("PASS", out2)

    def test_gate_integrity_detects_rh1_rh4_and_rh10_in_diff(self):
        self._git("init", "-q", "-b", "develop")
        self._git("config", "user.email", "t@example.com")
        self._git("config", "user.name", "Tester")
        self._write("doc/features/UC-06/spec.md", "## A/C\n- [ ] AC-01: Bắt buộc lọc theo quyền\n")
        self._write("src/test/java/FooTest.java", "@Test\nvoid shouldWork() {}\n")
        self._write("src/main/java/FooService.java", "class FooService { int run() { return 1; } }\n")
        self._git("add", "-A")
        self._git("commit", "-q", "-m", "base")

        # Tạo nhánh mới và mô phỏng 3 kiểu lỗi RH-1, RH-4, RH-10
        self._git("checkout", "-q", "-b", "feature/uc-06")
        self._write("doc/features/UC-06/spec.md", "## A/C\n")  # RH-10: tự xóa AC-01
        self._write("src/test/java/FooTest.java", "@Disabled\n@Test\nvoid shouldWork() {}\n")  # RH-1
        self._write("src/main/java/FooService.java", "class FooService { int run() { throw new UnsupportedOperationException(); } }\n")  # RH-4

        code, out = self._run("audit", "--root", str(self.root), "--changed-against", "develop")
        self.assertEqual(code, 1, out)
        self.assertIn("[RH-1]", out)
        self.assertIn("[RH-4]", out)
        self.assertIn("[RH-10]", out)

    def test_set_and_clear_scope_reads_markdown_table_card(self):
        card = self._write("tasks/T-UC06.4.md", """# Task T-UC06.4
| Thuộc tính | Giá trị |
|---|---|
| **Mã task** | `T-UC06.4` |
| **Trạng thái** | `review` |
| **Phạm vi sửa đổi (scope_edit)** | `src/main/java/com/gdt/**`, `src/test/**` |
""")
        code, out = self._run("set-scope", "--root", str(self.root), "--mode", "implement", "--card", str(card))
        self.assertEqual(code, 0, out)
        scope_file = self.root / ".agentbase-scope.json"
        self.assertTrue(scope_file.is_file())
        data = json.loads(scope_file.read_text(encoding="utf-8"))
        self.assertEqual(data["card_id"], "T-UC06.4")
        self.assertEqual(data["mode"], "implement")
        self.assertEqual(data["scope_edit"], ["src/main/java/com/gdt/**", "src/test/**"])

        code2, _ = self._run("clear-scope", "--root", str(self.root))
        self.assertEqual(code2, 0)
        self.assertFalse(scope_file.exists())


if __name__ == "__main__":
    unittest.main()

