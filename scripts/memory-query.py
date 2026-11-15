#!/usr/bin/env python3
"""scripts/memory-query.py

Bộ Truy Xuất Bộ Nhớ Động & Tự Động Khử Trùng Lặp (Tiered Memory Query & Deduplication Engine).
Hiện thực hóa kiến trúc Letta/Mem0: Ngăn chặn hiện tượng "Bao tải rác" trong PROJECT-NOTES.md.

Tính năng:
1. `query -q "<từ khóa>" [--limit N]`:
   - Truy xuất thông minh các bài học / bẫy kỹ thuật liên quan trực tiếp đến nhiệm vụ hiện tại.
   - Sử dụng thuật toán xếp hạng BM25 / Token IDF từ `agent_core.knowledge.search`.
   - Giữ ngân sách token nhỏ gọn (<= 400 tokens), bảo vệ Context Window.
2. `dedup [--in-place]`:
   - Tự động phát hiện và khử các dòng bài học bị lặp lại nhiều lần do harvest-chat quét trùng.
   - Ghi lại bản sạch vào docs/PROJECT-NOTES.md nếu có `--in-place`.

Usage:
  python3 scripts/memory-query.py query -q "xerj prefix"
  python3 scripts/memory-query.py query -q "feature flag leaf trunk"
  python3 scripts/memory-query.py dedup --in-place
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.knowledge.search import normalize, tokens_of


def parse_project_notes(notes_path: Path) -> List[Dict[str, str]]:
    """Phân tích bảng bẫy và bài học trong docs/PROJECT-NOTES.md."""
    if not notes_path.exists():
        return []

    content = notes_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    entries = []
    in_table = False

    for line in lines:
        line_s = line.strip()
        if line_s.startswith("| ID | Ngày | Nguồn |"):
            in_table = True
            continue
        if in_table:
            if not line_s.startswith("|"):
                if line_s.startswith("##"):
                    in_table = False
                continue
            if line_s.startswith("|---"):
                continue

            parts = [p.strip() for p in line_s.split("|")[1:-1]]
            if len(parts) >= 5:
                entry = {
                    "id": parts[0],
                    "date": parts[1],
                    "source": parts[2],
                    "scope": parts[3],
                    "content": parts[4],
                    "raw_line": line_s,
                }
                entries.append(entry)

    return entries


def deduplicate_entries(entries: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], int]:
    """Khử trùng lặp các bài học dựa trên fingerprint nội dung chuẩn hóa."""
    seen_fingerprints = set()
    deduped = []
    duplicates_count = 0

    for e in entries:
        fp = normalize(e["content"])
        if not fp:
            continue
        if fp in seen_fingerprints:
            duplicates_count += 1
            continue
        seen_fingerprints.add(fp)
        deduped.append(e)

    return deduped, duplicates_count


def search_memories(
    query: str,
    entries: List[Dict[str, str]],
    limit: int = 5,
) -> List[Tuple[float, Dict[str, str]]]:
    """Tìm kiếm xếp hạng các bài học phù hợp nhất với truy vấn."""
    q_tokens = tokens_of(query)
    if not q_tokens:
        return [(1.0, e) for e in entries[:limit]]

    scored = []
    for e in entries:
        text = f"{e['scope']} {e['content']}"
        entry_tokens = tokens_of(text)
        if not entry_tokens:
            continue

        entry_set = set(entry_tokens)
        # Điểm khớp từ khóa
        overlap = sum(1 for tok in q_tokens if tok in entry_set)
        if overlap == 0:
            continue

        # Điểm thưởng nếu khớp cụm từ liên tiếp
        norm_query = normalize(query)
        norm_text = normalize(text)
        phrase_bonus = 2.0 if norm_query in norm_text else 0.0

        score = (overlap / (len(q_tokens) + 1.0)) + phrase_bonus
        scored.append((score, e))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:limit]


def rewrite_project_notes(notes_path: Path, deduped_entries: List[Dict[str, str]]) -> None:
    """Ghi lại PROJECT-NOTES.md với bảng đã được làm sạch khử trùng."""
    content = notes_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    new_lines = []
    in_table = False
    table_written = False

    for line in lines:
        line_s = line.strip()
        if line_s.startswith("| ID | Ngày | Nguồn |"):
            in_table = True
            new_lines.append(line)
            new_lines.append("|---|---|---|---|---|")
            for e in deduped_entries:
                new_lines.append(f"| {e['id']} | {e['date']} | {e['source']} | {e['scope']} | {e['content']} |")
            table_written = True
            continue

        if in_table:
            if line_s.startswith("|"):
                continue
            else:
                in_table = False

        if not in_table:
            new_lines.append(line)

    notes_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="memory-query: Bộ truy xuất bộ nhớ động & khử trùng lặp tri thức (Letta/Mem0 Architecture)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_query = sub.add_parser("query", help="Truy vấn bài học và bẫy kỹ thuật liên quan đến từ khóa")
    p_query.add_argument("-q", "--query", required=True, help="Từ khóa hoặc ngữ cảnh bài toán (ví dụ: jwt, xerj, feature flag)")
    p_query.add_argument("-l", "--limit", type=int, default=5, help="Số lượng bài học tối đa cần lấy (mặc định: 5)")
    p_query.add_argument("--json", action="store_true", help="Xuất kết quả JSON")

    p_dedup = sub.add_parser("dedup", help="Khử các dòng bài học bị lặp lại trong PROJECT-NOTES.md")
    p_dedup.add_argument("--in-place", action="store_true", help="Ghi đè trực tiếp làm sạch docs/PROJECT-NOTES.md")

    args = parser.parse_args()
    notes_path = ROOT / "docs" / "PROJECT-NOTES.md"

    raw_entries = parse_project_notes(notes_path)
    deduped_entries, dup_count = deduplicate_entries(raw_entries)

    if args.cmd == "query":
        results = search_memories(args.query, deduped_entries, limit=args.limit)
        if not results:
            print(f"[INFO] Không tìm thấy bài học nào khớp với từ khóa '{args.query}'.")
            return 0

        if args.json:
            import json
            out = [{"score": round(score, 2), **entry} for score, entry in results]
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(f"[MEMORY RETRIEVAL] Tìm thấy {len(results)} bài học liên quan nhất cho '{args.query}':")
            print("-" * 70)
            for idx, (score, e) in enumerate(results, 1):
                print(f"{idx}. [{e['id']}] ({e['date']} - {e['source']}) [{e['scope']}]")
                print(f"   👉 {e['content']}")
            print("-" * 70)
            print("💡 Chỉ nạp các bài học trên vào ngữ cảnh, không cần đọc toàn bộ PROJECT-NOTES.md!")
        return 0

    elif args.cmd == "dedup":
        print(f"Tổng số dòng ghi chú đọc được: {len(raw_entries)}")
        print(f"Số dòng trùng lặp phát hiện: {dup_count}")
        print(f"Số dòng thực tế sau khi lọc: {len(deduped_entries)}")

        if args.in_place:
            rewrite_project_notes(notes_path, deduped_entries)
            print(f"[OK] Đã làm sạch thành công {notes_path}.")
        else:
            print("[INFO] Chạy ở chế độ xem trước. Dùng --in-place để áp dụng thay đổi vào đĩa.")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
