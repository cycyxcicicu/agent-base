> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục B (từ WBS_Planning đến sheet mở rộng)

# Chuẩn viết từng sheet SRS_FDD — Phần 3: Kế hoạch WBS, RTM, Actor & Kiểm thử

### `WBS_Planning` (hoặc WBS gọn)
- Nhập: `No`/ `STT`, `Task`, `Notes/ Assumptions`, `Est (MH)`, `Pre`, `Assignee`, `Status`, `PCT`. **Không ghi đè ô công thức** (E, H, I, J, M, timeline, tổng dòng cha).
- Một task = **một kết quả nghiệm thu được** (file/ test/ hành vi) trong **≤ ~1 ngày công** (6,4 giờ = 1 MD); ghi **Mục tiêu/ Kết quả mong đợi** và **Liên kết**: use-case/ user-story, mục `Component_Detail_Design`/ tài liệu, số RTM.
- Task phụ thuộc → điền `Pre`. Giả định/ ngoài phạm vi ghi ở đầu sheet. Ước lượng là **đề xuất**, người dùng chốt.

### `Function_RTM`
- **Mỗi file code/ hàm/ service chính một dòng** (cấp lá); dòng cha là nhóm chức năng.
- Điền đủ chuỗi: `BRD/ SRS Reference` (mục SRS, `AC-xx`) → `UI Reference` (màn hình/ mockup) → `Code Reference` (**đường dẫn file thật**) → `Unit/ Integration/ System/ UAT Test Reference` (**tên lớp test/ ID test case thật**). Chưa có → để `-` và ghi lý do, **không bịa đường dẫn/ ID**.
- `Trạng thái dòng` do người đối soát với git cập nhật; `Xác nhận` (Yes/No + ngày) **chỉ người dùng**.

### `Actors_Peronas`
- Mỗi khối: `Name` (vai trò thật: Kế toán, Mess-seller, Telesale, CSKH, Kho, ADS…), `Description` (làm gì trên hệ thống, quyền gì — lấy từ ma trận chức năng SRS mục 2.3). **Cấm để "Lorem ipsum".**

### `TDD-TestScenario`
- Mỗi chức năng/ task một khối: **Happy Path trước**, rồi dữ liệu sai/ lỗi hệ thống. Bảng `No, Thứ tự luồng, Test Case ID, Hành động của người dùng, Kết quả mong đợi (góc nhìn người dùng)`.
- Ngôn ngữ **giao diện** (nút, ô, thông báo hiển thị), **một hành động một bước**, kết quả quan sát được — theo `qa-process.md`. Có phần "Test planning & Assignment" khi cần chia việc.

### `TDD_TestCases`
- ID: `HP_xx` (happy), `EC_xx` (biên/ lỗi), `UT_xx` (unit). Cột: `Name` ("Kiểm tra …"), `Summary`, `Step` (đánh số 1., 2.), `Expected results`, `Trạng thái test` (**dropdown `Pass/Fail/Not run`**; AI **không tự ghi Pass** khi chưa chạy), `Trạng thái dev xử lý`, `Use-Case Reference`, `Acceptance Criteria Ref`.
- Mỗi A/C có **ít nhất một** test case (happy), case lỗi cho nhánh ngoại lệ. Xuất sang TestLink bằng mẫu XML ở `agents/knowledge/quy-trinh/templates/`.

### Sheet mở rộng (dùng khi người dùng đồng ý) **[ĐỀ XUẤT]**
- `Test_Execution_Report`: một dòng mỗi lần chạy thật (ngày, loại, ID, kết quả, đường dẫn log) — chỉ ghi kết quả **đã chạy thật**.
- `Risk_Register`: `RISK-xx`, liên kết task/ use-case, ảnh hưởng/ xác suất, mitigation, rủi ro thứ cấp, người phụ trách.
- `ADR_Log`: `ADR-xx`, bối cảnh, **≥ 2 phương án có điểm + tiêu chí có trọng số**, lựa chọn, lý do, hệ quả; "xác nhận con người" để trống.
