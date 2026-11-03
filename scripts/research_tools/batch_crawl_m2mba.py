"""scripts/batch_crawl_m2mba.py

Cào bài viết phân tích nghiệp vụ từ m2mba.com/blog về D:/test-repo/m2mba/
kèm 100% hình ảnh infographic, phân loại theo vai trò (BA, Product, Architect).
"""

from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.crawl_jina_assets import crawl_page, fetch_jina_markdown

BASE_BLOG_URL = "https://m2mba.com/blog"

KEY_ARTICLES = [
    {
        "url": "https://m2mba.com/blog/articles/ba-khong-can-hieu-ky-thuat-nhung-can-hieu-dung-2-thu-nay-khi-lam-viec-voi-dev",
        "slug": "ba-lam-viec-voi-dev-2-dieu-cot-loi",
        "title": "BA không cần hiểu kỹ thuật — nhưng cần hiểu đúng 2 thứ này khi làm việc với Dev",
        "role": "ba",
        "summary": "Kỹ năng giao tiếp và bóc tách yêu cầu khả thi giữa Business Analyst và Development Team.",
    },
    {
        "url": "https://m2mba.com/blog/articles/tai-lieu-mau-srs-cua-hoc-vien",
        "slug": "tai-lieu-mau-srs-chuan",
        "title": "Tài liệu mẫu SRS (Software Requirements Specification)",
        "role": "ba",
        "summary": "Mẫu đặc tả yêu cầu phần mềm chuẩn cho dự án thực tế từ đầu đến cuối.",
    },
    {
        "url": "https://m2mba.com/blog/articles/ky-thuat-state-diagram-cho-business-analyst",
        "slug": "state-diagram-cho-ba-huong-dan-chi-tiet",
        "title": "Kỹ thuật State Diagram cho Business Analyst: Hướng dẫn chi tiết & Các sai lầm cần tránh",
        "role": "ba",
        "summary": "Phương pháp mô hình hóa các trạng thái nghiệp vụ và chuyển trạng thái không bị sót case.",
    },
    {
        "url": "https://m2mba.com/blog/articles/vi-sao-ba-nen-hieu-mcp",
        "slug": "vi-sao-ba-nen-hieu-mcp-tool-calling",
        "title": "Vì sao BA nên hiểu Model Context Protocol (MCP) & Tool Calling trong AI",
        "role": "architect",
        "summary": "Cơ chế Tool Calling, chuẩn giao tiếp MCP và ứng dụng vào tự động hóa phân tích nghiệp vụ.",
    },
    {
        "url": "https://m2mba.com/blog/articles/c4887a1a-8104-4bc2-82f3-4b5ef5bacd9a",
        "slug": "giai-ma-langchain-rag-chatbot-cho-ba",
        "title": "Giải Mã Sức Mạnh của LangChain, RAG và Chatbot: Hướng Dẫn Dành Cho BA",
        "role": "architect",
        "summary": "Hiểu cấu trúc Retrieval-Augmented Generation, vector embedding và prompt engineering.",
    },
    {
        "url": "https://m2mba.com/blog/articles/ai-agent-builder-openAI",
        "slug": "ai-agent-builder-workflow-api",
        "title": "AI Agent Builder: Thiết kế Workflow và Gọi API Tự Động",
        "role": "product",
        "summary": "Định hình sản phẩm ứng dụng AI Agent, thiết kế luồng người dùng và API integration.",
    },
    {
        "url": "https://m2mba.com/blog/articles/tu-vector-rag-embeddingmodel-den-chatbot",
        "slug": "tu-vector-rag-den-chatbot-thong-minh",
        "title": "Từ Vector đến Chatbot: Hành trình để AI hiểu và trả lời như con người",
        "role": "architect",
        "summary": "Cách thức xử lý dữ liệu phi cấu trúc, vector search và indexing cho hệ thống AI.",
    },
    {
        "url": "https://m2mba.com/blog/articles/lo-trinh-iiba-nang-tam-su-nghiep-ba",
        "slug": "lo-trinh-chuan-iiba-cho-business-analyst",
        "title": "Lộ trình IIBA – Chuẩn Khung Năng Lực Quốc Tế Cho Phân Tích Nghiệp Vụ",
        "role": "ba",
        "summary": "Khung chuẩn BABOK, 6 vùng tri thức (Knowledge Areas) và quy trình quản trị yêu cầu.",
    },
]


def main():
    m2mba_dir = Path("D:/test-repo/m2mba")
    posts_dir = m2mba_dir / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)

    print("=== BẮT ĐẦU CÀO CÁC BÀI VIẾT CHỦ LỰC TỪ M2MBA.COM/BLOG ===")

    downloaded = []
    for idx, item in enumerate(KEY_ARTICLES, 1):
        print(f"\n[{idx}/{len(KEY_ARTICLES)}] Đang tải bài: {item['title']}...")
        try:
            out_file = crawl_page(
                target_url=item["url"],
                out_dir=posts_dir,
                doc_slug=item["slug"],
                download_images=True,
                max_workers=5,
                timeout=45,
            )
            downloaded.append({**item, "file": out_file.relative_to(m2mba_dir).as_posix()})
            time.sleep(1)
        except Exception as e:
            print(f"  [WARN] Lỗi tải bài {item['slug']}: {e}", file=sys.stderr)

    # Sinh file CLASSIFICATION.md
    clf_path = m2mba_dir / "CLASSIFICATION.md"
    content = [
        "# Bảng Phân Loại & Đánh Giá Tri Thức M2MBA Cho Đội Ngũ Agent\n\n",
        "Tài liệu này đánh giá các bài viết chuyên môn từ m2mba.com/blog và phân bổ tri thức vào các vai trò tương ứng trong `agent-base`.\n\n",
        "## 1. Phân Bổ Theo Vai Trò\n\n",
        "### A. Vai Business Analyst (`ba`)\n",
        "- **Kỹ năng cốt lõi**: Khảo sát nghiệp vụ, quản lý yêu cầu (BABOK), đặc tả SRS, mô hình hóa State Machine, kỹ năng làm việc với Dev.\n",
        "- **Bài viết tương ứng**:\n",
    ]

    for d in [x for x in downloaded if x.get("role") == "ba"]:
        content.append(f"  - **[{d['title']}]({d['file']})**\n    - *Tóm tắt*: {d['summary']}\n")

    content.append("\n### B. Vai Product Lead / Manager (`product`)\n")
    content.append("- **Kỹ năng cốt lõi**: Định hình tính năng, Scope-Cut, xây dựng workflow cho AI Agent, MVP roadmap.\n")
    content.append("- **Bài viết tương ứng**:\n")
    for d in [x for x in downloaded if x.get("role") == "product"]:
        content.append(f"  - **[{d['title']}]({d['file']})**\n    - *Tóm tắt*: {d['summary']}\n")

    content.append("\n### C. Vai System Architect (`architect`)\n")
    content.append("- **Kỹ năng cốt lõi**: Thiết kế RAG, Vector Search, giao thức MCP Tool Calling, tích hợp hệ thống LLM.\n")
    content.append("- **Bài viết tương ứng**:\n")
    for d in [x for x in downloaded if x.get("role") == "architect"]:
        content.append(f"  - **[{d['title']}]({d['file']})**\n    - *Tóm tắt*: {d['summary']}\n")

    clf_path.write_text("".join(content), encoding="utf-8")
    print(f"\n[OK] Đã xuất bản phân loại tri thức: {clf_path}")


if __name__ == "__main__":
    main()

