"""Kiểm thử đồ thị tri thức: phủ đủ file, có cạnh liên quan, và tra cứu theo tình huống thật ra đúng nút."""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def manifest():
    return json.loads((ROOT / "agents" / "knowledge" / "knowledge-manifest.json").read_text(encoding="utf-8"))


def query(q, *args):
    r = subprocess.run([sys.executable, "scripts/knowledge.py", "query", "-q", q, "--format", "json", *args],
                       cwd=ROOT, capture_output=True, text=True)
    return json.loads(r.stdout) if r.stdout.strip().startswith("[") else []


class TestGraphCoverage(unittest.TestCase):
    def test_every_protocol_knowledge_doc_and_skill_has_a_node(self):
        refs = {n["content_ref"] for n in manifest()["nodes"]}
        wanted = [p.relative_to(ROOT).as_posix() for p in (ROOT / "agents" / "protocols").glob("*.md")]
        wanted += [p.relative_to(ROOT).as_posix() for p in (ROOT / "agents" / "knowledge").rglob("*.md")
                   if p.name != "README.md" and "review-rules" not in p.parts]
        wanted += [p.relative_to(ROOT).as_posix() for p in (ROOT / ".agents" / "skills").glob("*/SKILL.md")]
        missing = [w for w in wanted if w not in refs]
        self.assertEqual(missing, [], f"Chưa có nút (chạy scripts/refresh.py): {missing}")

    def test_every_content_node_has_a_related_edge(self):
        nodes = manifest()["nodes"]
        linked = set()
        for n in nodes:
            for r in n["relations"]:
                if r["type"] == "related_to":
                    linked.update([n["id"], r["target"]])
        alone = [n["id"] for n in nodes if n["kind"] != "Role" and n["id"] not in linked]
        self.assertEqual(alone, [], f"Nút chưa nối cạnh liên quan nào: {alone}")

    def test_all_new_nodes_stay_draft_in_the_shipped_manifest(self):
        self.assertEqual({n["state"] for n in manifest()["nodes"]}, {"draft"})

    def test_every_skill_node_has_a_role_owner(self):
        for n in manifest()["nodes"]:
            if n["kind"] == "Skill":
                self.assertTrue(any(r["type"] == "owned_by" for r in n["relations"]), n["id"])


# Tình huống thật -> các nút chấp nhận được trong 3 kết quả đầu. Không ghi cứng một nút để khỏi gò theo dữ liệu.
GOLDEN = [
    ("viết câu sql chậm", {"Design:sql-postgresql-and-jpa-hibernate", "Design:chuan-sql-va-loi"}),
    ("jpa n+1", {"Design:sql-postgresql-and-jpa-hibernate", "Skill:jpa-patterns"}),
    ("đổi schema không dừng hệ thống", {"Design:zero-downtime-migrations"}),
    ("vẽ sơ đồ hoạt động", {"Design:diagram-mo-ta-hoat-dong-so-do", "Design:chuan-ve-so-do", "Design:diagram-quy-uoc-draw-io-va-archify"}),
    ("mô tả sơ đồ", {"Design:diagram-mo-ta-hoat-dong-so-do"}),
    ("review code checklist", {"Design:chuan-code-va-review"}),
    ("tdd spring boot", {"Skill:springboot-tdd", "Design:tdd-13-steps"}),
    ("thay đổi yêu cầu ccb", {"Requirement:change-request", "Requirement:baccm-and-cr"}),
    ("git commit nhánh", {"Design:git-rules"}),
    ("bài học retro", {"Requirement:lesson-learned", "Skill:retro"}),
    ("release note", {"Requirement:release-note"}),
    ("redis khóa phân tán", {"Design:redis-patterns-and-enterprise-architecture"}),
    ("kubernetes", {"Design:kubernetes-architecture-and-manifests"}),
    ("bảo mật audit", {"Design:cso-security", "Skill:security-scan"}),
    ("prompt registry", {"Design:prompt-as-code-registry", "Requirement:ai-provenance"}),
    ("bug hàng loạt", {"Design:bug-handling-pipeline"}),
    ("srs đặc tả", {"Requirement:srs-writing-standard"}),
    ("phản biện kế hoạch trước khi code", {"Requirement:plan-critique"}),
    ("trạng thái ticket", {"Requirement:ticket-status"}),
    ("wayfinder", {"Skill:wayfinder"}),
]


class TestGoldenQueries(unittest.TestCase):
    def test_realistic_tasks_find_the_right_node_in_top_three(self):
        failures = []
        for q, expected in GOLDEN:
            top = {h["id"] for h in query(q)}
            if not top & expected:
                failures.append((q, sorted(top)))
        self.assertEqual(failures, [], f"Tra cứu trượt: {failures}")

    def test_hits_pull_in_related_nodes_through_edges(self):
        hits = query("viết câu sql chậm")
        related = {r["id"] for r in hits[0].get("related", [])}
        self.assertTrue(related & {"Skill:postgres-patterns", "Skill:jpa-patterns", "Design:zero-downtime-migrations"},
                        f"Không kéo được nút liên quan: {related}")

    def test_query_logs_usage_locally(self):
        # Dùng từ khóa riêng để không lẫn với lần tra của tiến trình khác chạy cùng lúc.
        marker = "kubernetes-nhat-ky-kiem-thu"
        query(marker)
        log = ROOT / ".local" / "knowledge-usage.jsonl"
        entries = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertTrue(any(e.get("q") == marker for e in entries))


def _run_set(filename):
    cases = json.loads((ROOT / "tests" / filename).read_text(encoding="utf-8"))
    failures = []
    for q, expected in cases:
        top = {h["id"] for h in query(q)}
        if not top & set(expected):
            failures.append((q, sorted(top)))
    return len(cases), failures


class TestOffScriptQueries(unittest.TestCase):
    def test_offscript_queries_all_found(self):
        total, failures = _run_set("knowledge_offscript_queries.json")
        self.assertEqual(failures, [], f"Trượt {len(failures)}/{total}: {failures}")

    def test_fresh_queries_mostly_found(self):
        """Bộ này đã được dùng để chỉnh thuật toán nên chỉ là chỉ báo; đòi tối thiểu 80%."""
        total, failures = _run_set("knowledge_fresh_queries.json")
        self.assertGreaterEqual(total - len(failures), int(total * 0.8), f"Trượt: {failures}")


if __name__ == "__main__":
    unittest.main()
