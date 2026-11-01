"""scripts/reorganize_m2mba_posts.py

Tổ chức lại toàn bộ các bài viết m2mba thành từng thư mục riêng biệt:
D:/test-repo/m2mba/posts/<post-slug>/
  ├── README.md (Nội dung bài viết)
  └── images/ (Chỉ chứa các ảnh thuộc riêng bài viết này)
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_POSTS = Path("D:/test-repo/m2mba/posts")
OLD_IMAGES_DIR = ROOT_POSTS / "images"
FULL_INDEX_PATH = Path("D:/test-repo/m2mba/FULL_INDEX.md")


def reorganize():
    if not ROOT_POSTS.exists():
        print("Thư mục posts không tồn tại!")
        return

    # Lấy danh sách các file markdown hiện tại ở thư mục gốc của posts
    md_files = [f for f in ROOT_POSTS.iterdir() if f.is_file() and f.suffix == ".md"]
    print(f"Bắt đầu chia tách {len(md_files)} bài viết thành từng thư mục riêng biệt...")

    index_entries = []
    
    for f in md_files:
        post_slug = f.stem
        post_dir = ROOT_POSTS / post_slug
        post_dir.mkdir(parents=True, exist_ok=True)
        post_images_dir = post_dir / "images"

        content = f.read_text(encoding="utf-8")
        
        # Trích xuất tiêu đề bài viết
        title_match = re.search(r'title:\s*["\'](.*?)["\']', content)
        if not title_match:
            title_match = re.search(r'^#\s*(.*?)$', content, re.M)
        title = title_match.group(1) if title_match else post_slug

        # Tìm toàn bộ ảnh được bài viết này tham chiếu
        # Cả dạng ![...](images/xyz.png) lẫn ![...](images\xyz.png)
        img_refs = re.findall(r'!\[.*?\]\(images[/\\]([^)\s]+)\)', content)
        
        # Nếu có ảnh, copy vào thư mục images/ của riêng bài viết
        copied_images = 0
        if img_refs:
            post_images_dir.mkdir(parents=True, exist_ok=True)
            for img_name in set(img_refs):
                src_img = OLD_IMAGES_DIR / img_name
                dest_img = post_images_dir / img_name
                if src_img.exists():
                    shutil.copy2(src_img, dest_img)
                    copied_images += 1
        
        # Chuẩn hóa đường dẫn ảnh trong markdown về dạng images/<tên_ảnh>
        new_content = re.sub(r'!\[(.*?)\]\(images[/\\]([^)\s]+)\)', r'![\1](images/\2)', content)

        # Lưu thành README.md trong thư mục riêng của bài viết
        dest_md = post_dir / "README.md"
        dest_md.write_text(new_content, encoding="utf-8")

        # Xóa file .md cũ ở root posts
        f.unlink()

        index_entries.append({
            "slug": post_slug,
            "title": title,
            "path": f"posts/{post_slug}/README.md",
            "img_count": copied_images
        })

    # Xóa thư mục images chung cũ sau khi đã phân bổ hết vào từng bài
    if OLD_IMAGES_DIR.exists():
        shutil.rmtree(OLD_IMAGES_DIR, ignore_errors=True)
        print("Đã dọn dẹp thư mục images tập trung cũ.")

    # Cập nhật FULL_INDEX.md
    index_lines = [
        f"# Mục Lục Toàn Bộ {len(index_entries)} Bài Viết Chuyên Môn M2MBA Blog (Đã Tách Thư Mục)\n\n",
        f"> Mỗi bài viết là một thư mục độc lập kèm ảnh cục bộ | Cập nhật: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "| STT | Mã / Slug | Tiêu Đề Bài Viết | Số Ảnh | Đường Dẫn Bài Viết |\n",
        "|---|---|---|---|---|\n",
    ]

    for idx, item in enumerate(sorted(index_entries, key=lambda x: x["title"]), 1):
        index_lines.append(
            f"| {idx} | `{item['slug']}` | **{item['title']}** | {item['img_count']} | [{item['path']}]({item['path']}) |\n"
        )

    FULL_INDEX_PATH.write_text("".join(index_lines), encoding="utf-8")
    print(f"Hoàn tất! Đã chia tách {len(index_entries)} bài viết thành {len(index_entries)} thư mục riêng biệt.")
    print(f"Cập nhật xong {FULL_INDEX_PATH}")


if __name__ == "__main__":
    reorganize()

