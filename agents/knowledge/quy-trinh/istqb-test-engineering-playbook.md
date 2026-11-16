# Cẩm Nang Kỹ Nghệ Thiết Kế & Định Lượng Kiểm Thử (ISTQB Test Engineering Hub)

> **Loại: tham khảo.** Cửa ngõ điều phối và chuẩn hóa kỹ thuật kiểm thử theo ISTQB, ISO/IEC/IEEE 29119.
> Kiến trúc Hub-and-Spoke: 1 file Lõi điều phối + các tệp vệ tinh chuyên sâu.

## 1. Bảy Nguyên Lý Kiểm Thử Cốt Lõi (ISTQB)

1. **Chứng minh sự hiện diện của lỗi:** Test chỉ giảm thiểu rủi ro, không chứng minh phần mềm hết lỗi.
2. **Kiểm thử kiệt quệ là bất khả thi:** Bắt buộc dùng toán học và rủi ro để chọn tập mẫu đại diện tối ưu.
3. **Kiểm thử càng sớm càng tốt (Early Testing):** Bắt lỗi tại pha Yêu cầu/Thiết kế rẻ hơn gấp 100x–1000x so với Prod.
4. **Sự tập trung của lỗi (Pareto 80/20):** 80% lỗi hệ thống tập trung ở 20% module phức tạp nhất.
5. **Nghịch lý thuốc trừ sâu:** Chạy lặp lại cùng bộ test cũ sẽ không tìm được lỗi mới $\rightarrow$ Cần test đột biến.
6. **Kiểm thử phụ thuộc ngữ cảnh:** Hệ thống tài chính/y tế đòi hỏi kỹ thuật khác biệt so với web nội bộ.
7. **Ảo tưởng về sự vắng bóng lỗi:** Phần mềm không lỗi code nhưng không đúng nhu cầu người dùng vẫn thất bại.

## 2. Mô Hình 8 Lát Cắt Kỹ Thuật Nguyên Tử (Test Facets)

Agent bóc tách mọi tính năng thành 8 lát cắt nguyên tử để định tuyến kỹ thuật:
1. **Dữ liệu (Data):** Input, kiểu dữ liệu, ngưỡng biên, format ngày/tiền.
2. **Logic (Rules):** Nhánh IF-ELSE lồng nhau, công thức tính toán, voucher, bảng giá.
3. **Trạng thái (State):** Vòng đời Entity, enum status, thứ tự bước quy trình.
4. **Quyền hạn (Auth):** Role, Tenant, sở hữu ID (chống leo quyền IDOR/BOLA).
5. **Đồng thời (Concurrency):** Tranh chấp tài nguyên, race condition, trừ kho flash sale.
6. **Giao tiếp ngoài (Comm):** Cổng thanh toán, Webhook, API bên thứ 3, rớt mạng.
7. **Khối lượng (Volume):** Dữ liệu rỗng (0 dòng), 1 dòng, 100k dòng, batch job, rollback.
8. **Thời gian (Time):** Timezone, năm nhuận, TTL cache, timeout kết nối, cron schedule.

## 3. Chỉ Mục Các Tệp Vệ Tinh Chuyên Sâu

| Chủ đề | Nội dung chính | Đường dẫn tệp vệ tinh |
|---|---|---|
| **Định tuyến kỹ thuật** | Bảng Heuristic & Triggers tự động từ code | `istqb-playbook-routing-matrix.md` |
| **Định lượng số ca test** | Công thức Dynamic Sizing hướng bài toán | `istqb-playbook-test-sizing.md` |
| **Thẩm định Gate 2** | Ma trận truy vết RTM & 3 luật cứng duyệt test | `istqb-playbook-gate2-justification.md` |
| **Kỹ thuật Hộp đen** | Chi tiết EP, BVA, Decision Table, State, Pairwise | `testing/istqb-blackbox-techniques.md` |
| **Kỹ thuật Hộp trắng** | McCabe Cyclomatic, MC/DC, PIT Mutation Testing | `testing/istqb-whitebox-and-mutation.md` |
| **Ước lượng & Rủi ro** | TPA, PERT 3-điểm, Ma trận rủi ro PRISMA | `testing/test-estimation-and-risk.md` |
| **Heuristics & Oracles** | FEW HICCUPPS, SFDIPOT, OWASP API Top 10 | `testing/test-heuristics-and-oracles.md` |
| **Quản trị Test Data** | Chiến lược Mock, Fixtures, Anonymization | `testing/test-data-management.md` |
