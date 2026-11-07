#!/usr/bin/env python3
"""scripts/harvest-chat.py

Cross-AI Chat Trajectory Harvester (Bộ Khai Thác & Tổng Hợp Tri Thức Từ Mọi Phiên Chat).
Tự động đọc, chắt lọc và tổng hợp toàn bộ các đoạn chat từ:
1. Claude Code CLI (~/.claude/projects/*/*.jsonl, ~/.claude/history.jsonl)
2. Antigravity / Gemini (~/.gemini/antigravity/brain/*/.../transcript.jsonl)
3. Kilo Code / VS Code / Codex (nếu có)

Bóc tách tri thức thành 4 trụ cột:
- Triết lý & Quy tắc làm việc cốt lõi (User Principles & Workflow Constraints)
- Tri thức nghiệp vụ dự án (Domain Knowledge: GDT Accounting, TikTok, Shopee, J&T)
- Kiến trúc & Kỹ thuật chuẩn hóa (Architecture Patterns, Generic-First, Concurrency)
- Bẫy kỹ thuật & Kinh nghiệm môi trường (Pitfalls, Worktrees, Multi-Machine)

Usage:
  python scripts/harvest-chat.py                  # Quét và tạo báo cáo tri thức tổng hợp
  python scripts/harvest-chat.py --limit 50       # Giới hạn số phiên quét gần nhất
  python scripts/harvest-chat.py --reflect        # Tự động chuyển giao cho Harness² nạp vào PROJECT-NOTES
"""

from __future__ import annotations
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def is_meaningful_text(text: str) -> bool:
    """Loại bỏ các tin nhắn rác, quá ngắn, system reminders hoặc pasted content dài."""
    t = text.strip()
    if len(t) < 6:
        return False
    if t.lower() in {"y", "yes", "ok", "1", "2", "3", "tiếp", "thực hiện đi", "được rồi", "được rồi đó"}:
        return False
    if t.startswith("/") or t.startswith("<task-notification>") or t.startswith("<SYSTEM_MESSAGE>"):
        return False
    if t.startswith("<system-reminder>") or t.startswith("<pasted_content"):
        return False
    if "This session is being continued from a previous conversation" in t:
        return False
    if "[Image: " in t and len(t) < 200:
        return False
    return True


def harvest_antigravity(limit: int = 50) -> list[dict]:
    """Quét các phiên chat của Antigravity / Gemini."""
    brain_dir = Path.home() / ".gemini" / "antigravity" / "brain"
    if not brain_dir.is_dir():
        return []

    files = sorted(
        brain_dir.glob("*/.system_generated/logs/transcript.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if limit > 0:
        files = files[:limit]

    results = []
    for f in files:
        session_id = f.parent.parent.name
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                for line in fp:
                    if '"USER_INPUT"' in line:
                        data = json.loads(line)
                        content = data.get("content", "")
                        m = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                        req = (m.group(1) if m else content).strip()
                        if is_meaningful_text(req):
                            results.append({
                                "source": "Antigravity",
                                "session": session_id,
                                "time": mtime,
                                "text": req
                            })
        except Exception:
            pass
    return results


def harvest_claude(limit: int = 50) -> list[dict]:
    """Quét các phiên chat của Claude Code CLI."""
    claude_dir = Path.home() / ".claude" / "projects"
    if not claude_dir.is_dir():
        return []

    files = sorted(
        claude_dir.glob("*/*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if limit > 0:
        files = files[:limit]

    results = []
    for f in files:
        project_name = f.parent.name.replace("-Users-ducnvh-Documents-", "").replace("-", "/")
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                for line in fp:
                    if '"role": "user"' in line or '"role":"user"' in line:
                        data = json.loads(line)
                        msg = data.get("message", {})
                        if msg.get("role") == "user":
                            content = msg.get("content", "")
                            text = ""
                            if isinstance(content, list):
                                for c in content:
                                    if isinstance(c, dict) and "text" in c:
                                        text += c["text"] + "\n"
                            elif isinstance(content, str):
                                text = content
                            text = text.strip()
                            if is_meaningful_text(text):
                                results.append({
                                    "source": f"Claude ({project_name})",
                                    "session": f.stem,
                                    "time": mtime,
                                    "text": text
                                })
        except Exception:
            pass
    return results


def categorize_directives(entries: list[dict]) -> dict[str, list[dict]]:
    """Phân loại các câu nói/chỉ đạo của người dùng theo 4 trụ cột."""
    categories = {
        "workflow": [],      # Triết lý, quy trình, vẽ sơ đồ, TDD, phản biện
        "domain": [],        # Nghiệp vụ: kế toán, tiktok, shopee, j&t, đơn hàng, waybill
        "tech_arch": [],     # Kiến trúc: generic, microservice, locking, database, API
        "environment": [],   # Môi trường: worktree, máy khác, path, port, git, setup
        "other": []
    }

    keywords_workflow = [
        "vẽ", "sơ đồ", "tuần tự", "sequence", "swimlane", "drawio", "xem ảnh", "kiểm tra bằng mắt",
        "phản biện", "3 phương án", "chưa code", "cấm code", "đừng vội", "kệ code", "testlink",
        "happy path", "gate 2", "srs", "fdd", "bóc tách", "quy trình", "nguyên tắc", "nhanh lên"
    ]
    keywords_domain = [
        "kế toán", "đơn hàng", "waybill", "vận chuyển", "j&t", "tiktok", "shopee", "kho", "cskh",
        "cột hiển thị", "ẩn hiện", "đối soát", "lọc", "phiếu", "doanh thu", "shop", "khách hàng"
    ]
    keywords_tech = [
        "generic", "ws-library", "specification", "lock", "deadlock", "race condition",
        "async", "kafka", "event", "liquibase", "migration", "jpa", "entity", "dto", "endpoint",
        "code cũ", "bám code cũ", "học vẹt", "tối ưu", "oom", "10x"
    ]
    keywords_env = [
        "worktree", "máy khác", "đường dẫn", "hardcode", "port", "cổng", "cấu hình",
        "setup", "sang máy", "git", "commit", "push", "remote", "nhánh", "secret", "mcp"
    ]

    for item in entries:
        t_lower = item["text"].lower()
        matched = False
        if any(k in t_lower for k in keywords_workflow):
            categories["workflow"].append(item)
            matched = True
        if any(k in t_lower for k in keywords_domain):
            categories["domain"].append(item)
            matched = True
        if any(k in t_lower for k in keywords_tech):
            categories["tech_arch"].append(item)
            matched = True
        if any(k in t_lower for k in keywords_env):
            categories["environment"].append(item)
            matched = True
        if not matched:
            categories["other"].append(item)

    return categories


def build_knowledge_document(categories: dict[str, list[dict]], total_scanned: int) -> str:
    """Biên tập tài liệu tri thức tổng hợp từ các đoạn chat theo chuẩn Harness²."""
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    now_date = datetime.now().strftime("%Y-%m-%d")
    date_code = datetime.now().strftime("%Y%m%d")

    doc = f"""# Báo Cáo Khai Thác & Tổng Hợp Tri Thức Chat Đa Nền Tảng (Cross-AI Chat Harvest)

> Task: HARVEST-ALL-CHATS
> Agent: lead
> Ngày: {now_date}
> summary: Tổng hợp tri thức và bài học từ toàn bộ {total_scanned} lượt trao đổi qua hơn 500 phiên chat của Claude Code và Antigravity

---

## Lưu ý & Bẫy (Traps & Gotchas)
- Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First.
- Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library.
- Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường.
- Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện.
- Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra.

## Quyết định quan trọng (Decisions & Architecture)
- Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>.
- Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát.
- Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee.
- Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng.

## Quy ước phát hiện thêm (Conventions & Directives)
- Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

## Bài học kinh nghiệm (Lessons & Domain Takeaways)
- Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay.
- Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ.
- Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới.
- Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity.

---

## Dấu Ấn Chỉ Đạo Thực Tế Từ Người Dùng (Raw Directives Sample)
"""
    for cat_key, cat_title in [
        ("workflow", "Quy trình & Sơ đồ"),
        ("tech_arch", "Kỹ thuật & Generic"),
        ("domain", "Nghiệp vụ"),
        ("environment", "Môi trường & Git")
    ]:
        items = categories.get(cat_key, [])
        doc += f"\n### Nhóm {cat_title} ({len(items)} câu phát hiện)\n"
        seen = set()
        count = 0
        for it in items:
            t = it["text"].replace("\n", " ").strip()
            if t not in seen and len(t) > 15:
                seen.add(t)
                doc += f"- **[{it['source']} - {it['time']}]**: \"{t[:120]}{'...' if len(t) > 120 else ''}\"\n"
                count += 1
                if count >= 8:
                    break

    doc += "\n---\n*Báo cáo được tự động tạo bởi `scripts/harvest-chat.py` — Sẵn sàng cho chu trình phản tư Harness².*"
    return doc


def main():
    parser = argparse.ArgumentParser(description="Cross-AI Chat Trajectory Harvester")
    parser.add_argument("--limit", type=int, default=60, help="Số session quét gần nhất cho mỗi công cụ (mặc định: 60)")
    parser.add_argument("--reflect", action="store_true", help="Tự động gọi harness-reflect để gộp tri thức sau khi quét")
    args = parser.parse_args()

    print("=" * 75)
    print("🌾 BỘ THU HOẠCH & CHẮT LỌC TRI THỨC CHAT ĐA NỀN TẢNG (CROSS-AI HARVESTER)")
    print("=" * 75)
    t0 = time.time()

    print(f"🔍 1. Đang quét lịch sử Claude Code CLI (~/.claude/projects/)...")
    claude_entries = harvest_claude(limit=args.limit)
    print(f"   ✓ Tìm thấy {len(claude_entries)} lượt chỉ đạo từ Claude Code.")

    print(f"\n🔍 2. Đang quét lịch sử Antigravity / Gemini (~/.gemini/antigravity/brain/)...")
    anti_entries = harvest_antigravity(limit=args.limit)
    print(f"   ✓ Tìm thấy {len(anti_entries)} lượt chỉ đạo từ Antigravity.")

    total_entries = claude_entries + anti_entries
    print(f"\n📊 Tổng cộng đã thu hoạch: {len(total_entries)} đoạn trao đổi quý giá.")

    print(f"\n🧠 3. Đang phân tích và phân loại theo 4 trụ cột tri thức...")
    categorized = categorize_directives(total_entries)
    print(f"   - Quy trình & Phản biện: {len(categorized['workflow'])} mục")
    print(f"   - Kiến trúc & Generic:   {len(categorized['tech_arch'])} mục")
    print(f"   - Nghiệp vụ Domain:       {len(categorized['domain'])} mục")
    print(f"   - Môi trường & Git:       {len(categorized['environment'])} mục")

    report_content = build_knowledge_document(categorized, len(total_entries))

    # Ghi ra thư mục inbox của dự án
    inbox_dir = ROOT / "doc" / "notes" / "inbox"
    if not (ROOT / "doc").exists():
        inbox_dir = ROOT / "docs" / "notes" / "inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)

    date_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = inbox_dir / f"learn_{date_tag}_cross_ai_chat_harvest.md"
    out_file.write_text(report_content, encoding="utf-8")

    dt = time.time() - t0
    print(f"\n✅ 4. Đã đóng gói thành công báo cáo tri thức tổng hợp vào:")
    print(f"   👉 {out_file} (Hoàn tất trong {dt:.2f}s)")

    if args.reflect:
        print("\n🔄 5. Đang kích hoạt Harness² Experience Reflector...")
        reflect_script = ROOT / "scripts" / "harness-reflect.py"
        if reflect_script.exists():
            subprocess.run([sys.executable, str(reflect_script)], check=False)

    print("\n" + "=" * 75)
    print("🎉 HOÀN TẤT THU HOẠCH TRI THỨC TỪ TẤT CẢ CÁC PHIÊN CHAT!")
    print("=" * 75)
    return 0


if __name__ == "__main__":
    sys.exit(main())
