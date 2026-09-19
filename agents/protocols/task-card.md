# Mẫu task card

Sao chép nội dung dưới đây thành `tasks/T-xxx.md`. Phần giữa hai dòng `---` được script đọc (`scripts/merge-gate.ps1`), giữ đúng tên khóa và định dạng danh sách.

```markdown
---
id: T-012
size: medium
status: todo
owner: dev-a
branch: feat/T-012
requirements: [R-003, R-004]
scope_edit:
  - src/auth/**
  - tests/auth/**
scope_deny:
  - package.json
---

# T-012: <tiêu đề ngắn>

## Mục tiêu
(1–3 câu: làm gì, để đạt gì)

## Tiêu chí xong
- [ ] ...
- [ ] ...

## Phụ thuộc
(task nào phải xong trước, hoặc "không")

## Ghi chú bàn giao
(thêm ở cuối, mỗi mục ghi ngày và tên agent)

## Nhật ký phiên
(đã làm gì, quyết định gì, còn dang dở gì)

## File đã đổi
(danh sách, kèm lý do)

## Kết quả test
(lệnh đã chạy và kết quả)

## Kịch bản hoàn tác
(bắt buộc nếu đụng cơ sở dữ liệu, dữ liệu thật hoặc deploy. Nếu không: "chỉ cần git revert")
```

## Giá trị hợp lệ

| Khóa | Giá trị |
|---|---|
| `size` | `small`, `medium`, `large` |
| `status` | `todo`, `doing`, `review`, `done`, `blocked` |
| `scope_edit` | mẫu đường dẫn tính từ gốc repo, dùng `*` (trong một thư mục) và `**` (nhiều cấp) |
| `scope_deny` | mẫu đường dẫn, luôn thắng `scope_edit` |

Card của chính task (`tasks/<id>.md`) luôn được phép sửa, không cần khai báo.
Hai task chạy song song không được có `scope_edit` chồng nhau. File dùng chung chỉ đưa vào `scope_edit` của một task duy nhất.
