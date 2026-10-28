#!/usr/bin/env python3
"""
scripts/knowledge.py
CLI quản lý, kiểm chuẩn và trích xuất ngữ cảnh tri thức theo vai và nhiệm vụ.
Tuân thủ đặc tả T-11 §3 và các yêu cầu R-01, R-02, R-03, R-04.

Mã thoát (Exit codes):
  0: Thành công / Hợp lệ
  1: Lỗi nội dung hoặc độ cũ tri thức (V01–V10) hoặc luật vượt ngân sách
  2: Lỗi tham số đầu vào (thiếu root, tham số sai)
  3: Thiếu bằng chứng phê duyệt tin cậy

Usage:
  python scripts/knowledge.py validate --root <dir> [--as-of <UTC>] [--format json]
  python scripts/knowledge.py context --root <dir> --role <vai> [--task <T-xx>] [--as-of <UTC>] [--budget <n>] [--include-draft] [--format json]
"""

from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.knowledge.catalog import load_catalog, validate_catalog
from agent_core.knowledge.context import build_context, ContextRequest


def parse_as_of(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception as e:
        sys.stderr.write(f"Lỗi: Định dạng thời gian as-of không hợp lệ ('{raw}'): {str(e)}\n")
        sys.exit(2)


def cmd_validate(args: argparse.Namespace) -> int:
    root_dir = args.root
    if not root_dir or not os.path.isdir(root_dir):
        sys.stderr.write(f"Lỗi: Thư mục root không tồn tại: {root_dir}\n")
        return 2

    as_of = parse_as_of(args.as_of)
    catalog = load_catalog(root_dir, filename=args.manifest)
    diagnostics = validate_catalog(catalog, as_of=as_of)

    if args.format == "json":
        out = {
            "root": root_dir,
            "as_of": as_of.isoformat() if as_of else datetime.now(timezone.utc).isoformat(),
            "diagnostic_count": len(diagnostics),
            "diagnostics": [d.to_dict() for d in diagnostics],
            "valid": len(diagnostics) == 0,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        if not diagnostics:
            print(f"✅ Catalog hợp lệ: 0 lỗi ({len(catalog.nodes)} nodes).")
        else:
            print(f"❌ Phát hiện {len(diagnostics)} lỗi trong catalog tri thức:")
            for d in diagnostics:
                node_part = f" [{d.node_id}]" if d.node_id else ""
                path_part = f" (tại {d.path})" if d.path else ""
                print(f"  - [{d.code}] {d.message}{node_part}{path_part}")

    return 0 if len(diagnostics) == 0 else 1


def cmd_context(args: argparse.Namespace) -> int:
    root_dir = args.root
    if not root_dir or not os.path.isdir(root_dir):
        sys.stderr.write(f"Lỗi: Thư mục root không tồn tại: {root_dir}\n")
        return 2

    if not args.role:
        sys.stderr.write("Lỗi: Tham số --role là bắt buộc.\n")
        return 2

    as_of = parse_as_of(args.as_of)
    catalog = load_catalog(root_dir, filename=args.manifest)

    req = ContextRequest(
        role=args.role,
        task_id=args.task,
        as_of=as_of,
        budget=args.budget,
        include_draft=args.include_draft,
    )

    try:
        bundle = build_context(catalog, req)
    except ValueError as e:
        sys.stderr.write(f"Lỗi: {str(e)}\n")
        return 1

    if args.format == "json":
        print(json.dumps(bundle.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"🎯 NGỮ CẢNH TRI THỨC CHO VAI: {bundle.role}" + (f" (Task: {bundle.task_id})" if bundle.task_id else ""))
        print(f"  - Ước lượng tokens: {bundle.estimated_tokens}" + (f" / {bundle.budget}" if bundle.budget else ""))
        print(f"  - Số node được chọn: {len(bundle.nodes)}")
        for n in bundle.nodes:
            print(f"    * [{n.get('kind')}] {n.get('id')}: {n.get('title')} ({n.get('estimated_tokens', 0)} tokens)")
        if bundle.appendix:
            print(f"  - Phụ lục dự thảo (Draft Appendix): {len(bundle.appendix)} nodes")
            for n in bundle.appendix:
                print(f"    * [{n.get('kind')}] {n.get('id')}: {n.get('title')} (DRAFT)")
        if bundle.omitted_ids:
            print(f"  - Node bị cắt giảm do vượt ngân sách: {', '.join(bundle.omitted_ids)}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="CLI Quản lý & Trích xuất ngữ cảnh tri thức")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Lệnh validate
    p_val = subparsers.add_parser("validate", help="Kiểm chuẩn tính toàn vẹn của catalog tri thức")
    p_val.add_argument("--root", required=True, help="Thư mục gốc chứa knowledge.manifest.json")
    p_val.add_argument("--manifest", default="knowledge.manifest.json", help="Tên hoặc đường dẫn file manifest")
    p_val.add_argument("--as-of", help="Mốc thời gian đánh giá độ cũ (ISO UTC, ví dụ 2026-10-28T00:00:00Z)")
    p_val.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    # Lệnh context
    p_ctx = subparsers.add_parser("context", help="Trích xuất ngữ cảnh tối thiểu theo vai trò và nhiệm vụ")
    p_ctx.add_argument("--root", required=True, help="Thư mục gốc chứa knowledge.manifest.json")
    p_ctx.add_argument("--manifest", default="knowledge.manifest.json", help="Tên hoặc đường dẫn file manifest")
    p_ctx.add_argument("--role", required=True, help="Vai trò cần trích xuất (dev, reviewer, architect, ...)")
    p_ctx.add_argument("--task", help="Mã task (T-xx) nếu có")
    p_ctx.add_argument("--as-of", help="Mốc thời gian đánh giá độ cũ (ISO UTC)")
    p_ctx.add_argument("--budget", type=int, help="Trần ngân sách token tối đa cho phép")
    p_ctx.add_argument("--include-draft", action="store_true", help="Bao gồm tài liệu draft ở phần phụ lục appendix")
    p_ctx.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    args = parser.parse_args()

    if args.command == "validate":
        sys.exit(cmd_validate(args))
    elif args.command == "context":
        sys.exit(cmd_context(args))
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
