"""Kiểm tra nhất quán giữa khai báo (vai trò, protocol) và tri thức: mỗi chủ đề một nơi chuẩn, tri thức chỉ là tham khảo."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARD_STATUSES = {"todo", "doing", "review", "done", "blocked"}
LABEL = "**Loại: tham khảo.**"


def _md_files(*parts):
    base = ROOT.joinpath(*parts)
    return sorted(p for p in base.glob("*.md") if p.name != "README.md")


class TestKnowledgeIsReference(unittest.TestCase):
    def test_knowledge_files_are_labeled_reference(self):
        """Tri thức không đặt luật: mỗi file quy-trinh, ky-thuat, srs có nhãn 'tham khảo' ở đầu."""
        missing = []
        for sub in ("quy-trinh", "ky-thuat", "srs", "diagrams"):
            for p in _md_files("agents", "knowledge", sub):
                head = "\n".join(p.read_text(encoding="utf-8").split("\n")[:6])
                if LABEL not in head:
                    missing.append(str(p.relative_to(ROOT)))
        self.assertEqual(missing, [], f"Thiếu nhãn tham khảo ở đầu file: {missing}")

    def test_every_knowledge_file_is_in_the_index(self):
        readme = (ROOT / "agents" / "knowledge" / "README.md").read_text(encoding="utf-8")
        missing = []
        for sub in ("quy-trinh", "ky-thuat", "srs", "diagrams"):
            for p in _md_files("agents", "knowledge", sub):
                if f"{sub}/{p.name}" not in readme:
                    missing.append(f"{sub}/{p.name}")
        self.assertEqual(missing, [], f"File tri thức chưa có trong agents/knowledge/README.md: {missing}")


class TestKnowledgeGraphCoverage(unittest.TestCase):
    def test_every_standard_and_knowledge_file_has_a_node(self):
        """Mọi file tri thức và protocol chuẩn phải có nút trong knowledge-manifest.json (sinh bằng build-knowledge-catalog.py)."""
        import json
        manifest = json.loads((ROOT / "agents" / "knowledge" / "knowledge-manifest.json").read_text(encoding="utf-8"))
        refs = {n["content_ref"] for n in manifest["nodes"]}
        required = [f"agents/protocols/{n}.md" for n in (
            "task-loop", "definition-of-done", "git-rules", "change-request", "ai-provenance",
            "plan-critique", "pair-review", "release-note", "lesson-learned", "ticket-status")]
        for sub in ("quy-trinh", "ky-thuat", "srs", "diagrams"):
            required += [f"agents/knowledge/{sub}/{p.name}" for p in _md_files("agents", "knowledge", sub)]
        missing = [r for r in required if r not in refs]
        self.assertEqual(missing, [], f"Chưa có nút trong catalog (chạy scripts/build-knowledge-catalog.py): {missing}")

    def test_only_core_rules_are_mandatory_for_every_role(self):
        """Rule bị nạp cho MỌI vai khi approved; giữ ít để không tăng ngữ cảnh."""
        import json
        manifest = json.loads((ROOT / "agents" / "knowledge" / "knowledge-manifest.json").read_text(encoding="utf-8"))
        rules = sorted(n["id"] for n in manifest["nodes"] if n["kind"] == "Rule")
        self.assertLessEqual(len(rules), 3, f"Quá nhiều Rule bắt buộc: {rules}")


class TestStatusesAndGit(unittest.TestCase):
    def test_ticket_status_maps_only_to_card_statuses(self):
        text = (ROOT / "agents" / "protocols" / "ticket-status.md").read_text(encoding="utf-8")
        used = set()
        for line in text.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if line.startswith("|") and len(cells) >= 2 and re.fullmatch(r"`[a-z]+`", cells[1]):
                used.add(cells[1].strip("`"))
        self.assertTrue(used, "Không đọc được bảng ánh xạ trạng thái")
        self.assertTrue(used <= CARD_STATUSES, f"Trạng thái ngoài danh sách của card: {used - CARD_STATUSES}")

    def test_roles_do_not_ban_reversible_git_commands(self):
        """AGENTS.md mục 4 cho phép lệnh git hoàn tác được; vai trò không được tự cấm lại."""
        loosened = ("pull", "fetch", "merge", "rebase", "checkout", "switch", "stash")
        ban = re.compile(r"(không|cấm)[^\n]*`(" + "|".join(loosened) + r")`", re.I)
        offenders = []
        for p in sorted((ROOT / "agents" / "roles").glob("*.md")):
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if ban.search(line):
                    offenders.append(f"{p.name}:{n}")
        self.assertEqual(offenders, [], f"Vai trò còn cấm lệnh git đã được phép: {offenders}")


class TestLowFrictionRules(unittest.TestCase):
    def test_agents_md_fits_antigravity_limit(self):
        n = len((ROOT / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertLessEqual(n, 20000, f"AGENTS.md dài {n} ký tự, vượt giới hạn an toàn")

    def test_refresh_check_passes(self):
        """Một lệnh kiểm cả bốn file sinh tự động mà CI yêu cầu (adapter, catalog, task board, notes index)."""
        import subprocess
        import sys
        r = subprocess.run([sys.executable, "scripts/refresh.py", "--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, (r.stdout or "") + (r.stderr or ""))

    def test_chat_consent_is_valid_and_recorded(self):
        text = (ROOT / "agents" / "protocols" / "approval.md").read_text(encoding="utf-8")
        self.assertIn("AI ghi hộ", text)
        self.assertIn("trích nguyên văn", text)

    def test_no_role_or_protocol_forces_empty_handoff_notes(self):
        offenders = []
        for p in list((ROOT / "agents" / "roles").glob("*.md")) + list((ROOT / "agents" / "protocols").glob("*.md")):
            if 'dù chỉ ghi "không có lưu ý"' in p.read_text(encoding="utf-8"):
                offenders.append(p.name)
        self.assertEqual(offenders, [], f"Còn bắt ghi chú bàn giao rỗng: {offenders}")


if __name__ == "__main__":
    unittest.main()
