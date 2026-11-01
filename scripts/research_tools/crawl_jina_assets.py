"""scripts/crawl_jina_assets.py

Engine cào dữ liệu qua r.jina.ai, bóc tách và tải toàn bộ ảnh minh họa về máy cục bộ.
Hỗ trợ cào đơn lẻ hoặc cào hàng loạt theo danh sách link/sitemap.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import os
from pathlib import Path
import re
import sys
import time
from typing import List, Optional, Set, Tuple
import urllib.parse
import urllib.request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
JINA_PREFIX = "https://r.jina.ai/"


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Loại bỏ ký tự không hợp lệ trên Windows và giới hạn độ dài."""
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    name = re.sub(r"\s+", "_", name).strip("._")
    if len(name) > max_len:
        base, ext = os.path.splitext(name)
        h = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
        return f"{base[:max_len-10]}_{h}{ext}"
    return name or "unnamed"


def fetch_url(url: str, timeout: int = 40, headers: Optional[dict] = None) -> bytes:
    """Tải dữ liệu từ URL. Dùng curl.exe trực tiếp để đảm bảo chống chặn Cloudflare."""
    import shutil
    import subprocess

    req_headers: dict[str, str] = {}
    if not url.startswith(JINA_PREFIX):
        req_headers["User-Agent"] = USER_AGENT
    if headers:
        req_headers.update(headers)

    # Ưu tiên curl.exe nếu có sẵn
    if shutil.which("curl.exe"):
        cmd = ["curl.exe", "-sL", "--max-time", str(timeout)]
        for k, v in req_headers.items():
            cmd.extend(["-H", f"{k}: {v}"])
        cmd.append(url)
        proc = subprocess.run(cmd, capture_output=True)
        if proc.returncode == 0 and len(proc.stdout) > 0:
            # Nếu Jina trả về 403 HTML thì thử lại không header
            if b"<title>403</title>" in proc.stdout[:200]:
                retry = subprocess.run(["curl.exe", "-sL", "--max-time", str(timeout), url], capture_output=True)
                if retry.returncode == 0 and len(retry.stdout) > 0 and b"<title>403</title>" not in retry.stdout[:200]:
                    return retry.stdout
            else:
                return proc.stdout

    # Fallback urllib
    req = urllib.request.Request(url, headers=req_headers or {"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def fetch_jina_markdown(target_url: str, timeout: int = 45) -> str:
    """Tải nội dung Markdown từ trang đích qua r.jina.ai."""
    clean_target = target_url.strip()
    jina_url = f"{JINA_PREFIX}{clean_target}"
    headers = {
        "X-Return-Format": "markdown",
    }
    content = fetch_url(jina_url, timeout=timeout, headers=headers)
    return content.decode("utf-8", errors="replace")


def extract_image_urls(markdown_text: str, base_url: str) -> List[Tuple[str, str, str]]:
    """
    Trích xuất toàn bộ URL ảnh từ Markdown và HTML tags.
    Trả về danh sách (full_match, alt_text, image_url).
    """
    results: List[Tuple[str, str, str]] = []
    seen: Set[str] = set()

    # Match ![alt](url "title")
    md_img_pat = re.compile(r'!\[(.*?)\]\(\s*([^\s\)\'\"]+)(?:\s+[\'\"](.*?)[\'\"])?\s*\)')
    for match in md_img_pat.finditer(markdown_text):
        full_match = match.group(0)
        alt = match.group(1)
        raw_url = match.group(2).strip()
        if raw_url and raw_url not in seen:
            seen.add(raw_url)
            abs_url = urllib.parse.urljoin(base_url, raw_url)
            results.append((full_match, alt, abs_url))

    # Match <img src="url" alt="alt">
    html_img_pat = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.I)
    for match in html_img_pat.finditer(markdown_text):
        full_match = match.group(0)
        raw_url = match.group(1).strip()
        if raw_url and raw_url not in seen:
            seen.add(raw_url)
            abs_url = urllib.parse.urljoin(base_url, raw_url)
            results.append((full_match, "", abs_url))

    return results


def download_single_image(img_url: str, dest_path: Path, timeout: int = 25) -> bool:
    """Tải 1 ảnh về đường dẫn đích nếu chưa tồn tại hoặc bị rỗng."""
    if dest_path.exists() and dest_path.stat().st_size > 0:
        return True
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        img_bytes = fetch_url(img_url, timeout=timeout)
        if len(img_bytes) > 0:
            dest_path.write_bytes(img_bytes)
            return True
    except Exception as e:
        print(f"  [WARN] Không thể tải ảnh {img_url}: {e}", file=sys.stderr)
    return False


def crawl_page(
    target_url: str,
    out_dir: Path,
    doc_slug: Optional[str] = None,
    download_images: bool = True,
    max_workers: int = 5,
    timeout: int = 40,
) -> Path:
    """
    Cào một trang web qua Jina, tải ảnh về thư mục images/ và lưu file .md.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir = out_dir / "images"

    if not doc_slug:
        parsed = urllib.parse.urlparse(target_url)
        path_part = parsed.path.strip("/").replace("/", "_")
        doc_slug = path_part or "index"
        if doc_slug.endswith(".html") or doc_slug.endswith(".htm"):
            doc_slug = os.path.splitext(doc_slug)[0]
    doc_slug = sanitize_filename(doc_slug)
    out_file = out_dir / f"{doc_slug}.md"

    print(f"[CRAWL] Đang tải qua Jina: {target_url} -> {out_file.name}")
    md_content = fetch_jina_markdown(target_url, timeout=timeout)

    if download_images:
        images_dir.mkdir(parents=True, exist_ok=True)
        img_list = extract_image_urls(md_content, target_url)
        print(f"  -> Tìm thấy {len(img_list)} hình ảnh liên kết.")

        url_to_relpath: dict[str, str] = {}
        tasks = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for full_match, alt, img_url in img_list:
                # Lấy tên file ảnh
                parsed_img = urllib.parse.urlparse(img_url)
                img_name = os.path.basename(parsed_img.path)
                if not img_name or "." not in img_name:
                    h = hashlib.md5(img_url.encode("utf-8")).hexdigest()[:8]
                    img_name = f"image_{h}.png"
                img_name = sanitize_filename(img_name)
                dest_file = images_dir / img_name

                # Tránh trùng tên từ các URL khác nhau
                counter = 1
                while dest_file.exists() and url_to_relpath.get(img_url) != f"images/{dest_file.name}":
                    if hashlib.md5(img_url.encode("utf-8")).hexdigest()[:6] in dest_file.name:
                        break
                    base, ext = os.path.splitext(img_name)
                    dest_file = images_dir / f"{base}_{counter}{ext}"
                    counter += 1

                rel_path = f"images/{dest_file.name}"
                url_to_relpath[img_url] = rel_path
                tasks.append(executor.submit(download_single_image, img_url, dest_file, timeout))

            # Chờ tải xong ảnh
            for future in as_completed(tasks):
                future.result()

        # Viết lại đường dẫn ảnh trong Markdown
        for full_match, alt, img_url in img_list:
            rel = url_to_relpath.get(img_url)
            if rel:
                # Thay thế liên kết ảnh Markdown
                if full_match.startswith("!"):
                    replacement = f"![{alt}]({rel})"
                    md_content = md_content.replace(full_match, replacement)
                elif "<img" in full_match:
                    replacement = f'<img src="{rel}" alt="{alt}"/>'
                    md_content = md_content.replace(full_match, replacement)

    # Thêm header truy vết
    header = (
        f"---\n"
        f"source_url: \"{target_url}\"\n"
        f"crawled_at: \"{time.strftime('%Y-%m-%d %H:%M:%S')}\"\n"
        f"title: \"{doc_slug}\"\n"
        f"---\n\n"
    )
    final_text = header + md_content
    out_file.write_text(final_text, encoding="utf-8")
    print(f"  [OK] Đã lưu {out_file} ({len(final_text)} ký tự)")
    return out_file


def extract_internal_links(markdown_text: str, base_domain: str, base_url: str) -> List[str]:
    """Trích xuất tất cả các liên kết thuộc cùng base_domain."""
    link_pat = re.compile(r'\[.*?\]\(\s*([^\s\)\'\"]+)')
    found_urls = []
    seen = set()

    for match in link_pat.finditer(markdown_text):
        href = match.group(1).strip()
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("javascript:"):
            continue
        abs_url = urllib.parse.urljoin(base_url, href)
        parsed = urllib.parse.urlparse(abs_url)
        clean_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
        if base_domain in parsed.netloc and clean_url not in seen:
            seen.add(clean_url)
            found_urls.append(clean_url)
    return found_urls


def main():
    parser = argparse.ArgumentParser(description="Jina AI Crawler với tính năng tải ảnh & viết lại link.")
    parser.add_argument("--url", required=True, help="URL trang web cần cào")
    parser.add_argument("--out-dir", required=True, help="Thư mục xuất kết quả")
    parser.add_argument("--slug", help="Tên file tài liệu (không gồm .md)")
    parser.add_argument("--images", action="store_true", default=True, help="Tải toàn bộ hình ảnh liên kết")
    parser.add_argument("--no-images", action="store_false", dest="images", help="Không tải hình ảnh")
    parser.add_argument("--max-workers", type=int, default=5, help="Số luồng tải ảnh song song")
    parser.add_argument("--timeout", type=int, default=40, help="Timeout kết nối mạng (giây)")

    args = parser.parse_args()
    out_path = Path(args.out_dir).resolve()

    try:
        crawl_page(
            target_url=args.url,
            out_dir=out_path,
            doc_slug=args.slug,
            download_images=args.images,
            max_workers=args.max_workers,
            timeout=args.timeout,
        )
    except Exception as e:
        print(f"[ERROR] Cào thất bại {args.url}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
