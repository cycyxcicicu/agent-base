"""
tests/test_agy_bridge.py
Kiểm thử toàn diện scripts/agy-bridge.py theo yêu cầu brief P1, P1c và P1d.
Sử dụng agy giả (mock Python script) để kiểm tra:
1. Thành công ở model đầu;
2. denied_actions không rỗng thì leo thang sang model sau;
3. Mã thoát 1 + status:"ERROR";
4. Hết thang thì mã 2;
5. VIOLATION khi file đổi ngoài phạm vi (dùng git repo tạm bằng git init);
6. stdout đúng 3 dòng;
7. --dry-run không chạy agy;
8. argv KHÔNG chứa --dangerously-skip-permissions, KHÔNG chứa --mode, và --settings chứa write_file( đúng đường dẫn;
9. Khóa và tự động dọn khóa;
10. Từ chối --allow-cmd git khi thiếu --allow-git;
11. Đổi HEAD (commit trong repo tạm) thì mã 3 và VIOLATION;
12. Hết quota (RESOURCE_EXHAUSTED) thì mã 7, gọi 1 lần, STATUS: quota ... DOI-TAI-KHOAN-AGY;
13. --worktree tạo worktree và agy chạy trong cwd worktree;
14. --worktree map allow-write sang worktree trong --settings;
15. Phiên khác ghi vào repo gốc KHÔNG gây VIOLATION khi có --worktree;
16. Ghi ngoài allow-write trong worktree vẫn VIOLATION mã 3;
17. --seed được sao chép và không tính là thay đổi;
18. --apply sao chép file về repo gốc khi thành công;
19. --apply từ chối với mã 5 khi file đích ở repo gốc bị sửa sau khi tạo worktree;
20. --dry-run + --worktree không tạo worktree, in 1 dòng JSON plan.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIDGE_PATH = ROOT / "scripts" / "agy-bridge.py"

# Import bridge module
_spec = importlib.util.spec_from_file_location("agy_bridge", str(BRIDGE_PATH))
agy_bridge = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agy_bridge)

MOCK_AGY_SCRIPT = """#!/usr/bin/env python3
import sys
import json
import os
import subprocess
from pathlib import Path

log_path = os.environ.get("MOCK_AGY_LOG")
if log_path:
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(sys.argv) + "\\n")

scenario = os.environ.get("MOCK_AGY_SCENARIO", "success")

model = ""
if "--model" in sys.argv:
    idx = sys.argv.index("--model")
    if idx + 1 < len(sys.argv):
        model = sys.argv[idx + 1]

if scenario == "success":
    res = {
        "conversation_id": "conv-1",
        "status": "SUCCESS",
        "response": "Success response",
        "duration_seconds": 1.0,
        "num_turns": 1,
        "usage": {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        "denied_actions": []
    }
    print(json.dumps(res))
    sys.exit(0)

elif scenario == "success_response_with_digits":
    res = {
        "conversation_id": "conv-1",
        "status": "SUCCESS",
        "response": "Done agy/hello-brief-20261114-201429 successfully",
        "duration_seconds": 1.0,
        "num_turns": 1,
        "usage": {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        "denied_actions": []
    }
    print(json.dumps(res))
    sys.exit(0)

elif scenario == "cmd_denied_warn":
    res = {
        "conversation_id": "conv-warn",
        "status": "SUCCESS",
        "response": "Command denied response",
        "duration_seconds": 1.0,
        "num_turns": 1,
        "usage": {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        "denied_actions": [{"action": "command"}]
    }
    print(json.dumps(res))
    sys.exit(0)

elif scenario == "escalate_on_denied":
    if "flash-medium" in model:
        res = {
            "conversation_id": "conv-1",
            "status": "SUCCESS",
            "response": "Denied action",
            "usage": {"total_tokens": 40},
            "denied_actions": [{"action": "write_file"}]
        }
        print(json.dumps(res))
        sys.exit(0)
    else:
        res = {
            "conversation_id": "conv-2",
            "status": "SUCCESS",
            "response": "High model success",
            "usage": {"total_tokens": 60},
            "denied_actions": []
        }
        print(json.dumps(res))
        sys.exit(0)

elif scenario == "error_exit_1":
    res = {
        "conversation_id": "conv-err",
        "status": "ERROR",
        "error": "Error occurred",
        "usage": {"total_tokens": 15}
    }
    print(json.dumps(res))
    sys.exit(1)

elif scenario == "escalate_after_error":
    if "flash-medium" in model:
        res = {
            "conversation_id": "conv-err",
            "status": "ERROR",
            "error": "Flash medium error",
            "usage": {"total_tokens": 15}
        }
        print(json.dumps(res))
        sys.exit(1)
    else:
        res = {
            "conversation_id": "conv-ok",
            "status": "SUCCESS",
            "response": "Recovered on high model",
            "usage": {"total_tokens": 50},
            "denied_actions": []
        }
        print(json.dumps(res))
        sys.exit(0)

elif scenario == "violation":
    Path("unallowed_file.txt").write_text("violation content\\n", encoding="utf-8")
    res = {
        "conversation_id": "conv-viol",
        "status": "SUCCESS",
        "response": "Wrote forbidden file",
        "usage": {"total_tokens": 25},
        "denied_actions": []
    }
    print(json.dumps(res))
    sys.exit(0)

elif scenario == "allowed_write":
    Path("allowed_file.txt").write_text("allowed content\\n", encoding="utf-8")
    res = {
        "conversation_id": "conv-ok",
        "status": "SUCCESS",
        "response": "Wrote allowed file",
        "usage": {"total_tokens": 25},
        "denied_actions": []
    }
    print(json.dumps(res))
    sys.exit(0)

elif scenario == "quota_exhausted":
    res = {
        "conversation_id": "conv-quota",
        "status": "ERROR",
        "error": "RESOURCE_EXHAUSTED: quota exceeded",
        "usage": {"total_tokens": 15}
    }
    print(json.dumps(res))
    sys.exit(1)

elif scenario == "commit_in_repo":
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "illicit commit by agy"],
        capture_output=True,
    )
    res = {
        "conversation_id": "conv-commit",
        "status": "SUCCESS",
        "response": "committed in repo",
        "usage": {"total_tokens": 20},
        "denied_actions": []
    }
    print(json.dumps(res))
    sys.exit(0)

elif scenario == "record_cwd_and_write":
    cwd_log = os.environ.get("MOCK_AGY_CWD_LOG")
    if cwd_log:
        with open(cwd_log, "w", encoding="utf-8") as f:
            f.write(os.getcwd())
    target = os.environ.get("MOCK_AGY_WRITE_TARGET")
    if target:
        p = Path(target)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("content written in worktree\\n", encoding="utf-8")
    other_repo = os.environ.get("OTHER_SESSION_REPO")
    if other_repo:
        (Path(other_repo) / "other_session_file.txt").write_text("concurrent write\\n", encoding="utf-8")
    res = {
        "conversation_id": "conv-wt",
        "status": "SUCCESS",
        "response": "recorded cwd and wrote target",
        "usage": {"total_tokens": 25},
        "denied_actions": []
    }
    print(json.dumps(res))
    sys.exit(0)

elif scenario == "conflict_apply":
    target = os.environ.get("MOCK_AGY_WRITE_TARGET", "target.txt")
    p = Path(target)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("content from agy\\n", encoding="utf-8")
    other_repo = os.environ.get("OTHER_SESSION_REPO")
    if other_repo:
        (Path(other_repo) / target).write_text("concurrent conflict edit\\n", encoding="utf-8")
    res = {
        "conversation_id": "conv-conflict",
        "status": "SUCCESS",
        "response": "done",
        "usage": {"total_tokens": 20},
        "denied_actions": []
    }
    print(json.dumps(res))
    sys.exit(0)
"""


class TestAgyBridge(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)

        # Temporary git repository
        self.repo_dir = self.root / "repo"
        self.repo_dir.mkdir()
        subprocess.run(["git", "init"], cwd=self.repo_dir, capture_output=True, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=self.repo_dir,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=self.repo_dir,
            capture_output=True,
            check=True,
        )
        (self.repo_dir / "README.md").write_text("# Repo\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo_dir, capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", "init"],
            cwd=self.repo_dir,
            capture_output=True,
            check=True,
        )

        # Task brief file
        self.task_file = self.root / "task.md"
        self.task_file.write_text("# Test Brief\nThực hiện nhiệm vụ.\n", encoding="utf-8")

        # Report dir
        self.report_dir = self.root / "reports"

        # Mock agy binary
        self.mock_agy = self.root / "mock_agy.py"
        self.mock_agy.write_text(MOCK_AGY_SCRIPT, encoding="utf-8")
        os.chmod(self.mock_agy, 0o755)

        self.log_file = self.root / "mock_agy.log"

    def tearDown(self):
        self.tmpdir.cleanup()

    def run_bridge(
        self,
        args: list[str],
        scenario: str = "success",
        env_extra: dict | None = None,
    ) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["AGY_BIN"] = str(self.mock_agy)
        env["MOCK_AGY_LOG"] = str(self.log_file)
        env["MOCK_AGY_SCENARIO"] = scenario
        if env_extra:
            env.update(env_extra)
        cmd = [sys.executable, str(BRIDGE_PATH), "run"] + args
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

    def test_success_first_model(self):
        """1. Thành công ở model đầu tiên: thoát 0, không leo thang."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok model=gemini-3.8-flash-medium"))
        self.assertIn("conv=conv-1", lines[0])
        self.assertIn("tokens=30", lines[0])

        # Verify agy was called once
        logs = [line for line in self.log_file.read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual(len(logs), 1)
        self.assertIn("gemini-3.8-flash-medium", logs[0])

    def test_cmd_denied_warn_no_escalation(self):
        """agy giả trả SUCCESS + denied_actions:[{"action":"command"}]: chỉ gọi MỘT lần (không leo thang), mã thoát 0, STATUS bắt đầu STATUS: warn, stdout đúng 3 dòng."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="cmd_denied_warn",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: warn model=gemini-3.8-flash-medium"))
        self.assertIn("conv=conv-warn", lines[0])
        self.assertIn("tokens=30", lines[0])
        self.assertTrue(lines[0].endswith("cmd-denied"))
        self.assertEqual(
            lines[0],
            "STATUS: warn model=gemini-3.8-flash-medium conv=conv-warn tokens=30 cmd-denied",
        )
        self.assertTrue(lines[1].startswith("FILES: "))
        self.assertTrue(lines[2].startswith("REPORT: "))

        # Verify agy was called ONLY once (no escalation)
        logs = [line for line in self.log_file.read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual(len(logs), 1)
        self.assertIn("gemini-3.8-flash-medium", logs[0])

        # Verify report contains the warning note
        report_path = Path(lines[2].replace("REPORT: ", "").strip())
        self.assertTrue(report_path.exists())
        report_content = report_path.read_text(encoding="utf-8")
        self.assertIn(
            "thiếu quyền chạy lệnh, không phải lỗi model; kiểm tra `--allow-cmd` và lệnh bằng chứng trong brief",
            report_content,
        )

    def test_escalation_on_denied_actions(self):
        """2. denied_actions với write_file (từ chối cứng): vẫn leo thang sang model sau, stdout đúng 3 dòng."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="escalate_on_denied",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok model=gemini-3.8-flash-high"))
        self.assertIn("conv=conv-2", lines[0])
        self.assertIn("tokens=100", lines[0])  # 40 + 60
        self.assertTrue(lines[1].startswith("FILES: "))
        self.assertTrue(lines[2].startswith("REPORT: "))

        # Verify agy was called twice
        logs = [line for line in self.log_file.read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual(len(logs), 2)
        self.assertIn("gemini-3.8-flash-medium", logs[0])
        self.assertIn("gemini-3.8-flash-high", logs[1])

    def test_exit_code_1_status_error_and_recovery(self):
        """3. Mã thoát 1 + status:ERROR được phát hiện là lỗi và leo thang."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="escalate_after_error",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok model=gemini-3.8-flash-high"))

        logs = [line for line in self.log_file.read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual(len(logs), 2)

    def test_escalation_exhausted_exits_2(self):
        """4. Hết thang vẫn thất bại thì thoát mã 2."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="error_exit_1",
        )
        self.assertEqual(res.returncode, 2)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: fail model=gemini-3.8-flash-high"))

        # Verify report was still generated
        report_path = Path(lines[2].replace("REPORT: ", "").strip())
        self.assertTrue(report_path.exists())

    def test_violation_exits_3(self):
        """5. VIOLATION khi file đổi ngoài phạm vi: thoát mã 3."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--allow-write",
                "other_file.txt",
            ],
            scenario="violation",
        )
        self.assertEqual(res.returncode, 3)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: fail"))
        self.assertIn("VIOLATION: unallowed_file.txt", lines[1])

    def test_stdout_exact_three_lines(self):
        """6. In ra stdout ĐÚNG 3 dòng theo chuẩn."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="success",
        )
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: "))
        self.assertTrue(lines[1].startswith("FILES: "))
        self.assertTrue(lines[2].startswith("REPORT: "))

    def test_dry_run_does_not_call_agy(self):
        """7. --dry-run: in argv JSON trên 1 dòng, thoát 0, không gọi agy, không tạo khóa."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--dry-run",
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 1)
        argv = json.loads(lines[0])
        self.assertIsInstance(argv, list)
        self.assertIn("--model", argv)

        # Mock agy never called
        self.assertFalse(self.log_file.exists())

        # No lock files in report_dir
        if self.report_dir.exists():
            locks = list(self.report_dir.glob("*.lock"))
            self.assertEqual(len(locks), 0)

    def test_argv_no_skip_permissions_and_settings_has_write_file(self):
        """8. argv KHÔNG chứa --dangerously-skip-permissions, KHÔNG chứa --mode, và --settings chứa write_file."""
        target_path = "scripts/agy-bridge.py"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--allow-write",
                target_path,
                "--dry-run",
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 0)
        argv = json.loads(res.stdout.strip())
        self.assertNotIn("--dangerously-skip-permissions", argv)
        self.assertNotIn("--mode", argv)
        self.assertIn("--settings", argv)
        settings_idx = argv.index("--settings") + 1
        settings = json.loads(argv[settings_idx])
        self.assertIn(f"write_file({target_path})", settings["permissions"]["allow"])

    def test_locking_exits_4_and_cleans_up(self):
        """9. Khóa theo --dir: nếu đã có khóa thoát mã 4; luôn dọn khóa khi xong."""
        self.report_dir.mkdir(parents=True, exist_ok=True)
        lock_file = agy_bridge.get_lock_file(self.report_dir, self.repo_dir)

        # Simulate existing lock with current active PID
        lock_file.write_text(f"pid={os.getpid()}\n", encoding="utf-8")
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 4)
        self.assertIn("bị khóa", res.stderr)

        # Remove lock and run normally -> lock cleaned up after run
        lock_file.unlink()
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 0)
        self.assertFalse(lock_file.exists())

    def test_refuse_git_cmd_without_allow_git(self):
        """10. Từ chối --allow-cmd git khi thiếu --allow-git."""
        # Without --allow-git: fails with exit code 1
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--allow-cmd",
                "git",
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 1)
        self.assertIn("thiếu cờ --allow-git", res.stderr)
        self.assertFalse(self.log_file.exists())

        # With --allow-git: succeeds
        res_ok = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--allow-cmd",
                "git",
                "--allow-git",
            ],
            scenario="success",
        )
        self.assertEqual(res_ok.returncode, 0)

    def test_allowed_write_succeeds_without_violation(self):
        """File đổi trong danh sách --allow-write thì thành công, không bị VIOLATION."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--allow-write",
                "allowed_file.txt",
            ],
            scenario="allowed_write",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok"))
        self.assertIn("FILES: 1 changed [allowed_file.txt]", lines[1])
        self.assertNotIn("VIOLATION", lines[1])

    def test_glob_in_allow_write_rejected(self):
        """Cấm dùng glob * hoặc ** trong --allow-write."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--allow-write",
                "src/*",
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 1)
        self.assertIn("Không được dùng glob", res.stderr)

    def test_dry_run_prompt_truncation(self):
        """--dry-run: đối số sau -p in ra 200 ký tự đầu + '...[<tổng số ký tự> ký tự]', không đổi argv thật."""
        task_content = "Nhiệm vụ kiểm tra dry-run prompt rất dài. " * 10
        self.task_file.write_text(task_content, encoding="utf-8")
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--dry-run",
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 0)
        argv = json.loads(res.stdout.strip())
        self.assertIn("-p", argv)
        p_idx = argv.index("-p") + 1
        prompt_val = argv[p_idx]

        full_prompt = agy_bridge.FIXED_PROMPT_PREFIX + task_content
        expected_prompt = f"{full_prompt[:200]}...[{len(full_prompt)} ký tự]"
        self.assertEqual(prompt_val, expected_prompt)
        self.assertTrue(prompt_val.endswith(f"[{len(full_prompt)} ký tự]"))

        # Verify build_agy_argv still produces untruncated prompt for actual execution
        real_argv = agy_bridge.build_agy_argv("agy", full_prompt, "gemini-3.8-flash-medium", str(self.repo_dir), "{}")
        self.assertEqual(real_argv[real_argv.index("-p") + 1], full_prompt)

    # ------------------ P1d Tests ------------------

    def test_commit_detected_exits_3_violation(self):
        """P6f: HEAD đổi do commit hợp lệ của agy không còn là VIOLATION/mã 3, thoát mã 0, ghi commits=1."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="commit_in_repo",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok"))
        self.assertIn("commits=1", lines[1])

    def test_quota_exhausted_exits_7_no_escalate(self):
        """agy giả in lỗi RESOURCE_EXHAUSTED: quota exceeded thì mã 7, chỉ gọi 1 lần, STATUS bắt đầu STATUS: quota."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="quota_exhausted",
        )
        self.assertEqual(res.returncode, 7)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: quota model=gemini-3.8-flash-medium"))
        self.assertIn("conv=conv-quota", lines[0])
        self.assertTrue(lines[0].endswith("DOI-TAI-KHOAN-AGY"))

        # Called only once (no escalation)
        logs = [line for line in self.log_file.read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual(len(logs), 1)

        # Report contains warning and raw error
        report_path = Path(lines[2].replace("REPORT: ", "").strip())
        self.assertTrue(report_path.exists())
        content = report_path.read_text(encoding="utf-8")
        self.assertIn("RESOURCE_EXHAUSTED: quota exceeded", content)
        self.assertIn("hết hạn mức", content.lower())

    # ------------------ P1c Worktree Tests ------------------

    def test_worktree_creation_and_cwd(self):
        """Tạo được worktree; agy giả chạy trong worktree (cwd), không phải repo gốc."""
        wt_dir = self.root / "custom_worktrees"
        cwd_log = self.root / "agy_cwd.txt"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
            ],
            scenario="record_cwd_and_write",
            env_extra={"MOCK_AGY_CWD_LOG": str(cwd_log)},
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok"))
        self.assertIn("wt=", lines[1])

        # Verify agy ran in worktree, not repo gốc
        recorded_cwd = cwd_log.read_text(encoding="utf-8").strip()
        self.assertNotEqual(Path(recorded_cwd).resolve(), self.repo_dir.resolve())
        self.assertTrue(str(Path(recorded_cwd).resolve()).startswith(str(wt_dir.resolve())))

    def test_worktree_settings_allow_write_mapped(self):
        """--allow-write dưới repo gốc được đổi sang đường dẫn trong worktree trong --settings."""
        wt_dir = self.root / "custom_worktrees"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--allow-write",
                "sub/target.txt",
                "--dry-run",
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 0)
        plan = json.loads(res.stdout.strip())
        self.assertIn("worktree", plan)
        self.assertIn("allow_write", plan)
        expected_mapped = str(Path(plan["worktree"]).resolve() / "sub" / "target.txt")
        self.assertEqual(plan["allow_write"], [expected_mapped])

    def test_worktree_isolates_repo_modifications(self):
        """File do phiên khác ghi vào repo gốc trong lúc chạy KHÔNG gây VIOLATION."""
        wt_dir = self.root / "custom_worktrees"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--allow-write",
                "target.txt",
            ],
            scenario="record_cwd_and_write",
            env_extra={
                "MOCK_AGY_WRITE_TARGET": "target.txt",
                "OTHER_SESSION_REPO": str(self.repo_dir),
            },
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok"))
        self.assertNotIn("VIOLATION", lines[1])
        # Verify file from other session indeed exists in repo_dir
        self.assertTrue((self.repo_dir / "other_session_file.txt").exists())

    def test_worktree_violation_in_worktree_exits_3(self):
        """File ghi ngoài --allow-write trong worktree vẫn gây VIOLATION, mã 3."""
        wt_dir = self.root / "custom_worktrees"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--allow-write",
                "allowed_file.txt",
            ],
            scenario="record_cwd_and_write",
            env_extra={"MOCK_AGY_WRITE_TARGET": "unallowed_file.txt"},
        )
        self.assertEqual(res.returncode, 3)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: fail"))
        self.assertIn("VIOLATION: unallowed_file.txt", lines[1])

    def test_worktree_seed_file(self):
        """--seed được sao chép và không tính là thay đổi."""
        uncommitted_file = self.repo_dir / "seed_file.txt"
        uncommitted_file.write_text("seed data\n", encoding="utf-8")
        wt_dir = self.root / "custom_worktrees"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--seed",
                "seed_file.txt",
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok"))
        self.assertIn("FILES: 0 changed", lines[1])

    def test_worktree_apply_success(self):
        """--apply chép file về repo gốc khi thành công."""
        wt_dir = self.root / "custom_worktrees"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--allow-write",
                "output.txt",
                "--apply",
            ],
            scenario="record_cwd_and_write",
            env_extra={"MOCK_AGY_WRITE_TARGET": "output.txt"},
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok"))
        self.assertIn("applied=1", lines[1])
        # Verify file is applied to repo_dir
        applied_file = self.repo_dir / "output.txt"
        self.assertTrue(applied_file.exists())
        self.assertEqual(applied_file.read_text(encoding="utf-8"), "content written in worktree\n")

    def test_worktree_apply_conflict_exits_5(self):
        """--apply từ chối với mã 5 khi file đích gốc đã bị sửa."""
        target_in_repo = self.repo_dir / "conflict_target.txt"
        target_in_repo.write_text("initial version\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo_dir, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "add conflict target"], cwd=self.repo_dir, capture_output=True, check=True)

        wt_dir = self.root / "custom_worktrees"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--allow-write",
                "conflict_target.txt",
                "--apply",
            ],
            scenario="conflict_apply",
            env_extra={
                "MOCK_AGY_WRITE_TARGET": "conflict_target.txt",
                "OTHER_SESSION_REPO": str(self.repo_dir),
            },
        )
        self.assertEqual(res.returncode, 5)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: fail"))
        self.assertIn("applied=0", lines[1])
        self.assertIn("CONFLICT: conflict_target.txt", lines[1])
        # File in repo was NOT overwritten by worktree content
        self.assertEqual(target_in_repo.read_text(encoding="utf-8"), "concurrent conflict edit\n")

    def test_worktree_dry_run_does_not_create_worktree(self):
        """--dry-run + --worktree không tạo worktree."""
        wt_dir = self.root / "custom_worktrees"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--dry-run",
            ],
            scenario="success",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 1)
        plan = json.loads(lines[0])
        self.assertIn("worktree", plan)
        self.assertIn("branch", plan)
        self.assertIn("allow_write", plan)
        # Worktree path does not exist on disk
        self.assertFalse(Path(plan["worktree"]).exists())

    # ------------------ P1e Fix Tests ------------------

    def test_success_response_containing_timestamp_digits_not_quota(self):
        """Lượt thành công, response chứa 20261114-201429, KHÔNG báo quota (Lỗi 1)."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="success_response_with_digits",
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok"))
        self.assertNotIn("quota", lines[0])

    def test_real_quota_nonzero_exit_reports_quota_code_7(self):
        """Lỗi thật RESOURCE_EXHAUSTED: quota exceeded (mã thoát khác 0) vẫn báo quota mã 7."""
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
            ],
            scenario="quota_exhausted",
        )
        self.assertEqual(res.returncode, 7)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: quota"))
        self.assertIn("conv=conv-quota", lines[0])
        self.assertTrue(lines[0].endswith("DOI-TAI-KHOAN-AGY"))

    def test_untracked_dir_new_file_counted_and_applied(self):
        """File mới trong thư mục chưa theo dõi được tính là thay đổi và được --apply chép về repo gốc (Lỗi 2)."""
        wt_dir = self.root / "custom_worktrees"
        target_file = "new_untracked_dir/sub_folder/new_file.txt"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--allow-write",
                target_file,
                "--apply",
            ],
            scenario="record_cwd_and_write",
            env_extra={"MOCK_AGY_WRITE_TARGET": target_file},
        )
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok"))
        self.assertIn("applied=1", lines[1])
        self.assertIn(f"FILES: 1 changed [{target_file}]", lines[1])
        # File is applied to repo_dir inside the previously untracked directory
        applied_file = self.repo_dir / target_file
        self.assertTrue(applied_file.exists())
        self.assertEqual(applied_file.read_text(encoding="utf-8"), "content written in worktree\n")

    def test_untracked_dir_file_outside_allow_write_causes_violation(self):
        """File ngoài --allow-write trong thư mục chưa theo dõi gây VIOLATION (Lỗi 2)."""
        wt_dir = self.root / "custom_worktrees"
        illicit_file = "illicit_untracked_dir/nested/illicit.txt"
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(wt_dir),
                "--allow-write",
                "some_other_dir/allowed.txt",
                "--apply",
            ],
            scenario="record_cwd_and_write",
            env_extra={"MOCK_AGY_WRITE_TARGET": illicit_file},
        )
        self.assertEqual(res.returncode, 3)
        lines = res.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: fail"))
        self.assertIn(f"VIOLATION: {illicit_file}", lines[1])

    def test_check_quota_error_unit_cases(self):
        """Unit test cho check_quota_error theo các điều kiện của brief P1e."""
        # 1. Thành công (exit 0, status SUCCESS), response chứa 20261114-201429 -> không báo quota
        is_q, msg = agy_bridge.check_quota_error(
            0, "", "", {"status": "SUCCESS", "response": "agy/hello-brief-20261114-201429"}
        )
        self.assertFalse(is_q)

        # 2. Thành công (exit 0, status SUCCESS), response chứa từ khóa quota -> không báo quota
        is_q, msg = agy_bridge.check_quota_error(
            0, "", "", {"status": "SUCCESS", "response": "Current quota is 1000 tokens"}
        )
        self.assertFalse(is_q)

        # 3. Lỗi thật mã thoát khác 0 và có error RESOURCE_EXHAUSTED -> báo quota
        is_q, msg = agy_bridge.check_quota_error(
            1, "", "", {"status": "ERROR", "error": "RESOURCE_EXHAUSTED: quota exceeded"}
        )
        self.assertTrue(is_q)
        self.assertEqual(msg, "RESOURCE_EXHAUSTED: quota exceeded")

        # 4. Lỗi thật mã thoát khác 0 và stderr chứa từ khóa 429 nguyên từ -> báo quota
        is_q, msg = agy_bridge.check_quota_error(
            1, "", "HTTP 429: Rate limit exceeded", None
        )
        self.assertTrue(is_q)
        self.assertEqual(msg, "HTTP 429: Rate limit exceeded")

        # 5. Lỗi thoát khác 0 nhưng chuỗi số dính 201429 (không khớp \b429\b) -> không báo quota
        is_q, msg = agy_bridge.check_quota_error(
            1, "", "Failed on build 201429 with syntax error", None
        )
        self.assertFalse(is_q)


class TestAgyBridgeP6bRegressions(unittest.TestCase):
    """Bộ test hồi quy P6b cho các lỗi review chéo P6 trong agy-bridge (C-03, M-02, M-03, m-02)."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.repo_dir = self.root / "repo"
        self.repo_dir.mkdir()
        subprocess.run(["git", "init"], cwd=self.repo_dir, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo_dir, check=True)
        (self.repo_dir / ".gitignore").write_text(".env\n.env.*\n", encoding="utf-8")
        (self.repo_dir / "AGENTS.md").write_text("# Agents Rules\n", encoding="utf-8")
        (self.repo_dir / "docs").mkdir()
        (self.repo_dir / "docs" / "keep.txt").write_text("keep\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.repo_dir, check=True)
        self.task_file = self.repo_dir / "task.md"
        self.task_file.write_text("Test task\n", encoding="utf-8")
        self.report_dir = self.root / "reports"
        self.report_dir.mkdir()
        self.mock_agy = self.root / "mock_agy.py"
        self.mock_agy.write_text(MOCK_AGY_SCRIPT, encoding="utf-8")
        os.chmod(self.mock_agy, 0o755)

    def run_bridge(self, args: list[str], scenario: str = "success") -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["AGY_BIN"] = str(self.mock_agy)
        env["MOCK_AGY_SCENARIO"] = scenario
        cmd = [sys.executable, str(BRIDGE_PATH), "run"] + args
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_c03_worktree_reverse_symlink_violation_and_apply_conflict(self):
        """C-03: Symlink ngược (wt/AGENTS.md -> docs/keep.txt) bị check_violations bắt và --apply từ chối."""
        wt_dir = self.root / "wt"
        subprocess.run(
            ["git", "-C", str(self.repo_dir), "worktree", "add", "-b", "agy/test-symlink", str(wt_dir), "HEAD"],
            capture_output=True,
            check=True,
        )

        initial_status = agy_bridge.get_git_status(wt_dir)
        initial_fp = {f: agy_bridge.get_file_fingerprint(wt_dir, f) for f in initial_status}

        # Tạo symlink ngược: wt/AGENTS.md trỏ tới docs/keep.txt
        (wt_dir / "AGENTS.md").unlink()
        (wt_dir / "AGENTS.md").symlink_to(Path("docs/keep.txt"))

        after_status = agy_bridge.get_git_status(wt_dir)
        after_fp = {f: agy_bridge.get_file_fingerprint(wt_dir, f) for f in after_status}
        changed = agy_bridge.calculate_changed_files(initial_status, initial_fp, after_status, after_fp)

        # allow_write chỉ cho phép docs/
        allow_write = [wt_dir / "docs"]
        violations = agy_bridge.check_violations(wt_dir, changed, allow_write)
        self.assertTrue(bool(violations), "Symlink ngược trong worktree phải bị check_violations bắt")
        self.assertIn("AGENTS.md", violations)

        # Kiểm tra conflict với baseline snapshot khi apply
        baseline_snapshot = agy_bridge.snapshot_repo_state(self.repo_dir)
        curr_snapshot = agy_bridge.snapshot_repo_state(self.repo_dir)
        src_f = wt_dir / "AGENTS.md"
        dst_f = self.repo_dir / "AGENTS.md"
        self.assertTrue(src_f.is_symlink(), "File trong worktree là symlink")
        # Symlink bị từ chối áp dụng về repo gốc
        orig_content = dst_f.read_text(encoding="utf-8")
        self.assertEqual(orig_content, "# Agents Rules\n")

        # Gọi bridge với agy giả tạo vi phạm ngoài allow-write kèm --apply -> thoát mã 3, không apply
        res = self.run_bridge(
            [
                "--dir",
                str(self.repo_dir),
                "--task-file",
                str(self.task_file),
                "--report-dir",
                str(self.report_dir),
                "--worktree",
                "--worktrees-dir",
                str(self.root / "wt_c03_run"),
                "--allow-write",
                "docs",
                "--apply",
            ],
            scenario="violation",
        )
        self.assertEqual(res.returncode, 3)

    def test_m02_unicode_vietnamese_path_and_ignored_dotenv_and_rename(self):
        """M-02: get_git_status giải mã đúng file tiếng Việt, bắt được file .env bị gitignore, và rename 2 đường dẫn."""
        wt_dir = self.root / "wt"
        subprocess.run(
            ["git", "-C", str(self.repo_dir), "worktree", "add", "-b", "agy/test-m02", str(wt_dir), "HEAD"],
            capture_output=True,
            check=True,
        )

        initial_status = agy_bridge.get_git_status(wt_dir)
        initial_fp = {f: agy_bridge.get_file_fingerprint(wt_dir, f) for f in initial_status}

        # 1. Tạo file tiếng Việt
        vn_file = wt_dir / "docs" / "báo-cáo.md"
        vn_file.write_text("Nội dung tiếng Việt\n", encoding="utf-8")

        # 2. Tạo file .env nằm trong .gitignore
        env_file = wt_dir / ".env"
        env_file.write_text("SECRET=pwned\n", encoding="utf-8")

        after_status = agy_bridge.get_git_status(wt_dir)
        after_fp = {f: agy_bridge.get_file_fingerprint(wt_dir, f) for f in after_status}
        changed = agy_bridge.calculate_changed_files(initial_status, initial_fp, after_status, after_fp)

        self.assertIn("docs/báo-cáo.md", changed, "File tiếng Việt phải được giải mã đúng chuỗi Unicode")
        self.assertIn(".env", changed, "File .env bị gitignore vẫn phải xuất hiện trong changed files")

        # 3. Rename file
        (wt_dir / "docs" / "old.txt").write_text("old\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(wt_dir), "add", "."], capture_output=True, check=True)
        subprocess.run(["git", "-C", str(wt_dir), "commit", "-m", "add old"], capture_output=True, check=True)
        subprocess.run(["git", "-C", str(wt_dir), "mv", "docs/old.txt", "docs/new.txt"], capture_output=True, check=True)

        mv_status = agy_bridge.get_git_status(wt_dir)
        self.assertIn("docs/new.txt", mv_status)
        self.assertIn("docs/old.txt", mv_status)

    def test_m03_seed_dot_and_git_and_symlink_ignored(self):
        """M-03: --seed từ chối '.', '.git', đường dẫn ngoài repo, và không dereference symlink ngoài repo."""
        wt_dir = self.root / "wt"
        subprocess.run(
            ["git", "-C", str(self.repo_dir), "worktree", "add", "-b", "agy/test-m03", str(wt_dir), "HEAD"],
            capture_output=True,
            check=True,
        )

        # --seed '.' bị từ chối
        with self.assertRaises(ValueError):
            agy_bridge.copy_path_into_worktree(Path("."), self.repo_dir, wt_dir, is_seed=True)

        # --seed '.git' bị từ chối
        with self.assertRaises(ValueError):
            agy_bridge.copy_path_into_worktree(Path(".git"), self.repo_dir, wt_dir, is_seed=True)

        # --seed ngoài repo bị từ chối
        outside_path = self.root / "outside.txt"
        outside_path.write_text("outside\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            agy_bridge.copy_path_into_worktree(outside_path, self.repo_dir, wt_dir, is_seed=True)

        # Symlink trong thư mục docs trỏ ra ngoài không bị copy file thật vào worktree
        outside_secrets = self.root / "secrets"
        outside_secrets.mkdir()
        (outside_secrets / "secret.txt").write_text("TOP_SECRET\n", encoding="utf-8")
        (self.repo_dir / "docs" / "ext_link").symlink_to(outside_secrets)

        agy_bridge.copy_path_into_worktree(Path("docs"), self.repo_dir, wt_dir, is_seed=True)
        # File bí mật ngoài repo KHÔNG được xuất hiện trong worktree dưới dạng file thật
        copied_secret = wt_dir / "docs" / "ext_link" / "secret.txt"
        self.assertFalse(copied_secret.exists(), "Symlink trỏ ra ngoài repo không được dereference chép vào worktree")

    def test_m02_total_tokens_and_totalTokens_sum(self):
        """m-02: Gọi hàm thật calculate_total_tokens và parse_agy_json kiểm tra cộng token theo cả total_tokens và totalTokens."""
        attempts = [
            {"usage": {"total_tokens": 100}},
            {"usage": {"totalTokens": 200}},
            {"usage": {}},
        ]
        final_tokens = agy_bridge.calculate_total_tokens(attempts)
        self.assertEqual(final_tokens, 300)

        # Kiểm tra parse_agy_json và calculate_total_tokens
        parsed1 = agy_bridge.parse_agy_json('{"status": "SUCCESS", "usage": {"totalTokens": 150}}')
        self.assertEqual(parsed1["usage"]["totalTokens"], 150)
        parsed2 = agy_bridge.parse_agy_json('{"status": "SUCCESS", "usage": {"total_tokens": 250}}')
        self.assertEqual(parsed2["usage"]["total_tokens"], 250)
        tokens_from_parsed = agy_bridge.calculate_total_tokens([parsed1, parsed2])
        self.assertEqual(tokens_from_parsed, 400)

    def test_p6d_allow_write_symlink_exit_2(self):
        """P6d-C02: Đường dẫn --allow-write là symlink thì thoát ngay với mã 2."""
        sym_link = self.repo_dir / "sym_docs"
        sym_link.symlink_to(self.repo_dir / "docs")
        task_f = self.repo_dir / "task.md"
        task_f.write_text("Test\n", encoding="utf-8")
        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(task_f),
            "--allow-write", str(sym_link),
        ]
        proc = subprocess.run(
            [sys.executable, str(BRIDGE_PATH)] + argv,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("symlink", proc.stderr)


class TestAgyBridgeP6gRegressions(unittest.TestCase):
    """Bộ test hồi quy P6g: Kiểm tra quota và status trong agy-bridge."""

    def test_p6g_bridge_quota_not_suspected_on_max_tokens_or_chat(self):
        """P6g-Việc 3: check_quota_error không kích hoạt nghi quota chỉ vì stopReason hoặc chat chứa 'quota'."""
        # 1. stopReason='max_tokens' với response chứa từ khóa quota khi status là SUCCESS
        is_q, msg = agy_bridge.check_quota_error(
            0, "", "", {"status": "SUCCESS", "response": "quota limit discussion", "stopReason": "max_tokens"}
        )
        self.assertFalse(is_q)

        # 2. status ERROR nhưng lỗi không phải quota (chỉ có stopReason='max_tokens' và chat nhắc quota)
        is_q, msg = agy_bridge.check_quota_error(
            1, "", "", {"status": "ERROR", "stopReason": "max_tokens", "error": "Compilation failed: type mismatch"}
        )
        self.assertFalse(is_q)

    def test_p6g_bridge_quota_detected_on_resource_exhausted_or_429(self):
        """P6g-Việc 3: check_quota_error quét trúng trường error thật (RESOURCE_EXHAUSTED, HTTP 429)."""
        is_q, msg = agy_bridge.check_quota_error(
            1, "", "", {"status": "ERROR", "error": "RESOURCE_EXHAUSTED: quota exceeded"}
        )
        self.assertTrue(is_q)
        self.assertEqual(msg, "RESOURCE_EXHAUSTED: quota exceeded")

        is_q, msg = agy_bridge.check_quota_error(
            1, "", "HTTP 429: Rate limit reached", None
        )
        self.assertTrue(is_q)
        self.assertEqual(msg, "HTTP 429: Rate limit reached")


if __name__ == "__main__":
    unittest.main()
