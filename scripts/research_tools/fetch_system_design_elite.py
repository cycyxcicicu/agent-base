import json
import re
import sys
import urllib.request
import urllib.parse
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = ROOT / "assets" / "system-design-elite"
PAGES_DIR = BASE_DIR / "pages"
IMAGES_DIR = BASE_DIR / "images"

BASE_DIR.mkdir(parents=True, exist_ok=True)
PAGES_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

ELITE_FILES = [
    # Nhóm 1: Database Scaling & Storage
    "100x-postgres-scaling-at-figma.md",
    "how-discord-stores-trillions-of-messages.md",
    "a-crash-course-in-database-sharding.md",
    "top-4-data-sharding-algorithms-explained.md",
    "consistent-hashing.md",
    
    # Nhóm 2: Payment & Financial Systems
    "10-principles-for-building-resilient-payment-systems-by-shopify.md",
    "how-to-avoid-double-payment.md",
    "payment-system.md",
    "reconciliation-in-payment.md",
    
    # Nhóm 3: Caching & Distributed Concurrency
    "how-can-cache-systems-go-wrong.md",
    "things-to-consider-when-using-cache.md",
    "top-8-cache-eviction-strategies.md",
    "why-do-we-need-to-use-a-distributed-lock.md",
    
    # Nhóm 4: Message Queue & Streaming Architecture
    "why-is-kafka-fast.md",
    "can-kafka-lose-messages.md",
    "netflixs-overall-architecture.md"
]

RAW_BASE = "https://raw.githubusercontent.com/ByteByteGoHq/system-design-101/main/data/guides/"

def download_file(url: str, dest: Path) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
        dest.write_bytes(data)
        return data

print("=== BẮT ĐẦU TẢI 16 BÀI TOÁN KIẾN TRÚC TINH HOA TỪ BYTEBYTEGO ===")

collected_guides = []

for idx, filename in enumerate(ELITE_FILES, 1):
    md_url = RAW_BASE + filename
    slug = filename.replace(".md", "")
    dest_md = PAGES_DIR / filename
    
    print(f"[{idx}/{len(ELITE_FILES)}] Tải bài viết: {filename}")
    try:
        req = urllib.request.Request(md_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw_text = resp.read().decode("utf-8", errors="ignore")
            
        # Parse image url from frontmatter or content
        img_match = re.search(r'image:\s*[\'"]?(https://[^\s\'"]+)[\'"]?', raw_text)
        if not img_match:
            img_match = re.search(r'!\[.*?\]\((https://[^\s\)]+)\)', raw_text)
            
        img_local_rel = None
        img_name = None
        if img_match:
            img_url = img_match.group(1)
            img_name = f"{slug}.png"
            dest_img = IMAGES_DIR / img_name
            try:
                print(f"    Tải ảnh infographic: {img_url}")
                download_file(img_url, dest_img)
                img_local_rel = f"assets/system-design-elite/images/{img_name}"
            except Exception as ie:
                print(f"    [WARN] Không tải được ảnh {img_url}: {ie}")
                
        # Parse title
        title_match = re.search(r'title:\s*[\'"]?(.*?)[\'"]?\n', raw_text)
        title = title_match.group(1).strip() if title_match else slug.replace("-", " ").title()
        
        # Save local md
        dest_md.write_text(raw_text, encoding="utf-8")
        
        collected_guides.append({
            "slug": slug,
            "filename": filename,
            "title": title,
            "image_name": img_name,
            "image_rel_path": img_local_rel,
            "md_path": f"assets/system-design-elite/pages/{filename}"
        })
        
    except Exception as e:
        print(f"    [ERROR] Lỗi khi tải {filename}: {e}")

# Save manifest index
manifest_file = BASE_DIR / "INDEX.md"
with open(manifest_file, "w", encoding="utf-8") as f:
    f.write("# ByteByteGo System Design — 16 Tinh Hoa Kiến Trúc Chọn Lọc\n\n")
    for g in collected_guides:
        img_text = f" - 🖼️ [Infographic]({g['image_rel_path']})" if g['image_rel_path'] else ""
        f.write(f"- [{g['title']}]({g['md_path']}){img_text}\n")

print(f"\n✅ Đã tải thành công {len(collected_guides)}/{len(ELITE_FILES)} bài viết tinh hoa và ảnh sơ đồ!")
