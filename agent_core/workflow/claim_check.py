"""agent_core.workflow.claim_check

Kiểm tra điều kiện nhận task (Claim Check) theo 5 tiêu chí: G0, SEQ, DoR, BLK, PLAN.
Cung cấp chẩn đoán cố vấn độc lập, không thay thế cơ chế cưỡng chế cấp host.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import fnmatch
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set

from agent_core.workflow.task_discovery import (
    discover_tasks,
    parse_task_frontmatter,
)


@dataclass
class ClaimCheckResult:
    card_id: str
    card_path: str
    verdict: str  # "PASS" | "BLOCKED"
    checks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    advisory_notice: str = (
        "ADVISORY ONLY: Đây là chẩn đoán cố vấn tiền điều kiện nhận việc (Cổng 4 PDF), "
        "chưa phải cưỡng chế cấp host."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "card_id": self.card_id,
            "card_path": self.card_path,
            "verdict": self.verdict,
            "checks": self.checks,
            "advisory_notice": self.advisory_notice,
        }


def _glob_to_regex(pat: str) -> str:
    """Chuyển đổi glob pattern (hỗ trợ cả ** và *) sang regex chuẩn."""
    # Chuẩn hóa đường dẫn dấu gạch chéo
    p = pat.replace("\\", "/")
    # Escape các ký tự regex đặc biệt trừ * và ?
    p = re.escape(p)
    # Khôi phục ** và *
    p = p.replace(r"\*\*", ".*")
    p = p.replace(r"\*", "[^/]*")
    p = p.replace(r"\?", "[^/]")
    return f"^{p}$"


def _patterns_overlap(pat1: str, pat2: str) -> bool:
    """Kiểm tra xem hai glob pattern có khả năng chạm cùng tập file hay không."""
    p1 = pat1.replace("\\", "/").strip()
    p2 = pat2.replace("\\", "/").strip()

    if p1 == p2:
        return True

    # Nếu một trong hai chứa wildcard, kiểm tra đối sánh chéo
    r1 = re.compile(_glob_to_regex(p1))
    r2 = re.compile(_glob_to_regex(p2))

    # Nếu p1 khớp trực tiếp pattern của p2 hoặc ngược lại
    if r1.match(p2) or r2.match(p1):
        return True

    # Kiểm tra prefix thư mục chung nếu có wildcard
    if "*" in p1 or "*" in p2:
        p1_base = p1.split("*")[0]
        p2_base = p2.split("*")[0]
        if p1_base.startswith(p2_base) or p2_base.startswith(p1_base):
            # Cùng chung tiền tố thư mục
            ext1 = os.path.splitext(p1)[1]
            ext2 = os.path.splitext(p2)[1]
            if not ext1 or not ext2 or ext1 == ext2 or "*" in (ext1 + ext2):
                return True

    return False


def check_task_claim(card_path: Path | str, tasks_root: Optional[Path | str] = None) -> ClaimCheckResult:
    card_p = Path(card_path).resolve()
    if not card_p.is_file():
        raise FileNotFoundError(f"Card không tồn tại: {card_p}")

    text = card_p.read_text(encoding="utf-8", errors="replace")
    meta = parse_task_frontmatter(text, card_p)
    card_id = meta.get("id") or card_p.stem

    if tasks_root is None:
        # Tự tìm thư mục tasks cha
        curr = card_p.parent
        while curr != curr.parent:
            if curr.name == "tasks":
                tasks_root = curr
                break
            curr = curr.parent
        if tasks_root is None:
            tasks_root = card_p.parent

    all_cards = discover_tasks(tasks_root)
    card_map = {c["id"]: c for c in all_cards}

    checks: Dict[str, Dict[str, Any]] = {}

    # 1. G0: User Approval Check
    # Dấu duyệt: - [x] **Người dùng duyệt...**: <tên> · <ngày>
    user_approved = False
    m_approval = re.search(
        r"-\s*\[x\]\s*\*\*Người dùng duyệt[^*]*\*\*:\s*([^·\n]+)\s*·\s*(\d{4}-\d{2}-\d{2})",
        text,
        re.I,
    )
    if m_approval:
        user_approved = True

    if user_approved:
        checks["G0"] = {"pass": True, "message": "Card đã có dấu người dùng duyệt hợp lệ."}
    else:
        checks["G0"] = {
            "pass": False,
            "message": "Card chưa được người dùng duyệt bằng file (- [x] **Người dùng duyệt...**).",
        }

    # 2. SEQ: Sequential Dependencies Check
    blocked_by = meta.get("blocked_by", [])
    unmet_deps: List[str] = []
    for dep_id in blocked_by:
        dep_card = card_map.get(dep_id)
        if not dep_card:
            unmet_deps.append(f"{dep_id} (không tìm thấy card)")
        elif dep_card.get("status") != "done":
            unmet_deps.append(f"{dep_id} (đang {dep_card.get('status')})")

    if not unmet_deps:
        checks["SEQ"] = {"pass": True, "message": "Toàn bộ task phụ thuộc đã DONE."}
    else:
        checks["SEQ"] = {
            "pass": False,
            "message": f"Các task phụ thuộc chưa hoàn thành: {', '.join(unmet_deps)}.",
        }

    # 3. DoR: Definition of Ready
    dor_failures: List[str] = []
    has_target = bool(re.search(r"##\s+Mục tiêu\s*\n\s*\S+", text))
    if not has_target:
        dor_failures.append("Thiếu mục 'Mục tiêu' hoặc nội dung rỗng")

    has_dod = bool(re.search(r"##\s+Tiêu chí xong\s*\n[\s\S]*?-\s*\[[ x]\]", text))
    if not has_dod:
        dor_failures.append("Thiếu mục 'Tiêu chí xong' hoặc không có checklist")

    scope_edit = meta.get("scope_edit", [])
    if not scope_edit:
        dor_failures.append("scope_edit rỗng (chưa định nghĩa phạm vi sửa)")

    has_subtasks = bool(re.search(r"##\s+Phân Rã Subtasks[\s\S]*?-\s*\[[ x]\].*?Handoff:", text, re.I))
    if not has_subtasks:
        dor_failures.append("Thiếu mục 'Phân Rã Subtasks' hoặc subtask thiếu đường dẫn Handoff")

    if not dor_failures:
        checks["DoR"] = {"pass": True, "message": "Đạt chuẩn Definition of Ready (DoR)."}
    else:
        checks["DoR"] = {
            "pass": False,
            "message": f"Chưa đạt DoR: {'; '.join(dor_failures)}.",
        }

    # 4. BLK: ADR Requirement Check
    needs_adr = bool(re.search(r"(?i)(>=?\s*2\s*phương\s*án|lựa\s*chọn\s*phương\s*án|ADR)", text))
    outputs = meta.get("outputs", [])
    has_adr_output = any("docs/adr/" in str(out) for out in outputs)

    if needs_adr and not has_adr_output:
        # Nếu thân card nhắc đến phương án mà outputs không khai ADR
        checks["BLK"] = {
            "pass": False,
            "message": "Task có >= 2 phương án kiến trúc nhưng chưa khai báo file ADR trong outputs.",
        }
    else:
        checks["BLK"] = {"pass": True, "message": "Không bị chặn bởi yêu cầu ADR mới."}

    # 5. PLAN: Scope Overlap Check with 'doing' cards
    overlap_errors: List[str] = []
    doing_cards = [c for c in all_cards if c.get("status") == "doing" and c.get("id") != card_id]

    for doing in doing_cards:
        doing_scopes = doing.get("scope_edit", [])
        for my_pat in scope_edit:
            for other_pat in doing_scopes:
                if _patterns_overlap(my_pat, other_pat):
                    overlap_errors.append(
                        f"Phạm vi '{my_pat}' chồng lấn với task đang doing '{doing['id']}' ('{other_pat}')"
                    )

    if not overlap_errors:
        checks["PLAN"] = {"pass": True, "message": "Phạm vi scope_edit không bị chồng lấn với task nào đang doing."}
    else:
        checks["PLAN"] = {
            "pass": False,
            "message": f"Phát hiện xung đột phạm vi: {'; '.join(overlap_errors)}.",
        }

    # Tổng kết verdict
    all_passed = all(item["pass"] for item in checks.values())
    verdict = "PASS" if all_passed else "BLOCKED"

    return ClaimCheckResult(
        card_id=card_id,
        card_path=str(card_p),
        verdict=verdict,
        checks=checks,
    )
