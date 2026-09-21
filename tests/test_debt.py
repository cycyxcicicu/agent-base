import unittest
import tempfile
from pathlib import Path
from agent_core.debt.parser import DebtParser
from agent_core.debt.ledger import DebtLedger


class TestDebtModules(unittest.TestCase):
    def test_parse_structured_debt_line(self):
        line = "# debt: dùng sqlite thay vì postgres để test nhanh, ceiling: 50 requests/s, upgrade: chuyển sang postgres pool"
        item = DebtParser.parse_line(line, "test.py", 10)
        self.assertIsNotNone(item)
        self.assertEqual(item.shortcut, "dùng sqlite thay vì postgres để test nhanh")
        self.assertEqual(item.ceiling, "50 requests/s")
        self.assertEqual(item.upgrade_path, "chuyển sang postgres pool")

    def test_debt_ledger_scan_and_render(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            code_file = tmp_path / "app.py"
            code_file.write_text(
                "def run():\n"
                "    # debt: hardcode timeout 10s, ceiling: 100 users, upgrade: đọc từ env config\n"
                "    pass\n",
                encoding="utf-8"
            )

            ledger = DebtLedger(tmp_path)
            items = ledger.harvest()
            self.assertEqual(len(items), 1)

            md = ledger.render_markdown()
            self.assertIn("hardcode timeout 10s", md)
            self.assertIn("100 users", md)

    def test_debt_ceiling_audit_and_pre_commit_gate(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            code_file = tmp_path / "service.py"
            code_file.write_text(
                "def process():\n"
                "    # debt: bypass cache, ceiling: 50 req/s, upgrade: add redis\n"
                "    # debt: temp mock, ceiling: 2020-01-01, upgrade: connect live db\n"
                "    pass\n",
                encoding="utf-8"
            )

            ledger = DebtLedger(tmp_path)
            # 1. Đo lường bình thường: tải 20 req/s (dưới trần 50) nhưng dính hạn 2020-01-01
            breaches = ledger.audit_ceilings({"req/s": 20})
            self.assertEqual(len(breaches), 1)
            self.assertEqual(breaches[0]["type"], "DATE_EXPIRED")

            # 2. Quá tải 80 req/s (vượt trần 50 req/s)
            breaches_overload = ledger.audit_ceilings({"req/s": 80})
            self.assertEqual(len(breaches_overload), 2)

            # 3. Pre-commit gate phát hiện vi phạm
            passed, msg = ledger.verify_pre_commit_gate({"req/s": 80})
            self.assertFalse(passed)
            self.assertIn("CẢNH BÁO PRE-COMMIT", msg)


if __name__ == "__main__":
    unittest.main()
