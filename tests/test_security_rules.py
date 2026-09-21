"""
tests/test_security_rules.py
Kiểm thử tự động các quy tắc cho phép/bị chặn (allow/deny) trong .claude/settings.json và Kilo agents.
Bảo đảm không chặn nhầm 6/18 lệnh Git chỉ đọc hợp lệ, các lệnh băm shasum/sha256sum, và lệnh framework.
"""

import json
import fnmatch
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestSecurityDenyRules(unittest.TestCase):
    """Kiểm tra độ chính xác của các quy tắc chặn trong .claude/settings.json và Kilo."""

    @classmethod
    def setUpClass(cls):
        # Đọc quy tắc deny từ .claude/settings.json
        settings_path = ROOT / ".claude" / "settings.json"
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls.claude_denies = data.get("permissions", {}).get("deny", [])

        # Trích xuất các pattern Bash(...) và PowerShell(...)
        cls.bash_patterns = []
        cls.ps_patterns = []
        for rule in cls.claude_denies:
            m_bash = re.match(r"^Bash\((.+)\)$", rule)
            if m_bash:
                cls.bash_patterns.append(m_bash.group(1))
            m_ps = re.match(r"^PowerShell\((.+)\)$", rule)
            if m_ps:
                cls.ps_patterns.append(m_ps.group(1))

        # Đọc quy tắc của vai dev trong Kilo
        kilo_dev_path = ROOT / ".kilo" / "agents" / "dev.md"
        cls.kilo_dev_denies = []
        if kilo_dev_path.exists():
            content = kilo_dev_path.read_text(encoding="utf-8")
            for line in content.splitlines():
                m = re.match(r'^\s+"([^"]+)":\s*deny\b', line)
                if m:
                    cls.kilo_dev_denies.append(m.group(1))

    def _is_blocked(self, command: str, patterns: list, case_sensitive: bool = False) -> bool:
        cmd = command if case_sensitive else command.lower()
        for pat in patterns:
            p = pat if case_sensitive else pat.lower()
            if fnmatch.fnmatch(cmd, p):
                return True
        return False

    def test_git_readonly_allowed_in_bash(self):
        """Các lệnh Git chỉ đọc được AGENTS.md cho phép KHÔNG bị chặn trong Bash."""
        allowed_cmds = [
            "git diff --name-only",
            "git log --name-only",
            "git blame agent_core/eval/code_reviewer.py",
            "git log --author=Alice",
            "git branch --list",
            "git status",
            "git status -s",
            "git diff HEAD~1",
            "git log -n 5",
            "git grep -n commit",
            'git log --grep="revert"',
            'git log --oneline -i --grep="hoan tac"',
            "git.exe status"
        ]
        for cmd in allowed_cmds:
            blocked = self._is_blocked(cmd, self.bash_patterns)
            self.assertFalse(blocked, f"Lệnh Git chỉ đọc hợp lệ bị chặn trong Bash: {cmd}")

    def test_git_write_blocked_in_bash_and_powershell(self):
        """Các lệnh Git làm biến đổi trạng thái BẮT BUỘC bị chặn cả ở Bash và PowerShell."""
        dangerous_cmds = [
            "git commit -m 'feat: something'",
            "git.exe commit -m 'feat: something'",
            "git push origin main",
            "git push --force origin main",
            "git reset --hard HEAD~1",
            "git revert HEAD",
            "git.exe revert HEAD",
            "git am patch.mbox",
            "git.exe am patch.mbox",
            "git rebase main",
            "git merge main",
            "git checkout -b new-branch",
            "git branch -d feat",
            "git tag -a v1.0.0 -m 'release'"
        ]
        for cmd in dangerous_cmds:
            blocked_bash = self._is_blocked(cmd, self.bash_patterns)
            self.assertTrue(blocked_bash, f"Lệnh Git nguy hiểm bị lọt trong Bash: {cmd}")

            blocked_ps = self._is_blocked(cmd, self.ps_patterns)
            self.assertTrue(blocked_ps, f"Lệnh Git nguy hiểm bị lọt trong PowerShell: {cmd}")

    def test_hash_commands_with_dash_c_not_blocked(self):
        """Các lệnh kiểm tra checksum shasum -c, sha256sum -c KHÔNG bị chặn nhầm."""
        safe_hash_cmds = [
            "shasum -c checksums.txt",
            "sha256sum -c sha256sums.txt",
            "shasum -a 256 -c hash.txt"
        ]
        for cmd in safe_hash_cmds:
            blocked = self._is_blocked(cmd, self.bash_patterns)
            self.assertFalse(blocked, f"Lệnh hash hợp lệ bị chặn nhầm bởi sh* -c: {cmd}")

    def test_node_build_flags_not_blocked(self):
        """Lệnh node build.js -e production KHÔNG bị chặn nhầm bởi node -e."""
        safe_node_cmds = [
            "node build.js -e production",
            "node scripts/bundle.js -e env.json"
        ]
        for cmd in safe_node_cmds:
            blocked = self._is_blocked(cmd, self.bash_patterns)
            self.assertFalse(blocked, f"Lệnh build hợp lệ bị chặn nhầm: {cmd}")

    def test_powershell_framework_commands_not_blocked_on_windows(self):
        """Lệnh framework với cờ -Check, -Card KHÔNG bị khớp powershell* -c* trên Windows."""
        framework_cmds = [
            "powershell -File scripts/sync-adapters.ps1 -Check",
            "powershell -ExecutionPolicy Bypass -File scripts/merge-gate.ps1 -Branch feat -Card tasks/T-01.md",
            "pwsh -File scripts/doctor.ps1 -Check"
        ]
        for cmd in framework_cmds:
            # Kiểm thử ở chế độ không phân biệt hoa thường (case-insensitive) như môi trường Windows
            blocked_ps = self._is_blocked(cmd, self.ps_patterns, case_sensitive=False)
            self.assertFalse(blocked_ps, f"Lệnh framework bị chặn nhầm trên Windows: {cmd}")

    def test_execution_escape_commands_blocked(self):
        """Các lệnh thoát vỏ bọc thực thi chuỗi inline (-c, -Command, -e) BẮT BUỘC bị chặn."""
        escape_cmds = [
            'sh -c "cat /etc/passwd"',
            'bash -c "rm -rf /"',
            'node -e "process.exit(1)"',
            'node --eval "console.log(process.env)"',
            'python -c "import os; os.system(\'id\')"',
            'py -c "print(1)"',
            'powershell -c "Get-Process"',
            'powershell -Command "Stop-Service foo"',
            'powershell.exe -command "Remove-Item foo"',
            'pwsh -c "ls"',
            'pwsh -Command "whoami"'
        ]
        for cmd in escape_cmds:
            # Kiểm tra trong Bash hoặc PowerShell tương ứng
            if cmd.startswith(("sh ", "bash ", "node ", "python ", "py ")):
                self.assertTrue(self._is_blocked(cmd, self.bash_patterns), f"Escape lọt trong Bash: {cmd}")
            if cmd.startswith(("powershell", "pwsh", "python ", "py ")):
                self.assertTrue(self._is_blocked(cmd, self.ps_patterns), f"Escape lọt trong PowerShell: {cmd}")

    def test_kilo_agent_roles_sync(self):
        """Kilo agent dev có quy tắc chặn chính xác tương đương."""
        self.assertTrue(len(self.kilo_dev_denies) > 0)
        self.assertTrue(any("git am" in p for p in self.kilo_dev_denies))
        self.assertFalse(any("*git*am*" in p for p in self.kilo_dev_denies))
        self.assertFalse(self._is_blocked("git diff --name-only", self.kilo_dev_denies))
        self.assertTrue(self._is_blocked("git am patch.mbox", self.kilo_dev_denies))


if __name__ == "__main__":
    unittest.main()
