"""Kiểm thử mô hình học hỏi 3 tầng và các bản vá kỹ thuật liên kết đa dự án:
1. scripts/harness-reflect.py (UTF-8, doc/docs, domain-glossary filter, projects.json)
2. scripts/agent-base-diff.py & setup-project.py (.agentbase.json vs .agent-base.json)
3. scripts/knowledge.py (cmd_learn khớp chuẩn parser harness-reflect)
4. scripts/build-knowledge-catalog.py (parse_yaml_frontmatter & auto_nodes không ghi đè RAW_NODES)
"""

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Dynamic imports for scripts with hyphens in filename
def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

harness_mod = load_module("harness_reflect_mod", ROOT / "scripts" / "harness-reflect.py")
diff_mod = load_module("agent_base_diff_mod", ROOT / "scripts" / "agent-base-diff.py")
catalog_builder_mod = load_module("build_catalog_mod", ROOT / "scripts" / "build-knowledge-catalog.py")


class TestHarnessReflectionAndCrossProject(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_extract_domain_keywords_from_glossary(self):
        glossary_file = self.tmp_dir / "domain-glossary.md"
        content = """# Từ điển thuật ngữ (Domain Glossary)
| Thuật ngữ | Tiếng Anh | Định nghĩa |
|---|---|---|
| Bệnh án điện tử | Electronic Medical Record | Hồ sơ bệnh nhân nội bộ |
| Xét nghiệm máu | Blood Test | Chỉ số sinh hóa |

- **Bảo hiểm y tế**: Chế độ thanh toán BHYT
- *Tiền viện phí*: Chi phí khám chữa bệnh
- Không có gì
"""
        glossary_file.write_text(content, encoding="utf-8")
        extracted = harness_mod.extract_domain_keywords_from_glossary(glossary_file)
        self.assertIn("bệnh án điện tử", extracted)
        self.assertIn("electronic medical record", extracted)
        self.assertIn("xét nghiệm máu", extracted)
        self.assertIn("bảo hiểm y tế", extracted)
        self.assertIn("tiền viện phí", extracted)
        # Bỏ qua các từ khóa định nghĩa, stt, thuật ngữ
        self.assertNotIn("thuật ngữ", extracted)
        self.assertNotIn("định nghĩa", extracted)

    def test_cmd_learn_matches_harness_reflect_parser(self):
        from scripts.knowledge import cmd_learn
        import argparse

        # Tạo dự án với thư mục doc/notes/inbox/
        inbox_dir = self.tmp_dir / "doc" / "notes" / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)

        args = argparse.Namespace(
            root=str(self.tmp_dir),
            title="Xử lý JPA Concurrency Lock",
            note="Sử dụng Optimistic Lock với @Version để tránh xung đột cập nhật đồng thời.",
            role="architect",
            trap="Tránh dùng Pessimistic Lock trên bảng có lưu lượng truy vấn cao gây deadlock.",
            decision="Áp dụng Optimistic Lock cho tất cả Entity có giao dịch thanh toán.",
        )
        res = cmd_learn(args)
        self.assertEqual(res, 0)

        # Kiểm tra file đã được tạo trong inbox
        notes = list(inbox_dir.glob("*.md"))
        self.assertEqual(len(notes), 1)

        # Phân tích bằng parser của harness-reflect
        parsed_notes = harness_mod.parse_inbox_notes(inbox_dir)
        self.assertEqual(len(parsed_notes), 1)
        note_data = parsed_notes[0]

        self.assertEqual(note_data["summary"], "Xử lý JPA Concurrency Lock")
        self.assertEqual(note_data["task"], "LEARN")
        self.assertEqual(note_data["agent"], "architect")
        self.assertEqual(len(note_data["traps"]), 1)
        self.assertIn("Pessimistic Lock", note_data["traps"][0])
        self.assertEqual(len(note_data["decisions"]), 1)
        self.assertIn("Optimistic Lock", note_data["decisions"][0])
        self.assertEqual(len(note_data["lessons"]), 1)
        self.assertIn("Optimistic Lock với @Version", note_data["lessons"][0])

    def test_agent_base_diff_find_meta_file(self):
        # 1. Thư mục có .agent-base.json
        dir1 = self.tmp_dir / "p1"
        dir1.mkdir()
        (dir1 / ".agent-base.json").write_text('{"source": "/path1"}', encoding="utf-8")
        self.assertEqual(diff_mod.find_meta_file(dir1).name, ".agent-base.json")

        # 2. Thư mục có .agentbase.json
        dir2 = self.tmp_dir / "p2"
        dir2.mkdir()
        (dir2 / ".agentbase.json").write_text('{"hub_path": "/path2"}', encoding="utf-8")
        self.assertEqual(diff_mod.find_meta_file(dir2).name, ".agentbase.json")

    def test_parse_yaml_frontmatter(self):
        text = """---
id: Design:cloud-recipes
kind: Design
title: Cloud Architecture Recipes
owner_role: architect
version: 2
keywords:
  - aws
  - k8s
  - cloud
relations:
  - type: owned_by
    target: Role:architect
  - type: related_to
    target: Design:clean-architecture-and-ddd
---
# Nội dung chính
Đây là bài viết chi tiết...
"""
        fm = catalog_builder_mod.parse_yaml_frontmatter(text)
        self.assertIsNotNone(fm)
        self.assertEqual(fm["id"], "Design:cloud-recipes")
        self.assertEqual(fm["kind"], "Design")
        self.assertEqual(fm["title"], "Cloud Architecture Recipes")
        self.assertEqual(fm["owner_role"], "architect")
        self.assertEqual(fm["version"], 2)
        self.assertEqual(fm["keywords"], ["aws", "k8s", "cloud"])
        self.assertEqual(len(fm["relations"]), 2)
        self.assertEqual(fm["relations"][0], {"type": "owned_by", "target": "Role:architect"})

    def test_auto_nodes_frontmatter_scanner_does_not_overwrite_raw_nodes(self):
        # Kiểm tra rằng auto_nodes tôn trọng RAW_NODES và không ghi đè
        taken_refs = {r["content_ref"] for r in catalog_builder_mod.RAW_NODES}
        taken_ids = {r["id"] for r in catalog_builder_mod.RAW_NODES}

        # Tạo file tạm trong một thư mục giả lập
        knowledge_dir = self.tmp_dir / "agents" / "knowledge" / "custom"
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        sample_file = knowledge_dir / "custom-topic.md"
        sample_file.write_text("""---
id: Design:custom-topic
kind: Design
title: Custom Knowledge Topic
owner_role: dev
relations:
  - type: owned_by
    target: Role:dev
---
# Custom Topic
""", encoding="utf-8")

        nodes = catalog_builder_mod.auto_nodes(self.tmp_dir)
        custom_node = next((n for n in nodes if n["id"] == "Design:custom-topic"), None)
        self.assertIsNotNone(custom_node)
        self.assertEqual(custom_node["title"], "Custom Knowledge Topic")
        self.assertEqual(custom_node["owner_role"], "dev")

        # Đảm bảo không trùng với bất kỳ ID nào trong RAW_NODES
        self.assertNotIn(custom_node["id"], taken_ids)


if __name__ == "__main__":
    unittest.main()
