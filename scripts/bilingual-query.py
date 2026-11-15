#!/usr/bin/env python3
"""scripts/bilingual-query.py

Cầu Nối Truy Vấn Song Ngữ & Mở Rộng Từ Khóa Mã Nguồn (Bilingual Query Bridge & Code Expansion Engine).
Giải quyết triệt để bài toán: Người dùng hỏi bằng Tiếng Việt nhưng Mã nguồn và Tri thức lưu bằng Tiếng Anh.

Tính năng:
- Nhận đầu vào câu hỏi / yêu cầu tiếng Việt của người dùng.
- Tự động phân tích và tra cứu từ điển đồng nghĩa kỹ thuật `agents/knowledge/synonyms.json`.
- Sinh ra:
  * Các từ khóa mã nguồn Tiếng Anh tương đương (Code Tokens: Class, Method, Variable).
  * Gợi ý câu lệnh tìm kiếm AST cấu trúc (`xerj_def` / `xerj_search` kèm prefix dự án).
  * Gợi ý câu lệnh tìm kiếm text thuần (`safe-search.py` cho nhãn UI tiếng Việt / i18n).
- Hỗ trợ cờ `--json` để các Agent tích hợp trực tiếp vào pipeline tìm kiếm tự động.

Usage:
  python3 scripts/bilingual-query.py -q "sửa bug khóa lạc quan và nợ kỹ thuật"
  python3 scripts/bilingual-query.py -q "xuất đơn vận chuyển j&t" --prefix gdt
  python3 scripts/bilingual-query.py -q "thanh toán qr" --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent

# Từ điển ánh xạ nghiệp vụ cơ bản bổ trợ nhanh cho mã nguồn phần mềm
CORE_MAPPINGS = {
    "vận đơn": ["waybill", "tracking_number", "consignment", "shipping_label"],
    "xuất đơn": ["dispatch", "fulfill", "ship_order", "export_order"],
    "đơn hàng": ["order", "purchase_order", "order_item"],
    "thanh toán": ["payment", "checkout", "transaction", "billing"],
    "hoàn tiền": ["refund", "reversal", "chargeback"],
    "khóa lạc quan": ["optimistic_lock", "version", "optimistic"],
    "khóa bi quan": ["pessimistic_lock", "for_update", "lock_mode"],
    "phân trang": ["pagination", "pageable", "page", "limit", "offset"],
    "phân quyền": ["authorization", "rbac", "permission", "role"],
    "xác thực": ["authentication", "auth", "jwt", "token"],
    "người dùng": ["user", "account", "principal"],
    "bộ nhớ đệm": ["cache", "redis", "caching"],
    "hàng đợi": ["queue", "kafka", "rabbitmq", "message_broker"],
    "sự cố": ["incident", "outage", "post_mortem", "downtime"],
    "nợ kỹ thuật": ["technical_debt", "debt", "shortcut", "ponytail"],
    "bẫy": ["pitfall", "gotcha", "trap", "caveat"],
    "sơ đồ": ["diagram", "sequence", "erd", "flowchart"],
    "viết như người": ["humanizer", "natural_writing", "prose", "human_like"],
    "văn phong tự nhiên": ["humanizer", "tone", "style", "natural"],
    "viết văn": ["writing", "humanizer", "prose", "copywriting"],
}


def normalize_vietnamese(text: str) -> str:
    """Chuẩn hóa chuỗi tiếng Việt: chữ thường, bỏ dấu thanh, chuyển đ -> d."""
    text = (text or "").lower()
    text = unicodedata.normalize("NFD", text).replace("đ", "d")
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text).strip()


def load_synonyms(synonyms_path: Path | None = None) -> Dict[str, str]:
    """Nạp file từ điển đồng nghĩa Việt-Anh."""
    path = synonyms_path or (ROOT / "agents" / "knowledge" / "synonyms.json")
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        # Loại bỏ trường chú thích nếu có
        return {k: v for k, v in data.items() if not k.startswith("_")}
    except Exception:
        return {}


def expand_bilingual_query(
    user_query: str,
    prefix: str = "",
    synonyms_dict: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """Phân rã câu hỏi tiếng Việt và mở rộng sang thuật ngữ mã nguồn tiếng Anh."""
    synonyms = synonyms_dict if synonyms_dict is not None else load_synonyms()
    norm_query = normalize_vietnamese(user_query)

    matched_vi_terms: List[str] = []
    en_code_tokens: Set[str] = set()

    # 1. Khớp từ điển CORE_MAPPINGS
    for vi_phrase, en_tokens in CORE_MAPPINGS.items():
        norm_vi = normalize_vietnamese(vi_phrase)
        if norm_vi in norm_query:
            matched_vi_terms.append(vi_phrase)
            en_code_tokens.update(en_tokens)

    # 2. Khớp từ điển synonyms.json
    for key, val in synonyms.items():
        norm_key = normalize_vietnamese(key)
        if norm_key in norm_query:
            matched_vi_terms.append(key)
            # Tách các từ tiếng Anh trong val
            for tok in val.split():
                clean_tok = re.sub(r"[^a-zA-Z0-9_\-]", "", tok).strip()
                if clean_tok and len(clean_tok) > 2:
                    en_code_tokens.add(clean_tok.lower())

    # 3. Trích xuất các thực thể tiếng Anh có sẵn trong câu hỏi của người dùng
    raw_en_tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9_\-\.]{2,}\b", user_query)
    for t in raw_en_tokens:
        en_code_tokens.add(t.lower())

    sorted_en_tokens = sorted(list(en_code_tokens))
    prefix_str = f' prefix="{prefix}"' if prefix else ""

    # Gợi ý lệnh tìm kiếm AST
    ast_suggestions = []
    for tok in sorted_en_tokens[:4]:
        ast_suggestions.append(f'xerj_search(query="{tok}"{prefix_str})')

    # Gợi ý lệnh tìm kiếm text thuần tiếng Việt
    text_suggestions = []
    if matched_vi_terms:
        text_suggestions.append(f'python3 scripts/safe-search.py -q "{matched_vi_terms[0]}" -d .')
    else:
        # Lấy cụm từ ngắn từ câu hỏi gốc
        text_suggestions.append(f'python3 scripts/safe-search.py -q "{user_query[:30]}" -d .')

    return {
        "original_query": user_query,
        "normalized_query": norm_query,
        "matched_vi_concepts": sorted(list(set(matched_vi_terms))),
        "expanded_en_code_tokens": sorted_en_tokens,
        "ast_search_recommendations": ast_suggestions,
        "text_search_recommendations": text_suggestions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="bilingual-query: Cầu nối truy vấn song ngữ Việt - Anh cho mã nguồn và tri thức"
    )
    parser.add_argument("-q", "--query", required=True, help="Câu hỏi hoặc yêu cầu tiếng Việt của người dùng")
    parser.add_argument("--prefix", default="", help="Prefix dự án khi gọi AST XERJ (ví dụ: gdt, agentbase, tiktok)")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả dưới định dạng JSON")

    args = parser.parse_args()

    result = expand_bilingual_query(args.query, prefix=args.prefix)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("🌐 CẦU NỐI TRUY VẤN SONG NGỮ (VIETNAMESE ➔ ENGLISH CODE BRIDGE)")
        print("=" * 70)
        print(f"• Yêu cầu gốc        : {result['original_query']}")
        print(f"• Khái niệm nhận diện : {', '.join(result['matched_vi_concepts']) or '(không có)'}")
        print(f"• Từ khóa Code (EN)   : {', '.join(result['expanded_en_code_tokens'][:8]) or '(không có)'}")
        print("\n🔍 KHUYẾN NGHỊ TRA CỨU MÃ NGUỒN CHUẨN XÁC:")
        if result["ast_search_recommendations"]:
            print("  1. Dùng AST MCP cho Symbol/Class tiếng Anh:")
            for cmd in result["ast_search_recommendations"][:3]:
                print(f"     👉 {cmd}")
        if result["text_search_recommendations"]:
            print("  2. Dùng safe-search cho nhãn UI / chuỗi i18n tiếng Việt:")
            for cmd in result["text_search_recommendations"]:
                print(f"     👉 {cmd}")
        print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
