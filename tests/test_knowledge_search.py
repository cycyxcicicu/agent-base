"""Kiểm thử bộ xếp hạng tra cứu (agent_core/knowledge/search.py)."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent_core.knowledge import search as S  # noqa: E402
from agent_core.knowledge.catalog import load_catalog  # noqa: E402


class TestSearchHelpers(unittest.TestCase):
    def test_normalize_removes_diacritics_and_keeps_n_plus_one(self):
        self.assertEqual(S.normalize("Chỉ mục Đồng bộ"), "chi muc dong bo")
        self.assertEqual(S.normalize("JPA N+1"), "jpa nplus1")

    def test_stopwords_are_dropped_but_never_empty_the_query(self):
        self.assertEqual(S.tokens_of("viết câu sql chậm"), ["cau", "sql", "cham"])
        self.assertTrue(S.tokens_of("của và"))  # toàn chữ nhiễu thì giữ nguyên, không rỗng

    def test_prefix_matching_handles_plurals(self):
        self.assertTrue(S._has("migrations", {"migration"}))
        self.assertFalse(S._has("sql", {"sqlite"}))  # từ ngắn phải khớp đúng


class TestRanking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(str(ROOT), filename="agents/knowledge/knowledge-manifest.json")

    def top(self, q, role=None):
        return [n.id for _, n in S.rank(self.catalog, str(ROOT), q, role)[:3]]

    def test_works_without_vietnamese_diacritics(self):
        self.assertIn("Design:zero-downtime-migrations", self.top("doi schema khong dung he thong"))

    def test_synonyms_bridge_vietnamese_and_english_terms(self):
        self.assertIn("Skill:ponytail-debt", self.top("nợ kỹ thuật"))

    def test_role_gives_a_small_boost_only(self):
        # vai không được lật kết quả khi từ khóa khớp rõ một nút khác
        self.assertEqual(self.top("kubernetes", "qa")[0], "Design:kubernetes-architecture-and-manifests")

    def test_empty_or_noise_query_returns_nothing_crashing(self):
        self.assertEqual(S.rank(self.catalog, str(ROOT), ""), [])
        self.assertIsInstance(S.rank(self.catalog, str(ROOT), "zzzxqj"), list)


if __name__ == "__main__":
    unittest.main()
