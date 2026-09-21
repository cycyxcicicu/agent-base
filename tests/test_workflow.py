import unittest
from agent_core.workflow.tracer_bullet import Ticket, TicketParser, DependencyGraph
from agent_core.workflow.expand_contract import MigrationTracker, MigrationPhase
from agent_core.workflow.handoff import HandoffRouter


class TestWorkflowModules(unittest.TestCase):
    def test_parse_tracer_bullet_ticket(self):
        sample_md = (
            "# T-01: Xác thực Session Cookie\n"
            "- Trạng thái: DONE\n"
            "- Bị chặn bởi: Không có\n"
            "## Các tầng cắt dọc\n"
            "- UI: Giao diện đăng nhập\n"
            "- API: Route /auth/login\n"
            "- DB: Bảng sessions\n"
            "- Test: E2E login flow\n"
        )
        ticket = TicketParser.parse_markdown(sample_md, "tasks/T-01.md")
        self.assertEqual(ticket.ticket_id, "T-01")
        self.assertEqual(ticket.status, "DONE")
        self.assertTrue(ticket.has_ui)
        self.assertTrue(ticket.has_api)
        self.assertTrue(ticket.has_db)
        self.assertTrue(ticket.has_test)

    def test_dependency_graph_frontier(self):
        t1 = Ticket(ticket_id="T-01", title="Ticket 1", status="DONE")
        t2 = Ticket(ticket_id="T-02", title="Ticket 2", status="TODO", blocked_by=["T-01"])
        t3 = Ticket(ticket_id="T-03", title="Ticket 3", status="TODO", blocked_by=["T-02"])

        graph = DependencyGraph([t1, t2, t3])
        frontier = graph.get_frontier()

        # T-01 đã DONE, vậy chỉ có T-02 nằm ở đường biên Frontier sẵn sàng thực thi (T-03 còn chờ T-02)
        self.assertEqual(len(frontier), 1)
        self.assertEqual(frontier[0].ticket_id, "T-02")

    def test_expand_contract_migration(self):
        tracker = MigrationTracker()
        task = tracker.register_migration("user_email_split", old_target="users.name", new_target="users.first_name", initial_callers=5)
        self.assertEqual(task.phase, MigrationPhase.EXPAND)

        # Di chuyển còn 2 callers
        task = tracker.advance_phase("user_email_split", remaining_callers=2)
        self.assertEqual(task.phase, MigrationPhase.MIGRATE)
        self.assertFalse(task.is_safe_to_contract)

        # Di chuyển hết callers
        task = tracker.advance_phase("user_email_split", remaining_callers=0)
        self.assertEqual(task.phase, MigrationPhase.CONTRACT)
        self.assertTrue(task.is_safe_to_contract)

    def test_handoff_router(self):
        self.assertTrue(HandoffRouter.can_transition("dev", "qa"))
        self.assertTrue(HandoffRouter.can_transition("qa", "dev"))
        note = HandoffRouter.create_note(
            from_role="dev",
            to_role="qa",
            task_id="T-01",
            summary="Đã xong API và UI",
            files_changed=["src/api.py"],
            proof_of_done="pytest 10 passed"
        )
        self.assertEqual(note.task_id, "T-01")

    def test_cycle_detection_and_topological_sort(self):
        # 1. Hợp lệ: Không có chu trình
        t1 = Ticket(ticket_id="T-01", title="Init", status="DONE")
        t2 = Ticket(ticket_id="T-02", title="API", status="TODO", blocked_by=["T-01"])
        t3 = Ticket(ticket_id="T-03", title="UI", status="TODO", blocked_by=["T-02"])

        graph = DependencyGraph([t1, t2, t3])
        self.assertIsNone(graph.detect_cycles())

        order = graph.topological_sort()
        self.assertEqual(order, ["T-01", "T-02", "T-03"])

        crit_path = graph.calculate_critical_path()
        self.assertEqual(crit_path, ["T-01", "T-02", "T-03"])

        # 2. Bất hợp lệ: Có chu trình vòng (Deadlock: T-A -> T-B -> T-A)
        ta = Ticket(ticket_id="T-A", title="Task A", status="TODO", blocked_by=["T-B"])
        tb = Ticket(ticket_id="T-B", title="Task B", status="TODO", blocked_by=["T-A"])
        cycle_graph = DependencyGraph([ta, tb])
        cycle = cycle_graph.detect_cycles()
        self.assertIsNotNone(cycle)
        self.assertIn("T-A", cycle)
        self.assertIn("T-B", cycle)

        with self.assertRaises(ValueError):
            cycle_graph.topological_sort()


if __name__ == "__main__":
    unittest.main()
