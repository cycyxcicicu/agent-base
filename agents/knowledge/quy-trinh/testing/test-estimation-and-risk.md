# Ước Lượng Quy Mô & Quản Trị Rủi Ro Kiểm Thử (Estimation & Risk Management)

> **Loại: tham khảo.** Tổng quan các phương pháp toán học ước lượng quy mô kiểm thử, mô hình rủi ro PRISMA và mô hình hiệu năng.
> Tiêu chuẩn: ISTQB CTAL-TM, Erik van Veenendaal (TPA), Rex Black (PRISMA), Little's Law, Neil Gunther (USL).

## 1. Bản Đồ Quản Trị Rủi Ro & Ước Lượng Kiểm Thử

Kiểm thử chuyên nghiệp không dựa trên phỏng đoán cảm tính mà dựa trên mô hình toán học lượng hóa:

```
                  ƯỚC LƯỢNG & QUẢN TRỊ RỦI RO KIỂM THỬ
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         ▼                                                     ▼
  [1. ĐỊNH LƯỢNG QUY MÔ & CÔNG SỨC]              [2. RỦI RO & HIỆU NĂNG HỆ THỐNG]
  • Phân tích điểm kiểm thử (TPA)                • Ma trận rủi ro sản phẩm PRISMA
  • Chuyển đổi Function Points sang Test Points  • 4 vùng rủi ro (Chí mạng, Tiềm ẩn, Vặt, Thấp)
  • Phân phối xác suất 3 điểm Beta PERT          • Định luật Little (L = λW) trong xếp hàng
  • Khoảng tin cậy thống kê (68%, 95%, 99.7%)    • Universal Scalability Law (USL)
  • Cảnh báo yêu cầu mơ hồ (σ/E > 0.25)          • 5 loại kiểm thử tải (Load, Stress, Spike...)
```

## 2. Chỉ Mục 2 Tệp Vệ Tinh Chuyên Sâu

Để tra cứu chi tiết công thức toán học và bảng ma trận, Agent mở các tệp vệ tinh tương ứng:

| Tệp vệ tinh | Kỹ thuật bao phủ | Khi nào tra cứu |
|---|---|---|
| **[test-estimation-tpa-pert.md](test-estimation-tpa-pert.md)** | • Phân tích điểm kiểm thử TPA: hệ số phức tạp $C_i$, rủi ro nghiệp vụ $R_i$, môi trường $EF$<br>• Quy đổi Test Points ra giờ công kiểm thử (Test Effort Hours)<br>• Mô hình phân phối xác suất 3 điểm PERT ($E, \sigma, \sigma^2$)<br>• Chỉ số cảnh báo yêu cầu mơ hồ $\sigma / E > 0.25$ | Khi lập Test Plan, ước lượng giờ công kiểm thử cho Sprint/Dự án |
| **[test-risk-prisma-performance.md](test-risk-prisma-performance.md)** | • Ma trận rủi ro PRISMA & PRAM: $\text{Risk} = \text{Likelihood} \times \text{Impact}$<br>• Bốn vùng rủi ro: Chí mạng (Vùng 1), Tiềm ẩn (Vùng 2), Lỗi vặt (Vùng 3), Thấp (Vùng 4)<br>• Mô hình hàng đợi Little's Law ($L = \lambda W$) tính toán Target TPS<br>• Định luật mở rộng Neil Gunther (USL) chống sụt giảm do tranh chấp lock<br>• 5 loại kiểm thử tải (Load, Stress, Spike, Soak, Breakpoint) | Khi phân bổ nguồn lực kiểm thử theo rủi ro hoặc thiết kế kịch bản kiểm thử tải K6 |
