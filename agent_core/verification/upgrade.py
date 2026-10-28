"""agent_core.verification.upgrade

Recipe kiểm chứng nâng cấp (Upgrade Verification) trên fixture cô lập.
Kiểm tra 4 kịch bản: giữ tùy chỉnh, phát hiện xung đột, an toàn dry-run, chạy lại idempotent.
Tuân thủ đặc tả T-11 §5.
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


def _compute_dir_hash(directory: Path) -> str:
    """Tính băm tổng hợp của toàn bộ các file trong thư mục để kiểm tra byte mutation."""
    hasher = hashlib.sha256()
    for root, _, files in sorted(os.walk(directory)):
        for f in sorted(files):
            p = Path(root) / f
            hasher.update(p.relative_to(directory).as_posix().encode("utf-8"))
            try:
                hasher.update(p.read_bytes())
            except Exception:
                pass
    return hasher.hexdigest()


def run_upgrade_verification(evidence_root: Path | str, keep_fixture: bool = False) -> Path:
    start_time = datetime.now(timezone.utc)
    run_id = f"upgrade-{start_time.strftime('%Y%m%d-%H%M%S')}"
    ev_root = Path(evidence_root).resolve()
    bundle_evidence_dir = ev_root / run_id
    bundle_evidence_dir.mkdir(parents=True, exist_ok=True)

    # 1. Khởi tạo fixture cô lập
    fixture_dir = Path(tempfile.mkdtemp(prefix="agy_fixture_upg_"))
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

    # 2. Bootstrap ban đầu (Baseline)
    boot_script = ROOT / "scripts" / "bootstrap-project.py"
    cmd_boot = [sys.executable, str(boot_script), "--target", str(fixture_dir), "--mode", "git"]
    t0 = time.time()
    res_boot = subprocess.run(cmd_boot, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration_boot = int((time.time() - t0) * 1000)

    command_records.append(
        CommandRecord(
            sequence=1,
            argv=cmd_boot,
            cwd_rel=".",
            timeout_sec=60,
            exit_code=res_boot.returncode,
            duration_ms=duration_boot,
            stdout_sha256=hashlib.sha256(res_boot.stdout.encode("utf-8")).hexdigest(),
            stderr_sha256=hashlib.sha256(res_boot.stderr.encode("utf-8")).hexdigest(),
        )
    )

    # 3. Tạo các tùy chỉnh và xung đột trên dự án fixture
    # Kịch bản 1 (Tùy chỉnh riêng): Sửa tệp tasks/quick-log.md
    custom_file = fixture_dir / "tasks" / "quick-log.md"
    custom_content = "# Nhật ký việc nhỏ\n\n| 2026-10-28 | T-USER | dev | Custom local fix | src/my.py | a1b2c3 |\n"
    custom_file.write_text(custom_content, encoding="utf-8")
    custom_sha_before = hashlib.sha256(custom_content.encode("utf-8")).hexdigest()

    # Kịch bản 2 (Xung đột/Khác biệt): Sửa một file framework thuộc tracked manifest
    agents_file = fixture_dir / "AGENTS.md"
    if agents_file.is_file():
        conflict_content = agents_file.read_text(encoding="utf-8") + "\n# custom conflict line\n"
        agents_file.write_text(conflict_content, encoding="utf-8")

    trace_records.append(
        TraceRecord(
            sequence=seq_counter,
            actor="dev",
            action="inject_customization_and_conflict",
            target=str(fixture_dir),
            result="modified",
            timestamp=datetime.now(timezone.utc).isoformat(),
            capture="observed",
        )
    )
    seq_counter += 1

    # 4. Kịch bản 3: Dry-run nâng cấp (không làm đổi byte nào)
    hash_before_dry = _compute_dir_hash(fixture_dir)
    cmd_dry = [sys.executable, str(boot_script), "--target", str(fixture_dir), "--mode", "git", "--dry-run"]
    t0 = time.time()
    res_dry = subprocess.run(cmd_dry, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration_dry = int((time.time() - t0) * 1000)
    hash_after_dry = _compute_dir_hash(fixture_dir)

    a_dry_pass = (hash_before_dry == hash_after_dry) and (res_dry.returncode == 0)
    assertion_records.append(
        AssertionRecord(
            id="assert-dry-run-safe",
            expected="Dry-run không làm biến đổi bất kỳ byte nào trên fixture",
            observed=f"Hash trước={hash_before_dry[:8]}, sau={hash_after_dry[:8]}",
            passed=a_dry_pass,
        )
    )

    command_records.append(
        CommandRecord(
            sequence=2,
            argv=cmd_dry,
            cwd_rel=".",
            timeout_sec=60,
            exit_code=res_dry.returncode,
            duration_ms=duration_dry,
            stdout_sha256=hashlib.sha256(res_dry.stdout.encode("utf-8")).hexdigest(),
            stderr_sha256=hashlib.sha256(res_dry.stderr.encode("utf-8")).hexdigest(),
        )
    )

    # 5. Kịch bản 2: Chạy so sánh bằng script đã copy sang fixture
    diff_script = fixture_dir / "scripts" / "agent-base-diff.py"
    cmd_diff = [sys.executable, str(diff_script), "--base", str(ROOT)]
    t0 = time.time()
    res_diff = subprocess.run(cmd_diff, cwd=str(fixture_dir), capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration_diff = int((time.time() - t0) * 1000)

    # Báo cáo xung đột hoặc khác biệt
    diff_stdout = res_diff.stdout
    a_conflict_reported = ("AGENTS.md" in diff_stdout or "cần xem" in diff_stdout or "đã sửa" in diff_stdout)
    assertion_records.append(
        AssertionRecord(
            id="assert-report-conflicts",
            expected="Phát hiện và báo cáo khác biệt/xung đột giữa dự án và agent-base",
            observed="Đã phát hiện và liệt kê khác biệt" if a_conflict_reported else "Không phát hiện khác biệt",
            passed=a_conflict_reported,
        )
    )

    command_records.append(
        CommandRecord(
            sequence=3,
            argv=cmd_diff,
            cwd_rel=str(fixture_dir),
            timeout_sec=60,
            exit_code=res_diff.returncode,
            duration_ms=duration_diff,
            stdout_sha256=hashlib.sha256(res_diff.stdout.encode("utf-8")).hexdigest(),
            stderr_sha256=hashlib.sha256(res_diff.stderr.encode("utf-8")).hexdigest(),
        )
    )

    # 6. Kịch bản 1: Nâng cấp không ghi đè tùy chỉnh của người dùng (bootstrap rerun)
    cmd_upgrade = [sys.executable, str(boot_script), "--target", str(fixture_dir), "--mode", "git"]
    t0 = time.time()
    res_upg = subprocess.run(cmd_upgrade, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration_upg = int((time.time() - t0) * 1000)

    custom_content_after = custom_file.read_text(encoding="utf-8")
    custom_sha_after = hashlib.sha256(custom_content_after.encode("utf-8")).hexdigest()
    a_preserve_pass = (custom_sha_before == custom_sha_after)
    assertion_records.append(
        AssertionRecord(
            id="assert-preserve-customization",
            expected="Tùy chỉnh riêng của dự án (quick-log.md) được bảo toàn nguyên vẹn",
            observed="Bảo toàn thành công" if a_preserve_pass else "Bị ghi đè",
            passed=a_preserve_pass,
        )
    )

    # 7. Kịch bản 4: Idempotent rerun
    hash_run1 = _compute_dir_hash(fixture_dir)
    subprocess.run(cmd_upgrade, capture_output=True, text=True, encoding="utf-8", errors="replace")
    hash_run2 = _compute_dir_hash(fixture_dir)
    a_idempotent_pass = (hash_run1 == hash_run2)
    assertion_records.append(
        AssertionRecord(
            id="assert-idempotent-rerun",
            expected="Chạy lại nhiều lần sinh ra cùng cấu trúc và nội dung byte",
            observed="Khớp 100% băm cấu trúc" if a_idempotent_pass else "Có biến đổi giữa 2 lần chạy",
            passed=a_idempotent_pass,
        )
    )

    # Lưu artifact diff stdout
    diff_art_file = bundle_evidence_dir / "upgrade_diff_output.txt"
    diff_bytes = diff_stdout.encode("utf-8")
    diff_art_file.write_bytes(diff_bytes)
    artifact_records.append(
        ArtifactRecord(
            path_rel="upgrade_diff_output.txt",
            sha256=hashlib.sha256(diff_bytes).hexdigest(),
            byte_count=len(diff_bytes),
            media_type="text/plain",
        )
    )

    all_assertions_passed = (
        a_dry_pass and a_conflict_reported and a_preserve_pass and a_idempotent_pass
    )
    final_result = "pass" if all_assertions_passed else "fail"

    # 8. Dọn dẹp fixture
    cleanup_errors: List[str] = []
    if not keep_fixture:
        try:
            shutil.rmtree(fixture_dir)
        except Exception as e:
            cleanup_errors.append(f"Lỗi khi dọn fixture: {str(e)}")

    end_time = datetime.now(timezone.utc)

    bundle = ProofBundle(
        schema_version=1,
        run_id=run_id,
        scenario_id="upgrade-flow",
        phase="final",
        started_at=start_time.isoformat(),
        ended_at=end_time.isoformat(),
        result=final_result,
        repo_revision=os.environ.get("GITHUB_SHA", "local-dev-commit"),
        dirty_input_manifest=[],
        input_digest=hashlib.sha256(b"agent-base-upgrade-recipe-v1").hexdigest(),
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
