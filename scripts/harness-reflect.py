#!/usr/bin/env python3
"""scripts/harness-reflect.py

Experience Reflector (Bộ phản tư kinh nghiệm theo mô hình Harness² của Google Research).
Tự động hóa chu trình học hỏi và cập nhật tri thức:
1. Quét các ghi chú bàn giao & bài học trong docs/notes/inbox/.
2. Tổng hợp các bẫy, quyết định và bài học vào docs/PROJECT-NOTES.md (tuân thủ nguyên tắc không xóa bỏ âm thầm).
3. Phát hiện các đề xuất sửa đổi Quy tắc Cốt lõi (AGENTS.md, hard-rules.md, git) hoặc bài học lặp lại >= 2 lần.
   -> Tuyệt đối KHÔNG tự ý sửa file cốt lõi!
   -> Tự động lập bản đề xuất docs/proposals/PRP-xxx.md và in cảnh báo nổi bật để con người biết đi sửa.
4. Đồng bộ và cập nhật lại Knowledge Graph (11 Validators V00-V10).
5. Tự động tái phân vùng Scoped Context cho 20 roles (agents/knowledge/context/).

Usage:
  python scripts/harness-reflect.py              # Quét và phản tư cập nhật tri thức
  python scripts/harness-reflect.py --dry-run    # Xem trước nội dung sẽ gộp và đề xuất
  python scripts/harness-reflect.py --archive    # Di chuyển note đã gộp sang docs/notes/archive/
"""

from __future__ import annotations
import argparse
from datetime import datetime, timezone
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import json

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Từ khóa nhận diện liên quan đến Quy tắc Cốt lõi & Bảo mật Git
CORE_RULE_KEYWORDS = [
    "agents.md",
    "hard-rules.md",
    "quy tắc cốt lõi",
    "quy tac cot loi",
    "hard rules",
    "hard rule",
    "bảo mật git",
    "bao mat git",
    "git secret",
    "author: ducnvh",
    "commit rule",
    "push rule",
    "tự ý commit",
    "tu y commit",
]


def parse_inbox_notes(inbox_dir: Path) -> list[dict]:
    """Quét và phân tích toàn bộ ghi chú bàn giao trong docs/notes/inbox/."""
    notes = []
    if not inbox_dir.is_dir():
        return notes

    for file_path in sorted(inbox_dir.rglob("*.md")):
        if file_path.name.startswith(".") or file_path.name == ".gitkeep":
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            sys.stderr.write(f"Cảnh báo: Không thể đọc file {file_path}: {e}\n")
            continue

        note_data = {
            "path": file_path,
            "filename": file_path.name,
            "task": "N/A",
            "agent": "N/A",
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "summary": "",
            "traps": [],
            "decisions": [],
            "conventions": [],
            "lessons": [],
            "skills": [],
        }

        # Trích xuất Header metadata
        for line in content.splitlines()[:15]:
            if line.startswith("> summary:"):
                note_data["summary"] = line.replace("> summary:", "").strip()
            task_match = re.search(r"Task:\s*([A-Za-z0-9_.-]+)", line, re.I)
            if task_match:
                note_data["task"] = task_match.group(1)
            agent_match = re.search(r"Agent:\s*([A-Za-z0-9_.-]+)", line, re.I)
            if agent_match:
                note_data["agent"] = agent_match.group(1)
            date_match = re.search(r"Ngày:\s*(\d{4}-\d{2}-\d{2})", line)
            if date_match:
                note_data["date"] = date_match.group(1)

        # Trích xuất các mục nội dung
        cur_section = None
        for line in content.splitlines():
            clean = line.strip()
            if clean.startswith("## "):
                sec_title = clean[3:].lower()
                if any(k in sec_title for k in ["lưu ý", "luu y", "bẫy", "bay", "trap", "gotcha", "warning"]):
                    cur_section = "traps"
                elif any(k in sec_title for k in ["quyết định", "quyet dinh", "decision", "adr"]):
                    cur_section = "decisions"
                elif any(k in sec_title for k in ["quy ước", "quy uoc", "đề xuất", "de xuat", "convention", "proposal"]):
                    cur_section = "conventions"
                elif any(k in sec_title for k in ["bài học", "bai hoc", "lesson", "takeaway"]):
                    cur_section = "lessons"
                else:
                    cur_section = None
                continue

            if cur_section and (clean.startswith("- ") or clean.startswith("* ")):
                item = clean[2:].strip()
                if item and not item.lower().startswith("không có"):
                    if cur_section == "traps":
                        note_data["traps"].append(item)
                    elif cur_section == "decisions":
                        note_data["decisions"].append(item)
                    elif cur_section == "conventions":
                        note_data["conventions"].append(item)
                    elif cur_section == "lessons":
                        note_data["lessons"].append(item)

            if "skill đã chọn" in clean.lower():
                note_data["skills"].append(clean)

        notes.append(note_data)

    return notes


def find_next_note_id(project_notes_content: str) -> int:
    """Tìm số thứ tự N-xxx tiếp theo trong docs/PROJECT-NOTES.md."""
    matches = re.findall(r"\bN-(\d{3,})\b", project_notes_content)
    if not matches:
        return 1
    return max(int(m) for m in matches) + 1


def find_next_proposal_id(proposals_dir: Path) -> int:
    """Tìm số thứ tự PRP-xxx tiếp theo trong docs/proposals/."""
    if not proposals_dir.is_dir():
        return 1
    existing = list(proposals_dir.glob("PRP-*.md"))
    ids = []
    for p in existing:
        m = re.match(r"PRP-(\d+)", p.stem)
        if m:
            ids.append(int(m.group(1)))
    return max(ids) + 1 if ids else 1


def detect_core_rule_proposals(notes: list[dict], existing_project_notes: str) -> list[dict]:
    """Phát hiện các lưu ý hoặc bài học chạm đến Quy tắc Cốt lõi hoặc xuất hiện >= 2 lần."""
    proposals_needed = []

    for note in notes:
        # Gom toàn bộ các ý kiến từ note
        candidates = []
        for trap in note["traps"]:
            candidates.append(("trap", trap))
        for conv in note["conventions"]:
            candidates.append(("convention", conv))
        for lesson in note["lessons"]:
            candidates.append(("lesson", lesson))

        for c_type, text in candidates:
            text_lower = text.lower()
            is_core_rule = any(kw in text_lower for kw in CORE_RULE_KEYWORDS)

            # Đếm số lần xuất hiện tương tự trong PROJECT-NOTES.md
            # Sử dụng 3 từ khóa chính để kiểm tra độ lặp lại
            words = [w for w in re.findall(r"\w+", text_lower) if len(w) > 3][:4]
            repeat_count = 0
            if words:
                matches = 0
                for line in existing_project_notes.splitlines():
                    if all(w in line.lower() for w in words):
                        matches += 1
                repeat_count = matches

            if is_core_rule or repeat_count >= 1:  # Xuất hiện thêm lần này nữa là >= 2 lần
                proposals_needed.append({
                    "source_note": note["filename"],
                    "task": note["task"],
                    "agent": note["agent"],
                    "type": c_type,
                    "text": text,
                    "is_core_rule": is_core_rule,
                    "repeat_count": repeat_count + 1,
                })

    return proposals_needed


def generate_human_proposal(prop_data: dict, proposals_dir: Path, next_pid: int, dry_run: bool = False) -> str:
    """Tạo file đề xuất docs/proposals/PRP-xxx.md theo chuẩn CMMI Level 3 (3 phương án, 1 khuyến nghị)."""
    prp_code = f"PRP-{next_pid:03d}"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    prop_file = proposals_dir / f"{prp_code}.md"

    reason_tag = "QUY TẮC CỐT LÕI / BẢO MẬT" if prop_data["is_core_rule"] else f"BÀI HỌC LẶP LẠI ({prop_data['repeat_count']} LẦN)"

    content = f"""# Đề Xuất Điều Chỉnh Quy Tắc & Quy Ước: {prp_code}

> **Mã đề xuất:** `{prp_code}`  
> **Ngày tạo:** {today}  
> **Nguồn phát hiện:** `{prop_data['source_note']}` (Task: `{prop_data['task']}`, Agent: `{prop_data['agent']}`)  
> **Lý do kích hoạt:** {reason_tag}  
> **Trạng thái:** `PENDING_HUMAN_APPROVAL` (Chờ con người thẩm định & nghiệm thu)  

---

## 1. Bằng Chứng & Vấn Đề Thực Tế (Evidence)

Hệ thống Harness² trong quá trình phản tư nhận thấy vấn đề sau:
> "{prop_data['text']}"

- **Phân loại:** `{prop_data['type']}`
- **Nguy cơ tiềm ẩn:** Nếu để agent tự do xử lý hoặc thiếu hướng dẫn rõ ràng ở cấp hệ thống, lỗi này có thể tiếp tục lặp lại hoặc làm sai lệch quy trình release.
- **Ràng buộc an toàn:** Hệ thống **TUYỆT ĐỐI KHÔNG TỰ SỬA** `AGENTS.md` hoặc `hard-rules.md`. Toàn bộ quyền quyết định thuộc về Con người.

---

## 2. Ba Phương Án & Một Khuyến Nghị (3 Options & 1 Recommendation)

### Phương Án 1: Giữ nguyên hiện trạng, chỉ ghi nhận vào PROJECT-NOTES.md
- **Mô tả:** Không thay đổi bất kỳ quy tắc nào, chỉ duy trì dòng lưu ý trong nhật ký.
- **Ưu điểm:** Không làm xáo trộn quy trình đang chạy.
- **Nhược điểm:** Tỷ lệ lặp lại lỗi ở các phiên làm việc sau vẫn ở mức cao.

### Phương Án 2: Bổ sung Scoped Rule cục bộ cho Role thực thi
- **Mô tả:** Đưa quy tắc này vào tài liệu hướng dẫn riêng của role (ví dụ: `agents/knowledge/rules/`).
- **Ưu điểm:** Tác động khoanh vùng, không ảnh hưởng đến toàn bộ workspace.
- **Nhược điểm:** Các role phối hợp khác không nắm được giới hạn này.

### Phương Án 3: (KHUYẾN NGHỊ DỨT KHOÁT) Con người cập nhật trực tiếp vào AGENTS.md / hard-rules.md
- **Mô tả:** Con người trực tiếp bổ sung điều khoản kiểm soát hoặc tinh chỉnh quy tắc cứng trong `AGENTS.md` hoặc `hard-rules.md`.
- **Lý do phản biện sâu sắc:** Đây là điểm nghẽn mang tính quy tắc nền tảng hoặc bảo mật; chỉ khi được ghi nhận vào cấp Core Rules thì toàn bộ các agent và subagent mới đồng bộ tuân thủ 100%.

---

## 3. Đánh Giá Rủi Ro & Cách Khắc Phục

| Rủi ro tiềm ẩn | Đánh giá mức độ | Cách khắc phục |
|---|---|---|
| Xung đột với quy trình CI/CD hiện hữu | Trung bình | Kiểm tra tương thích với `scripts/hard-check.py` trước khi sửa |
| Gây nghẽn luồng commit/review | Thấp | Bổ sung ngoại lệ rõ ràng trong tài liệu hướng dẫn |
| Agent diễn giải sai quy tắc mới | Thấp | Viết câu lệnh mệnh lệnh ngắn gọn, không dùng từ mơ hồ |

---

## 4. Checklist Hành Động Cho Con Người (Human Action Items)

- [ ] **Bước 1:** Đọc và đánh giá 3 phương án nêu trên.
- [ ] **Bước 2:** Nếu duyệt Phương án 3, mở file `AGENTS.md` hoặc `hard-rules.md` để sửa bằng tay.
- [ ] **Bước 3:** Chạy `python scripts/hard-check.py` để đảm bảo không vi phạm định dạng.
- [ ] **Bước 4:** Đổi trạng thái file này từ `PENDING_HUMAN_APPROVAL` sang `APPROVED` (hoặc `REJECTED`).
"""

    if not dry_run:
        prop_file.write_text(content, encoding="utf-8")

    return str(prop_file.relative_to(ROOT))


def update_project_notes(project_notes_path: Path, notes: list[dict], dry_run: bool = False) -> int:
    """Gộp các lưu ý, bẫy, bài học vào docs/PROJECT-NOTES.md mà không xóa bỏ âm thầm."""
    if not project_notes_path.is_file():
        sys.stderr.write(f"Lỗi: Không tìm thấy {project_notes_path}\n")
        return 0

    content = project_notes_path.read_text(encoding="utf-8")
    next_id = find_next_note_id(content)
    added_count = 0

    new_traps = []
    new_decisions = []
    new_conventions = []

    for note in notes:
        date_str = note["date"]
        source_tag = f"`{note['filename']}`" if note["task"] == "N/A" else f"`{note['task']}`"

        # 1. Bẫy & Lưu ý
        for trap in note["traps"]:
            nid = f"N-{next_id:03d}"
            next_id += 1
            new_traps.append(f"| {nid} | {date_str} | {source_tag} | Toàn cục | {trap} |")
            added_count += 1

        # 1.1 Bài học kinh nghiệm (Lessons)
        for lesson in note["lessons"]:
            nid = f"N-{next_id:03d}"
            next_id += 1
            new_traps.append(f"| {nid} | {date_str} | {source_tag} | Toàn cục | [Bài học] {lesson} |")
            added_count += 1

        # 2. Quyết định kỹ thuật
        for dec in note["decisions"]:
            nid = f"N-{next_id:03d}"
            next_id += 1
            new_decisions.append(f"| {nid} | {date_str} | {dec} | Theo {source_tag} |")
            added_count += 1

        # 3. Quy ước phát hiện thêm
        for conv in note["conventions"]:
            nid = f"N-{next_id:03d}"
            next_id += 1
            new_conventions.append(f"- **[{nid} - {date_str}]** ({source_tag}): {conv}")
            added_count += 1

    if added_count == 0:
        print("ℹ️ Không có lưu ý, bẫy hoặc bài học mới cần gộp.")
        return 0

    # Chèn vào các bảng của PROJECT-NOTES.md
    if new_traps:
        trap_marker = "| ID | Ngày | Nguồn | Phạm vi | Lưu ý |\n|---|---|---|---|---|"
        if trap_marker in content:
            replacement = trap_marker + "\n" + "\n".join(new_traps)
            content = content.replace(trap_marker, replacement, 1)

    if new_decisions:
        dec_marker = "| ID | Ngày | Quyết định | ADR |\n|---|---|---|---|"
        if dec_marker in content:
            replacement = dec_marker + "\n" + "\n".join(new_decisions)
            content = content.replace(dec_marker, replacement, 1)

    if new_conventions:
        conv_marker = "## Quy ước phát hiện thêm"
        if conv_marker in content:
            replacement = conv_marker + "\n\n" + "\n".join(new_conventions)
            content = content.replace(conv_marker, replacement, 1)

    if not dry_run:
        project_notes_path.write_text(content, encoding="utf-8")
        try:
            rel_display = project_notes_path.relative_to(ROOT)
        except ValueError:
            rel_display = project_notes_path
        print(f"📝 Đã gộp thành công {added_count} mục bài học/lưu ý vào: {rel_display}")
    else:
        print(f"🔍 [DRY-RUN] Sẽ gộp {added_count} mục vào PROJECT-NOTES.md")

    return added_count


def run_catalog_builder():
    """Kích hoạt bộ biên dịch Knowledge Graph để tự động kiểm chuẩn và phân vùng ngữ cảnh."""
    builder_script = ROOT / "scripts" / "build-knowledge-catalog.py"
    if not builder_script.is_file():
        print(f"⚠️ Cảnh báo: Không tìm thấy {builder_script}")
        return

    print("\n🔄 Đang kích hoạt bộ biên dịch Knowledge Graph (11 Validators)...")
    res = subprocess.run([sys.executable, str(builder_script)], capture_output=True, text=True)
    if res.returncode == 0:
        print("✅ Knowledge Graph và Scoped Context đã được cập nhật đồng bộ hoàn hảo!")
    else:
        sys.stderr.write(f"❌ Lỗi biên dịch Knowledge Graph:\n{res.stderr}\n{res.stdout}\n")


def archive_processed_notes(inbox_dir: Path, archive_dir: Path):
    """Di chuyển các note đã phản tư sang thư mục lưu trữ archive."""
    archive_month = archive_dir / datetime.now(timezone.utc).strftime("%Y-%m")
    archive_month.mkdir(parents=True, exist_ok=True)
    moved_count = 0

    for file_path in inbox_dir.rglob("*.md"):
        if file_path.name.startswith(".") or file_path.name == ".gitkeep":
            continue
        dest = archive_month / file_path.name
        shutil.move(str(file_path), str(dest))
        moved_count += 1

    if moved_count > 0:
        try:
            rel_display = archive_month.relative_to(ROOT)
        except ValueError:
            rel_display = archive_month
        print(f"📦 Đã lưu trữ an toàn {moved_count} note vào: {rel_display}/")


def extract_domain_keywords_from_glossary(glossary_path: Path) -> set[str]:
    """Trích xuất danh sách thuật ngữ nghiệp vụ từ file domain-glossary.md để tự động khử dữ liệu nhạy cảm."""
    keywords = set()
    if not glossary_path.is_file():
        return keywords
    try:
        content = glossary_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return keywords

    ignore_terms = {
        "thuật ngữ", "thuat ngu", "định nghĩa", "dinh nghia", "mô tả", "mo ta",
        "tiếng anh", "tieng anh", "viết tắt", "viet tat", "stt", "no", "term",
        "definition", "meaning", "note", "ghi chú", "ghi chu", "ví dụ", "vi du",
        "nghĩa là", "nghia la", "không phải", "khong phai", "tổng quan", "tong quan",
        "mục đích", "muc dich", "phạm vi", "pham vi", "yêu cầu", "yeu cau",
    }

    def add_term(term_str: str):
        if not term_str:
            return
        cleaned = re.sub(r"[`*_#]", "", term_str).strip().lower()
        if not cleaned or cleaned.startswith("---") or cleaned in ignore_terms:
            return
        # Bóc tách cụm trong ngoặc đơn nếu có: "Bệnh án điện tử (EMR)" -> "Bệnh án điện tử" và "emr"
        parens = re.findall(r"\(([^)]+)\)", cleaned)
        for p in parens:
            p_clean = p.strip()
            if p_clean and p_clean not in ignore_terms and len(p_clean) >= 3:
                keywords.add(p_clean)
        cleaned_no_paren = re.sub(r"\([^)]*\)", "", cleaned).strip()
        if cleaned_no_paren and cleaned_no_paren not in ignore_terms and len(cleaned_no_paren) >= 3:
            keywords.add(cleaned_no_paren)

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue

        # 1. Tiêu đề Markdown: ## 1. Bệnh án điện tử (EMR) hoặc ### Kế toán công nợ
        if line.startswith("#"):
            m = re.match(r"^#{1,4}\s+(?:\d+[\.\)]\s*)?([^\n#]+)", line)
            if m:
                add_term(m.group(1))
            continue

        # 2. Bảng Markdown: | Thuật ngữ | Tiếng Anh | Định nghĩa |
        if line.startswith("|") and line.endswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            for p in parts[:2]:
                add_term(p)
            continue

        # 3. Danh sách gạch đầu dòng hoặc in đậm: - **Bệnh án**: ... hoặc **Bệnh án**: ...
        m = re.match(r"^(?:[-*]\s+)?\*{1,2}([^:*(\[]+)\*{1,2}\s*:", line)
        if m:
            add_term(m.group(1))
        elif line.startswith(("- ", "* ")):
            m = re.match(r"^[-*]\s+\*{0,2}([^:*(\[]+)\*{0,2}", line)
            if m:
                add_term(m.group(1))

    return keywords


def main():
    parser = argparse.ArgumentParser(description="Harness² Experience Reflector: Tự động học và cập nhật tri thức")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ xem trước các bài học sẽ gộp, không ghi file")
    parser.add_argument("--archive", action="store_true", help="Di chuyển các ghi chú đã gộp sang docs/notes/archive/")
    parser.add_argument("--harvest", help="Đường dẫn tới dự án bên ngoài để tự động thu hoạch bài học kỹ nghệ")
    args = parser.parse_args()

    project_root = ROOT
    doc_dir_name = None

    if args.harvest:
        harvest_target = args.harvest.strip()
        projects_file = ROOT / "projects.json"
        if projects_file.is_file():
            try:
                pdata = json.loads(projects_file.read_text(encoding="utf-8"))
                for p in pdata.get("projects", []):
                    if harvest_target in (p.get("id"), p.get("name")):
                        p_path = Path(p.get("path", "")).expanduser().resolve()
                        if p_path.is_dir():
                            project_root = p_path
                            doc_dir_name = p.get("doc_dir")
                            break
                    elif p.get("path") and Path(p.get("path")).expanduser().resolve() == Path(harvest_target).expanduser().resolve():
                        project_root = Path(p.get("path")).expanduser().resolve()
                        doc_dir_name = p.get("doc_dir")
                        break
            except Exception:
                pass

        if project_root == ROOT and harvest_target:
            project_root = Path(harvest_target).resolve()

    # Tự động phát hiện doc_dir nếu chưa xác định từ projects.json
    if not doc_dir_name:
        if (project_root / "doc" / "notes" / "inbox").is_dir():
            doc_dir_name = "doc"
        elif (project_root / "docs" / "notes" / "inbox").is_dir():
            doc_dir_name = "docs"
        elif (project_root / "doc").is_dir():
            doc_dir_name = "doc"
        else:
            doc_dir_name = "docs"

    inbox_dir = project_root / doc_dir_name / "notes" / "inbox"
    archive_dir = project_root / doc_dir_name / "notes" / "archive"
    project_notes_path = ROOT / "docs" / "PROJECT-NOTES.md"
    if not project_notes_path.is_file():
        if (ROOT / "doc" / "PROJECT-NOTES.md").is_file():
            project_notes_path = ROOT / "doc" / "PROJECT-NOTES.md"
        elif (ROOT / "doc" / "notes" / "PROJECT-NOTES.md").is_file():
            project_notes_path = ROOT / "doc" / "notes" / "PROJECT-NOTES.md"

    proposals_dir = ROOT / "docs" / "proposals"
    proposals_dir.mkdir(parents=True, exist_ok=True)

    print("==================================================================")
    if args.harvest:
        print(f"🌾 HARNESS² HARVESTER — THU HOẠCH TRI THỨC TỪ DỰ ÁN: {project_root.name}")
    else:
        print("🧠 HARNESS² EXPERIENCE REFLECTOR — TỰ ĐỘNG HỌC & CẬP NHẬT TRI THỨC")
    print("==================================================================")

    # 1. Quét ghi chú trong inbox
    raw_notes = parse_inbox_notes(inbox_dir)
    print(f"📬 Tìm thấy {len(raw_notes)} ghi chú bàn giao trong: {inbox_dir}")

    # Nếu là chế độ thu hoạch từ dự án ngoài, lọc bỏ thông tin nghiệp vụ riêng
    notes = []
    if args.harvest:
        glossary_candidates = [
            project_root / doc_dir_name / "architecture" / "domain-glossary.md",
            project_root / "doc" / "architecture" / "domain-glossary.md",
            project_root / "docs" / "architecture" / "domain-glossary.md",
            project_root / doc_dir_name / "domain-glossary.md",
            project_root / "doc" / "domain-glossary.md",
            project_root / "docs" / "domain-glossary.md",
        ]
        glossary_file = next((f for f in glossary_candidates if f.is_file()), None)
        loaded_keywords = set()
        if glossary_file:
            loaded_keywords = extract_domain_keywords_from_glossary(glossary_file)
            try:
                rel_g = glossary_file.relative_to(project_root)
            except ValueError:
                rel_g = glossary_file
            print(f"📖 Đã nạp động {len(loaded_keywords)} từ khóa nghiệp vụ từ: {rel_g}")

        default_keywords = {"accounting-service", "iam-service", "j&t", "pancake", "kế toán", "ke toan", "tiền tệ", "đơn hàng", "don hang"}
        domain_keywords = sorted(default_keywords | loaded_keywords)

        for n in raw_notes:
            filtered_traps = [t for t in n["traps"] if not any(dk in t.lower() for dk in domain_keywords)]
            filtered_lessons = [l for l in n["lessons"] if not any(dk in l.lower() for dk in domain_keywords)]
            filtered_conventions = [c for c in n["conventions"] if not any(dk in c.lower() for dk in domain_keywords)]
            filtered_decisions = [d for d in n["decisions"] if not any(dk in d.lower() for dk in domain_keywords)]

            if filtered_traps or filtered_lessons or filtered_conventions or filtered_decisions or n["skills"]:
                filtered_note = dict(n)
                filtered_note["traps"] = filtered_traps
                filtered_note["lessons"] = filtered_lessons
                filtered_note["conventions"] = filtered_conventions
                filtered_note["decisions"] = filtered_decisions
                notes.append(filtered_note)
        print(f"🔍 Bộ lọc phân loại: Đã trích xuất {len(notes)} bài học kỹ nghệ chung (bỏ qua nghiệp vụ riêng).")
    else:
        notes = raw_notes

    # 2. Đọc PROJECT-NOTES.md hiện tại để đối soát
    existing_content = project_notes_path.read_text(encoding="utf-8") if project_notes_path.is_file() else ""

    # 3. Phát hiện đề xuất liên quan Quy tắc Cốt lõi hoặc Bài học lặp lại >= 2 lần
    proposals = detect_core_rule_proposals(notes, existing_content)
    created_proposals = []
    if proposals:
        current_pid = find_next_proposal_id(proposals_dir)
        for prop in proposals:
            prop_file = generate_human_proposal(prop, proposals_dir, current_pid, dry_run=args.dry_run)
            created_proposals.append((prop, prop_file))
            current_pid += 1

    # 4. Gộp vào PROJECT-NOTES.md
    added = update_project_notes(project_notes_path, notes, dry_run=args.dry_run)

    # 5. Kích hoạt cập nhật Knowledge Graph & Scoped Context
    if not args.dry_run:
        run_catalog_builder()

    # 6. Lưu trữ (nếu có cờ --archive)
    if args.archive and not args.dry_run and len(notes) > 0:
        archive_processed_notes(inbox_dir, archive_dir)
        # Tự động cập nhật lại INDEX.md sau khi di chuyển các note
        notes_idx_script = ROOT / "scripts" / "notes-index.py"
        if notes_idx_script.exists():
            subprocess.run([sys.executable, str(notes_idx_script)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 7. Hiển thị Cảnh Báo Con Người nếu có đề xuất sửa đổi Quy Tắc Cốt Lõi
    if created_proposals:
        print("\n" + "🚨" * 38)
        print("🚨 [CẢNH BÁO BẬC CAO: YÊU CẦU CON NGƯỜI DUYỆT SỬA ĐỔI QUY TẮC]")
        print("🚨 Hệ thống phát hiện bài học/lưu ý chạm đến QUY TẮC CỐT LÕI / BẢO MẬT:")
        print("🚨 Hệ thống TUYỆT ĐỐI KHÔNG tự sửa AGENTS.md hay hard-rules.md!")
        for p_data, p_file in created_proposals:
            print(f"   👉 Đã lập bản đề xuất: {p_file}")
            print(f"      Lý do: {p_data['text'][:70]}...")
        print("🚨 Con người vui lòng xem xét file đề xuất và tự thực hiện sửa đổi nếu duyệt.")
        print("🚨" * 38 + "\n")

    print("==================================================================")
    print("🎉 HOÀN TẤT CHU TRÌNH PHẢN TƯ VÀ CẬP NHẬT TRI THỨC!")
    print("==================================================================")


if __name__ == "__main__":
    main()
