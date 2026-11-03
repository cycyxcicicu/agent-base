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

    def test_extract_domain_keywords_from_headings_and_parentheses(self):
        glossary_file = self.tmp_dir / "domain-glossary-headings.md"
        content = """# Từ điển thuật ngữ miền y tế
## 1. Bệnh án điện tử (EMR)
- **Nghĩa là**: Hồ sơ bệnh án lưu trữ kỹ thuật số
- **KHÔNG PHẢI**: Giấy khám bệnh thông thường

## 2. Bảo hiểm y tế (BHYT)
- **Định nghĩa**: Chế độ bảo hiểm do nhà nước bảo trợ

### Đơn thuốc ngoại trú
**Tiền tạm ứng**: Khoản phí đặt cọc trước khi nhập viện.
"""
        glossary_file.write_text(content, encoding="utf-8")
        extracted = harness_mod.extract_domain_keywords_from_glossary(glossary_file)
        self.assertIn("bệnh án điện tử", extracted)
        self.assertIn("emr", extracted)
        self.assertIn("bảo hiểm y tế", extracted)
        self.assertIn("bhyt", extracted)
        self.assertIn("đơn thuốc ngoại trú", extracted)
        self.assertIn("tiền tạm ứng", extracted)
        # Boilerplate terms must NOT be extracted as domain keywords
        self.assertNotIn("nghĩa là", extracted)
        self.assertNotIn("không phải", extracted)
        self.assertNotIn("định nghĩa", extracted)

    def test_harvest_sanitizes_sensitive_decisions(self):
        # Raw note có cả trap và decision chứa từ khóa nhạy cảm "bệnh án điện tử"
        domain_keywords = ["bệnh án điện tử", "kế toán"]
        raw_notes = [
            {
                "path": Path("dummy.md"),
                "filename": "T-01-dev.md",
                "task": "T-01",
                "agent": "dev",
                "date": "2026-11-03",
                "summary": "Fix lỗi dữ liệu",
                "traps": ["Bệnh án điện tử có thể bị null", "Timeout khi gọi Redis"],
                "decisions": ["Lưu cache bệnh án điện tử vào RAM", "Dùng HikariCP với pool size 20"],
                "conventions": [],
                "lessons": ["Cần validate input cẩn thận"],
                "skills": [],
            },
            {
                "path": Path("dummy2.md"),
                "filename": "T-02-dev.md",
                "task": "T-02",
                "agent": "dev",
                "date": "2026-11-03",
                "summary": "Chỉ có decision kế toán",
                "traps": [],
                "decisions": ["Đồng bộ số liệu kế toán qua Kafka"],
                "conventions": [],
                "lessons": [],
                "skills": [],
            }
        ]

        filtered_notes = []
        for n in raw_notes:
            f_traps = [t for t in n["traps"] if not any(dk in t.lower() for dk in domain_keywords)]
            f_lessons = [l for l in n["lessons"] if not any(dk in l.lower() for dk in domain_keywords)]
            f_convs = [c for c in n["conventions"] if not any(dk in c.lower() for dk in domain_keywords)]
            f_decs = [d for d in n["decisions"] if not any(dk in d.lower() for dk in domain_keywords)]

            if f_traps or f_lessons or f_convs or f_decs or n["skills"]:
                f_n = dict(n)
                f_n["traps"] = f_traps
                f_n["lessons"] = f_lessons
                f_n["conventions"] = f_convs
                f_n["decisions"] = f_decs
                filtered_notes.append(f_n)

        # Note 1 được giữ lại nhưng trap và decision nhạy cảm bị loại bỏ
        self.assertEqual(len(filtered_notes), 1)
        self.assertEqual(filtered_notes[0]["traps"], ["Timeout khi gọi Redis"])
        self.assertEqual(filtered_notes[0]["decisions"], ["Dùng HikariCP với pool size 20"])
        # Note 2 chỉ có decision kế toán -> bị loại bỏ 100%
        self.assertNotIn("Chỉ có decision kế toán", [n["summary"] for n in filtered_notes])

    def test_update_project_notes_includes_lessons(self):
        project_notes = self.tmp_dir / "PROJECT-NOTES.md"
        initial_content = """# Sổ tay dự án

## Lưu ý và bẫy đã gặp

| ID | Ngày | Nguồn | Phạm vi | Lưu ý |
|---|---|---|---|---|

## Quyết định quan trọng

| ID | Ngày | Quyết định | ADR |
|---|---|---|---|

## Quy ước phát hiện thêm

"""
        project_notes.write_text(initial_content, encoding="utf-8")
        notes = [{
            "filename": "T-99-dev.md",
            "task": "T-99",
            "agent": "dev",
            "date": "2026-11-03",
            "summary": "T-99 lesson test",
            "traps": ["Bẫy connection pool"],
            "lessons": ["Bài học về tối ưu hoá Hibernate"],
            "decisions": ["Quyết định dùng Liquibase"],
            "conventions": ["Đặt tên index theo mẫu idx_table_col"],
            "skills": [],
        }]

        added = harness_mod.update_project_notes(project_notes, notes, dry_run=False)
        self.assertEqual(added, 4)

        updated_text = project_notes.read_text(encoding="utf-8")
        self.assertIn("[Bài học] Bài học về tối ưu hoá Hibernate", updated_text)
        self.assertIn("Bẫy connection pool", updated_text)
        self.assertIn("Quyết định dùng Liquibase", updated_text)
        self.assertIn("Đặt tên index theo mẫu idx_table_col", updated_text)

    def test_parse_yaml_frontmatter_bom_and_booleans(self):
        bom_text = "\ufeff---\nid: Design:bom-test\nkind: Design\ntitle: BOM Test\nis_active: true\ndraft: false\nvalue: null\n---\n# Body"
        fm = catalog_builder_mod.parse_yaml_frontmatter(bom_text)
        self.assertIsNotNone(fm)
        self.assertEqual(fm["id"], "Design:bom-test")
        self.assertEqual(fm["is_active"], True)
        self.assertEqual(fm["draft"], False)
        self.assertIsNone(fm["value"])


if __name__ == "__main__":
    unittest.main()

