# Định nghĩa hoàn thành (theo cỡ việc)

## Nhỏ
- [ ] Nhánh riêng, một commit đúng mẫu (`Task:`, `Agent:`).
- [ ] Test và lint chạy qua.
- [ ] `scripts/merge-gate.ps1` PASS (hoặc diff nằm trong phạm vi đã nêu).
- [ ] Một dòng trong `tasks/quick-log.md`.
- [ ] Ghi chú cho agent sau trong `docs/notes/inbox/` (ngắn được, nhưng không bỏ qua).
- [ ] Người dùng đã xem diff.

## Vừa
- [ ] Mọi mục của "Nhỏ".
- [ ] Task card đầy đủ: tiêu chí xong đạt hết, nhật ký phiên, file đã đổi, kết quả test.
- [ ] Reviewer duyệt (theo checklist trong `agents/roles/reviewer.md`).
- [ ] QA xác nhận từng tiêu chí bằng test hoặc bước kiểm tra cụ thể.

## Lớn
- [ ] Mọi mục của "Vừa", cho từng task con.
- [ ] Yêu cầu R-xxx đều được thực hiện và đã được người dùng duyệt từ đầu.
- [ ] Nếu có tài liệu: Analyst đã đối chiếu tài liệu với code, báo cáo lệch trong `docs/analysis/` không còn mục "chặn việc".
- [ ] Nếu đổi xác thực, gói phụ thuộc hoặc dữ liệu nhạy cảm: Security duyệt.
- [ ] Các nhánh gộp vào nhánh tích hợp từng cái một, test chạy sau mỗi lần gộp.
- [ ] Squash merge: mỗi task một commit, gắn tag `T-xxx`.
- [ ] Tech Writer cập nhật CHANGELOG và tài liệu, **gộp ghi chú từ `docs/notes/inbox/` vào `docs/PROJECT-NOTES.md`**.
- [ ] Người dùng duyệt cuối trước khi vào `main`.

## Luôn luôn
- [ ] Không có khóa bí mật trong code, log, card, ghi chú.
- [ ] Việc đụng DB, dữ liệu thật hoặc deploy có "Kịch bản hoàn tác".
- [ ] Người làm sau đọc `docs/PROJECT-NOTES.md` trước khi bắt đầu.
