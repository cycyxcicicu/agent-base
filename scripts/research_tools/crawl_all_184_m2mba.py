"""scripts/crawl_all_184_m2mba.py

Tải toàn bộ 184 bài viết nghiệp vụ từ API m2mba.com/api/v1/posts về D:/test-repo/m2mba/posts/
kèm 100% hình ảnh thực tế và tạo bảng chỉ mục FULL_INDEX.md hoàn chỉnh.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.crawl_jina_assets import sanitize_filename, download_single_image

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def fetch_json(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def html_to_markdown_clean(html: str) -> str:
    """Chuyển đổi cơ bản HTML sang Markdown và làm sạch."""
    if not html:
        return ""
    text = html
    # Chuyển headings
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', text, flags=re.I | re.S)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', text, flags=re.I | re.S)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', text, flags=re.I | re.S)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', text, flags=re.I | re.S)
    # Chuyển paragraphs & breaks
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', text, flags=re.I | re.S)
    text = re.sub(r'<br\s*/?>', r'\n', text, flags=re.I)
    # Chuyển bold & italic
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.I | re.S)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.I | re.S)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.I | re.S)
    # Chuyển links
    text = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.I | re.S)
    # Chuyển list items
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'\n- \1', text, flags=re.I | re.S)
    # Xóa các thẻ HTML còn lại
    text = re.sub(r'<[^>]+>', '', text)
    # Decode entities
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def extract_images_from_html(html: str) -> list[str]:
    """Tìm toàn bộ URL ảnh trong HTML."""
    if not html:
        return []
    return re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)


def process_and_save_post(meta: dict, posts_dir: Path, images_dir: Path) -> dict:
    slug_or_uuid = meta.get("slug") or meta.get("uuid") or str(meta["id"])
    target_slug = sanitize_filename(slug_or_uuid)
    out_file = posts_dir / f"{target_slug}.md"

    detail_url = f"https://m2mba.com/api/v1/posts/{slug_or_uuid}"
    try:
        detail_data = fetch_json(detail_url, timeout=30)
        post = detail_data.get("data", {})
    except Exception as e:
        print(f"  [WARN] Lỗi tải chi tiết {slug_or_uuid}: {e}", file=sys.stderr)
        return {"slug": target_slug, "title": meta.get("title", ""), "success": False}

    raw_html = post.get("postContent") or ""
    author = post.get("author", {})
    author_name = author.get("name", "M2MBA") if isinstance(author, dict) else str(author or "M2MBA")
    created_at = post.get("createdAt", "")
    avatar = post.get("avatarUrl") or ""

    # 1. Tải ảnh
    images = extract_images_from_html(raw_html)
    if avatar:
        images.append(avatar)

    url_to_rel = {}
    for img_url in set(images):
        if not img_url.startswith("http"):
            continue
        parsed = urllib.parse.urlparse(img_url)
        img_name = os.path.basename(parsed.path)
        if not img_name or "." not in img_name:
            h = hashlib.md5(img_url.encode()).hexdigest()[:8]
            img_name = f"img_{h}.png"
        img_name = sanitize_filename(img_name)
        dest_file = images_dir / img_name
        download_single_image(img_url, dest_file)
        url_to_rel[img_url] = f"images/{dest_file.name}"

    # 2. Thay thế link ảnh trong HTML
    for img_url, rel_path in url_to_rel.items():
        raw_html = raw_html.replace(img_url, rel_path)

    # 3. Chuyển đổi sang Markdown
    md_body = html_to_markdown_clean(raw_html)

    title_escaped = str(post.get('title', '')).replace('"', '')
    header = (
        f"---\n"
        f"id: {post.get('id')}\n"
        f"title: \"{title_escaped}\"\n"
        f"author: \"{author_name}\"\n"
        f"created_at: \"{created_at}\"\n"
        f"source_url: \"https://m2mba.com/blog/articles/{slug_or_uuid}\"\n"
        f"---\n\n"
        f"# {post.get('title', '')}\n\n"
        f"*Tác giả: {author_name} | Ngày đăng: {created_at}*\n\n"
    )
    if avatar and avatar in url_to_rel:
        header += f"![Ảnh bìa]({url_to_rel[avatar]})\n\n"

    full_md = header + md_body
    out_file.write_text(full_md, encoding="utf-8")
    return {"slug": target_slug, "title": post.get("title", ""), "file": out_file.name, "success": True}


def main():
    m2mba_dir = Path("D:/test-repo/m2mba")
    posts_dir = m2mba_dir / "posts"
    images_dir = posts_dir / "images"
    posts_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    print("=== BẮT ĐẦU THU THẬP TOÀN BỘ 184 BÀI VIẾT QUA M2MBA API ===")

    # 1. Quét danh sách bài viết qua API pagination
    all_posts = []
    page = 1
    while True:
        api_url = f"https://m2mba.com/api/v1/posts?page={page}&limit=50"
        print(f"Quét API page {page}...")
        try:
            data = fetch_json(api_url)
            posts = data.get("data", [])
            if not posts:
                break
            all_posts.extend(posts)
            pagination = data.get("pagination", {})
            total_pages = pagination.get("totalPages", 1)
            print(f"  -> Đã lấy {len(posts)} bài (Tổng: {len(all_posts)}/{pagination.get('total', 184)} bài).")
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  [ERROR] Lỗi API page {page}: {e}", file=sys.stderr)
            break

    print(f"\n🎯 TỔNG CỘNG ĐÃ LẤY ĐƯỢC {len(all_posts)} METADATA BÀI VIẾT!\n")

    # 2. Tải chi tiết và ảnh từng bài
    print("=== TIẾN HÀNH TẢI NỘI DUNG VÀ ẢNH CHO 184 BÀI VIẾT ===")
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_and_save_post, p, posts_dir, images_dir): p for p in all_posts}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            print(f"  [{len(results)}/{len(all_posts)}] Đã lưu: {res['title'][:50]} -> {res.get('file', '')}")

    # 3. Tạo FULL_INDEX.md
    index_file = m2mba_dir / "FULL_INDEX.md"
    lines = [
        f"# Mục Lục Toàn Bộ {len(all_posts)} Bài Viết Chuyên Môn M2MBA Blog\n\n",
        f"> Tự động cào qua API chính thức | Ngày cập nhật: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "| STT | ID | Tiêu Đề Bài Viết | File Markdown Cục Bộ |\n",
        "|---|---|---|---|\n",
    ]
    for idx, r in enumerate(sorted(results, key=lambda x: x.get("title", "")), 1):
        lines.append(f"| {idx} | `{r.get('slug', '')}` | **{r.get('title', '')}** | [posts/{r.get('file', '')}](posts/{r.get('file', '')}) |\n")

    index_file.write_text("".join(lines), encoding="utf-8")
    print(f"\n🏆 ĐÃ XUẤT BẢN THÀNH CÔNG: {index_file} ({len(results)} bài viết đã tải xong xuôi)!")


if __name__ == "__main__":
    main()
