#!/usr/bin/env python3
"""scripts/safe-exec.py

Bộ thực thi lệnh thông minh với cơ chế nén & gọt đầu ra (Smart Output Folding & Truncation).
Ngăn chặn hiện tượng Tràn RAM Ngữ Cảnh (Context Rot / RAM Bloat) theo chuẩn Context Engineering 2025.

Tính năng:
- Thực thi command an toàn với timeout và stream capture.
- Bảo toàn mã thoát (exit code) nguyên bản của lệnh con.
- Output Folding:
  - Nếu output <= max_lines (mặc định 30 dòng): in đầy đủ.
  - Nếu output > max_lines:
    * Giữ lại phần header/ngữ cảnh ban đầu (mặc định 6 dòng).
    * Tự động quét và phát hiện các vùng lỗi (Traceback, Error, Exception, FAIL, AssertionError, Build Failure...).
    * Gập các dòng output rác/lặp lại thành: `... [gập N dòng output rác/lặp lại] ...`.
    * Giữ lại phần summary/exit status ở cuối (mặc định 6 dòng).
- Hỗ trợ cờ `--json` để xuất báo cáo có cấu trúc cho Orchestrator / Subagent handoff.
- Hỗ trợ cờ `--lines <N>` để điều chỉnh ngân sách dòng.

Usage:
  python3 scripts/safe-exec.py -c "mvn test"
  python3 scripts/safe-exec.py -c "pytest tests/" -l 40
  python3 scripts/safe-exec.py --json -c "python3 -m unittest"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_MAX_LINES = 30
DEFAULT_HEAD_LINES = 6
DEFAULT_TAIL_LINES = 6

ERROR_PATTERNS = [
    re.compile(r"\b(?:traceback|exception|error|fatal|fail(?:ed|ure)?)\b", re.IGNORECASE),
    re.compile(r"\b(?:assert(?:ion)?error|panic|undefined|nullpointerexception)\b", re.IGNORECASE),
    re.compile(r"^\s*(?:File\s+\".*\",\s+line\s+\d+|at\s+[\w\.\$]+\([\w\.\s]+:\d+\))"),
    re.compile(r"\b(?:passed|failed|skipped|errors?|warnings?)\b.*(?:\d+|%)", re.IGNORECASE),
    re.compile(r"\b(?:build\s+(?:failure|failed|successful))\b", re.IGNORECASE),
    re.compile(r"^[=\-]{4,}\s*(?:fail|error|summary)"),
]


def is_error_or_summary_line(line: str) -> bool:
    """Kiểm tra xem một dòng có chứa tín hiệu lỗi hoặc tổng kết quan trọng hay không."""
    return any(pattern.search(line) for pattern in ERROR_PATTERNS)


def _extract_critical_indices(pool: List[str], budget: int) -> set[int]:
    """Tìm các dòng lỗi và ngữ cảnh quanh nó trong middle pool."""
    indices = set()
    for idx, line in enumerate(pool):
        if is_error_or_summary_line(line):
            indices.add(idx)
            if idx > 0:
                indices.add(idx - 1)
            if idx + 1 < len(pool):
                indices.add(idx + 1)
    sorted_idx = sorted(list(indices))
    if len(sorted_idx) > budget:
        sorted_idx = sorted_idx[-budget:]
    return set(sorted_idx)


def _fold_middle_pool(pool: List[str], selected: set[int]) -> Tuple[List[str], int]:
    """Gập các đoạn output rác liên tiếp."""
    result = []
    folded = 0
    idx = 0
    while idx < len(pool):
        if idx in selected:
            result.append(pool[idx])
            idx += 1
        else:
            start_skip = idx
            while idx < len(pool) and idx not in selected:
                idx += 1
            skipped_len = idx - start_skip
            folded += skipped_len
            result.append(f"... [gập {skipped_len} dòng output rác/lặp lại] ...")
    return result, folded


def compress_output(
    lines: List[str],
    max_lines: int = DEFAULT_MAX_LINES,
    head_count: int = DEFAULT_HEAD_LINES,
    tail_count: int = DEFAULT_TAIL_LINES,
) -> Tuple[List[str], int]:
    """Nén và gọt danh sách các dòng output theo thuật toán Smart Folding."""
    total = len(lines)
    if total <= max_lines:
        return lines, 0

    if head_count + tail_count >= max_lines:
        head_count = max_lines // 2
        tail_count = max_lines - head_count

    head = lines[:head_count]
    tail = lines[-tail_count:] if tail_count > 0 else []
    middle_pool = lines[head_count : (total - tail_count if tail_count > 0 else total)]

    budget = max(0, max_lines - head_count - tail_count - 2)
    critical_set = _extract_critical_indices(middle_pool, budget)
    result_middle, folded_count = _fold_middle_pool(middle_pool, critical_set)

    return head + result_middle + tail, folded_count


def _run_subprocess_safe(cmd: str, timeout_sec: float, cwd: str | None, env: dict | None) -> Tuple[str, int, float, bool]:
    """Thực thi lệnh và bắt timeout an toàn."""
    start = time.time()
    try:
        proc = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", timeout=timeout_sec,
            cwd=cwd, env=env,
        )
        return proc.stdout or "", proc.returncode, round(time.time() - start, 2), False
    except subprocess.TimeoutExpired as exc:
        msg = (exc.stdout or "") + f"\n[safe-exec] ERROR: Lệnh vượt quá thời gian chờ (Timeout {timeout_sec}s)"
        return msg, 124, round(time.time() - start, 2), True


def execute_command(
    cmd: str,
    max_lines: int = DEFAULT_MAX_LINES,
    timeout_sec: float = 300.0,
    cwd: str | None = None,
    env: dict | None = None,
) -> dict:
    """Thực thi lệnh trong subprocess, bắt toàn bộ stdout/stderr và gọt output."""
    raw_output, exit_code, duration, timed_out = _run_subprocess_safe(cmd, timeout_sec, cwd, env)
    lines = raw_output.splitlines()
    total_lines = len(lines)
    compressed, folded_count = compress_output(lines, max_lines=max_lines)

    status_str = "SUCCESS" if exit_code == 0 else ("TIMEOUT" if timed_out else "FAILED")
    header = (
        f"[safe-exec] Command: '{cmd}' | Status: {status_str} (Code: {exit_code}) | "
        f"Time: {duration}s | Lines: {total_lines} -> {len(compressed)}"
    )

    return {
        "command": cmd, "exit_code": exit_code, "duration_sec": duration,
        "timed_out": timed_out, "total_lines": total_lines, "folded_lines": folded_count,
        "header": header, "output": "\n".join(compressed), "raw_output": raw_output,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="safe-exec: Thực thi lệnh và gọt output thông minh chống tràn Context Window"
    )
    parser.add_argument(
        "-c", "--command", required=True, help="Lệnh shell cần thực thi"
    )
    parser.add_argument(
        "-l",
        "--lines",
        type=int,
        default=DEFAULT_MAX_LINES,
        help=f"Ngân sách dòng tối đa hiển thị (mặc định: {DEFAULT_MAX_LINES})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=300.0,
        help="Thời gian chờ tối đa bằng giây (mặc định: 300s)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Xuất kết quả dưới định dạng JSON",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Không in header tóm tắt của safe-exec",
    )

    args = parser.parse_args()

    res = execute_command(args.command, max_lines=args.lines, timeout_sec=args.timeout)

    if args.json:
        payload = {k: v for k, v in res.items() if k != "raw_output"}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not args.no_header:
            print(res["header"])
        if res["output"]:
            print(res["output"])

    return res["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
