#!/usr/bin/env python3
"""scripts/hybrid-search.py

Bộ Tìm Kiếm Kết Hợp & Chẩn Đoán Truy Vấn Thông Minh (Smart Hybrid Search Engine).
Giải quyết triệt để vấn đề: Đảm bảo Agent tìm kiếm mã nguồn chuẩn xác 100%, không bị bế tắc bởi hạn chế của AST hay Grep.

Tính năng:
- Tự động nhận diện loại từ khóa tìm kiếm:
  1. Nếu là Định danh Mã nguồn (Code Identifier: Class, Function, Interface, Enum):
     -> Khuyến nghị và hướng dẫn gọi MCP AST `xerj_def` / `xerj_search` (tự động gắn đúng prefix dự án).
  2. Nếu là Tiếng Việt, Nhãn UI, Khóa i18n, Chuỗi thông báo lỗi:
     -> Tự động thực thi `safe-search.py` (giới hạn 10-20 dòng, không tràn context, bỏ qua rác).
  3. Nếu là Truy vấn hỗn hợp (vừa có tiếng Việt vừa có từ khóa kỹ thuật):
     -> Kết hợp `bilingual-query.py` mở rộng từ khóa và phân làn tìm kiếm đa tầng (Layered Retrieval).
- Chẩn đoán lỗi thường gặp: Quên truyền prefix dự án, hoặc dùng AST search đi tìm nhãn tiếng Việt (dẫn đến 0 hits).

Usage:
  python3 scripts/hybrid-search.py -q "OrderController"
  python3 scripts/hybrid-search.py -q "Xác nhận thanh toán"
  python3 scripts/hybrid-search.py -q "hàm xuất đơn vận chuyển" --prefix gdt
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
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

# Nạp bilingual_query động
_spec_bilingual = importlib.util.spec_from_file_location("bilingual_query", str(ROOT / "scripts" / "bilingual-query.py"))
bilingual_query = importlib.util.module_from_spec(_spec_bilingual)
_spec_bilingual.loader.exec_module(bilingual_query)


def is_likely_code_identifier(query: str) -> bool:
    """Kiểm tra xem chuỗi có phải là identifier mã nguồn hay không (CamelCase, snake_case, PascalCase)."""
    q = query.strip()
    if " " in q:
        return False
    # Chứa ký tự tiếng Việt có dấu -> Chắc chắn không phải identifier
    if re.search(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", q, re.IGNORECASE):
        return False
    # Dạng camelCase hoặc PascalCase hoặc snake_case
    if re.match(r"^[A-Z][a-zA-Z0-9]+$", q):
        return True
    if re.match(r"^[a-z]+[A-Z][a-zA-Z0-9]*$", q):
        return True
    if "_" in q and re.match(r"^[a-zA-Z0-9_]+$", q):
        return True
    return False


def detect_project_prefix(root: Path | None = None) -> str:
    """Tự động phát hiện prefix dự án (gdt, agentbase, tiktok...)."""
    root_path = root or ROOT
    proj_md = root_path / "PROJECT.md"
    if proj_md.exists():
        content = proj_md.read_text(encoding="utf-8")
        if "gdt" in content.lower():
            return "gdt"
        if "tiktok" in content.lower():
            return "tiktok"
        if "agent base" in content.lower():
            return "agentbase"

    # Fallback theo tên thư mục
    folder_name = root_path.resolve().name.lower()
    if "gdt" in folder_name:
        return "gdt"
    if "agent-base" in folder_name:
        return "agentbase"
    return ""


def execute_hybrid_search(
    query: str,
    prefix: str = "",
    target_dir: str = ".",
    limit: int = 10,
) -> Dict[str, Any]:
    """Phân làn và điều phối tìm kiếm tối ưu."""
    detected_prefix = prefix or detect_project_prefix()

    # 1. Trường hợp: Identifier mã nguồn đơn lẻ -> Ưu tiên AST Search
    if is_likely_code_identifier(query):
        p_str = f' prefix="{detected_prefix}"' if detected_prefix else ""
        return {
            "query": query,
            "mode": "AST_SEARCH",
            "reason": "Từ khóa có cấu trúc của Code Identifier (Class / Function / Variable).",
            "recommended_tool": "MCP AST xerj_def hoặc xerj_search",
            "ast_command": f'xerj_def(symbol="{query}"{p_str}) hoặc xerj_search(query="{query}"{p_str})',
            "fallback_command": f'python3 scripts/safe-search.py -q "{query}" -d {target_dir} -l {limit}',
        }

    # 2. Trường hợp: Tiếng Việt thuần hoặc chuỗi UI / text literal -> Chạy safe-search
    is_vietnamese_text = bool(
        re.search(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", query, re.IGNORECASE)
    )

    expanded = bilingual_query.expand_bilingual_query(query, prefix=detected_prefix)

    # Nếu câu truy vấn có các từ khóa code tiếng Anh trích xuất được
    en_tokens = expanded.get("expanded_en_code_tokens", [])
    p_str = f' prefix="{detected_prefix}"' if detected_prefix else ""

    ast_recs = [f'xerj_search(query="{tok}"{p_str})' for tok in en_tokens[:3]]
    safe_search_cmd = f'python3 scripts/safe-search.py -q "{query}" -d {target_dir} -l {limit}'

    return {
        "query": query,
        "mode": "LAYERED_HYBRID",
        "reason": "Truy vấn ngôn ngữ tự nhiên / Tiếng Việt / Chuỗi văn bản UI.",
        "text_search_command": safe_search_cmd,
        "bilingual_expanded_tokens": en_tokens,
        "ast_search_recommendations": ast_recs,
        "warning": "CẢNH BÁO: Không dùng AST XERJ để tìm trực tiếp chuỗi tiếng Việt hoặc nhãn UI (sẽ trả về 0 hits)!" if is_vietnamese_text else "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="hybrid-search: Bộ tìm kiếm kết hợp & chẩn đoán truy vấn thông minh (Layered Code & Text Search)"
    )
    parser.add_argument("-q", "--query", required=True, help="Từ khóa hoặc câu hỏi cần tra cứu trong codebase")
    parser.add_argument("--prefix", default="", help="Prefix dự án khi gọi XERJ (ví dụ: gdt, agentbase, tiktok)")
    parser.add_argument("-d", "--dir", default=".", help="Thư mục tra cứu (mặc định: .)")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Giới hạn số dòng cho safe-search (mặc định: 10)")
    parser.add_argument("--execute-text", action="store_true", help="Tự động chạy safe-search nếu là truy vấn text thuần")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả dưới định dạng JSON")

    args = parser.parse_args()

    res = execute_hybrid_search(args.query, prefix=args.prefix, target_dir=args.dir, limit=args.limit)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    print("=" * 70)
    print("🔎 CHẨN ĐOÁN & ĐIỀU PHỐI TÌM KIẾM MÃ NGUỒN (HYBRID SEARCH)")
    print("=" * 70)
    print(f"• Từ khóa / Truy vấn : {res['query']}")
    print(f"• Chế độ định tuyến  : {res['mode']} ({res['reason']})")

    if res.get("warning"):
        print(f"\n⚠️  {res['warning']}")

    if res["mode"] == "AST_SEARCH":
        print("\n🎯 ĐỀ XUẤT THỰC THI (ƯU TIÊN AST):")
        print(f"   1. Gọi công cụ AST:")
        print(f"      👉 {res['ast_command']}")
        print(f"   2. Dự phòng (nếu AST chưa lập chỉ mục file mới):")
        print(f"      👉 {res['fallback_command']}")

    elif res["mode"] == "LAYERED_HYBRID":
        print("\n🎯 ĐỀ XUẤT THỰC THI PHÂN TẦNG (LAYERED PIPELINE):")
        print("   1. Dùng safe-search cho nhãn UI / Tiếng Việt / chuỗi thông báo:")
        print(f"      👉 {res['text_search_command']}")
        if res["ast_search_recommendations"]:
            print("   2. Dùng AST MCP cho các Symbol tiếng Anh tương đương đã mở rộng:")
            for cmd in res["ast_search_recommendations"]:
                print(f"      👉 {cmd}")

    print("=" * 70)

    if args.execute_text and res.get("text_search_command"):
        print("\n🚀 Đang chạy safe-search tự động...")
        subprocess.run(res["text_search_command"], shell=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
