import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
import hashlib

# Sẽ import từ agent_core.knowledge.catalog
# Ban đầu chưa có file sẽ FAIL
from agent_core.knowledge.catalog import (
    load_catalog,
    validate_catalog,
    Catalog,
    Node,
    Diagnostic,
    DIAGNOSTIC_CODES,
)


class TestKnowledgeCatalogContract(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.catalog_path = os.path.join(self.tmp_dir, "knowledge.manifest.json")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def _create_sample_file(self, rel_path: str, content: str) -> str:
        abs_path = os.path.join(self.tmp_dir, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def test_v00_malformed_catalog_schema(self):
        # Thiếu schema_version hoặc trường bắt buộc
        data = {"nodes": []}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V00" for d in diags))

    def test_v01_duplicate_node_id(self):
        h = self._create_sample_file("docs/doc1.md", "Content 1")
        node1 = {
            "id": "Design:arch-overview",
            "kind": "Design",
            "title": "Arch Overview",
            "state": "draft",
            "version": 1,
            "content_ref": "docs/doc1.md",
            "content_sha256": h,
            "provenance": ["Source:upstream"],
            "owner_role": "architect",
            "relations": []
        }
        node2 = dict(node1) # trùng ID
        data = {"schema_version": 1, "nodes": [node1, node2]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V01" for d in diags))

    def test_v02_invalid_node_id_format(self):
        h = self._create_sample_file("docs/doc1.md", "Content 1")
        node = {
            "id": "invalid_id_format",
            "kind": "Design",
            "title": "Invalid ID",
            "state": "draft",
            "version": 1,
            "content_ref": "docs/doc1.md",
            "content_sha256": h,
            "provenance": [],
            "owner_role": "architect",
            "relations": []
        }
        data = {"schema_version": 1, "nodes": [node]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V02" for d in diags))

    def test_v03_path_escape_content_ref(self):
        node = {
            "id": "Design:escape",
            "kind": "Design",
            "title": "Escape",
            "state": "draft",
            "version": 1,
            "content_ref": "../secret.txt",
            "content_sha256": "abc",
            "provenance": [],
            "owner_role": "architect",
            "relations": []
        }
        data = {"schema_version": 1, "nodes": [node]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V03" for d in diags))

    def test_v04_missing_content_file(self):
        node = {
            "id": "Design:missing",
            "kind": "Design",
            "title": "Missing File",
            "state": "draft",
            "version": 1,
            "content_ref": "docs/nonexistent.md",
            "content_sha256": "abc",
            "provenance": [],
            "owner_role": "architect",
            "relations": []
        }
        data = {"schema_version": 1, "nodes": [node]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V04" for d in diags))

    def test_v05_content_hash_mismatch(self):
        h = self._create_sample_file("docs/doc1.md", "Content 1")
        node = {
            "id": "Design:mismatch",
            "kind": "Design",
            "title": "Hash Mismatch",
            "state": "draft",
            "version": 1,
            "content_ref": "docs/doc1.md",
            "content_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
            "provenance": [],
            "owner_role": "architect",
            "relations": []
        }
        data = {"schema_version": 1, "nodes": [node]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V05" for d in diags))

    def test_v06_dangling_relation(self):
        h = self._create_sample_file("docs/doc1.md", "Content 1")
        node = {
            "id": "Task:T-1",
            "kind": "Task",
            "title": "Task 1",
            "state": "draft",
            "version": 1,
            "content_ref": "docs/doc1.md",
            "content_sha256": h,
            "provenance": [],
            "owner_role": "dev",
            "relations": [
                {"type": "depends_on", "target": "Task:T-nonexistent"}
            ]
        }
        data = {"schema_version": 1, "nodes": [node]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V06" for d in diags))

    def test_v07_invalid_relation_type_or_endpoint(self):
        h = self._create_sample_file("docs/doc1.md", "Content 1")
        h2 = self._create_sample_file("docs/doc2.md", "Content 2")
        # depends_on chỉ giữa Task -> Task
        node1 = {
            "id": "Design:arch",
            "kind": "Design",
            "title": "Design 1",
            "state": "draft",
            "version": 1,
            "content_ref": "docs/doc1.md",
            "content_sha256": h,
            "provenance": [],
            "owner_role": "architect",
            "relations": [
                {"type": "depends_on", "target": "Requirement:R-1"}
            ]
        }
        node2 = {
            "id": "Requirement:R-1",
            "kind": "Requirement",
            "title": "Req 1",
            "state": "draft",
            "version": 1,
            "content_ref": "docs/doc2.md",
            "content_sha256": h2,
            "provenance": [],
            "owner_role": "ba",
            "relations": []
        }
        data = {"schema_version": 1, "nodes": [node1, node2]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V07" for d in diags))

    def test_v08_self_edge(self):
        h = self._create_sample_file("docs/doc1.md", "Content 1")
        node = {
            "id": "Task:T-self",
            "kind": "Task",
            "title": "Task Self",
            "state": "draft",
            "version": 1,
            "content_ref": "docs/doc1.md",
            "content_sha256": h,
            "provenance": [],
            "owner_role": "dev",
            "relations": [
                {"type": "depends_on", "target": "Task:T-self"}
            ]
        }
        data = {"schema_version": 1, "nodes": [node]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V08" for d in diags))

    def test_v09_cycle_detection(self):
        h1 = self._create_sample_file("docs/t1.md", "T1")
        h2 = self._create_sample_file("docs/t2.md", "T2")
        h3 = self._create_sample_file("docs/t3.md", "T3")
        # Chu trình: T-1 -> T-2 -> T-3 -> T-1
        node1 = {
            "id": "Task:T-1", "kind": "Task", "title": "T1", "state": "draft", "version": 1,
            "content_ref": "docs/t1.md", "content_sha256": h1, "provenance": [], "owner_role": "dev",
            "relations": [{"type": "depends_on", "target": "Task:T-2"}]
        }
        node2 = {
            "id": "Task:T-2", "kind": "Task", "title": "T2", "state": "draft", "version": 1,
            "content_ref": "docs/t2.md", "content_sha256": h2, "provenance": [], "owner_role": "dev",
            "relations": [{"type": "depends_on", "target": "Task:T-3"}]
        }
        node3 = {
            "id": "Task:T-3", "kind": "Task", "title": "T3", "state": "draft", "version": 1,
            "content_ref": "docs/t3.md", "content_sha256": h3, "provenance": [], "owner_role": "dev",
            "relations": [{"type": "depends_on", "target": "Task:T-1"}]
        }
        data = {"schema_version": 1, "nodes": [node1, node2, node3]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        diags = validate_catalog(catalog)
        self.assertTrue(any(d.code == "V09" for d in diags))

    def test_v10_stale_and_invalid_state_transitions(self):
        h = self._create_sample_file("docs/doc1.md", "Content 1")
        # review_due_at đã quá hạn so với as_of
        node = {
            "id": "Requirement:R-expired",
            "kind": "Requirement",
            "title": "Expired Req",
            "state": "approved",
            "version": 1,
            "content_ref": "docs/doc1.md",
            "content_sha256": h,
            "provenance": [],
            "owner_role": "ba",
            "review_due_at": "2026-01-01T00:00:00Z",
            "relations": []
        }
        data = {"schema_version": 1, "nodes": [node]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        # as_of là 2026-10-28 -> đã quá hạn -> phải báo V10 (stale)
        as_of = datetime(2026, 10, 28, tzinfo=timezone.utc)
        diags = validate_catalog(catalog, as_of=as_of)
        self.assertTrue(any(d.code == "V10" for d in diags))

    def test_happy_path_valid_catalog(self):
        h_src = self._create_sample_file("sources/upstream.md", "Source Upstream")
        h_req = self._create_sample_file("docs/requirements/R-1.md", "Req 1")
        h_task = self._create_sample_file("tasks/T-1.md", "Task 1")

        nodes = [
            {
                "id": "Source:upstream",
                "kind": "Source",
                "title": "Upstream",
                "state": "approved",
                "version": 1,
                "content_ref": "sources/upstream.md",
                "content_sha256": h_src,
                "provenance": [],
                "owner_role": "architect",
                "relations": []
            },
            {
                "id": "Requirement:R-1",
                "kind": "Requirement",
                "title": "Req 1",
                "state": "approved",
                "version": 1,
                "content_ref": "docs/requirements/R-1.md",
                "content_sha256": h_req,
                "provenance": ["Source:upstream"],
                "owner_role": "ba",
                "relations": [
                    {"type": "derived_from", "target": "Source:upstream"}
                ]
            },
            {
                "id": "Task:T-1",
                "kind": "Task",
                "title": "Task 1",
                "state": "draft",
                "version": 1,
                "content_ref": "tasks/T-1.md",
                "content_sha256": h_task,
                "provenance": [],
                "owner_role": "dev",
                "relations": [
                    {"type": "implements", "target": "Requirement:R-1"}
                ]
            }
        ]
        data = {"schema_version": 1, "nodes": [nodes[0], nodes[1], nodes[2]]}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        catalog = load_catalog(self.tmp_dir)
        as_of = datetime(2026, 10, 28, tzinfo=timezone.utc)
        diags = validate_catalog(catalog, as_of=as_of)
        self.assertEqual(len(diags), 0, f"Expected 0 diagnostics, got: {[d.to_dict() for d in diags]}")


if __name__ == "__main__":
    unittest.main()
