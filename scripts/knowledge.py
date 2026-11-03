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
from agent_core.knowledge.project_graph import (
    detect_project_context,
    build_project_graph,
    query_project_graph,
)


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

    inbox_candidates = [
        os.path.join(root_dir, "doc", "notes", "inbox"),
        os.path.join(root_dir, "docs", "notes", "inbox"),
    ]
    inbox_dir = next((d for d in inbox_candidates if os.path.isdir(d)), None)
    if not inbox_dir:
        inbox_dir = os.path.join(root_dir, "doc", "notes", "inbox") if os.path.isdir(os.path.join(root_dir, "doc")) else os.path.join(root_dir, "docs", "notes", "inbox")
    os.makedirs(inbox_dir, exist_ok=True)

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    today_str = now.strftime("%Y-%m-%d")
    slug = re.sub(r'[^a-zA-Z0-9_-]', '_', title.lower())[:30]
    filename = f"learn_{timestamp}_{slug}.md"
    file_path = os.path.join(inbox_dir, filename)

    # Định dạng bullet points cho Lessons
    note_lines = [ln.strip() for ln in note_content.splitlines() if ln.strip()]
    formatted_lessons = []
    for ln in note_lines:
        if ln.startswith(("- ", "* ")):
            formatted_lessons.append(ln)
        else:
            formatted_lessons.append(f"- {ln}")
    lessons_block = "\n".join(formatted_lessons) if formatted_lessons else f"- {note_content}"

    trap_input = getattr(args, "trap", None)
    if trap_input and trap_input.strip():
        trap_lines = [ln.strip() for ln in trap_input.strip().splitlines() if ln.strip()]
        formatted_traps = [ln if ln.startswith(("- ", "* ")) else f"- {ln}" for ln in trap_lines]
        traps_block = "\n".join(formatted_traps)
    else:
        traps_block = f"- Cần lưu ý khi triển khai {title} để tránh tái diễn lỗi trong các phiên làm việc tiếp theo."

    decision_input = getattr(args, "decision", None)
    if decision_input and decision_input.strip():
        dec_lines = [ln.strip() for ln in decision_input.strip().splitlines() if ln.strip()]
        formatted_dec = [ln if ln.startswith(("- ", "* ")) else f"- {ln}" for ln in dec_lines]
        decisions_block = "\n".join(formatted_dec)
    else:
        decisions_block = f"- Chuẩn hóa giải pháp kỹ thuật theo đề xuất và bài học từ vai trò {role}."

    content = f"""> summary: {title}

Task: LEARN        Agent: {role}        Ngày: {today_str}

# Bài học tự phản tư: {title}

> **Vai trò:** {role}  
> **Thời gian:** {now.isoformat()}  
> **Trạng thái:** inbox (Chờ harness-reflect tổng hợp)

## Bẫy & Lưu ý (Traps)
{traps_block}

## Quyết định kỹ thuật (Decisions)
{decisions_block}

## Bài học kinh nghiệm (Lessons)
{lessons_block}
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




def cmd_section(args: argparse.Namespace) -> int:
    """Trích xuất đúng 1 mục (heading) cụ thể trong file Markdown."""
    target_file = Path(args.root) / args.file if not Path(args.file).is_absolute() else Path(args.file)
    if not target_file.exists():
        target_file = ROOT / args.file
    if not target_file.exists():
        print(f"❌ Không tìm thấy tệp: {args.file}")
        return 1

    content = target_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    target_heading = args.heading.lower().strip()

    matched_lines = []
    recording = False
    current_level = 0
    found_title = ""

    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            if target_heading in title.lower():
                recording = True
                current_level = level
                found_title = title
                matched_lines.append(line)
                continue
            elif recording and level <= current_level:
                recording = False
                break
        if recording:
            matched_lines.append(line)

    if not matched_lines:
        print(f"❌ Không tìm thấy mục chứa tiêu đề '{args.heading}' trong tệp {args.file}.")
        headings = [line.strip() for line in lines if re.match(r'^#{1,4}\s+', line)]
        if headings:
            print("  Các tiêu đề có sẵn:")
            for h in headings[:10]:
                print(f"    - {h}")
        return 1

    extracted_content = "\n".join(matched_lines).strip()
    tokens = estimate_tokens(extracted_content)
    images = re.findall(r'!\[.*?\]\((.*?)\)', extracted_content)

    print(f"🎯 TRÍCH XUẤT MỤC: '{found_title}'")
    print(f"   Tệp nguồn: {args.file} | Dung lượng: ~{tokens} tokens")
    if images:
        print(f"   Ảnh sơ đồ đi kèm ({len(images)}): {', '.join(images)}")
    print("-" * 60)
    print(extracted_content)
    return 0


def cmd_image(args: argparse.Namespace) -> int:
    """Tra cứu ảnh sơ đồ mẫu từ IMAGE_REGISTRY.json theo từ khóa và loại sơ đồ."""
    reg_path = Path(args.root) / "agents/knowledge/IMAGE_REGISTRY.json"
    if not reg_path.exists():
        reg_path = ROOT / "agents/knowledge/IMAGE_REGISTRY.json"

    if not reg_path.exists():
        print("❌ Chưa tìm thấy sổ bộ ảnh IMAGE_REGISTRY.json.")
        return 1

    with open(reg_path, "r", encoding="utf-8") as fh:
        registry = json.load(fh)

    query = args.query.lower().strip()
    diagram_filter = getattr(args, "type", None)

    matched = []
    for item in registry:
        if diagram_filter and diagram_filter.lower() not in item.get("diagram_type", "").lower():
            continue
        text_corpus = f"{item.get('caption', '')} {item.get('image_name', '')} {item.get('diagram_type', '')}".lower()
        if all(word in text_corpus for word in query.split()):
            matched.append(item)

    limit = getattr(args, "limit", 5) or 5
    print(f"🎯 KẾT QUẢ TRA CỨU ẢNH SƠ ĐỒ MẪU (Từ khóa: '{args.query}', Khớp: {len(matched)} ảnh)")
    if not matched:
        print("  Không tìm thấy ảnh nào khớp. Thử tìm với từ khóa ngắn hơn (ví dụ: 'sequence', 'state', 'class', 'alt', 'qr').")
        return 0

    for idx, img in enumerate(matched[:limit], 1):
        rel = img.get("rel_path", "").replace("\\", "/")
        full_path = (ROOT / rel).resolve()
        file_uri = full_path.as_uri()
        print(f"\n  [{idx}] Mã ảnh: {img['id']} | Loại: {img['diagram_type']}")
        print(f"      Mô tả: {img['caption']}")
        print(f"      Đường dẫn cục bộ: {full_path}")
        print(f"      Cú pháp nhúng Markdown: ![{img['caption']}]({rel})")
        print(f"      URI trực tiếp: {file_uri}")

    return 0

def cmd_query_skill(args: argparse.Namespace) -> int:
    from agent_core.knowledge.skill_graph import (
        load_skills_config, load_skill_graph, scan_quarantine_skills,
        save_skill_graph, check_skill_graph_drift, search_skills
    )
    root = Path(args.root or ROOT).resolve()
    graph_path = root / "agents" / "knowledge" / "skill-graph.json"
    quarantine_dir, _, _ = load_skills_config(root)

    # 1. Tự động sinh nếu chưa có file đồ thị
    if not graph_path.exists():
        if quarantine_dir and quarantine_dir.exists():
            msg = "⚠️ Chưa có file đồ thị skill-graph.json. Đang tự động quét và xây dựng...\n"
            if getattr(args, "format", "text") == "json":
                sys.stderr.write(msg)
            else:
                print(msg, end="")
            graph_data = scan_quarantine_skills(quarantine_dir, root_dir=root)
            save_skill_graph(graph_data, graph_path)
        else:
            sys.stderr.write("❌ Lỗi: Chưa có đồ thị kỹ năng và không tìm thấy quarantine_dir.\n")
            return 1
    else:
        graph_data = load_skill_graph(graph_path)

    # 2. Tìm kiếm trên đồ thị
    results = search_skills(
        graph_data,
        args.query,
        role=args.role,
        budget=args.budget,
        limit=args.limit,
        quarantine_dir=quarantine_dir,
        root_dir=root
    )

    # 3. Khi không tìm thấy kết quả hoặc người dùng bật --auto-update:
    # Tự động kiểm tra kho quarantine xem có skill mới thêm/sửa hay không
    if (not results or getattr(args, "auto_update", False)) and quarantine_dir and quarantine_dir.exists():
        is_sync, drift = check_skill_graph_drift(graph_data, quarantine_dir)
        if not is_sync:
            added_cnt = len(drift["added"])
            mod_cnt = len(drift["modified"])
            del_cnt = len(drift["deleted"])
            msg = f"🔄 Phát hiện kho quarantine thay đổi (+{added_cnt} mới, ~{mod_cnt} sửa, -{del_cnt} xóa). Đang tự động cập nhật đồ thị...\n"
            if getattr(args, "format", "text") == "json":
                sys.stderr.write(msg)
            else:
                print(msg, end="")
            graph_data = scan_quarantine_skills(quarantine_dir, root_dir=root)
            save_skill_graph(graph_data, graph_path)
            # Tìm lại trên đồ thị mới
            results = search_skills(
                graph_data,
                args.query,
                role=args.role,
                budget=args.budget,
                limit=args.limit,
                quarantine_dir=quarantine_dir,
                root_dir=root
            )

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    role_str = f" [Vai: {args.role}]" if args.role else ""
    print(f"🎯 KẾT QUẢ TRA CỨU ĐỒ THỊ KỸ NĂNG (Từ khóa: '{args.query}'{role_str}, Ngân sách: {args.budget} tokens)")
    if not results:
        print("  🔍 Không tìm thấy kỹ năng nào phù hợp.")
        return 0

    for idx, item in enumerate(results, 1):
        status = " [ĐÃ DUYỆT]" if item.get("approved") else ""
        installed = " [ĐÃ CÀI ĐẶT]" if item.get("installed") else ""
        print(f"\n  [{idx}] {item['name']}{status}{installed} (Điểm khớp: {item.get('score', 0)})")
        print(f"      Domain: {item.get('domain')} | Vai trò: {', '.join(item.get('roles', []))}")
        print(f"      Mô tả: {item.get('description', '')[:160]}...")
        if item.get("local_path"):
            print(f"      Đường dẫn cục bộ: {item['local_path']}")
            print(f"      URI: {item.get('file_uri')}")
        else:
            primary = item.get("primary_source", {})
            print(f"      Nguồn repo: {primary.get('repo')} ({primary.get('rel_path')})")

    return 0


def cmd_skill_graph(args: argparse.Namespace) -> int:
    from agent_core.knowledge.skill_graph import (
        load_skills_config, save_skills_local_config, load_skill_graph,
        scan_quarantine_skills, save_skill_graph, check_skill_graph_drift
    )
    root = Path(args.root or ROOT).resolve()
    action = args.action
    quarantine_dir, _, cfg_source = load_skills_config(root)
    graph_path = root / "agents" / "knowledge" / "skill-graph.json"

    if action == "config":
        new_dir = getattr(args, "dir", None)
        if new_dir:
            try:
                saved = save_skills_local_config(Path(new_dir), root_dir=root)
                print(f"✅ Đã cấu hình kho kỹ năng cục bộ vào: {saved.name}")
                print(f"   Đường dẫn: {new_dir}")
                print(f"   File này nằm trong .gitignore, không bao giờ bị commit lên Git.")
                return 0
            except Exception as e:
                sys.stderr.write(f"❌ Lỗi cấu hình: {e}\n")
                return 1
        else:
            print("📋 CẤU HÌNH KHO KỸ NĂNG HIỆN TẠI:")
            print(f"   - Nguồn cấu hình: {cfg_source.name if cfg_source else 'Chưa có'}")
            print(f"   - Thư mục quarantine: {quarantine_dir if quarantine_dir else 'Chưa tìm thấy'}")
            print(f"   👉 Để đổi đường dẫn: python scripts/knowledge.py skill-graph config --dir <đường_dẫn>")
            return 0

    elif action in ("build", "sync", "update"):
        if not quarantine_dir or not quarantine_dir.exists():
            sys.stderr.write(
                "❌ Lỗi: Chưa cấu hình hoặc không tìm thấy thư mục quarantine trên máy này.\n"
                "👉 Dùng: python scripts/knowledge.py skill-graph config --dir <đường_dẫn>\n"
            )
            return 2

        if action in ("sync", "update") and graph_path.exists():
            graph_data = load_skill_graph(graph_path)
            if graph_data:
                is_sync, drift = check_skill_graph_drift(graph_data, quarantine_dir)
                if is_sync:
                    print(f"✅ Đồ thị Kỹ năng đã hoàn toàn đồng bộ với kho quarantine ({drift['total_current']} files).")
                    return 0
                print(f"🔄 Phát hiện lệch: {len(drift['added'])} thêm mới, {len(drift['modified'])} sửa, {len(drift['deleted'])} bị xóa. Đang cập nhật...")

        print(f"🔍 Đang quét kho kỹ năng tại: {quarantine_dir} ...")
        graph_data = scan_quarantine_skills(quarantine_dir, root_dir=root)
        save_skill_graph(graph_data, graph_path)
        stats = graph_data["stats"]
        print(f"✅ Đã cập nhật Đồ thị Kỹ năng: {stats['total_skills']} unique skills ({stats['total_variants']} files) từ {len(stats['repos_scanned'])} repos.")
        return 0

    elif action == "check":
        if not graph_path.exists():
            print("⚠️ Chưa có file đồ thị skill-graph.json.")
            if getattr(args, "auto_update", False) and quarantine_dir and quarantine_dir.exists():
                return cmd_skill_graph(argparse.Namespace(action="build", root=str(root)))
            return 1
        graph_data = load_skill_graph(graph_path)
        if not quarantine_dir or not quarantine_dir.exists():
            sys.stderr.write("❌ Lỗi: Thư mục quarantine không khả dụng trên máy này.\n")
            return 2
        is_sync, drift = check_skill_graph_drift(graph_data, quarantine_dir)
        if is_sync:
            print(f"✅ Đồ thị Kỹ năng đồng bộ 100% với kho quarantine ({drift['total_current']} files).")
            return 0
        else:
            print(f"⚠️ Phát hiện lệch (Drift): {len(drift['added'])} thêm mới, {len(drift['modified'])} sửa đổi, {len(drift['deleted'])} bị xóa.")
            if getattr(args, "auto_update", False):
                print("🔄 Bật --auto-update: Đang tự động cập nhật lại Đồ thị Kỹ năng...")
                return cmd_skill_graph(argparse.Namespace(action="build", root=str(root)))
            return 1

    elif action == "status":
        if not graph_path.exists():
            print("❌ Chưa có file đồ thị skill-graph.json.")
            return 1
        graph_data = load_skill_graph(graph_path)
        stats = graph_data.get("stats", {})
        print("📋 TRẠNG THÁI ĐỒ THỊ KỸ NĂNG:")
        print(f"   - Nguồn cấu hình: {cfg_source.name if cfg_source else 'Mặc định'}")
        print(f"   - Thư mục quarantine: {quarantine_dir}")
        print(f"   - Tổng số kỹ năng: {stats.get('total_skills')} unique skills")
        print(f"   - Tổng số biến thể: {stats.get('total_variants')} files")
        print(f"   - Kỹ năng đã duyệt: {stats.get('total_approved')}")
        print(f"   - Kỹ năng đã cài đặt: {stats.get('total_installed')}")
        if quarantine_dir and quarantine_dir.exists():
            is_sync, _ = check_skill_graph_drift(graph_data, quarantine_dir)
            print(f"   - Trạng thái đồng bộ: {'ĐỒNG BỘ 100% ✅' if is_sync else 'CẦN ĐỒNG BỘ ⚠️'}")
        return 0

    return 2


def _resolve_project_target(cli_root: str | None = None) -> tuple[Path, Path]:
    """Tìm thư mục dự án và file project-graph.json tương ứng."""
    if cli_root:
        p = Path(cli_root).resolve()
    else:
        cwd = Path.cwd().resolve()
        if (cwd / ".agentbase.json").exists() or (cwd / ".agent-base.json").exists() or (cwd / "doc").exists():
            p = cwd
        else:
            pj_file = ROOT / "projects.json"
            p = cwd
            if pj_file.exists():
                try:
                    with open(pj_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        def_id = data.get("default_project")
                        for item in data.get("projects", []):
                            if item.get("id") == def_id and Path(item.get("path", "")).exists():
                                p = Path(item["path"]).resolve()
                                break
                except Exception:
                    pass

    doc_dir = p / "doc" / "architecture"
    if not (p / "doc").exists() and (p / "docs").exists():
        doc_dir = p / "docs" / "architecture"
    graph_file = doc_dir / "project-graph.json"
    return p, graph_file


def cmd_query_api(args) -> int:
    """Tra cứu nhanh API, Controller, Bảng DB của dự án."""
    proj_root, graph_file = _resolve_project_target(getattr(args, "root", None))
    if not graph_file.exists():
        sys.stderr.write(f"⚠️ Chưa có đồ thị tại {graph_file}. Đang quét tự động...\n")
        build_project_graph(proj_root, graph_file)

    try:
        with open(graph_file, "r", encoding="utf-8") as f:
            graph_data = json.load(f)
    except Exception as e:
        sys.stderr.write(f"❌ Lỗi nạp đồ thị dự án: {e}\n")
        return 1

    results = query_project_graph(graph_data, args.query, service=getattr(args, "service", None), kind=getattr(args, "kind", None))
    fmt = getattr(args, "format", "text")
    if fmt == "json":
        print(json.dumps(results[:getattr(args, "limit", 10)], ensure_ascii=False, indent=2))
        return 0

    print(f"🎯 KẾT QUẢ TRA CỨU KIẾN TRÚC DỰ ÁN '{graph_data.get('project', {}).get('project_id')}' (Từ khóa: '{args.query}')")
    print(f"  Tìm thấy {len(results)} kết quả:\n")
    limit = getattr(args, "limit", 10)
    for i, node in enumerate(results[:limit], 1):
        kind = node.get("kind")
        if kind == "Endpoint":
            print(f"  [{i}] [API] {node.get('http_method')} {node.get('path')}")
            print(f"      Service: {node.get('service')} | Controller: {node.get('controller')}::{node.get('method_name')}()")
            if node.get("description"):
                print(f"      Mô tả: {node.get('description')}")
            print(f"      Tệp: {node.get('source_file')}:{node.get('line_number')}\n")
        elif kind == "Table":
            print(f"  [{i}] [BẢNG DB] {node.get('table_name')} (Service: {node.get('service')})")
            print(f"      Cột: {', '.join(node.get('columns', [])[:8])}")
            print(f"      Entities: {', '.join(node.get('entities', []))}\n")
        elif kind == "GatewayRoute":
            print(f"  [{i}] [GATEWAY ROUTE] {node.get('route_id')} -> {node.get('target_uri')}")
            print(f"      Paths: {', '.join(node.get('paths', []))}\n")
        else:
            print(f"  [{i}] [{kind}] {node.get('name') or node.get('id')}\n")
    return 0


def cmd_project_graph(args) -> int:
    """Quản lý và đồng bộ đồ thị kiến trúc dự án (build, status, sync)."""
    proj_root, graph_file = _resolve_project_target(getattr(args, "root", None))
    action = getattr(args, "action", "status")

    if action in ("build", "sync"):
        print(f"🔍 Đang quét kiến trúc dự án tại: {proj_root} ...")
        graph = build_project_graph(proj_root, graph_file)
        stats = graph.get("stats", {})
        print(f"✅ Đã cập nhật Đồ thị Dự án ({stats.get('project_id')}):")
        print(f"   - {stats.get('total_services')} services | {stats.get('total_gateway_routes')} gateway routes")
        print(f"   - {stats.get('total_endpoints')} endpoints | {stats.get('total_tables')} tables | {stats.get('total_entities')} entities")
        print(f"   - Lưu tại: {graph_file}")
        return 0

    elif action == "status":
        if not graph_file.exists():
            print(f"⚠️ Chưa có file đồ thị tại: {graph_file}")
            print("👉 Chạy: python scripts/knowledge.py project-graph sync")
            return 1
        with open(graph_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        stats = data.get("stats", {})
        print(f"📋 TRẠNG THÁI ĐỒ THỊ DỰ ÁN: {stats.get('project_id')}")
        print(f"   - Thư mục dự án: {proj_root}")
        print(f"   - Tệp đồ thị: {graph_file}")
        print(f"   - Services: {stats.get('total_services')} | Gateway Routes: {stats.get('total_gateway_routes')}")
        print(f"   - Endpoints: {stats.get('total_endpoints')} | Bảng DB: {stats.get('total_tables')}")
        print(f"   - Trạng thái: SẴN SÀNG ✅")
        return 0

    return 2


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

    # Lệnh query-skill (Tra cứu kỹ năng trong Đồ thị Kỹ năng)
    p_qsk = subparsers.add_parser("query-skill", help="Tra cứu kỹ năng JIT On-Demand trong Đồ thị Kỹ năng (Skill Graph)")
    p_qsk.add_argument("--query", "-q", required=True, help="Từ khóa tìm kiếm skill (VD: 'subagent', 'react', 'adr', 'cso')")
    p_qsk.add_argument("--root", default=".", help="Thư mục gốc agent-base (mặc định .)")
    p_qsk.add_argument("--role", help="Lọc theo vai trò (dev, architect, qa...)")
    p_qsk.add_argument("--budget", type=int, default=1200, help="Ngân sách token tối đa")
    p_qsk.add_argument("--limit", type=int, default=5, help="Số lượng kỹ năng tối đa")
    p_qsk.add_argument("--auto-update", action="store_true", help="Tự động cập nhật nếu kho quarantine có thay đổi")
    p_qsk.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    # Lệnh skill-graph (Quản lý đồ thị kỹ năng)
    p_skg = subparsers.add_parser("skill-graph", help="Quản lý và đồng bộ Đồ thị Kỹ năng (build, check, status, sync, update, config)")
    p_skg.add_argument("action", choices=["build", "check", "status", "sync", "update", "config"], help="Hành động: build (quét & tạo đồ thị), check (kiểm tra lệch), status (xem trạng thái), sync/update (tự cập nhật khi lệch), config (cấu hình đường dẫn local)")
    p_skg.add_argument("--root", default=".", help="Thư mục gốc agent-base")
    p_skg.add_argument("--auto-update", action="store_true", help="Tự động cập nhật nếu phát hiện độ lệch (dùng cho action check)")
    p_skg.add_argument("--dir", help="Đường dẫn thư mục quarantine khi dùng lệnh config")

    # Lệnh query-api (Tra cứu Endpoint, Controller, Bảng DB trong Đồ thị Dự án)
    p_qapi = subparsers.add_parser("query-api", help="Tra cứu REST Endpoint, Controller, Bảng DB trong Đồ thị Dự án (Project Graph)")
    p_qapi.add_argument("--query", "-q", required=True, help="Từ khóa tìm kiếm (VD: 'orders', 'status', 'check-duplicate')")
    p_qapi.add_argument("--root", help="Thư mục gốc của dự án (mặc định: tự nhận diện qua .agentbase.json hoặc thư mục hiện tại)")
    p_qapi.add_argument("--service", "-s", help="Lọc theo tên dịch vụ (accounting-service, ws-iam...)")
    p_qapi.add_argument("--kind", "-k", choices=["Endpoint", "Table", "Entity", "GatewayRoute"], help="Lọc theo loại node")
    p_qapi.add_argument("--limit", type=int, default=10, help="Số lượng kết quả hiển thị tối đa")
    p_qapi.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    # Lệnh project-graph (Quản lý và đồng bộ đồ thị dự án)
    p_pjg = subparsers.add_parser("project-graph", help="Quản lý và đồng bộ Đồ thị Kiến trúc Dự án (build, status, sync)")
    p_pjg.add_argument("action", choices=["build", "status", "sync"], default="status", nargs="?", help="Hành động: status (xem trạng thái), sync/build (quét và cập nhật)")
    p_pjg.add_argument("--root", help="Thư mục gốc của dự án (mặc định: tự nhận diện)")
    p_pjg.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    # Lệnh learn (Ghi nhận bài học tự học mà không làm rác context)
    p_lrn = subparsers.add_parser("learn", help="Ghi nhận bài học mới vào inbox an toàn mà không làm phình to context")
    p_lrn.add_argument("--title", required=True, help="Tiêu đề bài học kinh nghiệm")
    p_lrn.add_argument("--note", required=True, help="Nội dung bài học và hiện tượng lỗi")
    p_lrn.add_argument("--role", default="dev", help="Vai trò phát hiện bài học")
    p_lrn.add_argument("--trap", help="Bẫy và lưu ý kỹ thuật cần phòng tránh")
    p_lrn.add_argument("--decision", help="Quyết định kỹ thuật đưa ra")
    p_lrn.add_argument("--root", default=".", help="Thư mục gốc (mặc định .)")

    # Lệnh image (Tra cứu ảnh sơ đồ mẫu từ IMAGE_REGISTRY)
    p_img = subparsers.add_parser("image", help="Tra cứu ảnh sơ đồ mẫu chuẩn từ IMAGE_REGISTRY.json")
    p_img.add_argument("--query", "-q", required=True, help="Từ khóa tìm kiếm ảnh (VD: 'sequence alt', 'binary association', 'qr')")
    p_img.add_argument("--type", "-t", help="Lọc theo loại sơ đồ (class-diagram, sequence-diagram...)")
    p_img.add_argument("--limit", type=int, default=4, help="Số lượng ảnh tối đa")
    p_img.add_argument("--root", default=".", help="Thư mục gốc (mặc định .)")

    # Lệnh section (Trích xuất nguyên tử một mục duy nhất)
    p_sec = subparsers.add_parser("section", help="Trích xuất đúng một mục (heading) cụ thể trong tệp tri thức")
    p_sec.add_argument("--file", "-f", required=True, help="Đường dẫn tệp Markdown cần trích xuất")
    p_sec.add_argument("--heading", "-s", required=True, help="Tiêu đề mục cần trích xuất (VD: 'State Machine', 'Quy tắc 2')")
    p_sec.add_argument("--root", default=".", help="Thư mục gốc (mặc định .)")

    args = parser.parse_args()

    # Không chỉ định --manifest và gốc không có knowledge.manifest.json: dùng catalog của khung agent-base.
    default_name = "knowledge.manifest.json"
    alt_name = "agents/knowledge/knowledge-manifest.json"
    root = getattr(args, "root", None) or "."
    if args.command not in ("query-api", "project-graph"):
        if root == "." and not os.path.exists(os.path.join(root, default_name)) and not os.path.exists(os.path.join(root, alt_name)):
            root = str(ROOT)
            args.root = root
    if getattr(args, "manifest", None) == default_name and not os.path.exists(os.path.join(root, default_name)) \
            and os.path.exists(os.path.join(root, alt_name)):
        args.manifest = alt_name

    if args.command == "validate":
        sys.exit(cmd_validate(args))
    elif args.command == "context":
        sys.exit(cmd_context(args))
    elif args.command == "query":
        sys.exit(cmd_query(args))
    elif args.command == "query-skill":
        sys.exit(cmd_query_skill(args))
    elif args.command == "skill-graph":
        sys.exit(cmd_skill_graph(args))
    elif args.command == "query-api":
        sys.exit(cmd_query_api(args))
    elif args.command == "project-graph":
        sys.exit(cmd_project_graph(args))
    elif args.command == "learn":
        sys.exit(cmd_learn(args))
    elif args.command == "section":
        sys.exit(cmd_section(args))
    elif args.command == "image":
        sys.exit(cmd_image(args))
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
