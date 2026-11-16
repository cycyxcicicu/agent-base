# Kiểm Thử Đột Biến & Đặc Tính (Mutation & Property-Based Testing)

> **Loại: tham khảo.**
> Nguồn: tách từ istqb-whitebox-and-mutation.md mục 5, 6.
> Tiêu chuẩn: PIT (Pitest JVM), Claessen & Hughes (QuickCheck / jqwik).

## 1. Kiểm Thử Đột Biến (Mutation Testing & PIT)

Bản chất: *"Testing The Tests"* — Đo lường độ nhạy thực chất của bộ test suite bằng cách cố tình tiêm lỗi nhân tạo (*Mutants*) vào bytecode:
- **Conditional Boundary:** Đổi `>` thành `>=`, `<` thành `<=`.
- **Math Mutation:** Đổi `+` thành `-`, `*` thành `/`.
- **Negate Conditionals:** Đổi `if (x > y)` thành `if (!(x > y))`.
- **Return Value:** Đổi `return true` thành `return false`, hoặc trả về `null`.

### 1.1 Công Thức Chỉ Số Đột Biến (Mutation Score)
$$\text{Mutation Score} = \left( \frac{\text{Killed Mutants}}{\text{Total Mutants} - \text{Equivalent Mutants}} \right) \times 100\%$$

- **Killed Mutant:** Bộ test có ít nhất 1 bài test bị FAIL khi có đột biến $\rightarrow$ **Tốt** (Bộ test có khả năng phát hiện lỗi thực sự).
- **Surviving Mutant:** Code bị sửa sai mà bộ test vẫn PASS $\rightarrow$ **Xấu** (Bộ test có điểm mù, thiếu assert hoặc assert hình thức).
- **Equivalent Mutant:** Đột biến đổi cú pháp nhưng ngữ nghĩa toán học không đổi $\rightarrow$ Luôn sống sót (loại trừ khỏi mẫu).
- **Chuẩn công nghiệp:** Điểm Mutation Score đạt $\ge 85\%$ trên core domain logic là bảo chứng thép cho bộ test suite chất lượng.

## 2. Kiểm Thử Dựa Trên Đặc Tính (Property-Based Testing - PBT)

Khác với Unit test truyền thống chỉ kiểm tra vài ví dụ cố định, PBT kiểm thử dựa trên **Các Bất Biến Toán Học (Invariants)** trên hàng nghìn giá trị ngẫu nhiên sinh tự động.

### 2.1 Ba Bất Biến Kinh Điển (Common Invariants)
1. **Symmetric (Tính đối xứng / Round-trip):**
   $\text{decode}(\text{encode}(x)) == x$ (Serialization JSON, Nén/Giải nén, Mã hóa/Giải mã).
2. **Idempotent (Tính lũy thừa):**
   $f(f(x)) == f(x)$ (Sắp xếp danh sách, Format chuỗi, Xử lý webhook lặp).
3. **Metamorphic (Thuật toán tham chiếu):**
   Kết quả của giải thuật tối ưu song song phức tạp phải cho ra giá trị tương đương giải thuật tuần tự đơn giản.

### 2.2 Thuật Toán Co Cụm (Shrinking Algorithm)
Khi phát hiện input ngẫu nhiên làm sập hệ thống (ví dụ: mảng 1000 phần tử gây crash), framework PBT tự động co cụm input về **ca lỗi tối thiểu tuyệt đối** (ví dụ: mảng 1 phần tử mang giá trị `-1`), giúp định vị lỗi trong tích tắc.
