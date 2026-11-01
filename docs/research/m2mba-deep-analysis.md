# BÁO CÁO PHÂN TÍCH CHUYÊN SÂU 190 BÀI VIẾT M2MBA (BA STREAM)
> Chuyên viên thực hiện: **Sophia (Senior BA)** | Thời gian: 2026-11-01 12:35:10

## 1. TỔNG QUAN ĐỊNH LƯỢNG
- **Tổng số bài viết đã phân tích**: 190 bài
- **Bài viết có giá trị chuyên môn cao (GIỮ LẠI)**: 182 bài (95%)
- **Bài viết tuyển sinh / rác quảng cáo (LOẠI BỎ)**: 8 bài (4%)
- **Tổng số hình ảnh sơ đồ thực tế**: 81 ảnh

## 2. PHÂN BỔ THEO 5 NHÓM CHUYÊN MÔN CỐT LÕI

| Nhóm Chuyên Môn | Số Lượng Bài | Số Hình Ảnh | Ứng Dụng Thực Tế Cho Agent-Base |
|---|---|---|---|
| **1. Thanh toán & Cổng GD (Payment)** | 9 bài | 5 ảnh | Mẫu luồng QR Momo, POS, CITAD, Webhook |
| **2. State Machine & Vòng đời** | 5 bài | 1 ảnh | Bắt trọn vẹn mọi trạng thái ngoại lệ, tránh sót bug |
| **3. CSDL, SQL & ERD Thực chiến** | 40 bài | 11 ảnh | Mapping UI ra Table, Rule validate 2 tầng |
| **4. API & Tích Hợp Hệ Thống** | 21 bài | 7 ảnh | Đặc tả hợp đồng API, Idempotency key |
| **5. Quy Trình BA & SRS Chuẩn** | 107 bài | 56 ảnh | RTM, Use Case Include/Extend, Phân tích nghiệp vụ |
| **6. Bài Tuyển Sinh / Rác (BỎ)** | 8 bài | 0 ảnh | ĐÃ LỌC BỎ KHỎI KHO TRI THỨC |

## 3. DANH SÁCH CHI TIẾT CÁC BÀI CHUYÊN MÔN NÊN LẤY (TOP TIÊU BIỂU)

### NHÓM THANH TOÁN & GIAO DỊCH (9 bài)
- **Cài đặt postman để chạy thử API** (`cai-dat-postman-de-chay-thu-api`) — 1 ảnh | [posts/cai-dat-postman-de-chay-thu-api/README.md](file:///D:/test-repo/m2mba/posts/cai-dat-postman-de-chay-thu-api/README.md)
- **Luồng GD chuyển tiền qua CITAD** (`luong-giao-dich-chuyen-tien-qua-citad`) — 1 ảnh | [posts/luong-giao-dich-chuyen-tien-qua-citad/README.md](file:///D:/test-repo/m2mba/posts/luong-giao-dich-chuyen-tien-qua-citad/README.md)
- **Luồng giao dịch quẹt thẻ máy POS** (`luong-giao-dich-quet-the-may-pos`) — 1 ảnh | [posts/luong-giao-dich-quet-the-may-pos/README.md](file:///D:/test-repo/m2mba/posts/luong-giao-dich-quet-the-may-pos/README.md)
- **Luồng thanh toán QR** (`luong-thanh-toan-qr`) — 1 ảnh | [posts/luong-thanh-toan-qr/README.md](file:///D:/test-repo/m2mba/posts/luong-thanh-toan-qr/README.md)
- **Tạo QR thanh toán Momo - Tài liệu chức năng có actor là end user** (`tao-qr-thanh-toan-momo-tai-lieu-chuc-nang`) — 1 ảnh | [posts/tao-qr-thanh-toan-momo-tai-lieu-chuc-nang/README.md](file:///D:/test-repo/m2mba/posts/tao-qr-thanh-toan-momo-tai-lieu-chuc-nang/README.md)
- **Test API thông qua tool Postman** (`9166ed5e-88c4-40f8-9573-f83853859e81`) — 0 ảnh | [posts/9166ed5e-88c4-40f8-9573-f83853859e81/README.md](file:///D:/test-repo/m2mba/posts/9166ed5e-88c4-40f8-9573-f83853859e81/README.md)
- **Luồng xử lý thanh toán qua thẻ tín dụng** (`cach-tinh-interchange-accessment-fee-trong-cac-giao-dich-the`) — 0 ảnh | [posts/cach-tinh-interchange-accessment-fee-trong-cac-giao-dich-the/README.md](file:///D:/test-repo/m2mba/posts/cach-tinh-interchange-accessment-fee-trong-cac-giao-dich-the/README.md)
- **Thảo luận về luồng thanh toán QR** (`giai-phap-thanh-toan-qr-da-nen-tang`) — 0 ảnh | [posts/giai-phap-thanh-toan-qr-da-nen-tang/README.md](file:///D:/test-repo/m2mba/posts/giai-phap-thanh-toan-qr-da-nen-tang/README.md)
- **Lịch sử phát triển thẻ ở VN** (`lich-su-phat-trien-the-o-vn-va-bai-hoc-qr`) — 0 ảnh | [posts/lich-su-phat-trien-the-o-vn-va-bai-hoc-qr/README.md](file:///D:/test-repo/m2mba/posts/lich-su-phat-trien-the-o-vn-va-bai-hoc-qr/README.md)

### NHÓM STATE MACHINE & VÒNG ĐỜI TRẠNG THÁI (5 bài)
- **state-diagram-cho-ba-huong-dan-chi-tiet** (`state-diagram-cho-ba-huong-dan-chi-tiet`) — 1 ảnh | [posts/state-diagram-cho-ba-huong-dan-chi-tiet/README.md](file:///D:/test-repo/m2mba/posts/state-diagram-cho-ba-huong-dan-chi-tiet/README.md)
- **Kỹ thuật State Diagram cho Business Analyst: Hướng dẫn chi tiết & Các sai lầm cần tránh** (`68f4ec24-19bf-4468-9a72-1fa7de9c74db`) — 0 ảnh | [posts/68f4ec24-19bf-4468-9a72-1fa7de9c74db/README.md](file:///D:/test-repo/m2mba/posts/68f4ec24-19bf-4468-9a72-1fa7de9c74db/README.md)
- **State diagram** (`huong-dan-ve-bieu-do-trang-thai-cho-ba`) — 0 ảnh | [posts/huong-dan-ve-bieu-do-trang-thai-cho-ba/README.md](file:///D:/test-repo/m2mba/posts/huong-dan-ve-bieu-do-trang-thai-cho-ba/README.md)
- **Phân biệt Flowchart, BPMN, Activity diagram, workflow, state diagram** (`phan-biet-flowchart-bpmn-activity-diagram`) — 0 ảnh | [posts/phan-biet-flowchart-bpmn-activity-diagram/README.md](file:///D:/test-repo/m2mba/posts/phan-biet-flowchart-bpmn-activity-diagram/README.md)
- **Tìm hiểu về hệ thống GPS, trạng thái giao thông google map** (`tim-hieu-ve-he-thong-gps-va-giao-thong-google-map`) — 0 ảnh | [posts/tim-hieu-ve-he-thong-gps-va-giao-thong-google-map/README.md](file:///D:/test-repo/m2mba/posts/tim-hieu-ve-he-thong-gps-va-giao-thong-google-map/README.md)

### NHÓM CSDL, ERD & QUY TẮC DỮ LIỆU (40 bài)
- **Bài test mẫu cho khóa IT cơ bản** (`bai-test-cuoi-khoa-it-co-ban`) — 1 ảnh | [posts/bai-test-cuoi-khoa-it-co-ban/README.md](file:///D:/test-repo/m2mba/posts/bai-test-cuoi-khoa-it-co-ban/README.md)
- **Câu lệnh Select** (`cau-lenh-select-trong-sql`) — 1 ảnh | [posts/cau-lenh-select-trong-sql/README.md](file:///D:/test-repo/m2mba/posts/cau-lenh-select-trong-sql/README.md)
- **Câu lệnh Update, Delete** (`cch-s-dng-cu-lnh-update-delete-trong-sql-hiu-qu`) — 1 ảnh | [posts/cch-s-dng-cu-lnh-update-delete-trong-sql-hiu-qu/README.md](file:///D:/test-repo/m2mba/posts/cch-s-dng-cu-lnh-update-delete-trong-sql-hiu-qu/README.md)
- **Giới thiệu về Database** (`cm-nang-c-bn-v-database`) — 1 ảnh | [posts/cm-nang-c-bn-v-database/README.md](file:///D:/test-repo/m2mba/posts/cm-nang-c-bn-v-database/README.md)
- **Câu lệnh Insert** (`cu-lnh-insert-trong-sql---hng-dn-s-dng-chi-tit`) — 1 ảnh | [posts/cu-lnh-insert-trong-sql---hng-dn-s-dng-chi-tit/README.md](file:///D:/test-repo/m2mba/posts/cu-lnh-insert-trong-sql---hng-dn-s-dng-chi-tit/README.md)
- **Câu lệnh Join** (`cu-lnh-join-trong-sql---hng-dn-ton-din-2023`) — 1 ảnh | [posts/cu-lnh-join-trong-sql---hng-dn-ton-din-2023/README.md](file:///D:/test-repo/m2mba/posts/cu-lnh-join-trong-sql---hng-dn-ton-din-2023/README.md)
- **Demo lệnh Join** (`demo-lnh-join-trong-sql-hng-dn-y--cc-loi`) — 1 ảnh | [posts/demo-lnh-join-trong-sql-hng-dn-y--cc-loi/README.md](file:///D:/test-repo/m2mba/posts/demo-lnh-join-trong-sql-hng-dn-y--cc-loi/README.md)
- **Khóa chính (Primary Key)** (`kha-chnh-primary-key--ngha-v-vai-tr-trong-csdl`) — 1 ảnh | [posts/kha-chnh-primary-key--ngha-v-vai-tr-trong-csdl/README.md](file:///D:/test-repo/m2mba/posts/kha-chnh-primary-key--ngha-v-vai-tr-trong-csdl/README.md)
- **Lập trình tương tác với Database** (`lap-trinh-tuong-tac-voi-db`) — 1 ảnh | [posts/lap-trinh-tuong-tac-voi-db/README.md](file:///D:/test-repo/m2mba/posts/lap-trinh-tuong-tac-voi-db/README.md)
- **Tổng hợp mối quan hệ giữa các bảng trong database** (`moi-quan-he-cac-bang-trong-thiet-ke-CSDL`) — 1 ảnh | [posts/moi-quan-he-cac-bang-trong-thiet-ke-CSDL/README.md](file:///D:/test-repo/m2mba/posts/moi-quan-he-cac-bang-trong-thiet-ke-CSDL/README.md)
- **Mối quan hệ giữa các bảng** (`moi-quan-he-giua-cac-bang-trong-csdl`) — 1 ảnh | [posts/moi-quan-he-giua-cac-bang-trong-csdl/README.md](file:///D:/test-repo/m2mba/posts/moi-quan-he-giua-cac-bang-trong-csdl/README.md)
- **Cú pháp SQL phổ biến** (`181a3926-9850-4a1f-a702-1076a7d38aac`) — 0 ảnh | [posts/181a3926-9850-4a1f-a702-1076a7d38aac/README.md](file:///D:/test-repo/m2mba/posts/181a3926-9850-4a1f-a702-1076a7d38aac/README.md)

### NHÓM API & TÍCH HỢP HỆ THỐNG (21 bài)
- **ai-agent-builder-workflow-api** (`ai-agent-builder-workflow-api`) — 5 ảnh | [posts/ai-agent-builder-workflow-api/README.md](file:///D:/test-repo/m2mba/posts/ai-agent-builder-workflow-api/README.md)
- **Giới thiệu về API** (`gioi-thieu-ve-api`) — 1 ảnh | [posts/gioi-thieu-ve-api/README.md](file:///D:/test-repo/m2mba/posts/gioi-thieu-ve-api/README.md)
- **Tài liệu dạng API (API đặt bàn)** (`tai-lieu-dang-api-dat-ban`) — 1 ảnh | [posts/tai-lieu-dang-api-dat-ban/README.md](file:///D:/test-repo/m2mba/posts/tai-lieu-dang-api-dat-ban/README.md)
- **Thành phần request API** (`034d254b-abef-4afb-9b40-68c1019b3a39`) — 0 ảnh | [posts/034d254b-abef-4afb-9b40-68c1019b3a39/README.md](file:///D:/test-repo/m2mba/posts/034d254b-abef-4afb-9b40-68c1019b3a39/README.md)
- **Xác định API trong 1 UC (lý thuyết)** (`0c614d23-b75a-42e4-99a5-c4490fd12812`) — 0 ảnh | [posts/0c614d23-b75a-42e4-99a5-c4490fd12812/README.md](file:///D:/test-repo/m2mba/posts/0c614d23-b75a-42e4-99a5-c4490fd12812/README.md)
- **Tích hợp API của bên đối tác - Hướng dẫn đọc hiểu chi tiết đặc tả từng API** (`2f190b9d-fc3f-418e-aa3c-de7e2129ac1a`) — 0 ảnh | [posts/2f190b9d-fc3f-418e-aa3c-de7e2129ac1a/README.md](file:///D:/test-repo/m2mba/posts/2f190b9d-fc3f-418e-aa3c-de7e2129ac1a/README.md)
- **Sử dụng google Opal để phân tích API của 1 usecase** (`2ff377c7-cfb5-4ecf-9a66-e0f370daeedb`) — 0 ảnh | [posts/2ff377c7-cfb5-4ecf-9a66-e0f370daeedb/README.md](file:///D:/test-repo/m2mba/posts/2ff377c7-cfb5-4ecf-9a66-e0f370daeedb/README.md)
- **Định nghĩa về API** (`3da6088b-7ae3-4491-bed2-429c2fe9da1d`) — 0 ảnh | [posts/3da6088b-7ae3-4491-bed2-429c2fe9da1d/README.md](file:///D:/test-repo/m2mba/posts/3da6088b-7ae3-4491-bed2-429c2fe9da1d/README.md)
- **Tích hợp API của bên đối tác - Viết tài liệu transfer cho dev** (`49f5cf20-200f-436e-942a-afb11a5ed273`) — 0 ảnh | [posts/49f5cf20-200f-436e-942a-afb11a5ed273/README.md](file:///D:/test-repo/m2mba/posts/49f5cf20-200f-436e-942a-afb11a5ed273/README.md)
- **Format Data trao đổi trong API** (`5dff67ff-9b48-40c9-af43-fa3f348c121d`) — 0 ảnh | [posts/5dff67ff-9b48-40c9-af43-fa3f348c121d/README.md](file:///D:/test-repo/m2mba/posts/5dff67ff-9b48-40c9-af43-fa3f348c121d/README.md)
- **Thành phần response API** (`890865ac-a81d-44e0-9e78-1f8cec48e1ab`) — 0 ảnh | [posts/890865ac-a81d-44e0-9e78-1f8cec48e1ab/README.md](file:///D:/test-repo/m2mba/posts/890865ac-a81d-44e0-9e78-1f8cec48e1ab/README.md)
- **Đặc tả API** (`9c04bdfe-fb77-4c33-a8a1-863becb6d6cc`) — 0 ảnh | [posts/9c04bdfe-fb77-4c33-a8a1-863becb6d6cc/README.md](file:///D:/test-repo/m2mba/posts/9c04bdfe-fb77-4c33-a8a1-863becb6d6cc/README.md)

