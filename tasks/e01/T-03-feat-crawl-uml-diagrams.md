---
id: T-03
size: large
status: done
owner: analyst
epic: E01
phase: GĐ1
outputs:
  - D:/test-repo/uml/
branch: feature/03-crawl-uml-diagrams
requirements: [REQ-KG-02]
scope_edit:
  - D:/test-repo/uml/**
scope_deny:
  - AGENTS.md
---

# T-03: Khai Thác Toàn Diện `uml-diagrams.org` (Tài Liệu + 100% Ảnh Mẫu + Template Drawio/JSON)

## Mục tiêu
Dùng engine crawler đã tạo ở T-02 cào toàn bộ các loại sơ đồ trên trang `https://www.uml-diagrams.org/`, tải 100% ảnh sơ đồ minh họa gốc, bóc tách cấu trúc lý thuyết và chuyển hóa thành các mẫu sơ đồ (`.drawio` / `.json` / `.md`) để Agent học tập và vẽ chuẩn xác cho các dự án sau này.

## Tài liệu tham chiếu & Sơ đồ
- **Nguồn gốc**: `https://www.uml-diagrams.org/`
- **Các loại sơ đồ mục tiêu**:
  1. *Structure Diagrams*: Class diagram, Component diagram, Deployment diagram, Object diagram, Package diagram, Composite structure, Profile diagram.
  2. *Behavior Diagrams*: Use Case diagram, Activity diagram, State Machine diagram.
  3. *Interaction Diagrams*: Sequence diagram, Communication diagram, Interaction overview, Timing diagram.

## Contract & Happy Path
- **Đầu ra tại `D:\test-repo\uml\`**:
  - Mỗi loại sơ đồ nằm trong 1 thư mục riêng: `D:\test-repo\uml\<tên-sơ-đồ>/`:
    + `spec.md`: Mô tả chi tiết cú pháp, các ký hiệu chuẩn, quy tắc bơi làn, điểm bắt đầu/kết thúc.
    + `images/`: Chứa toàn bộ ảnh mẫu gốc `.png`, `.svg` tải về từ trang web.
    + `template.drawio`: File sơ đồ mẫu chuẩn XML/Draw.io để Agent có thể copy mẫu và chỉnh sửa.
    + `template.json`: Bản đặc tả JSON IR (để dùng với `run-archify.mjs` sinh sơ đồ tự động).

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch
- [x] **T-03.1** [Bóc tách danh mục]: Quét trang sitemap/chỉ mục của `uml-diagrams.org`, trích xuất danh sách tất cả các URL thành phần vào file `D:\test-repo\uml\urls.txt` · Assigned: `analyst`.
- [x] **T-03.2** [Cào dữ liệu & Tải ảnh]: Chạy crawler tải toàn bộ bài viết và 100% ảnh sơ đồ minh họa về `D:\test-repo\uml/` · Assigned: `dev` · Tiêu chí xong: Không bị thiếu ảnh, tất cả đường dẫn ảnh trong Markdown đều hiển thị tốt offline.
- [x] **T-03.3** [Đóng gói Template Mẫu]: Tạo file mẫu `template.drawio` và `template.json` cho từng loại sơ đồ chính (Class, Sequence, Activity, State, Component, Deployment) tuân thủ 5 quy tắc chuẩn vẽ sơ đồ · Assigned: `designer`.
- [x] **T-03.4** [Kiểm thử sơ đồ]: Dùng `scripts/diagram-describe.py --check` kiểm tra các file mẫu `.drawio` vừa tạo đạt chuẩn 100% không lỗi · Assigned: `qa`.

## Tiêu chí xong
- [x] Tải về đầy đủ 14+ loại sơ đồ UML kèm 100% ảnh minh họa cục bộ.
- [x] Mỗi sơ đồ có file đặc tả Markdown + Mã template mẫu Drawio/JSON sẵn sàng cho Agent tái sử dụng.
