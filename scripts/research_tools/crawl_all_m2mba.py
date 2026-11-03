"""scripts/crawl_all_m2mba.py

Cào toàn bộ 184+ bài viết trên m2mba.com/blog qua cả 19 trang phân trang,
tải đầy đủ nội dung Markdown và 100% hình ảnh thực tế về D:/test-repo/m2mba/posts/
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.crawl_jina_assets import crawl_page, fetch_url, JINA_PREFIX

BASE_URL = "https://m2mba.com"
BLOG_URL = "https://m2mba.com/blog"


def get_all_article_links(max_pages=20) -> list[dict]:
    """Duyệt qua tất cả các trang phân trang để bóc tách 100% link bài viết."""
    articles = {}
    print(f"=== BẮT ĐẦU QUÉT TẤT CẢ CÁC TRANG TỪ 1 ĐẾN {max_pages} CỦA M2MBA BLOG ===")

    for page in range(1, max_pages + 1):
        page_url = f"{BLOG_URL}?page={page}"
        print(f"  [PAGE {page}/{max_pages}] Đang quét: {page_url}...")
        try:
            jina_page_url = f"{JINA_PREFIX}{page_url}"
            content = fetch_url(jina_page_url, timeout=40).decode("utf-8", errors="replace")

            # Tìm các liên kết dạng /blog/articles/... hoặc https://m2mba.com/blog/articles/...
            pat = re.compile(r'\[([^\]]+)\]\((https?://m2mba\.com/blog/articles/[^\s\)\'\"]+|/blog/articles/[^\s\)\'\"]+)\)')
            matches = pat.findall(content)

            new_in_page = 0
            for title, link in matches:
                title = title.strip()
                if not link.startswith("http"):
                    link = f"{BASE_URL}{link}"
                clean_link = link.split("#")[0].split("?")[0].rstrip("/")
                slug = clean_link.split("/")[-1]

                # Bỏ qua ảnh hoặc tiêu đề rác
                if slug and slug not in articles and not title.startswith("Image "):
                    articles[slug] = {
                        "slug": slug,
                        "url": clean_link,
                        "title": title or slug,
                        "page": page,
                    }
                    new_in_page += 1

            print(f"    -> Tìm thấy {new_in_page} bài mới (Tổng tích lũy: {len(articles)} bài).")
            # Nếu trang không có bài viết nào thì dừng sớm
            if new_in_page == 0 and page > 1:
                break
            time.sleep(1)
        except Exception as e:
            print(f"  [WARN] Lỗi quét trang {page}: {e}", file=sys.stderr)

    return list(articles.values())


def main():
    m2mba_dir = Path("D:/test-repo/m2mba")
    posts_dir = m2mba_dir / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)

    # 1. Thu thập toàn bộ danh sách bài viết
    all_articles = get_all_article_links(max_pages=20)
    print(f"\n🎯 TỔNG CỘNG ĐÃ TÌM THẤY {len(all_articles)} BÀI VIẾT DUY NHẤT TRÊN M2MBA BLOG!\n")

    # Lưu danh sách URL
    url_file = m2mba_dir / "all_articles_urls.txt"
    with open(url_file, "w", encoding="utf-8") as f:
        for a in all_articles:
            f.write(f"{a['title']}\t{a['url']}\n")
    print(f"💾 Đã lưu danh sách bài viết vào: {url_file}")

    # 2. Cào toàn bộ bài viết và tải ảnh
    print("\n=== TIẾN HÀNH TẢI TOÀN BỘ BÀI VIẾT VÀ ẢNH VỀ D:/test-repo/m2mba/posts ===")
    success_count = 0
    failures = []

    for idx, item in enumerate(all_articles, 1):
        target_file = posts_dir / f"{item['slug']}.md"
        print(f"[{idx}/{len(all_articles)}] {item['title'][:60]}...")
        if target_file.exists() and target_file.stat().st_size > 1000:
            print(f"  -> [EXISTS] Đã có sẵn ({target_file.stat().st_size} bytes)")
            success_count += 1
            continue

        try:
            crawl_page(
                target_url=item["url"],
                out_dir=posts_dir,
                doc_slug=item["slug"],
                download_images=True,
                max_workers=4,
                timeout=45,
            )
            success_count += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  [WARN] Lỗi tải bài {item['slug']}: {e}", file=sys.stderr)
            failures.append(item)

    # 3. Tạo FULL_INDEX.md
    index_file = m2mba_dir / "FULL_INDEX.md"
    lines = [
        f"# Mục Lục Toàn Bộ {len(all_articles)} Bài Viết M2MBA Blog\n\n",
        f"> Tự động thu thập từ `https://m2mba.com/blog` | Cập nhật ngày {time.strftime('%Y-%m-%d')}\n\n",
        "| STT | Tiêu Đề Bài Viết | Đường Dẫn Markdown Cục Bộ | URL Gốc |\n",
        "|---|---|---|---|\n",
    ]
    for idx, a in enumerate(all_articles, 1):
        md_rel = f"posts/{a['slug']}.md"
        lines.append(f"| {idx} | **{a['title']}** | [{a['slug']}.md]({md_rel}) | [Link]({a['url']}) |\n")

    index_file.write_text("".join(lines), encoding="utf-8")
    print(f"\n🏆 ĐÃ XUẤT BẢN FULL_INDEX TẠI: {index_file}")
    print(f"✅ Hoàn tất thành công: {success_count}/{len(all_articles)} bài viết.")


if __name__ == "__main__":
    main()

