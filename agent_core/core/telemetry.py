"""
The Iron Law & Proof-of-Execution Telemetry.
Học hỏi từ: superpowers (The Iron Law: Không có log bằng chứng thực tế thì chưa được coi là xong).
"""

import subprocess
import shlex
import time
from typing import Dict, Any, Optional, List


class ProofValidator:
    """Xác thực bằng chứng thực thi lệnh hệ thống."""

    @staticmethod
    def execute_and_prove(command: str, cwd: Optional[str] = None, timeout: float = 60.0) -> Dict[str, Any]:
        """
        Thực thi lệnh và sinh bằng chứng kiểm thử (Proof of Execution).
        Chỉ trả về passed = True khi lệnh kết thúc với exit_code == 0.
        """
        start_time = time.time()
        try:
            is_str = isinstance(command, str)
            res = subprocess.run(
                command,
                shell=is_str,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout
            )
            duration = round(time.time() - start_time, 3)
            return {
                "command": command,
                "exit_code": res.returncode,
                "stdout": res.stdout.strip(),
                "stderr": res.stderr.strip(),
                "duration_seconds": duration,
                "passed": res.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Hết thời gian chờ {timeout}s",
                "duration_seconds": round(time.time() - start_time, 3),
                "passed": False
            }
        except Exception as e:
            return {
                "command": command,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "duration_seconds": round(time.time() - start_time, 3),
                "passed": False
            }


def verify_iron_law(proof: Dict[str, Any]) -> bool:
    """Quy luật thép: Kiểm tra xem lệnh có bằng chứng hoàn thành hợp lệ không."""
    return bool(proof and proof.get("exit_code") == 0 and proof.get("passed") is True)
