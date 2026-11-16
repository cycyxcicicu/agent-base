# Toàn Thư Kỹ Thuật Kiểm Thử Hộp Trắng & Đột Biến (White-Box & Mutation Testing)

> **Loại: tham khảo.** Tổng quan các kỹ thuật kiểm thử hộp trắng, đo lường cấu trúc và phân tích đột biến mã nguồn.
> Tiêu chuẩn: Thomas J. McCabe (Cyclomatic Complexity), DO-178C (MC/DC), ISO 26262, PIT JVM.

## 1. Bản Đồ Kỹ Thuật Kiểm Thử Hộp Trắng

Kiểm thử hộp trắng đi sâu vào cấu trúc mã nguồn, đo lường độ bao phủ dòng lệnh, nhánh rẽ và kiểm chứng độ nhạy của bộ test suite:

```
                     KIỂM THỬ HỘP TRẮNG (WHITE-BOX)
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
  [1. CẤU TRÚC & LUỒNG ĐIỀU KHIỂN]                   [2. ĐỘT BIẾN & ĐẶC TÍNH]
  • Độ phức tạp chu trình McCabe V(G)                • Kiểm thử đột biến (PIT)
  • Basis Path Testing                               • Diệt Mutants & Mutation Score ≥ 85%
  • Độ bao phủ câu lệnh, nhánh (C0, C1)              • Property-Based Testing (PBT)
  • Chuẩn hàng không & ô tô MC/DC (n + 1 ca)         • Bất biến toán học & Shrinking
  • Dị thường dòng dữ liệu (UR, DU, DD)
```

## 2. Chỉ Mục 2 Tệp Vệ Tinh Chuyên Sâu

Để tra cứu chi tiết công thức toán học và hướng dẫn thực thi, Agent mở các tệp vệ tinh tương ứng:

| Tệp vệ tinh | Kỹ thuật bao phủ | Khi nào tra cứu |
|---|---|---|
| **[istqb-whitebox-control-flow.md](istqb-whitebox-control-flow.md)** | • Độ phức tạp chu trình McCabe $V(G) = E - N + 2P$<br>• Ngưỡng rủi ro SEI/CMMI ($V(G) > 20$ bắt buộc refactor)<br>• Cấp độ bao phủ Statement (C0), Branch (C1), MCC<br>• Chuẩn an toàn sinh mạng MC/DC ($n+1$ ca test)<br>• Phân tích dòng dữ liệu Data Flow (bẫy UR, DU, DD) | Kiểm thử tầng Unit/Component, đo lường độ bao phủ nhánh, refactor hàm phức tạp |
| **[istqb-whitebox-mutation-testing.md](istqb-whitebox-mutation-testing.md)** | • Kiểm thử đột biến Mutation Testing (PIT Bytecode)<br>• Các toán tử đột biến (Boundary, Math, Negate, Return)<br>• Công thức tính Mutation Score & ngưỡng chuẩn $\ge 85\%$<br>• Property-Based Testing (PBT / jqwik)<br>• 3 Bất biến kinh điển (Symmetric, Idempotent, Metamorphic)<br>• Thuật toán co cụm lỗi Shrinking Algorithm | Đánh giá độ nhạy thực chất của Unit test suite, kiểm thử thuật toán và parser |
