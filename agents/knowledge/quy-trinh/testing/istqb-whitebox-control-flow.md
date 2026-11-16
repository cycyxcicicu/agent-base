# Kiểm Thử Hộp Trắng & Luồng Điều Khiển (White-Box Control Flow Testing)

> **Loại: tham khảo.**
> Nguồn: tách từ istqb-whitebox-and-mutation.md mục 1, 2, 3, 4.
> Tiêu chuẩn: Thomas J. McCabe (Cyclomatic Complexity), DO-178C (MC/DC), ISO 26262.

## 1. Độ Phức Tạp Chu Trình McCabe (Cyclomatic Complexity - CC)

Đo lường số lượng đường dẫn độc lập tuyến tính qua mã nguồn trên Đồ thị Dòng Điều Khiển (CFG):
$$V(G) = E - N + 2P = \text{Số điểm quyết định (if, while, for, case)} + 1$$
- $V(G)$ chính là **Số ca test tối thiểu** cần để đạt 100% Branch Coverage (Basis Path Testing).
- **Ngưỡng rủi ro theo chuẩn SEI/CMMI:**
  - $V(G) \le 10$: Hàm đơn giản, rủi ro thấp.
  - $11 \le V(G) \le 20$: Phức tạp trung bình, cần tối thiểu 15 test cases.
  - $V(G) > 20$: Rủi ro cực cao, khó bảo trì $\rightarrow$ **Bắt buộc refactor tách hàm trước khi test**.

## 2. Các Cấp Độ Bao Phủ Luồng Điều Khiển (Control Flow)

1. **Statement Coverage (C0):** Tỷ lệ dòng lệnh được thực thi. Nhược điểm: dễ ảo tưởng an toàn, bỏ sót nhánh `else` thiếu.
2. **Branch / Decision Coverage (C1):** Tỷ lệ nhánh True/False được duyệt. Mọi dự án nghiêm túc bắt buộc đạt $\ge 80\%$.
3. **Condition Coverage:** Mỗi điều kiện con trong biểu thức phức hợp phải nhận True ít nhất 1 lần và False ít nhất 1 lần.
4. **Multiple Condition Coverage (MCC):** Vét cạn toàn bộ $2^n$ tổ hợp chân trị $\rightarrow$ Chi phí bùng nổ tổ hợp lớn.

## 3. Tiêu Chuẩn Bao Phủ Điều Kiện Sửa Đổi (MC/DC Coverage)

Chuẩn kiểm thử bắt buộc cho phần mềm an toàn cao (Hàng không DO-178C Level A, Ô tô ISO 26262 ASIL D):
- Mỗi quyết định phải thử qua đủ kết quả `True` và `False`.
- Mỗi điều kiện con phải chứng minh **ảnh hưởng độc lập** tới kết quả quyết định (giữ nguyên các điều kiện khác, chỉ lật giá trị điều kiện đang xét).
- **Công thức số ca test:** Cho biểu thức có $n$ điều kiện con:
  $$\text{Số ca } (MC/DC) = n + 1$$
  *(Tối ưu tuyến tính $n+1$ thay vì $2^n$ ca của MCC mà vẫn chứng minh được tính độc lập).*

## 4. Kiểm Thử Dòng Dữ Liệu (Data Flow Testing)

Kiểm tra vòng đời biến: Khởi tạo (Definition - `d`), Sử dụng (Use - `u`), Hủy bỏ (Kill - `k`).
- **c-use:** Dùng trong phép tính/gán (`y = x + 1`).
- **p-use:** Dùng trong điều kiện rẽ nhánh (`if (x > 0)`).

### Ba Dị Thường Dòng Dữ Liệu Cần Bắt (Anomalies):
1. **UR (Use before Defined):** Dùng biến trước khi khởi tạo $\rightarrow$ Gây lỗi NullPointerException hoặc dữ liệu rác.
2. **DU (Defined then Defined without Use):** Gán giá trị nhưng bị ghi đè ngay mà chưa từng đọc $\rightarrow$ Logic thừa hoặc lỗi copy-paste.
3. **DD (Defined and never used):** Khởi tạo nhưng không dùng $\rightarrow$ Rác bộ nhớ.
