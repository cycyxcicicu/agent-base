@AGENTS.md

# Ghi chú riêng cho Claude Code

Mọi quy tắc nằm trong `AGENTS.md` (được nhập ở dòng đầu). Chỉ thêm ở đây những điều đặc thù của Claude Code, nếu có.

## Bộ khung agent-base, epic, bảng tổng

`AGENTS.md` gần chạm giới hạn 12.000 ký tự của Antigravity nên phần này ở đây và trong protocol:

- Card nằm ở `tasks/<thư mục epic>/T-<số>.md`; epic khai trong `tasks/EPICS.md`; tiến độ ở `tasks/BOARD.md` (sinh bằng `python scripts/task-board.py`, không sửa tay). Chi tiết: `agents/protocols/task-card.md`.
- Danh sách file khung: `agents/manifest.txt`. **Sửa file khung** thì ghi vào mục "Thay đổi dùng chung cho agent-base" của ghi chú bàn giao và đưa ngược về agent-base: `agents/protocols/agent-base-sync.md` (`python scripts/agent-base-diff.py`).
- Tri thức dùng chung (quy trình, chuẩn code/SQL, chuẩn SRS và sơ đồ, tech radar...): tra `agents/knowledge/README.md`, chỉ mở đúng file khớp việc, không đọc cả thư mục. Viết tài liệu (đặc tả, thiết kế kỹ thuật, test report, TestLink): mở mẫu trong `agents/templates/README.md`.
- Được đưa đường dẫn agent-base để cài cho dự án mới: đọc `README.md` mục "Dùng cho dự án mới", dùng `scripts/bootstrap-project.py`, không copy cả thư mục.
