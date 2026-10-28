"""agent_core.workflow.task_discovery

Khám phá task card đồng nhất (hỗ trợ cả card ở gốc và card lồng trong tasks/E*-*/).
Tuân thủ đặc tả T-11 §3, R-05 và không thêm dependency.
"""

from __future__ import annotations
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

STATUS_CANONICAL = {"todo", "doing", "review", "done", "blocked"}

LEGACY_STATUS_MAP = {
    "TODO": "todo",
    "IN_PROGRESS": "doing",
    "IN-PROGRESS": "doing",
    "DOING": "doing",
    "REVIEW": "review",
    "DONE": "done",
    "BLOCKED": "blocked",
    "CANCELLED": "cancelled",
}


def normalize_status(raw: str) -> str:
    cleaned = raw.strip()
    if cleaned.lower() in STATUS_CANONICAL:
        return cleaned.lower()
    upper = cleaned.upper()
    if upper in LEGACY_STATUS_MAP:
        return LEGACY_STATUS_MAP[upper]
    return cleaned.lower()


def parse_task_frontmatter(text: str, path: Optional[Path] = None) -> Dict[str, Any]:
    """Phân tích frontmatter YAML và metadata cơ bản từ nội dung Markdown."""
    meta: Dict[str, Any] = {
        "_text": text,
        "_path": path,
        "id": "",
        "title": "",
        "status": "todo",
        "owner": "?",
        "epic": "",
        "phase": "",
        "blocked_by": [],
        "outputs": [],
        "scope_edit": [],
        "scope_deny": [],
        "is_example": False,
    }

    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if m:
        current_key: Optional[str] = None
        for line in m.group(1).splitlines():
            # Multiline list item: '  - value'
            list_match = re.match(r"^\s+-\s+(.*)$", line)
            if list_match and current_key:
                val = list_match.group(1).strip().strip("\"'")
                meta.setdefault(current_key, []).append(val)
                continue

            # Key-value pair
            kv = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
            if kv:
                k, v = kv.group(1), kv.group(2).strip()
                current_key = k
                if v == "" or v == "[]":
                    meta[k] = []
                elif v.startswith("[") and v.endswith("]"):
                    items = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
                    meta[k] = items
                elif v.lower() in ("true", "false"):
                    meta[k] = v.lower() == "true"
                else:
                    meta[k] = v.strip("\"'")
            else:
                current_key = None

    # Tìm id nếu chưa có
    if not meta.get("id") and path:
        meta["id"] = path.stem

    # Chuẩn hóa status
    if "status" in meta and isinstance(meta["status"], str):
        meta["status"] = normalize_status(meta["status"])

    # Tìm tiêu đề
    title = meta.get("title") or ""
    if not title:
        h1 = re.search(r"^#\s+(?:[A-Za-z0-9_.-]+:\s*)?(.+)$", text, re.M)
        if h1:
            title = h1.group(1).strip()
    meta["title"] = title

    return meta


def sort_key_for_id(cid: str) -> Tuple[int, Any, str]:
    """Khóa sắp xếp tự nhiên cho ID card (hỗ trợ T-01, T-11.2, T-20)."""
    m = re.match(r"^T-(\d+)(?:\.(\d+))?$", cid)
    if m:
        main_num = int(m.group(1))
        sub_num = int(m.group(2)) if m.group(2) else 0
        return (0, (main_num, sub_num), cid)
    return (1, (0, 0), cid)


def discover_tasks(root_dir: Path | str) -> List[Dict[str, Any]]:
    """
    Quét đệ quy tìm kiếm tất cả các card T-*.md trong thư mục root_dir.
    Bắt buộc:
      - Bỏ qua các file bắt đầu bằng '_' (như _template.md).
      - Bỏ qua file BOARD.md.
      - Kiểm tra path escape qua symlink.
      - Báo lỗi nếu trùng ID ở nhiều file khác nhau.
    """
    base_path = Path(root_dir).resolve()
    if not base_path.exists():
        return []

    found_files = [p for p in base_path.rglob("T-*.md") if p.is_file() and not p.name.startswith("_")]

    cards: List[Dict[str, Any]] = []
    id_to_files: Dict[str, List[Path]] = {}

    for f in found_files:
        # Kiểm tra symlink escape
        try:
            resolved = f.resolve()
            if not str(resolved).startswith(str(base_path)):
                raise ValueError(f"Symlink escape phát hiện tại: {f} trỏ ra ngoài {base_path}")
        except Exception as e:
            raise ValueError(f"Không thể resolve đường dẫn {f}: {str(e)}")

        text = f.read_text(encoding="utf-8", errors="replace")
        meta = parse_task_frontmatter(text, f)
        cid = meta.get("id")
        if not cid:
            continue

        id_to_files.setdefault(cid, []).append(f)

        folder = ""
        if f.parent != base_path:
            try:
                folder = f.parent.relative_to(base_path).as_posix()
            except ValueError:
                folder = f.parent.name

        meta["file"] = f.relative_to(base_path).as_posix()
        meta["folder"] = folder
        cards.append(meta)

    # Kiểm tra trùng lặp ID
    duplicates = {cid: files for cid, files in id_to_files.items() if len(files) > 1}
    if duplicates:
        err_msg = ["Trùng lặp card ID ở nhiều file:"]
        for cid, files in sorted(duplicates.items()):
            file_list = ", ".join(p.as_posix() for p in files)
            err_msg.append(f"  - {cid}: {file_list}")
        raise ValueError("\n".join(err_msg))

    cards.sort(key=lambda c: sort_key_for_id(c.get("id", "")))
    return cards


def discover_task_tickets(root_dir: Path | str) -> List[Any]:
    """
    Khám phá các task card và chuyển đổi thành danh sách Ticket (tracer_bullet).
    """
    from agent_core.workflow.tracer_bullet import Ticket

    cards = discover_tasks(root_dir)
    tickets: List[Ticket] = []

    for c in cards:
        status_raw = c.get("status", "todo")
        # Ánh xạ sang UPPERCASE của Ticket
        if status_raw == "done":
            ticket_status = "DONE"
        elif status_raw in ("doing", "review"):
            ticket_status = "IN_PROGRESS"
        elif status_raw == "blocked":
            ticket_status = "BLOCKED"
        else:
            ticket_status = "TODO"

        content = c.get("_text", "")
        has_ui = bool(re.search(r"(?i)\b(UI|Giao diện|Frontend|Component)\b", content))
        has_api = bool(re.search(r"(?i)\b(API|Route|Endpoint|Controller|Backend)\b", content))
        has_db = bool(re.search(r"(?i)\b(DB|Database|Migration|Schema|Bảng|Model)\b", content))
        has_test = bool(re.search(r"(?i)\b(Test|Kiểm thử|Unit test|E2E)\b", content))

        ticket = Ticket(
            ticket_id=c["id"],
            title=c.get("title") or c["id"],
            status=ticket_status,
            blocked_by=c.get("blocked_by", []),
            has_ui=has_ui,
            has_api=has_api,
            has_db=has_db,
            has_test=has_test,
            file_path=str(c.get("_path")) if c.get("_path") else None,
        )
        tickets.append(ticket)

    return tickets
