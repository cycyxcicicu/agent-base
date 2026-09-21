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

    def test_python_subprocess_shell_true(self):
        code = "import subprocess\ndef run_cmd(u):\n    subprocess.run(f'echo {u}', shell=True)\n"
        comments = self.reviewer.analyze_source("src/cmd.py", code)
        self.assertTrue(any(c.severity == "critical" and "shell=True" in c.content for c in comments))

    def test_python_sqli_formatting(self):
        code = "def query(uid):\n    cursor.execute(f'SELECT * FROM users WHERE id = {uid}')\n"
        comments = self.reviewer.analyze_source("src/db.py", code)
        self.assertTrue(any(c.severity == "critical" and "SQL" in c.content for c in comments))

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

    def test_python_undefined_variable(self):
        code = (
            "def calculate_total(prices):\n"
            "    return sum(prices) + tax_rate\n"
        )
        comments = self.reviewer.analyze_source("src/billing.py", code)
        self.assertTrue(any(c.category == "bug" and "tax_rate" in c.content for c in comments))
        # Verify severity is medium (non-blocking)
        bug_comment = next(c for c in comments if "tax_rate" in c.content)
        self.assertEqual(bug_comment.severity, "medium")
        self.assertFalse(bug_comment.blocking)

    def test_valid_patterns_no_undefined_variable_false_positives(self):
        """Kiểm chứng 20 mẫu mã nguồn Python hợp lệ không bị CodeReviewer báo lỗi sai."""
        cases = [
            # 1. Biến gán trong try/except
            ("try:\n    HAS_ORJSON = True\nexcept ImportError:\n    HAS_ORJSON = False\n\ndef check():\n    return HAS_ORJSON\n", "try_assign"),
            # 2. Import module trong try/except
            ("try:\n    import orjson\nexcept ImportError:\n    orjson = None\n\ndef parse(d):\n    return orjson.loads(d) if orjson else {}\n", "try_import"),
            # 3. Import from trong try/except
            ("try:\n    from openai import OpenAI\nexcept ImportError:\n    OpenAI = None\n\ndef client():\n    return OpenAI()\n", "try_from_import"),
            # 4. Tham số closure của hàm bao ngoài (func, max_attempts, base_delay)
            ("def retry(func, max_attempts=3, base_delay=1.0):\n    def wrapper(*args, **kwargs):\n        return func(max_attempts, base_delay)\n    return wrapper\n", "closure_params"),
            # 5. Hằng số class dùng làm giá trị mặc định cho method
            ("class SandboxRunner:\n    DEFAULT_TIMEOUT_SEC = 30\n    def run(self, timeout=DEFAULT_TIMEOUT_SEC):\n        return timeout\n", "class_constant_default"),
            # 6. async with context as s
            ("async def fetch(client):\n    async with client.get('/data') as resp:\n        return await resp.text()\n", "async_with"),
            # 6b. async for x in stream: print(x)
            ("async def stream_items(c):\n    async for x in c:\n        print(x)\n", "async_for"),
            # 7. with open(...) as f
            ("def read_file(path):\n    with open(path, 'r') as f:\n        return f.read()\n", "sync_with"),
            # 8. Multi-target assignment a = b = 10
            ("def setup():\n    a = b = 10\n    return a + b\n", "multi_assign"),
            # 9. Tuple / List unpacking (x, y) = val
            ("def coords(pt):\n    x, y = pt\n    return x + y\n", "tuple_unpack"),
            # 10. Walrus operator (:=)
            ("def check_len(data):\n    if (n := len(data)) > 0:\n        return n\n    return 0\n", "walrus_operator"),
            # 11. Vòng lặp for item in items
            ("def process(items):\n    res = []\n    for item in items:\n        res.append(item.strip())\n    return res\n", "for_loop"),
            # 12. List comprehension
            ("def double_all(data):\n    return [x * 2 for x in data]\n", "list_comprehension"),
            # 13. Dict / Set comprehension
            ("def dict_comp(pairs):\n    return {k: v for k, v in pairs}\n", "dict_comprehension"),
            # 14. Nested comprehension
            ("def flatten(matrix):\n    return [col for row in matrix for col in row]\n", "nested_comprehension"),
            # 15. Except handler variable
            ("def safe_int(s):\n    try:\n        return int(s)\n    except ValueError as err:\n        return str(err)\n", "except_handler_var"),
            # 16. Lambda parameter
            ("def sort_keys(data):\n    return sorted(data, key=lambda x: x.name)\n", "lambda_param"),
            # 17. Global variable declaration
            ("counter = 0\ndef increment():\n    global counter\n    counter += 1\n    return counter\n", "global_var"),
            # 18. Builtin functions và typing
            ("def builtins_use(seq):\n    return sum(range(len(seq))) + int(isinstance(seq, list))\n", "builtins"),
            # 19. Builtin exceptions
            ("def raise_errors(condition):\n    if condition:\n        raise KeyError('missing')\n    raise ValueError('invalid')\n", "builtin_exceptions"),
            # 20. Module-level conditional definition
            ("import sys\nif sys.platform == 'win32':\n    PLATFORM_NAME = 'windows'\nelse:\n    PLATFORM_NAME = 'posix'\n\ndef get_plat():\n    return PLATFORM_NAME\n", "module_conditional")
        ]

        for code, label in cases:
            comments = self.reviewer.analyze_source(f"src/{label}.py", code)
            undefined_comments = [c for c in comments if "chưa được định nghĩa" in c.content]
            self.assertEqual(
                len(undefined_comments), 0,
                f"Pattern '{label}' falsely flagged undefined variable: {[c.content for c in undefined_comments]}"
            )


if __name__ == "__main__":
    unittest.main()
