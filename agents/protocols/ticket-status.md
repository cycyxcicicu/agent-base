# Ánh xạ trạng thái ticket của công ty sang task card

Nguồn: quy trình công ty (`quy-trinh-cong-ty.md` mục 1). Khung dùng năm trạng thái `todo`, `doing`, `review`, `done`, `blocked` (`task-card.md`, script `task-board.py` kiểm các giá trị này). **Không thêm trạng thái mới**; dự án cần theo dõi sâu hơn thì ghi giai đoạn trong card và dùng bảng ánh xạ dưới.

| Trạng thái ticket công ty | Trạng thái card | Ai chuyển | Điều kiện sang trạng thái này |
|---|---|---|---|
| New | `todo` | lead, product | Có mã task và mô tả; chưa đủ DoR |
| Ready for Technical Architect | `todo` | ba, analyst | Yêu cầu và A/C đã rõ, chờ thiết kế giải pháp |
| Ready for Development | `todo` | architect | Thiết kế đã qua Solution-Pair (`pair-review.md`), spec `Approved`, đủ DoR |
| To Do | `todo` | lead | Đã xếp vào sprint hoặc đợt làm, có người nhận |
| In Progress | `doing` | dev | Plan đã duyệt (`plan-critique.md`), đang làm trong nhánh riêng |
| In Quality Assurance | `review` | dev | Test xanh, đã qua Code-Review-Pair; qa kiểm thử đầy đủ |
| Release | `done` | writer sau khi người dùng duyệt | Đã merge và có release note (`release-note.md`) |
| (bị chặn) | `blocked` | bất kỳ ai | Ghi lý do vào card; không tự đoán tiếp |

## Quy tắc

1. Chỉ lùi trạng thái bằng cách ghi lý do vào card (ví dụ qa trả lại: `review` về `doing`, kèm mã lỗi).
2. Đổi `status` xong chạy `python scripts/task-board.py` để cập nhật bảng, như `task-card.md` đã quy định.
3. Giai đoạn chi tiết của công ty (cột 1) ghi vào nhật ký phiên của card, không tạo trường mới.
4. Đóng lỗi theo quy tắc công ty: dev chỉ đưa về "đã sửa", **chỉ qa mới đóng**; lỗi cũ tái phát thì mở lại, không tạo mới.
