# Toàn Thư Kỹ Thuật Kiểm Thử Hộp Đen (ISTQB Black-Box Test Design)

> **Loại: tham khảo.** Tổng hợp các kỹ thuật thiết kế kiểm thử hộp đen theo chuẩn ISO/IEC/IEEE 29119-4 và ISTQB Advanced Level Test Analyst (CTAL-TA).
> Kiến trúc Hub: File tổng quan điều phối + 3 tệp vệ tinh chuyên sâu.

## 1. Bản Đồ Kỹ Thuật Kiểm Thử Hộp Đen

Kỹ thuật kiểm thử hộp đen tập trung vào hành vi đầu vào/ra của phần mềm mà không cần soi cấu trúc mã nguồn bên trong:

```
                          KIỂM THỬ HỘP ĐEN (BLACK-BOX)
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
  [1. DỮ LIỆU & BIÊN]          [2. LOGIC & TỔ HỢP]         [3. TRẠNG THÁI & LUỒNG]
  • Phân vùng tương đương (EP) • Bảng quyết định (DTT)      • Chuyển trạng thái (STT)
  • Phân tích giá trị biên     • Biểu đồ Nhân - Quả         • Thuật toán Chow's W
  • Kiểm thử miền (Domain)     • Cây phân loại (CTM)        • Ma trận Taguchi Pairwise
                               • Rút gọn Don't Care (-)     • Kịch bản Use Case
```

## 2. Chỉ Mục 3 Tệp Vệ Tinh Chuyên Sâu

Để tra cứu chi tiết công thức toán học và hướng dẫn thực thi, Agent mở các tệp vệ tinh tương ứng:

| Tệp vệ tinh | Kỹ thuật bao phủ | Khi nào tra cứu |
|---|---|---|
| **[istqb-blackbox-ep-bva.md](istqb-blackbox-ep-bva.md)** | • Phân vùng tương đương (Weak/Strong, Normal/Robust)<br>• Giá trị biên BVA (2-point chuẩn vs 3-point Copeland)<br>• Kiểm thử miền Domain Testing (ON/OFF/IN/OUT, Closed vs Open) | Bài toán có dải số, độ dài chuỗi, ngày tháng, tiền tệ, ngưỡng chặn |
| **[istqb-blackbox-decision-table.md](istqb-blackbox-decision-table.md)** | • Bảng quyết định (DTT) 4 góc chuẩn mực<br>• Thuật toán rút gọn Don't Care (`-`)<br>• Biểu đồ Nhân - Quả & 5 ràng buộc logic (E, I, O, R, M)<br>• Cây phân loại Daimler-Benz (CTM) | Bài toán có nhiều nhánh `if-else` lồng nhau, bảng giá, voucher, ma trận chiết khấu |
| **[istqb-blackbox-state-and-pairwise.md](istqb-blackbox-state-and-pairwise.md)** | • Ma trận trực giao Pairwise & Bảng chuẩn Taguchi $L_4..L_{18}$<br>• Kiểm thử chuyển trạng thái FSM (0-switch, 1-switch, Invalid edge)<br>• Thuật toán Chow's W ($T = P \cdot Z \cdot W$)<br>• Kịch bản Use Case (Golden Thread, Alternative, Exception) | Màn hình tìm kiếm nhiều dropdown bộ lọc, thực thể có vòng đời status Enum |
