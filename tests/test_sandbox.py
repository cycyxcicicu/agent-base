"""
tests/test_sandbox.py
Unit tests for isolated execution SandboxRunner.
"""

import os
import unittest
from agent_core.core.sandbox import SandboxRunner

class TestSandboxRunner(unittest.TestCase):
    def setUp(self):
        self.runner = SandboxRunner()

    def test_run_python_code_success(self):
        code = "print('sandbox_ok')"
        result = self.runner.run_python_code(code)
        self.assertTrue(result.is_success)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("sandbox_ok", result.stdout)
        self.assertFalse(result.timed_out)

    def test_run_python_code_error(self):
        code = "raise ValueError('sandbox_err')"
        result = self.runner.run_python_code(code)
        self.assertFalse(result.is_success)
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("ValueError: sandbox_err", result.stderr)

    def test_timeout_enforcement(self):
        code = "import time; time.sleep(2)"
        result = self.runner.run_python_code(code, timeout=0.2)
        self.assertTrue(result.timed_out)
        self.assertFalse(result.is_success)
        self.assertIn("timed out", result.stderr)

    def test_env_sanitization(self):
        dirty_env = {
            "PATH": "/usr/bin",
            "APP_ENV": "test",
            "AWS_SECRET_ACCESS_KEY": "supersecret",
            "USER_SECRET_TOKEN": "token123",
            "GITHUB_TOKEN": "ghp_1234567890abcdef",
            "OPENAI_API_KEY": "sk-1234567890abcdef",
            "ANTHROPIC_API_KEY": "sk-ant-1234567890",
            "DB_PASSWORD": "rootpassword123",
            "GEMINI_SECURE_1PSID": "cookie_secret"
        }
        clean_env = self.runner.sanitize_env(dirty_env)
        self.assertIn("PATH", clean_env)
        self.assertIn("APP_ENV", clean_env)
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", clean_env)
        self.assertNotIn("USER_SECRET_TOKEN", clean_env)
        self.assertNotIn("GITHUB_TOKEN", clean_env)
        self.assertNotIn("OPENAI_API_KEY", clean_env)
        self.assertNotIn("ANTHROPIC_API_KEY", clean_env)
        self.assertNotIn("DB_PASSWORD", clean_env)
        self.assertNotIn("GEMINI_SECURE_1PSID", clean_env)

    def test_allow_list_env(self):
        dirty_env = {
            "PATH": "/usr/bin",
            "CUSTOM_VAR": "keep_me",
            "GITHUB_TOKEN": "ghp_1234567890abcdef",
            "OTHER_VAR": "drop_me"
        }
        allowed = self.runner.sanitize_env(dirty_env, allow_list=["PATH", "CUSTOM_VAR"])
        self.assertEqual(set(allowed.keys()), {"PATH", "CUSTOM_VAR"})

if __name__ == "__main__":
    unittest.main()
