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

            out = _run_main(root, check=True)
            self.assertIn("OK: generated files are up to date.", out)


if __name__ == "__main__":
    unittest.main()
