#!/usr/bin/env python3
"""
scripts/crawl_sourcemaking_uml.py
Crawl and archive the entire SourceMaking UML 2.0 tutorial and Airport Case Study.
Downloads all 71 articles, text content, tables, and diagram images.
Stores output self-contained inside assets/sourcemaking-uml/
"""

import os
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = ROOT / "assets" / "sourcemaking-uml"
PAGES_DIR = TARGET_DIR / "pages"
IMAGES_DIR = TARGET_DIR / "images"

TARGET_DIR.mkdir(parents=True, exist_ok=True)
PAGES_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://sourcemaking.com"
START_URL = "https://sourcemaking.com/uml/basic-principles-and-background/introduction-to-the-case-study"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def download_image(img_url: str, dest_path: Path):
    if dest_path.exists() and dest_path.stat().st_size > 0:
        return
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(img_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            with open(dest_path, "wb") as f:
                f.write(data)
    except Exception as e:
        print(f"    [WARN] Failed to download image {img_url}: {e}")

def html_to_markdown(article_el, base_page_url: str, page_img_dir: Path, rel_img_prefix: str) -> tuple[str, list]:
    images_found = []
    
    # Process images first: download and update src
    for img in article_el.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        full_img_url = urllib.parse.urljoin(BASE_URL, src)
        img_name = Path(urllib.parse.urlparse(src).path).name
        if not img_name:
            continue
        
        # Download to global images and local page images
        global_dest = IMAGES_DIR / img_name
        local_dest = page_img_dir / img_name
        download_image(full_img_url, global_dest)
        download_image(full_img_url, local_dest)
        
        alt_text = img.get("alt") or ""
        caption = alt_text
        # Check next sibling or parent for caption
        parent = img.parent
        if parent and parent.name in ["figure", "div", "p"]:
            figcaption = parent.find(["figcaption", "em", "i"])
            if figcaption and figcaption.get_text(strip=True):
                caption = figcaption.get_text(strip=True)
        
        images_found.append({
            "img_name": img_name,
            "url": full_img_url,
            "caption": caption or alt_text or img_name,
            "local_path": f"{rel_img_prefix}/{img_name}"
        })
        
        # Replace img tag with a markdown token placeholder
        token = f"\n\n![{caption}]({rel_img_prefix}/{img_name})\n\n"
        img.replace_with(token)

    # Convert headers
    for h in article_el.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(h.name[1])
        h_text = h.get_text(strip=True)
        h.replace_with(f"\n\n{'#' * level} {h_text}\n\n")

    # Convert paragraphs
    for p in article_el.find_all("p"):
        p_text = p.get_text(strip=True)
        if p_text:
            p.replace_with(f"\n\n{p_text}\n\n")

    # Convert unordered lists
    for ul in article_el.find_all("ul"):
        items = []
        for li in ul.find_all("li", recursive=False):
            items.append(f"- {li.get_text(strip=True)}")
        ul.replace_with("\n" + "\n".join(items) + "\n")

    # Convert ordered lists
    for ol in article_el.find_all("ol"):
        items = []
        for idx, li in enumerate(ol.find_all("li", recursive=False), 1):
            items.append(f"{idx}. {li.get_text(strip=True)}")
        ol.replace_with("\n" + "\n".join(items) + "\n")

    # Tables
    for tbl in article_el.find_all("table"):
        rows = tbl.find_all("tr")
        if not rows:
            continue
        md_table = []
        for r_idx, row in enumerate(rows):
            cols = [td.get_text(strip=True).replace("\n", " ") for td in row.find_all(["th", "td"])]
            md_table.append("| " + " | ".join(cols) + " |")
            if r_idx == 0:
                md_table.append("| " + " | ".join(["---"] * len(cols)) + " |")
        tbl.replace_with("\n\n" + "\n".join(md_table) + "\n\n")

    text = article_el.get_text()
    # Clean up excess blank lines
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text, images_found

def main():
    print(f"=== KHỞI ĐỘNG CRAWL TOÀN BỘ SOURCEMAKING UML TUTORIAL ===")
    print(f"Trang khởi đầu: {START_URL}")
    
    start_html = fetch_html(START_URL)
    soup = BeautifulSoup(start_html, "html.parser")
    
    # Find all unique links
    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/uml") and not href.endswith("/uml"):
            full = urllib.parse.urljoin(BASE_URL, href)
            if full not in seen:
                seen.add(full)
                links.append(full)
                
    print(f"Tìm thấy tổng cộng {len(links)} trang UML cần crawl.")
    
    manifest_articles = []
    total_images_collected = 0
    
    for idx, page_url in enumerate(links, 1):
        rel_slug = page_url.replace(BASE_URL + "/uml/", "").strip("/")
        if not rel_slug:
            rel_slug = "index"
        
        parts = rel_slug.split("/")
        category = parts[0] if len(parts) > 1 else "general"
        doc_name = parts[-1]
        
        category_dir = PAGES_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        doc_dir = category_dir / doc_name
        doc_dir.mkdir(parents=True, exist_ok=True)
        img_dir = doc_dir / "images"
        img_dir.mkdir(parents=True, exist_ok=True)
        
        dest_md = doc_dir / "README.md"
        
        print(f"[{idx}/{len(links)}] Crawling: {page_url} -> {category}/{doc_name}")
        
        try:
            html = fetch_html(page_url)
            page_soup = BeautifulSoup(html, "html.parser")
            
            article = page_soup.find("article") or page_soup.find("div", class_="article-content")
            if not article:
                print(f"    [WARN] Không tìm thấy thẻ article trên {page_url}")
                continue
            
            # Title
            h1 = article.find("h1")
            title = h1.get_text(strip=True) if h1 else doc_name.replace("-", " ").title()
            
            md_content, imgs = html_to_markdown(article, page_url, img_dir, "images")
            total_images_collected += len(imgs)
            
            header_meta = f"""# {title}

> **Nguồn gốc:** [{page_url}]({page_url})  
> **Phân mục:** SourceMaking UML 2.0 / {category}  
> **Số lượng hình ảnh:** {len(imgs)}  

---

"""
            full_md = header_meta + md_content
            dest_md.write_text(full_md, encoding="utf-8")
            
            manifest_articles.append({
                "url": page_url,
                "title": title,
                "category": category,
                "slug": rel_slug,
                "file_path": f"assets/sourcemaking-uml/pages/{category}/{doc_name}/README.md",
                "images": imgs
            })
            
            time.sleep(0.3)  # Gentle delay
            
        except Exception as e:
            print(f"    [ERROR] Lỗi khi tải {page_url}: {e}")

    # Write summary index
    index_file = TARGET_DIR / "INDEX.md"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("# SourceMaking UML 2.0 & Case Study — Index\n\n")
        f.write(f"Tổng số bài viết: {len(manifest_articles)}  \n")
        f.write(f"Tổng số hình ảnh / sơ đồ: {total_images_collected}  \n\n")
        
        current_cat = None
        for a in manifest_articles:
            if a["category"] != current_cat:
                current_cat = a["category"]
                f.write(f"\n## Phân mục: {current_cat.upper()}\n\n")
            f.write(f"- [{a['title']}]({a['file_path']}) ({len(a['images'])} ảnh)\n")
            
    print(f"\n=== HOÀN TẤT CRAWL SOURCEMAKING UML ===")
    print(f"- Tổng số bài viết: {len(manifest_articles)}")
    print(f"- Tổng số ảnh đã tải: {total_images_collected}")
    print(f"- File mục lục: {index_file}")

if __name__ == "__main__":
    main()
