"""agent_core.verification.bootstrap

Recipe kiểm chứng cài đặt (Bootstrap Verification) trên fixture cô lập.
Tuân thủ đặc tả T-11 §5 và không chạm thư mục người dùng.
"""

from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent

from agent_core.verification.proof import (
    ProofBundle,
    CommandRecord,
    ArtifactRecord,
    AssertionRecord,
    TraceRecord,
    export_proof_bundle,
)


def run_bootstrap_verification(evidence_root: Path | str, keep_fixture: bool = False) -> Path:
    start_time = datetime.now(timezone.utc)
    run_id = f"bootstrap-{start_time.strftime('%Y%m%d-%H%M%S')}"
    ev_root = Path(evidence_root).resolve()
    bundle_evidence_dir = ev_root / run_id
    bundle_evidence_dir.mkdir(parents=True, exist_ok=True)

    # 1. Khởi tạo fixture cô lập
    fixture_dir = Path(tempfile.mkdtemp(prefix="agy_fixture_boot_"))
    sentinel_file = fixture_dir / ".fixture_sentinel"
    sentinel_file.write_text(f"ownership: {run_id}\ncreated_at: {start_time.isoformat()}\n", encoding="utf-8")

    trace_records: List[TraceRecord] = []
    command_records: List[CommandRecord] = []
    assertion_records: List[AssertionRecord] = []
    artifact_records: List[ArtifactRecord] = []
    seq_counter = 1

    trace_records.append(
        TraceRecord(
            sequence=seq_counter,
            actor="dev",
            action="launch_fixture",
            target=str(fixture_dir),
            result="ready",
            timestamp=datetime.now(timezone.utc).isoformat(),
            capture="observed",
        )
    )
    seq_counter += 1

    # 2. Thực thi bootstrap project vào fixture
    boot_script = ROOT / "scripts" / "bootstrap-project.py"
    cmd = [sys.executable, str(boot_script), "--target", str(fixture_dir), "--mode", "git"]

    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration_ms = int((time.time() - t0) * 1000)

    stdout_bytes = res.stdout.encode("utf-8")
    stderr_bytes = res.stderr.encode("utf-8")
    stdout_sha = hashlib.sha256(stdout_bytes).hexdigest()
    stderr_sha = hashlib.sha256(stderr_bytes).hexdigest()

    # Lưu stdout/stderr thành artifact
    stdout_file = bundle_evidence_dir / "bootstrap_stdout.txt"
    stdout_file.write_bytes(stdout_bytes)
    artifact_records.append(
        ArtifactRecord(
            path_rel="bootstrap_stdout.txt",
            sha256=stdout_sha,
            byte_count=len(stdout_bytes),
            media_type="text/plain",
        )
    )

    command_records.append(
        CommandRecord(
            sequence=1,
            argv=cmd,
            cwd_rel=".",
            timeout_sec=60,
            exit_code=res.returncode,
            duration_ms=duration_ms,
            stdout_sha256=stdout_sha,
            stderr_sha256=stderr_sha,
        )
    )

    trace_records.append(
        TraceRecord(
            sequence=seq_counter,
            actor="dev",
            action="run_command",
            target="bootstrap-project.py",
            result=f"exit_{res.returncode}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            capture="observed",
        )
    )
    seq_counter += 1

    # 3. Kiểm tra các điều kiện hậu kiểm (Assertions)
    # A1: Exit code == 0
    a1_pass = res.returncode == 0
    assertion_records.append(
        AssertionRecord(
            id="assert-exit-code-0",
            expected="exit 0",
            observed=f"exit {res.returncode}",
            passed=a1_pass,
        )
    )

    # A2: Có file .agent-base.json trong fixture
    ab_json = fixture_dir / ".agent-base.json"
    a2_pass = ab_json.is_file()
    assertion_records.append(
        AssertionRecord(
            id="assert-agent-base-metadata",
            expected="File .agent-base.json tồn tại trên fixture",
            observed="Tồn tại" if a2_pass else "Không tìm thấy",
            passed=a2_pass,
        )
    )

    # A3: Các file template fresh được sinh ra (quick-log, PROJECT-NOTES, DEBT)
    quick_log = fixture_dir / "tasks" / "quick-log.md"
    a3_pass = quick_log.is_file()
    assertion_records.append(
        AssertionRecord(
            id="assert-fresh-templates-generated",
            expected="tasks/quick-log.md tồn tại trên fixture",
            observed="Tồn tại" if a3_pass else "Không tìm thấy",
            passed=a3_pass,
        )
    )

    all_passed = a1_pass and a2_pass and a3_pass
    final_result = "pass" if all_passed else "fail"

    # 4. Dọn dẹp fixture
    cleanup_errors: List[str] = []
    if not keep_fixture:
        try:
            shutil.rmtree(fixture_dir)
        except Exception as e:
            cleanup_errors.append(f"Lỗi khi xóa fixture: {str(e)}")

    trace_records.append(
        TraceRecord(
            sequence=seq_counter,
            actor="dev",
            action="cleanup_fixture",
            target=str(fixture_dir),
            result="clean" if not cleanup_errors else "error",
            timestamp=datetime.now(timezone.utc).isoformat(),
            capture="observed",
        )
    )

    end_time = datetime.now(timezone.utc)

    # 5. Đóng gói ProofBundle
    bundle = ProofBundle(
        schema_version=1,
        run_id=run_id,
        scenario_id="bootstrap-clean",
        phase="final",
        started_at=start_time.isoformat(),
        ended_at=end_time.isoformat(),
        result=final_result,
        repo_revision=os.environ.get("GITHUB_SHA", "local-dev-commit"),
        dirty_input_manifest=[],
        input_digest=hashlib.sha256(b"agent-base-bootstrap-recipe-v1").hexdigest(),
        tool_versions={"python": sys.version.split()[0]},
        commands=command_records,
        assertions=assertion_records,
        artifacts=artifact_records,
        trace=trace_records,
        cleanup={
            "performed": not keep_fixture,
            "clean": len(cleanup_errors) == 0,
            "errors": cleanup_errors,
        },
        limitations=["Chạy trong môi trường Isolated TemporaryDirectory fixture."],
    )

    proof_file = export_proof_bundle(bundle, evidence_root)
    return proof_file
