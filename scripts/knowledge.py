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
import re
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
from agent_core.knowledge.context import build_context, ContextRequest, estimate_tokens


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


def cmd_query(args: argparse.Namespace) -> int:
    root_dir = args.root or "."
    catalog = load_catalog(root_dir, filename=args.manifest)
    query_str = args.query.lower().strip()
    if not query_str:
        sys.stderr.write("Lỗi: Cần cung cấp từ khóa tìm kiếm qua --query\n")
        return 2

    budget = args.budget or 1200
    role = args.role.strip() if args.role else None

    # Xếp hạng: không phân biệt dấu, bỏ chữ nhiễu, IDF, cụm từ, đồng nghĩa (agent_core/knowledge/search.py)
    from agent_core.knowledge.search import rank
    scored_nodes = rank(catalog, root_dir, args.query, role)

    # Hàng xóm theo cạnh (hai chiều): kiến thức nối với nút khớp nhất, để tra một chủ đề ra cả phần liên quan.
    adjacency = {}
    for nid, node in catalog.nodes.items():
        for r in node.relations:
            if r.type in ("related_to", "constrains", "implements", "refines") and r.target in catalog.nodes:
                adjacency.setdefault(nid, []).append(r.target)
                adjacency.setdefault(r.target, []).append(nid)

    def related_of(hits, cap=4):
        hit_ids = {n.id for _, n in hits}
        found, seen = [], set()
        for _, n in hits:
            for other in adjacency.get(n.id, []):
                if other not in hit_ids and other not in seen:
                    seen.add(other)
                    found.append(catalog.nodes[other])
        return found[:cap]

    def log_usage(hits, related):
        """Ghi nhật ký cục bộ (không commit) để biết nút nào được dùng và từ khóa nào trả rỗng."""
        try:
            log_dir = os.path.join(root_dir, ".local")
            os.makedirs(log_dir, exist_ok=True)
            entry = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "role": role, "q": args.query,
                     "hits": [n.id for _, n in hits], "related": [n.id for n in related]}
            with open(os.path.join(log_dir, "knowledge-usage.jsonl"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass

    if not scored_nodes:
        log_usage([], [])
        print(f"🔍 Không tìm thấy tri thức nào khớp với từ khóa: '{args.query}'")
        return 0

    limit = getattr(args, "limit", 3) or 3
    top_hits = scored_nodes[:limit]
    related_nodes = related_of(top_hits)
    log_usage(top_hits, related_nodes)

    if args.format == "json":
        out = []
        for score, n in scored_nodes[:limit]:
            entry = {"id": n.id, "title": n.title, "score": score, "file": n.content_ref}
            path = os.path.join(root_dir, n.content_ref) if n.content_ref else None
            if path and os.path.isfile(path):
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
                entry["summary"] = n.raw_data.get("summary") or _outline(text)[0]
                entry["headings"] = _outline(text)[1]
                entry["tokens"] = estimate_tokens(text)
            out.append(entry)
        if out:
            out[0]["related"] = [{"id": n.id, "title": n.title, "file": n.content_ref} for n in related_nodes]
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    print(f"🎯 KẾT QUẢ TRA CỨU TRI THỨC JIT (Từ khóa: '{args.query}', Ngân sách: {budget} tokens)")
    print(f"  Tìm thấy {len(scored_nodes)} node phù hợp. Top {min(len(scored_nodes), limit)} node:")

    current_tokens = 0
    for idx, (score, node) in enumerate(scored_nodes[:limit], 1):
        content_path = os.path.join(root_dir, node.content_ref) if node.content_ref else None
        print(f"\n  [{idx}] {node.id} — {node.title} (Điểm khớp: {score})")
        print(f"      Tệp: {node.content_ref}")

        if content_path and os.path.isfile(content_path):
            with open(content_path, "r", encoding="utf-8", errors="replace") as f:
                full_text = f.read()

            t_count = estimate_tokens(full_text)

            if current_tokens + t_count <= budget:
                print(f"      Dung lượng: ~{t_count} tokens (Nạp trong ngân sách)")
                print("      " + "-" * 60)
                indented = "\n".join("      " + line for line in full_text.splitlines())
                print(indented)
                current_tokens += t_count
            else:
                remaining_budget = max(0, budget - current_tokens)
                print(f"      Dung lượng: ~{t_count} tokens (Vượt ngân sách còn lại {remaining_budget} tokens -> Trích xuất tóm lược)")
                outline_summary, headings = _outline(full_text)
                summary = node.raw_data.get("summary") or outline_summary or "Không có tóm tắt"
                print(f"      Tóm tắt: {summary}")
                if headings:
                    print("      Mục: " + " | ".join(headings))
                print(f"      (Chỉ đọc tệp trên khi cần chi tiết, có thể đọc riêng một mục: {node.content_ref})")
                current_tokens += estimate_tokens(summary)

    if related_nodes:
        print("\n  Liên quan (nối bằng cạnh, chỉ đọc khi cần):")
        for n in related_nodes:
            print(f"    - {n.id} — {n.title}  [{n.content_ref}]")

    return 0


def _outline(text: str, max_headings: int = 8):
    """Tóm tắt một dòng và danh sách mục (##) của một file md, để agent chọn đọc đúng phần thay vì nạp cả file."""
    summary = ""
    for line in text.splitlines():
        t = line.strip()
        if not t or t.startswith(("#", ">", "|", "---", "```", "<!--", "- [", "!")):
            continue
        summary = re.sub(r"[`*_]", "", t)[:220]
        break
    headings = [re.sub(r"^#+\s*", "", ln).strip() for ln in text.splitlines() if ln.startswith("## ")]
    return summary, headings[:max_headings]


def cmd_learn(args: argparse.Namespace) -> int:
    root_dir = args.root or "."
    title = args.title.strip()
    note_content = args.note.strip()
    role = args.role.strip() if args.role else "dev"

    if not title or not note_content:
        sys.stderr.write("Lỗi: Cần cung cấp --title và --note\n")
        return 2

    inbox_dir = os.path.join(root_dir, "docs", "notes", "inbox")
    os.makedirs(inbox_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r'[^a-zA-Z0-9_-]', '_', title.lower())[:30]
    filename = f"learn_{timestamp}_{slug}.md"
    file_path = os.path.join(inbox_dir, filename)

    content = f"""# Bài học tự phản tư: {title}

> **Vai trò:** {role}  
> **Thời gian:** {datetime.now(timezone.utc).isoformat()}  
> **Trạng thái:** inbox (Chờ harness-reflect tổng hợp)

## 1. Bối cảnh & Hiện tượng
{note_content}

## 2. Bài học rút ra (Do & Don't)
- Ghi nhận tự động từ phiên làm việc nhằm tránh vỡ context.
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Tự động đồng bộ INDEX.md để không lệch CI check
    notes_script = Path(root_dir) / "scripts" / "notes-index.py"
    if notes_script.is_file():
        import subprocess
        subprocess.run([sys.executable, str(notes_script)], check=False, stdout=subprocess.DEVNULL)

    print(f"✅ Đã ghi nhận bài học mới an toàn vào: {file_path}")
    print("💡 Bài học đã được lưu vào inbox của hệ sinh thái mà KHÔNG làm phình to context window.")
    print("   Hệ thống có thể chạy `python3 scripts/harness-reflect.py --archive` định kỳ để cô đọng vào PROJECT-NOTES.")
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
    p_ctx.add_argument("--budget", type=int, default=30000, help="Trần ngân sách token tối đa (mặc định 30000)")
    p_ctx.add_argument("--include-draft", action="store_true", help="Bao gồm tài liệu draft ở phần phụ lục appendix")
    p_ctx.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    # Lệnh query (JIT On-Demand Knowledge Retrieval)
    p_qry = subparsers.add_parser("query", help="Tra cứu tri thức JIT On-Demand theo từ khóa và ngân sách token")
    p_qry.add_argument("--query", "-q", required=True, help="Từ khóa tìm kiếm (VD: 'jpa n+1', 'redis lock', 'drawio csv')")
    p_qry.add_argument("--root", default=".", help="Thư mục gốc của kho tri thức (mặc định .)")
    p_qry.add_argument("--manifest", default="knowledge.manifest.json", help="Tên hoặc đường dẫn file manifest")
    p_qry.add_argument("--budget", type=int, default=1200, help="Trần ngân sách token tối đa (mặc định 1200)")
    p_qry.add_argument("--limit", type=int, default=3, help="Số lượng node hiển thị tối đa (mặc định 3)")
    p_qry.add_argument("--role", help="Lọc ưu tiên theo vai trò (dev, architect, qa...)")
    p_qry.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    # Lệnh learn (Ghi nhận bài học tự học mà không làm rác context)
    p_lrn = subparsers.add_parser("learn", help="Ghi nhận bài học mới vào inbox an toàn mà không làm phình to context")
    p_lrn.add_argument("--title", required=True, help="Tiêu đề bài học kinh nghiệm")
    p_lrn.add_argument("--note", required=True, help="Nội dung bài học và hiện tượng lỗi")
    p_lrn.add_argument("--role", default="dev", help="Vai trò phát hiện bài học")
    p_lrn.add_argument("--root", default=".", help="Thư mục gốc (mặc định .)")

    args = parser.parse_args()

    # Không chỉ định --manifest và gốc không có knowledge.manifest.json: dùng catalog của khung agent-base.
    default_name = "knowledge.manifest.json"
    alt_name = "agents/knowledge/knowledge-manifest.json"
    root = getattr(args, "root", None) or "."
    if getattr(args, "manifest", None) == default_name and not os.path.exists(os.path.join(root, default_name)) \
            and os.path.exists(os.path.join(root, alt_name)):
        args.manifest = alt_name

    if args.command == "validate":
        sys.exit(cmd_validate(args))
    elif args.command == "context":
        sys.exit(cmd_context(args))
    elif args.command == "query":
        sys.exit(cmd_query(args))
    elif args.command == "learn":
        sys.exit(cmd_learn(args))
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
