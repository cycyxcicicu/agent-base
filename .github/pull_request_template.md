## Tiêu đề

Đặt tiêu đề Merge Request theo dạng `<type>(scope): <tóm tắt ngắn>` (loại: feat fix chore refactor docs test ci build perf).

## Ticket

- Link ticket: (điền)
- Task card: `tasks/T-<ticket>.md`
- Yêu cầu liên quan: R-xxx

## Tóm tắt thay đổi

(1–3 câu: làm gì, để đạt gì. Liệt kê chỗ rủi ro hoặc điều đã đổi ngoài dự kiến)

## Bằng chứng kiểm thử

- Link test case hoặc kết quả chạy: (điền, ví dụ đầu ra `npm test`)
- Ảnh chụp màn hình nếu có giao diện: (điền)

## Kiểm tra trước khi xin duyệt

- [ ] Tên nhánh đúng dạng `<type>/<ticket>-<mô-tả-ngắn>`
- [ ] Mỗi commit một thay đổi logic, đúng `<type>(scope): <tóm tắt>`
- [ ] Nhánh đã **rebase** lên nhánh gốc mới nhất (không dùng merge vào nhánh cá nhân)
- [ ] `scripts/merge-gate.ps1` PASS
- [ ] CI qua
- [ ] Không có khóa bí mật, `.env`, file lớn hoặc file sinh ra không thuộc quy ước
- [ ] Ghi chú cho agent sau nằm trong `docs/notes/inbox/`
- [ ] Nếu đụng cơ sở dữ liệu, dữ liệu thật hoặc deploy: task card có kịch bản hoàn tác
- [ ] Có ít nhất 2 người duyệt (theo chính sách trong `agents/protocols/git-rules.md`)
