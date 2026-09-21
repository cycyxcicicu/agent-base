# Định nghĩa hoàn thành (theo cỡ việc)

Ghi chú: AI chỉ commit hoặc push khi người dùng yêu cầu rõ và duyệt từng lệnh. Các mục về commit, nhánh, Merge Request là việc của **người dùng** (AI chuẩn bị kế hoạch và có thể chạy giúp theo yêu cầu).

## Nhỏ
- [ ] Sửa trong nhánh riêng do người dùng tạo (`<type>/<ticket>-<mô-tả>`).
- [ ] Test và lint chạy qua (có thể nhờ `runner` chạy).
- [ ] `scripts/merge-gate.ps1` PASS (hoặc diff nằm trong phạm vi đã nêu).
- [ ] Kế hoạch commit trong `tasks/quick-log.md` hoặc card: mỗi commit một thay đổi logic, đúng `<type>(scope): <tóm tắt>`.
- [ ] Ghi chú cho agent sau trong `docs/notes/inbox/` (ngắn được, nhưng không bỏ qua).
- [ ] Người dùng đã xem diff và tự chạy các lệnh commit.

## Vừa
- [ ] Mọi mục của "Nhỏ".
- [ ] Task card đầy đủ: tiêu chí xong đạt hết, nhật ký phiên, file đã đổi, kết quả test, kế hoạch commit.
- [ ] Reviewer duyệt (theo checklist trong `agents/roles/reviewer.md`).
- [ ] QA xác nhận từng tiêu chí bằng test hoặc bước kiểm tra cụ thể.

## Lớn
- [ ] Mọi mục của "Vừa", cho từng task con.
- [ ] Yêu cầu R-xxx đều được thực hiện và đã được người dùng duyệt từ đầu.
- [ ] Nếu có tài liệu: Analyst đã đối chiếu tài liệu với code, báo cáo lệch trong `docs/analysis/` không còn mục "chặn việc".
- [ ] Nếu đổi xác thực, gói phụ thuộc hoặc dữ liệu nhạy cảm: Security duyệt.
- [ ] Nhánh đã **rebase** lên `develop`, tạo Merge Request đúng chính sách (tiêu đề, link ticket, tóm tắt, bằng chứng test, CI qua, đủ người duyệt).
- [ ] Sau khi merge: mã merge commit ghi vào card để hoàn tác được.
- [ ] Tech Writer cập nhật CHANGELOG và tài liệu, **gộp ghi chú từ `docs/notes/inbox/` vào `docs/PROJECT-NOTES.md`**.
- [ ] Release: tag `v<MAJOR>.<MINOR>.<PATCH>` trên `main` do người dùng đánh.

## Luôn luôn
- [ ] Đã xác định rõ Đầu vào (Input), Đầu ra (Output) và kịch bản Happy Path trước khi lập trình.
- [ ] Có Unit Test cho Happy Path được viết bằng công nghệ của dự án và chạy PASS (100% xanh).
- [ ] Không có khóa bí mật trong code, log, card, ghi chú.
- [ ] Việc đụng DB, dữ liệu thật hoặc deploy có "Kịch bản hoàn tác".
- [ ] Người làm sau đọc `docs/PROJECT-NOTES.md` trước khi bắt đầu.
