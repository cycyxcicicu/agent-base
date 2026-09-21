#!/usr/bin/env python3
"""
scripts/convert-docs.py
Turnkey document & image ingestion pipeline for Business Analyst (BA) in agent-base.
Converts PDF, DOCX, XLSX, PPTX, HTML, TXT, and Images into clean Markdown.
Supports LLM Vision OCR (via 9Router or OpenAI-compatible endpoint) for reading images.

Usage:
  python scripts/convert-docs.py --file docs/source/spec.docx
  python scripts/convert-docs.py --all
  python scripts/convert-docs.py --file docs/source/mockup.png --enable-ocr
"""

import os
import sys
import argparse
import base64
import json
from pathlib import Path
from datetime import datetime

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Check optional libraries for advanced conversion and notify developer
def check_optional_dependencies():
    missing = []
    try:
        import markitdown
    except ImportError:
        missing.append("markitdown")
    try:
        import openai
    except ImportError:
        missing.append("openai")

    if missing:
        print(f"[convert-docs] Thông báo: Chưa cài đặt các thư viện tùy chọn: {', '.join(missing)}")
        print(f"[convert-docs] Để bật đầy đủ LLM Vision OCR / chuyển đổi tài liệu nâng cao, chạy lệnh:")
        print(f"               pip install {' '.join(missing)}")
        print(f"[convert-docs] Tiếp tục chạy với bộ chuyển đổi chuẩn (fallback converter)...\n")

check_optional_dependencies()

try:
    from markitdown import MarkItDown
    HAS_MARKITDOWN = True
except ImportError:
    HAS_MARKITDOWN = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


def get_llm_client(base_url=None, api_key=None):
    if not HAS_OPENAI:
        return None
    url = base_url or os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:20128/v1")
    key = api_key or os.environ.get("OPENAI_API_KEY", "9router-key")
    try:
        return OpenAI(base_url=url, api_key=key, timeout=60.0, max_retries=3)
    except Exception:
        return None


def describe_image_with_llm(image_path: Path, client: OpenAI, model: str = "gpt-4o") -> str:
    """Read an image and extract text, diagram structure, and data tables using LLM Vision."""
    mime = "image/png"
    if image_path.suffix.lower() in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    elif image_path.suffix.lower() == ".webp":
        mime = "image/webp"

    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        "Analyze this image in detail for a Business Analyst / Software Engineer. "
        "1. Transcribe all visible text, labels, and numbers accurately into Markdown.\n"
        "2. If this is a diagram, flowchart, or UI mockup: describe the layout, steps, inputs, buttons, and state transitions.\n"
        "3. If this is a table: transcribe it into a Markdown table format.\n"
        "Output clean Markdown."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{b64}"}
                        }
                    ]
                }
            ],
            max_tokens=2500
        )
        content = response.choices[0].message.content or ""
        return f"\n*[Image OCR & Visual Analysis: {image_path.name}]*\n\n{content}\n\n*[End Image Analysis]*\n"
    except Exception as e:
        return f"\n*[Image Analysis Failed for {image_path.name}: {e}]*\n"


def convert_single_file(file_path: Path, output_dir: Path, enable_ocr: bool = False, model: str = "gpt-4o", base_url: str = None) -> dict:
    file_path = file_path.resolve()
    base_name = file_path.stem
    ext = file_path.suffix.lower()
    
    out_md = output_dir / f"{base_name}.md"
    out_report = output_dir / f"{base_name}.report.md"
    
    report = {
        "source_file": str(file_path),
        "source_name": file_path.name,
        "extension": ext,
        "file_size_bytes": file_path.stat().st_size,
        "converted_at": datetime.now().isoformat(),
        "method": "unknown",
        "ocr_enabled": enable_ocr,
        "warnings": []
    }

    markdown_text = ""
    client = get_llm_client(base_url) if enable_ocr else None

    # Handle standalone image formats
    if ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"]:
        report["method"] = "llm_vision" if (client and enable_ocr) else "image_metadata"
        if client and enable_ocr:
            ocr_text = describe_image_with_llm(file_path, client, model=model)
            markdown_text = f"# Phân Tích Hình Ảnh: {file_path.name}\n\n" + ocr_text
        else:
            markdown_text = (
                f"# Hình Ảnh Gốc: {file_path.name}\n\n"
                f"- **Tệp gốc**: `docs/source/{file_path.name}`\n"
                f"- **Kích thước**: {file_path.stat().st_size} bytes\n"
                f"- **Ghi chú**: Chưa bật OCR hoặc không có kết nối Vision LLM. BA cần mở trực tiếp bản gốc để đối chiếu.\n"
            )
            report["warnings"].append("Image processed without LLM Vision OCR.")

    # Handle document formats
    elif HAS_MARKITDOWN:
        report["method"] = "markitdown"
        try:
            md_engine = MarkItDown(
                enable_plugins=enable_ocr,
                llm_client=client if enable_ocr else None,
                llm_model=model if enable_ocr else None
            )
            res = md_engine.convert(str(file_path))
            # Support both text_content and markdown attribute across markitdown versions
            markdown_text = getattr(res, "text_content", None) or getattr(res, "markdown", str(res))
        except Exception as e:
            report["warnings"].append(f"MarkItDown failed: {e}. Falling back to plain text extraction.")
            report["method"] = "fallback"
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    markdown_text = f.read()
            except Exception as read_err:
                markdown_text = f"Lỗi đọc tệp: {read_err}"
    else:
        # Fallback if markitdown is not yet installed
        report["method"] = "plain_fallback"
        report["warnings"].append("MarkItDown not installed. Run 'pip install markitdown' for high-fidelity conversion.")
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                markdown_text = f.read()
        except Exception as read_err:
            markdown_text = f"# {file_path.name}\n\nKhông thể giải mã tệp dạng nhị phân ({ext}) khi chưa cài MarkItDown.\nLỗi: {read_err}"

    # Write Markdown output
    out_md.write_text(markdown_text, encoding="utf-8")

    # Generate Conversion Report
    report_content = f"""# Báo Cáo Chuyển Đổi Tài Liệu: {file_path.name}

- **Tệp gốc**: `{file_path}`
- **Thời gian chuyển đổi**: `{report['converted_at']}`
- **Dung lượng gốc**: `{report['file_size_bytes']} bytes`
- **Phương thức xử lý**: `{report['method']}`
- **Bật LLM Vision OCR**: `{'Có' if enable_ocr else 'Không'}`
- **Tệp xuất**: [`docs/converted/{out_md.name}`](file:///{out_md.as_posix()})

## Ghi chú đối chiếu & Cảnh báo (Audit Checklist)
"""
    if report["warnings"]:
        for w in report["warnings"]:
            report_content += f"- ⚠️ **Cảnh báo**: {w}\n"
    else:
        report_content += "- ✅ Chuyển đổi thành công, không phát hiện lỗi nghiêm trọng.\n"

    report_content += """
## Các bước tiếp theo cho Business Analyst (BA):
1. Mở song song bản gốc trong `docs/source/` và bản `docs/converted/`.
2. Kiểm tra các ô gộp, công thức tính toán và số liệu bảng biểu.
3. Rút các dòng yêu cầu `R-xxx` đưa vào `docs/requirements/requirements.md`.
4. Liệt kê các điểm mơ hồ hoặc mâu thuẫn vào mục "Không chắc" để Orchestrator/Người dùng duyệt.
"""

    out_report.write_text(report_content, encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description="Convert documents and images to Markdown for Business Analyst.")
    parser.add_argument("--file", type=str, help="Specific file in docs/source/ to convert.")
    parser.add_argument("--all", action="store_true", help="Convert all files in docs/source/.")
    parser.add_argument("--enable-ocr", action="store_true", help="Enable LLM Vision OCR for images/scanned docs.")
    parser.add_argument("--model", type=str, default="gpt-4o", help="Vision LLM model (default: gpt-4o).")
    parser.add_argument("--base-url", type=str, default=None, help="OpenAI-compatible base URL (default: 9Router).")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    source_dir = root_dir / "docs" / "source"
    converted_dir = root_dir / "docs" / "converted"

    source_dir.mkdir(parents=True, exist_ok=True)
    converted_dir.mkdir(parents=True, exist_ok=True)

    targets = []
    if args.file:
        p = Path(args.file)
        if not p.is_absolute():
            p = (root_dir / p).resolve()
        if p.exists():
            targets.append(p)
        else:
            print(f"Error: File not found: {p}")
            sys.exit(1)
    elif args.all:
        for item in source_dir.iterdir():
            if item.is_file() and not item.name.startswith("."):
                targets.append(item)
        if not targets:
            print(f"No files found in {source_dir}. Place documents or images into docs/source/ first.")
            sys.exit(0)
    else:
        print("Specify --file <path> or --all. Use --help for options.")
        sys.exit(1)

    print(f"Converting {len(targets)} file(s)... (OCR={'Enabled' if args.enable_ocr else 'Disabled'})")
    for t in targets:
        print(f"-> Processing: {t.name}")
        rep = convert_single_file(t, converted_dir, enable_ocr=args.enable_ocr, model=args.model, base_url=args.base_url)
        print(f"   Done: docs/converted/{t.stem}.md [Method: {rep['method']}]")

    print("\nAll conversions completed successfully.")


if __name__ == "__main__":
    main()
