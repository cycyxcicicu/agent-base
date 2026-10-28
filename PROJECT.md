# PROJECT.md — phần riêng của từng dự án

Đây là file duy nhất (cùng `agents/stacks/`) cần sửa khi mang `agent-base` sang dự án mới. Điền đầy đủ trước khi giao việc cho agent.

| Mục | Giá trị |
|---|---|
| Tên dự án | (điền) |
| Mô tả một câu | (điền) |
| Stack | (chọn file trong `agents/stacks/`: python / node / dotnet / ...) |
| Nhánh chính | main |
| Nhánh tích hợp | develop |
| Thư mục tài liệu | docs |
| Thư mục SRS | docs/spec |

## Lệnh

Ghi lệnh thật của dự án. Nếu để trống, agent dùng mặc định trong file stack.

| Việc | Lệnh |
|---|---|
| Cài phụ thuộc | (điền) |
| Chạy | (điền) |
| Test | (điền) |
| Lint / format | (điền) |
| Build | (điền) |

## Phạm vi và ràng buộc

- Ngoài phạm vi: (điền)
- Ràng buộc kỹ thuật (phiên bản, giấy phép, hạ tầng): (điền)
- File dùng chung, chỉ task được chỉ định mới sửa: (ví dụ `package.json`, lockfile)
- File/thư mục cấm agent đụng thêm ngoài quy tắc chung: (điền)

## Domain

Thuật ngữ, quy tắc nghiệp vụ, tài liệu tham chiếu quan trọng của dự án này: (điền)

## Có thao tác không hoàn tác được không?

Cơ sở dữ liệu, dữ liệu thật, deploy, dịch vụ ngoài: (điền). Task nào đụng các thứ này phải có "Kịch bản hoàn tác" trong task card.
