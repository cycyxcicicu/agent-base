> summary: Lead lập epic E2 và 18 card T-12..T-29 từ báo cáo phân tích; chưa duyệt, chưa thực thi, không ai tự đóng dấu duyệt.

Task: E2 (T-12..T-29)        Agent: lead (Claude)        Ngày: 2026-10-28

## Đã làm
- Thêm epic E2 vào `tasks/EPICS.md` (người dùng cần xác nhận theo quy tắc "Lead đổi epic phải báo").
- Tạo 18 card trong `tasks/E2-tri-thuc-quy-trinh/`. `python scripts/task-board.py`: 29 card, 0 lỗi. Kiểm tra bằng script tạm: không có hai card chạy song song nào trùng `scope_edit`.

## Lưu ý cho agent sau
- Mọi cổng "Người dùng duyệt" đang **để trống có chủ đích**. Không agent nào được đóng dấu thay; card chỉ `doing` khi người dùng ghi dấu bằng file (xem T-13).
- Thứ tự: T-12 → (T-13, T-14, T-17, T-18 song song) → T-15 → T-16, T-19 → code T-20, T-22 (song song) → T-21, T-23, T-24 → T-25 → T-26, T-27 → T-28 → T-29.
- `.deploy.json` chưa có: `scripts/task-branch.py` không tạo được nhánh; việc của người dùng, ghi ở T-12.
- Code T-20..T-28 chỉ bắt đầu sau khi người dùng duyệt R-xxx (T-18) và spec đã căn chỉnh (T-19).
- T-25/T-26 dùng chung `scripts/verify.py`; T-28 là chủ duy nhất của `manifest.txt`, `check.yml`, `bootstrap-project.py`, `agent-base-diff.py`.
- `AGENTS.md` và `agents/roles/**` do người dùng sửa; T-16 chỉ soạn đề xuất.
- Giả định chưa kiểm chứng: RK-2 đã xử lý `tasks/*.py` (T-12.2 phải đối chiếu `docs/risk/RK-2.md`); Kilo/Antigravity có hỗ trợ hook/MCP để ép `claim_task` hay không.
- Bản sửa lỗi `{}` trong `scripts/skill-eval.py` (kèm 3 test) đã làm trước, chưa commit; nằm trong scope T-27 chỉ để giữ xanh.

## Việc dở dang hoặc nợ kỹ thuật
Q8–Q11 trong `docs/analysis/ai-sdlc-graph-lauren-gdt-2026-10-28.md` chưa được người dùng trả lời; card dùng mặc định đề xuất (RTM sinh từ card, bản cố vấn, hai cấp task/subtask).

## Ảnh hưởng đến task khác
T-08 thu hẹp phạm vi (T-12.2); T-11 thêm `blocked_by` T-12, T-18 (T-19.2).

## Đề xuất cập nhật quy ước hoặc tài liệu
Xem T-13..T-17.

## Thay đổi dùng chung cho agent-base
`tasks/EPICS.md` (thêm E2). Không sửa file khung khác.

Skill đã chọn & áp dụng: codebase-design — một chủ cho mỗi file dùng chung, giao diện giữ ổn định, tách module nhỏ.
Checklist đã tuân thủ: đọc task-card/handoff-note trước khi viết; không sửa AGENTS.md/roles; không tự duyệt; test trước code ở mọi card code.
