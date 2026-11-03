"""tests/test_skill_graph.py

Kiểm thử toàn diện cho Đồ thị Kỹ năng (Skill Knowledge Graph) theo Phương án 1:
- Cấu hình cục bộ máy (local config priority & portable paths).
- Phân giải đường dẫn động (dynamic path resolution).
- Quét và xây dựng đồ thị (scanner & graph builder).
- Phát hiện độ lệch và cập nhật (drift detection & sync).
- Tra cứu JIT (role filtering, token budget).
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.knowledge.skill_graph import (
    load_skills_config,
    save_skills_local_config,
    check_forbidden_system_path,
    parse_frontmatter,
    classify_taxonomy_and_roles,
    select_primary_source,
    scan_quarantine_skills,
    save_skill_graph,
    load_skill_graph,
    resolve_skill_path,
    check_skill_graph_drift,
    search_skills,
)


class TestSkillGraph(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_forbidden_system_paths(self):
        """Kiểm tra chặn các đường dẫn nguy hiểm vào hệ thống."""
        is_bad, msg = check_forbidden_system_path(Path("/"))
        if sys.platform != "win32":
            self.assertTrue(is_bad)
            self.assertIn("CẤM", msg)

        is_bad_sys, _ = check_forbidden_system_path(Path("/System/Library"))
        if sys.platform != "win32":
            self.assertTrue(is_bad_sys)

        safe_path = self.temp_path / "safe-quarantine"
        safe_path.mkdir()
        is_bad_safe, _ = check_forbidden_system_path(safe_path)
        self.assertFalse(is_bad_safe)

    def test_local_config_priority(self):
        """Kiểm tra skills.config.local.json được ưu tiên cao hơn skills.config.json."""
        root = self.temp_path
        (root / ".agents" / "skills").mkdir(parents=True)

        local_dir = root / "local_repo"
        fallback_dir = root / "fallback_repo"
        local_dir.mkdir()
        fallback_dir.mkdir()

        # Tạo cả 2 file cấu hình
        fallback_cfg = root / "skills.config.json"
        fallback_cfg.write_text(json.dumps({"quarantine_dir": str(fallback_dir)}), encoding="utf-8")

        local_cfg = root / "skills.config.local.json"
        local_cfg.write_text(json.dumps({"quarantine_dir": str(local_dir)}), encoding="utf-8")

        q_dir, s_dir, chosen_cfg = load_skills_config(root)
        self.assertEqual(chosen_cfg.resolve(), local_cfg.resolve())
        self.assertEqual(q_dir.resolve(), local_dir.resolve())

    def test_parse_frontmatter(self):
        """Kiểm tra trích xuất metadata từ frontmatter YAML."""
        content = """---
name: my-test-skill
description: A great skill for testing
version: 1.2.0
triggers:
  - test this
  - run test
allowed-tools:
  - Bash
  - Read
---
# Content here
Details about skill.
"""
        fm, body = parse_frontmatter(content)
        self.assertEqual(fm["name"], "my-test-skill")
        self.assertEqual(fm["description"], "A great skill for testing")
        self.assertEqual(fm["version"], "1.2.0")
        self.assertEqual(fm["triggers"], ["test this", "run test"])
        self.assertEqual(fm["allowed_tools"], ["Bash", "Read"])
        self.assertIn("Details about skill", body)

    def test_no_absolute_paths_in_generated_graph(self):
        """Kiểm tra file graph JSON KHÔNG chứa đường dẫn tuyệt đối của máy (portable)."""
        graph_file = ROOT / "agents" / "knowledge" / "skill-graph.json"
        if not graph_file.exists():
            self.skipTest("skill-graph.json chưa được tạo")

        content = graph_file.read_text(encoding="utf-8")
        # Không được chứa username người dùng hiện tại
        import getpass
        current_user = getpass.getuser()
        self.assertNotIn(f"/Users/{current_user}", content)
        self.assertNotIn(f"C:\\Users\\{current_user}", content)

        # Kiểm tra mọi node có primary_source.rel_path là relative
        data = json.loads(content)
        for node in data.get("nodes", []):
            rel_p = node["primary_source"]["rel_path"]
            self.assertFalse(os.path.isabs(rel_p), f"Đường dẫn không được là absolute: {rel_p}")
            self.assertFalse(rel_p.startswith("/"), f"Đường dẫn không được bắt đầu bằng /: {rel_p}")

    def test_dynamic_path_resolution(self):
        """Kiểm tra phân giải đường dẫn động dựa trên quarantine_dir của từng máy."""
        mock_quarantine = self.temp_path / "mock_quarantine"
        skill_file = mock_quarantine / "repoA" / "skills" / "demo-skill" / "SKILL.md"
        skill_file.parent.mkdir(parents=True)
        skill_file.write_text("dummy skill", encoding="utf-8")

        node = {
            "name": "demo-skill",
            "primary_source": {
                "repo": "repoA",
                "rel_path": "repoA/skills/demo-skill/SKILL.md"
            }
        }

        # Trên máy A (temp_path)
        resolved = resolve_skill_path(node, quarantine_dir=mock_quarantine)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved, skill_file.resolve())

        # Trên máy B (đường dẫn khác)
        mock_quarantine_b = self.temp_path / "machine_b" / "quarantine"
        skill_file_b = mock_quarantine_b / "repoA" / "skills" / "demo-skill" / "SKILL.md"
        skill_file_b.parent.mkdir(parents=True)
        skill_file_b.write_text("dummy skill B", encoding="utf-8")

        resolved_b = resolve_skill_path(node, quarantine_dir=mock_quarantine_b)
        self.assertIsNotNone(resolved_b)
        self.assertEqual(resolved_b, skill_file_b.resolve())

    def test_scan_and_drift_detection(self):
        """Kiểm tra quét quarantine và phát hiện độ lệch khi có skill mới hoặc thay đổi."""
        quarantine = self.temp_path / "quarantine"
        repo = quarantine / "test-repo"
        repo.mkdir(parents=True)

        s1 = repo / "skills" / "skill-alpha" / "SKILL.md"
        s1.parent.mkdir(parents=True)
        s1.write_text("---\nname: skill-alpha\ndescription: Alpha skill for react dev\n---\n# Alpha", encoding="utf-8")

        s2 = repo / "skills" / "skill-beta" / "SKILL.md"
        s2.parent.mkdir(parents=True)
        s2.write_text("---\nname: skill-beta\ndescription: Beta skill for testing\n---\n# Beta", encoding="utf-8")

        # 1. Quét ban đầu
        graph = scan_quarantine_skills(quarantine, root_dir=self.temp_path)
        self.assertEqual(graph["stats"]["total_skills"], 2)
        self.assertEqual(graph["stats"]["total_variants"], 2)

        # Ban đầu: đồng bộ
        is_sync, drift = check_skill_graph_drift(graph, quarantine)
        self.assertTrue(is_sync)
        self.assertEqual(len(drift["added"]), 0)

        # 2. Thêm 1 skill mới vào thư mục
        s3 = repo / "skills" / "skill-gamma" / "SKILL.md"
        s3.parent.mkdir(parents=True)
        s3.write_text("---\nname: skill-gamma\ndescription: Gamma skill\n---\n# Gamma", encoding="utf-8")

        is_sync2, drift2 = check_skill_graph_drift(graph, quarantine)
        self.assertFalse(is_sync2)
        self.assertEqual(len(drift2["added"]), 1)
        self.assertIn("test-repo/skills/skill-gamma/SKILL.md", drift2["added"])

        # 3. Sửa đổi nội dung của skill-alpha
        s1.write_text("---\nname: skill-alpha\ndescription: Updated alpha description\n---\n# Alpha Modified", encoding="utf-8")
        is_sync3, drift3 = check_skill_graph_drift(graph, quarantine)
        self.assertFalse(is_sync3)
        self.assertEqual(len(drift3["modified"]), 1)

        # 4. Quét lại và cập nhật đồ thị -> trở lại đồng bộ
        new_graph = scan_quarantine_skills(quarantine, root_dir=self.temp_path)
        self.assertEqual(new_graph["stats"]["total_skills"], 3)
        is_sync4, _ = check_skill_graph_drift(new_graph, quarantine)
        self.assertTrue(is_sync4)

    def test_search_skills_with_role_and_budget(self):
        """Kiểm tra tra cứu JIT với phân quyền vai trò và ngân sách token."""
        graph_data = {
            "nodes": [
                {
                    "name": "react-patterns",
                    "domain": "development",
                    "roles": ["dev", "reviewer"],
                    "description": "Best practices for React and TypeScript components",
                    "triggers": ["react", "component"],
                    "estimated_tokens": 300,
                    "primary_source": {"rel_path": "repo/react/SKILL.md"}
                },
                {
                    "name": "k8s-deploy",
                    "domain": "devops",
                    "roles": ["devops", "sre"],
                    "description": "Kubernetes deployment automation and manifests",
                    "triggers": ["k8s", "deploy"],
                    "estimated_tokens": 400,
                    "primary_source": {"rel_path": "repo/k8s/SKILL.md"}
                }
            ]
        }

        # Query "react" với vai "dev" -> tìm thấy react-patterns
        hits = search_skills(graph_data, "react", role="dev")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["name"], "react-patterns")

        # Query "react" với vai "sre" -> bị chặn bởi RBAC
        hits_sre = search_skills(graph_data, "react", role="sre")
        self.assertEqual(len(hits_sre), 0)

        # Query "deploy" với vai "devops" -> tìm thấy k8s-deploy
        hits_devops = search_skills(graph_data, "deploy", role="devops")
        self.assertEqual(len(hits_devops), 1)
        self.assertEqual(hits_devops[0]["name"], "k8s-deploy")

    def test_cli_knowledge_query_skill(self):
        """Kiểm tra gọi lệnh CLI python scripts/knowledge.py query-skill."""
        cmd = [sys.executable, str(ROOT / "scripts" / "knowledge.py"), "query-skill", "-q", "subagent", "--format", "json"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertIsInstance(out, list)
        self.assertTrue(len(out) > 0)
        self.assertTrue(any("subagent" in item["name"].lower() for item in out))

    def test_save_skills_local_config(self):
        """Kiểm tra lưu cấu hình chỉ ghi vào skills.config.local.json và không chạm vào skills.config.json."""
        root = self.temp_path
        (root / ".agents" / "skills").mkdir(parents=True)
        fallback_cfg = root / "skills.config.json"
        fallback_cfg.write_text(json.dumps({"quarantine_dir": "~/skills-quarantine"}), encoding="utf-8")

        mock_q = self.temp_path / "custom_quarantine"
        mock_q.mkdir()

        saved_path = save_skills_local_config(mock_q, root_dir=root)
        self.assertEqual(saved_path.resolve(), (root / "skills.config.local.json").resolve())
        self.assertTrue(saved_path.exists())

        # Kiểm tra nội dung local config
        local_data = json.loads(saved_path.read_text(encoding="utf-8"))
        self.assertEqual(local_data["quarantine_dir"], str(mock_q.resolve()).replace("\\", "/"))

        # skills.config.json không bị biến đổi
        fallback_data = json.loads(fallback_cfg.read_text(encoding="utf-8"))
        self.assertEqual(fallback_data["quarantine_dir"], "~/skills-quarantine")

    def test_dynamic_path_resolution_polymorphism(self):
        """Kiểm tra resolve_skill_path hỗ trợ đa hình: dict, variant, chuỗi str hoặc Path."""
        mock_q = self.temp_path / "mock_q"
        target = mock_q / "ECC" / "skills" / "foo" / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("hello", encoding="utf-8")

        # 1. Truyền node dict
        node = {"name": "foo", "primary_source": {"rel_path": "ECC/skills/foo/SKILL.md"}}
        p1 = resolve_skill_path(node, quarantine_dir=mock_q)
        self.assertEqual(p1, target.resolve())

        # 2. Truyền variant dict
        variant = {"rel_path": "ECC/skills/foo/SKILL.md"}
        p2 = resolve_skill_path(variant, quarantine_dir=mock_q)
        self.assertEqual(p2, target.resolve())

        # 3. Truyền chuỗi relative path (có hoặc không có leading slash)
        p3 = resolve_skill_path("ECC/skills/foo/SKILL.md", quarantine_dir=mock_q)
        p4 = resolve_skill_path("/ECC/skills/foo/SKILL.md", quarantine_dir=mock_q)
        self.assertEqual(p3, target.resolve())
        self.assertEqual(p4, target.resolve())

        # 4. Truyền đối tượng Path
        p5 = resolve_skill_path(Path("ECC/skills/foo/SKILL.md"), quarantine_dir=mock_q)
        self.assertEqual(p5, target.resolve())

    def test_search_skills_token_boundary_precision(self):
        """Kiểm tra từ khóa ngắn (như 'ba', 'qa') khớp chính xác token thay vì chuỗi con (tránh 'database' -> 'ba')."""
        graph_data = {
            "nodes": [
                {
                    "name": "database-tuning",
                    "domain": "development",
                    "roles": ["dev"],
                    "description": "PostgreSQL database indexing and query tuning",
                    "triggers": ["sql"],
                    "primary_source": {"rel_path": "repo/db/SKILL.md"}
                },
                {
                    "name": "ba-spec-writing",
                    "domain": "business",
                    "roles": ["ba"],
                    "description": "BABOK business analysis and SRS specification writing",
                    "triggers": ["ba", "srs"],
                    "primary_source": {"rel_path": "repo/ba/SKILL.md"}
                }
            ]
        }
        # Tìm 'ba': chỉ được khớp ba-spec-writing, không được dính database-tuning
        res = search_skills(graph_data, "ba", role="ba")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["name"], "ba-spec-writing")

    def test_cli_skill_graph_actions(self):
        """Kiểm tra các hành động CLI status, check, sync trong knowledge.py."""
        # Status
        cmd_status = [sys.executable, str(ROOT / "scripts" / "knowledge.py"), "skill-graph", "status"]
        res_s = subprocess.run(cmd_status, capture_output=True, text=True)
        self.assertEqual(res_s.returncode, 0, res_s.stderr)
        self.assertIn("TRẠNG THÁI ĐỒ THỊ KỸ NĂNG", res_s.stdout)

        # Sync / Update
        cmd_sync = [sys.executable, str(ROOT / "scripts" / "knowledge.py"), "skill-graph", "sync"]
        res_sync = subprocess.run(cmd_sync, capture_output=True, text=True)
        self.assertEqual(res_sync.returncode, 0, res_sync.stderr)

    def test_auto_update_on_missing_skill(self):
        """Kiểm tra cơ chế tự phát hiện và đồng bộ khi query skill mới được thêm vào quarantine."""
        mock_root = self.temp_path / "agent_base_mock"
        mock_root.mkdir()
        (mock_root / "agents" / "knowledge").mkdir(parents=True)
        (mock_root / ".agents" / "skills").mkdir(parents=True)

        mock_quarantine = self.temp_path / "mock_quarantine"
        mock_repo = mock_quarantine / "repo1"
        mock_repo.mkdir(parents=True)

        # 1. Ban đầu có skill A
        s_a = mock_repo / "skills" / "skill-a" / "SKILL.md"
        s_a.parent.mkdir(parents=True)
        s_a.write_text("---\nname: skill-a\ndescription: Skill A\n---\n# A", encoding="utf-8")

        save_skills_local_config(mock_quarantine, root_dir=mock_root)
        graph_data = scan_quarantine_skills(mock_quarantine, root_dir=mock_root)
        graph_file = mock_root / "agents" / "knowledge" / "skill-graph.json"
        save_skill_graph(graph_data, graph_file)

        # 2. Thêm skill-new vào quarantine mà chưa cập nhật đồ thị
        s_new = mock_repo / "skills" / "skill-new" / "SKILL.md"
        s_new.parent.mkdir(parents=True)
        s_new.write_text("---\nname: skill-new\ndescription: A brand new skill just downloaded\n---\n# New", encoding="utf-8")

        # 3. Gọi CLI query-skill tìm 'skill-new'
        cmd = [
            sys.executable, str(ROOT / "scripts" / "knowledge.py"), "query-skill",
            "-q", "skill-new", "--root", str(mock_root), "--format", "json"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["name"], "skill-new")


if __name__ == "__main__":
    unittest.main()

