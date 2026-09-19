# Định nghĩa hoàn thành (theo cỡ việc)

## Nhỏ
- [ ] Nhánh riêng, một commit đúng mẫu (`Task:`, `Agent:`).
- [ ] Test và lint chạy qua.
- [ ] `scripts/merge-gate.ps1` PASS (hoặc diff nằm trong phạm vi đã nêu).
- [ ] Một dòng trong `tasks/quick-log.md`.
- [ ] Người dùng đã xem diff.

## Vừa
- [ ] Mọi mục của "Nhỏ".
- [ ] Task card đầy đủ: tiêu chí xong đạt hết, nhật ký phiên, file đã đổi, kết quả test.
- [ ] Reviewer duyệt (theo checklist trong `agents/roles/reviewer.md`).
- [ ] QA xác nhận từng tiêu chí bằng test hoặc bước kiểm tra cụ thể.

## Lớn
- [ ] Mọi mục của "Vừa", cho từng task con.
- [ ] Yêu cầu R-xxx đều được thực hiện và đã được người dùng duyệt từ đầu.
- [ ] Các nhánh gộp vào nhánh tích hợp từng cái một, test chạy sau mỗi lần gộp.
- [ ] Squash merge: mỗi task một commit, gắn tag `T-xxx`.
- [ ] Tech Writer cập nhật CHANGELOG và tài liệu.
- [ ] Người dùng duyệt cuối trước khi vào `main`.

## Luôn luôn
- [ ] Không có khóa bí mật trong code, log, card.
- [ ] Việc đụng DB, dữ liệu thật hoặc deploy có "Kịch bản hoàn tác".
