#!/usr/bin/env python3
"""scripts/trace-logger.py

Hệ Thống Quan Sát & Nhật Ký Thực Thi Theo Dòng Thời Gian (Session Observability & Tracing).
Hiện thực hóa chuẩn OpenTelemetry / Langfuse cho AI Agent: Theo dõi chi phí, độ trễ và tỷ lệ lỗi tool call.

Tính năng:
- Ghi vết thực thi dạng JSON Lines vào `.agentbase/traces/<session_id>.jsonl`.
- Các loại sự kiện: `SESSION_START`, `TOOL_CALL`, `CHECKPOINT`, `GATE_CHECK`, `HANDOFF`, `SESSION_END`.
- `summary [--session <id>]`: Xuất báo cáo hiệu năng phiên:
  * Tổng thời gian thực thi (wall-clock duration).
  * Tổng số tool calls, tỷ lệ thành công/thất bại.
  * Các tool tốn nhiều thời gian nhất (hotspots).
  * Danh sách các cổng kiểm đã đi qua.

Usage:
  python3 scripts/trace-logger.py start --session S-101 --task T-12.1 --agent dev
  python3 scripts/trace-logger.py log --session S-101 --type TOOL_CALL --tool safe-exec --status OK --duration 0.45
  python3 scripts/trace-logger.py end --session S-101 --status SUCCESS
  python3 scripts/trace-logger.py summary --session S-101
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / ".agentbase" / "traces"


def get_trace_path(session_id: str) -> Path:
    """Trả về đường dẫn tệp trace của session."""
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    clean_id = "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in session_id)
    return TRACE_DIR / f"{clean_id}.jsonl"


def append_event(session_id: str, event_type: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ghi thêm một sự kiện vào trace log."""
    path = get_trace_path(session_id)
    payload = {
        "session_id": session_id,
        "type": event_type,
        "timestamp": time.time(),
        "iso_time": datetime.now(timezone.utc).isoformat(),
        "data": data or {},
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return payload


def get_session_summary(session_id: str) -> Dict[str, Any]:
    """Tổng hợp phân tích hiệu năng của một phiên làm việc."""
    path = get_trace_path(session_id)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu trace cho session '{session_id}'")

    events = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    events.append(json.loads(line.strip()))
                except Exception:
                    continue

    if not events:
        return {"session_id": session_id, "total_events": 0}

    start_time = events[0]["timestamp"]
    end_time = events[-1]["timestamp"]
    duration = round(end_time - start_time, 2)

    tool_calls = 0
    tool_failures = 0
    tool_durations = {}
    gates_passed = 0
    gates_failed = 0

    for ev in events:
        etype = ev["type"]
        edata = ev.get("data", {})

        if etype == "TOOL_CALL":
            tool_calls += 1
            tool_name = edata.get("tool", "unknown")
            tool_status = edata.get("status", "OK").upper()
            tool_dur = float(edata.get("duration", 0.0))

            if tool_status not in ("OK", "SUCCESS", "0"):
                tool_failures += 1

            if tool_name not in tool_durations:
                tool_durations[tool_name] = {"count": 0, "total_sec": 0.0}
            tool_durations[tool_name]["count"] += 1
            tool_durations[tool_name]["total_sec"] += tool_dur

        elif etype == "GATE_CHECK":
            gate_status = edata.get("status", "PASS").upper()
            if gate_status in ("PASS", "OK"):
                gates_passed += 1
            else:
                gates_failed += 1

    # Tìm tool tốn nhiều thời gian nhất
    sorted_tools = sorted(tool_durations.items(), key=lambda x: x[1]["total_sec"], reverse=True)
    hotspots = [
        {"tool": k, "calls": v["count"], "total_sec": round(v["total_sec"], 2)}
        for k, v in sorted_tools[:3]
    ]

    return {
        "session_id": session_id,
        "total_events": len(events),
        "duration_sec": duration,
        "tool_calls": tool_calls,
        "tool_failures": tool_failures,
        "tool_success_rate": round(100.0 * (tool_calls - tool_failures) / tool_calls, 1) if tool_calls else 100.0,
        "gates_passed": gates_passed,
        "gates_failed": gates_failed,
        "hotspots": hotspots,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="trace-logger: Hệ thống quan sát & nhật ký hành trình Agent (Telemetry & Observability)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_start = sub.add_parser("start", help="Bắt đầu ghi vết session mới")
    p_start.add_argument("--session", required=True, help="Mã định danh session (ví dụ: S-101)")
    p_start.add_argument("--task", default="", help="Mã task (ví dụ: T-12.1)")
    p_start.add_argument("--agent", default="dev", help="Vai trò agent chính")

    p_log = sub.add_parser("log", help="Ghi một sự kiện vào trace")
    p_log.add_argument("--session", required=True, help="Mã định danh session")
    p_log.add_argument("--type", required=True, choices=["TOOL_CALL", "CHECKPOINT", "GATE_CHECK", "HANDOFF", "INFO"], help="Loại sự kiện")
    p_log.add_argument("--tool", default="", help="Tên tool nếu là TOOL_CALL")
    p_log.add_argument("--status", default="OK", help="Trạng thái (OK, FAIL, PASS)")
    p_log.add_argument("--duration", type=float, default=0.0, help="Thời gian thực thi của tool (giây)")
    p_log.add_argument("--msg", default="", help="Thông điệp chi tiết")

    p_end = sub.add_parser("end", help="Kết thúc session trace")
    p_end.add_argument("--session", required=True, help="Mã định danh session")
    p_end.add_argument("--status", default="SUCCESS", help="Kết quả cuối cùng của session")

    p_summary = sub.add_parser("summary", help="Hiển thị báo cáo hiệu năng của session")
    p_summary.add_argument("--session", required=True, help="Mã định danh session")
    p_summary.add_argument("--json", action="store_true", help="Xuất định dạng JSON")

    args = parser.parse_args()

    if args.cmd == "start":
        ev = append_event(args.session, "SESSION_START", {"task": args.task, "agent": args.agent})
        print(f"[OK] Bắt đầu Trace Session '{args.session}' lúc {ev['iso_time']}.")
        return 0

    elif args.cmd == "log":
        data = {"status": args.status, "duration": args.duration, "msg": args.msg}
        if args.tool:
            data["tool"] = args.tool
        append_event(args.session, args.type, data)
        return 0

    elif args.cmd == "end":
        append_event(args.session, "SESSION_END", {"final_status": args.status})
        print(f"[OK] Đã kết thúc Trace Session '{args.session}'.")
        return 0

    elif args.cmd == "summary":
        try:
            summ = get_session_summary(args.session)
            if args.json:
                print(json.dumps(summ, ensure_ascii=False, indent=2))
            else:
                print("=" * 60)
                print(f"📊 BÁO CÁO HIỆU NĂNG PHIÊN (SESSION TRACE): {summ['session_id']}")
                print("=" * 60)
                print(f"• Thời lượng chạy (Wall-clock)  : {summ['duration_sec']}s")
                print(f"• Tổng số lượt gọi Tool         : {summ['tool_calls']} (Tỷ lệ thành công: {summ['tool_success_rate']}%)")
                print(f"• Số lần Tool bị lỗi / timeout   : {summ['tool_failures']}")
                print(f"• Cổng kiểm soát (Gate checks)   : {summ['gates_passed']} PASS | {summ['gates_failed']} FAIL")
                if summ["hotspots"]:
                    print("• Các công cụ chiếm nhiều thời gian nhất:")
                    for h in summ["hotspots"]:
                        print(f"   - {h['tool']}: {h['calls']} lượt gọi, tổng {h['total_sec']}s")
                print("=" * 60)
            return 0
        except Exception as exc:
            print(f"[ERROR] Không thể lập báo cáo: {exc}", file=sys.stderr)
            return 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
