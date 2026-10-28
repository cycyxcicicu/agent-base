"""agent_core.workflow.rtm

Sinh và kiểm tra tính toàn vẹn của Ma trận truy vết yêu cầu (Function_RTM).
Chuỗi liên kết: Yêu cầu R-xxx -> Task card -> Tệp mã nguồn -> Tệp kiểm thử -> Bằng chứng kiểm thử -> Xác nhận con người.
Tuân thủ đặc tả T-11 §7, các yêu cầu R-08, R-09 và không thêm dependency.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from agent_core.workflow.task_discovery import discover_tasks


@dataclass
class RTMEntry:
    req_id: str
    req_title: str
    task_id: str
    task_title: str
    task_status: str
    files: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    has_proof: bool = False
    proof_summary: str = ""
    user_approval: str = "[ ] Chờ duyệt (người)"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "req_id": self.req_id,
            "req_title": self.req_title,
            "task_id": self.task_id,
            "task_title": self.task_title,
            "task_status": self.task_status,
            "files": self.files,
            "tests": self.tests,
            "has_proof": self.has_proof,
            "proof_summary": self.proof_summary,
            "user_approval": self.user_approval,
        }


@dataclass
class RTMReport:
    entries: List[RTMEntry] = field(default_factory=list)
    issues: List[Dict[str, Any]] = field(default_factory=list)
    is_clean: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_count": len(self.entries),
            "issue_count": len(self.issues),
            "is_clean": self.is_clean,
            "entries": [e.to_dict() for e in self.entries],
            "issues": self.issues,
        }


def parse_requirements(req_dir: Path | str) -> List[Dict[str, str]]:
    """Quét và phân tích các yêu cầu R-xxx trong thư mục docs/requirements/."""
    base_dir = Path(req_dir).resolve()
    if not base_dir.is_dir():
        return []

    reqs: List[Dict[str, str]] = []
    for f in sorted(base_dir.glob("R-*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        # Tìm các khối: ### R-xx: Tiêu đề
        sections = re.split(r"\n(?=###\s+R-\d+)", text)
        for sec in sections:
            m_header = re.search(r"###\s+(R-\d+):\s*(.*)", sec)
            if not m_header:
                continue
            r_id = m_header.group(1).strip()
            r_title = m_header.group(2).strip()

            m_card = re.search(r"-\s*\*\*Card thực hiện\*\*:\s*([A-Za-z0-9_.-]+)", sec)
            card_ref = m_card.group(1).strip().rstrip(".") if m_card else ""

            m_desc = re.search(r"-\s*\*\*Mô tả\*\*:\s*(.*)", sec)
            desc = m_desc.group(1).strip() if m_desc else ""

            reqs.append({
                "id": r_id,
                "title": r_title,
                "card": card_ref,
                "desc": desc,
                "source_file": f.name,
            })

    # Sắp xếp theo mã R
    def req_key(item: Dict[str, str]) -> int:
        m = re.search(r"\d+", item["id"])
        return int(m.group(0)) if m else 999

    reqs.sort(key=req_key)
    return reqs


def _extract_card_files_and_proof(card_data: Dict[str, Any]) -> Tuple[List[str], List[str], bool, str]:
    """Trích xuất file mã nguồn, file test và bằng chứng từ nội dung card."""
    text = card_data.get("_text", "")
    files: List[str] = []
    tests: List[str] = []
    has_proof = False
    proof_summary = ""

    # 1. Trích xuất File đã đổi
    m_files = re.search(r"##\s+File đã đổi\s*\n([\s\S]*?)(?=\n##|\Z)", text)
    if m_files:
        raw_list = m_files.group(1)
        for line in raw_list.splitlines():
            line_m = re.search(r"-\s*`([^`]+)`", line)
            if line_m:
                path_str = line_m.group(1).strip()
                if "test" in path_str.lower() and path_str.endswith(".py"):
                    tests.append(path_str)
                else:
                    files.append(path_str)

    # Nếu mục "File đã đổi" chưa có, thử lấy từ scope_edit
    if not files and not tests:
        for p in card_data.get("scope_edit", []):
            if "test" in p.lower() and p.endswith(".py"):
                tests.append(p)
            elif not p.endswith(".md"):
                files.append(p)

    # 2. Trích xuất Kết quả test / Bằng chứng
    m_test_res = re.search(r"##\s+Kết quả test\s*\n([\s\S]*?)(?=\n##|\Z)", text)
    if m_test_res:
        proof_text = m_test_res.group(1).strip()
        if proof_text and "chưa chạy" not in proof_text.lower():
            has_proof = True
            proof_summary = proof_text.splitlines()[0][:80]

    return sorted(list(set(files))), sorted(list(set(tests))), has_proof, proof_summary


def build_rtm_data(requirements_dir: Path | str, tasks_dir: Path | str) -> RTMReport:
    reqs = parse_requirements(requirements_dir)
    all_cards = discover_tasks(tasks_dir)
    card_map = {c["id"]: c for c in all_cards}

    entries: List[RTMEntry] = []
    issues: List[Dict[str, Any]] = []

    for r in reqs:
        r_id = r["id"]
        r_title = r["title"]
        assigned_card_id = r["card"]

        # Nếu req chưa khai báo card, tìm xem có card nào khai requirements: [r_id]
        if not assigned_card_id:
            for cid, cdata in card_map.items():
                c_reqs = cdata.get("requirements", [])
                if r_id in c_reqs:
                    assigned_card_id = cid
                    break

        if not assigned_card_id:
            issues.append({
                "type": "MISSING_TASK",
                "req_id": r_id,
                "message": f"Yêu cầu {r_id} ({r_title}) chưa có task card phụ trách",
            })
            entry = RTMEntry(
                req_id=r_id,
                req_title=r_title,
                task_id="(chưa giao)",
                task_title="",
                task_status="todo",
                files=[],
                tests=[],
                has_proof=False,
                proof_summary="",
            )
            entries.append(entry)
            continue

        card_data = card_map.get(assigned_card_id)
        if not card_data:
            # Task ID được chỉ định nhưng file card chưa tạo
            issues.append({
                "type": "MISSING_CARD_FILE",
                "req_id": r_id,
                "task_id": assigned_card_id,
                "message": f"Yêu cầu {r_id} trỏ tới card {assigned_card_id} nhưng file card chưa tồn tại",
            })
            entry = RTMEntry(
                req_id=r_id,
                req_title=r_title,
                task_id=assigned_card_id,
                task_title="(chưa có file card)",
                task_status="todo",
                files=[],
                tests=[],
                has_proof=False,
                proof_summary="",
            )
            entries.append(entry)
            continue

        files, tests, has_proof, proof_summary = _extract_card_files_and_proof(card_data)

        # Kiểm tra thiếu test
        if not tests:
            issues.append({
                "type": "MISSING_TEST",
                "req_id": r_id,
                "task_id": assigned_card_id,
                "message": f"Task {assigned_card_id} ({r_id}) chưa có file test",
            })

        # Kiểm tra thiếu bằng chứng test
        if not has_proof and card_data.get("status") in ("review", "done"):
            issues.append({
                "type": "MISSING_PROOF",
                "req_id": r_id,
                "task_id": assigned_card_id,
                "message": f"Task {assigned_card_id} ({r_id}) chưa có bằng chứng kiểm thử chạy thật trong 'Kết quả test'",
            })

        entry = RTMEntry(
            req_id=r_id,
            req_title=r_title,
            task_id=assigned_card_id,
            task_title=card_data.get("title", ""),
            task_status=card_data.get("status", "todo"),
            files=files,
            tests=tests,
            has_proof=has_proof,
            proof_summary=proof_summary,
            user_approval="[ ] Chờ duyệt (người)",
        )
        entries.append(entry)

    is_clean = len(issues) == 0
    return RTMReport(entries=entries, issues=issues, is_clean=is_clean)


def render_rtm_markdown(report: RTMReport) -> str:
    """Sinh tài liệu Markdown RTM.md chuẩn."""
    lines: List[str] = [
        "> Bản sinh tự động bởi scripts/rtm.py, không sửa tay.",
        "",
        "# Ma trận truy vết yêu cầu phần mềm (Function_RTM)",
        "",
        "Bản sinh tự động đối chiếu yêu cầu từ `docs/requirements/` với task card trong `tasks/`.",
        "Quy tắc cứng: Cột 'Xác nhận (Người dùng)' chỉ người dùng có quyền đánh dấu sau khi kiểm tra.",
        "",
        "| Mã YC | Tên Yêu Cầu | Card | Trạng thái | Tệp mã nguồn | Tệp kiểm thử | Bằng chứng kiểm thử | Xác nhận (Người dùng) |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for e in report.entries:
        files_str = "<br>".join(f"`{f}`" for f in e.files) if e.files else "—"
        tests_str = "<br>".join(f"`{t}`" for t in e.tests) if e.tests else "—"
        proof_str = f"✅ `{e.proof_summary}`" if e.has_proof else "❌ Chưa có"
        lines.append(
            f"| **{e.req_id}** | {e.req_title} | `{e.task_id}` | `{e.task_status}` | {files_str} | {tests_str} | {proof_str} | {e.user_approval} |"
        )

    lines.append("")
    lines.append("## Thống kê tính toàn vẹn truy vết")
    lines.append(f"- Tổng số yêu cầu: **{len(report.entries)}**")
    lines.append(f"- Số vấn đề phát hiện: **{len(report.issues)}**")
    if report.issues:
        lines.append("")
        lines.append("### Danh mục thiếu sót cần xử lý:")
        for iss in report.issues:
            lines.append(f"- `[{iss['type']}]` {iss['message']}")
    else:
        lines.append("- Trạng thái truy vết: ✅ **100% Yêu cầu đã được liên kết đầy đủ.**")

    lines.append("")
    return "\n".join(lines)


def generate_rtm(requirements_dir: Path | str, tasks_dir: Path | str, output_dir: Path | str) -> RTMReport:
    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    report = build_rtm_data(requirements_dir, tasks_dir)

    md_content = render_rtm_markdown(report)
    out_file = out_dir / "RTM.md"
    out_file.write_text(md_content, encoding="utf-8")
    return report


def check_rtm(requirements_dir: Path | str, tasks_dir: Path | str) -> RTMReport:
    return build_rtm_data(requirements_dir, tasks_dir)
