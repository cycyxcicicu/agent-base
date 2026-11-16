> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục D, H

# Quy trình soạn thảo Markdown & Xuất Excel SRS_FDD — Phần 1: Khung 3 File

## D. Định dạng md, nơi lưu, quy ước (chuẩn hiện hành)
- **Giai đoạn này viết ra file md**, chưa đổ vào xlsx. Khung: `agents/templates/srs-chuc-nang/srs-chuc-nang-template.md` (16 mục, mỗi mục ghi rõ ứng với sheet nào của mẫu SRS_FDD) — **sao chép khung rồi điền, không tự đổi cấu trúc**; mục không dùng → ghi "Không áp dụng — <lý do>".
- **Nơi lưu:** `doc/features/<UC>/<UC>-<slug>.md`, **một thư mục một chức năng**; cập nhật bảng ở `doc/features/README.md` (mã, tên, trạng thái, căn cứ, ngày).
- **Mã chức năng:** `UC-<nn>` (hỏi người dùng nếu chưa có quy ước; mặc định đề xuất, chưa chốt). Trạng thái: `Draft` → `Đã soát` → `Approved` (**chỉ người dùng đổi**).
- **Khi bắt đầu một SRS:** (1) xác nhận với người dùng tên chức năng, phạm vi, đã code hay chưa; (2) đọc nguồn: `doc/yeu-cau/project-doc` (mục liên quan), `doc/ban-do-tai-lieu.md` → file 05/06/07; code thật của service; (3) soạn bản **Draft** từng mục, đánh dấu **câu hỏi chờ xác nhận** ở mục 16; (4) báo người dùng soát — không tự chuyển trạng thái.
- Về sau nếu chuyển sang xlsx: nội dung mỗi mục md copy sang đúng sheet theo chú thích `*(sheet …)*`.

## H. Ba file cho mỗi chức năng (chốt 18/10/2026)

| File | Trả lời câu hỏi | Mẫu |
|---|---|---|
| `doc/features/<UC>/<UC>-<slug>.md` | Hệ thống phải làm gì (yêu cầu, A/C, giao diện, API, test) | `templates/srs-chuc-nang-template.md` |
| `doc/features/<UC>/<UC>-thiet-ke-ky-thuat.md` | Làm bằng công nghệ gì, từng class và hàm làm gì, luồng chạy ra sao, mở rộng thế nào | `templates/thiet-ke-ky-thuat-template.md` |
| `doc/features/<UC>/<UC>-doi-chieu.md` | Code hiện có khớp hay lệch đặc tả, việc còn lại, RTM | Xem `UC-01-doi-chieu.md` |

Thiết kế kỹ thuật ứng với các mục "Công nghệ và cài đặt", sơ đồ mức lớp và hàm, đặc tả service của mẫu SRS_FDD (sheet `Functions_Services_Detail_Desig` mục 2b, 3 và 6). Viết sau đặc tả và trước code (chức năng mới) hoặc sau khi đọc code (chức năng đã có). Mỗi hàm quan trọng phải có: vào, ra, logic từng bước, ngoại lệ. Mỗi thuật toán không hiển nhiên phải giải thích lý do chọn.
