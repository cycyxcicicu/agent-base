import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Module sẽ cài đặt
from agent_core.workflow.task_discovery import (
    discover_tasks,
    discover_task_tickets,
    parse_task_frontmatter,
)


class TestTaskDiscovery(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.root_tasks = Path(self.tmp_dir) / "tasks"
        self.root_tasks.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_recursive_discovery_and_metadata(self):
        # Tạo card ở gốc và trong thư mục lồng
        card1 = self.root_tasks / "T-01.md"
        card1.write_text(
            """---
id: T-01
status: done
owner: dev
epic: E1
---
# T-01: Root Task
""",
            encoding="utf-8",
        )

        sub_dir = self.root_tasks / "E2-epic"
        sub_dir.mkdir()
        card2 = sub_dir / "T-02.md"
        card2.write_text(
            """---
id: T-02
status: todo
owner: architect
epic: E2
blocked_by: [T-01]
---
# T-02: Nested Task
""",
            encoding="utf-8",
        )

        # File bắt đầu bằng _ hoặc không phải T-*.md
        (self.root_tasks / "_template.md").write_text("# Template", encoding="utf-8")
        (self.root_tasks / "BOARD.md").write_text("# Board", encoding="utf-8")

        cards = discover_tasks(self.root_tasks)
        self.assertEqual(len(cards), 2)
        c_ids = {c["id"] for c in cards}
        self.assertEqual(c_ids, {"T-01", "T-02"})

        # Kiểm tra metadata
        c2 = next(c for c in cards if c["id"] == "T-02")
        self.assertEqual(c2["status"], "todo")
        self.assertEqual(c2["blocked_by"], ["T-01"])
        self.assertEqual(c2["folder"], "E2-epic")

    def test_dotted_id_support(self):
        card = self.root_tasks / "T-11.2.md"
        card.write_text(
            """---
id: T-11.2
status: doing
owner: dev
---
# T-11.2: Subtask
""",
            encoding="utf-8",
        )
        cards = discover_tasks(self.root_tasks)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["id"], "T-11.2")

    def test_duplicate_id_raises_error(self):
        (self.root_tasks / "T-01.md").write_text(
            """---
id: T-01
status: todo
---
# T-01
""",
            encoding="utf-8",
        )
        sub = self.root_tasks / "sub"
        sub.mkdir()
        (sub / "T-01-dup.md").write_text(
            """---
id: T-01
status: todo
---
# T-01 Duplicate
""",
            encoding="utf-8",
        )
        with self.assertRaises(ValueError) as ctx:
            discover_tasks(self.root_tasks)
        self.assertIn("Trùng lặp card ID", str(ctx.exception))

    def test_legacy_uppercase_status_normalization(self):
        card = self.root_tasks / "T-05.md"
        card.write_text(
            """---
id: T-05
status: IN_PROGRESS
---
# T-05: Legacy Status
""",
            encoding="utf-8",
        )
        cards = discover_tasks(self.root_tasks)
        self.assertEqual(cards[0]["status"], "doing")

    def test_tickets_conversion(self):
        card = self.root_tasks / "T-08.md"
        card.write_text(
            """---
id: T-08
status: todo
blocked_by: [T-07]
---
# T-08: Task Title
Giao diện frontend component UI.
Kiểm thử Unit test.
""",
            encoding="utf-8",
        )
        tickets = discover_task_tickets(self.root_tasks)
        self.assertEqual(len(tickets), 1)
        t = tickets[0]
        self.assertEqual(t.ticket_id, "T-08")
        self.assertEqual(t.status, "TODO")
        self.assertEqual(t.blocked_by, ["T-07"])
        self.assertTrue(t.has_ui)
        self.assertTrue(t.has_test)

    def test_markdown_table_card_fallback_parsing(self):
        card = self.root_tasks / "T-UC06.4-demo.md"
        card.write_text(
            """# Task Card: T-UC06.4-demo

| Thuộc tính | Giá trị |
|---|---|
| **Mã task** | `T-UC-06.4` |
| **Trạng thái** | `review` (chưa commit) |
| **Phạm vi sửa đổi (scope_edit)** | `src/main/java/com/gdt/`, `src/main/resources/application.yml` |
""",
            encoding="utf-8",
        )
        cards = discover_tasks(self.root_tasks)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["id"], "T-UC-06.4")
        self.assertEqual(cards[0]["status"], "review")
        self.assertEqual(cards[0]["scope_edit"], ["src/main/java/com/gdt/", "src/main/resources/application.yml"])


if __name__ == "__main__":
    unittest.main()
