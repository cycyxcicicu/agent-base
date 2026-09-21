"""
agent_core/core/sandbox.py
Process Execution Environment & Sanitized Runner.
Enforces timeout boundaries, sanitized environment variables (stripping sensitive API keys/tokens),
and structured execution result streaming (note: runs locally as a sanitized sub-process, not a hardware MicroVM).
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class ExecutionResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    timed_out: bool = False
    artifacts: List[str] = field(default_factory=list)

    @property
    def is_success(self) -> bool:
        return self.exit_code == 0 and not self.timed_out

class SandboxRunner:
    """Executes commands and code snippets in an isolated working directory with timeout gates."""

    DEFAULT_TIMEOUT_SEC = 30.0

    def __init__(self, sandbox_dir: Optional[Path] = None, timeout_sec: float = DEFAULT_TIMEOUT_SEC):
        self.sandbox_dir = sandbox_dir or Path.cwd()
        self.timeout_sec = timeout_sec

    BLOCKED_ENV_PATTERNS = [
        "secret", "private_key", "password", "passwd", "token", "api_key", "apikey",
        "auth", "bearer", "credential", "jwt", "access_key", "client_secret",
        "database_url", "db_password", "db_pass", "conn_str", "cookie", "session_id",
        "secure_1psid", "openai", "anthropic", "github_token", "gh_token", "gemini"
    ]

    def sanitize_env(
        self,
        base_env: Optional[Dict[str, str]] = None,
        extra_blocked: Optional[List[str]] = None,
        allow_list: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Strip dangerous or secret environment variables before running in sandbox."""
        env = dict(base_env or os.environ)

        # If allow_list is provided, keep only allowed keys
        if allow_list is not None:
            allow_set = {k.upper() for k in allow_list}
            return {k: v for k, v in env.items() if k.upper() in allow_set}

        patterns = list(self.BLOCKED_ENV_PATTERNS)
        if extra_blocked:
            patterns.extend(extra_blocked)

        # Block leakage of critical secrets to untrusted child processes
        secret_keys = [k for k in env if any(p in k.lower() for p in patterns)]
        for k in secret_keys:
            env.pop(k, None)
        return env

    def run_command(self, cmd_args: List[str], cwd: Optional[Path] = None, timeout: Optional[float] = None) -> ExecutionResult:
        """Executes a command safely with list args (preventing shell injection) and timeout enforcement."""
        working_dir = cwd or self.sandbox_dir
        effective_timeout = timeout or self.timeout_sec
        clean_env = self.sanitize_env()

        start_time = time.perf_counter()
        try:
            proc = subprocess.run(
                cmd_args,
                cwd=str(working_dir),
                env=clean_env,
                capture_output=True,
                text=True,
                timeout=effective_timeout
            )
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                command=" ".join(cmd_args),
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                duration_ms=duration_ms,
                timed_out=False
            )
        except subprocess.TimeoutExpired as e:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                command=" ".join(cmd_args),
                exit_code=-1,
                stdout=e.stdout or "",
                stderr=(e.stderr or "") + f"\nProcess timed out after {effective_timeout}s.",
                duration_ms=duration_ms,
                timed_out=True
            )
        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                command=" ".join(cmd_args),
                exit_code=-1,
                stdout="",
                stderr=str(e),
                duration_ms=duration_ms,
                timed_out=False
            )

    def run_python_code(self, code: str, timeout: Optional[float] = None) -> ExecutionResult:
        """Runs a python snippet in isolated execution."""
        return self.run_command([sys.executable, "-c", code], timeout=timeout)
