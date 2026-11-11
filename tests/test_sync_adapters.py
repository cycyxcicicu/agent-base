"""
tests/test_sync_adapters.py
Khóa hành vi sinh adapter Qoder: map công cụ theo vai, loader trung tính,
dọn file mồ côi và phát hiện drift bằng --check.
"""

import importlib.util
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("sync_adapters", str(ROOT / "scripts" / "sync-adapters.py"))
_argv = sys.argv
try:
    sys.argv = [str(ROOT / "scripts" / "sync-adapters.py"), "--check"]
    sync_adapters = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(sync_adapters)
finally:
    sys.argv = _argv


def _meta(**overrides):
    meta = {"name": "dev", "description": "Vai dev", "mode": "all", "bash": "full", "web": "deny"}
    meta.update(overrides)
    return meta


def _run_main(root: Path, check: bool):
    old_root, old_check = sync_adapters.ROOT, sync_adapters.CHECK
    sync_adapters.ROOT, sync_adapters.CHECK = root, check
    out = io.StringIO()
    try:
        with redirect_stdout(out):
            sync_adapters.main()
    finally:
        sync_adapters.ROOT, sync_adapters.CHECK = old_root, old_check
    return out.getvalue()


def _make_project(root: Path):
    (root / "agents" / "roles").mkdir(parents=True)
    (root / "AGENTS.md").write_text("rules\n", encoding="utf-8")
    (root / "agents" / "models.txt").write_text("", encoding="utf-8")
    (root / "agents" / "roles" / "lead.md").write_text(
        "---\nname: lead\ndescription: Lead\nmode: primary\nbash: full\n---\n\n# Lead\n", encoding="utf-8")
    (root / "agents" / "roles" / "dev.md").write_text(
        "---\nname: dev\ndescription: Dev\nmode: all\nbash: full\nedit_allow:\n  - src/**\n---\n\n# Dev\n",
        encoding="utf-8")


class TestQoderAdapters(unittest.TestCase):
    def test_loader_is_neutral_and_marked(self):
        text = sync_adapters.QODER_LOADER_RULE
        self.assertIn("trigger: model_decision", text)
        self.assertIn("description:", text)
        self.assertIn(sync_adapters.MARKER, text)
        self.assertIn("docs/notes/INDEX.md", text)
        self.assertIn("docs/notes/inbox", text)
        self.assertNotIn("Humana", text)
        body = text.split("-->\n", 1)[1].strip().splitlines()
        self.assertLessEqual(len(body), 9, "loader phai sieu ngon de tiep tuc nap du re")

    def test_readonly_role_has_no_write(self):
        text = sync_adapters.build_qoder(_meta(name="runner", bash="readonly"), "body", "agents/roles/runner.md")
        self.assertIn("tools: Read, Grep, Glob, Bash", text)
        self.assertNotIn("Write", text)

    def test_edit_allow_maps_write_and_web_deny(self):
        text = sync_adapters.build_qoder(_meta(edit_allow=["src/**"]), "body", "agents/roles/dev.md")
        self.assertIn("Edit", text)
        self.assertIn("Write", text)
        self.assertNotIn("WebFetch", text)

    def test_sweep_removes_marked_orphan_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rules = root / ".qoder" / "rules"
            rules.mkdir(parents=True)
            orphan = rules / "00-humana-loader.md"
            orphan.write_text(f"<!-- {sync_adapters.MARKER} -->\n", encoding="utf-8")
            manual = rules / "manual.md"
            manual.write_text("hand-written\n", encoding="utf-8")
            agents = root / ".qoder" / "agents"
            agents.mkdir(parents=True)
            manual_agent = agents / "manual.md"
            manual_agent.write_text("hand-written\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(sync_adapters.sweep_stale(root, {}, check=False), 0)
            self.assertFalse(orphan.exists())
            self.assertTrue(manual.exists())
            self.assertTrue(manual_agent.exists())

    def test_sweep_check_reports_stale_without_deleting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rules = root / ".qoder" / "rules"
            rules.mkdir(parents=True)
            orphan = rules / "00-humana-loader.md"
            orphan.write_text(f"<!-- {sync_adapters.MARKER} -->\n", encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                problems = sync_adapters.sweep_stale(root, {}, check=True)
            self.assertEqual(problems, 1)
            self.assertIn("STALE", out.getvalue())
            self.assertTrue(orphan.exists())

    def test_generates_all_roles_and_is_idempotent(self):
        roles = sorted((ROOT / "agents" / "roles").glob("*.md"))
        self.assertEqual(len(roles), 21)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "agents" / "roles").mkdir(parents=True)
            shutil.copy(ROOT / "AGENTS.md", root / "AGENTS.md")
            shutil.copy(ROOT / "agents" / "models.txt", root / "agents" / "models.txt")
            for role in roles:
                shutil.copy(role, root / "agents" / "roles" / role.name)

            _run_main(root, check=False)
            first = {p.name: p.read_text(encoding="utf-8") for p in (root / ".qoder").rglob("*.md")}
            _run_main(root, check=False)
            second = {p.name: p.read_text(encoding="utf-8") for p in (root / ".qoder").rglob("*.md")}

            self.assertEqual(len(second) - 1, len(roles))  # trừ loader
            self.assertEqual(first, second)

    def test_check_detects_missing_qoder_files_then_generates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_project(root)
            with self.assertRaises(SystemExit) as ctx:
                _run_main(root, check=True)
            self.assertEqual(ctx.exception.code, 1)

            _run_main(root, check=False)
            self.assertTrue((root / ".qoder" / "agents" / "lead.md").is_file())
            self.assertTrue((root / ".qoder" / "agents" / "dev.md").is_file())
            self.assertTrue((root / ".qoder" / "rules" / "00-agent-loader.md").is_file())
            self.assertTrue((root / "CLAUDE.md").is_file())
            self.assertTrue((root / "GEMINI.md").is_file())
            self.assertIn("Cơ chế Subagents trong Claude Code", (root / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertIn("Hướng dẫn riêng cho Gemini Code Assist", (root / "GEMINI.md").read_text(encoding="utf-8"))

            out = _run_main(root, check=True)
            self.assertIn("OK: generated files are up to date.", out)

    def test_build_claude_excludes_powershell_and_keeps_posix_tools(self):
        # Role dev has bash: full, edit_allow
        text = sync_adapters.build_claude(_meta(name="dev", bash="full", edit_allow=["src/**"]), "body", "agents/roles/dev.md")
        self.assertIn("tools: Read, Grep, Glob, Edit, Write, Bash", text)
        self.assertNotIn("PowerShell", text)

        # Role runner has bash: readonly, no edit_allow
        text_runner = sync_adapters.build_claude(_meta(name="runner", bash="readonly"), "body", "agents/roles/runner.md")
        self.assertIn("tools: Read, Grep, Glob, Bash", text_runner)
        self.assertNotIn("PowerShell", text_runner)

        # Role researcher has bash: deny, web: allow
        text_researcher = sync_adapters.build_claude(_meta(name="researcher", bash="deny", web="allow"), "body", "agents/roles/researcher.md")
        self.assertIn("tools: Read, Grep, Glob, WebFetch, WebSearch", text_researcher)
        self.assertNotIn("PowerShell", text_researcher)

    def test_all_generated_claude_agents_have_no_powershell_and_only_valid_posix_tools(self):
        claude_agents_dir = ROOT / ".claude" / "agents"
        agent_files = list(claude_agents_dir.glob("*.md"))
        self.assertEqual(len(agent_files), 20)
        allowed_tools = {"Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"}

        for f in agent_files:
            content = f.read_text(encoding="utf-8")
            tool_line = next((line for line in content.splitlines() if line.startswith("tools:")), None)
            self.assertIsNotNone(tool_line, f"{f.name} missing tools declaration")
            tools = [t.strip() for t in tool_line.replace("tools:", "").split(",") if t.strip()]
            self.assertNotIn("PowerShell", tools, f"{f.name} contains PowerShell tool")
            for t in tools:
                self.assertIn(t, allowed_tools, f"{f.name} contains invalid tool {t}")

    def test_claude_md_generated_with_agents_md_and_subagents_guide(self):
        claude_path = ROOT / "CLAUDE.md"
        self.assertTrue(claude_path.is_file())
        content = claude_path.read_text(encoding="utf-8")
        self.assertNotIn("@AGENTS.md", content)
        self.assertIn(sync_adapters.MARKER, content)
        self.assertIn("# AGENTS.md — quy tắc chung cho mọi agent", content)
        self.assertIn("Cơ chế Subagents trong Claude Code (`.claude/agents/`)", content)

    def test_gemini_md_generated_with_role_instructions(self):
        gemini_path = ROOT / "GEMINI.md"
        self.assertTrue(gemini_path.is_file())
        content = gemini_path.read_text(encoding="utf-8")
        self.assertIn(sync_adapters.MARKER, content)
        self.assertIn("# AGENTS.md — quy tắc chung cho mọi agent", content)
        self.assertIn("Hướng dẫn riêng cho Gemini Code Assist", content)
        self.assertIn("agents/roles/", content)

    def test_sync_global_claude_permissions_preserves_env_hooks_and_dirs(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            fake_claude_dir = Path(tmp) / ".claude"
            fake_claude_dir.mkdir(parents=True)
            target = fake_claude_dir / "settings.json"
            target.write_text(json.dumps({
                "env": {"TEST_KEY": "preserve-me"},
                "hooks": {"PreToolUse": [{"matcher": "Bash"}]},
                "theme": "dark",
                "permissions": {
                    "additionalDirectories": [tmp],
                    "deny": ["Bash(git  *)"],
                },
            }), encoding="utf-8")
            hub_settings = {
                "permissions": {
                    "additionalDirectories": [str(ROOT)],
                    "allow": ["Bash(git status*)"],
                    "deny": ["Bash(git reset*)"],
                    "ask": ["Bash(git commit*)"],
                }
            }
            with redirect_stdout(io.StringIO()):
                backup = sync_adapters.sync_global_claude_permissions(hub_settings, target_path=target)
            self.assertIsNotNone(backup)
            self.assertTrue(backup.is_file())
            updated = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(updated["env"], {"TEST_KEY": "preserve-me"})
            self.assertEqual(updated["hooks"], {"PreToolUse": [{"matcher": "Bash"}]})
            self.assertEqual(updated["theme"], "dark")
            self.assertEqual(updated["permissions"]["allow"], ["Bash(git status*)"])
            self.assertEqual(updated["permissions"]["deny"], ["Bash(git reset*)"])
            self.assertEqual(updated["permissions"]["ask"], ["Bash(git commit*)"])
            self.assertIn(str(Path(tmp).resolve()), updated["permissions"]["additionalDirectories"])
            self.assertIn(str(ROOT.resolve()), updated["permissions"]["additionalDirectories"])

    def test_load_registered_project_dirs_merges_active_projects_into_global_claude(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            ws_dir = tmp_path / "demo-workspace"
            ws_dir.mkdir()
            (tmp_path / "projects.local.json").write_text(json.dumps({
                "projects": [
                    {"id": "demo", "path": str(ws_dir), "is_active": True},
                    {"id": "missing", "path": str(tmp_path / "does-not-exist"), "is_active": True},
                    {"id": "inactive", "path": str(tmp_path), "is_active": False},
                ]
            }), encoding="utf-8")
            dirs = sync_adapters._load_registered_project_dirs(tmp_path)
            self.assertEqual(dirs, [str(ws_dir.resolve())])

            target = tmp_path / "settings.json"
            target.write_text(json.dumps({"permissions": {"additionalDirectories": []}}), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                sync_adapters.sync_global_claude_permissions({"permissions": {}}, target_path=target, extra_dirs=dirs)
            updated = json.loads(target.read_text(encoding="utf-8"))
            self.assertIn(str(ws_dir.resolve()), updated["permissions"]["additionalDirectories"])


if __name__ == "__main__":
    unittest.main()
