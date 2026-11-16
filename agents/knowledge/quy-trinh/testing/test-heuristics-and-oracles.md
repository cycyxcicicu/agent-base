# Heuristics Kiểm Thử, Bẫy Lỗi & Oracles (Exploratory Testing Hub)

> **Loại: tham khảo.** Tổng quan các phương pháp heuristic kiểm thử thăm dò, nhận diện lỗi Oracle và danh mục bẫy lỗi kinh nghiệm.
> Tiêu chuẩn: James Bach (HTSM / SFDIPOT), Elisabeth Hendrickson (Explore It!), OWASP API Top 10, WCAG 2.1 AA.

## 1. Bản Đồ Heuristics & Oracles Kiểm Thử

Kiểm thử thăm dò chuyên nghiệp được dẫn dắt bởi các mô hình heuristic tư duy có kỷ luật:

```
                     HEURISTICS & ORACLES KIỂM THỬ
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
  [1. KHÁM PHÁ & NHẬN DIỆN LỖI]                       [2. BẪY LỖI & BẢO MẬT]
  • Mô hình quét sản phẩm SFDIPOT                    • Danh mục bẫy lỗi Defect Taxonomy
  • Heuristic tấn công biến số (Count 0, 1, Many)    • Tràn số, sai số float, múi giờ
  • Heuristic Goldilocks (Quá nhỏ, Vừa, Quá lớn)     • OWASP API Security Top 10
  • Bộ 11 Oracles nhận diện bug FEW HICCUPPS         • Leo quyền BOLA / BFLA, Mass Assignment
  • Kiểm tra tính nhất quán và quy định pháp lý      • Responsive UI, WCAG 2.1 AA, Console Error = 0
```

## 2. Chỉ Mục 2 Tệp Vệ Tinh Chuyên Sâu

Để tra cứu chi tiết danh mục câu hỏi và kịch bản tấn công, Agent mở các tệp vệ tinh tương ứng:

| Tệp vệ tinh | Kỹ thuật bao phủ | Khi nào tra cứu |
|---|---|---|
| **[test-heuristics-few-hiccups.md](test-heuristics-few-hiccups.md)** | • Mô hình phân tích sản phẩm 7 chiều SFDIPOT (San Francisco Depot)<br>• Heuristic tấn công biến số: Count 0-1-Many, Quy tắc Goldilocks, Xáo trộn trình tự<br>• Bộ 11 tiêu chí Oracle nhận diện bug FEW HICCUPPS (Familiarity, World, History, Claims, Statutes...) | Khi phân tích bài toán mới, tìm bẫy logic tiềm ẩn hoặc kiểm thử thăm dò (Exploratory Testing) |
| **[test-heuristics-owasp-security.md](test-heuristics-owasp-security.md)** | • Bảng tra cứu bẫy lỗi kinh nghiệm: Ký tự dị, SQLi, XSS, Overflow, Idempotency, Concurrency, Timezone<br>• Heuristic bảo mật OWASP API: BOLA, BFLA, Mass Assignment, Rate Limit<br>• Kiểm thử trải nghiệm UI/UX: Ma trận Viewports (Mobile/Tablet/Desktop), WCAG 2.1 AA, Console Error = 0 | Khi thiết kế test case bảo mật API, kiểm thử giao diện frontend và kiểm tra lỗi rò rỉ dữ liệu |
