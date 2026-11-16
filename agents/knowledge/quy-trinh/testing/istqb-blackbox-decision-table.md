# Bảng Quyết Định & Sơ Đồ Nhân - Quả (Decision Table & Cause-Effect)

> **Loại: tham khảo.**
> Nguồn: tách từ istqb-blackbox-techniques.md mục 4, 5, 6.
> Tiêu chuẩn: ISO/IEC/IEEE 29119-4, ISTQB CTAL-TA, Matthias Grochtmann (CTM).

## 1. Bảng Quyết Định (Decision Table Testing - DTT)

Đặc trị các bài toán chứa nhiều điều kiện logic `if-else` lồng nhau, bảng giá, voucher, chính sách chiết khấu.

### 1.1 Cấu Trúc 4 Phần Chuẩn Mực
- **Condition Stub:** Danh sách các điều kiện đầu vào (Boolean hoặc Enum).
- **Condition Entries:** Các tổ hợp giá trị khả dĩ (True / False).
- **Action Stub:** Danh sách các hành động hệ thống kích hoạt.
- **Action Entries:** Kết quả hành động tương ứng với mỗi tổ hợp.

### 1.2 Thuật Toán Rút Gọn Don't Care (`-`)
- Số quy tắc thô ban đầu: $2^n$ (với $n$ điều kiện nhị phân).
- Hai quy tắc $R_1$ và $R_2$ được gộp thành 1 cột khi:
  1. Mọi Hành động (Actions) của $R_1$ và $R_2$ giống hệt nhau.
  2. Các Điều kiện giống nhau ở $n-1$ dòng, chỉ lệch nhau ở đúng 1 điều kiện $C_k$ ($R_1$ True, $R_2$ False).
  3. Lúc này, điều kiện $C_k$ được thay thế bằng ký hiệu **Don't Care (`-`)**.
- Sau khi rút gọn, số ca test tối ưu giảm từ $2^n$ xuống còn $\le n + 2$.

## 2. Biểu Đồ Nhân - Quả & 5 Ràng Buộc Logic (Cause-Effect Graphing)

Chuyển đổi đặc tả ngôn ngữ tự nhiên thành mạng logic Boolean giữa Nguyên nhân (Causes) và Kết quả (Effects).
Năm loại ràng buộc logic chuẩn mực để loại trừ kịch bản vô nghĩa:
1. **E – Exclusive (Loại trừ lẫn nhau):** Tối đa 1 nguyên nhân được đúng (Có thể cùng Sai, cấm cùng Đúng).
2. **I – Inclusive (Bao hàm):** Ít nhất 1 nguyên nhân phải đúng (Cấm cùng Sai).
3. **O – One and Only One (Một và chỉ một):** Đúng duy nhất 1 nguyên nhân được đúng (Cấm cùng Đúng, cấm cùng Sai).
4. **R – Requires (Đòi hỏi phụ thuộc):** Nếu $C_1$ Đúng thì $C_2$ bắt buộc phải Đúng.
5. **M – Masking (Che giấu / Gạt bỏ):** Nếu Kết quả $E_1$ xảy ra thì Kết quả $E_2$ bắt buộc bị vô hiệu hóa (False).

## 3. Phương Pháp Cây Phân Loại (Classification Tree Method - CTM)

Kỹ thuật đồ họa (Daimler-Benz 1993) trực quan hóa phân vùng và tổ hợp:
1. **Gốc (Root):** Hệ thống hoặc chức năng cần test.
2. **Nhánh (Classifications):** Các khía cạnh kiểm thử độc lập (ví dụ: Loại khách, Phương thức giao hàng, Giá trị đơn).
3. **Lá (Classes):** Các phân vùng giá trị rời rạc không giao nhau.
4. **Bảng Tổ Hợp Dưới Chân Cây:** Mỗi dòng là 1 kịch bản test, tester tích chọn đúng 1 Lớp cho mỗi Khía cạnh.
