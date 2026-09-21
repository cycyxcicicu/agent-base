"""
Unit Tests for Alibaba Open-Code-Review (OCR) Engine.
Kiểm thử toàn diện: Lọc tệp, phân giải luật, phân tích AST, Line-Level Comments, và Gate Classification.
"""

import unittest
from agent_core.eval.code_reviewer import (
    CodeReviewer,
    ReviewComment,
    ReviewRuleResolver,
    FileExclusionFilter,
)


class TestFileExclusionFilter(unittest.TestCase):
    def test_secret_exclusions(self):
        cases = [
            (".env", "secret_exclude"),
            (".env.local", "secret_exclude"),
            (".ssh/id_rsa", "secret_exclude"),
            ("config/private.key", "secret_exclude"),
            ("cert.pem", "secret_exclude"),
        ]
        for path, expected_reason in cases:
            excluded, reason = FileExclusionFilter.check_exclusion(path)
            self.assertTrue(excluded, f"Should exclude secret: {path}")
            self.assertEqual(reason, expected_reason)

    def test_provider_directory_exclusions(self):
        cases = [
            ("node_modules/axios/index.js", "provider_directory"),
            ("vendor/github.com/pkg/errors.go", "provider_directory"),
            ("dist/main.bundle.js", "provider_directory"),
            ("src/__pycache__/app.cpython-311.pyc", "provider_directory"),
        ]
        for path, expected_reason in cases:
            excluded, reason = FileExclusionFilter.check_exclusion(path)
            self.assertTrue(excluded, f"Should exclude provider directory: {path}")
            self.assertEqual(reason, expected_reason)

    def test_default_path_exclusions(self):
        cases = [
            ("tests/test_calculator.py", "default_path"),
            ("pkg/service_test.go", "default_path"),
            ("src/components/Button.test.tsx", "default_path"),
            ("package-lock.json", "default_path"),
            ("pnpm-lock.yaml", "default_path"),
            ("static/bundle.min.js", "default_path"),
        ]
        for path, expected_reason in cases:
            excluded, reason = FileExclusionFilter.check_exclusion(path)
            self.assertTrue(excluded, f"Should exclude default path: {path}")
            self.assertEqual(reason, expected_reason)

    def test_reviewable_clean_files(self):
        cases = [
            "src/models/user.py",
            "internal/service/order.go",
            "frontend/src/components/Header.tsx",
            "services/AuthService.java",
        ]
        for path in cases:
            excluded, reason = FileExclusionFilter.check_exclusion(path)
            self.assertFalse(excluded, f"Should NOT exclude clean source file: {path}")
            self.assertEqual(reason, "")


class TestReviewRuleResolver(unittest.TestCase):
    def setUp(self):
        self.resolver = ReviewRuleResolver()

    def test_language_mappings(self):
        self.assertEqual(self.resolver.resolve_rule_name("src/main.py"), "python.md")
        self.assertEqual(self.resolver.resolve_rule_name("web/app.tsx"), "ts_js_tsx_jsx.md")
        self.assertEqual(self.resolver.resolve_rule_name("cmd/server.go"), "go.md")
        self.assertEqual(self.resolver.resolve_rule_name("com/app/Service.java"), "java.md")
        self.assertEqual(self.resolver.resolve_rule_name(".github/workflows/deploy.yml"), "github_workflows.md")
        self.assertEqual(self.resolver.resolve_rule_name("README.txt"), "default.md")


class TestCodeReviewerAnalysis(unittest.TestCase):
    def setUp(self):
        self.reviewer = CodeReviewer()

    def test_python_mutable_default_argument(self):
        code = (
            "def append_item(item, bucket=[]):\n"
            "    bucket.append(item)\n"
            "    return bucket\n"
        )
        comments = self.reviewer.analyze_source("src/utils.py", code)
        self.assertEqual(len(comments), 1)
        c = comments[0]
        self.assertEqual(c.category, "bug")
        self.assertEqual(c.severity, "high")
        self.assertTrue(c.blocking)
        self.assertEqual(c.start_line, 1)
        self.assertIn("mutable default argument", c.content)

    def test_python_bare_except(self):
        code = (
            "try:\n"
            "    val = int('abc')\n"
            "except:\n"
            "    val = 0\n"
        )
        comments = self.reviewer.analyze_source("src/converter.py", code)
        self.assertEqual(len(comments), 1)
        c = comments[0]
        self.assertEqual(c.category, "bug")
        self.assertEqual(c.severity, "medium")
        self.assertFalse(c.blocking)
        self.assertEqual(c.start_line, 3)
        self.assertIn("bare 'except:'", c.content)

    def test_python_float_equality(self):
        code = (
            "def is_pi(val):\n"
            "    if val == 3.14159:\n"
            "        return True\n"
            "    return False\n"
        )
        comments = self.reviewer.analyze_source("src/math_util.py", code)
        self.assertEqual(len(comments), 1)
        c = comments[0]
        self.assertEqual(c.category, "bug")
        self.assertEqual(c.severity, "medium")
        self.assertEqual(c.start_line, 2)
        self.assertIn("float equality", c.content)

    def test_python_dangerous_eval(self):
        code = (
            "def run_user_code(user_str):\n"
            "    return eval(user_str)\n"
        )
        comments = self.reviewer.analyze_source("src/runner.py", code)
        self.assertEqual(len(comments), 1)
        c = comments[0]
        self.assertEqual(c.category, "security")
        self.assertEqual(c.severity, "critical")
        self.assertTrue(c.blocking)
        self.assertIn("Remote Code Execution", c.content)

    def test_js_dangerous_eval_and_inner_html(self):
        code = (
            "function render(data) {\n"
            "    const val = eval(data.formula);\n"
            "    return <div dangerouslySetInnerHTML={{__html: val}} />;\n"
            "}\n"
        )
        comments = self.reviewer.analyze_source("web/Component.tsx", code)
        self.assertEqual(len(comments), 2)
        severities = {c.severity for c in comments}
        self.assertIn("critical", severities)
        self.assertIn("high", severities)

    def test_clean_code_produces_no_comments(self):
        clean_code = (
            "def safe_add(a: int, b: int) -> int:\n"
            "    \"\"\"Sum two integers safely.\"\"\"\n"
            "    return a + b\n"
        )
        comments = self.reviewer.analyze_source("src/math.py", clean_code)
        self.assertEqual(len(comments), 0)

    def test_report_generation_blocked_gate(self):
        bad_code = "def bad(x=[]): eval(x)\n"
        comments = self.reviewer.analyze_source("src/leak.py", bad_code)
        report = self.reviewer.generate_report(comments, total_files=1)
        self.assertIn("⛔ BLOCKED", report)
        self.assertIn("Alibaba Open-Code-Review Report", report)
        self.assertIn("Favor precision over recall", report)

    def test_report_generation_passed_gate(self):
        report = self.reviewer.generate_report([], total_files=5)
        self.assertIn("✅ PASS", report)
        self.assertIn("no issues found", report)


if __name__ == "__main__":
    unittest.main()
