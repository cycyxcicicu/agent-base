# Mẫu task card

Sao chép nội dung dưới đây thành `tasks/T-<ticket>.md`. Số ticket dùng luôn trong tên nhánh: ticket 12 ↔ `tasks/T-12.md` ↔ `feature/12-token-check`. Phần giữa hai dòng `---` được script đọc (`scripts/merge-gate.ps1`), giữ đúng tên khóa và định dạng danh sách.

```markdown
---
id: T-12
size: medium
status: todo
owner: dev-a
branch: feature/12-token-check
requirements: [R-003, R-004]
scope_edit:
  - src/auth/**
  - tests/auth/**
scope_deny:
  - package.json
---

# T-12: <tiêu đề ngắn>

## Mục tiêu
(1–3 câu: làm gì, để đạt gì)

## Contract & Happy Path (Đặc tả trước khi code)
- **Đầu vào (Input)**: (cấu trúc dữ liệu, request payload, parameters)
- **Đầu ra (Output)**: (response payload, status code, format)
- **Kịch bản Happy Path**: (input cụ thể -> kết quả mong đợi cụ thể có thể quan sát được)

## Tiêu chí xong
- [ ] Happy Path Unit Test chạy PASS 100%
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

## Kế hoạch commit (người dùng chạy)
(agent viết theo `agents/protocols/commit-plan.md`; agent KHÔNG tự chạy)

## Chấp thuận rủi ro
(nếu task có việc mất code, dữ liệu hay công việc: số phiếu RK-<n> và trạng thái. Xem `agents/protocols/risk-gate.md`. Không có thì ghi "không có")

## Sau khi merge
- Mã merge commit: (người dùng điền, dùng để hoàn tác bằng `git revert -m 1`)

## Kịch bản hoàn tác
(bắt buộc nếu đụng cơ sở dữ liệu, dữ liệu thật hoặc deploy. Nếu không: "chỉ cần git revert -m 1 <merge commit>")
```

## Giá trị hợp lệ

| Khóa | Giá trị |
|---|---|
| `size` | `small`, `medium`, `large` |
| `status` | `todo`, `doing`, `review`, `done`, `blocked` |
| `branch` | `<type>/<ticket>-<mô-tả-ngắn>` theo `agents/protocols/git-rules.md` |
| `scope_edit` | mẫu đường dẫn tính từ gốc repo, dùng `*` (trong một thư mục) và `**` (nhiều cấp) |
| `scope_deny` | mẫu đường dẫn, luôn thắng `scope_edit` |

Card của chính task (`tasks/<id>.md`) luôn được phép sửa, không cần khai báo.
Hai task chạy song song không được có `scope_edit` chồng nhau. File dùng chung chỉ đưa vào `scope_edit` của một task duy nhất.
