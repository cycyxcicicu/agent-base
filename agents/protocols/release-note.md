# Release note

Nguồn: quy trình công ty, phần CI/CD (`quy-trinh-cong-ty.md` mục 7). Viết **mỗi lần phát hành**, do `writer` soạn sau khi merge, người dùng duyệt. Lưu ở `docs/releases/<phiên-bản>.md` (tạo thư mục khi cần), cùng tên với tag `v<MAJOR>.<MINOR>.<PATCH>`.

## Nội dung bắt buộc

1. **Thông tin phát hành:** dự án, phiên bản, ngày, nhánh, tag, người duyệt (để tracking, audit, rollback).
2. **Tính năng mới và cải tiến:** theo module, mỗi dòng kèm mã task.
3. **Lỗi đã sửa:** mã lỗi và mô tả một dòng.
4. **Thay đổi có thể ảnh hưởng tương thích:** API, cấu hình, xác thực, schema. Nếu không có thì ghi "không có".
5. **Vấn đề còn tồn tại** đã biết.
6. **Thay đổi kỹ thuật ảnh hưởng vận hành:** migration, biến môi trường mới, bước triển khai thủ công.
7. **Xác nhận chất lượng:** test pass, báo cáo scan, ai đã review và duyệt.
8. **Cách quay lại:** lệnh hoặc quy trình hoàn tác, theo `risk-gate.md`.

## Quy tắc

- Chỉ ghi điều có trong git log, task card, kết quả test. Không ghi điều chưa kiểm chứng.
- Release note là đầu vào của CHANGELOG do `writer` giữ; không để hai bản lệch nhau.
