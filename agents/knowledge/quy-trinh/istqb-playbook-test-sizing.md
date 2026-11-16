# Định Lượng Số Ca Test Hướng Bài Toán (Problem-Driven Test Sizing)

> **Loại: tham khảo.**
> Nguồn: tách từ istqb-test-engineering-playbook.md mục VI.
> Quy tắc định lượng số lượng test case dựa trên toán học và cấu trúc bài toán, bài trừ hạn ngạch võ đoán.

## 1. Cấm Tuyệt Đối Áp Hạn Ngạch Võ Đoán (Anti-Pattern)

Không có quy chuẩn quốc tế nào quy định cứng *"task vừa phải 8-15 test"* hay *"task lớn phải 20-40 test"*.
- Ép hạn ngạch cố định dẫn đến hai hệ lụy nghiêm trọng:
  1. *Lạm phát test rác:* Viết các ca kiểm thử trùng lặp phân vùng chỉ để cho "đủ số lượng KPI".
  2. *Bỏ sót rủi ro cốt tử:* Với bài toán phức tạp nhiều trạng thái, hạn ngạch cứng làm bỏ lọt các nhánh ngoại lệ nguy hiểm.

## 2. Công Thức Định Lượng Hướng Bài Toán (Dynamic Sizing)

Số lượng Test Case tối ưu ($N_{total}$) là hàm số phụ thuộc trực tiếp vào các Lát cắt bài toán ($F_k$):

$$N_{total} = \sum_{k=1}^{m} N(F_k) - \text{Overlap}$$

Trong đó, số ca test tối thiểu cho từng lát cắt được tính theo chuẩn ISTQB:
- **Dữ liệu biên ($F_{data}$):** $N = 2 \times (\text{Số biên}) + 1$ (kỹ thuật 2-point BVA).
- **Quy tắc logic ($F_{logic}$):** $N = 2^k$ (rút gọn theo bảng quyết định Don't Care).
- **Tổ hợp bộ lọc ($F_{form}$):** $N = \text{Cỡ ma trận trực giao Pairwise}$ (thay vì nhân toàn bộ tổ hợp).
- **Vòng đời trạng thái ($F_{state}$):** $N = (\text{Số chuyển đổi hợp lệ}) + (\text{Số cạnh lậu trái phép bất hợp lệ})$.
- **Phân quyền ($F_{auth}$):** $N = (\text{Số Role}) \times (\text{Số Endpoint}) \text{ theo ma trận CRUD}$.
- **Giao tiếp ngoài ($F_{comm}$):** $N = 3$ (1 Thành công + 1 Timeout/Mất mạng + 1 Gửi lặp lại Idempotent).

## 3. Ba Tiêu Chuẩn Nghiệm Thu Bộ Test (Minimal Spanning Test Suite)

Một bộ Test Case đạt chuẩn khi và chỉ khi thỏa mãn đủ 3 tiêu chuẩn toán học:
1. **Tính Cần Thiết (Necessity):** Mọi test case đều bảo vệ 1 giá trị biên, 1 phân vùng hoặc 1 quy tắc cụ thể (xóa đi là mất độ bao phủ).
2. **Tính Đầy Đủ (Sufficiency):** Không còn bất kỳ nhánh logic, giá trị biên hoặc chuyển đổi trạng thái nào trong đặc tả bị bỏ sót.
3. **Tính Độc Lập (Orthogonality):** Cấm 2 test case cùng kiểm thử 1 phân vùng với cùng một kịch bản logic (chống trùng lặp lãng phí).
