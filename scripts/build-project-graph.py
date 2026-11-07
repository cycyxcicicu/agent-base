#!/usr/bin/env python3
"""
scripts/build-project-graph.py
CLI Sinh Đồ thị Kiến trúc Dự án (Project Architecture Graph Generator)

Tự động quét mã nguồn dự án hiện tại (hoặc thư mục chỉ định):
  - Phân tích Gateway Routes (Spring Cloud Gateway)
  - Phân tích REST Endpoints (@RestController, @RequestMapping, @GetMapping...)
  - Phân tích JPA Entities & Bảng Cơ sở Dữ liệu (@Entity, @Table, @Column...)
  - Phân tích Cuộc gọi giữa các Service (@FeignClient)

Xuất kết quả chuẩn chỉ tại: <project>/doc/architecture/project-graph.json

Sử dụng:
  python scripts/build-project-graph.py                  # Tự động quét dự án hiện tại
  python scripts/build-project-graph.py --root /path/to # Chỉ định dự án cần quét
  python scripts/build-project-graph.py --check         # Kiểm tra trạng thái đồ thị
  python scripts/build-project-graph.py --format json   # Xuất JSON ra stdout
"""

import sys
import json
import argparse
from pathlib import Path

# Đảm bảo import được agent_core từ agent-base
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from agent_core.knowledge.project_graph import (
        detect_project_context,
        build_project_graph,
        query_project_graph,
    )
except ImportError as e:
    print(f"⛔ Lỗi nạp mô-đun agent_core: {e}", file=sys.stderr)
    sys.exit(1)


def find_target_project_root(cli_root: str = None) -> Path:
    """Xác định thư mục gốc của dự án mục tiêu."""
    if cli_root:
        p = Path(cli_root).resolve()
        if p.exists() and p.is_dir():
            return p
        print(f"⛔ Đường dẫn không hợp lệ: {cli_root}", file=sys.stderr)
        sys.exit(2)

    # Thử lấy từ thư mục làm việc hiện tại (cwd)
    cwd = Path.cwd().resolve()
    if (cwd / ".agentbase.json").exists() or (cwd / ".agent-base.json").exists() or (cwd / "doc").exists() or (cwd / "business").exists():
        return cwd

    # Thử tìm trong projects.local.json hoặc projects.json nếu đang đứng ở agent-base
    pj_file = ROOT_DIR / "projects.local.json" if (ROOT_DIR / "projects.local.json").exists() else (ROOT_DIR / "projects.json")
    if pj_file.exists():
        try:
            with open(pj_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                def_id = data.get("default_project")
                for p in data.get("projects", []):
                    target_p = Path(p.get("path", "")).expanduser()
                    if p.get("id") == def_id and target_p.exists():
                        return target_p.resolve()
        except Exception:
            pass

    return cwd


def main():
    parser = argparse.ArgumentParser(description="Bộ sinh Đồ thị Kiến trúc Dự án (Project Architecture Graph)")
    parser.add_argument("--root", type=str, help="Đường dẫn thư mục gốc dự án (mặc định: tự phát hiện)")
    parser.add_argument("--output", type=str, help="Đường dẫn lưu file project-graph.json")
    parser.add_argument("--check", action="store_true", help="Kiểm tra trạng thái đồ thị hiện tại")
    parser.add_argument("--query", "-q", type=str, help="Tra cứu nhanh Endpoint hoặc Bảng DB trong đồ thị")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    args = parser.parse_args()
    proj_root = find_target_project_root(args.root)

    # Xác định đường dẫn file graph
    if args.output:
        graph_file = Path(args.output).resolve()
    else:
        # Mặc định lưu tại doc/architecture/project-graph.json
        doc_name = "doc"
        if not (proj_root / "doc").exists() and (proj_root / "docs").exists():
            doc_name = "docs"
        graph_file = proj_root / doc_name / "architecture" / "project-graph.json"

    # Chế độ tra cứu
    if args.query:
        if not graph_file.exists():
            print(f"⚠️ Chưa có file đồ thị tại: {graph_file}. Đang tiến hành quét tự động...", file=sys.stderr)
            build_project_graph(proj_root, graph_file)
        with open(graph_file, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        results = query_project_graph(graph_data, args.query)
        if args.format == "json":
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"🎯 KẾT QUẢ TRA CỨU KIẾN TRÚC DỰ ÁN (Từ khóa: '{args.query}')")
            print(f"  Tìm thấy {len(results)} kết quả:\n")
            for i, node in enumerate(results[:10], 1):
                kind = node.get("kind")
                if kind == "Endpoint":
                    print(f"  [{i}] [API] {node.get('http_method')} {node.get('path')}")
                    print(f"      Service: {node.get('service')} | Controller: {node.get('controller')}::{node.get('method_name')}()")
                    if node.get("description"):
                        print(f"      Mô tả: {node.get('description')}")
                    print(f"      Tệp: {node.get('source_file')}:{node.get('line_number')}\n")
                elif kind == "Table":
                    print(f"  [{i}] [TABLE] {node.get('table_name')} (Service: {node.get('service')})")
                    print(f"      Cột ({len(node.get('columns', []))}): {', '.join(node.get('columns', [])[:8])}")
                    print(f"      Entities: {', '.join(node.get('entities', []))}\n")
                elif kind == "GatewayRoute":
                    print(f"  [{i}] [GATEWAY ROUTE] {node.get('route_id')} -> {node.get('target_uri')}")
                    print(f"      Paths: {', '.join(node.get('paths', []))}\n")
                else:
                    print(f"  [{i}] [{kind}] {node.get('name') or node.get('id')}\n")
        return

    # Chế độ kiểm tra
    if args.check:
        if not graph_file.exists():
            print(f"⚠️ Đồ thị dự án CHƯA ĐƯỢC TẠO tại {graph_file}")
            sys.exit(1)
        with open(graph_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        stats = data.get("stats", {})
        if args.format == "json":
            print(json.dumps(stats, indent=2))
        else:
            print(f"📋 TRẠNG THÁI ĐỒ THỊ DỰ ÁN: {stats.get('project_id')}")
            print(f"   - Tệp đồ thị: {graph_file}")
            print(f"   - Số dịch vụ: {stats.get('total_services')}")
            print(f"   - Gateway Routes: {stats.get('total_gateway_routes')}")
            print(f"   - REST Endpoints: {stats.get('total_endpoints')}")
            print(f"   - Bảng cơ sở dữ liệu: {stats.get('total_tables')}")
            print(f"   - JPA Entities: {stats.get('total_entities')}")
            print(f"   - Cuộc gọi liên dịch vụ: {stats.get('total_feign_clients')}")
            print(f"   - Trạng thái: SẴN SÀNG ✅")
        return

    # Chế độ sinh / cập nhật đồ thị
    if args.format == "text":
        print(f"🚀 Bắt đầu quét mã nguồn dự án: {proj_root}...")
    graph = build_project_graph(proj_root, graph_file)
    stats = graph["stats"]

    if args.format == "json":
        print(json.dumps(graph, ensure_ascii=False, indent=2))
    else:
        print(f"\n✅ ĐÃ XÂY DỰNG XONG ĐỒ THỊ KIẾN TRÚC DỰ ÁN: {stats['project_id']}")
        print(f"   📁 Vị trí lưu: {graph_file}")
        print(f"   📦 Đã quét {stats['files_scanned']} tệp Java / YAML")
        print(f"   🏢 Dịch vụ: {stats['total_services']} services")
        print(f"   🌐 Gateway Routes: {stats['total_gateway_routes']} routes")
        print(f"   🎯 REST Endpoints: {stats['total_endpoints']} endpoints")
        print(f"   🗄️ Bảng Database: {stats['total_tables']} tables")
        print(f"   🧩 JPA Entities: {stats['total_entities']} entities")
        print(f"   🔗 Feign Clients: {stats['total_feign_clients']} inter-service calls")
        print(f"   ✨ Tổng số Nodes: {stats['total_nodes']} | Cạnh quan hệ: {stats['total_edges']}")


if __name__ == "__main__":
    main()
