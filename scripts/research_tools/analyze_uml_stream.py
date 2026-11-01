"""scripts/analyze_uml_stream.py

Kiến trúc sư (Marcus) phân tích toàn bộ 41 chủ đề và 22+ sơ đồ UML 2.5:
- Đọc từng tệp lý thuyết và bóc tách 348 hình ảnh
- Phân loại: 8 Sơ đồ Cốt lõi (Core 8) vs Sơ đồ Mở rộng/Hàn lâm
- Lập sổ bộ định danh ảnh toàn hệ thống: agents/knowledge/IMAGE_REGISTRY.json
- Xuất báo cáo D:/test-repo/benchmarks/uml-deep-analysis.md
"""

import json
from pathlib import Path
import re
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

UML_DIR = Path("D:/test-repo/uml")
OUT_FILE = Path("D:/test-repo/benchmarks/uml-deep-analysis.md")
REGISTRY_FILE = Path("agents/knowledge/IMAGE_REGISTRY.json")

CORE_8_DIAGRAMS = {
    "class-diagram": "Class Diagram (Cấu trúc lớp, Entity, DTO, Quan hệ)",
    "sequence-diagram": "Sequence Diagram (Luồng tuần tự, Đồng bộ/Bất đồng bộ, Alt, Loop)",
    "activity-diagram": "Activity Diagram (Quy trình nghiệp vụ, Bơi làn, Fork, Join)",
    "state-machine-diagram": "State Machine Diagram (Vòng đời đối tượng, Guard, Event)",
    "component-diagram": "Component Diagram (Ranh giới module, Cổng Ports & Connectors)",
    "deployment-diagram": "Deployment Diagram (Môi trường máy chủ, Docker container)",
    "use-case-diagram": "Use Case Diagram (Tác nhân Actor, Hệ thống, Include, Extend)",
    "package-diagram": "Package Diagram (Cấu trúc phân gói, Phụ thuộc module)"
}

def analyze_uml():
    subdirs = sorted([d for d in UML_DIR.iterdir() if d.is_dir()])
    print(f"Bắt đầu phân tích {len(subdirs)} thư mục chuyên đề UML...")

    image_registry = []
    diagram_analysis = []

    for d in subdirs:
        md_files = list(d.glob("*.md"))
        imgs = list((d / "images").glob("*.*")) if (d / "images").exists() else []

        is_core = d.name in CORE_8_DIAGRAMS
        role_type = "Core (Cốt lõi làm dự án)" if is_core else "Extended/Academic (Mở rộng/Hàn lâm)"

        # Phân tích từng file md
        sections = []
        for mf in md_files:
            text = mf.read_text(encoding="utf-8", errors="ignore")
            # Tìm các heading
            headings = re.findall(r'^#{1,3}\s+(.*?)$', text, re.M)
            # Tìm ảnh
            img_matches = re.findall(r'!\[(.*?)\]\(images[/\\]([^)\s]+)\)', text)
            for caption, iname in img_matches:
                img_path = f"uml/{d.name}/images/{iname}"
                image_registry.append({
                    "id": f"IMG-{len(image_registry)+1:04d}",
                    "diagram_type": d.name,
                    "file_source": f"uml/{d.name}/{mf.name}",
                    "image_name": iname,
                    "rel_path": img_path,
                    "caption": caption.strip() or iname,
                    "is_core": is_core,
                    "target_role": "architect" if d.name in ["class-diagram", "component-diagram", "deployment-diagram"] else ("ba" if d.name in ["use-case-diagram", "activity-diagram"] else "all")
                })

            sections.append({
                "file": mf.name,
                "headings_count": len(headings),
                "headings": headings[:5]
            })

        diagram_analysis.append({
            "diagram": d.name,
            "title": CORE_8_DIAGRAMS.get(d.name, d.name.replace("-", " ").title()),
            "is_core": is_core,
            "md_count": len(md_files),
            "img_count": len(imgs),
            "sections": sections
        })

    # Lưu IMAGE_REGISTRY.json
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps(image_registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Đã tạo Sổ Bộ Ảnh: {REGISTRY_FILE} ({len(image_registry)} ảnh được lập chỉ mục)")

    # Viết báo cáo phân tích UML
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report = []
    report.append("# BÁO CÁO PHÂN TÍCH CHUYÊN SÂU 22+ LOẠI SƠ ĐỒ UML 2.5 & DANH BẠ ẢNH (ARCHITECT STREAM)\n")
    report.append(f"> Chuyên viên thực hiện: **Marcus (Principal Architect)** | Thời gian: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    report.append("## 1. TỔNG QUAN TẬP SƠ ĐỒ ĐÃ BÓC TÁCH\n")
    report.append(f"- **Tổng số phân loại sơ đồ**: {len(subdirs)} loại\n")
    report.append(f"- **Nhóm Sơ Đồ Cốt Lõi (Core 8)**: 8 loại (Áp dụng bắt buộc trong tài liệu Gate 2)\n")
    report.append(f"- **Nhóm Sơ Đồ Mở Rộng / Chuyên sâu**: {len(subdirs)-8} loại (Dùng khi cần thiết kế phức tạp)\n")
    report.append(f"- **Tổng số hình ảnh sơ đồ đã lập chỉ mục**: {len(image_registry)} ảnh\n\n")

    report.append("## 2. MA TRẬN 8 SƠ ĐỒ CỐT LÕI (CORE 8) DÀNH CHO DỰ ÁN THỰC CHIẾN\n\n")
    report.append("| STT | Sơ Đồ | Vai Trò Chính | Số Ảnh Minh Họa | Ứng Dụng Trong Hồ Sơ Gate 2 |\n")
    report.append("|---|---|---|---|---|\n")
    for idx, d in enumerate(sorted([x for x in diagram_analysis if x['is_core']], key=lambda x: -x['img_count']), 1):
        report.append(f"| {idx} | **{d['title']}** | `architect` / `ba` | {d['img_count']} ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |\n")

    report.append("\n## 3. DANH SÁCH SƠ ĐỒ MỞ RỘNG (CHỌN LỌC KHI CẦN)\n\n")
    report.append("| Sơ Đồ Mở Rộng | Số Ảnh | Đánh Giá Áp Dụng |\n")
    report.append("|---|---|---|\n")
    for d in sorted([x for x in diagram_analysis if not x['is_core']], key=lambda x: -x['img_count']):
        report.append(f"| **{d['title']}** | {d['img_count']} ảnh | {'Tham khảo' if d['img_count'] > 0 else 'Hàn lâm ít dùng'} |\n")

    report.append("\n## 4. QUY TẮC CHUYỂN ĐỔI ẢNH THÀNH DRAWIO CHUẨN DỰ ÁN\n")
    report.append("Khi Agent cần vẽ sơ đồ cho một Use Case:\n")
    report.append("1. **Tra cứu Sổ bộ ảnh** `IMAGE_REGISTRY.json` để lấy mẫu chuẩn của phần tử (VD: cách vẽ Alt fragment, cách vẽ Port, Fork/Join).\n")
    report.append("2. **Tuân thủ 5 quy tắc chuẩn (.ai-rules/srs/chuan-ve-so-do.md)**:\n")
    report.append("   - Bơi làn (swimlane) rõ ràng giữa các tầng kiến trúc.\n")
    report.append("   - Đúng 1 điểm bắt đầu và ĐÚNG 1 điểm kết thúc duy nhất.\n")
    report.append("   - Nhánh lỗi luôn tô màu đỏ `#dc2626` có chú thích mã lỗi.\n")
    report.append("   - 100% dữ liệu thật từ code/DB.\n")
    report.append("   - Xuất file `.drawio` nhiều tab kèm file ảnh `.png` độ nét cao lưu tại `doc/features/<UC>/hinh/`.\n")

    OUT_FILE.write_text("".join(report), encoding="utf-8")
    print(f"Hoàn tất phân tích UML! Đã lưu: {OUT_FILE}")

if __name__ == "__main__":
    analyze_uml()

