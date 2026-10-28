@AGENTS.md

# Ghi chú riêng cho Claude Code

Mọi quy tắc nằm trong `AGENTS.md` (được nhập ở dòng đầu). Chỉ thêm ở đây những điều đặc thù của Claude Code, nếu có.

## Bộ khung agent-base, epic, bảng tổng

`AGENTS.md` gần chạm giới hạn 12.000 ký tự của Antigravity nên phần này ở đây và trong protocol:

- Card nằm ở `tasks/<thư mục epic>/T-<số>.md`; epic khai trong `tasks/EPICS.md`; tiến độ ở `tasks/BOARD.md` (sinh bằng `python scripts/task-board.py`, không sửa tay). Chi tiết: `agents/protocols/task-card.md`.
- Danh sách file khung: `agents/manifest.txt`. **Sửa file khung** thì ghi vào mục "Thay đổi dùng chung cho agent-base" của ghi chú bàn giao và đưa ngược về agent-base: `agents/protocols/agent-base-sync.md` (`python scripts/agent-base-diff.py`).
- Tri thức dùng chung (quy trình, chuẩn code/SQL, chuẩn SRS và sơ đồ, tech radar...): tra `agents/knowledge/README.md`, chỉ mở đúng file khớp việc, không đọc cả thư mục. Không nạp sẵn: tự tra theo từ khóa bằng `scripts/knowledge.py query -q "<từ khóa>"` (xem `AGENTS.md` mục 1). `context --role <vai>` chỉ để xem trọn bộ của một vai (người dùng hoặc CI), không dùng đầu phiên; sau khi sửa file đã đăng ký trong catalog thì chạy lại `python scripts/build-knowledge-catalog.py` để cập nhật mã băm; duyệt nút sang `approved` do người dùng ghi ở `agents/knowledge/approvals.json` (trong dự án đã cài). Riêng agent-base giữ manifest mẫu toàn `draft`; dấu duyệt của chính agent-base nằm ở `.local/knowledge-approvals.json` (không commit), nạp bằng `--manifest .local/knowledge-manifest.json`. Viết tài liệu (đặc tả, thiết kế kỹ thuật, test report, TestLink): mở mẫu trong `agents/templates/README.md`.
- Được đưa đường dẫn agent-base để cài cho dự án mới: đọc `README.md` mục "Dùng cho dự án mới", dùng `scripts/bootstrap-project.py`, không copy cả thư mục.
