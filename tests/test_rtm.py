import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Module sẽ cài đặt
from agent_core.workflow.rtm import (
    generate_rtm,
    check_rtm,
    RTMEntry,
    RTMReport,
)


class TestRTMContract(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.req_dir = Path(self.tmp_dir) / "docs" / "requirements"
        self.req_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_dir = Path(self.tmp_dir) / "tasks"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.out_dir = Path(self.tmp_dir) / "build" / "rtm"

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def _create_sample_req(self, filename: str, content: str):
        p = self.req_dir / filename
        p.write_text(content, encoding="utf-8")
        return p

    def _create_sample_card(self, filename: str, content: str):
        p = self.tasks_dir / filename
        p.write_text(content, encoding="utf-8")
        return p

    def test_rtm_generation_and_columns(self):
        self._create_sample_req("R-test.md", """
### R-01: First Requirement
- **Mô tả**: Phải có catalog.
- **Card thực hiện**: T-20.

### R-02: Second Requirement
- **Mô tả**: Phải có context.
- **Card thực hiện**: T-21.
""")
        self._create_sample_card("T-20.md", """---
id: T-20
status: review
requirements: [R-01]
scope_edit:
  - agent_core/knowledge/catalog.py
---
# T-20: Catalog

## File đã đổi
- `agent_core/knowledge/catalog.py`

## Kết quả test
Ran 12 tests in 0.1s - OK
""")
        report = generate_rtm(
            requirements_dir=self.req_dir,
            tasks_dir=self.tasks_dir,
            output_dir=self.out_dir,
        )
        self.assertEqual(len(report.entries), 2)
        # R-01 đã có task T-20
        e1 = next(e for e in report.entries if e.req_id == "R-01")
        self.assertEqual(e1.task_id, "T-20")
        self.assertIn("agent_core/knowledge/catalog.py", e1.files)
        self.assertTrue(e1.has_proof)
        # Cột xác nhận con người tuyệt đối không tự ghi Yes
        self.assertNotIn("Yes", e1.user_approval)

        # R-02 chưa có file card T-21 trên đĩa
        e2 = next(e for e in report.entries if e.req_id == "R-02")
        self.assertEqual(e2.task_id, "T-21")
        self.assertEqual(len(e2.files), 0)

        # File Markdown RTM.md được sinh
        rtm_file = self.out_dir / "RTM.md"
        self.assertTrue(rtm_file.is_file())
        content = rtm_file.read_text(encoding="utf-8")
        self.assertIn("R-01", content)
        self.assertIn("R-02", content)
        self.assertIn("(người)", content)

    def test_check_reports_missing_linkages(self):
        self._create_sample_req("R-test.md", """
### R-01: Fully linked
- **Card thực hiện**: T-20.

### R-02: Missing task
- **Mô tả**: Chưa giao card nào.
""")
        self._create_sample_card("T-20.md", """---
id: T-20
status: todo
requirements: [R-01]
---
# T-20: Missing test and proof
""")
        report = check_rtm(
            requirements_dir=self.req_dir,
            tasks_dir=self.tasks_dir,
        )
        # Báo cáo phát hiện:
        # R-02 thiếu task
        # T-20 thiếu test và thiếu bằng chứng
        self.assertFalse(report.is_clean)
        issue_types = [issue["type"] for issue in report.issues]
        self.assertIn("MISSING_TASK", issue_types)
        self.assertIn("MISSING_TEST", issue_types)

    def test_idempotent_rtm_generation(self):
        self._create_sample_req("R-test.md", "### R-01: Req\n- **Card thực hiện**: T-01.\n")
        self._create_sample_card("T-01.md", "---\nid: T-01\n---\n# T-01\n")

        generate_rtm(self.req_dir, self.tasks_dir, self.out_dir)
        bytes1 = (self.out_dir / "RTM.md").read_bytes()

        generate_rtm(self.req_dir, self.tasks_dir, self.out_dir)
        bytes2 = (self.out_dir / "RTM.md").read_bytes()

        self.assertEqual(bytes1, bytes2)


    def test_cli_execution(self):
        import subprocess
        import sys

        self._create_sample_req("R-test.md", "### R-01: Req\n- **Card thực hiện**: T-01.\n")
        self._create_sample_card("T-01.md", "---\nid: T-01\n---\n# T-01\n")

        cmd = [
            sys.executable, "scripts/rtm.py",
            "--req-dir", str(self.req_dir),
            "--tasks-dir", str(self.tasks_dir),
            "--output", str(self.out_dir / "custom_rtm.md"),
            "--format", "json"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["entry_count"], 1)
        self.assertTrue((self.out_dir / "custom_rtm.md").is_file())


if __name__ == "__main__":
    unittest.main()
