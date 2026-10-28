> summary: Hoàn thành T-22 thống nhất cơ chế khám phá task card đệ quy cho frontier, Board, audit và next.
# Handoff Note: T-22 — Thống nhất cách tìm card (Card lồng thư mục epic)

- **Task**: T-22
- **Agent**: dev
- **Ngày**: 2026-10-28

## 1. Việc đã làm
- Tạo module trung tâm `agent_core/workflow/task_discovery.py` với các hàm:
  - `discover_tasks`: Quét đệ quy `tasks/` tìm các file `T-*.md`, phát hiện lỗi trùng ID ở nhiều file (`ValueError`), kiểm tra symlink escape (`ValueError`), chuẩn hóa trạng thái YAML.
  - `parse_task_frontmatter`: Trích xuất frontmatter YAML (hỗ trợ cả inline và multiline list), chuẩn hóa status lowercase (`todo`, `doing`, `review`, `done`, `blocked`).
  - `discover_task_tickets`: Chuyển đổi sang `Ticket` object của tracer-bullet.
- Mở rộng `agent_core/workflow/tracer_bullet.py` để regex `TicketParser` hỗ trợ cả mã ticket dạng số thực/chấm (`T-11.2`) cho cả tiêu đề H1 và trường `blocked_by`.
- Cập nhật lệnh `frontier` trong `agent_core/cli.py` sử dụng `discover_task_tickets`.
- Đồng bộ `scripts/task-board.py`, `scripts/card-audit.py`, `scripts/next.py` sử dụng chung `discover_tasks`.
- Bổ sung 4 bộ test mới:
  - `tests/test_frontier_discovery.py`
  - `tests/test_task_discovery.py`
  - `tests/test_task_board_discovery.py`
  - `tests/test_audit_discovery.py`

## 2. Ghi chú cho agent sau
- Tất cả các script nội bộ giờ đây nhìn thấy đúng và đủ tập card, không còn tình trạng glob tầng gốc làm lệch dữ liệu frontier so với Board.
- T-23 (`claim_task`) và T-24 (`RTM`) có thể gọi thẳng `discover_tasks(ROOT / 'tasks')`.

Skill đã chọn & áp dụng: sparc-methodology
Checklist đã tuân thủ:
- Thống nhất một interface duy nhất cho discovery.
- TDD đầy đủ từng bước, 100% test xanh.
