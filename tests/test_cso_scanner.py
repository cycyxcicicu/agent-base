"""
tests/test_cso_scanner.py
Unit tests for CSO Static Security Audit Engine.
"""

import unittest
from pathlib import Path
from agent_core.eval.cso_scanner import CsoScanner

class TestCsoScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = CsoScanner()

    def test_detect_hardcoded_api_key(self):
        code = "API_KEY = 'sk-proj-1234567890abcdef1234567890'"
        findings = self.scanner.scan_file_content(code, "test_file.py")
        self.assertTrue(any(f.rule_id == "SECRET-01" for f in findings))
        self.assertEqual(findings[0].severity, "CRITICAL")

        # JSON / YAML format
        json_code = '{"api_key": "sk-proj-1234567890abcdef1234567890", "password": "supersecretpassword"}'
        findings_json = self.scanner.scan_file_content(json_code, "config.json")
        self.assertTrue(any(f.rule_id == "SECRET-01" for f in findings_json))
        self.assertTrue(any(f.rule_id == "SECRET-03" for f in findings_json))

    def test_detect_command_injection(self):
        code = "os.system(f'rm -rf {user_input}')"
        findings = self.scanner.scan_file_content(code, "test_file.py")
        self.assertTrue(any(f.rule_id == "INJ-01" for f in findings))
        self.assertEqual(findings[0].severity, "CRITICAL")

    def test_detect_sqli(self):
        code = "cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')"
        findings = self.scanner.scan_file_content(code, "test_file.py")
        self.assertTrue(any(f.rule_id == "SQLI-01" for f in findings))
        self.assertEqual(findings[0].severity, "CRITICAL")

    def test_detect_path_traversal(self):
        code = "with open(f'/tmp/{user_filename}', 'r') as f:"
        findings = self.scanner.scan_file_content(code, "test_file.py")
        self.assertTrue(any(f.rule_id == "TRAVERSAL-01" for f in findings))
        self.assertEqual(findings[0].severity, "HIGH")

    def test_clean_code_passes_gate(self):
        clean_code = """
import os
import subprocess

def run_task(file_path):
    safe_env = os.environ.get('API_KEY')
    result = subprocess.run(['python', '--version'], capture_output=True, check=True)
    return result.returncode
"""
        findings = self.scanner.scan_file_content(clean_code, "clean.py")
        gate = self.scanner.evaluate_gate(findings)
        self.assertTrue(gate["passed"])
        self.assertEqual(gate["verdict"], "PASSED")
        self.assertEqual(len(findings), 0)

    def test_detect_multiline_shell_true(self):
        code = """
import subprocess
def run_cmd(user_arg):
    subprocess.run(
        ["echo", user_arg],
        capture_output=True,
        shell=True
    )
"""
        findings = self.scanner.scan_file_content(code, "test_proc.py")
        self.assertTrue(any(f.rule_id == "INJ-02" for f in findings))
        inj = next(f for f in findings if f.rule_id == "INJ-02")
        self.assertEqual(inj.severity, "CRITICAL")

    def test_detect_eval_and_popen(self):
        code = """
import os
val = eval("1 + 2")
pipe = os.popen("ls -la")
"""
        findings = self.scanner.scan_file_content(code, "danger.py")
        rules = {f.rule_id for f in findings}
        self.assertIn("INJ-03", rules)
        self.assertIn("INJ-05", rules)

    def test_detect_verify_false_and_md5(self):
        code = """
import requests
import hashlib
res = requests.get('https://example.com', verify=False)
h = hashlib.md5(b'test').hexdigest()
"""
        findings = self.scanner.scan_file_content(code, "net_crypto.py")
        rules = {f.rule_id for f in findings}
        self.assertIn("INSEC-01", rules)
        self.assertIn("CRYPTO-01", rules)

    def test_github_and_githooks_not_skipped(self):
        gh_workflow = Path("/repo/.github/workflows/check.yml")
        githook = Path("/repo/.githooks/pre-commit")
        git_internal = Path("/repo/.git/config")

        self.assertFalse(self.scanner.should_skip(gh_workflow))
        self.assertFalse(self.scanner.should_skip(githook))
        self.assertTrue(self.scanner.should_skip(git_internal))

if __name__ == "__main__":
    unittest.main()
