---
id: T-05
size: large
status: done
owner: researcher
epic: E02
phase: GĐ2
outputs:
  - D:/test-repo/repos/
  - D:/test-repo/benchmarks/30-repos-analysis.md
branch: feature/05-clone-analyze-30-repos
requirements: [REQ-KG-04]
scope_edit:
  - D:/test-repo/repos/**
  - D:/test-repo/benchmarks/**
scope_deny:
  - AGENTS.md
---

# T-05: Tải Về & Giải Phẫu Đối Chuẩn 30+ Siêu Repo Kinh Điển Thế Giới

## Mục tiêu
Tải toàn bộ 30+ repository mã nguồn mở hàng đầu thế giới về `D:\test-repo\repos\` (sử dụng `git clone --depth 1` để tối ưu thời gian và dung lượng đĩa). Tiến hành đọc chuẩn chỉ, giải phẫu cấu trúc và lập Ma Trận Đối Chuẩn (Benchmark Matrix) đánh giá chi tiết: từng repo có kiến trúc hay kỹ thuật gì tinh hoa có thể áp dụng ngay vào `agent-base`.

## Contract & Happy Path
- **Đầu ra**:
  - `D:\test-repo\repos/<tên-repo>/`: 30+ thư mục mã nguồn clone sạch sẽ.
  - `D:\test-repo\benchmarks/30-repos-analysis.md`: Bảng ma trận đối chuẩn chi tiết.

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch
- [x] **T-05.1** [Tải dữ liệu hàng loạt]: Viết và thực thi kịch bản `scripts/research_tools/batch_clone_repos.py` clone toàn bộ 30+ repos với cờ `--depth 1` vào `D:\test-repo\repos/` · Assigned: `devops`.
- [x] **T-05.2** [Phân tích kiến trúc từng repo]: Bóc tách 5 nhóm chủ đề: Multi-Agent Swarm, Testing/ATDD, Software Architecture, Database/JPA, và AI Engineering · Assigned: `researcher`.
- [x] **T-05.3** [Xuất bản Ma Trận Đối Chuẩn]: Tổng hợp và lập báo cáo `D:\test-repo\benchmarks/30-repos-analysis.md` rút ra 5 bài học tối thượng cho `agent-base` · Assigned: `architect`.

## Tiêu chí xong
- [x] 100% repos trong danh sách được clone về `D:\test-repo\repos/`.
- [x] File báo cáo `30-repos-analysis.md` hoàn chỉnh, sắc bén, định hướng chính xác kiến trúc.
