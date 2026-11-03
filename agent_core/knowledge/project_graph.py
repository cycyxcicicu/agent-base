#!/usr/bin/env python3
"""
agent_core/knowledge/project_graph.py
Mô-đun Phân tích & Xây dựng Đồ thị Kiến trúc Dự án (Project Architecture Graph Engine)

Quét và biểu diễn kiến trúc dự án (Microservices, Gateway routes, REST Endpoints,
JPA Entities, Database Tables, Feign Clients) thành một Đồ thị liên kết hoàn chỉnh (Graph).

Đặc tính cốt lõi:
  1. Độc lập & Tái sử dụng (Core Hub): Nằm tại agent-base, dùng được cho MỌI dự án.
  2. Phân giải động: Tự động nhận diện dự án qua .agentbase.json hoặc thư mục hiện tại.
  3. Portable: 100% đường dẫn trong Graph là đường dẫn tương đối (relative path).
  4. Tự động kiểm tra độ lệch (Drift Detection): Phát hiện khi code thay đổi để cập nhật.
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set


# Regex trích xuất Java Spring Boot
RE_PACKAGE = re.compile(r'^\s*package\s+([\w\.]+);', re.MULTILINE)
RE_REST_CONTROLLER = re.compile(r'@(Rest)?Controller\b')
RE_CLASS_DECL = re.compile(r'(?:public\s+)?(?:final\s+)?class\s+(\w+)')
RE_REQUEST_MAPPING_CLASS = re.compile(r'@RequestMapping\s*\(\s*(?:value\s*=\s*|path\s*=\s*)?(?:\{?\s*"([^"]+)"|\{?\s*\'([^\']+)\')')
RE_MAPPING_METHOD = re.compile(
    r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)\s*'
    r'(?:\(\s*(?:(?:value|path)\s*=\s*)?(?:\{?\s*["\']([^"\']*)["\']|\{\s*["\']([^"\']*)["\']\s*,\s*["\']([^"\']*)["\'])?)?'
)
RE_METHOD_SIGNATURE = re.compile(
    r'(?:public|protected|private)?\s*(?:[<\w\s,>?\[\]]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)\s*(?:throws\s+[\w\s,]+)?\s*\{'
)
RE_DOC_COMMENT = re.compile(r'/\*\*?(.*?)\*/', re.DOTALL)
RE_LINE_COMMENT = re.compile(r'//\s*(.*)')

# Regex trích xuất JPA Entity & Table
RE_ENTITY = re.compile(r'@Entity\b')
RE_TABLE = re.compile(r'@Table\s*\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']')
RE_COLUMN = re.compile(r'@Column\s*\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']')
RE_ID = re.compile(r'@Id\b')
RE_RELATION = re.compile(r'@(ManyToOne|OneToMany|ManyToMany|OneToOne)\b')
RE_JOIN_COLUMN = re.compile(r'@JoinColumn\s*\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']')

# Regex trích xuất Feign Client
RE_FEIGN_CLIENT = re.compile(r'@FeignClient\s*\(\s*(?:(?:value|name)\s*=\s*)?["\']([^"\']+)["\'](?:\s*,\s*(?:url\s*=\s*["\']([^"\']*)["\']|path\s*=\s*["\']([^"\']*)["\']))?')


def _clean_path(base: str, sub: str) -> str:
    """Nối và chuẩn hóa URL path."""
    b = (base or '').strip()
    s = (sub or '').strip()
    if not b.startswith('/'):
        b = '/' + b if b else ''
    b = b.rstrip('/')
    if s and not s.startswith('/'):
        s = '/' + s
    full = b + s
    return full if full else '/'


def detect_project_context(project_root: Path) -> Dict[str, Any]:
    """Nhận diện ngữ cảnh dự án (id, name, tech stack, services)."""
    project_root = Path(project_root).resolve()
    context = {
        "project_id": project_root.name,
        "project_name": project_root.name,
        "root_rel_path": ".",
        "is_multi_service": False,
        "services": [],
        "gateway_path": None,
        "doc_dir": "doc"
    }

    # Đọc từ .agentbase.json nếu có
    ab_file = project_root / ".agentbase.json"
    if not ab_file.exists():
        ab_file = project_root / ".agent-base.json"
    if ab_file.exists():
        try:
            with open(ab_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                context["project_id"] = data.get("target_project", context["project_id"])
        except Exception:
            pass

    # Tìm các service con (Microservices)
    sub_dirs = []
    # Quét các thư mục con cấp 1 và cấp 2
    for parent in [project_root, project_root / "business", project_root / "platform-services", project_root / "platform", project_root / "frontend", project_root / "apps"]:
        if parent.exists() and parent.is_dir():
            for child in parent.iterdir():
                if child.is_dir() and not child.name.startswith('.') and (child / "pom.xml").exists() or (child / "package.json").exists() or (child / "src").exists():
                    sub_dirs.append(child)

    if sub_dirs:
        context["is_multi_service"] = True
        context["services"] = [d.name for d in sub_dirs]
        for d in sub_dirs:
            if "gateway" in d.name.lower():
                context["gateway_path"] = str(d.relative_to(project_root))

    return context


def parse_gateway_routes(gateway_dir: Path) -> List[Dict[str, Any]]:
    """Phân tích các route gateway từ file application.yml (hỗ trợ cả PyYAML và Regex)."""
    routes: List[Dict[str, Any]] = []
    if not gateway_dir.exists():
        return routes

    yml_files = list(gateway_dir.glob("**/resources/application*.yml")) + list(gateway_dir.glob("**/resources/application*.yaml"))
    for yf in yml_files:
        try:
            text = yf.read_text(encoding="utf-8", errors="ignore")
            parsed_yaml = False
            try:
                import yaml
                data = yaml.safe_load(text)
                if isinstance(data, dict):
                    gw = data.get("spring", {}).get("cloud", {}).get("gateway", {})
                    raw_routes = gw.get("routes", [])
                    if isinstance(raw_routes, list):
                        for r in raw_routes:
                            if isinstance(r, dict) and "id" in r:
                                paths = []
                                for pred in r.get("predicates", []):
                                    if isinstance(pred, str) and pred.startswith("Path="):
                                        raw_p = pred.replace("Path=", "").strip()
                                        paths.extend([p.strip() for p in raw_p.split(",") if p.strip()])
                                routes.append({
                                    "id": str(r["id"]).strip(),
                                    "target_uri": str(r.get("uri", "")).strip(),
                                    "paths": paths,
                                    "source_file": str(yf.name)
                                })
                        parsed_yaml = True
            except Exception:
                parsed_yaml = False

            if not parsed_yaml:
                # Regex fallback
                route_blocks = re.findall(r'-\s*id:\s*([A-Za-z0-9_\-]+)\s*\n\s*uri:\s*([^\n]+)\s*\n\s*predicates:\s*\n((?:\s*-\s*[^\n]+(?:\n|$))+)', text + "\n")
                for r_id, uri, preds in route_blocks:
                    paths = []
                    for p_line in preds.splitlines():
                        p_match = re.search(r'Path=([^\n]+)', p_line)
                        if p_match:
                            raw_paths = p_match.group(1).strip()
                            paths.extend([p.strip() for p in raw_paths.split(',') if p.strip()])
                    routes.append({
                        "id": r_id.strip(),
                        "target_uri": uri.strip(),
                        "paths": paths,
                        "source_file": str(yf.name)
                    })
        except Exception:
            pass
    return routes


def parse_java_controller(java_file: Path, project_root: Path, service_name: str) -> List[Dict[str, Any]]:
    """Phân tích một file Java Controller để trích xuất các endpoints."""
    endpoints: List[Dict[str, Any]] = []
    try:
        content = java_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return endpoints

    if not RE_REST_CONTROLLER.search(content):
        return endpoints

    class_match = RE_CLASS_DECL.search(content)
    class_name = class_match.group(1) if class_match else java_file.stem

    # Trích xuất base path của class
    base_path = ""
    req_class = RE_REQUEST_MAPPING_CLASS.search(content)
    if req_class:
        base_path = req_class.group(1) or req_class.group(2) or ""

    # Trích xuất các comment mô tả
    class_doc = ""
    doc_match = RE_DOC_COMMENT.search(content[:content.find("class ")]) if "class " in content else None
    if doc_match:
        class_doc = doc_match.group(1).replace('*', '').strip()
    else:
        # Thử lấy line comment ngay trước class
        lines = content[:content.find("class ")].splitlines()
        comments = [l.strip().lstrip('//').strip() for l in lines if l.strip().startswith('//')]
        if comments:
            class_doc = " | ".join(comments)

    rel_path = str(java_file.relative_to(project_root)).replace('\\', '/')
    lines = content.splitlines()

    # Tìm vị trí bắt đầu của class để chỉ quét method bên trong class
    class_line_idx = 0
    for idx, line in enumerate(lines):
        if "class " in line and not line.strip().startswith("//"):
            class_line_idx = idx
            break

    # Tìm tất cả các mapping methods bên trong class
    for i in range(class_line_idx, len(lines)):
        line = lines[i]
        m_map = RE_MAPPING_METHOD.search(line)
        if m_map:
            ann_type = m_map.group(1)
            http_method = {
                "GetMapping": "GET",
                "PostMapping": "POST",
                "PutMapping": "PUT",
                "DeleteMapping": "DELETE",
                "PatchMapping": "PATCH",
                "RequestMapping": "ALL"
            }.get(ann_type, "GET")

            sub_path = m_map.group(2) or m_map.group(3) or ""
            full_path = _clean_path(base_path, sub_path)

            # Lấy comment ngay phía trên method nếu có
            method_desc = ""
            for prev_idx in range(max(0, i - 4), i):
                prev_line = lines[prev_idx].strip()
                if prev_line.startswith('//'):
                    method_desc = prev_line.lstrip('//').strip()
                elif '*/' in prev_line:
                    # Comment block
                    method_desc = prev_line.replace('*/', '').replace('/**', '').replace('*', '').strip()

            # Tìm tên hàm ở các dòng kế tiếp
            method_name = ""
            for next_idx in range(i, min(len(lines), i + 8)):
                sig_line = lines[next_idx]
                if "(" in sig_line and not sig_line.strip().startswith("@") and not sig_line.strip().startswith("//"):
                    sig_match = RE_METHOD_SIGNATURE.search(sig_line + " {")
                    if sig_match:
                        method_name = sig_match.group(1)
                        break
                    # Fallback tìm từ ngay trước dấu mở ngoặc
                    paren_pos = sig_line.find("(")
                    tokens = sig_line[:paren_pos].split()
                    if tokens:
                        cand = tokens[-1]
                        if cand not in {"public", "private", "protected", "final", "static", "default"}:
                            method_name = cand
                            break

            endpoints.append({
                "id": f"Endpoint:{service_name}:{http_method}:{full_path}",
                "service": service_name,
                "controller": class_name,
                "method_name": method_name,
                "http_method": http_method,
                "path": full_path,
                "description": method_desc or class_doc,
                "source_file": rel_path,
                "line_number": i + 1
            })

    return endpoints


def parse_java_entity(java_file: Path, project_root: Path, service_name: str) -> Optional[Dict[str, Any]]:
    """Phân tích một file Java Entity để trích xuất cấu trúc bảng và quan hệ."""
    try:
        content = java_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    if not RE_ENTITY.search(content):
        return None

    class_match = RE_CLASS_DECL.search(content)
    if not class_match:
        return None
    class_name = class_match.group(1)

    # Trích xuất tên bảng
    table_match = RE_TABLE.search(content)
    table_name = table_match.group(1) if table_match else class_name.lower()

    # Trích xuất các cột
    columns = []
    for col_match in RE_COLUMN.finditer(content):
        col_name = col_match.group(1)
        if col_name not in columns:
            columns.append(col_name)

    # Trích xuất các quan hệ
    relations = []
    lines = content.splitlines()
    for i, line in enumerate(lines):
        rel_match = RE_RELATION.search(line)
        if rel_match:
            rel_type = rel_match.group(1)
            join_col = ""
            for next_idx in range(i, min(len(lines), i + 4)):
                jc_match = RE_JOIN_COLUMN.search(lines[next_idx])
                if jc_match:
                    join_col = jc_match.group(1)
                    break
            relations.append({
                "type": rel_type,
                "join_column": join_col
            })

    rel_path = str(java_file.relative_to(project_root)).replace('\\', '/')

    return {
        "id": f"Entity:{service_name}:{class_name}",
        "class_name": class_name,
        "table_name": table_name,
        "service": service_name,
        "columns": columns,
        "relations": relations,
        "source_file": rel_path
    }


def parse_feign_client(java_file: Path, project_root: Path, service_name: str) -> Optional[Dict[str, Any]]:
    """Phân tích Feign Client để xác định các cuộc gọi giữa các service."""
    try:
        content = java_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    fc_match = RE_FEIGN_CLIENT.search(content)
    if not fc_match:
        return None

    target_service = fc_match.group(1)
    class_match = RE_CLASS_DECL.search(content)
    client_name = class_match.group(1) if class_match else java_file.stem
    rel_path = str(java_file.relative_to(project_root)).replace('\\', '/')

    return {
        "id": f"Client:{service_name}:{client_name}",
        "client_name": client_name,
        "caller_service": service_name,
        "target_service": target_service,
        "source_file": rel_path
    }


def build_project_graph(project_root: Path, output_file: Optional[Path] = None) -> Dict[str, Any]:
    """Quét toàn bộ dự án và sinh ra Đồ thị Kiến trúc Project Graph hoàn chỉnh."""
    project_root = Path(project_root).resolve()
    context = detect_project_context(project_root)

    # Thu thập Gateway routes
    gateway_routes = []
    if context.get("gateway_path"):
        gw_dir = project_root / context["gateway_path"]
        gateway_routes = parse_gateway_routes(gw_dir)

    endpoints: List[Dict[str, Any]] = []
    entities: List[Dict[str, Any]] = []
    feign_clients: List[Dict[str, Any]] = []
    tables_map: Dict[str, Dict[str, Any]] = {}
    services_found: Set[str] = set()
    files_scanned = 0

    # Quét tất cả các file Java trong project
    for root, dirs, files in os.walk(project_root):
        # Bỏ qua các thư mục tạm / build
        dirs[:] = [d for d in dirs if d not in {'.git', 'target', 'bin', 'node_modules', '.idea', 'build'}]
        p_root = Path(root)

        # Xác định tên service từ đường dẫn tương đối
        rel_to_proj = p_root.relative_to(project_root)
        parts = rel_to_proj.parts
        service_name = parts[1] if len(parts) > 1 and parts[0] in {'business', 'platform-services', 'platform'} else (parts[0] if parts else context["project_id"])
        services_found.add(service_name)

        for file in files:
            if file.endswith('.java'):
                files_scanned += 1
                java_path = p_root / file

                # 1. Quét Controller
                eps = parse_java_controller(java_path, project_root, service_name)
                if eps:
                    endpoints.extend(eps)

                # 2. Quét Entity
                ent = parse_java_entity(java_path, project_root, service_name)
                if ent:
                    entities.append(ent)
                    t_name = ent["table_name"]
                    if t_name not in tables_map:
                        tables_map[t_name] = {
                            "id": f"Table:{t_name}",
                            "table_name": t_name,
                            "service": service_name,
                            "entities": [ent["class_name"]],
                            "columns": list(ent["columns"])
                        }
                    else:
                        tables_map[t_name]["entities"].append(ent["class_name"])
                        tables_map[t_name]["columns"] = list(set(tables_map[t_name]["columns"] + ent["columns"]))

                # 3. Quét Feign Client
                fc = parse_feign_client(java_path, project_root, service_name)
                if fc:
                    feign_clients.append(fc)

    # Xây dựng các Node và Cạnh (Nodes & Edges)
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    # Node Services
    for s_name in sorted(services_found):
        nodes.append({
            "id": f"Service:{s_name}",
            "kind": "Service",
            "name": s_name,
            "project": context["project_id"]
        })

    # Node Gateway Routes
    for gw in gateway_routes:
        g_id = f"GatewayRoute:{gw['id']}"
        nodes.append({
            "id": g_id,
            "kind": "GatewayRoute",
            "route_id": gw["id"],
            "target_uri": gw["target_uri"],
            "paths": gw["paths"],
            "source_file": gw["source_file"]
        })
        # Nối GatewayRoute -> Service tương ứng
        for s_name in services_found:
            if s_name.lower() in gw["target_uri"].lower():
                edges.append({
                    "type": "routes_to",
                    "source": g_id,
                    "target": f"Service:{s_name}"
                })

    # Node Endpoints
    for ep in endpoints:
        nodes.append({
            "id": ep["id"],
            "kind": "Endpoint",
            "service": ep["service"],
            "controller": ep["controller"],
            "http_method": ep["http_method"],
            "path": ep["path"],
            "method_name": ep["method_name"],
            "description": ep["description"],
            "source_file": ep["source_file"],
            "line_number": ep["line_number"]
        })
        edges.append({
            "type": "exposes_endpoint",
            "source": f"Service:{ep['service']}",
            "target": ep["id"]
        })

    # Node Tables & Entities
    for t_name, t_info in tables_map.items():
        nodes.append({
            "id": t_info["id"],
            "kind": "Table",
            "table_name": t_name,
            "service": t_info["service"],
            "columns": t_info["columns"],
            "entities": t_info["entities"]
        })
        edges.append({
            "type": "has_table",
            "source": f"Service:{t_info['service']}",
            "target": t_info["id"]
        })

    for ent in entities:
        nodes.append({
            "id": ent["id"],
            "kind": "Entity",
            "class_name": ent["class_name"],
            "table_name": ent["table_name"],
            "service": ent["service"],
            "source_file": ent["source_file"]
        })
        edges.append({
            "type": "persists_to",
            "source": ent["id"],
            "target": f"Table:{ent['table_name']}"
        })

    # Node Clients
    for fc in feign_clients:
        nodes.append({
            "id": fc["id"],
            "kind": "Client",
            "client_name": fc["client_name"],
            "caller_service": fc["caller_service"],
            "target_service": fc["target_service"],
            "source_file": fc["source_file"]
        })
        edges.append({
            "type": "calls_service",
            "source": f"Service:{fc['caller_service']}",
            "target": f"Service:{fc['target_service']}"
        })

    stats = {
        "project_id": context["project_id"],
        "total_services": len(services_found),
        "total_gateway_routes": len(gateway_routes),
        "total_endpoints": len(endpoints),
        "total_tables": len(tables_map),
        "total_entities": len(entities),
        "total_feign_clients": len(feign_clients),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "files_scanned": files_scanned
    }

    graph = {
        "schema_version": "1.0.0",
        "generated_at": str(Path(__file__).stat().st_mtime),
        "project": context,
        "stats": stats,
        "nodes": nodes,
        "edges": edges
    }

    # Lưu kết quả
    if output_file is None:
        doc_dir = project_root / context.get("doc_dir", "doc") / "architecture"
        doc_dir.mkdir(parents=True, exist_ok=True)
        output_file = doc_dir / "project-graph.json"
    else:
        output_file = Path(output_file).resolve()
        output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    return graph


def query_project_graph(graph_data: Dict[str, Any], query_str: str, service: Optional[str] = None, kind: Optional[str] = None) -> List[Dict[str, Any]]:
    """Tra cứu nhanh các Node trong Đồ thị Dự án (Endpoint, Table, Service, Route)."""
    q = (query_str or "").lower().strip()
    nodes = graph_data.get("nodes", [])
    results = []

    for node in nodes:
        if kind and node.get("kind", "").lower() != kind.lower():
            continue
        if service and node.get("service", "").lower() != service.lower():
            continue

        score = 0
        node_kind = node.get("kind")
        text_corpus = f"{node.get('name', '')} {node.get('path', '')} {node.get('table_name', '')} {node.get('description', '')} {node.get('class_name', '')} {node.get('controller', '')}".lower()

        if q in text_corpus:
            score += 20
        # Khớp chính xác path
        if q == node.get("path", "").lower():
            score += 50
        # Khớp tên table
        if q == node.get("table_name", "").lower():
            score += 40

        if score > 0 or not q:
            results.append((score, node))

    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results]
