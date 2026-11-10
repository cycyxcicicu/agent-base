"""tests/test_safe_search.py
Kiểm thử scripts/safe-search.py: quét .md/.yaml mặc định, chuẩn hóa tiếng Việt NFC/NFD,
ưu tiên tài liệu hiện hành trước archive/, giới hạn chống tràn context.
"""

import importlib.util
import io
import tempfile
import unittest
import unicodedata
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("safe_search", str(ROOT / "scripts" / "safe-search.py"))
safe_search = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(safe_search)


class TestSafeSearch(unittest.TestCase):
    def test_default_exts_include_docs_and_config(self):
        for ext in (".md", ".txt", ".yaml", ".yml", ".adoc", ".xml", ".java", ".ts", ".py"):
            self.assertIn(ext, safe_search.DEFAULT_EXTS)

    def test_searches_markdown_and_prefers_active_docs_over_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "archive"
            archive.mkdir()
            (archive / "old.md").write_text("Check trùng bản cũ\n", encoding="utf-8")
            (root / "UC-04.md").write_text("### 4.7. Quy tắc Check trùng\n", encoding="utf-8")

            out = io.StringIO()
            with redirect_stdout(out):
                rc = safe_search.search_text("Check trùng", root, safe_search.DEFAULT_EXTS, limit=10)
            self.assertEqual(rc, 0)
            text = out.getvalue()
            self.assertIn("UC-04.md:1:", text)
            self.assertLess(text.index("UC-04.md"), text.index("archive/old.md"))

    def test_vietnamese_nfc_nfd_normalization(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nfd_text = unicodedata.normalize("NFD", "Quy trình kiểm tra trùng lặp\n")
            nfc_query = unicodedata.normalize("NFC", "kiểm tra trùng")
            (root / "doc.md").write_text(nfd_text, encoding="utf-8")

            out = io.StringIO()
            with redirect_stdout(out):
                rc = safe_search.search_text(nfc_query, root, safe_search.DEFAULT_EXTS, limit=10)
            self.assertEqual(rc, 0)
            self.assertIn("doc.md:1:", out.getvalue())

    def test_normalize_exts_without_leading_dot(self):
        self.assertEqual(safe_search._normalize_exts("md, ts ,.json"), {".md", ".ts", ".json"})

    def test_single_file_target_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "note.md"
            f.write_text("Dòng 4.7 quan trọng\n", encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                rc = safe_search.search_text("4.7", f, safe_search.DEFAULT_EXTS, limit=10)
            self.assertEqual(rc, 0)
            self.assertIn("note.md:1:", out.getvalue())


if __name__ == "__main__":
    unittest.main()

