import os
import shutil
import tempfile
import unittest
from pathlib import Path

from agent_core.workflow.tracer_bullet import TicketParser, DependencyGraph


class TestFrontierDiscovery(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.task_dir = Path(self.tmp_dir) / "tasks"
        self.task_dir.mkdir()

        # Tạo card tầng gốc
        root_card = self.task_dir / "T-01.md"
        root_card.write_text(
            """---
id: T-01
status: done
---
# T-01: Root Task
Status: DONE
""",
            encoding="utf-8",
        )

        # Tạo card lồng trong thư mục epic
        epic_dir = self.task_dir / "E1-test"
        epic_dir.mkdir()
        nested_card = epic_dir / "T-02.md"
        nested_card.write_text(
            """---
id: T-02
status: todo
blocked_by: [T-01]
---
# T-02: Nested Task
Status: TODO
Bị chặn bởi: T-01
""",
            encoding="utf-8",
        )

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_frontier_legacy_fails_to_find_nested_card(self):
        # Mô phỏng logic cũ của agent_core/cli.py dòng 63:
        # chỉ dùng task_dir.glob("*.md")
        tickets = []
        for p in self.task_dir.glob("*.md"):
            if p.name.startswith("_"):
                continue
            ticket = TicketParser.parse_markdown(p.read_text(encoding="utf-8", errors="replace"), str(p))
            if ticket:
                tickets.append(ticket)

        # Legacy glob chỉ tìm thấy 1 card ở gốc (T-01), bỏ sót T-02
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0].ticket_id, "T-01")

        # Bây giờ kiểm tra hàm mới mong muốn: phải tìm thấy cả T-01 và T-02
        from agent_core.workflow.task_discovery import discover_task_tickets
        all_tickets = discover_task_tickets(self.task_dir)
        ticket_ids = {t.ticket_id for t in all_tickets}
        self.assertIn("T-01", ticket_ids)
        self.assertIn("T-02", ticket_ids)
        self.assertEqual(len(all_tickets), 2)


if __name__ == "__main__":
    unittest.main()
