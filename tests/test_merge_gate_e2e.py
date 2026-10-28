"""
tests/test_merge_gate_e2e.py
Kiểm thử end-to-end cho scripts/merge-gate.py trên repo git tạm.

Khác với tests/test_merge_gate.py (chỉ kiểm phân tích YAML và khớp glob), file này chạy đúng lệnh CLI trên các nhánh thật
để giữ các lỗ hổng đã từng tồn tại: card do chính nhánh tự sửa scope, đổi tên file bị cấm bằng `git mv`, card mới chỉ có
trên nhánh, phiếu rủi ro tự tạo hoặc tự nâng lên APPROVED, xoá card.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE = Path(os.environ.get("MERGE_GATE_SCRIPT", str(ROOT / "scripts" / "merge-gate.py")))

CARD_TEMPLATE = (
    "---\nid: T-1\nstatus: {status}\nscope_edit:\n{edit}\nscope_deny:\n{deny}\n---\n# card\n"
)
DEFAULT_EDIT = "  - src/**\n  - tests/**"
DEFAULT_DENY = "  - AGENTS.md"


def card(status="todo", edit=DEFAULT_EDIT, deny=DEFAULT_DENY, task_id="T-1"):
    return CARD_TEMPLATE.replace("T-1", task_id).format(status=status, edit=edit, deny=deny)


class GateRepoTestCase(unittest.TestCase):
    """Tạo repo git tạm có nhánh gốc `develop`, card T-1 và phiếu rủi ro RK-9 (PENDING)."""

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="gate-e2e-"))
        self.addCleanup(shutil.rmtree, str(self.repo), True)
        self.git("init", "-q", "-b", "develop")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "Human")
        self.git("config", "core.autocrlf", "false")
        self.write("AGENTS.md", "# rules\n")
        self.write("src/a.py", "print(1)\n")
        self.write("tasks/T-1.md", card())
        self.write("docs/risk/RK-9.md", "Status: PENDING\n\n## Chấp thuận\n(để trống)\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")

    # ------------------------------------------------------------------ helpers
    def git(self, *args):
        res = subprocess.run(["git", *args], cwd=self.repo, capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            raise AssertionError(f"git {' '.join(args)} failed: {res.stderr}")
        return res.stdout

    def write(self, rel, text):
        p = self.repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(text)

    def branch(self, name):
        self.git("checkout", "-q", "develop")
        self.git("checkout", "-q", "-b", name)

    def commit_all(self):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", "change")

    def run_gate(self, branch, card_path="tasks/T-1.md"):
        res = subprocess.run(
            [sys.executable, str(GATE), "--branch", branch, "--card", card_path, "--base", "develop"],
            cwd=self.repo, capture_output=True, text=True, encoding="utf-8",
        )
        return res.returncode, res.stdout + res.stderr

    def assertGatePasses(self, branch, card_path="tasks/T-1.md"):
        code, out = self.run_gate(branch, card_path)
        self.assertEqual(code, 0, out)

    def assertGateFails(self, branch, card_path="tasks/T-1.md", text=None):
        code, out = self.run_gate(branch, card_path)
        self.assertEqual(code, 1, out)
        if text:
            self.assertIn(text, out)


class TestGateMustBlock(GateRepoTestCase):
    def test_editing_denied_file(self):
        self.branch("f-deny")
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.assertGateFails("f-deny", text="AGENTS.md")

    def test_git_mv_of_denied_file_into_scope(self):
        """`git mv AGENTS.md src/AGENTS.md`: chỉ in tên mới nếu không dùng --no-renames."""
        self.branch("f-mv")
        self.git("mv", "AGENTS.md", "src/AGENTS.md")
        self.commit_all()
        self.assertGateFails("f-mv", text="AGENTS.md")

    def test_file_outside_scope(self):
        self.branch("f-out")
        self.write("README.md", "x\n")
        self.commit_all()
        self.assertGateFails("f-out", text="README.md")

    def test_deleting_denied_file(self):
        self.branch("f-del")
        self.git("rm", "-q", "AGENTS.md")
        self.git("commit", "-q", "-m", "rm")
        self.assertGateFails("f-del", text="AGENTS.md")

    def test_agent_widens_own_scope_in_card(self):
        self.branch("f-widen")
        self.write("tasks/T-1.md", card(edit='  - "**"', deny=""))
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.assertGateFails("f-widen", text="tampered")

    def test_agent_removes_scope_deny_only(self):
        self.branch("f-nodeny")
        self.write("tasks/T-1.md", card(deny=""))
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.assertGateFails("f-nodeny", text="tampered")

    def test_scope_rewritten_as_inline_list(self):
        self.branch("f-inline")
        self.write("tasks/T-1.md", "---\nid: T-1\nstatus: todo\nscope_edit: [\"**\"]\nscope_deny: []\n---\n# card\n")
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.assertGateFails("f-inline")

    def test_duplicate_scope_key_trick(self):
        self.branch("f-dupkey")
        self.write("tasks/T-1.md", "---\nid: T-1\nstatus: todo\nscope_edit:\n  - src/**\n  - tests/**\n  - \"**\"\nscope_deny:\n  - AGENTS.md\n---\n")
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.assertGateFails("f-dupkey")

    def test_card_id_changed(self):
        self.branch("f-id")
        self.write("tasks/T-1.md", card(task_id="T-77"))
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.assertGateFails("f-id")

    def test_card_that_exists_only_on_the_branch(self):
        self.branch("f-newcard")
        self.write("tasks/T-9.md", card(edit='  - "**"', deny="", task_id="T-9"))
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.assertGateFails("f-newcard", card_path="tasks/T-9.md", text="does not exist on base")

    def test_deleting_own_card(self):
        self.branch("f-delcard")
        self.git("rm", "-q", "tasks/T-1.md")
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.assertGateFails("f-delcard")

    def test_new_approved_risk_ticket_created_on_branch(self):
        self.branch("f-rk-new")
        self.write("docs/risk/RK-8.md", "Status: APPROVED\n\n## Chấp thuận\nOK\n")
        self.commit_all()
        self.assertGateFails("f-rk-new")

    def test_pending_risk_ticket_promoted_to_approved_on_branch(self):
        self.branch("f-rk-up")
        self.write("docs/risk/RK-9.md", "Status: APPROVED\n\n## Chấp thuận\nNgười dùng đồng ý RK-9\n")
        self.commit_all()
        self.assertGateFails("f-rk-up")

    def test_approved_risk_ticket_edited_on_branch(self):
        self.git("checkout", "-q", "develop")
        self.write("docs/risk/RK-5.md", "Status: APPROVED\n\n## Chấp thuận\nNgười thật đồng ý ngày 2026-09-21\n")
        self.commit_all()
        self.branch("f-rk-edit")
        self.write("docs/risk/RK-5.md", "Status: APPROVED\n\n## Chấp thuận\nĐã đổi nội dung\n")
        self.commit_all()
        self.assertGateFails("f-rk-edit")

    def test_base_branch_missing(self):
        self.branch("f-nobase")
        self.write("src/a.py", "print(2)\n")
        self.commit_all()
        res = subprocess.run(
            [sys.executable, str(GATE), "--branch", "f-nobase", "--card", "tasks/T-1.md", "--base", "no-such-branch"],
            cwd=self.repo, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertNotEqual(res.returncode, 0)


class TestGateMustPass(GateRepoTestCase):
    def test_change_inside_scope(self):
        self.branch("l-ok")
        self.write("src/a.py", "print(2)\n")
        self.commit_all()
        self.assertGatePasses("l-ok")

    def test_new_file_in_tests(self):
        self.branch("l-tests")
        self.write("tests/t.py", "x = 1\n")
        self.commit_all()
        self.assertGatePasses("l-tests")

    def test_status_change_in_card(self):
        self.branch("l-status")
        self.write("tasks/T-1.md", card(status="review"))
        self.commit_all()
        self.assertGatePasses("l-status")

    def test_session_log_appended_to_card_body(self):
        self.branch("l-log")
        self.write("tasks/T-1.md", card() + "\n## Nhật ký phiên\n- xong\n")
        self.commit_all()
        self.assertGatePasses("l-log")

    def test_handoff_note_in_inbox(self):
        self.branch("l-note")
        self.write("docs/notes/inbox/T-1-dev.md", "không có lưu ý\n")
        self.commit_all()
        self.assertGatePasses("l-note")

    def test_new_pending_risk_ticket(self):
        """risk-gate.md: lead lập phiếu PENDING trên nhánh, việc duyệt do người thực hiện trên nhánh gốc."""
        self.branch("l-rk")
        self.write("docs/risk/RK-3.md", "Status: PENDING\n\n## Chấp thuận\n(để trống)\n")
        self.commit_all()
        self.assertGatePasses("l-rk")

    def test_scope_lines_reordered(self):
        self.branch("l-order")
        self.write("tasks/T-1.md", card(edit="  - tests/**\n  - src/**"))
        self.write("src/a.py", "print(4)\n")
        self.commit_all()
        self.assertGatePasses("l-order")

    def test_yaml_comment_added_to_scope_line(self):
        self.branch("l-comment")
        self.write("tasks/T-1.md", card(edit='  - "src/**"\n  - tests/**   # test'))
        self.write("src/a.py", "print(5)\n")
        self.commit_all()
        self.assertGatePasses("l-comment")

    def test_card_saved_with_crlf(self):
        self.branch("l-crlf")
        self.write("tasks/T-1.md", card().replace("\n", "\r\n"))
        self.write("src/a.py", "print(6)\n")
        self.commit_all()
        self.assertGatePasses("l-crlf")

    def test_branch_without_changes(self):
        self.branch("l-empty")
        self.commit_all()
        self.assertGatePasses("l-empty")

    def test_develop_merged_back_into_branch(self):
        self.branch("l-merge")
        self.write("src/a.py", "print(7)\n")
        self.commit_all()
        self.git("checkout", "-q", "develop")
        self.write("docs/z.md", "z\n")
        self.commit_all()
        self.git("checkout", "-q", "l-merge")
        self.git("merge", "-q", "develop", "-m", "merge develop")
        self.assertGatePasses("l-merge")

    def test_gate_run_while_standing_on_base_branch(self):
        """Chạy gate khi đang đứng ở develop (không checkout nhánh) vẫn phải chặn nhánh sửa file cấm."""
        self.branch("l-standing")
        self.write("AGENTS.md", "# rules\nhack\n")
        self.commit_all()
        self.git("checkout", "-q", "develop")
        self.assertGateFails("l-standing", text="AGENTS.md")


class TestGateChangeSize(GateRepoTestCase):
    """Cỡ thay đổi (PR nguyên tử): mặc định chỉ cảnh báo, --strict-size mới chặn; lockfile không tính."""

    def run_gate_args(self, branch, *extra):
        res = subprocess.run(
            [sys.executable, str(GATE), "--branch", branch, "--card", "tasks/T-1.md", "--base", "develop", *extra],
            cwd=self.repo, capture_output=True, text=True, encoding="utf-8",
        )
        return res.returncode, res.stdout + res.stderr

    def big_branch(self, name, lines=30):
        self.branch(name)
        self.write("src/big.py", "".join(f"x{i} = {i}\n" for i in range(lines)))
        self.commit_all()

    def test_over_limit_warns_but_passes(self):
        self.big_branch("s-warn")
        code, out = self.run_gate_args("s-warn", "--max-lines", "10")
        self.assertEqual(code, 0, out)
        self.assertIn("WARN", out)
        self.assertIn("src/big.py", out)

    def test_over_limit_fails_when_strict(self):
        self.big_branch("s-strict")
        code, out = self.run_gate_args("s-strict", "--max-lines", "10", "--strict-size")
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL", out)

    def test_under_limit_is_silent(self):
        self.big_branch("s-ok", lines=5)
        code, out = self.run_gate_args("s-ok", "--max-lines", "10", "--strict-size")
        self.assertEqual(code, 0, out)
        self.assertNotIn("WARN", out)

    def test_limit_read_from_project_md(self):
        self.branch("s-proj")
        self.write("PROJECT.md", "| Giới hạn dòng thay đổi | 10 |\n")
        self.commit_all()
        self.git("checkout", "-q", "develop")
        self.git("merge", "-q", "s-proj")
        self.branch("s-proj2")
        self.write("src/big.py", "".join(f"x{i} = {i}\n" for i in range(30)))
        self.commit_all()
        code, out = self.run_gate_args("s-proj2", "--strict-size")
        self.assertEqual(code, 1, out)

    def test_lockfile_not_counted(self):
        self.branch("s-lock")
        self.write("package-lock.json", "".join(f'"a{i}": {i},\n' for i in range(500)))
        self.write("src/a.py", "print(2)\n")
        self.commit_all()
        code, out = self.run_gate_args("s-lock", "--max-lines", "10")
        # package-lock.json nằm ngoài scope_edit nên vẫn bị chặn theo phạm vi, nhưng KHÔNG được báo vượt cỡ
        self.assertNotIn("dòng thay đổi", out)


if __name__ == "__main__":
    unittest.main()
