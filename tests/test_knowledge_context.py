import hashlib
import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime, timezone

from agent_core.knowledge.catalog import load_catalog
# Module sẽ cài đặt
from agent_core.knowledge.context import (
    build_context,
    ContextRequest,
    ContextBundle,
)


class TestKnowledgeContextContract(unittest.TestCase):
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

    def _build_fixture_catalog(self):
        h_rule = self._create_sample_file("rules/git-rule.md", "Git rule: no force push.")
        h_spec = self._create_sample_file("spec/t-20.md", "T-20 Spec details for dev.")
        h_design = self._create_sample_file("design/ui.md", "Designer UI mockups.")
        h_draft = self._create_sample_file("drafts/idea.md", "Draft idea for next version.")

        nodes = [
            {
                "id": "Rule:git-rules",
                "kind": "Rule",
                "title": "Git Rules",
                "state": "approved",
                "version": 1,
                "content_ref": "rules/git-rule.md",
                "content_sha256": h_rule,
                "provenance": [],
                "owner_role": "architect",
                "relations": []
            },
            {
                "id": "Design:dev-spec",
                "kind": "Design",
                "title": "Dev Spec",
                "state": "approved",
                "version": 1,
                "content_ref": "spec/t-20.md",
                "content_sha256": h_spec,
                "provenance": [],
                "owner_role": "dev",
                "relations": []
            },
            {
                "id": "Design:ui-mockup",
                "kind": "Design",
                "title": "UI Mockup",
                "state": "approved",
                "version": 1,
                "content_ref": "design/ui.md",
                "content_sha256": h_design,
                "provenance": [],
                "owner_role": "designer",
                "relations": []
            },
            {
                "id": "Design:future-draft",
                "kind": "Design",
                "title": "Future Draft",
                "state": "draft",
                "version": 1,
                "content_ref": "drafts/idea.md",
                "content_sha256": h_draft,
                "provenance": [],
                "owner_role": "dev",
                "relations": []
            }
        ]
        data = {"schema_version": 1, "nodes": nodes}
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return load_catalog(self.tmp_dir)

    def test_role_filtering_and_mandatory_rule(self):
        catalog = self._build_fixture_catalog()
        req = ContextRequest(role="dev", as_of=datetime(2026, 10, 28, tzinfo=timezone.utc))
        bundle = build_context(catalog, req)

        included_ids = [n["id"] for n in bundle.nodes]
        # Rule bắt buộc cho mọi vai
        self.assertIn("Rule:git-rules", included_ids)
        # Node của vai dev được chọn
        self.assertIn("Design:dev-spec", included_ids)
        # Node của designer bị loại trừ
        self.assertNotIn("Design:ui-mockup", included_ids)
        # Draft mặc định không nằm trong main nodes
        self.assertNotIn("Design:future-draft", included_ids)

    def test_draft_appendix_with_include_draft(self):
        catalog = self._build_fixture_catalog()
        req = ContextRequest(role="dev", include_draft=True)
        bundle = build_context(catalog, req)

        included_ids = [n["id"] for n in bundle.nodes]
        appendix_ids = [n["id"] for n in bundle.appendix]
        self.assertNotIn("Design:future-draft", included_ids)
        self.assertIn("Design:future-draft", appendix_ids)

    def test_budget_omits_non_mandatory_nodes(self):
        catalog = self._build_fixture_catalog()
        # Đặt budget nhỏ chỉ vừa đủ cho Rule:git-rules nhưng không đủ cho Design:dev-spec
        # Rule byte size ~26 -> ceil(26/3) = 9 tokens.
        req = ContextRequest(role="dev", budget=12)
        bundle = build_context(catalog, req)

        included_ids = [n["id"] for n in bundle.nodes]
        self.assertIn("Rule:git-rules", included_ids)
        self.assertIn("Design:dev-spec", bundle.omitted_ids)

    def test_budget_mandatory_overflow_raises_error(self):
        catalog = self._build_fixture_catalog()
        # Budget = 2 quá nhỏ không chứa nổi mandatory rule
        req = ContextRequest(role="dev", budget=2)
        with self.assertRaises(ValueError) as ctx:
            build_context(catalog, req)
        self.assertIn("vượt ngân sách", str(ctx.exception))

    def test_cli_execution_and_exit_codes(self):
        import subprocess
        import sys

        catalog = self._build_fixture_catalog()

        # 1. validate hợp lệ -> exit 0
        cmd_val = [sys.executable, "scripts/knowledge.py", "validate", "--root", self.tmp_dir, "--format", "json"]
        res = subprocess.run(cmd_val, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0, f"validate failed: {res.stderr}")
        data = json.loads(res.stdout)
        self.assertTrue(data["valid"])

        # 2. context hợp lệ -> exit 0
        cmd_ctx = [
            sys.executable, "scripts/knowledge.py", "context",
            "--root", self.tmp_dir,
            "--role", "dev",
            "--budget", "500",
            "--format", "json"
        ]
        res = subprocess.run(cmd_ctx, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0, f"context failed: {res.stderr}")
        ctx_data = json.loads(res.stdout)
        self.assertEqual(ctx_data["role"], "dev")

        # 3. context vượt budget cho rule -> exit 1
        cmd_overflow = [
            sys.executable, "scripts/knowledge.py", "context",
            "--root", self.tmp_dir,
            "--role", "dev",
            "--budget", "2"
        ]
        res = subprocess.run(cmd_overflow, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 1)

        # 4. thiếu tham số bắt buộc --role -> exit 2
        cmd_bad = [sys.executable, "scripts/knowledge.py", "context", "--root", self.tmp_dir]
        res = subprocess.run(cmd_bad, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 2)


if __name__ == "__main__":
    unittest.main()
