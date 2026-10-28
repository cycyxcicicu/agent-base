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

    def test_scan_skips_docs_readme_and_generated_dirs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text(
                "# debt: docs, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )
            (root / "README.md").write_text(
                "# debt: readme, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )
            (root / ".claude" / "agents").mkdir(parents=True)
            (root / ".claude" / "agents" / "dev.py").write_text(
                "# debt: generated, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )
            (root / "app.py").write_text(
                "# debt: real, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )

            items = DebtParser.scan_directory(root)

            self.assertEqual([item.shortcut for item in items], ["real"])

    def test_prose_describing_syntax_is_not_debt(self):
        line = "# Nhận diện cả # debt:, // debt:, /* debt:, <!-- debt:"
        self.assertIsNone(DebtParser.parse_line(line, "parser.py", 25))

    def test_malformed_tag_only_at_comment_start(self):
        self.assertIsNotNone(
            DebtParser.parse_line("# debt: hack, ceiling: 50", "a.py", 1)
        )
        self.assertIsNone(
            DebtParser.parse_line("x = 1  # debt: hack", "a.py", 1)
        )
        self.assertIsNotNone(
            DebtParser.parse_line(
                "x = 1  # debt: hack, ceiling: 50, upgrade: later", "a.py", 1
            )
        )

    def test_render_uses_real_module_path(self):
        md = DebtLedger(Path(".")).render_markdown()
        self.assertIn("agent_core/debt/ledger.py", md)
        self.assertNotIn("src/debt/", md)

    def test_write_to_file_is_idempotent_and_ignores_its_output(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "app.py").write_text(
                "# debt: real, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )
            out = root / "docs" / "DEBT.md"

            first = DebtLedger(root)
            first.harvest()
            first.write_to_file(target_file=out)
            first_text = out.read_text(encoding="utf-8")

            second = DebtLedger(root)
            second.harvest()
            second.write_to_file(target_file=out)

            self.assertEqual(len(second.items), 1)
            self.assertEqual(second.items[0].shortcut, "real")
            self.assertEqual(first_text, out.read_text(encoding="utf-8"))

    def test_scan_handles_parent_dir_named_like_exclude(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            project = Path(tmp_dir) / "build" / "project"
            project.mkdir(parents=True)
            (project / "app.py").write_text(
                "# debt: real, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )

            items = DebtParser.scan_directory(project)

            self.assertEqual([item.shortcut for item in items], ["real"])

    def test_source_filename_and_comment_markers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "Makefile").write_text(
                "# debt: make, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )
            (root / "Dockerfile.dev").write_text(
                "# debt: docker, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )
            (root / "query.sql").write_text(
                "-- debt: sql, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )
            (root / "setup.ini").write_text(
                "; debt: ini, ceiling: 10, upgrade: later\n", encoding="utf-8"
            )

            items = DebtParser.scan_directory(root)

            self.assertEqual(
                sorted(item.shortcut for item in items),
                ["docker", "ini", "make", "sql"],
            )

    def test_ceiling_can_contain_comma(self):
        item = DebtParser.parse_line(
            "# debt: cache, ceiling: 50,000 users, upgrade: redis", "a.py", 1
        )
        self.assertIsNotNone(item)
        self.assertEqual(item.ceiling, "50,000 users")
        self.assertEqual(item.upgrade_path, "redis")

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
