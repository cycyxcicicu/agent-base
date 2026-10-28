"""Kiểm thử tính tương thích khi nâng cấp và bảo toàn tùy chỉnh dự án.
Đáp ứng yêu cầu T-28.3 (Contract & Happy Path).
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestUpgradeCompatibility(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="upgrade-compat-test-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.target = self.tmp / "my_project"
        self.target.mkdir()

        # Khởi tạo git repository tại target
        subprocess.run(["git", "init", "-b", "main"], cwd=str(self.target), capture_output=True, check=True)
        # Thiết lập user git cục bộ trong fixture
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(self.target), capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=str(self.target), capture_output=True, check=True)

    def test_bootstrap_and_preserve_customization(self):
        import os
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

        # 1. Bootstrap lần đầu
        bootstrap_script = ROOT / "scripts" / "bootstrap-project.py"
        res = subprocess.run(
            [sys.executable, str(bootstrap_script), "--target", str(self.target), "--mode", "git"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        self.assertEqual(res.returncode, 0, f"Bootstrap thất bại: {res.stderr}")
        self.assertTrue((self.target / ".agent-base.json").exists())

        # 2. Tùy chỉnh file template PROJECT.md và knowledge-manifest.json
        project_md = self.target / "PROJECT.md"
        custom_content = "# DỰ ÁN TÙY BIẾN CỦA TÔI\nThông tin mật và riêng biệt."
        project_md.write_text(custom_content, encoding="utf-8")

        km_file = self.target / "agents" / "knowledge" / "knowledge-manifest.json"
        if km_file.exists():
            km_custom = json.dumps({"schema_version": 1, "custom_field": "CUSTOM_DATA"}, indent=2)
            km_file.write_text(km_custom, encoding="utf-8")

        # 3. Bootstrap lần hai (nâng cấp / rerun idempotent)
        res2 = subprocess.run(
            [sys.executable, str(bootstrap_script), "--target", str(self.target), "--mode", "git"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        self.assertEqual(res2.returncode, 0)
        self.assertIn("bỏ qua", res2.stdout)

        # 4. Xác nhận nội dung tùy chỉnh không bị ghi đè
        self.assertEqual(project_md.read_text(encoding="utf-8"), custom_content)
        if km_file.exists():
            self.assertIn("CUSTOM_DATA", km_file.read_text(encoding="utf-8"))

        # 5. Kiểm tra agent-base-diff.py: file template không bị liệt kê vào danh sách tracked/diff
        diff_script = self.target / "scripts" / "agent-base-diff.py"
        if not diff_script.exists():
            diff_script = ROOT / "scripts" / "agent-base-diff.py"

        import os
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        res_diff = subprocess.run(
            [sys.executable, str(diff_script), "--base", str(ROOT)],
            cwd=str(self.target),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        self.assertEqual(res_diff.returncode, 0, f"Diff thất bại: {res_diff.stderr}")
        self.assertNotIn("PROJECT.md", res_diff.stdout)
        self.assertNotIn("knowledge-manifest.json", res_diff.stdout)


if __name__ == "__main__":
    unittest.main()
