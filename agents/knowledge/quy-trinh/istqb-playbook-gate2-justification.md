# Thẩm Định Kỹ Thuật Test Tại Cổng Gate 2 (Gate 2 Test Justification)

> **Loại: tham khảo.**
> Nguồn: tách từ istqb-test-engineering-playbook.md mục VII.
> Quy tắc thẩm định ma trận truy vết RTM và tiêu chuẩn nghiệm thu kịch bản kiểm thử trước khi code.

## 1. Ma Trận Truy Vết RTM ("Ma Trận Tick-Tick")

Mọi bộ hồ sơ kiểm thử bàn giao tại Gate 2 bắt buộc phải có bảng RTM đối chiếu 2 chiều:

| Mã Yêu Cầu (SRS/BR) | Quy Tắc Nghiệp Vụ | Lát Cắt | Kỹ Thuật Áp Dụng | Mã Test Case | Kết Quả Mong Đợi (Oracle) | Đánh Dấu |
|---|---|---|---|---|---|:---:|
| **BR-ORD-01** | Hạn mức COD tối đa 50 triệu | Dữ liệu | BVA (2-point) | `TC-ORD-01`, `TC-ORD-02` | 50tr nhận, 50tr+1 chặn | **✓** |
| **BR-ORD-02** | Khách VIP giảm 10% phí ship | Logic | Decision Table | `TC-ORD-03`, `TC-ORD-04` | Đúng số tiền sau chiết khấu | **✓** |
| **BR-ORD-03** | Đơn Đã giao cấm đổi trạng thái | Trạng thái | STT Invalid Jump | `TC-ORD-05` | HTTP 400 Bad Request | **✓** |
| **BR-ORD-04** | Trừ tồn kho Flash sale an toàn | Đồng thời | Concurrency Lock | `TC-ORD-06`, `TC-ORD-07` | Kho không âm, 1 ca thắng | **✓** |
| **BR-ORD-05** | Webhook thanh toán gửi lặp | Giao tiếp | Idempotency | `TC-ORD-08` | Giao dịch không trùng 2 lần | **✓** |

## 2. Ba Điều Luật Cứng Tại Cổng Thẩm Định Gate 2

1. **Zero-Uncovered Requirement (Không bỏ sót yêu cầu):** Mọi mã $BR-xxx$ hoặc $US-xxx$ trong đặc tả phải có ít nhất một dấu Tick (**✓**) trong bảng RTM. Nếu phát hiện một quy tắc không có bài test bảo vệ $\rightarrow$ **Gate 2 REJECTED**.
2. **Zero-Orphan Test Case (Không viết test rác):** Tuyệt đối cấm viết test case mà không thể truy vết ngược về một Lát cắt hoặc Yêu cầu nghiệp vụ cụ thể. Mọi test case vô căn cứ đều bị loại bỏ.
3. **Deterministic Test Oracle:** Mỗi test case bắt buộc phải có một và chỉ một kết quả mong đợi định lượng cụ thể (Mã HTTP, Trạng thái Entity trong DB, Số dư). Cấm các câu mơ hồ như: *"Hệ thống chạy bình thường"* hoặc *"Dữ liệu hợp lệ"*.

## 3. Checklist Phê Duyệt Của QA / Reviewer Tại Gate 2

- [ ] Test Suite có bảng RTM phủ 100% mã yêu cầu BR-xx.
- [ ] Số ca test được biện minh bằng công thức lát cắt (không áp hạn ngạch võ đoán).
- [ ] Dữ liệu đầu vào và kết quả mong đợi ghi rõ giá trị thực, không dùng placeholder.
- [ ] Có đầy đủ các ca kiểm thử tiêu cực (Negative tests) bảo vệ điểm gãy.
