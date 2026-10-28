"""Kiểm thử tính hợp lệ của bản phân phối manifest.txt và CI check.yml.
Đáp ứng yêu cầu T-28.2 (Contract & Happy Path).
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestDistribution(unittest.TestCase):
    def test_manifest_entries_and_ordering(self):
        manifest_path = ROOT / "agents" / "manifest.txt"
        self.assertTrue(manifest_path.exists())

        lines = [line.strip() for line in manifest_path.read_text(encoding="utf-8").splitlines()]
        entries = []
        for line in lines:
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                entries.append((parts[0], parts[1]))

        # Kiểm tra sự xuất hiện của các thư mục lõi
        copied_paths = [path for kind, path in entries if kind == "copy"]
        self.assertIn("agent_core/", copied_paths)
        self.assertIn("scripts/", copied_paths)
        self.assertIn("schemas/", copied_paths)
        self.assertIn("examples/", copied_paths)

        # Kiểm tra quy tắc ưu tiên: template knowledge-manifest.json phải đứng trước copy agents/
        template_idx = None
        copy_agents_idx = None
        for i, (kind, path) in enumerate(entries):
            if kind == "template" and "knowledge-manifest.json" in path:
                template_idx = i
            elif kind == "copy" and path == "agents/":
                copy_agents_idx = i

        self.assertIsNotNone(template_idx, "knowledge-manifest.json phải được khai báo dạng template")
        self.assertIsNotNone(copy_agents_idx, "agents/ phải được khai báo dạng copy")
        self.assertLess(template_idx, copy_agents_idx, "template phải đứng trước copy agents/ để thắng độ ưu tiên")

    def test_ci_workflow_valid_yaml_and_has_new_steps(self):
        ci_path = ROOT / ".github" / "workflows" / "check.yml"
        self.assertTrue(ci_path.exists())

        import yaml
        content = ci_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        self.assertIn("jobs", data)
        self.assertIn("agent-base", data["jobs"])
        steps = data["jobs"]["agent-base"].get("steps", [])

        step_names = [s.get("name") for s in steps if isinstance(s, dict)]
        self.assertIn("Validate Knowledge Catalog", step_names)
        self.assertIn("Check Requirements Traceability Matrix (RTM)", step_names)


if __name__ == "__main__":
    unittest.main()
