Loại việc: review · Model gợi ý: gemini-3.8-flash-medium
Xem luật chung tại [delegation-prompt.md](file:///Users/ducnvh/Documents/agent-base/agents/protocols/delegation-prompt.md). Chạy phiên agy MỚI, model khác phiên viết. KHÔNG sửa code.

## 1. Mục tiêu và Tiêu chí xong
- Mục tiêu: <Review diff và spec của Task X nhằm phát hiện lỗi logic, an ninh và hồi quy>.
- Tiêu chí xong: Chỉ đọc diff + spec; chỉ báo lỗi thật (critical/high, bỏ nits); file kết quả <Task>-review.md; không sửa code.
- Tên giao thức, đường dẫn, cờ, mã thoát: chép nguyên văn từ `--help` hoặc mã nguồn, không diễn đạt lại; chưa chắc thì ghi chưa kiểm chứng.

## 2. Phạm vi
- File được tạo: `docs/notes/inbox/<Task>/<Task>-review.md`. Đường dẫn chính xác, cấm dùng glob.
- File cấm chạm: Tuyệt đối KHÔNG sửa bất kỳ mã nguồn `src/`, test hay file tài liệu hiện có.

## 3. Định vị
- Điểm can thiệp: Hunk diff tại hàm `<function_name>`, lớp `<ClassName>`, hoặc trường `<field_name>`. Cấm dùng số dòng.

## 4. Lệnh bằng chứng
- Lệnh xem diff (git): `git diff <base>..<branch> -- <path/to/changed_file>`
- Gọi bridge với: --allow-write docs/notes/inbox/<Task>/<Task>-review.md --allow-cmd git

## 5. Báo cáo
- Chi tiết ghi vào: `docs/notes/inbox/<Task>/<Task>-review.md` (hoặc `<Task>-agy.md`) kèm mục "CHƯA kiểm chứng".
- Chat chỉ 3 dòng: (1) Kết luận review (PASS/BLOCKED), (2) Số lỗi thật phát hiện, (3) Đường dẫn file review.
