---
id: T-02
size: medium
status: done
owner: dev
epic: E01
phase: GĐ1
outputs:
  - scripts/research_tools/
  - scripts/research_tools/crawl_jina_assets.py
branch: feature/02-infra-crawler
requirements: [REQ-KG-01]
scope_edit:
  - scripts/research_tools/crawl_jina_assets.py
  - tests/test_crawler.py
scope_deny:
  - AGENTS.md
---

# T-02: Thiết Lập Trạm `D:\test-repo` & Xây Dựng Engine Crawler Jina Đa Năng (Kèm Tải Ảnh)

## Mục tiêu
Khởi tạo cấu trúc trạm trung chuyển dữ liệu tại `D:\test-repo` và xây dựng công cụ Python `scripts/research_tools/crawl_jina_assets.py` chuyên dụng: cào dữ liệu qua `r.jina.ai`, tự động phát hiện mọi liên kết ảnh trong Markdown, tải ảnh gốc lưu vào thư mục cục bộ và viết lại đường dẫn tương đối để Agent đọc offline kèm ảnh.

## Tài liệu tham chiếu & Sơ đồ
- **Yêu cầu kỹ thuật**: Đọc trang thông qua tiền tố `https://r.jina.ai/<url>`.
- **Thư mục trạm đích**: `D:\test-repo\`
  - `D:\test-repo\uml\` (Lưu tài liệu & ảnh mẫu UML)
  - `D:\test-repo\m2mba\` (Lưu blog & ảnh infographic M2MBA)
  - `D:\test-repo\repos\` (Lưu 30+ git repos cloned)
  - `D:\test-repo\benchmarks\` (Lưu ma trận phân tích đối chuẩn)

## Contract & Happy Path
- **Đầu vào (Input)**: URL trang web cần cào (ví dụ `https://www.uml-diagrams.org/` hoặc `https://m2mba.com/blog`), cờ `--download-images`, thư mục đích `--out-dir`.
- **Đầu ra (Output)**: File `.md` sạch sẽ + Thư mục con `images/` chứa 100% ảnh nhúng được tải về máy thành công; đường dẫn trong file `.md` được trỏ về `images/<tên-ảnh>`.
- **Kịch bản Happy Path**:
  Chạy lệnh: `python scripts/research_tools/crawl_jina_assets.py --url "https://m2mba.com/blog" --out-dir "D:/test-repo/m2mba" --images`
  ➔ Tạo file `index.md` và tải toàn bộ ảnh minh họa về `D:/test-repo/m2mba/images/`, exit code 0.

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch
- [x] **T-02.1** [Hạ tầng]: Tạo toàn bộ cây thư mục tại `D:\test-repo\` (uml, m2mba, repos, benchmarks) · Assigned: `devops` · Tiêu chí xong: `Test-Path D:\test-repo\*` đều True.
- [x] **T-02.2** [Mã nguồn]: Xây dựng `scripts/research_tools/crawl_jina_assets.py` (tích hợp urllib/requests, bóc tách ảnh `![]()`, tải ảnh song song với timeout an toàn) · Assigned: `dev` · Tiêu chí xong: Unit test cào thử 1 trang kèm tải ảnh đạt PASS.
- [x] **T-02.3** [Kiểm thử]: Viết kiểm thử `tests/test_crawler.py` kiểm tra xử lý lỗi mạng, timeout, và kiểm định đường dẫn ảnh tương đối · Assigned: `qa` · Tiêu chí xong: `pytest tests/test_crawler.py` PASS 100%.

## Tiêu chí xong
- [x] Thư mục `D:\test-repo` được cấu trúc đầy đủ.
- [x] Script `scripts/research_tools/crawl_jina_assets.py` hoạt động ổn định trên Windows, tải được cả Markdown và Ảnh đầy đủ.
- [x] Đạt chuẩn kiểm định code của framework.
