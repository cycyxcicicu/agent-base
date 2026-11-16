# Kiểm Thử Trạng Thái & Tổ Hợp Cặp (State Transition & Pairwise Testing)

> **Loại: tham khảo.**
> Nguồn: tách từ istqb-blackbox-techniques.md mục 7, 8, 9.
> Tiêu chuẩn: ISO/IEC/IEEE 29119-4, Tsun S. Chow (Chow's W-Method), NIST Pairwise Theorem.

## 1. Ma Trận Trực Giao & Kiểm Thử Cặp (Pairwise & Taguchi Arrays)

### 1.1 Định Lý NIST Về Tương Tác Tham Số
- **70% – 84%** lỗi phần mềm do tương tác giữa **2 tham số (Pairwise)** gây ra.
- **90% – 95%** lỗi do tương tác giữa **3 tham số (3-way)** gây ra.
$\rightarrow$ Áp dụng Pairwise giúp giảm số ca test từ hàng nghìn ca xuống vài chục ca mà vẫn bao phủ được hơn 80% rủi ro lỗi tương tác.

### 1.2 Bảng Tra Cứu Chuẩn Taguchi $L_N(s^k)$
- **$L_4(2^3)$:** 3 biến x 2 mức $\rightarrow$ **4 ca test** (thay vì $2^3 = 8$).
- **$L_8(2^7)$:** 7 biến x 2 mức $\rightarrow$ **8 ca test** (thay vì $2^7 = 128$).
- **$L_9(3^4)$:** 4 biến x 3 mức $\rightarrow$ **9 ca test** (thay vì $3^4 = 81$).
- **$L_{16}(2^{15})$:** 15 biến x 2 mức $\rightarrow$ **16 ca test** (thay vì 32.768 ca).
- **$L_{18}(2^1 \cdot 3^7)$:** 1 biến 2 mức và 7 biến 3 mức $\rightarrow$ **18 ca test** (thay vì 4.374 ca).

## 2. Kiểm Thử Chuyển Trạng Thái (State Transition Testing - STT)

Áp dụng cho mọi bài toán có vòng đời đối tượng (Entity Status Enum: `DRAFT`, `PENDING`, `APPROVED`, `SHIPPED`, `CANCELLED`).

### 2.1 Cấp Độ Bao Phủ Trạng Thái
1. **0-Switch Coverage (All Transitions):** Mọi chuyển đổi hợp lệ đơn lẻ phải được chạy qua ít nhất 1 lần (Đạt $100\%$ cạnh hợp lệ).
2. **1-Switch Coverage:** Mọi chuỗi 2 chuyển đổi liên tiếp $(T_a, T_b)$ phải được thực thi.
3. **Invalid Transitions Coverage (Robustness):** Thử kích hoạt sự kiện sai trên từng trạng thái (ví dụ: gửi lệnh `ShipOrder` khi đơn đang `Cancelled`) $\rightarrow$ Bắt buộc nhận lỗi HTTP 400 hoặc 409 Conflict.

### 2.2 Thuật Toán Chow's W-Method
Công thức sinh bộ test suite bảo đảm phát hiện 100% lỗi đầu ra, lỗi chuyển sai và lỗi thừa trạng thái:
$$T = P \cdot Z \cdot W$$
- $P$ (Transition Cover): Tập chuỗi input đi qua mọi trạng thái và kiểm tra mọi nhánh chuyển tiếp (duyệt BFS).
- $W$ (Characterization Set): Tập chuỗi input phân biệt hành vi đầu ra của bất kỳ cặp trạng thái nào.
- $Z$: Tập bù số lượng trạng thái phụ thuộc giả định trong mã nguồn.

## 3. Kiểm Thử Ca Sử Dụng (Use Case Scenario Testing)

Mỗi Ca Sử Dụng được phân rã thành:
- **Main Success Scenario (Happy Path):** Luồng hoàn hảo xuyên suốt từ đầu đến cuối.
- **Alternative Flows:** Các luồng rẽ nhánh hợp lệ.
- **Exception Flows:** Các luồng xử lý lỗi/ngoại lệ.
$$\text{Số ca} = 1 \text{ (Golden Thread)} + \sum (\text{Alternative}) + \sum (\text{Exception})$$
