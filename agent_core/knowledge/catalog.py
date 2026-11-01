"""agent_core.knowledge.catalog

Nạp và kiểm chuẩn danh mục tri thức (Catalog) theo spec T-11 §2 và R-01, R-02.
Tuân thủ Python stdlib, không thêm dependency bên ngoài.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
import re
from typing import Any, Dict, List, Optional, Set, Tuple

DIAGNOSTIC_CODES = {
    "V00": "MALFORMED_SCHEMA",
    "V01": "DUPLICATE_NODE_ID",
    "V02": "INVALID_NODE_ID_FORMAT",
    "V03": "PATH_ESCAPE",
    "V04": "MISSING_CONTENT_FILE",
    "V05": "CONTENT_HASH_MISMATCH",
    "V06": "DANGLING_RELATION",
    "V07": "INVALID_RELATION_ENDPOINT",
    "V08": "SELF_EDGE",
    "V09": "CYCLE_DETECTED",
    "V10": "STALE_OR_INVALID_STATE",
}

VALID_KINDS = {
    "Requirement",
    "Rule",
    "Design",
    "Task",
    "Feature",
    "Scenario",
    "Skill",
    "EvalSuite",
    "Proof",
    "Approval",
    "Role",
    "Source",
}

VALID_STATES = {"draft", "review", "approved", "stale", "deprecated"}

# Quy tắc kiểu đầu -> cuối theo spec §2
VALID_RELATION_ENDPOINTS: Dict[str, Tuple[Set[str], Set[str]]] = {
    "derived_from": (VALID_KINDS, {"Source"}),
    "refines": ({"Requirement"}, {"Requirement"}),
    "constrains": ({"Rule"}, {"Requirement", "Design", "Task", "Skill"}),
    "implements": ({"Task", "Design", "Feature"}, {"Requirement"}),
    "realizes": ({"Task"}, {"Design"}),
    "verified_by": ({"Requirement", "Feature"}, {"Scenario"}),
    "executed_by": ({"Scenario"}, {"Skill"}),
    "evaluated_by": ({"Skill"}, {"EvalSuite"}),
    "evidenced_by": ({"Scenario", "Task", "EvalSuite"}, {"Proof"}),
    "approved_by": (VALID_KINDS - {"Approval"}, {"Approval"}),
    "owned_by": (VALID_KINDS - {"Role"}, {"Role"}),
    "supersedes": (VALID_KINDS, VALID_KINDS), # Kiểm tra thêm: cùng kind
    "depends_on": ({"Task"}, {"Task"}),
    # Liên quan về chủ đề (không có hướng ngữ nghĩa); tra cứu coi như cạnh hai chiều.
    "related_to": (VALID_KINDS - {"Role"}, VALID_KINDS - {"Role"}),
}

NODE_ID_REGEX = re.compile(r"^[A-Za-z0-9_-]+:[A-Za-z0-9_.-]+$")


@dataclass
class Diagnostic:
    code: str
    message: str
    node_id: Optional[str] = None
    path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": DIAGNOSTIC_CODES.get(self.code, "UNKNOWN"),
            "node_id": self.node_id,
            "path": self.path,
            "message": self.message,
        }


@dataclass
class Relation:
    type: str
    target: str


@dataclass
class Node:
    id: str
    kind: str
    title: str
    state: str
    version: int
    content_ref: str
    content_sha256: str
    provenance: List[str] = field(default_factory=list)
    owner_role: str = ""
    relations: List[Relation] = field(default_factory=list)
    updated_at: Optional[str] = None
    review_due_at: Optional[str] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Catalog:
    root_dir: str
    schema_version: int = 1
    nodes: Dict[str, Node] = field(default_factory=dict)
    raw_nodes: List[Dict[str, Any]] = field(default_factory=list)
    load_errors: List[Diagnostic] = field(default_factory=list)
    duplicate_ids: List[str] = field(default_factory=list)


def load_catalog(root_dir: str, filename: str = "knowledge.manifest.json") -> Catalog:
    catalog_path = os.path.join(root_dir, filename)
    catalog = Catalog(root_dir=root_dir)

    if not os.path.isfile(catalog_path):
        # Fallback thử các biến thể phổ biến nếu filename mặc định không thấy
        candidate_alts = [
            os.path.join(root_dir, "knowledge-manifest.json"),
            os.path.join(root_dir, "agents", "knowledge", "knowledge-manifest.json"),
            os.path.join(root_dir, "agents", "knowledge", "knowledge.manifest.json"),
        ]
        found_alt = False
        for alt in candidate_alts:
            if os.path.isfile(alt):
                catalog_path = alt
                found_alt = True
                break
        if not found_alt:
            catalog.load_errors.append(
                Diagnostic(
                    code="V00",
                    message=f"Tệp manifest không tồn tại: {catalog_path}",
                    path=catalog_path,
                )
            )
            return catalog

    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        catalog.load_errors.append(
            Diagnostic(
                code="V00",
                message=f"Lỗi cú pháp JSON trong manifest: {str(e)}",
                path=catalog_path,
            )
        )
        return catalog

    if not isinstance(data, dict):
        catalog.load_errors.append(
            Diagnostic(
                code="V00",
                message="Dữ liệu manifest phải là một JSON Object",
                path=catalog_path,
            )
        )
        return catalog

    catalog.schema_version = data.get("schema_version", 0)
    raw_nodes = data.get("nodes")
    if not isinstance(raw_nodes, list):
        catalog.load_errors.append(
            Diagnostic(
                code="V00",
                message="Trường 'nodes' phải là một danh sách",
                path=catalog_path,
            )
        )
        return catalog

    catalog.raw_nodes = raw_nodes
    seen_ids: Set[str] = set()

    for item in raw_nodes:
        if not isinstance(item, dict):
            continue
        node_id = item.get("id")
        if not isinstance(node_id, str):
            continue

        if node_id in seen_ids:
            catalog.duplicate_ids.append(node_id)
        else:
            seen_ids.add(node_id)

        relations: List[Relation] = []
        for r in item.get("relations", []):
            if isinstance(r, dict) and "type" in r and "target" in r:
                relations.append(Relation(type=str(r["type"]), target=str(r["target"])))

        node = Node(
            id=node_id,
            kind=str(item.get("kind", "")),
            title=str(item.get("title", "")),
            state=str(item.get("state", "")),
            version=int(item.get("version", 1)) if str(item.get("version", "")).isdigit() else 1,
            content_ref=str(item.get("content_ref", "")),
            content_sha256=str(item.get("content_sha256", "")),
            provenance=[str(p) for p in item.get("provenance", [])] if isinstance(item.get("provenance"), list) else [],
            owner_role=str(item.get("owner_role", "")),
            relations=relations,
            updated_at=item.get("updated_at"),
            review_due_at=item.get("review_due_at"),
            raw_data=item,
        )
        # Chỉ lưu bản đầu tiên vào dict nếu chưa có
        if node_id not in catalog.nodes:
            catalog.nodes[node_id] = node

    return catalog


def validate_catalog(catalog: Catalog, as_of: Optional[datetime] = None) -> List[Diagnostic]:
    diags: List[Diagnostic] = []

    # 1. Các lỗi nạp từ trước
    diags.extend(catalog.load_errors)

    # V00: schema_version
    if catalog.schema_version != 1:
        diags.append(
            Diagnostic(
                code="V00",
                message=f"schema_version không hợp lệ: {catalog.schema_version} (yêu cầu = 1)",
            )
        )

    # V01: duplicate IDs
    for dup_id in catalog.duplicate_ids:
        diags.append(
            Diagnostic(
                code="V01",
                node_id=dup_id,
                message=f"Phát hiện trùng lặp node ID: {dup_id}",
            )
        )

    # 2. Kiểm tra từng node
    for raw in catalog.raw_nodes:
        if not isinstance(raw, dict):
            diags.append(Diagnostic(code="V00", message="Node không phải là object hợp lệ"))
            continue

        node_id = raw.get("id")
        # Kiểm tra required fields
        required_fields = [
            "id",
            "kind",
            "title",
            "state",
            "version",
            "content_ref",
            "content_sha256",
            "provenance",
            "owner_role",
            "relations",
        ]
        missing = [f for f in required_fields if f not in raw]
        if missing:
            diags.append(
                Diagnostic(
                    code="V00",
                    node_id=node_id,
                    message=f"Node thiếu các trường bắt buộc: {', '.join(missing)}",
                )
            )

        if not isinstance(node_id, str):
            continue

        # V02: format ID
        if not NODE_ID_REGEX.match(node_id):
            diags.append(
                Diagnostic(
                    code="V02",
                    node_id=node_id,
                    message=f"ID '{node_id}' không đúng định dạng TYPE:slug",
                )
            )
        else:
            id_prefix = node_id.split(":", 1)[0]
            kind = raw.get("kind")
            if kind and id_prefix != kind:
                diags.append(
                    Diagnostic(
                        code="V02",
                        node_id=node_id,
                        message=f"ID prefix '{id_prefix}' không khớp với kind '{kind}'",
                    )
                )

        kind = raw.get("kind")
        if kind not in VALID_KINDS:
            diags.append(
                Diagnostic(
                    code="V00",
                    node_id=node_id,
                    message=f"Kind '{kind}' không hợp lệ",
                )
            )

        state = raw.get("state")
        if state not in VALID_STATES:
            diags.append(
                Diagnostic(
                    code="V00",
                    node_id=node_id,
                    message=f"State '{state}' không hợp lệ",
                )
            )

        content_ref = raw.get("content_ref")
        if isinstance(content_ref, str):
            # V03: Path escape check
            norm = os.path.normpath(content_ref)
            if (
                os.path.isabs(content_ref)
                or norm.startswith("..")
                or "/../" in content_ref.replace("\\", "/")
            ):
                diags.append(
                    Diagnostic(
                        code="V03",
                        node_id=node_id,
                        path=content_ref,
                        message=f"content_ref '{content_ref}' thoát khỏi root hoặc là đường dẫn tuyệt đối",
                    )
                )
            else:
                abs_content_path = os.path.abspath(os.path.join(catalog.root_dir, content_ref))
                root_abs = os.path.abspath(catalog.root_dir)
                if not abs_content_path.startswith(root_abs):
                    diags.append(
                        Diagnostic(
                            code="V03",
                            node_id=node_id,
                            path=content_ref,
                            message=f"content_ref '{content_ref}' giải quyết ra ngoài root",
                        )
                    )
                elif not os.path.isfile(abs_content_path):
                    # V04: Missing content file
                    diags.append(
                        Diagnostic(
                            code="V04",
                            node_id=node_id,
                            path=content_ref,
                            message=f"Tệp nội dung không tồn tại: {content_ref}",
                        )
                    )
                else:
                    # V05: Hash mismatch
                    expected_hash = raw.get("content_sha256")
                    try:
                        with open(abs_content_path, "rb") as cf:
                            raw_bytes = cf.read().replace(b"\r\n", b"\n")
                            actual_hash = hashlib.sha256(raw_bytes).hexdigest()
                        if expected_hash and actual_hash.lower() != expected_hash.lower():
                            diags.append(
                                Diagnostic(
                                    code="V05",
                                    node_id=node_id,
                                    path=content_ref,
                                    message=f"Hash nội dung không khớp (kỳ vọng {expected_hash}, thực tế {actual_hash})",
                                )
                            )
                    except Exception as e:
                        diags.append(
                            Diagnostic(
                                code="V05",
                                node_id=node_id,
                                path=content_ref,
                                message=f"Không thể đọc tệp để tính hash: {str(e)}",
                            )
                        )

        # V10: Stale check dựa vào review_due_at
        review_due_at = raw.get("review_due_at")
        if review_due_at and as_of:
            try:
                # Parse ISO timestamp
                due_dt = datetime.fromisoformat(review_due_at.replace("Z", "+00:00"))
                if as_of.tzinfo is None:
                    as_of = as_of.replace(tzinfo=timezone.utc)
                if due_dt.tzinfo is None:
                    due_dt = due_dt.replace(tzinfo=timezone.utc)

                if as_of >= due_dt and state not in ("stale", "deprecated"):
                    diags.append(
                        Diagnostic(
                            code="V10",
                            node_id=node_id,
                            message=f"Node đã quá hạn xem xét ({review_due_at} so với mốc {as_of.isoformat()}), cần chuyển sang stale",
                        )
                    )
            except Exception:
                diags.append(
                    Diagnostic(
                        code="V10",
                        node_id=node_id,
                        message=f"Thời điểm review_due_at không đúng chuẩn ISO: {review_due_at}",
                    )
                )

    # 3. Kiểm tra các quan hệ (Relations)
    for node_id, node in catalog.nodes.items():
        src_kind = node.kind
        for rel in node.relations:
            # V08: Self-edge
            if rel.target == node_id:
                diags.append(
                    Diagnostic(
                        code="V08",
                        node_id=node_id,
                        message=f"Quan hệ tự trỏ vào chính nó: {rel.type} -> {rel.target}",
                    )
                )
                continue

            # V06: Dangling relation
            if rel.target not in catalog.nodes:
                diags.append(
                    Diagnostic(
                        code="V06",
                        node_id=node_id,
                        message=f"Quan hệ trỏ tới node không tồn tại trong catalog: {rel.type} -> {rel.target}",
                    )
                )
                continue

            target_node = catalog.nodes[rel.target]
            target_kind = target_node.kind

            # V07: Endpoint types validation
            if rel.type not in VALID_RELATION_ENDPOINTS:
                diags.append(
                    Diagnostic(
                        code="V07",
                        node_id=node_id,
                        message=f"Loại quan hệ không nằm trong allowlist: '{rel.type}'",
                    )
                )
            else:
                allowed_src, allowed_tgt = VALID_RELATION_ENDPOINTS[rel.type]
                if src_kind not in allowed_src or target_kind not in allowed_tgt:
                    diags.append(
                        Diagnostic(
                            code="V07",
                            node_id=node_id,
                            message=f"Quan hệ '{rel.type}' không hợp lệ giữa nguồn {src_kind} và đích {target_kind}",
                        )
                    )
                elif rel.type == "supersedes" and src_kind != target_kind:
                    diags.append(
                        Diagnostic(
                            code="V07",
                            node_id=node_id,
                            message=f"Quan hệ supersedes phải cùng kind ({src_kind} != {target_kind})",
                        )
                    )

    # 4. V09: Cycle detection cho depends_on, refines, supersedes
    cycle_rel_types = ["depends_on", "refines", "supersedes"]
    for rel_type in cycle_rel_types:
        adj: Dict[str, List[str]] = {nid: [] for nid in catalog.nodes}
        for nid, node in catalog.nodes.items():
            for r in node.relations:
                if r.type == rel_type and r.target in catalog.nodes:
                    adj[nid].append(r.target)

        visited: Dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited
        cycle_nodes: Set[str] = set()

        def dfs(curr: str, path: List[str]):
            visited[curr] = 1
            path.append(curr)
            for neighbor in adj.get(curr, []):
                if visited.get(neighbor, 0) == 1:
                    # Tìm thấy cycle
                    cycle_start_idx = path.index(neighbor)
                    cycle = path[cycle_start_idx:]
                    for c_node in cycle:
                        cycle_nodes.add(c_node)
                elif visited.get(neighbor, 0) == 0:
                    dfs(neighbor, path)
            path.pop()
            visited[curr] = 2

        for nid in catalog.nodes:
            if visited.get(nid, 0) == 0:
                dfs(nid, [])

        if cycle_nodes:
            for cn in sorted(cycle_nodes):
                diags.append(
                    Diagnostic(
                        code="V09",
                        node_id=cn,
                        message=f"Phát hiện chu trình phụ thuộc vòng trong quan hệ '{rel_type}' liên quan tới node {cn}",
                    )
                )

    return diags
