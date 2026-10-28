# Epic của dự án

**Epic** = một nhóm chức năng (ví dụ: "Đăng nhập & phân quyền", "Giỏ hàng", "Thanh toán"). Mỗi task card thuộc đúng một epic và **nằm trong thư mục của epic đó**: `tasks/<Thư mục>/T-<số>.md`. Nhờ vậy các task cùng chức năng nằm chung một chỗ, và `tasks/BOARD.md` (sinh bằng `python scripts/task-board.py`) cho biết đang ở đâu.

**Bảng này khác nhau ở mỗi dự án**, vì mỗi dự án có chức năng riêng. Agent-base chỉ để mẫu. Khi mang sang dự án mới: Lead đọc tài liệu yêu cầu và kế hoạch, thay bảng dưới bằng epic thật (bám theo phân hệ chức năng và mốc nghiệm thu), trình người dùng duyệt **trước khi tạo card đầu tiên**. Giữ `E0` cho phần phân tích và thiết kế.

Lưu ý cho dự án mới: hàng **E2** dưới đây là epic riêng của repo agent-base (đang cải tiến chính khung). Khi bootstrap sang dự án khác, **xóa hàng E2** cùng thư mục `tasks/E2-*` cùng lúc thay bảng bằng epic thật.

Quy tắc:
- Chỉ Lead thêm hoặc đổi epic, và phải báo người dùng khi đổi.
- Thư mục: `E<số>-<tên-ngắn-không-dấu>`, ví dụ `E2-tuyen-dung-cv`. Không đổi tên thư mục khi đã có card.
- Giữ đúng 5 cột dưới đây: script đọc bảng này.

| Epic | Thư mục | Tên | Mã yêu cầu | Phase |
|---|---|---|---|---|
| E0 | `E0-phan-tich` | Phân tích & thiết kế | — | PT |
| E1 | `E1-nen-tang` | Nền tảng: khung dự án, xác thực, cấu hình | (điền) | GĐ1 |
| E2 | `E2-tri-thuc-quy-trinh` | Tri thức, quy trình hợp nhất và kiểm chứng (đồ thị tài liệu, duyệt bằng file, vòng 13 bước, tái hiện lỗi, eval có bằng chứng) | R-pilot (chờ BA, T-18) | GĐ1 |

## Phase

| Phase | Nghĩa | Mốc |
|---|---|---|
| PT | Phân tích, thiết kế trước khi code | (điền) |
| GĐ1 | Giai đoạn 1 | (điền) |
