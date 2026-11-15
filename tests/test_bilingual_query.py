#!/usr/bin/env python3
"""tests/test_bilingual_query.py

Unit test cho công cụ scripts/bilingual-query.py (Cầu nối truy vấn song ngữ Việt - Anh).
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("bilingual_query", str(ROOT / "scripts" / "bilingual-query.py"))
bilingual_query = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bilingual_query)


class TestBilingualQuery(unittest.TestCase):
    def test_normalize_vietnamese(self):
        norm = bilingual_query.normalize_vietnamese("Khóa Lạc Quan & Vận Đơn")
        self.assertEqual(norm, "khoa lac quan & van don")

    def test_expand_query_core_mappings(self):
        res = bilingual_query.expand_bilingual_query("cần xử lý xuất đơn và kiểm tra khóa lạc quan")
        self.assertIn("xuất đơn", res["matched_vi_concepts"])
        self.assertIn("khóa lạc quan", res["matched_vi_concepts"])
        self.assertIn("dispatch", res["expanded_en_code_tokens"])
        self.assertIn("optimistic_lock", res["expanded_en_code_tokens"])

    def test_expand_query_with_custom_synonyms(self):
        mock_synonyms = {
            "thông báo đẩy": "fcm push notification device token alert",
        }
        res = bilingual_query.expand_bilingual_query("gửi thông báo đẩy cho shipper", synonyms_dict=mock_synonyms)
        self.assertIn("thông báo đẩy", res["matched_vi_concepts"])
        self.assertIn("notification", res["expanded_en_code_tokens"])
        self.assertIn("push", res["expanded_en_code_tokens"])


if __name__ == "__main__":
    unittest.main()
