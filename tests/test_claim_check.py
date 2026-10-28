import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Module sẽ cài đặt
from agent_core.workflow.claim_check import (
    check_task_claim,
    ClaimCheckResult,
)


class TestClaimCheckContract(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.tasks_dir = Path(self.tmp_dir) / "tasks"
        self.tasks_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def _create_sample_card(self, rel_path: str, content: str) -> Path:
        p = self.tasks_dir / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def test_g0_fails_when_no_user_approval(self):
        # Card chưa có dấu [x] người dùng duyệt
        card_content = """---
id: T-90
status: todo
scope_edit:
  - src/module.py
---
# T-90: Unapproved Task

## Mục tiêu
Làm tính năng mới.

## Tiêu chí xong
- [ ] Xong tính năng.

## Phân Rã Subtasks
- [ ] **T-90.1**: Scope: `src/module.py` · Handoff: `docs/notes/inbox/T-90.1-dev.md`

- **Cổng phê duyệt kế hoạch**:
  - [ ] **Người dùng duyệt phạm vi bằng file**: (chưa)
"""
        card_path = self._create_sample_card("T-90.md", card_content)
        result = check_task_claim(card_path, tasks_root=self.tasks_dir)
        self.assertEqual(result.verdict, "BLOCKED")
        self.assertFalse(result.checks["G0"]["pass"])
        self.assertIn("chưa được người dùng duyệt", result.checks["G0"]["message"])

    def test_seq_fails_when_blocked_by_not_done(self):
        # T-91 bị chặn bởi T-90 mà T-90 mới ở todo
        self._create_sample_card("T-90.md", """---
id: T-90
status: todo
---
# T-90
""")
        card_content = """---
id: T-91
status: todo
blocked_by: [T-90]
scope_edit:
  - src/feature.py
---
# T-91: Task With Dependency

## Mục tiêu
Mục tiêu hợp lệ.

## Tiêu chí xong
- [ ] Tiêu chí hợp lệ.

## Phân Rã Subtasks
- [ ] **T-91.1**: Scope: `src/feature.py` · Handoff: `docs/notes/inbox/T-91.1-dev.md`

- **Cổng phê duyệt kế hoạch**:
  - [x] **Người dùng duyệt phạm vi bằng file**: Nguoi dung · 2026-10-28
"""
        card_path = self._create_sample_card("T-91.md", card_content)
        result = check_task_claim(card_path, tasks_root=self.tasks_dir)
        self.assertEqual(result.verdict, "BLOCKED")
        self.assertFalse(result.checks["SEQ"]["pass"])
        self.assertIn("T-90", result.checks["SEQ"]["message"])

    def test_dor_fails_when_missing_subtasks_or_handoff(self):
        # Card thiếu mục Phân Rã Subtasks hoặc handoff path
        card_content = """---
id: T-92
status: todo
scope_edit:
  - src/code.py
---
# T-92: Incomplete DoR

## Mục tiêu
Có mục tiêu.

## Tiêu chí xong
- [ ] Xong việc.

- **Cổng phê duyệt kế hoạch**:
  - [x] **Người dùng duyệt phạm vi bằng file**: Nguoi dung · 2026-10-28
"""
        card_path = self._create_sample_card("T-92.md", card_content)
        result = check_task_claim(card_path, tasks_root=self.tasks_dir)
        self.assertEqual(result.verdict, "BLOCKED")
        self.assertFalse(result.checks["DoR"]["pass"])

    def test_plan_fails_when_scope_overlaps_with_doing_card(self):
        # T-93 đang doing và sửa `agent_core/knowledge/*.py`
        self._create_sample_card("T-93.md", """---
id: T-93
status: doing
scope_edit:
  - agent_core/knowledge/*.py
---
# T-93: Doing task
""")
        # T-94 muốn claim `agent_core/knowledge/catalog.py` -> XUNG ĐỘT
        card_content = """---
id: T-94
status: todo
scope_edit:
  - agent_core/knowledge/catalog.py
---
# T-94: Overlapping task

## Mục tiêu
Cải tiến catalog.

## Tiêu chí xong
- [ ] Hoàn tất.

## Phân Rã Subtasks
- [ ] **T-94.1**: Scope: `agent_core/knowledge/catalog.py` · Handoff: `docs/notes/inbox/T-94.1-dev.md`

- **Cổng phê duyệt kế hoạch**:
  - [x] **Người dùng duyệt phạm vi bằng file**: Nguoi dung · 2026-10-28
"""
        card_path = self._create_sample_card("T-94.md", card_content)
        result = check_task_claim(card_path, tasks_root=self.tasks_dir)
        self.assertEqual(result.verdict, "BLOCKED")
        self.assertFalse(result.checks["PLAN"]["pass"])
        self.assertIn("chồng lấn", result.checks["PLAN"]["message"])

    def test_happy_path_claim_passes(self):
        # Card thỏa mãn cả 5 điều kiện
        self._create_sample_card("T-80.md", """---
id: T-80
status: done
---
# T-80
""")
        card_content = """---
id: T-95
status: todo
blocked_by: [T-80]
scope_edit:
  - agent_core/other/safe.py
---
# T-95: Clean Task

## Mục tiêu
Phát triển tính năng an toàn độc lập.

## Tiêu chí xong
- [ ] Code hoàn tất và test pass.

## Phân Rã Subtasks
- [ ] **T-95.1**: Scope: `agent_core/other/safe.py` · Handoff: `docs/notes/inbox/T-95.1-dev.md`

- **Cổng phê duyệt kế hoạch**:
  - [x] **Người dùng duyệt phạm vi bằng file**: Nguoi dung · 2026-10-28
"""
        card_path = self._create_sample_card("T-95.md", card_content)
        result = check_task_claim(card_path, tasks_root=self.tasks_dir)
        self.assertEqual(result.verdict, "PASS")
        for k, v in result.checks.items():
            self.assertTrue(v["pass"], f"Check {k} failed: {v['message']}")


if __name__ == "__main__":
    unittest.main()
