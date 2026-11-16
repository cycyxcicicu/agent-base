> Task: T-15 · Epic: E2 · Vai: architect

# Tiêu chuẩn thiết kế kịch bản kiểm thử (Test Cases Design Protocol)

Giao thức này quy định phương pháp thiết kế kịch bản kiểm thử có kỷ luật, định hướng theo cấu trúc bài toán (Problem-Driven Test Strategy), đảm bảo mọi ca kiểm thử được thiết kế và phê duyệt theo chuẩn ISTQB & ATDD **trước khi viết mã nguồn**.

Tài liệu tham chiếu gốc: Cẩm nang **`istqb-test-engineering-playbook.md`** (`agents/knowledge/quy-trinh/istqb-test-engineering-playbook.md`) và 4 chuyên khảo vệ tinh (`agents/knowledge/quy-trinh/testing/`).

---

## 1. Các nguyên tắc cốt lõi

1. **Test-First (Viết kịch bản trước khi code)**: Kịch bản kiểm thử phải được lập ngay từ Bước 3 của chu trình task (`task-execution-cycle.md`); cấm nhảy vào code khi chưa có kịch bản test và chưa qua phê duyệt Swarm Gate 2.
2. **Phân biệt rạch ròi 3 tầng kiểm thử**:
   - **Cấp 1: Golden Thread (HP-00 — Luồng sợi chỉ vàng)**: Luồng nghiệp vụ chính xuyên suốt toàn trình từ đầu đến cuối (End-to-End Golden Thread) qua nhiều tác nhân/vai trò. Nếu Golden Thread hỏng, toàn bộ hệ thống tê liệt.
   - **Cấp 2: Happy Path E2E (HP-01..HP-n)**: Luồng thuận lợi chuẩn mực của từng phân hệ/màn hình khi mọi rẽ nhánh đều thành công. Happy Path là xương sống; Happy Path hỏng thì các test case khác (biên, ngoại lệ) không được chạy.
   - **Cấp 3: Happy Case chức năng & Test Cases (TC-01..TC-n)**: Từng ca kiểm thử cụ thể cho từng lát cắt chức năng, bao gồm Happy Cases, Error Cases, Boundary Cases và Edge Cases. Dev bắt buộc phải viết và chạy đạt trên môi trường thật trước khi tạo PR/MR.
3. **Chiến lược Kiểm thử Hướng Bài toán (Problem-Driven Testing)**:
   - Nghiêm cấm viết test mù quáng, sinh test hời hợt hoặc chọn kỹ thuật cảm tính.
   - Phân tích cấu trúc bài toán/code thành **8 Lát cắt Nguyên tử (Atomic Facets)**:
     1. *Miền giá trị rời rạc/liên tục*: Áp dụng EP (Lee Copeland 4 phân vùng) & BVA (2-point / 3-point).
     2. *Quy tắc nghiệp vụ tổ hợp (BR-xxx)*: Áp dụng Decision Table Testing (DTT) rút gọn Don't Care hoặc Cause-Effect Graphing.
     3. *Vòng đời thực thể & Sự kiện*: Áp dụng State Transition Testing (0-switch, Chow's W-Method).
     4. *Bộ lọc / Ma trận cấu hình đa chiều*: Áp dụng Pairwise / Combinatorial Testing (Taguchi OATS $L_4..L_{18}$) hoặc Classification Tree (CTM).
     5. *Luồng liên vai trò / Tích hợp phân hệ*: Áp dụng Use Case Testing & Scenario Testing.
     6. *Xử lý đồng thời / Tranh chấp tài nguyên*: Áp dụng Concurrency, Race Condition & Deadlock Testing (Pessimistic/Optimistic lock).
     7. *Tích hợp bên thứ 3 & Webhook*: Áp dụng Idempotency, Retry, Timeout & Fault Injection Testing.
     8. *Thuật toán lõi & Độ phức tạp nhánh*: Áp dụng White-box (McCabe Cyclomatic Complexity $V(G)$, MC/DC $n+1$) & Mutation Testing (PIT $\ge 85\%$).
   - **Bài toán đa chiều (Multi-faceted)**: Khi một tính năng chứa đồng thời nhiều lát cắt (ví dụ: vừa có Form nhập liệu, vừa có quy tắc voucher tổ hợp, vừa có vòng đời đơn hàng), BẮT BUỘC phối hợp các kỹ thuật tương ứng cho từng lát cắt, tuyệt đối không gò ép vào 1 kỹ thuật duy nhất.
4. **Ước lượng Sizing Toán học & Nghiêm cấm Hạn ngạch Cảm tính (Zero Arbitrary Quotas)**:
   - TUYỆT ĐỐI CẤM các hạn ngạch cứng tùy tiện ("Task vừa: 8–15 ca, Task lớn: 20–40 ca"). Số lượng ca test là hàm số toán học của cấu trúc bài toán:
     $$N_{total} = \sum_{k=1}^{M} N(F_k) - \text{Overlap}$$
   - Nghiệm thu theo tiêu chí **Minimal Spanning Test Suite**:
     * *Không thừa (Zero Redundancy)*: Mỗi phân vùng tương đương chỉ chọn ĐÚNG 1 ca đại diện; các nhánh điều kiện bất khả thi hoặc "Don't Care" phải được gộp lại.
     * *Không thiếu (Full Boundary Coverage)*: Bao phủ 100% điểm biên xác định được (2-point hoặc 3-point).
     * *Có căn cứ toán học*: Mọi test suite đều có công thức giải trình số lượng.
5. **Ma trận Truy vết Yêu cầu 2 chiều (Requirements Traceability Matrix - RTM)**:
   - Mọi task từ cỡ "vừa" trở lên bắt buộc có bảng RTM liên kết 2 chiều:
     $$\text{Yêu cầu } (R\text{-}xxx, BR\text{-}xxx) \longleftrightarrow \text{Ca kiểm thử } (TC\text{-}xx)$$
   - Đảm bảo tính toàn vẹn: $100\%$ yêu cầu có ít nhất một ca test bảo vệ, và $100\%$ ca test truy xuất được nguồn gốc yêu cầu (không viết test thừa ngoài phạm vi).
6. **Bảng Lý giải Căn cứ Kỹ thuật (Technique Justification Table)**:
   - Trình bày rõ: Nhóm ca test, Lát cắt bài toán, Kỹ thuật ISTQB/Heuristic áp dụng, Công thức sizing và lý do lựa chọn.
7. **Mỗi bước một hành động cụ thể**: Hành động đo lường được, dữ liệu thật cụ thể (cấm ghi "nhập dữ liệu hợp lệ"), kết quả mong đợi quan sát được bằng mắt hoặc phản hồi dữ liệu duy nhất.
8. **Quy tắc xuất TestLink XML**: Bắt buộc xuất file XML chuẩn TestLink (`doc/features/<UC>/<UC>-testlink-cases.xml` hoặc `BUG-<Mã>-testlink.xml`, Keyword = mã task hoặc mã bug Mantis).
9. **Cấm AI tự ghi "Passed"**: Kết quả chỉ được đánh dấu Passed khi có bằng chứng chạy thật (Exit code 0, log output kiểm thử tự động, hoặc trace CDP).
10. **Phân định thẩm quyền Dev vs QA**: Khi sửa lỗi, **Dev chỉ được đổi trạng thái sang `Resolved`**; **CHỈ QA HOẶC CON NGƯỜI MỚI CÓ QUYỀN ĐÓNG (`Closed`)** sau khi tái kiểm chứng đạt.

---

## 2. Bảng Ma Trận Định Tuyến Kỹ Thuật (Problem-Driven Routing Matrix)

| Lát cắt Bài toán (Problem Facet) | Dấu hiệu Nhận diện từ Yêu cầu / Mã nguồn | Kỹ thuật ISTQB Áp dụng | Công thức Toán học Ước lượng Sizing |
|---|---|---|---|
| **1. Miền giá trị / Nhập liệu** | Trường số lượng, tiền tệ, ngày tháng, độ dài chuỗi, định dạng Regex | **EP** (Copeland) + **BVA** (2-point/3-point) | $N_{EP} = 1_{\text{valid}} + k_{\text{invalid}}$<br/>$N_{BVA} = 2 \times (\text{số biên})$ (2-pt) hoặc $3 \times (\text{số biên})$ (3-pt) |
| **2. Logic nghiệp vụ đa điều kiện** | Nhiều `if-else`, ma trận phân loại khách hàng, chiết khấu, bảng thuế, `BR-xxx` | **Decision Table (DTT)** / **Cause-Effect Graph** | $N_{DTT} \le 2^n$ (Lý thuyết)<br/>$N_{DTT} \approx n + 2$ đến $2n$ sau rút gọn Don't Care |
| **3. Vòng đời thực thể / Quy trình** | Cột `status`, quy trình duyệt đơn, chuyển bước trạng thái (Draft $\rightarrow$ Done) | **State Transition Testing (STT)** / **W-Method** | $N_{STT} = N_{\text{transitions}} + N_{\text{invalid\_transitions}}$ (0-switch coverage) |
| **4. Bộ lọc / Cấu hình tổ hợp** | Màn hình tìm kiếm nhiều dropdown, checkbox, ma trận OS $\times$ Device $\times$ Role | **Pairwise / Orthogonal Array (OATS)** | Tra cứu mảng Taguchi ($L_4, L_8, L_9, L_{16}, L_{18}$)<br/>Giảm từ $V^k$ xuống $\sim O(V^2)$ |
| **5. Luồng liên vai trò / Tích hợp E2E** | Luồng nghiệp vụ qua nhiều Actor (Seller $\rightarrow$ Kho $\rightarrow$ Giao hàng $\rightarrow$ Kế toán) | **Use Case Testing** / **Scenario Testing** | $N_{UC} = 1_{\text{Basic}} + \sum (\text{Alternative}) + \sum (\text{Exception})$ |
| **6. Xử lý đồng thời / Tranh chấp** | Trừ tồn kho, ví tiền, số dư tài khoản, voucher số lượng có hạn | **Concurrency & Race Condition Testing** | Tối thiểu 3 ca: Đồng thời cùng lúc, Tuần tự sát nút, Deadlock rollback |
| **7. Tích hợp ngoài / Webhook** | Gọi bên thứ 3 (Payment, Vận chuyển), webhook callback, hàng đợi Message Queue | **Idempotency & Fault Injection Testing** | Tối thiểu 4 ca: Thành công, Gọi trùng lặp (Idempotent), Timeout/Retry, Webhook giả mạo |
| **8. Thuật toán lõi & Rẽ nhánh phức tạp** | Logic tính toán tài chính phức tạp, biểu thức điều kiện kép (`&&`, `\|\|`) | **White-box (MC/DC)** & **PIT Mutation** | $N_{\text{BasisPath}} = V(G) = E - N + 2P$<br/>$N_{MC/DC} = n + 1$<br/>Mutation Score $\ge 85\%$ |

---

## 3. Mẫu Bảng Kịch Bản Kiểm Thử Chuẩn (Kèm RTM & Căn Cứ Kỹ Thuật)

```markdown
### Bảng 1: Ma trận Truy vết Yêu cầu 2 Chiều (RTM)
| Mã Yêu cầu (SRS/BR) | Tóm tắt Nghiệp vụ | Mã Test Case (TC) | Mức độ Bao phủ |
|---|---|---|---|
| R-01 / BR-01 | Độ dài mật khẩu từ 8 đến 16 ký tự | TC-AUTH-04, TC-AUTH-05 | 100% Biên (2-point BVA) |
| R-02 / BR-02 | Khóa tài khoản sau 5 lần đăng nhập sai | TC-AUTH-06, TC-AUTH-07 | 100% Chuyển trạng thái (STT) |

### Bảng 2: Bảng Lý giải Căn cứ Kỹ thuật (Technique Justification Table)
| Nhóm Ca Kiểm thử | Lát cắt Bài toán | Kỹ thuật ISTQB Áp dụng | Công thức Sizing | Lý do Lựa chọn |
|---|---|---|---|---|
| TC-AUTH-01..03 | Miền giá trị tài khoản | Equivalence Partitioning (EP) | 1 Valid + 2 Invalid = 3 | Kiểm thử đại diện phân vùng hợp lệ, không tồn tại, và sai format |
| TC-AUTH-04..05 | Ngưỡng độ dài mật khẩu | 2-point BVA | 2 biên x 2 điểm = 4 | Bắt lỗi toán tử so sánh (> thay vì >=) tại ngưỡng 8 và 16 |
| TC-AUTH-06..07 | Vòng đời khóa tài khoản | State Transition Testing | 1 Valid transition + 1 Invalid | Xác nhận chuyển Active -> Locked và chặn đăng nhập khi Locked |

### Bảng 3: Chi tiết Kịch bản Kiểm thử
| Mã Case | Căn cứ RTM | Kỹ thuật ISTQB | Tiền điều kiện | Các bước thực hiện | Dữ liệu test cụ thể | Kết quả mong đợi quan sát được | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| TC-AUTH-01 | R-01 | EP (Valid) | User `test_user` tồn tại | 1. Nhập username<br/>2. Nhập password<br/>3. Bấm Đăng nhập | User: `test_user`<br/>Pass: `Pass@123` | HTTP 200, JWT cookie trả về, chuyển hướng `/dashboard` | [Log / Trace] | Passed |
```

---

## 4. Ví Dụ Minh Họa Đa Chiều: Tính Năng Đặt Hàng & Áp Mã Khuyến Mãi

Tính năng này kết hợp đồng thời **4 Lát cắt Bài toán**:
1. Lát cắt 1: Miền giá trị số lượng đặt mua ($1 \le Q \le 99$) $\rightarrow$ BVA 2-point.
2. Lát cắt 2: Logic áp mã giảm giá (Đơn $\ge 500k$, Thành viên VIP, Mã còn hạn) $\rightarrow$ Decision Table (DTT).
3. Lát cắt 3: Vòng đời đơn hàng (`New` $\rightarrow$ `Paid` $\rightarrow$ `Delivered` $\rightarrow$ `Cancelled`) $\rightarrow$ State Transition (STT).
4. Lát cắt 4: Trừ tồn kho đồng thời khi 2 khách cùng mua sản phẩm cuối cùng $\rightarrow$ Concurrency Lock.

### 4.1. Bảng Lý giải Kỹ thuật & Sizing
- **Lát cắt 1 (BVA Số lượng)**: Ngưỡng [1, 99]. 2-point BVA: $Q \in \{0, 1, 99, 100\} \Rightarrow 4$ ca.
- **Lát cắt 2 (DTT Mã giảm giá)**: 3 điều kiện Boolean (Giá trị đơn $\ge 500k$, Khách VIP, Mã còn hạn). Rút gọn Don't Care: Nếu mã hết hạn $\rightarrow$ từ chối ngay (1 ca); Nếu đơn $< 500k \rightarrow$ từ chối ngay (1 ca); Hợp lệ áp mã VIP (1 ca); Hợp lệ áp mã thường (1 ca) $\Rightarrow 4$ ca.
- **Lát cắt 3 (STT Vòng đời đơn)**: 3 chuyển đổi hợp lệ ($N \rightarrow P \rightarrow D$, $N \rightarrow C$) + 2 chuyển đổi bất hợp lệ ($N \rightarrow D$, $C \rightarrow P$) $\Rightarrow 5$ ca.
- **Lát cắt 4 (Concurrency)**: 2 luồng đồng thời tranh chấp 1 sản phẩm cuối $\Rightarrow 1$ ca.
- **Tổng số ca kiểm thử**: $N_{total} = 4 + 4 + 5 + 1 - 1 (\text{Overlap Happy Path}) = 13$ ca kiểm thử được chứng minh bằng toán học (không bịa đặt số lượng).

### 4.2. Bảng Kịch bản Chi tiết

| Mã Case | Căn cứ RTM | Lát cắt & Kỹ thuật | Tiền điều kiện | Các bước thực hiện & Dữ liệu test | Kết quả mong đợi quan sát được | Trạng thái |
|---|---|---|---|---|---|---|
| **TC-ORD-01** | R-01 (Happy Path) | Use Case / Golden Thread | Sản phẩm A có tồn kho 10; User VIP có giỏ hàng 600k | 1. Chọn mua số lượng $Q=2$<br/>2. Áp mã voucher `VIP50`<br/>3. Bấm Đặt hàng & Thanh toán | Đơn tạo thành công, giảm giá 50k, tồn kho A giảm còn 8, trạng thái đơn `Paid`. | Draft |
| **TC-ORD-02** | R-02 (Biên dưới) | Miền giá trị / BVA 2-point | Sản phẩm A tồn kho 10 | Nhập số lượng $Q=0$ vào ô số lượng | Hệ thống báo lỗi "Số lượng phải từ 1 đến 99", nút Đặt hàng bị vô hiệu hóa. | Draft |
| **TC-ORD-03** | R-02 (Biên trên) | Miền giá trị / BVA 2-point | Sản phẩm A tồn kho 200 | Nhập số lượng $Q=100$ vào ô số lượng | Hệ thống báo lỗi "Số lượng tối đa cho mỗi đơn là 99 sản phẩm". | Draft |
| **TC-ORD-04** | BR-01 (Voucher) | Tổ hợp / Decision Table | Giỏ hàng 400k (dưới 500k), voucher `VIP50` | 1. Nhập mã voucher `VIP50`<br/>2. Bấm áp dụng | Hệ thống từ chối áp dụng: "Đơn hàng tối thiểu 500.000đ để áp dụng mã này". | Draft |
| **TC-ORD-05** | BR-01 (Voucher) | Tổ hợp / Decision Table | Giỏ hàng 600k, voucher `EXPIRED` | 1. Nhập mã voucher `EXPIRED`<br/>2. Bấm áp dụng | Hệ thống từ chối: "Mã khuyến mại đã hết hạn sử dụng". | Draft |
| **TC-ORD-06** | BR-02 (Vòng đời) | State Transition (Invalid) | Đơn hàng `ORD-101` ở trạng thái `New` (chưa thanh toán) | Gọi API cập nhật trạng thái sang `Delivered` | HTTP 400 Bad Request: "Không thể giao đơn hàng chưa thanh toán". | Draft |
| **TC-ORD-07** | BR-02 (Vòng đời) | State Transition (Invalid) | Đơn hàng `ORD-102` đã ở trạng thái `Cancelled` | Gọi API xác nhận thanh toán `Paid` | HTTP 409 Conflict: "Đơn hàng đã hủy không thể thanh toán". | Draft |
| **TC-ORD-08** | R-03 (Tranh chấp) | Concurrency / Pessimistic Lock | Sản phẩm B chỉ còn tồn kho $1$ | 2 tài khoản Client 1 và Client 2 cùng bấm thanh toán $Q=1$ tại cùng miligiây $T_0$ | 1 Client thành công (tồn kho về 0); 1 Client nhận thông báo "Sản phẩm vừa hết hàng", không xảy ra âm kho. | Draft |
