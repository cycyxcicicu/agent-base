#!/usr/bin/env python3
"""scripts/build-skill-graph.py

Trình xây dựng, kiểm chuẩn và đồng bộ Đồ thị Kỹ năng (Skill Knowledge Graph).
Hỗ trợ:
  1. Quét toàn bộ thư mục quarantine (đọc qua skills.config.local.json hoặc tham số).
  2. Xây dựng đồ thị kỹ năng chuẩn hóa, không phụ thuộc đường dẫn máy chủ (portable).
  3. Kiểm tra độ lệch (drift check) khi có skill mới được thêm hoặc sửa đổi.
  4. Tra cứu nhanh kỹ năng theo từ khóa và vai trò.

Sử dụng:
  python scripts/build-skill-graph.py                 # Quét & cập nhật agents/knowledge/skill-graph.json
  python scripts/build-skill-graph.py --check         # Kiểm tra độ lệch (exit 0 nếu khớp, exit 1 nếu lệch)
  python scripts/build-skill-graph.py --status        # Xem thống kê tổng quan
  python scripts/build-skill-graph.py --query "react" # Tìm kiếm kỹ năng
"""

from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path

# Cấu hình UTF-8 cho Windows console
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

from agent_core.knowledge.skill_graph import (
    load_skills_config,
    save_skills_local_config,
    scan_quarantine_skills,
    save_skill_graph,
    load_skill_graph,
    check_skill_graph_drift,
    search_skills,
    resolve_skill_path
)


def cmd_build(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    quarantine_dir = Path(args.quarantine_dir).resolve() if args.quarantine_dir else None

    if not quarantine_dir:
        quarantine_dir, _, cfg_source = load_skills_config(root)
        if not quarantine_dir or not quarantine_dir.exists():
            sys.stderr.write(
                f"❌ Lỗi: Chưa cấu hình hoặc không tìm thấy thư mục quarantine trên máy này.\n"
                f"👉 Hãy tạo file 'skills.config.local.json' từ 'skills.config.template.json' và điền đường dẫn.\n"
            )
            return 2

    output_path = Path(args.output).resolve() if args.output else (root / "agents" / "knowledge" / "skill-graph.json")

    start_time = time.time()
    print(f"🔍 Đang quét kho kỹ năng tại: {quarantine_dir} ...")
    graph_data = scan_quarantine_skills(quarantine_dir, root_dir=root)
    elapsed = time.time() - start_time

    save_skill_graph(graph_data, output_path)

    stats = graph_data["stats"]
    print(f"✅ Đã tạo Đồ thị Kỹ năng thành công trong {elapsed:.2f}s:")
    print(f"   - File đồ thị: {output_path.relative_to(root) if output_path.is_relative_to(root) else output_path}")
    print(f"   - Tổng số kỹ năng độc nhất (Unique Skills): {stats['total_skills']}")
    print(f"   - Tổng số biến thể file (Total Variants): {stats['total_variants']}")
    print(f"   - Số kỹ năng đã duyệt (Approved): {stats['total_approved']}")
    print(f"   - Số kỹ năng đã cài đặt trong dự án: {stats['total_installed']}")
    print(f"   - Số repository nguồn: {len(stats['repos_scanned'])} ({', '.join(stats['repos_scanned'][:6])}...)")

    print("\n📊 Phân bổ theo 8 Taxonomy Domains:")
    for domain, count in sorted(graph_data["taxonomy_domains"].items(), key=lambda x: x[1], reverse=True):
        print(f"   * {domain:<15}: {count} skills")

    return 0


def cmd_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    quarantine_dir = Path(args.quarantine_dir).resolve() if args.quarantine_dir else None

    if not quarantine_dir:
        quarantine_dir, _, _ = load_skills_config(root)
        if not quarantine_dir or not quarantine_dir.exists():
            sys.stderr.write("❌ Lỗi: Thư mục quarantine không tồn tại trên máy này.\n")
            return 2

    graph_path = Path(args.output).resolve() if args.output else (root / "agents" / "knowledge" / "skill-graph.json")
    if not graph_path.exists():
        print(f"⚠️ Chưa có file đồ thị tại: {graph_path.name}. Cần chạy build trước.")
        if args.auto_update:
            return cmd_build(args)
        return 1

    graph_data = load_skill_graph(graph_path)
    if not graph_data:
        sys.stderr.write("❌ Lỗi: Không thể nạp file đồ thị kỹ năng.\n")
        return 1

    is_sync, drift = check_skill_graph_drift(graph_data, quarantine_dir)

    if is_sync:
        print(f"✅ Đồ thị Kỹ năng hoàn toàn ĐỒNG BỘ với kho quarantine ({drift['total_current']} files).")
        return 0
    else:
        print("⚠️ PHÁT HIỆN ĐỘ LỆCH (DRIFT) TRONG KHO KỸ NĂNG:")
        if drift["added"]:
            print(f"   ➕ Có {len(drift['added'])} skill mới được thêm vào:")
            for p in drift["added"][:5]:
                print(f"      - {p}")
            if len(drift["added"]) > 5:
                print(f"      ... và {len(drift['added']) - 5} skills khác")
        if drift["modified"]:
            print(f"   🔄 Có {len(drift['modified'])} skill bị sửa đổi nội dung:")
            for p in drift["modified"][:5]:
                print(f"      - {p}")
        if drift["deleted"]:
            print(f"   ➖ Có {len(drift['deleted'])} skill đã bị xóa khỏi quarantine:")
            for p in drift["deleted"][:5]:
                print(f"      - {p}")

        if args.auto_update:
            print("\n🔄 Đang tự động cập nhật lại Đồ thị Kỹ năng...")
            return cmd_build(args)

        print("\n👉 Hãy chạy `python scripts/build-skill-graph.py` để cập nhật lại đồ thị.")
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    graph_path = Path(args.output).resolve() if args.output else (root / "agents" / "knowledge" / "skill-graph.json")
    quarantine_dir, skills_dir, cfg_source = load_skills_config(root)

    print("📋 TRẠNG THÁI HỆ THỐNG KỸ NĂNG (SKILL ECOSYSTEM):")
    print(f"   - Nguồn cấu hình: {cfg_source.name if cfg_source else 'Mặc định'}")
    print(f"   - Thư mục quarantine: {quarantine_dir if quarantine_dir else 'Chưa tìm thấy'}")
    print(f"   - Thư mục cài đặt: {skills_dir}")

    if not graph_path.exists():
        print(f"   - Đồ thị Kỹ năng: Chưa tạo ({graph_path.name})")
        return 1

    graph_data = load_skill_graph(graph_path)
    if not graph_data:
        print("   - Đồ thị Kỹ năng: Lỗi định dạng JSON")
        return 1

    stats = graph_data["stats"]
    print(f"   - Đồ thị Kỹ năng: SẴN SÀNG (Phiên bản schema {graph_data.get('schema_version', 1)})")
    print(f"   - Thời gian sinh: {graph_data.get('generated_at')}")
    print(f"   - Tổng số kỹ năng: {stats['total_skills']} unique skills ({stats['total_variants']} files)")
    print(f"   - Kỹ năng đã duyệt: {stats['total_approved']}")
    print(f"   - Kỹ năng đã cài đặt: {stats['total_installed']}")
    print(f"   - Repositories: {', '.join(stats['repos_scanned'])}")

    if quarantine_dir and quarantine_dir.exists():
        is_sync, _ = check_skill_graph_drift(graph_data, quarantine_dir)
        print(f"   - Trạng thái đồng bộ: {'ĐỒNG BỘ 100% ✅' if is_sync else 'CẦN CẬP NHẬT ⚠️'}")

    return 0


def cmd_query(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    graph_path = Path(args.output).resolve() if args.output else (root / "agents" / "knowledge" / "skill-graph.json")
    quarantine_dir, _, _ = load_skills_config(root)

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
            sys.stderr.write("❌ Lỗi: Chưa có file đồ thị skill-graph.json và không tìm thấy quarantine. Hãy chạy build trước.\n")
            return 1
    else:
        graph_data = load_skill_graph(graph_path)

    if not graph_data:
        sys.stderr.write("❌ Lỗi: File đồ thị không hợp lệ.\n")
        return 1

    results = search_skills(
        graph_data,
        args.query,
        role=args.role,
        budget=args.budget,
        limit=args.limit,
        quarantine_dir=quarantine_dir,
        root_dir=root
    )

    # Tự động cập nhật nếu không tìm thấy hoặc người dùng bật --auto-update
    if (not results or getattr(args, "auto_update", False)) and quarantine_dir and quarantine_dir.exists():
        is_sync, drift = check_skill_graph_drift(graph_data, quarantine_dir)
        if not is_sync:
            msg = "🔄 Phát hiện skill mới hoặc thay đổi trong kho quarantine, đang tự động đồng bộ Đồ thị Kỹ năng...\n"
            if getattr(args, "format", "text") == "json":
                sys.stderr.write(msg)
            else:
                print(msg, end="")
            graph_data = scan_quarantine_skills(quarantine_dir, root_dir=root)
            save_skill_graph(graph_data, graph_path)
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
    print(f"🎯 KẾT QUẢ TRA CỨU KỸ NĂNG (Từ khóa: '{args.query}'{role_str}, Ngân sách: {args.budget} tokens):")
    if not results:
        print("   🔍 Không tìm thấy kỹ năng nào phù hợp.")
        return 0

    for idx, item in enumerate(results, 1):
        status = " [ĐÃ DUYỆT]" if item.get("approved") else ""
        installed = " [ĐÃ CÀI ĐẶT]" if item.get("installed") else ""
        print(f"\n   [{idx}] {item['name']}{status}{installed} (Điểm khớp: {item.get('score', 0)})")
        print(f"       Domain: {item.get('domain')} | Vai trò: {', '.join(item.get('roles', []))}")
        print(f"       Mô tả: {item.get('description', '')[:160]}...")
        if item.get("local_path"):
            print(f"       Đường dẫn cục bộ: {item['local_path']}")
            print(f"       URI: {item.get('file_uri')}")
        else:
            primary = item.get("primary_source", {})
            print(f"       Nguồn repo: {primary.get('repo')} ({primary.get('rel_path')})")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Quản lý và Đồng bộ Đồ thị Kỹ năng (Skill Knowledge Graph)")
    parser.add_argument("--root", default=str(ROOT), help="Thư mục gốc agent-base")
    parser.add_argument("--quarantine-dir", help="Đường dẫn ghi đè thư mục quarantine trong phiên chạy")
    parser.add_argument("--set-dir", help="Lưu đường dẫn quarantine vào skills.config.local.json (file riêng của máy, nằm trong .gitignore)")
    parser.add_argument("--output", help="Đường dẫn file đồ thị (mặc định agents/knowledge/skill-graph.json)")
    parser.add_argument("--check", action="store_true", help="Kiểm tra độ lệch giữa quarantine và graph")
    parser.add_argument("--auto-update", action="store_true", help="Tự động cập nhật nếu phát hiện lệch")
    parser.add_argument("--sync", "--update", dest="sync", action="store_true", help="Đồng bộ lại đồ thị kỹ năng nếu có lệch")
    parser.add_argument("--status", action="store_true", help="Xem báo cáo trạng thái hệ sinh thái kỹ năng")
    parser.add_argument("--query", "-q", help="Tra cứu kỹ năng theo từ khóa")
    parser.add_argument("--role", help="Lọc kỹ năng theo vai trò")
    parser.add_argument("--budget", type=int, default=1200, help="Ngân sách token tối đa")
    parser.add_argument("--limit", type=int, default=5, help="Số lượng kết quả hiển thị")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng xuất")

    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.set_dir:
        try:
            saved = save_skills_local_config(Path(args.set_dir), root_dir=root)
            print(f"✅ Đã lưu cấu hình máy cục bộ vào: {saved.name}")
            print(f"   Đường dẫn quarantine: {args.set_dir}")
            print(f"   File này nằm trong .gitignore, tuyệt đối không bị commit lên Git.")
        except Exception as e:
            sys.stderr.write(f"❌ Lỗi: {e}\n")
            sys.exit(1)

    if args.query:
        sys.exit(cmd_query(args))
    elif args.sync:
        args.auto_update = True
        sys.exit(cmd_check(args))
    elif args.check:
        sys.exit(cmd_check(args))
    elif args.status:
        sys.exit(cmd_status(args))
    else:
        sys.exit(cmd_build(args))


if __name__ == "__main__":
    main()

