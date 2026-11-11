"""
tests/test_worktree_manager.py
Kiểm thử cơ chế kế thừa quy tắc workspace & bảo vệ file Git tracked trong worktree-manager.py.
"""

import importlib.util
import shutil
import subprocess
import tempfile
import time
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("worktree_manager", str(ROOT / "scripts" / "worktree-manager.py"))
WM = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WM)


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


class TestWorktreeManager(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ws_root = self.tmp / "gdt-workspace"
        self.worktrees_dir = self.tmp / "worktrees"
        self.ws_root.mkdir()
        self.worktrees_dir.mkdir()

        # Thiết lập tài liệu và cấu hình giả lập tại workspace gốc
        (self.ws_root / "AGENTS.md").write_text("# Root AGENTS\n" * 20, encoding="utf-8")
        (self.ws_root / "CLAUDE.md").write_text("# Root CLAUDE\n@AGENTS.md\n", encoding="utf-8")
        (self.ws_root / "GEMINI.md").write_text("# Root GEMINI\n", encoding="utf-8")
        (self.ws_root / "PROJECT.md").write_text("# Root PROJECT\n", encoding="utf-8")
        (self.ws_root / "mcp.json").write_text("{}\n", encoding="utf-8")
        (self.ws_root / "doc" / "architecture" / "engineering").mkdir(parents=True)
        (self.ws_root / "doc" / "architecture" / "CODEMAP.md").write_text("# Codemap\n", encoding="utf-8")
        (self.ws_root / "doc" / "delivery" / "tasks").mkdir(parents=True)
        (self.ws_root / "doc" / "delivery" / "tasks" / "BOARD.md").write_text("# Board\n", encoding="utf-8")
        (self.ws_root / "doc" / "features" / "UC-06-department-based-access").mkdir(parents=True)

        self.old_ws = WM.WORKSPACE_ROOT
        self.old_wts = WM.WORKTREES_DIR
        self.old_reg_json = WM.REGISTRY_JSON
        self.old_reg_md = WM.REGISTRY_MD
        WM.WORKSPACE_ROOT = self.ws_root
        WM.WORKTREES_DIR = self.worktrees_dir
        WM.REGISTRY_JSON = self.ws_root / "doc/governance/standards/worktree-registry.json"
        WM.REGISTRY_MD = self.ws_root / "doc/governance/standards/worktree-registry.md"

    def tearDown(self):
        WM.WORKSPACE_ROOT = self.old_ws
        WM.WORKTREES_DIR = self.old_wts
        WM.REGISTRY_JSON = self.old_reg_json
        WM.REGISTRY_MD = self.old_reg_md
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _init_repo_with_worktree(self, wt_name: str, with_tracked_agents_stub: bool) -> tuple[Path, Path]:
        repo = self.ws_root / "business" / "accounting-service"
        repo.mkdir(parents=True)
        _git(repo, "init", "-b", "main")
        _git(repo, "config", "user.name", "Tester")
        _git(repo, "config", "user.email", "tester@example.com")
        (repo / "README.md").write_text("service\n", encoding="utf-8")
        if with_tracked_agents_stub:
            (repo / "AGENTS.md").write_text("# iam-service overrides\nstub\n", encoding="utf-8")
        _git(repo, "add", ".")
        _git(repo, "commit", "-m", "init")

        wt = self.worktrees_dir / wt_name
        _git(repo, "worktree", "add", "-b", "feature/uc-06", str(wt), "main")
        return repo, wt

    def test_tracked_agents_stub_not_overwritten_and_workspace_links_created(self):
        _, wt = self._init_repo_with_worktree("accounting-service-uc06", with_tracked_agents_stub=True)

        # Giả lập worktree từng bị script cũ thay nhầm AGENTS.md thành symlink -> kiểm tra khả năng tự phục hồi
        (wt / "AGENTS.md").unlink()
        (wt / "AGENTS.md").symlink_to(self.ws_root / "AGENTS.md")

        WM.inject_worktree_rules(wt, service_name="accounting-service", task_code="UC-06")

        # 1. File tracked AGENTS.md được phục hồi sạch, git status không bẩn
        self.assertFalse((wt / "AGENTS.md").is_symlink())
        self.assertIn("iam-service overrides", (wt / "AGENTS.md").read_text(encoding="utf-8"))
        status = _git(wt, "status", "--porcelain").stdout.strip()
        self.assertEqual(status, "", f"git status phải sạch, thực tế: {status}")

        # 2. Symlink workspace và CLAUDE.md định tuyến đúng tới feature UC-06
        self.assertEqual((wt / "AGENTS.workspace.md").resolve(), (self.ws_root / "AGENTS.md").resolve())
        self.assertEqual((wt / "CLAUDE.workspace.md").resolve(), (self.ws_root / "CLAUDE.md").resolve())
        self.assertEqual((wt / "PROJECT.workspace.md").resolve(), (self.ws_root / "PROJECT.md").resolve())
        self.assertEqual((wt / "GEMINI.md").resolve(), (self.ws_root / "GEMINI.md").resolve())

        claude_md = (wt / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("@AGENTS.workspace.md", claude_md)
        self.assertIn("@CLAUDE.workspace.md", claude_md)
        self.assertIn("@PROJECT.workspace.md", claude_md)
        self.assertIn("UC-06-department-based-access", claude_md)
        self.assertIn('prefix="gdt"', claude_md)
        self.assertIn("safe-search.py", claude_md)

    def test_untracked_repo_gets_clean_agents_symlink_and_excludes(self):
        _, wt = self._init_repo_with_worktree("ws-sdk-uc06", with_tracked_agents_stub=False)

        WM.inject_worktree_rules(wt, service_name="ws-sdk", task_code="UC-06")

        self.assertTrue((wt / "AGENTS.md").is_symlink())
        self.assertEqual((wt / "AGENTS.md").resolve(), (self.ws_root / "AGENTS.md").resolve())
        self.assertEqual((wt / "AGENTS.workspace.md").resolve(), (self.ws_root / "AGENTS.md").resolve())
        status = _git(wt, "status", "--porcelain").stdout.strip()
        self.assertEqual(status, "", f"git status phải sạch, thực tế: {status}")

    def test_doc_workspace_symlink_idempotency_and_foreign_repo_isolation(self):
        (self.ws_root / ".ai-rules").mkdir()
        (self.ws_root / ".ai-rules" / "rule.md").write_text("# rule\n", encoding="utf-8")
        _, wt = self._init_repo_with_worktree("accounting-service-uc06", with_tracked_agents_stub=True)

        WM.inject_worktree_rules(wt, service_name="accounting-service", task_code="UC-06")
        self.assertEqual((wt / "doc.workspace").resolve(), (self.ws_root / "doc").resolve())
        self.assertEqual((wt / ".ai-rules.workspace").resolve(), (self.ws_root / ".ai-rules").resolve())
        self.assertEqual(_git(wt, "status", "--porcelain").stdout.strip(), "")

        # Idempotent sync_all: lần sync thứ hai khi không đổi gì phải trả False ở save_registry và giữ nguyên CLAUDE.md
        WM.sync_all()
        first_mtime_ns = (wt / "CLAUDE.md").stat().st_mtime_ns
        time.sleep(0.02)
        reg2 = WM.sync_all()
        self.assertEqual((wt / "CLAUDE.md").stat().st_mtime_ns, first_mtime_ns)
        self.assertFalse(WM.save_registry(reg2))

        # Worktree thuộc repo khác ngoài workspace phải bị bỏ qua khỏi workspace này
        foreign = self.tmp / "other-project"
        foreign.mkdir()
        _git(foreign, "init", "-b", "main")
        _git(foreign, "config", "user.name", "Tester")
        _git(foreign, "config", "user.email", "tester@example.com")
        (foreign / "README.md").write_text("other\n", encoding="utf-8")
        _git(foreign, "add", ".")
        _git(foreign, "commit", "-m", "init")
        foreign_wt = self.worktrees_dir / "other-project-feat"
        _git(foreign, "worktree", "add", "-b", "feat/x", str(foreign_wt), "main")

        self.assertTrue(WM._belongs_to_workspace(wt, self.ws_root))
        self.assertFalse(WM._belongs_to_workspace(foreign_wt, self.ws_root))

    def test_install_watcher_renders_valid_watchpaths_plist_without_side_effects(self):
        plist_path = self.tmp / "LaunchAgents" / f"{WM.WATCHER_LABEL}.plist"
        out_path = WM.install_watcher(plist_path=plist_path, load_launchd=False, python_bin="/usr/bin/python3")
        self.assertEqual(out_path, plist_path)
        self.assertTrue(plist_path.is_file())

        root = ET.fromstring(plist_path.read_text(encoding="utf-8"))
        text_dump = plist_path.read_text(encoding="utf-8")
        self.assertEqual(root.tag, "plist")
        self.assertIn(WM.WATCHER_LABEL, text_dump)
        self.assertIn(str(self.worktrees_dir.resolve()), text_dump)
        self.assertIn("--debounce", text_dump)
        self.assertIn("WatchPaths", text_dump)


if __name__ == "__main__":
    unittest.main()

