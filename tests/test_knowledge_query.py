"""Kiểm thử tra cứu tri thức theo nhu cầu (knowledge.py query): trả tóm tắt, mục và đường dẫn, không nạp cả file."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def query(*args):
    return subprocess.run([sys.executable, "scripts/knowledge.py", "query", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


class TestKnowledgeQuery(unittest.TestCase):
    def test_default_manifest_is_the_framework_catalog(self):
        r = query("-q", "mô tả hoạt động sơ đồ", "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        top = json.loads(r.stdout)[0]
        self.assertEqual(top["id"], "Design:diagram-mo-ta-hoat-dong-so-do")

    def test_each_hit_has_summary_headings_and_size(self):
        hits = json.loads(query("-q", "jpa n+1", "--format", "json").stdout)
        self.assertTrue(hits)
        for h in hits:
            self.assertTrue(h["summary"], f"{h['id']} thiếu tóm tắt")
            self.assertTrue(h["headings"], f"{h['id']} thiếu danh sách mục")
            self.assertGreater(h["tokens"], 0)

    def test_text_output_stays_small_for_large_files(self):
        r = query("-q", "mô tả hoạt động sơ đồ")
        self.assertIn("Tóm tắt:", r.stdout)
        self.assertIn("Mục:", r.stdout)
        # ngân sách 1.200 token (khoảng 3.600 byte chữ) cho mỗi lần tra: đầu ra không được bằng cả file
        self.assertLess(len(r.stdout), 9000)

    def test_unknown_keyword_reports_nothing_found(self):
        r = query("-q", "zzzxqj-khong-co")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Không tìm thấy", r.stdout)


if __name__ == "__main__":
    unittest.main()
