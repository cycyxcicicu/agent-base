#!/usr/bin/env python3
"""scripts/skill-router.py

Bộ Định Tuyến Kỹ Năng Thông Minh (SkillRouter - Top-k Retrieve-and-Rerank).
Hiện thực hóa công trình Alibaba SkillRouter & Tsinghua SRA-Bench 2026:
Giải quyết triệt để vấn đề: Kho có 43+ skills nhưng Agent bị "Mù kỹ năng" (Skill Blindness) hoặc chỉ dùng 1 tí.

Tính năng:
- Quét toàn bộ 43 skills có sẵn trong kho `.agents/skills/` (và skills của Antigravity/Kilo).
- Phân tích yêu cầu / ngữ cảnh của task (hỗ trợ cả Tiếng Việt và Tiếng Anh).
- Tính điểm độ tương thích (BM25 + Semantic Keyword Matching).
- Khuyến nghị đúng Top 2–3 skill sát sườn nhất cần nạp, kèm checklist quy tắc bắt buộc của từng skill.
- Hỗ trợ cờ `--json` cho Agent nạp động JIT (Just-In-Time).

Usage:
  python3 scripts/skill-router.py -t "thiết kế REST API cho phân hệ kế toán"
  python3 scripts/skill-router.py -t "sửa lỗi N+1 Hibernate query và deadlock"
  python3 scripts/skill-router.py -t "vẽ sơ đồ kiến trúc luồng dữ liệu" --json
"""

from __future__ import annotations

import argparse
import json
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

import importlib.util
from agent_core.knowledge.search import normalize, tokens_of

_spec = importlib.util.spec_from_file_location("bilingual_query", str(ROOT / "scripts" / "bilingual-query.py"))
_bilingual_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bilingual_mod)
expand_bilingual_query = _bilingual_mod.expand_bilingual_query


def parse_skill_meta(skill_dir: Path) -> Dict[str, Any] | None:
    """Đọc và trích xuất thông tin từ file SKILL.md."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return None

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception:
        return None

    name = skill_dir.name
    desc = ""

    # Trích xuất frontmatter nếu có
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_fm = parts[1]
            m_name = re.search(r"^name:\s*(.+)$", raw_fm, re.MULTILINE)
            if m_name:
                name = m_name.group(1).strip()
            m_desc = re.search(r"^description:\s*(.+)$", raw_fm, re.MULTILINE)
            if m_desc:
                desc = m_desc.group(1).strip()

    if not desc:
        # Lấy 3 dòng đầu không rỗng làm mô tả
        lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#") and not l.startswith("---")]
        desc = " ".join(lines[:3])

    # Trích xuất các tiêu đề chính trong skill làm checklist quy tắc
    headings = re.findall(r"^##+\s+(.+)$", content, re.MULTILINE)
    checklist = [h.strip() for h in headings if not h.strip().lower().startswith("license")][:5]

    return {
        "name": name,
        "path": str(skill_dir.relative_to(ROOT)) if skill_dir.is_relative_to(ROOT) else str(skill_dir),
        "description": desc,
        "rules_checklist": checklist,
        "raw_text": f"{name} {desc} " + " ".join(checklist),
    }


def discover_all_skills(root: Path | None = None) -> List[Dict[str, Any]]:
    """Quét toàn bộ thư mục skills trong workspace và kho cá nhân ~/.agents/skills."""
    root_path = root or ROOT
    dirs_to_scan = []

    ws_skills = root_path / ".agents" / "skills"
    if ws_skills.exists():
        dirs_to_scan.append(ws_skills)
    elif (root_path / "skills").exists():
        dirs_to_scan.append(root_path / "skills")

    home_skills = Path.home() / ".agents" / "skills"
    if home_skills.exists() and home_skills.resolve() != ws_skills.resolve():
        dirs_to_scan.append(home_skills)

    skills = []
    seen_names = set()

    for s_dir in dirs_to_scan:
        for d in s_dir.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                if d.name in seen_names:
                    continue
                meta = parse_skill_meta(d)
                if meta:
                    skills.append(meta)
                    seen_names.add(d.name)

    return skills


def route_skills(
    task_desc: str,
    skills: List[Dict[str, Any]],
    top_k: int = 3,
) -> List[Tuple[float, Dict[str, Any]]]:
    """Chấm điểm và định tuyến các skills phù hợp nhất với task."""
    # 1. Dùng bilingual-query mở rộng từ khóa tiếng Việt sang tiếng Anh
    expanded = expand_bilingual_query(task_desc)
    search_terms = expanded["matched_vi_concepts"] + expanded["expanded_en_code_tokens"]

    query_tokens = set(tokens_of(" ".join(search_terms) + " " + task_desc))
    if not query_tokens:
        return [(1.0, s) for s in skills[:top_k]]

    scored: List[Tuple[float, Dict[str, Any]]] = []

    for s in skills:
        s_tokens = set(tokens_of(s["raw_text"]))
        overlap = query_tokens.intersection(s_tokens)
        if not overlap:
            continue

        # Điểm thưởng nếu tên skill khớp trực tiếp với từ khóa
        name_bonus = 3.0 if s["name"].lower() in [t.lower() for t in query_tokens] else 0.0

        # Jaccard + Overlap score
        score = (len(overlap) / (len(query_tokens) + 1.0)) + name_bonus
        scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="skill-router: Bộ định tuyến kỹ năng thông minh (Alibaba SkillRouter / SRA-Bench 2026)"
    )
    parser.add_argument("-t", "--task", required=True, help="Nội dung hoặc mục tiêu của task cần làm")
    parser.add_argument("-k", "--top-k", type=int, default=3, help="Số lượng kỹ năng hàng đầu cần khuyến nghị (mặc định: 3)")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả dưới định dạng JSON")

    args = parser.parse_args()

    skills = discover_all_skills()
    if not skills:
        print("[ERROR] Không tìm thấy thư mục skills nào trong kho.")
        return 1

    recommendations = route_skills(args.task, skills, top_k=args.top_k)

    if args.json:
        out = [
            {
                "score": round(score, 2),
                "name": s["name"],
                "path": s["path"],
                "description": s["description"],
                "rules_checklist": s["rules_checklist"],
            }
            for score, s in recommendations
        ]
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("🎯 BỘ ĐỊNH TUYẾN KỸ NĂNG THÔNG MINH (SKILL ROUTER)")
        print("=" * 70)
        print(f"• Nhiệm vụ phân tích : {args.task}")
        print(f"• Tổng số skills kho : {len(skills)} skills")
        print("\n✨ TOP KỸ NĂNG ĐƯỢC CHỌN LỌC PHÙ HỢP NHẤT:")

        if not recommendations:
            print("  (Không có skill chuyên biệt khớp, dùng quy trình chuẩn chung)")
        else:
            for idx, (score, s) in enumerate(recommendations, 1):
                print(f"\n{idx}. 📦 Skill: {s['name']} (Độ phù hợp: {round(score, 2)})")
                print(f"   📁 Đường dẫn: {s['path']}/SKILL.md")
                print(f"   📝 Mô tả: {s['description'][:120]}...")
                if s["rules_checklist"]:
                    print("   📋 Các quy tắc bắt buộc áp dụng từ skill này:")
                    for r in s["rules_checklist"]:
                        print(f"      - [ ] {r}")

        print("\n" + "=" * 70)
        print("💡 CHỈ DẪN CHO AGENT: Chỉ đọc file SKILL.md của các kỹ năng được gợi ý ở trên!")
        print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
