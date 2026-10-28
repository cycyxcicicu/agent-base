"""agent_core.verification.proof

Mô hình dữ liệu và bộ kiểm chuẩn hợp đồng bằng chứng thực thi (Proof Bundle).
Tuân thủ đặc tả T-11 §5, schema Draft 2020-12 bằng Python stdlib.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

SHA256_REGEX = re.compile(r"^[a-f0-9]{64}$")
ISO_DATETIME_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)

ALLOWED_ENVELOPE_KEYS = {
    "schema_version",
    "run_id",
    "scenario_id",
    "phase",
    "started_at",
    "ended_at",
    "result",
    "repo_revision",
    "dirty_input_manifest",
    "input_digest",
    "tool_versions",
    "commands",
    "assertions",
    "artifacts",
    "trace",
    "cleanup",
    "limitations",
}

VALID_PHASES = {"baseline", "final"}
VALID_RESULTS = {"pass", "fail", "inconclusive", "skipped"}
VALID_CAPTURES = {"observed", "reported"}


@dataclass
class CommandRecord:
    sequence: int
    argv: List[str]
    cwd_rel: str
    timeout_sec: int
    exit_code: int
    duration_ms: int
    stdout_sha256: str
    stderr_sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence": self.sequence,
            "argv": self.argv,
            "cwd_rel": self.cwd_rel,
            "timeout_sec": self.timeout_sec,
            "exit_code": self.exit_code,
            "duration_ms": self.duration_ms,
            "stdout_sha256": self.stdout_sha256,
            "stderr_sha256": self.stderr_sha256,
        }


@dataclass
class AssertionRecord:
    id: str
    expected: str
    observed: str
    passed: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "expected": self.expected,
            "observed": self.observed,
            "passed": self.passed,
        }


@dataclass
class ArtifactRecord:
    path_rel: str
    sha256: str
    byte_count: int
    media_type: str = "text/plain"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path_rel": self.path_rel,
            "sha256": self.sha256,
            "byte_count": self.byte_count,
            "media_type": self.media_type,
        }


@dataclass
class TraceRecord:
    sequence: int
    actor: str
    action: str
    target: str
    result: str
    timestamp: str
    capture: str = "observed"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence": self.sequence,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "result": self.result,
            "timestamp": self.timestamp,
            "capture": self.capture,
        }


@dataclass
class ProofBundle:
    run_id: str
    scenario_id: str
    phase: str
    started_at: str
    ended_at: str
    result: str
    repo_revision: str
    input_digest: str
    schema_version: int = 1
    dirty_input_manifest: List[str] = field(default_factory=list)
    tool_versions: Dict[str, str] = field(default_factory=dict)
    commands: List[CommandRecord] = field(default_factory=list)
    assertions: List[AssertionRecord] = field(default_factory=list)
    artifacts: List[ArtifactRecord] = field(default_factory=list)
    trace: List[TraceRecord] = field(default_factory=list)
    cleanup: Dict[str, Any] = field(default_factory=lambda: {"performed": True, "clean": True, "errors": []})
    limitations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "scenario_id": self.scenario_id,
            "phase": self.phase,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "result": self.result,
            "repo_revision": self.repo_revision,
            "dirty_input_manifest": self.dirty_input_manifest,
            "input_digest": self.input_digest,
            "tool_versions": self.tool_versions,
            "commands": [c.to_dict() for c in self.commands],
            "assertions": [a.to_dict() for a in self.assertions],
            "artifacts": [art.to_dict() for art in self.artifacts],
            "trace": [t.to_dict() for t in self.trace],
            "cleanup": self.cleanup,
            "limitations": self.limitations,
        }


def validate_proof_bundle(data: Dict[str, Any]) -> List[str]:
    """Kiểm tra hợp đồng Proof bundle theo chuẩn draft 2020-12 (T-11 spec §5)."""
    errors: List[str] = []

    if not isinstance(data, dict):
        return ["Proof bundle phải là một JSON object"]

    # additionalProperties: false
    extra = set(data.keys()) - ALLOWED_ENVELOPE_KEYS
    if extra:
        errors.append(f"additionalProperties: Phát hiện trường không được phép: {', '.join(sorted(extra))}")

    # Required fields
    required = ALLOWED_ENVELOPE_KEYS
    missing = [k for k in required if k not in data]
    if missing:
        errors.append(f"Thiếu các trường bắt buộc: {', '.join(sorted(missing))}")

    if data.get("schema_version") != 1:
        errors.append(f"schema_version phải là 1 (nhận {data.get('schema_version')})")

    phase = data.get("phase")
    if phase not in VALID_PHASES:
        errors.append(f"phase '{phase}' không hợp lệ (chỉ cho phép: baseline, final)")

    result = data.get("result")
    if result not in VALID_RESULTS:
        errors.append(f"result '{result}' không hợp lệ (chỉ cho phép: pass, fail, inconclusive, skipped)")

    digest = data.get("input_digest")
    if isinstance(digest, str) and not SHA256_REGEX.match(digest.lower()):
        errors.append(f"input_digest không phải là chuỗi SHA256 64-hex hợp lệ: '{digest}'")

    started_at = data.get("started_at")
    if isinstance(started_at, str) and not ISO_DATETIME_REGEX.match(started_at):
        errors.append(f"started_at không đúng định dạng ISO UTC timestamp: '{started_at}'")

    ended_at = data.get("ended_at")
    if isinstance(ended_at, str) and not ISO_DATETIME_REGEX.match(ended_at):
        errors.append(f"ended_at không đúng định dạng ISO UTC timestamp: '{ended_at}'")

    # Kiểm tra artifacts (chống path escape)
    artifacts = data.get("artifacts")
    if isinstance(artifacts, list):
        for idx, art in enumerate(artifacts):
            if not isinstance(art, dict):
                continue
            p_rel = art.get("path_rel")
            if isinstance(p_rel, str):
                norm = os.path.normpath(p_rel)
                if (
                    os.path.isabs(p_rel)
                    or norm.startswith("..")
                    or "/../" in p_rel.replace("\\", "/")
                ):
                    errors.append(f"artifacts[{idx}].path_rel '{p_rel}' vi phạm path escape")
            sha = art.get("sha256")
            if isinstance(sha, str) and not SHA256_REGEX.match(sha.lower()):
                errors.append(f"artifacts[{idx}].sha256 không hợp lệ: '{sha}'")

    # Kiểm tra trace
    traces = data.get("trace")
    if isinstance(traces, list):
        for idx, tr in enumerate(traces):
            if not isinstance(tr, dict):
                continue
            cap = tr.get("capture")
            if cap not in VALID_CAPTURES:
                errors.append(f"trace[{idx}].capture '{cap}' không hợp lệ (chỉ cho phép: observed, reported)")

    return errors


def export_proof_bundle(bundle: ProofBundle | Dict[str, Any], evidence_root: Path | str) -> Path:
    """Xuất proof bundle ra tệp proof.json trong thư mục run_id dưới evidence_root."""
    data = bundle.to_dict() if isinstance(bundle, ProofBundle) else bundle
    run_id = data.get("run_id", f"run-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}")

    out_dir = Path(evidence_root).resolve() / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    proof_file = out_dir / "proof.json"
    proof_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return proof_file
