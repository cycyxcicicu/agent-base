"""
tests/test_git_hooks.py
Kiểm thử hook `.githooks/pre-commit` và `commit-msg` trên repo git tạm bằng commit thật.

Giữ các điểm đã từng lọt: tên file bí mật (`.envrc`, `id_ed25519`, `*.pfx`, `credentials.json`, `terraform.tfstate`,
cookie Google `gemini_cookies.json` và `cookies/*.json` khi `git add -f`) và các định dạng token (Slack, Google `AIza`,
Anthropic `sk-ant-`, JWT, `__Secure-1PSID`). Đồng thời không chặn nhầm file mẫu (`*.example.*`), khóa công khai (`.pub`)
và các dòng mã bình thường.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECRET_FILES = [
    ".env", ".env.local", ".envrc", "secrets.json", "credentials.json", "config/credentials.json",
    "service-account.json", "id_rsa", "id_ed25519", "keys/id_ecdsa", "server.pem", "server.key",
    "cert.pfx", "cert.p12", "store.jks", "vault.kdbx", ".netrc", ".pypirc", "terraform.tfstate",
    "prod.tfvars", "gemini_cookies.json", "cookies/all_accounts.json", "search_grant.json",
]

ALLOWED_FILES = [
    ".env.example", "cookies/all_accounts.example.json", "gemini_cookies.example.json", "id_rsa.pub",
    "docs/secret_scanner.yml", "src/credentials_helper.py", "README.md", "src/app.py",
]

SECRET_LINES = {
    "aws access key": "AKIA" + "ABCDEFGHIJKLMNOP",
    "github token": "ghp_" + "abcdefghijklmnopqrstuvwxyz0123456789",
    "github fine-grained": "github_pat_" + "11ABCDEFG0abcdefghijkl_mnopqrstuvwxyz0123456789",
    "gitlab token": "glpat-" + "abcdefghijklmnopqrst",
    "slack token": "xoxb-" + "1234567890-abcdefghij",
    "google api key": "AIzaSy" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456",
    "anthropic key": "sk-ant-" + "api03-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN",
    "openai style key": "sk-" + "abcdefghijklmnopqrstuvwxyz0123456789",
    "jwt": "eyJhbGciOi" + "JIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghijklmnopqrstuvwxyz",
    "google cookie": "__Secure-1" + 'PSID="g.a000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"',
    "private key": "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
    "password assignment": "DB_PASSWORD" + "=Sup3rS3cretValue99",
    "slack webhook": "https://hooks.slack.com/" + "services/T01234567/B01234567/abcdefghijklmnopqrstuvwx",
}

ALLOWED_LINES = [
    'password = request.form["password"]',
    'token = os.environ["GITHUB_TOKEN"]',
    "secret_key = config.SECRET_KEY_NAME",
    "task-management-system-with-a-very-long-descriptive-name",
    "disk-usage-monitoring-and-alerting-tool-configuration",
    "Tiền tố khóa Google bắt đầu bằng AIza, khóa Slack bắt đầu bằng xoxb.",
]


class GitRepoTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = Path(tempfile.mkdtemp(prefix="hooks-e2e-"))
        cls.git("init", "-q", "-b", "main")
        cls.git("config", "user.email", "t@example.com")
        cls.git("config", "user.name", "Human")
        cls.git("config", "core.autocrlf", "false")
        shutil.copytree(Path(os.environ.get("GIT_HOOKS_DIR", str(ROOT / ".githooks"))), cls.repo / ".githooks")
        cls.write("base.txt", "base\n")
        cls.git("add", "base.txt")
        cls.git("commit", "-q", "--no-verify", "-m", "init")
        cls.git("checkout", "-q", "-b", "develop")
        cls.git("checkout", "-q", "-b", "feature/1-hooks")
        cls.git("config", "core.hooksPath", ".githooks")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(str(cls.repo), True)

    @classmethod
    def git(cls, *args, check=True):
        res = subprocess.run(["git", *args], cwd=cls.repo, capture_output=True, text=True, encoding="utf-8")
        if check and res.returncode != 0:
            raise AssertionError(f"git {' '.join(args)} failed: {res.stderr}")
        return res

    @classmethod
    def write(cls, rel, text):
        p = cls.repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(text)

    def try_commit(self, rel, content="content\n", message="docs(x): change", branch=None, extra=()):
        """Đưa một file vào vùng chờ (kể cả file bị .gitignore bằng -f) rồi thử commit; trả về (mã thoát, thông báo)."""
        if branch:
            self.git("checkout", "-q", branch)
        self.write(rel, content)
        self.git("add", "-f", rel)
        res = self.git(*extra, "commit", "-q", "-m", message, check=False)
        if res.returncode == 0:
            self.git("reset", "-q", "--soft", "HEAD~1")
        self.git("reset", "-q")
        (self.repo / rel).unlink()
        if branch:
            self.git("checkout", "-q", "feature/1-hooks")
        return res.returncode, res.stderr + res.stdout


class TestSecretFiles(GitRepoTestCase):
    def test_secret_like_file_names_are_refused(self):
        for name in SECRET_FILES:
            code, out = self.try_commit(name, "value\n")
            self.assertNotEqual(code, 0, f"hook cho qua file bí mật: {name}")
            self.assertIn("secret", out.lower(), name)

    def test_examples_templates_and_public_keys_are_allowed(self):
        for name in ALLOWED_FILES:
            code, out = self.try_commit(name, "harmless\n")
            self.assertEqual(code, 0, f"hook chặn nhầm file hợp lệ {name}: {out}")


class TestSecretContent(GitRepoTestCase):
    def test_token_formats_are_refused(self):
        for label, line in SECRET_LINES.items():
            code, out = self.try_commit("notes.txt", line + "\n")
            self.assertNotEqual(code, 0, f"hook cho qua {label}")

    def test_ordinary_lines_are_allowed(self):
        for line in ALLOWED_LINES:
            code, out = self.try_commit("notes.txt", line + "\n")
            self.assertEqual(code, 0, f"hook chặn nhầm dòng: {line!r}: {out}")


class TestBranchMessageAndIdentity(GitRepoTestCase):
    def test_direct_commit_on_protected_branches_is_refused(self):
        for branch in ("main", "develop"):
            code, out = self.try_commit("a.txt", branch=branch)
            self.assertNotEqual(code, 0, branch)
            self.assertIn("direct commits", out)

    def test_bad_branch_name_is_refused(self):
        self.git("checkout", "-q", "-b", "badbranch")
        try:
            code, out = self.try_commit("a.txt")
            self.assertNotEqual(code, 0)
        finally:
            self.git("checkout", "-q", "feature/1-hooks")
            self.git("branch", "-q", "-D", "badbranch")

    def test_bad_messages_are_refused(self):
        self.assertNotEqual(self.try_commit("a.txt", message="them file")[0], 0)
        self.assertNotEqual(self.try_commit("a.txt", message="feat(x): " + "a" * 80)[0], 0)

    def test_valid_commit_passes(self):
        self.assertEqual(self.try_commit("a.txt", message="feat(x): add a")[0], 0)

    def test_revert_needs_an_approved_risk_ticket(self):
        code, out = self.try_commit("a.txt", message="fix(x): revert something")
        self.assertNotEqual(code, 0)
        self.assertIn("Risk-Approved", out)

    def test_agent_identity_is_refused_but_user_identity_passes(self):
        self.git("config", "user.name", "Bot (agent)")
        try:
            code, out = self.try_commit("a.txt", message="feat(x): add a")
            self.assertNotEqual(code, 0)
            self.assertIn("(agent)", out)
        finally:
            self.git("config", "user.name", "Human")
        self.assertEqual(self.try_commit("a.txt", message="feat(x): add a\n\nCo-Authored-By: Claude <noreply@anthropic.com>")[0], 0)


if __name__ == "__main__":
    unittest.main()
