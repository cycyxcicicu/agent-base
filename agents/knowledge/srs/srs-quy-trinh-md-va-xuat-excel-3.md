> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục J, K

# Quy trình soạn thảo Markdown & Xuất Excel SRS_FDD — Phần 3: Tài Liệu Theo Màn & Câu Hỏi Mở

## J. Tài liệu theo từng màn hình và ERD (chốt 18/10/2026)

Mẫu SRS của dự án có cho **mỗi màn**: UI Form, User Story, ERD, Component diagram. Chức năng chạm nhiều màn (như xuất Excel, ẩn/hiện cột) phải có thêm phần theo màn.

1. **File theo màn:** `doc/features/<UC>/<UC>-theo-man-hinh.md`, mỗi màn một mục `## MAN-<nn> <tên màn>` gồm: bảng thông tin màn (đường dẫn, khoá màn, API), 1 Giao diện (mockup trong SRS và bảng thành phần với nhãn đúng giao diện), 2 Cột hiển thị, 3 phần riêng của chức năng, 4..., 5 ERD, 6 Component, 7 Happy path, 8 Happy case, 9 Câu hỏi mở.
2. **ERD là bắt buộc kể cả khi không thêm bảng:** vẽ các bảng mà màn đọc hoặc ghi, chỉ các cột màn dùng, kèm bảng "Cột | Kiểu | Giải thích | Dùng làm gì" như SRS. Lấy tên bảng, cột, kiểu từ Entity và Liquibase, không đoán. Không ghi "ERD: Không".
3. **Component diagram theo màn:** vẽ bằng archify (loại `architecture`): thành phần giao diện, API, service, DB, dịch vụ ngoài của đúng màn đó; dịch vụ ngoài đặt ngoài khung ranh giới.
4. **Happy path và happy case theo màn:** viết trong mục 7, 8 của file theo màn; bảng happy case có cột `Mã case | Tên case | Điều kiện | Bước | Hành động | Kết quả mong đợi | Mức`, mỗi hàng một bước, theo `quy-trinh/qa-process.md` (ngôn ngữ giao diện, nhãn kiểm chứng từ code hoặc locale).
5. **Sinh file import TestLink:** `python3 scripts/srs_md_to_testlink.py [--keyword MÃ-TASK]` ghi `doc/features/<UC>/<UC>-testlink-cases.xml` theo mẫu `quy-trinh/templates/testlink-import-sample-tracking.xml`. Chưa có mã task thì để trống Keyword và nhắc gắn tay trên TestLink.
6. **Viết thử 2 màn trước, duyệt cách viết rồi mới nhân ra các màn còn lại.**

## K. Câu hỏi gửi Kế toán, BA (chốt 18/10/2026)

Gộp các câu hỏi mở thành một file `doc/features/<UC>/cau-hoi-ke-toan.md` (một bảng: Mã, Nhóm, Màn, Câu hỏi, Bối cảnh, Phương án A, B, C, Khuyến nghị). Quy tắc: câu hỏi bằng ngôn ngữ nghiệp vụ (không tên class, hàm); mỗi câu 3 phương án và một khuyến nghị có lý do; bỏ câu đã quyết; câu kỹ thuật chuyển sang "hỏi BA và Dev". Bản Excel có ô chọn: `python3 scripts/srs_questions_to_xlsx.py`.
