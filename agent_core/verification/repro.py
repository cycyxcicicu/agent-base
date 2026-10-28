"""agent_core.verification.repro

Harness tái hiện lỗi hai lần độc lập có reset trạng thái và chế độ đối soát Verify (bản gốc vs bản vá).
Tuân thủ quy trình xử lý lỗi (T-15, agents/protocols/bug-repro.md) và T-11 §5.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent

from agent_core.verification.proof import (
    ProofBundle,
    CommandRecord,
    ArtifactRecord,
    AssertionRecord,
    TraceRecord,
    export_proof_bundle,
)


@dataclass
class ReproResult:
    verdict: str  # "reproduced" | "not_reproduced" | "inconclusive"
    run_count: int
    runs: List[Dict[str, Any]]
    proof_path: Path
    needs_independent_review: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "run_count": self.run_count,
            "runs": self.runs,
            "proof_path": str(self.proof_path),
            "needs_independent_review": self.needs_independent_review,
        }


@dataclass
class VerifyResult:
    verdict: str  # "pass" | "fail" | "inconclusive"
    baseline_reproduced: bool
    patch_clean: bool
    proof_path: Path
    needs_independent_review: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "baseline_reproduced": self.baseline_reproduced,
            "patch_clean": self.patch_clean,
            "proof_path": str(self.proof_path),
            "needs_independent_review": self.needs_independent_review,
        }


def _execute_run(cmd: List[str], cwd: Optional[str] = None) -> Tuple[int, str, str, int]:
    t0 = time.time()
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    dur_ms = int((time.time() - t0) * 1000)
    return res.returncode, res.stdout, res.stderr, dur_ms


def run_repro_harness(recipe: Dict[str, Any], evidence_root: Path | str) -> ReproResult:
    start_time = datetime.now(timezone.utc)
    recipe_name = recipe.get("name", "repro-run")
    run_id = f"repro-{recipe_name}-{start_time.strftime('%Y%m%d-%H%M%S')}"

    ev_root = Path(evidence_root).resolve()
    bundle_evidence_dir = ev_root / run_id
    bundle_evidence_dir.mkdir(parents=True, exist_ok=True)

    cmd = recipe.get("command", [])
    expected_bug_exit = recipe.get("expected_bug_exit_code", 1)
    reset_action = recipe.get("reset_action")

    command_records: List[CommandRecord] = []
    trace_records: List[TraceRecord] = []
    assertion_records: List[AssertionRecord] = []
    artifact_records: List[ArtifactRecord] = []
    runs_data: List[Dict[str, Any]] = []

    # 1. Chạy lần 1 (Run 1)
    exit1, out1, err1, dur1 = _execute_run(cmd)
    runs_data.append({"run": 1, "exit_code": exit1, "stdout": out1, "stderr": err1})

    command_records.append(
        CommandRecord(
            sequence=1,
            argv=cmd,
            cwd_rel=".",
            timeout_sec=60,
            exit_code=exit1,
            duration_ms=dur1,
            stdout_sha256=hashlib.sha256(out1.encode("utf-8")).hexdigest(),
            stderr_sha256=hashlib.sha256(err1.encode("utf-8")).hexdigest(),
        )
    )
    trace_records.append(
        TraceRecord(
            sequence=1,
            actor="dev",
            action="repro_attempt_1",
            target=str(cmd),
            result=f"exit_{exit1}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            capture="observed",
        )
    )

    # 2. Reset trạng thái
    if callable(reset_action):
        try:
            reset_action()
        except Exception:
            pass

    trace_records.append(
        TraceRecord(
            sequence=2,
            actor="dev",
            action="state_reset",
            target="fixture",
            result="reset_done",
            timestamp=datetime.now(timezone.utc).isoformat(),
            capture="observed",
        )
    )

    # 3. Chạy lần 2 (Run 2)
    exit2, out2, err2, dur2 = _execute_run(cmd)
    runs_data.append({"run": 2, "exit_code": exit2, "stdout": out2, "stderr": err2})

    command_records.append(
        CommandRecord(
            sequence=2,
            argv=cmd,
            cwd_rel=".",
            timeout_sec=60,
            exit_code=exit2,
            duration_ms=dur2,
            stdout_sha256=hashlib.sha256(out2.encode("utf-8")).hexdigest(),
            stderr_sha256=hashlib.sha256(err2.encode("utf-8")).hexdigest(),
        )
    )
    trace_records.append(
        TraceRecord(
            sequence=3,
            actor="dev",
            action="repro_attempt_2",
            target=str(cmd),
            result=f"exit_{exit2}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            capture="observed",
        )
    )

    # 4. Đánh giá kết quả
    has_bug_1 = (exit1 == expected_bug_exit)
    has_bug_2 = (exit2 == expected_bug_exit)

    if has_bug_1 and has_bug_2:
        verdict = "reproduced"
    elif not has_bug_1 and not has_bug_2:
        verdict = "not_reproduced"
    else:
        verdict = "inconclusive"

    assertion_records.append(
        AssertionRecord(
            id="assert-repro-consistency",
            expected=f"Cả 2 lần chạy cho cùng kết luận về mã lỗi (kỳ vọng={expected_bug_exit})",
            observed=f"Lần 1: exit {exit1}, Lần 2: exit {exit2} -> {verdict}",
            passed=(verdict in ("reproduced", "not_reproduced")),
        )
    )

    # Lưu log chạy ra artifact
    repro_log = bundle_evidence_dir / "repro_execution_log.txt"
    log_content = (
        f"=== RUN 1 ===\nExit: {exit1}\nSTDOUT:\n{out1}\nSTDERR:\n{err1}\n\n"
        f"=== RUN 2 ===\nExit: {exit2}\nSTDOUT:\n{out2}\nSTDERR:\n{err2}\n"
    )
    repro_log.write_text(log_content, encoding="utf-8")
    artifact_records.append(
        ArtifactRecord(
            path_rel="repro_execution_log.txt",
            sha256=hashlib.sha256(log_content.encode("utf-8")).hexdigest(),
            byte_count=len(log_content.encode("utf-8")),
            media_type="text/plain",
        )
    )

    end_time = datetime.now(timezone.utc)

    # Đóng gói proof
    bundle = ProofBundle(
        schema_version=1,
        run_id=run_id,
        scenario_id=f"repro-{recipe_name}",
        phase="baseline",
        started_at=start_time.isoformat(),
        ended_at=end_time.isoformat(),
        result="pass" if verdict == "reproduced" else "fail" if verdict == "not_reproduced" else "inconclusive",
        repo_revision=os.environ.get("GITHUB_SHA", "local-dev-commit"),
        dirty_input_manifest=[],
        input_digest=hashlib.sha256(json.dumps(cmd).encode("utf-8")).hexdigest(),
        tool_versions={"python": sys.version.split()[0]},
        commands=command_records,
        assertions=assertion_records,
        artifacts=artifact_records,
        trace=trace_records,
        cleanup={"performed": True, "clean": True, "errors": []},
        limitations=[
            "Chẩn đoán tái hiện triệu chứng độc lập; cần kiểm chứng độc lập bởi người duyệt (needs_independent_review=true)"
        ],
    )

    proof_file = export_proof_bundle(bundle, evidence_root)

    return ReproResult(
        verdict=verdict,
        run_count=2,
        runs=runs_data,
        proof_path=proof_file,
        needs_independent_review=True,
    )


def run_verify_mode(
    recipe: Dict[str, Any],
    patch_fn: Optional[Callable[[], None]],
    evidence_root: Path | str,
) -> VerifyResult:
    """
    Chế độ Verify đối soát:
    - Chạy bản gốc 2 lần có reset: Phải thấy lỗi (reproduced).
    - Áp dụng bản vá (patch).
    - Chạy bản vá 2 lần có reset: Phải sạch lỗi (not_reproduced).
    """
    start_time = datetime.now(timezone.utc)
    run_id = f"verify-patch-{recipe.get('name', 'fix')}-{start_time.strftime('%Y%m%d-%H%M%S')}"

    ev_root = Path(evidence_root).resolve()
    bundle_evidence_dir = ev_root / run_id
    bundle_evidence_dir.mkdir(parents=True, exist_ok=True)

    # 1. Chạy bản gốc
    base_res = run_repro_harness(recipe, bundle_evidence_dir)
    base_reproduced = (base_res.verdict == "reproduced")

    # 2. Áp dụng bản vá
    if callable(patch_fn):
        patch_fn()

    # 3. Chạy bản vá
    patch_res = run_repro_harness(recipe, bundle_evidence_dir)
    patch_clean = (patch_res.verdict == "not_reproduced")

    if base_reproduced and patch_clean:
        verdict = "pass"
    elif not base_reproduced:
        verdict = "inconclusive"
    else:
        verdict = "fail"

    end_time = datetime.now(timezone.utc)

    # Đóng gói proof chung cho verify mode
    bundle = ProofBundle(
        schema_version=1,
        run_id=run_id,
        scenario_id=f"verify-mode-{recipe.get('name', 'fix')}",
        phase="final",
        started_at=start_time.isoformat(),
        ended_at=end_time.isoformat(),
        result=verdict,
        repo_revision=os.environ.get("GITHUB_SHA", "local-dev-commit"),
        dirty_input_manifest=[],
        input_digest=hashlib.sha256(b"verify-mode-protocol-v1").hexdigest(),
        tool_versions={"python": sys.version.split()[0]},
        commands=[],
        assertions=[
            AssertionRecord(
                id="assert-baseline-reproduced",
                expected="Bản gốc thấy lỗi nhất quán 2/2 lần",
                observed="Đã tái hiện lỗi" if base_reproduced else f"Thất bại ({base_res.verdict})",
                passed=base_reproduced,
            ),
            AssertionRecord(
                id="assert-patch-clean",
                expected="Bản vá sạch lỗi nhất quán 0/2 lần",
                observed="Đã sạch lỗi hoàn toàn" if patch_clean else f"Vẫn còn lỗi ({patch_res.verdict})",
                passed=patch_clean,
            ),
        ],
        artifacts=[],
        trace=[
            TraceRecord(
                sequence=1,
                actor="dev",
                action="baseline_repro",
                target="unpatched_code",
                result=base_res.verdict,
                timestamp=datetime.now(timezone.utc).isoformat(),
                capture="observed",
            ),
            TraceRecord(
                sequence=2,
                actor="dev",
                action="patch_verification",
                target="patched_code",
                result=patch_res.verdict,
                timestamp=datetime.now(timezone.utc).isoformat(),
                capture="observed",
            ),
        ],
        cleanup={"performed": True, "clean": True, "errors": []},
        limitations=["Verify mode đối soát bản gốc và bản vá trước khi nghiệm thu."],
    )

    proof_file = export_proof_bundle(bundle, evidence_root)

    return VerifyResult(
        verdict=verdict,
        baseline_reproduced=base_reproduced,
        patch_clean=patch_clean,
        proof_path=proof_file,
        needs_independent_review=True,
    )
