"""
tests/test_doc_preflight.py
Kiểm thử cơ chế kiểm tra bản tài liệu mới/cũ, phát hiện mâu thuẫn và superseded docs trong doc-preflight.py.
"""

import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("doc_preflight", str(ROOT / "scripts" / "doc-preflight.py"))
DP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DP)


class TestDocPreflight(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.uc_dir = self.tmp / "doc" / "features" / "UC-99-demo"
        self.uc_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_clean_single_active_spec_and_archive_ignored(self):
        (self.uc_dir / "README.md").write_text("# UC-99\n> **Active Source:** `UC-99-demo.md`\n", encoding="utf-8")
        (self.uc_dir / "UC-99-demo.md").write_text("# Spec v2\n", encoding="utf-8")
        arch = self.uc_dir / "archive"
        arch.mkdir()
        (arch / "UC-99-demo-v1.md").write_text("# Old Spec v1\n", encoding="utf-8")

        info = DP.analyze_feature(self.uc_dir)
        self.assertEqual(info["traps"], [])
        self.assertEqual(info["archive_count"], 1)
        self.assertEqual([p.name for p in info["active_primary_mds"]], ["UC-99-demo.md"])
        self.assertIn("UC-99-demo.md", info["active_source_decl"])

    def test_detects_multiple_active_docs_unless_superseded_or_declared(self):
        old_doc = self.uc_dir / "UC-99-old.md"
        new_doc = self.uc_dir / "UC-99-v2.md"
        old_doc.write_text("# Old spec\n", encoding="utf-8")
        new_doc.write_text("# New spec\n", encoding="utf-8")
        os.utime(old_doc, (1000, 1000))
        os.utime(new_doc, (2000, 2000))

        info = DP.analyze_feature(self.uc_dir)
        self.assertTrue(any("[MULTIPLE-ACTIVE-DOCS]" in t for t in info["traps"]))
        self.assertEqual(info["active_primary_mds"][0].name, "UC-99-v2.md")

        # Gắn SUPERSEDED lên bản cũ -> hết cảnh báo
        old_doc.write_text("> **STATUS: SUPERSEDED BY:** `UC-99-v2.md`\n# Old spec\n", encoding="utf-8")
        info2 = DP.analyze_feature(self.uc_dir)
        self.assertEqual(info2["traps"], [])
        self.assertEqual([p.name for p in info2["superseded_mds"]], ["UC-99-old.md"])

    def test_detects_binary_docx_newer_than_markdown(self):
        md_doc = self.uc_dir / "UC-99-demo.md"
        docx_doc = self.uc_dir / "UC-99-demo.docx"
        md_doc.write_text("# Spec MD v1\n", encoding="utf-8")
        docx_doc.write_bytes(b"fake docx v2")
        os.utime(md_doc, (1000, 1000))
        os.utime(docx_doc, (5000, 5000))

        info = DP.analyze_feature(self.uc_dir)
        self.assertTrue(any("[BINARY-NEWER-THAN-MD]" in t for t in info["traps"]))

    def test_flags_cancelled_task_cards_separately(self):
        tasks_dir = self.uc_dir / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "T-UC99.1.md").write_text("| **Trạng thái** | `cancelled` |\n", encoding="utf-8")
        (tasks_dir / "T-UC99.2.md").write_text("| **Trạng thái** | `doing` |\n", encoding="utf-8")

        info = DP.analyze_feature(self.uc_dir)
        self.assertEqual(info["active_cards"], [("T-UC99.2.md", "doing")])
        self.assertEqual(info["inactive_cards"], [("T-UC99.1.md", "cancelled")])

    def test_distinguishes_bundle_plus_usecase_from_conflicting_drawio_versions(self):
        hinh = self.uc_dir / "hinh"
        hinh.mkdir()
        (hinh / "UC-99.drawio").write_text("<mxfile/>", encoding="utf-8")
        (hinh / "UC-99-usecase.drawio").write_text("<mxfile/>", encoding="utf-8")
        (hinh / "UC-99-erd.drawio").write_text("<mxfile/>", encoding="utf-8")

        info = DP.analyze_feature(self.uc_dir)
        self.assertEqual(info["traps"], [])

        (hinh / "UC-99-moi.drawio").write_text("<mxfile/>", encoding="utf-8")
        info2 = DP.analyze_feature(self.uc_dir)
        self.assertTrue(any("[MULTIPLE-DRAWIO]" in t for t in info2["traps"]))

    def test_resolves_workspace_doc_from_raw_and_linked_worktrees(self):
        # Tạo workspace con với repo service (có docs/ riêng không chứa features/) và worktree tách rời
        repo = self.tmp / "business" / "accounting-service"
        (repo / "docs").mkdir(parents=True)
        (repo / "docs" / "README.md").write_text("# service local docs\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "Tester"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        wt_root = Path(tempfile.mkdtemp())
        try:
            wt = wt_root / "accounting-service-uc99"
            subprocess.run(["git", "-C", str(repo), "worktree", "add", "-b", "feature/uc-99", str(wt), "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 1. Raw worktree (chưa sync symlink) vẫn tìm ngược về self.tmp/doc qua git-common-dir
            ws_found, doc_found = DP.resolve_doc_and_workspace_root(wt)
            self.assertEqual(ws_found, self.tmp.resolve())
            self.assertEqual(doc_found, (self.tmp / "doc").resolve())

            # 2. Khi có doc.workspace symlink -> resolve ngay không cần git
            (wt / "doc.workspace").symlink_to(self.tmp / "doc", target_is_directory=True)
            ws_linked, doc_linked = DP.resolve_doc_and_workspace_root(wt)
            self.assertEqual(ws_linked, self.tmp.resolve())
            self.assertEqual(doc_linked, (self.tmp / "doc").resolve())
        finally:
            subprocess.run(["git", "-C", str(repo), "worktree", "remove", "--force", str(wt_root / "accounting-service-uc99")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            shutil.rmtree(wt_root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
