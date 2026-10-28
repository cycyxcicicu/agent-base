import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Load setup-project.py bằng importlib vì có dấu gạch nối
script_path = Path(__file__).resolve().parent.parent / "scripts" / "setup-project.py"
spec = importlib.util.spec_from_file_location("setup_project_mod", script_path)
setup_project_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup_project_mod)
setup_project = setup_project_mod.setup_project


class TestSetupProject(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_setup_project_creates_structure(self):
        code = setup_project(self.tmp_dir)
        self.assertEqual(code, 0)

        # 1. Kiểm tra cấu trúc thư mục chuẩn
        self.assertTrue((self.tmp_dir / "docs" / "notes" / "inbox").is_dir())
        self.assertTrue((self.tmp_dir / "docs" / "notes" / "archive").is_dir())
        self.assertTrue((self.tmp_dir / "tasks").is_dir())
        self.assertTrue((self.tmp_dir / "doc").is_dir())

        # 2. Kiểm tra tasks/BOARD.md
        board = self.tmp_dir / "tasks" / "BOARD.md"
        self.assertTrue(board.is_file())
        self.assertIn("Task Board", board.read_text(encoding="utf-8"))

        # 3. Kiểm tra .agentbase.json
        link_file = self.tmp_dir / ".agentbase.json"
        self.assertTrue(link_file.is_file())
        data = json.loads(link_file.read_text(encoding="utf-8"))
        self.assertEqual(data.get("status"), "ready")
        self.assertEqual(data.get("roles_count"), 20)

        # 4. Kiểm tra AGENTS.md
        rule_file = self.tmp_dir / "AGENTS.md"
        self.assertTrue(rule_file.is_file())
        self.assertIn("agent-base", rule_file.read_text(encoding="utf-8"))

        # 5. Kiểm tra adapter .kilo và .agents được tạo
        kilo_dir = self.tmp_dir / ".kilo"
        self.assertTrue(kilo_dir.is_dir())
        self.assertFalse((kilo_dir / "agents").is_symlink())

        agents_dir = self.tmp_dir / ".agents"
        self.assertTrue(agents_dir.exists())

        # 6. Kiểm tra mẫu mcp.example.json được tạo an toàn
        mcp_example = self.tmp_dir / ".kilo" / "mcp.example.json"
        self.assertTrue(mcp_example.is_file())
        self.assertIn("mcpServers", mcp_example.read_text(encoding="utf-8"))

        # 7. Kiểm tra .gitignore chặn MCP cá nhân
        gitignore = self.tmp_dir / ".gitignore"
        self.assertTrue(gitignore.is_file())
        gi_content = gitignore.read_text(encoding="utf-8")
        self.assertIn(".kilo/mcp.json", gi_content)
        self.assertIn(".kilo/mcp.local.json", gi_content)


if __name__ == "__main__":
    unittest.main()
