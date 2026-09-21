"""
tests/test_merge_gate.py
Bộ kiểm thử toàn diện 14 kịch bản cho merge-gate (kiểm soát phạm vi tác vụ scope_edit/scope_deny).
"""

import sys
import unittest
from pathlib import Path

# Thêm scripts/ vào sys.path để import trực tiếp merge-gate
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import importlib.util
spec = importlib.util.spec_from_file_location("merge_gate", str(ROOT / "scripts" / "merge-gate.py"))
merge_gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(merge_gate)


class TestMergeGateScenarios(unittest.TestCase):
    """14 kịch bản kiểm thử quy tắc phân quyền tệp của merge-gate."""

    def test_01_clean_changes_strictly_inside_scope(self):
        """Kịch bản 1: Tất cả thay đổi nằm hoàn toàn trong scope_edit -> PASS."""
        allow = ["agent_core/eval/**", "tests/**"]
        deny = ["scripts/**", ".github/**"]
        files = ["agent_core/eval/code_reviewer.py", "tests/test_code_reviewer.py"]
        violations = merge_gate.check_files_in_scope(files, allow, deny)
        self.assertEqual(len(violations), 0)

    def test_02_file_outside_scope_edit(self):
        """Kịch bản 2: Nhánh sửa file nằm ngoài phạm vi scope_edit -> FAIL (OUT OF SCOPE)."""
        allow = ["agent_core/eval/**"]
        deny = ["scripts/**"]
        files = ["agent_core/core/sandbox.py"]
        violations = merge_gate.check_files_in_scope(files, allow, deny)
        self.assertEqual(len(violations), 1)
        self.assertIn("OUT OF SCOPE", violations[0])
        self.assertIn("agent_core/core/sandbox.py", violations[0])

    def test_03_file_inside_scope_deny(self):
        """Kịch bản 3: Nhánh sửa file nằm trong danh sách cấm scope_deny -> FAIL (DENIED)."""
        allow = ["**"]
        deny = [".github/workflows/**", "scripts/merge-gate.py"]
        files = ["scripts/merge-gate.py"]
        violations = merge_gate.check_files_in_scope(files, allow, deny)
        self.assertEqual(len(violations), 1)
        self.assertIn("DENIED", violations[0])

    def test_04_tampered_scope_edit_detected(self):
        """Kịch bản 4: Nhánh cố tình tự mở rộng scope_edit trong task card -> Phát hiện sai khác."""
        base_card = "---\nid: T-01\nscope_edit:\n  - tests/**\n---\n# Task 01"
        branch_card = "---\nid: T-01\nscope_edit:\n  - tests/**\n  - agent_core/**\n---\n# Task 01"
        _, base_allow, _ = merge_gate.parse_card_frontmatter(base_card)
        _, branch_allow, _ = merge_gate.parse_card_frontmatter(branch_card)
        self.assertNotEqual(base_allow, branch_allow)
        self.assertEqual(base_allow, ["tests/**"])
        self.assertEqual(branch_allow, ["tests/**", "agent_core/**"])

    def test_05_tampered_scope_deny_detected(self):
        """Kịch bản 5: Nhánh cố tình thu hẹp scope_deny trong task card -> Phát hiện sai khác."""
        base_card = "---\nid: T-01\nscope_edit:\n  - tests/**\nscope_deny:\n  - scripts/**\n---\n# Task 01"
        branch_card = "---\nid: T-01\nscope_edit:\n  - tests/**\nscope_deny: []\n---\n# Task 01"
        _, _, base_deny = merge_gate.parse_card_frontmatter(base_card)
        _, _, branch_deny = merge_gate.parse_card_frontmatter(branch_card)
        self.assertNotEqual(base_deny, branch_deny)
        self.assertEqual(base_deny, ["scripts/**"])
        self.assertEqual(branch_deny, [])

    def test_06_yaml_comments_on_scope_lines_stripped(self):
        """Kịch bản 6: Chú thích YAML sau dấu # được loại bỏ, không làm lệch scope."""
        card_with_comments = (
            "---\n"
            "id: T-01\n"
            "scope_edit:\n"
            "  - tests/** # ghi chú cho reviewer\n"
            "  - agent_core/eval/** # module đánh giá\n"
            "scope_deny:\n"
            "  - scripts/** # cấm sửa scripts trực tiếp\n"
            "---\n"
        )
        task_id, allow, deny = merge_gate.parse_card_frontmatter(card_with_comments)
        self.assertEqual(task_id, "T-01")
        self.assertEqual(allow, ["tests/**", "agent_core/eval/**"])
        self.assertEqual(deny, ["scripts/**"])

    def test_07_complex_yaml_comments_with_special_chars(self):
        """Kịch bản 7: Chú thích phức tạp có dấu ngoặc và ký tự đặc biệt được bóc tách sạch sẽ."""
        card_text = (
            "---\n"
            "id: T-02\n"
            "scope_edit:\n"
            '  - "agent_core/core/**" # [CRITICAL] Core modules (read/write)\n'
            "  - 'docs/notes/**'      # Ghi chú: path/to/somewhere\n"
            "---\n"
        )
        _, allow, _ = merge_gate.parse_card_frontmatter(card_text)
        self.assertEqual(allow, ["agent_core/core/**", "docs/notes/**"])

    def test_08_empty_scope_edit_detected(self):
        """Kịch bản 8: Thẻ công việc không khai báo scope_edit -> danh sách rỗng."""
        empty_card = "---\nid: T-EMPTY\n---\n# Empty scope card"
        _, allow, _ = merge_gate.parse_card_frontmatter(empty_card)
        self.assertEqual(allow, [])

    def test_09_multiple_files_within_scope(self):
        """Kịch bản 9: Nhiều tệp thay đổi đồng thời đều hợp lệ -> PASS."""
        allow = ["agent_core/**", "tests/**", "docs/**"]
        deny = ["scripts/**"]
        files = [
            "agent_core/eval/cso_scanner.py",
            "agent_core/eval/code_reviewer.py",
            "tests/test_cso_scanner.py",
            "tests/test_code_reviewer.py",
            "docs/notes/inbox/audit.md"
        ]
        violations = merge_gate.check_files_in_scope(files, allow, deny)
        self.assertEqual(len(violations), 0)

    def test_10_deep_directory_wildcard_matching(self):
        """Kịch bản 10: Khớp thư mục đệ quy sâu (agent_core/**)."""
        allow = ["agent_core/**"]
        self.assertTrue(merge_gate.test_match("agent_core/eval/cso_scanner.py", allow))
        self.assertTrue(merge_gate.test_match("agent_core/eval/sub/deep/file.py", allow))
        self.assertFalse(merge_gate.test_match("scripts/eval/cso_scanner.py", allow))

    def test_11_extension_wildcard_matching(self):
        """Kịch bản 11: Khớp theo đuôi tệp (*.py)."""
        allow = ["src/*.py"]
        self.assertTrue(merge_gate.test_match("src/main.py", allow))
        self.assertFalse(merge_gate.test_match("src/main.js", allow))
        self.assertFalse(merge_gate.test_match("src/sub/main.py", allow))

    def test_12_deny_precedence_over_allow(self):
        """Kịch bản 12: scope_deny luôn có độ ưu tiên cao hơn scope_edit khi cùng khớp."""
        allow = ["agent_core/**"]
        deny = ["agent_core/core/secret.py"]
        files = ["agent_core/eval/scanner.py", "agent_core/core/secret.py"]
        violations = merge_gate.check_files_in_scope(files, allow, deny)
        self.assertEqual(len(violations), 1)
        self.assertIn("DENIED", violations[0])
        self.assertIn("agent_core/core/secret.py", violations[0])

    def test_13_whitespace_and_quote_variations_in_frontmatter(self):
        """Kịch bản 13: Xử lý linh hoạt khoảng trắng thừa và dấu nháy đơn/kép."""
        card_text = (
            "---\n"
            "id:   T-15   \n"
            "scope_edit:   \n"
            '  -   "agent_core/eval/**"   \n'
            "  -   'tests/**'   \n"
            "---\n"
        )
        task_id, allow, deny = merge_gate.parse_card_frontmatter(card_text)
        self.assertEqual(task_id, "T-15")
        self.assertEqual(allow, ["agent_core/eval/**", "tests/**"])

    def test_14_windows_backslash_normalization(self):
        """Kịch bản 14: Chuẩn hóa đường dẫn Windows chứa dấu gạch chéo ngược (\\)."""
        allow = ["agent_core/eval/**"]
        deny = ["scripts/**"]
        # Đường dẫn kiểu Windows
        files = ["agent_core\\eval\\code_reviewer.py"]
        violations = merge_gate.check_files_in_scope(files, allow, deny)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    unittest.main()
