"""agent_core.knowledge.context

Trích xuất ngữ cảnh tri thức theo vai trò và kiểm soát ngân sách token tất định.
Tuân thủ đặc tả T-11 §3 và các yêu cầu R-03, R-04.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
import os
from typing import Any, Dict, List, Optional, Set, Tuple

from agent_core.knowledge.catalog import Catalog, Node


def estimate_tokens(content: bytes | str) -> int:
    """Ước lượng bảo thủ số lượng tokens: ceil(UTF-8 bytes / 3)."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return math.ceil(len(content) / 3) if content else 0


@dataclass
class ContextRequest:
    role: str
    task_id: Optional[str] = None
    as_of: Optional[datetime] = None
    budget: Optional[int] = None
    include_draft: bool = False


@dataclass
class ContextBundle:
    role: str
    task_id: Optional[str]
    as_of: str
    budget: Optional[int]
    budget_method: str = "ceil(bytes/3)"
    estimated_tokens: int = 0
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    appendix: List[Dict[str, Any]] = field(default_factory=list)
    omitted_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "task_id": self.task_id,
            "as_of": self.as_of,
            "budget": self.budget,
            "budget_method": self.budget_method,
            "estimated_tokens": self.estimated_tokens,
            "node_count": len(self.nodes),
            "appendix_count": len(self.appendix),
            "omitted_count": len(self.omitted_ids),
            "nodes": self.nodes,
            "appendix": self.appendix,
            "omitted_ids": self.omitted_ids,
        }


def _read_node_content(root_dir: str, content_ref: str) -> tuple[str, int]:
    """Đọc tệp và tính số token ước lượng."""
    if not content_ref:
        return "", 0
    full_path = os.path.join(root_dir, content_ref)
    if not os.path.isfile(full_path):
        return "", 0
    try:
        with open(full_path, "rb") as f:
            raw = f.read()
        return raw.decode("utf-8", errors="replace"), estimate_tokens(raw)
    except Exception:
        return "", 0


def build_context(catalog: Catalog, request: ContextRequest) -> ContextBundle:
    """
    Xây dựng ngữ cảnh tri thức tất định theo vai và nhiệm vụ.
    """
    as_of_dt = request.as_of or datetime.now(timezone.utc)
    if as_of_dt.tzinfo is None:
        as_of_dt = as_of_dt.replace(tzinfo=timezone.utc)
    as_of_str = as_of_dt.isoformat()

    role = request.role.strip()
    target_task_id = request.task_id.strip() if request.task_id else None

    # Phân nhóm độ ưu tiên (Priority):
    # P1: Mandatory rules (Rule approved)
    # P2: Task & dependencies (nếu có task_id)
    # P3: Role-owned approved nodes
    # P4: Directly connected approved nodes
    mandatory_candidates: List[Node] = []
    task_candidates: List[Node] = []
    role_candidates: List[Node] = []
    connected_candidates: List[Node] = []
    draft_candidates: List[Node] = []

    selected_ids: Set[str] = set()

    for nid, node in catalog.nodes.items():
        # Kiểm tra draft / review
        if node.state in ("draft", "review"):
            if request.include_draft:
                draft_candidates.append(node)
            continue

        if node.state != "approved":
            continue

        # P1: Rule approved
        if node.kind == "Rule":
            mandatory_candidates.append(node)
            selected_ids.add(nid)
            continue

        # P2: Task & dependencies
        if target_task_id and (nid == target_task_id or nid == f"Task:{target_task_id}"):
            task_candidates.append(node)
            selected_ids.add(nid)
            continue

        # P3: Role-owned
        if node.owner_role == role:
            role_candidates.append(node)
            selected_ids.add(nid)
            continue

    # P4: Các node có cạnh nối tới P1, P2, P3
    for nid, node in catalog.nodes.items():
        if node.state != "approved" or nid in selected_ids:
            continue
        # Kiểm tra xem có quan hệ với node đã chọn không
        has_conn = any(r.target in selected_ids for r in node.relations)
        if has_conn:
            connected_candidates.append(node)

    # Sắp xếp tất định theo (priority, kind, id, version)
    def node_sort_key(node: Node) -> Tuple[str, str, int]:
        return (node.kind, node.id, -node.version)

    mandatory_candidates.sort(key=node_sort_key)
    task_candidates.sort(key=node_sort_key)
    role_candidates.sort(key=node_sort_key)
    connected_candidates.sort(key=node_sort_key)
    draft_candidates.sort(key=node_sort_key)

    total_tokens = 0
    final_nodes: List[Dict[str, Any]] = []
    omitted_ids: List[str] = []

    # 1. Nạp Mandatory nodes trước
    mandatory_tokens = 0
    for node in mandatory_candidates:
        content_text, t_count = _read_node_content(catalog.root_dir, node.content_ref)
        mandatory_tokens += t_count
        node_dict = dict(node.raw_data)
        node_dict["content"] = content_text
        node_dict["estimated_tokens"] = t_count
        final_nodes.append(node_dict)

    if request.budget is not None and mandatory_tokens > request.budget:
        raise ValueError(
            f"Mandatory context ({mandatory_tokens} tokens) vượt ngân sách cho phép ({request.budget} tokens)"
        )

    total_tokens = mandatory_tokens

    # 2. Nạp tiếp Task, Role, Connected candidates nếu còn budget
    remaining_candidates = task_candidates + role_candidates + connected_candidates
    for node in remaining_candidates:
        content_text, t_count = _read_node_content(catalog.root_dir, node.content_ref)
        if request.budget is not None and (total_tokens + t_count) > request.budget:
            omitted_ids.append(node.id)
            continue

        total_tokens += t_count
        node_dict = dict(node.raw_data)
        node_dict["content"] = content_text
        node_dict["estimated_tokens"] = t_count
        final_nodes.append(node_dict)

    # 3. Phụ lục Appendix (Draft / Review)
    final_appendix: List[Dict[str, Any]] = []
    for node in draft_candidates:
        content_text, t_count = _read_node_content(catalog.root_dir, node.content_ref)
        node_dict = dict(node.raw_data)
        node_dict["content"] = content_text
        node_dict["estimated_tokens"] = t_count
        node_dict["_notice"] = "DRAFT_ONLY: Đây là tài liệu dự thảo, chỉ dùng tham khảo, không phải chỉ dẫn bắt buộc"
        final_appendix.append(node_dict)

    return ContextBundle(
        role=role,
        task_id=target_task_id,
        as_of=as_of_str,
        budget=request.budget,
        budget_method="ceil(bytes/3)",
        estimated_tokens=total_tokens,
        nodes=final_nodes,
        appendix=final_appendix,
        omitted_ids=omitted_ids,
    )
