#!/usr/bin/env python3
"""tests/test_hybrid_search.py

Unit test cho công cụ scripts/hybrid-search.py (Bộ tìm kiếm kết hợp & chẩn đoán truy vấn thông minh).
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("hybrid_search", str(ROOT / "scripts" / "hybrid-search.py"))
hybrid_search = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hybrid_search)


class TestHybridSearch(unittest.TestCase):
    def test_is_likely_code_identifier(self):
        self.assertTrue(hybrid_search.is_likely_code_identifier("OrderController"))
        self.assertTrue(hybrid_search.is_likely_code_identifier("find_by_id"))
        self.assertTrue(hybrid_search.is_likely_code_identifier("getUserProfile"))
        self.assertFalse(hybrid_search.is_likely_code_identifier("xuất đơn hàng"))
        self.assertFalse(hybrid_search.is_likely_code_identifier("xác nhận thanh toán"))
        self.assertFalse(hybrid_search.is_likely_code_identifier("search with spaces"))

    def test_execute_hybrid_search_routing(self):
        # 1. Identifier -> AST_SEARCH
        res_ast = hybrid_search.execute_hybrid_search("PaymentService")
        self.assertEqual(res_ast["mode"], "AST_SEARCH")
        self.assertIn("xerj", res_ast["ast_command"])

        # 2. Tiếng Việt -> LAYERED_HYBRID
        res_vi = hybrid_search.execute_hybrid_search("Xác nhận xuất kho")
        self.assertEqual(res_vi["mode"], "LAYERED_HYBRID")
        self.assertIn("safe-search.py", res_vi["text_search_command"])


if __name__ == "__main__":
    unittest.main()
