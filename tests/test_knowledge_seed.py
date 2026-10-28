"""Kiểm thử seed tri thức agents/knowledge/knowledge-manifest.json và examples/knowledge/catalog.json.
Đáp ứng yêu cầu T-28.1 (Contract & Happy Path).
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from agent_core.knowledge.catalog import load_catalog, validate_catalog


class TestKnowledgeSeed(unittest.TestCase):
    def test_seed_knowledge_manifest_valid(self):
        seed_path = ROOT / "agents" / "knowledge" / "knowledge-manifest.json"
        self.assertTrue(seed_path.exists(), "Seed manifest phải tồn tại")

        catalog = load_catalog(str(ROOT), filename="agents/knowledge/knowledge-manifest.json")
        diags = validate_catalog(catalog)
        self.assertEqual(len(diags), 0, f"Seed manifest phải hợp lệ, phát hiện lỗi: {[d.to_dict() for d in diags]}")

        # Kiểm tra nội dung: không node approved, draft sạch sẽ
        data = json.loads(seed_path.read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            self.assertEqual(node.get("state"), "draft", f"Node {node.get('id')} không được là approved")
            # Không chứa tên nhạy cảm
            title = node.get("title", "")
            self.assertNotIn("gdt", title.lower())
            self.assertNotIn("lauren tan", title.lower())

    def test_example_catalog_valid(self):
        example_path = ROOT / "examples" / "knowledge" / "catalog.json"
        self.assertTrue(example_path.exists(), "Example catalog phải tồn tại")

        catalog = load_catalog(str(ROOT), filename="examples/knowledge/catalog.json")
        diags = validate_catalog(catalog)
        self.assertEqual(len(diags), 0, f"Example catalog phải hợp lệ: {[d.to_dict() for d in diags]}")


if __name__ == "__main__":
    unittest.main()
