# Chuẩn thiết kế Happy Path, Happy Case & Test Plan Excel (SRS / FDD / UAT)

> **Loại: tham khảo.** Nguồn chuẩn hóa thực chiến 100% từ bộ hồ sơ kiểm thử 34 sheets `Accounting_TestPlan_NgaPT_20260826.xlsx`. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó.
> Phạm vi áp dụng: Kỹ sư BA, QA, Architect khi xây dựng sheet `TDD_TestScenario_Cases` trong file Excel SRS_FDD hoặc các file Test Plan / UAT độc lập.

---

## 1. Phân định 3 tầng kiểm thử: Golden Thread → Happy Path → Happy Case

Hồ sơ kiểm thử thực chiến phân biệt rõ 3 cấp độ kiểm thử thuận lợi:

```
┌────────────────────────────────────────────────────────────────────────┐
│  CẤP 1: GOLDEN THREAD (HP-00) — Luồng xuyên suốt toàn trình 10 chặng   │
│  Liên kết 5 vai trò (Mess-seller → Kế toán → Telesale → Kho → CSKH)   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  CẤP 2: HAPPY PATH E2E (HP-01..HP-n) — 15 cột chuẩn (V.19.10.2026)     │
│  Xương sống từng module, chuỗi phụ thuộc Master Data & truy vết RTM    │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  CẤP 3: HAPPY CASE CHỨC NĂNG (TC-01..TC-n) — 10 cột chuẩn (-v260925)   │
│  Từng nút bấm/màn hình con, phân nhóm quyền, Dev viết TRƯỚC KHI CODE   │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Cấp 1: Golden Thread (HP-00 — Luồng sợi chỉ vàng)**:
   - *"Nếu trong ngày chỉ chạy được một thứ duy nhất, hãy chạy luồng này."*
   - Xuyên suốt từ khi đơn phát sinh tới khi tiền về tài khoản, chuyển giao qua nhiều Actor khác nhau. Nếu Golden Thread đứt, toàn bộ hệ thống tê liệt.
2. **Cấp 2: Happy Path E2E từng phân hệ (15 cột)**:
   - Luồng nghiệp vụ thuận lợi của từng phân hệ (Master Data, Nguồn đơn, Check trùng, Vận chuyển, Đối soát...).
   - Đảm bảo tính phụ thuộc dữ liệu nền tảng (Master Data phải chạy trước).
3. **Cấp 3: Happy Case chức năng (10 cột)**:
   - Từng ca kiểm thử đơn lẻ trên màn hình (Xem đủ thẻ, Lọc trạng thái, Đổi thời gian chờ...).
   - Dev bắt buộc phải viết và chạy đạt trước khi tạo PR/MR (TDD/ATDD).

---

## 2. Khung Golden Thread (HP-00 — Luồng xuyên suốt liên hoàn)

Học từ sheet `Feature-HappyPath - Dev`, luồng sợi chỉ vàng gồm 10 chặng liên tục qua các Actor:

| Chặng | Vai trò (Actor) | Thao tác chính | Kết quả quan sát được | Mã TC liên kết |
|:---:|---|---|---|:---:|
| **1** | Mess-seller | Nhập 1 đơn SALEPAGE hợp lệ | Đơn có mã hệ thống, đúng nguồn data SALEPAGE | A03 |
| **2** | Kế toán | Thực hiện Check trùng | Đơn hợp lệ chuyển trạng thái: KHÔNG trùng | B02 |
| **3** | Kế toán | Thực hiện Check HNL & Blacklist | Đơn PASSED (tỷ lệ hoàn ≤ 60%, không Blacklist) | C04 |
| **4** | Telesale | Bấm "Tách địa chỉ" → AI chuẩn hóa → Xác nhận | Địa chỉ chuẩn 3 cấp, trạng thái Đã xác nhận | D04 |
| **5** | Kế toán | Tạo lô & Bấm xuất J&T Express | Nhận mã Waybill thật từ J&T trả về | E02 |
| **6** | Kế toán | Thực hiện Chia đơn cho Kho | Đơn chuyển sang nhóm Chờ in Waybill | F02 |
| **7** | NV Kho | Sắp xếp đơn → Bấm in Waybill | Phiếu in ra chuẩn, đơn chuyển sang Đã in Waybill | F07 |
| **8** | Kế toán | Thực hiện Chia đơn cho CSKH | Đơn gắn đúng nhân viên CSKH phụ trách | H01 |
| **9** | NV CSKH | Gọi khách → Cập nhật "Successful" | Trạng thái CSKH cập nhật, vận chuyển giữ nguyên | H05 |
| **10** | Kế toán | Đối soát file thanh toán J&T | Khớp tiền COD → Trạng thái "Đã thanh toán" | K03 |

---

## 3. Biểu mẫu Happy Path E2E (Chuẩn 15 cột V.19.10.2026)

### 3.1. Header Metadata & KPI Dashboard (Dòng 1–8)

```text
Dòng 1: Mã Module          | Happy Path
Dòng 2: Mục đích kiểm thử  | Kiểm thử luồng chức năng chính của phần mềm từ đầu đến cuối
Dòng 3: Mã tính năng       | Happy-path-E2E
Dòng 4: Tác giả            | <Email tác giả, ví dụ: NgaPT@gdttech.net>
Dòng 5: Người kiểm thử     | <Email tester phụ trách, ví dụ: Duongttb@gdttech.net>
Dòng 6: Ngày cập nhật      | YYYY-MM-DD
Dòng 7: Pass | Fail | Block | Untest | Tổng số luồng
Dòng 8:  8   |   7  |   5   |    4   | 24 (=SUM(A8:D8))
```

### 3.2. Cấu trúc 15 cột chi tiết (Bắt đầu từ Dòng 10)

| STT | Tên cột | Kiểu | Mô tả & Quy tắc định dạng | Ví dụ thực tế |
|:---:|---|---|---|---|
| 1 | **ID** | Text | Đánh số thứ tự theo chuỗi phụ thuộc: `HP-01`, `HP-02`... | `HP-01` |
| 2 | **Luồng** | Text | Tên luồng lớn: `L<số> · <Tên phân hệ>` | `L11 · Master Data` |
| 3 | **Màn hình** | Text | Đường dẫn breadcrumb từ menu chính | `Master Data › Sản phẩm` |
| 4 | **Vai** | Text | Actor thực hiện: Kế toán, Mess-seller, CSKH, Thủ kho, Admin | `Kế toán` |
| 5 | **Tiền điều kiện** | Text | Trạng thái dữ liệu và thứ tự bắt buộc: `Chạy TRƯỚC L1` | `Chưa có sản phẩm 'Sữa rửa mặt trà xanh'. Chạy TRƯỚC L1.` |
| 6 | **Dữ liệu test** | Text | Dạng key-value cô đọng ngăn cách bằng dấu `·` | `Ngành hàng: Mỹ phẩm · Tên: Sữa rửa mặt trà xanh · COD: 0 · Quy cách: 100ml` |
| 7 | **Các bước thực hiện** | Text | Đánh số thao tác: `1. ... \n 2. ... \n 3. ...` | `1. Bấm 'Thêm sản phẩm'\n2. Nhập đủ trường theo Dữ liệu test\n3. Bấm xác nhận` |
| 8 | **Kết quả mong đợi** | Text | Đánh số khớp 1-1 với bước thao tác, nêu rõ phản hồi UI và chỉ số KPI (+1) | `1. Form mở ra\n2. Nhập đủ, không lỗi\n3. Lưu thành công, form đóng; Tổng sản phẩm +1` |
| 9 | **Kết quả thực tế** | Text | `Chưa phát triển` (nếu chưa code) hoặc ghi chi tiết từng bước (`B1: Pass \n B2: Fail...`) | `Chưa phát triển` hoặc `B1: Pass\nB2: Hiển thị thiếu 2 trường => Fail` |
| 10 | **Trạng thái** | Enum | 4 trạng thái chuẩn: `Pass`, `Fail`, `Block`, `Untest` | `Untest` |
| 11 | **Tester** | Text | Email/Tên tester chạy ca test | `Duongttb@gdttech.net` |
| 12 | **Ngày chạy** | Date | Ngày thực tế kiểm thử (YYYY-MM-DD) | `2026-10-19` |
| 13 | **Mã Mantis** | Text | ID bug trên hệ thống Mantis nếu Fail | `MAN-0421` |
| 14 | **Ghi chú** | Text | Câu hỏi phản biện BA (`❓`), mâu thuẫn mockup/SRS | `❓ Bộ lọc ngày mặc định là gì? Mockup §3.1.2 khác §3.8.` |
| 15 | **Căn cứ (US/BR)** | Text | Ma trận truy vết yêu cầu (RTM): Mã User Story & Business Rule | `US-3.9.1-02 §3.9; rule BR1–BR8 §3.1.3` |

---

## 4. Biểu mẫu Happy Case Chức Năng (Chuẩn 10 cột -v260925)

Dành cho các sheet test chi tiết của từng màn hình con (`Đối soát Waybill & Hoàn`, `Check Trùng`...).

### 4.1. Header Metadata (Dòng 1–7)
```text
Dòng 1: Mã Module          | Nguồn đơn & Tiền xử lý
Dòng 2: Mục đích kiểm thử  | Kiểm thử các nút chức năng màn Nguồn đơn & Tiền xử lý
Dòng 3: Mã tính năng       | Waybill-reconciliation
Dòng 4: Tác giả            | NgaPT@gdttech.net
Dòng 5: Người kiểm thử     | Duongttb@gdttech.net
Dòng 6: Pass | Fail | Block | Not Run | Tổng số test case
Dòng 7:  2   |  14  |   0   |    0    | 16 (=SUM(A7:D7))
```

### 4.2. Dòng gom nhóm quyền hạn & 10 Cột chi tiết
Trước mỗi khối chức năng, đặt một dòng tiêu đề in hoa không ID:
> `NHÓM 1 — QUYỀN KẾ TOÁN (§2.3.2: Đối soát hàng hoàn với J&T = CRU · Xử lý bồi hoàn = RU)`

*Bảng dữ liệu bắt đầu từ Dòng 9:*
1. **Test ID**: `<Slug_chức_năng>_<Số>`, ví dụ `Waybill-reconciliation_1`.
2. **Tên test case**: Diễn đạt hành vi cụ thể (*Xem màn đối soát với đủ 4 thẻ và danh sách đơn*).
3. **Điều kiện tiên quyết**: Gạch đầu dòng (`- Đăng nhập Kế toán\n- Có đơn J&T Đang hoàn`).
4. **Các bước thực hiện**: Đánh số `1. ... \n 2. ... \n 3. ...`
5. **Kết quả mong đợi**: Đánh số tương ứng, trích dẫn mã quy tắc nghiệp vụ `(BR01, BR02)`.
6. **Kết quả thực tế**: Mô tả chi tiết khi Fail (bóc trần thiếu bộ đếm thời gian, lệch số liệu...).
7. **Độ ưu tiên**: `Cao`, `Trung bình`, `Thấp`.
8. **Trạng thái**: `Passed`, `Failed`, `Blocked`, `Not Run` (hoặc `N/A` khi chức năng bị hủy).
9. **Ngày test**: YYYY-MM-DD.
10. **Ghi chú**: Ghi chú thay đổi nghiệp vụ hoặc nguyên nhân hủy case.

---

## 5. Ma trận Kiểm thử Phân quyền 2 Chiều (RBAC CRUD Matrix)

Học từ sheet `Q-Phân quyền-v1`, kiểm thử phân quyền bắt buộc phải kiểm tra **2 chiều (Cả UI lẫn API)**:

| Loại quyền | Hành vi mong đợi trên UI | Hành vi mong đợi tại API |
|---|---|---|
| **Chỉ xem (R - Read)** | Mở được màn hình, xem danh sách. Nút Thêm/Sửa/Xóa bị **ẩn hoặc disable**. | Gọi API `GET` trả `200 OK`. Gọi API `POST/PUT/DELETE` trả `403 Forbidden`. |
| **Toàn quyền (CRU / CRUD)** | Thao tác đầy đủ Thêm, Sửa, Xem. Không có nút nào bị cấm. | Toàn bộ API nghiệp vụ tương ứng trả về thành công (`200 OK` / `201 Created`). |
| **Không có quyền (No Access)** | Chức năng **không xuất hiện trên menu điều hướng**. Truy cập URL trực tiếp bị chuyển hướng về trang 403 hoặc thông báo từ chối. | Mọi request API liên quan đều bị chặn ở tầng Gateway/Filter, trả về `401 Unauthorized` hoặc `403 Forbidden`. |

---

## 6. Bộ 5 biểu mẫu Báo cáo & Quản trị kiểm thử (Reports & Management)

### 6.1. Sheet "3. Reports" — Dashboard tổng hợp KPI toàn dự án

Bảng tổng hợp tình trạng kiểm thử theo phân hệ với **3 công thức vàng**:

```text
========================================================================================
                                       REPORTS
========================================================================================
STT | Mã Module             | Pass | Fail | Block | Not Run | Cancel | Tổng số test case
----+-----------------------+------+------+-------+---------+--------+------------------
1.0 | Happy path            |   8  |   7  |   5   |    4    |    0   |        23
2.0 | Nguồn đơn & Tiền xử lý|   4  |  15  |   0   |    0    |    0   |        19
3.0 | Check trùng           |  11  |   8  |   1   |    0    |    0   |        20
... | ...                   |  ... |  ... |  ...  |   ...   |   ...  |       ...
----+-----------------------+------+------+-------+---------+--------+------------------
    | Tổng                  |  46  |  99  |  18   |    0    |   43   |       211
----------------------------------------------------------------------------------------
1. Tỷ lệ kiểm thử (Progress Rate) = (Pass + Fail + Block) / Tổng = 77.3%
2. Tỷ lệ Pass (Quality Pass Rate) = Pass / Tổng                 = 21.8%
3. Tỷ lệ Bug (Defect Rate)       = Fail / Tổng                 = 55.5%
```

### 6.2. Sheet "Bug" — Sổ quản lý Defect (11 cột & 5 trạng thái)
- **Header KPI**: Theo dõi 5 trạng thái vòng đời lỗi: `Mới` | `Đang xử lý` | `Đã sửa` | `Tái mở` | `Đã đóng`.
- **11 Cột**: `ID`, `Module`, `Mô tả`, `Các bước thực hiện`, `Kết quả mong đợi`, `Kết quả thực tế`, `Độ ưu tiên (High/Medium/Low)`, `Trạng thái`, `Ngày test`, `Người test`, `Ghi chú`.

### 6.3. Sheet "Task Test" — Ma trận phân định ranh giới Code - Test
Phân định ranh giới chéo minh bạch giữa lập trình viên và kiểm thử viên:
`Màn hình / Phân hệ` | `Code (Dev phụ trách)` | `Test (QA kiểm thử chéo)`

### 6.4. Sheet "0. TestPlan" — Kế hoạch kiểm thử chuẩn UAT
Bao gồm 5 mục tiêu chuẩn:
1. **Thông tin tài liệu**: Dự án, Mã tài liệu, Tác giả, Ngày tạo/cập nhật, Phiên bản.
2. **Mục tiêu kiểm thử**: Mục tiêu chính, Tiêu chí hoàn thành (100% case Cao/TB được chạy; 100% Critical fix xong), **Tiêu chí dừng (Suspension Criteria)**: *Phát hiện defect Critical chặn luồng chính không có cách đi vòng, hoặc trên 30% test case trong 1 module bị Fail*.
3. **Phạm vi**: Trong phạm vi (In-scope) vs Ngoài phạm vi (Out-of-scope).
4. **Môi trường**: Máy chủ UAT độc lập, URL test, Trình duyệt chuẩn (Chrome latest), Hệ điều hành.
5. **Tài khoản test**: Danh sách tài khoản mẫu theo từng vai trò (Kế toán, Mess-seller, Telesale, CSKH, Kho, Admin).

### 6.5. Sheet "2. Scenario" — Sổ quản lý thay đổi kịch bản (Change Log)
Quản lý lịch sử thêm/bớt kịch bản theo mã phân loại:
- `A` (Add): Thêm mới test case.
- `D` (Delete): Xóa test case không còn giá trị.
- `M` (Modify): Sửa đổi bước test hoặc kỳ vọng do thay đổi yêu cầu.

---

## 7. Văn phong & Kỹ thuật viết kịch bản chuyên nghiệp

### 7.1. Chuỗi phụ thuộc luồng (Dependency Chain)
Ghi rõ điều kiện dữ liệu và thứ tự chạy trong cột *Tiền điều kiện*:
- `Chưa có sản phẩm 'Sữa rửa mặt trà xanh' trên hệ thống. Chạy TRƯỚC L1.`
- `Chưa có nhân viên 'Lê Thị Mai / mai.kt'. Chạy TRƯỚC L4, L7, L8.`

### 7.2. Chuẩn hóa dữ liệu test (Key-Value với dấu `·`)
Tránh viết đoạn văn dài. Sử dụng dấu `·` để phân tách rõ từng trường:
```text
Tên KH: Trần Thị Hạnh · SĐT: 9122223333 · Sản phẩm: Viên uống Collagen · SL: 1 · COD: 560.000 · NV SALE: NV_01
```

### 7.3. Kỹ thuật đối soát thực tế khi Fail
Mô tả rõ số lượng sai lệch và trường dữ liệu thừa/thiếu:
- *"Tổng đơn hệ thống: 35.571; Tổng đơn các nền tảng cộng lại: 35.522 (Lệch 49 đơn)."*
- *"FORM thêm mới hiển thị 10 trường: Thừa 2 trường NV-ADS và Tên Page so với SRS."*
- *"Có 30 đơn ở Chưa chia, sau khi bấm chia chỉ có 29 đơn hiển thị ở Đã chia."*

### 7.4. Phản biện BA trong cột Ghi chú bằng icon `❓`
Chất vấn thẳng thắn các điểm mâu thuẫn giữa Mockup và SRS:
- `❓ Bộ lọc ngày trên màn Nguồn đơn mặc định là ngày nào?`
- `❓ Menu bên trái khác nhau giữa các mockup: §3.1.2 gộp 'Nguồn đơn & Tiền xử lý', §3.8 tách riêng. Chốt cấu trúc menu để QA biết đi đường nào.`
- `❓ BR-3: Liệt kê bổ sung các trường bắt buộc trong form Thêm đơn mới.`

### 7.5. Xử lý kịch bản bị hủy (Cancel / N/A) khi Spec thay đổi
Khi yêu cầu nghiệp vụ thay đổi (ví dụ: Nghiệp vụ bỏ yêu cầu nộp file J&T, chỉ cần 1 file scan kho):
- Giữ nguyên dòng test case để duy trì tính toàn vẹn của mã số Test ID.
- Đổi trạng thái sang `N/A` hoặc `Cancel`.
- Hạ độ ưu tiên xuống `Thấp`.
- Cột Ghi chú ghi rõ: `Chức năng đã được thay đổi theo quyết định BA ngày DD/MM`.
- Cột Cancel trong sheet `3. Reports` tăng +1 tương ứng.

---

## 8. Lược đồ 4 thế hệ tiến hóa kịch bản kiểm thử trong dự án

```
Thế hệ 1 (Draft cá nhân):     Sheets 'Đức-', 'P-', 'K-', 'D-', 'B-', 'Q-' (Dev/Tester viết nháp)
                                              │
                                              ▼
Thế hệ 2 (Module chức năng):   Sheets '*-v260925' (10 cột, gom nhóm NHÓM 1, trích dẫn BR)
                                              │
                                              ▼
Thế hệ 3 (Happy Path E2E):     Sheet 'Happy path - V.261006' (11 cột, bắt đầu bóc tách từng bước B1..Bn)
                                              │
                                              ▼
Thế hệ 4 (Chuẩn hoàn thiện):  Sheet 'Happy path - V.19.10.2026' (15 cột, RTM, Màn hình, Vai, Dữ liệu test)
                               + Khung 'Feature-HappyPath - Dev' (Golden Thread HP-00 liên vai trò)
```
