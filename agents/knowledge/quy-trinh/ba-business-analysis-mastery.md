# Cẩm Nang Phân Tích Nghiệp Vụ Thực Chiến (BA Mastery)

**Loại: tham khảo.**
> **Phân vùng**: Business Analysis & Product Management  
> **Phân quyền truy cập (RBAC)**: `["ba", "product", "analyst"]`  
> **Nguồn đối chuẩn**: `https://m2mba.com/blog` & Trạm tri thức cục bộ `assets/m2mba/`  

---

## 1. Hai Thứ Cốt Lõi BA Cần Nắm Rõ Khi Làm Việc Với Đội Ngũ Dev
Khi tiếp nhận yêu cầu từ Product Owner (PO) hoặc Khách hàng, BA không cần phải là người viết code, nhưng bắt buộc phải nắm rõ **2 trụ cột khả thi**:
1. **Dữ liệu & Cấu trúc (Data Flow & Entities)**: Dữ liệu này lưu ở đâu? Có sinh bảng mới không? Có bị phụ thuộc khóa ngoại hay ảnh hưởng đến tính toàn vẹn dữ liệu hiện có không?
2. **Quy tắc nghiệp vụ & Ranh giới lỗi (Business Rules & Boundary States)**: Trạng thái này có thể chuyển sang trạng thái nào? Khi mạng đứt, thanh toán lỗi hoặc số dư không đủ thì hệ thống phản hồi như thế nào?

---

## 2. Kỹ Thuật Mô Hình Hóa State Machine Cho Business Analyst
Trong phân tích thiết kế, việc bỏ sót trạng thái là nguyên nhân hàng đầu sinh ra bug:
- **Nguyên tắc**: Mọi đối tượng kinh doanh (Đơn hàng, Hóa đơn, Giao dịch) phải được vẽ sơ đồ State Machine với đầy đủ:
  - Trạng thái khởi tạo (Initial State `[*]`).
  - Điều kiện chuyển trạng thái (Guard Conditions `[condition]`).
  - Trạng thái thành công và Trạng thái kết thúc có xử lý ngoại lệ (`Cancelled`, `Failed`, `Refunded`).

---

## 3. Phân Biệt Use Case Và User Story Trong Thực Tế
*(Trích xuất từ bài học thực chiến của chuyên gia Đậu Thị Ngọc Ánh - M2MBA)*
- **User Story (Góc nhìn Người dùng — Trả lời câu hỏi WHY)**:
  - Cấu trúc: `Là [Vai trò], tôi muốn [Hành động] để [Lợi ích]`.
  - Trọng tâm: Nêu rõ giá trị kinh doanh cho Stakeholder kèm **Tiêu chí nghiệm thu (Acceptance Criteria - AC)** có thể đo lường và kiểm chứng được.
- **Use Case (Góc nhìn Hệ thống — Trả lời câu hỏi HOW)**:
  - Cấu trúc: Tác nhân (`Actor`), Tiền điều kiện (`Pre-condition`), Luồng chính (`Happy Path`), Luồng rẽ nhánh (`Alternative Flow`), Luồng lỗi (`Exception Flow`), và Hậu điều kiện (`Post-condition`).
  - Trọng tâm: Nêu rõ từng bước tương tác giữa người dùng và hệ thống để dev cài đặt chính xác.
- **Quy tắc bóc tách**: Một User Story lớn có thể phân rã thành **nhiều Use Cases kỹ thuật**. Ví dụ: Story *"Thanh toán online đơn hàng"* được bẻ thành 3 Use Cases:
  1. `UC-01`: Khởi tạo thanh toán sang Cổng thanh toán (Momo/VNPAY).
  2. `UC-02`: Xử lý hiển thị kết quả khi redirect URL về website.
  3. `UC-03`: Cập nhật trạng thái đơn hàng qua Webhook ngầm.

---

## 4. Kỹ Thuật Viết Luồng Rẽ Nhánh (Alternative) vs Luồng Ngoại Lệ (Exception)
- **Alternative Flow**: Người dùng chọn hướng đi khác nhưng **vẫn đạt được mục tiêu ban đầu** (Ví dụ: Thay vì quẹt thẻ POS thì chuyển sang quét mã QR).
- **Exception Flow**: Hệ thống gặp sự cố, lỗi logic hoặc điều kiện bảo vệ không thỏa mãn dẫn đến **mục tiêu thất bại** (Ví dụ: Số dư tài khoản không đủ, thẻ hết hạn, đơn hàng đã bị hủy). Bắt buộc phải có thông báo lỗi rõ ràng và phương án hồi phục (Rollback/Retry).

---

## 5. Các Luồng Thanh Toán Tài Chính Cốt Lõi Tại Việt Nam
1. **Momo / VietQR Dynamic QR**:
   - Sinh mã QR chứa `Mã đơn hàng`, `Số tiền`, `Merchant ID`, thời gian hết hạn (15 phút).
   - Tích hợp Webhook xác nhận giao dịch bất đồng bộ (Async Notification) có chữ ký số HMAC-SHA256.
2. **Luồng Giao Dịch Quẹt Thẻ Máy POS**:
   - Tương tác 4 bên: Khách hàng (Cardholder) ➔ POS Merchant ➔ Ngân hàng thanh toán (Acquirer) ➔ Tổ chức thẻ (Visa/Mastercard) ➔ Ngân hàng phát hành (Issuer).
   - Xử lý phí Interchange Fee và phí Accessment Fee.
3. **Chuyển Tiền Liên Ngân Hàng CITAD & Napas**:
   - Luồng hạch toán 2 bước: Trừ tiền tài khoản nguồn ➔ Gửi lệnh thanh toán liên ngân hàng ➔ Nhận điện phản hồi đối soát.

---

## 6. Cấu Trúc Bộ Hồ Sơ Đặc Tả Yêu Cầu SRS Tiêu Chuẩn (14 Sheets Mẫu)
1. Danh mục thuật ngữ (Domain Glossary) — thống nhất khái niệm giữa Nghiệp vụ và Lập trình viên.
2. Ma trận truy vết yêu cầu (Requirement Traceability Matrix - RTM).
3. Luồng nghiệp vụ Happy Path (100% kịch bản thành công).
4. Ma trận giá trị biên và các ca kiểm thử ngoại lệ (Edge Cases & Error Scenarios).
5. File TestLink XML đính kèm sẵn sàng cho đội ngũ QA kiểm thử độc lập.

---

## 7. Tra Cứu Ảnh Mẫu Nghiệp Vụ Cục Bộ Qua CLI
Khi BA cần tìm ảnh mẫu sơ đồ Use Case, Activity hay Payment để đối chiếu cú pháp:
```bash
# Tra cứu ảnh sơ đồ use case
python scripts/knowledge.py image -q "use case include"

# Tra cứu ảnh luồng thanh toán hoặc rẽ nhánh
python scripts/knowledge.py image -q "sequence alt"
```
Mọi ảnh trả về đều có đường dẫn `assets/...` sẵn sàng copy hoặc nhúng trực tiếp vào hồ sơ đặc tả.
