"""Kiểm thử scripts/hard-check.py (luật cứng khai báo bằng JSON). Viết bằng unittest để CI chạy được."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "hard-check.py"

RULES = {"rules": [
    {"id": "no-use-effect", "type": "forbid_regex", "include": ["src/**/*.tsx"], "exclude": ["**/*.test.tsx"],
     "pattern": "\\buseEffect\\(", "message": "Không dùng useEffect"},
    {"id": "max-5-lines", "type": "max_file_lines", "include": ["src/**/*.ts"], "max": 5, "message": "File quá dài"},
    {"id": "soft-todo", "type": "forbid_regex", "include": ["src/**"], "pattern": "TODO", "severity": "warn"},
]}


class HardCheckCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="hardcheck-")
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def rules(self, data=RULES):
        self.write("docs/HARD-RULES.json", json.dumps(data, ensure_ascii=False))

    def run_check(self, *extra):
        r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *extra],
                           capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr


class TestRules(HardCheckCase):
    def test_no_rules_file_passes(self):
        code, out = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("Chưa có", out)

    def test_forbid_regex_reports_file_and_line(self):
        self.rules()
        self.write("src/a.tsx", "const x = 1;\nuseEffect(() => {}, []);\n")
        code, out = self.run_check()
        self.assertEqual(code, 1, out)
        self.assertIn("src/a.tsx:2: [no-use-effect]", out)

    def test_exclude_glob_is_respected(self):
        self.rules()
        self.write("src/a.test.tsx", "useEffect(() => {}, []);\n")
        code, out = self.run_check()
        self.assertEqual(code, 0, out)

    def test_ignore_needs_reason(self):
        self.rules()
        self.write("src/ok.tsx", "// hard-ignore: no-use-effect đồng bộ với API bên ngoài\nuseEffect(() => {}, []);\n")
        self.write("src/bad.tsx", "useEffect(() => {}, []); // hard-ignore: no-use-effect\n")
        code, out = self.run_check()
        self.assertEqual(code, 1, out)
        self.assertIn("src/bad.tsx", out)
        self.assertNotIn("src/ok.tsx", out)
        self.assertIn("1 lần bỏ qua có lý do", out)

    def test_max_file_lines(self):
        self.rules()
        self.write("src/long.ts", "\n".join(f"x{i}" for i in range(9)) + "\n")
        code, out = self.run_check()
        self.assertEqual(code, 1, out)
        self.assertIn("[max-5-lines]", out)
        self.assertIn("9 dòng", out)

    def test_path_must_match_enforces_structure(self):
        self.rules({"rules": [{"id": "features-in-place", "type": "path_must_match", "include": ["src/**/*.tsx"],
                               "exclude": ["src/shared/**"], "allow": ["src/features/*/**"],
                               "message": "Mã tính năng phải nằm trong src/features/<tên>/"}]})
        self.write("src/features/billing/Invoice.tsx", "export const A = 1;\n")
        self.write("src/shared/Button.tsx", "export const B = 1;\n")
        self.write("src/Loose.tsx", "export const C = 1;\n")
        code, out = self.run_check()
        self.assertEqual(code, 1, out)
        self.assertIn("src/Loose.tsx:1: [features-in-place]", out)
        self.assertNotIn("Invoice.tsx", out)
        self.assertNotIn("Button.tsx", out)

    def test_path_rule_needs_allow(self):
        self.rules({"rules": [{"id": "x", "type": "path_must_match", "include": ["**"]}]})
        code, out = self.run_check()
        self.assertEqual(code, 2, out)

    def test_warn_severity_does_not_fail(self):
        self.rules()
        self.write("src/note.js", "// TODO sau\n")
        code, out = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("cảnh báo", out)

    def test_bad_config_exits_2(self):
        for bad in ({"rules": [{"id": "A B", "type": "forbid_regex", "include": ["**"], "pattern": "x"}]},
                    {"rules": [{"id": "dup", "type": "forbid_regex", "include": ["**"], "pattern": "x"},
                               {"id": "dup", "type": "forbid_regex", "include": ["**"], "pattern": "y"}]},
                    {"rules": [{"id": "x", "type": "nope", "include": ["**"]}]},
                    {"rules": [{"id": "x", "type": "forbid_regex", "include": ["**"], "pattern": "("}]},
                    {"rules": [{"id": "x", "type": "max_file_lines", "include": ["**"], "max": 0}]}):
            self.rules(bad)
            code, out = self.run_check()
            self.assertEqual(code, 2, f"{bad} -> {out}")


class TestShippedExample(unittest.TestCase):
    def test_example_rules_load_and_history_comment_rule_is_narrow(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("hard_check_under_test", SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        rules = {r["id"]: r for r in mod.load_rules(ROOT / "examples" / "hard-rules" / "hard-rules.example.json")}
        self.assertIn("features-in-place", rules)
        regex = rules["no-conversation-comments"]["regex"]
        self.assertTrue(regex.search("// as the user said, never touch this"))
        self.assertTrue(regex.search("# theo yêu cầu của người dùng"))
        self.assertFalse(regex.search("// retry because the upstream API is flaky"))
        self.assertFalse(regex.search("# người dùng nhập sai email thì trả lỗi 400"))


class TestChangedAgainst(HardCheckCase):
    def git(self, *args):
        r = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_only_changed_files_are_scanned(self):
        self.git("init", "-q", "-b", "develop")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "T")
        self.rules()
        self.write("src/legacy.tsx", "useEffect(() => {}, []);\n")  # vi phạm cũ, có sẵn ở nhánh gốc
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        self.git("checkout", "-q", "-b", "feature/1-x")
        self.write("src/new.tsx", "const ok = 1;\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "change")
        code, out = self.run_check("--changed-against", "develop")
        self.assertEqual(code, 0, out)  # chỉ new.tsx được quét, vi phạm cũ không làm đỏ PR
        self.write("src/bad.tsx", "useEffect(() => {}, []);\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "bad")
        code, out = self.run_check("--changed-against", "develop")
        self.assertEqual(code, 1, out)
        self.assertIn("src/bad.tsx", out)
        self.assertNotIn("legacy", out)

    def test_changed_against_unknown_ref_is_config_error(self):
        self.rules()
        code, out = self.run_check("--changed-against", "no-such-ref")
        self.assertEqual(code, 2, out)

    def test_diff_lines_ignores_untouched_legacy_lines_in_modified_file(self):
        self.git("init", "-q", "-b", "develop")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "T")
        self.rules()
        self.write("src/mixed.tsx", "useEffect(() => {}, []);\nexport const clean = 1;\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")

        # Sửa dòng khác trong chính src/mixed.tsx (không sửa dòng useEffect cũ) -> --diff-lines phải PASS
        self.git("checkout", "-q", "-b", "feature/fix")
        self.write("src/mixed.tsx", "useEffect(() => {}, []);\nexport const clean = 2;\n")
        code, out = self.run_check("--changed-against", "develop", "--diff-lines")
        self.assertEqual(code, 0, out)

        # Thêm dòng useEffect mới chưa commit -> --diff-lines phải FAIL ngay dòng mới
        self.write("src/mixed.tsx", "useEffect(() => {}, []);\nexport const clean = 2;\nuseEffect(() => {}, [clean]);\n")
        code2, out2 = self.run_check("--changed-against", "develop", "--diff-lines")
        self.assertEqual(code2, 1, out2)
        self.assertIn("src/mixed.tsx:3", out2)


if __name__ == "__main__":
    unittest.main()
