# Thiết kế kỹ thuật: <tên chức năng>

| Trường | Giá trị |
|---|---|
| Mã chức năng | `UC-<nn>` |
| Loại tài liệu | Thiết kế kỹ thuật (FDD, mục "Công nghệ và cài đặt", sơ đồ mức lớp và hàm) |
| Trạng thái | Draft |
| Ngày đọc code / viết | dd/mm/yyyy |
| Phạm vi | <module, service, đường dẫn gốc; viết tắt đường dẫn dùng trong file> |
| Đặc tả liên quan | `UC-<nn>-<slug>.md`, `UC-<nn>-doi-chieu.md` |

<!-- Viết sau đặc tả. Chức năng chưa có code: ghi thiết kế dự kiến ("sẽ"); đã có code: ghi đúng code đọc được, không đoán. Văn phong mục F. -->

## 1. Công nghệ
| Lớp | Công nghệ | Dùng để | Lý do chọn |
|---|---|---|---|

## 2. Kiến trúc
<sơ đồ thành phần (Mermaid) + nguyên tắc thiết kế (3 đến 5 điều) + phân vai các thành phần>

## 3. Luồng chạy chi tiết
<bảng bước: Bước | Nơi (class.hàm) | Việc; kèm sơ đồ sequence mức class>

## 4. Mô tả class
| Class (gói) | Trách nhiệm |
|---|---|

## 5. Mô tả hàm
<mỗi hàm quan trọng: Hàm | Vào | Ra | Logic từng bước | Ngoại lệ>
<mỗi thuật toán không hiển nhiên: giải thích lý do chọn (hiệu năng, an toàn, đồng thời)>

## 6. Cấu trúc dữ liệu
<kiểu, record, JSON mẫu, bảng DB nếu có>

## 7. Hằng số và cấu hình
| Tên | Giá trị | Nơi | Ý nghĩa |
|---|---|---|---|

## 8. Xử lý lỗi
| Tình huống | Nơi phát hiện | Ngoại lệ | Kết quả cho người dùng |
|---|---|---|---|

## 9. Hiệu năng, bộ nhớ, đồng thời
<số liệu đã đo; chưa đo thì ghi "chưa đo">

## 10. Cách mở rộng
<các việc thường gặp: thêm trường, thêm màn, thêm kiểu; mỗi việc là danh sách bước đánh số>

## 11. Lưu ý khi sửa code
<ràng buộc dễ vỡ, thứ tự phụ thuộc, test liên quan, hạn chế đã biết>
