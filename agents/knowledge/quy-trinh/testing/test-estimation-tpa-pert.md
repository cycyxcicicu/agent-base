# Ước Lượng Quy Mô & Giờ Công Kiểm Thử (TPA & PERT 3-Point)

> **Loại: tham khảo.**
> Nguồn: tách từ test-estimation-and-risk.md mục 1, 2.
> Tiêu chuẩn: ISTQB CTAL-TM, Erik van Veenendaal (TPA), Phân phối Beta PERT.

## 1. Phân Tích Điểm Kiểm Thử (Test Point Analysis - TPA)

Phương pháp đo lường quy mô kiểm thử hộp đen chuẩn hóa của Hà Lan, chuyển đổi từ Function Points (FP) sang Test Points (TP):
$$\text{Tổng số Test Points } (TP) = \sum_{i=1}^{n} (\text{Function Point}_i \times C_i \times R_i) \times EF$$

### 1.1 Các Hệ Số Thành Phần
1. **Hệ Số Độ Phức Tạp Chức Năng ($C_i$):**
   - Đơn giản ($< 3$ input/màn hình, không có công thức tính): Hệ số $0.8$
   - Trung bình (4–7 input, CRUD tiêu chuẩn): Hệ số $1.0$
   - Phức tạp ($> 7$ input, tính toán đa tầng, workflow): Hệ số $1.4$
2. **Hệ Số Rủi Ro Nghiệp Vụ ($R_i$):**
   - Thấp (Giao diện hiển thị tĩnh, báo cáo phụ): Hệ số $0.7$
   - Vừa (CRUD dữ liệu nghiệp vụ thông thường): Hệ số $1.0$
   - Cao (Thanh toán tài chính, Khóa tồn kho, Token bảo mật): Hệ số $1.6$
3. **Hệ Số Môi Trường ($EF$):** Độ ổn định môi trường và kinh nghiệm đội ngũ ($0.8 \le EF \le 1.3$).

### 1.2 Quy Đổi Ra Giờ Công (Test Effort)
$$\text{Thời gian test (giờ)} = TP \times \text{Năng suất (0.5 – 1.5 giờ/TP)}$$

## 2. Mô Hình Phân Phối Xác Suất 3 Điểm PERT

Xử lý sự bất định và độ trễ trong các dự án phần mềm theo phân phối xác suất Beta:
$$\text{Quy mô / Giờ công kỳ vọng } (E) = \frac{O + 4M + P}{6}$$
$$\text{Độ lệch chuẩn rủi ro } (\sigma) = \frac{P - O}{6}, \quad \text{Phương sai } (V) = \sigma^2 = \left(\frac{P - O}{6}\right)^2$$
- $O$ (Optimistic): Kịch bản lạc quan nhất (mọi thứ rõ ràng, không có bẫy ẩn).
- $M$ (Most Likely): Kịch bản thực tế có xác suất xảy ra cao nhất.
- $P$ (Pessimistic): Kịch bản bi quan nhất (phát sinh nhiều bug, môi trường lỗi).

### 2.1 Khoảng Tin Cậy Thống Kê
- **Khoảng $68.27\%$:** $E \pm \sigma$
- **Khoảng $95.45\%$:** $E \pm 2\sigma$
- **Khoảng $99.73\%$:** $E \pm 3\sigma$

### 2.2 Chỉ Số Cảnh Báo Rủi Ro (Ambiguity Alert)
$$\text{Nếu } \frac{\sigma}{E} > 0.25 \implies \text{Yêu cầu quá mơ hồ, bắt buộc chất vấn BA/User trước khi chốt Test Plan.}$$
