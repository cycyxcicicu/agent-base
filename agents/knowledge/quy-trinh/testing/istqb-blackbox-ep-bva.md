# Phân Vùng Tương Đương & Phân Tích Giá Trị Biên (EP, BVA & Domain Testing)

> **Loại: tham khảo.**
> Nguồn: tách từ istqb-blackbox-techniques.md mục 1, 2, 3.
> Tiêu chuẩn: ISO/IEC/IEEE 29119-4, ISTQB CTAL-TA, Lee Copeland, Cem Kaner.

## 1. Phân Vùng Tương Đương (Equivalence Partitioning - EP)

### 1.1 Bản Chất
Chia không gian dữ liệu đầu vào/ra thành các lớp tương đương. Các phần tử trong cùng một lớp được giả định kích hoạt cùng nhánh xử lý trong mã nguồn. Chọn duy nhất 1 giá trị đại diện cho mỗi lớp.

### 1.2 Bốn Biến Thể Của Lee Copeland (Cho $n$ biến)
1. **Weak Normal:** Mỗi phân vùng hợp lệ xuất hiện ít nhất 1 lần trong test suite: $\text{Số ca} = \max(V_i)$.
2. **Strong Normal:** Tích Descartes mọi tổ hợp hợp lệ: $\text{Số ca} = \prod V_i$.
3. **Weak Robust:** Bao phủ mọi phân vùng hợp lệ, thử từng phân vùng lỗi đơn lập: $\text{Số ca} = \max(V_i) + \sum I_i$.
4. **Strong Robust:** Tích Descartes toàn bộ các phân vùng: $\text{Số ca} = \prod (V_i + I_i)$.

## 2. Phân Tích Giá Trị Biên (Boundary Value Analysis - BVA)

Lỗi phần mềm tập trung cao nhất tại ranh giới chuyển tiếp (Off-by-one errors: dùng sai $>$ thay vì $\ge$, tràn số, lệch chỉ mục mảng `array[0..n]`).

### 2.1 So Sánh 2-Point BVA vs 3-Point BVA
Cho khoảng giá trị hợp lệ $[A, B]$:

| Tiêu chí | 2-Point BVA (Chuẩn ISTQB) | 3-Point BVA (Lee Copeland) |
|---|---|---|
| **Các điểm kiểm tra** | $\{\text{Tại biên}, \text{Sát ngoài biên}\}$ | $\{\text{Sát trong}, \text{Tại biên}, \text{Sát ngoài}\}$ |
| **Tập điểm $[A, B]$** | $\{A-1, A, B, B+1\}$ | $\{A-1, A, A+1, \text{Nominal}, B-1, B, B+1\}$ |
| **Số ca cho 1 biến** | **4 ca** | **6 ca** (+ 1 nominal) |
| **Áp dụng** | Web app, CRUD thông thường | Hệ thống hàng không, y tế, tài chính lõi |

### 2.2 Công Thức Cho $n$ Biến Đầu Vào
1. **Standard BVA:** $4n + 1$ (gồm $min, min^+, nominal, max^-, max$).
2. **Robust BVA:** $6n + 1$ (thêm $min^-, max^+$).
3. **Worst-Case BVA:** $5^n$.
4. **Worst-Case Robust BVA:** $7^n$.

## 3. Kiểm Thử Miền Chuyên Sâu (Domain Testing)

Xác định 4 điểm kiểm thử cốt tử trên mỗi đường biên:
- **ON Point:** Điểm nằm chính xác trên đường biên.
- **OFF Point:** Điểm sát nhất với ON, nằm ở phía bên kia đường biên.
- **IN Point / OUT Point:** Nằm an toàn bên trong / ngoài miền hợp lệ.

### Quy Tắc Vàng Giữa Biên Mở và Biên Đóng:
| Loại biên | Toán tử trong code | Điểm ON | Điểm OFF | Quy tắc ghi nhớ |
|---|---|---|---|---|
| **Biên Đóng** | $\le$ hoặc $\ge$ | Trong miền hợp lệ | Ngoài miền hợp lệ | **Closed OFF Outside** |
| **Biên Mở** | $<$ hoặc $>$ | Ngoài miền hợp lệ | Trong miền hợp lệ | **Open OFF Inside** |

- *Ví dụ:*
  - Biên đóng `Tuổi <= 60`: $\text{ON} = 60 \text{ (Hợp lệ)}, \text{OFF} = 61 \text{ (Chặn)}$.
  - Biên mở `Tuổi < 60`: $\text{ON} = 60 \text{ (Chặn)}, \text{OFF} = 59 \text{ (Hợp lệ)}$.
