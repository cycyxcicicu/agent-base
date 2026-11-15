#!/usr/bin/env python3
"""tests/test_memory_query.py

Unit test cho công cụ scripts/memory-query.py (Tiered Memory Retrieval & Deduplication).
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("memory_query", str(ROOT / "scripts" / "memory-query.py"))
memory_query = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(memory_query)


class TestMemoryQuery(unittest.TestCase):
    def test_deduplicate_entries(self):
        entries = [
            {"id": "N-01", "date": "2026-11-10", "source": "TEST", "scope": "Auth", "content": "Luôn dùng Bearer token chuẩn"},
            {"id": "N-02", "date": "2026-11-11", "source": "TEST", "scope": "Auth", "content": "Luôn dùng Bearer token chuẩn"}, # trùng
            {"id": "N-03", "date": "2026-11-12", "source": "TEST", "scope": "DB", "content": "Tạo index cho foreign key"},
        ]
        deduped, dups = memory_query.deduplicate_entries(entries)
        self.assertEqual(len(deduped), 2)
        self.assertEqual(dups, 1)

    def test_search_memories_keyword_match(self):
        entries = [
            {"id": "N-01", "scope": "JWT", "content": "Cẩn thận bẫy expired token khi refresh"},
            {"id": "N-02", "scope": "Docker", "content": "Dùng multi-stage build để tối ưu dung lượng image"},
            {"id": "N-03", "scope": "JPA", "content": "Tránh N+1 query bằng cách dùng EntityGraph"},
        ]
        results = memory_query.search_memories("expired token", entries, limit=2)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1]["id"], "N-01")


if __name__ == "__main__":
    unittest.main()
