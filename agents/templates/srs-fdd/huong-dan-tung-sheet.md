# SRS_FDD_Template-v3.0 — hướng dẫn từng sheet, từng cột

Nguồn đã phân tích:
- **Mẫu gốc:** `doc/quy-trinh/template/03-srs-fdd-template-v3/goc/SRS_FDD_Template-v3.0.xlsx` (Google Sheet "SRS_FDD_Template-v3.0", người dùng tải về ngày 2026-10-17; 11 sheet, 14MB vì có nhiều ảnh/ sơ đồ minh họa).
- **Bản đã điền thật của dự án khác:** `doc/quy-trinh/template/04-srs-fdd-copilot-da-dien/goc/_SRS_FDD_AI-Agent-Copilot.xlsx` (14 sheet) — dùng để biết **điền như thế nào** và mẫu được mở rộng ra sao.
> Phân tích từ **chữ, công thức, ô gộp, dropdown** trong hai file. Các ảnh/ sơ đồ nhúng trong ô không đọc được. Nội dung ví dụ trong mẫu là của dự án khác (hệ thống tin tức "News System", quản lý trung tâm anh văn, i18n Toktak…) — **chỉ học cách viết, không lấy nội dung**. Quy trình tổng thể: `huong-dan/tong-hop/02-viet-detail-design-document.md`.

## 0. Bức tranh chung

Mẫu = bộ **tài liệu thiết kế chi tiết (FDD) + kế hoạch + truy vết + kiểm thử trong MỘT file**, mỗi sheet một vai trò, liên kết với nhau bằng **ID**:

```
DauMucTaiLieuCanLam  (chọn sheet/ mục nào dùng)
        │
Component_Detail_Design  (yêu cầu, luồng, wireframe, kiến trúc, công nghệ)  ← bức tranh lớn
        │
Functions_Services_Detail_Desig  (chi tiết TỪNG chức năng/ service: use-case/ user-story, giao diện, API, diagram, NFR, tác động)
        │                 │
   WBS_Planning     Function_RTM  ◄──── truy vết: yêu cầu → thiết kế → code → test
   (task, ước lượng)      │
                    TDD-TestScenario → TDD_TestCases  (kịch bản → test case)
NhatKyThayDoi (nhật ký thay đổi toàn file) · PJT_Definition (ngày bắt đầu) · Actors_Peronas (các tác nhân)
```
Sheet `20210620` là **ví dụ thiết kế một màn hình** (kiểu Nhật: Screen ID, Screen Items) — chỉ tham khảo.

**Quy tắc xuyên suốt rút ra từ hai file:**
1. Mỗi chức năng có **một ID** (use-case/ user-story, vd `UC-01`, `US/UC-1.1`) và ID đó xuất hiện ở: Use-case → WBS → RTM → test case (`Use-Case Reference`).
2. Sửa mẫu phải **ghi lý do** (`DauMucTaiLieuCanLam`, cột "Lý do thay đổi so với mẫu") và có phê duyệt (SEPG Head).
3. Mọi thay đổi ghi vào `NhatKyThayDoi`.
4. Không điền "xác nhận" thay người: ở bản Copilot, AI chỉ **đề xuất**, **con người xác nhận bằng file** (cột "Xác nhận của con người (File-based)"), không xác nhận qua chat (đúng tinh thần slide *AI in SDLC*).

---

## 1. `NhatKyThayDoi` — nhật ký thay đổi tài liệu
| Cột | Ý nghĩa / cách điền |
|---|---|
| **No.** | Công thức `=ROW()-1` — không gõ tay |
| **updated date** | Ngày sửa (dd/mm/yyyy) |
| **updated by** | Người sửa (tên người; nếu AI soạn thì ghi rõ công cụ + người duyệt) |
| **updated part** | Loại: `Create new` / `Update` |
| **updated info** | Mô tả **sửa gì** (ngắn, cụ thể; có thể liệt kê gạch đầu dòng) |
| **notes** | Ghi chú, điều kiện, việc chờ xác nhận |
| *(mở rộng ở bản Copilot)* **Liên quan đến (Use-Case/Component ID)**, **Trạng thái duyệt (Draft/Approved)** | Truy vết thay đổi theo ID; chỉ `Approved` khi có người duyệt |

Ví dụ mẫu: dòng 1 "Create new — Create Design file"; dòng 2 "Update — bổ sung mô tả chi tiết cho việc tạo content…".

## 2. `PJT_Definition` — thông số dự án (rất ngắn nhưng **được công thức dùng**)
| Ô | Ý nghĩa |
|---|---|
| `B2` Project Start Date | Ngày bắt đầu dự án (mẫu: 12/01/2026) |
| `B3` StartDate | `=B2` — **mốc bắt đầu mặc định của task không có tiền nhiệm** trong `WBS_Planning` (cột Start Date) |
| `B4` StartSprint | Sprint bắt đầu (mẫu: 15) |
→ Chỉ sửa `B2` (và `B4`); đừng ghi đè `B3`. `WBS_Planning` đọc `B2` làm cột ngày đầu tiên của Gantt.

## 3. `DauMucTaiLieuCanLam` — chọn hạng mục thiết kế cần làm
Bảng **lựa chọn "dùng/ không dùng" từng mục** của các sheet cho một Epic/ Use-case/ User-story/ Page/ Function/ Service.
| Cột | Cách điền |
|---|---|
| **STT** | 1.0 = `Component_Detail_Design`, 2.0 = `Function_RTM`, 3.0 = `Functions_Services_Detail_Desig` |
| **Tên Sheet** / **Nội dung cần phân tích** | Tên sheet và các mục con (xem dưới) — có sẵn, không gõ lại |
| **PM, QAO, EPIC Leader → Sử dụng (Yes/No)** | Epic này **có làm** mục này không |
| **→ Hiệu chỉnh so với mẫu (Yes/No)** | Có sửa cấu trúc mục so với mẫu gốc không |
| **→ Lý do thay đổi so với mẫu tài liệu gốc** | Bắt buộc điền nếu "Hiệu chỉnh = Yes" (vd mẫu: gộp mục 02 và 03 thành 01 vì biểu mẫu chưa hợp lý khi nhận nhiều yêu cầu của khách) |
| **SEPG Head → Phê duyệt thay đổi (Yes/No), Ghi chú** | Người phụ trách quy trình duyệt việc hiệu chỉnh |
| **Chú thích** | |
Mục con mẫu (mặc định "Sử dụng = Yes", riêng **UseCase Diagram = No** vì mặc định dùng User-Story Map): *Yêu cầu nghiệp vụ, Business Flow Diagram, Yêu cầu chức năng, luồng màn hình, Wire Frame, User-Story Map / Use-Case Diagram, Component Diagram, System/ Deployment Diagram, công nghệ mỗi layer, gói cài đặt; Function_RTM; Use-case hoặc User-story, giao diện, mô tả service, Sequence, ERD/ lớp, NFR, đánh giá tác động, công nghệ & cài đặt*.
Cuối sheet có hai vùng tự do: **II. Mục tiêu thiết kế chức năng hệ thống** (dòng 38) và **III. Mục tiêu thiết kế kiến trúc hệ thống** (dòng 61).
*(Bản Copilot thêm: "Đề xuất của Claude Code" [Đề xuất sử dụng, Lý do] và "Xác nhận của con người (File-based)" [Xác nhận, Ngày xác nhận].)*

## 4. `Component_Detail_Design` — thiết kế tổng quan (bức tranh lớn)
Sheet dạng **văn bản + vùng ảnh**, đánh số mục:
| Mục | Viết gì |
|---|---|
| **1.a Yêu cầu nghiệp vụ** | Gạch đầu dòng: hệ thống là gì, nguồn dữ liệu, người dùng làm được gì, tải/ sẵn sàng/ bảo mật ở mức nghiệp vụ |
| **1.b Luồng nghiệp vụ / Business Flow Diagram** | Dán **sơ đồ** (BPMN: pool/ lane) — vùng ~45 dòng |
| **2. Yêu cầu chức năng** | Danh sách việc phải thiết kế/ giao ra (màn hình, sequence, kiến trúc, tech stack…) |
| **3.a Luồng thiết kế màn hình** | Sơ đồ chuyển màn hình |
| **3.b Wire Frame** | Ảnh wireframe/ mockup |
| **3.c User-Story Map / Use-Case Diagram** | (i) Component Diagram, (ii) **Lựa chọn 1 – User-Story Map**, (iii) Lựa chọn 2 – Use-Case Diagram. Chọn một trong hai (khớp cột "Sử dụng" ở sheet chọn mục) |
| **4.a Component Diagram / 4.b System–Deployment Diagram** | Sơ đồ thành phần/ triển khai |
| **4.c System Architect** | Thiết kế kiến trúc hệ thống + *Migration/ Communication solution* (với hệ thống khác) |
| **4.d Software Architect** | (i) Tổng quan thiết kế phần mềm, (ii) Architect detail design cho từng layer |
| **5.a Công nghệ mỗi layer** | **Bảng:** `No` · `Layer` · `Description` · `Technical/Framework/Device` (một layer có nhiều dòng công nghệ) · `Explain` · `Description` · `Best practice` |
| **5.b Gói cần cài đặt** | Bảng: `No` · `Service/Function – No` · `Gói cần cài đặt` · `Mô tả/ Hướng dẫn/ File cài đặt` |
Layer ví dụ trong mẫu: Load balancer, WebApps, Brokers, WAS, Authen & Security, Account Manager, Logging, Log Analyze, Message Queue, Jobs, DB/ lưu trữ, Discovery & monitoring. **Cách viết:** mỗi layer ghi *công nghệ dùng* + *vì sao* (Explain) + *best practice* — đây là phần "What & Why" mà đề bài mẫu yêu cầu.

## 5. `WBS_Planning` — phân rã công việc, ước lượng, Gantt (có công thức!)
Đầu sheet: **Trong phạm vi** (A2) · **Ngoài phạm vi** (A4) · **Giả định** (A6) · **Đầu vào từ Stakeholders/ BA** (A8); bảng từ dòng 10–11.
| Cột | Ý nghĩa / cách điền |
|---|---|
| **A No** | ID dạng cây: nhóm `Cawling_1`, task `Cawling_1-1.1`, `Cawling_2-2.1`… (dùng làm khóa cho cột `Pre`) |
| **B Task** | Tên task (dòng cha = nhóm việc) |
| **C Notes/ Assumptions/ Description/ Result/ Links** | Mô tả, giả định, kết quả, link tham khảo |
| **D Est (MH)** | Ước lượng **man-hour** — nhập tay ở dòng con; **dòng cha là `=SUM(con)`** |
| **E Est (MD)** | `=D/6.4` (**1 man-day = 6,4 giờ**) |
| **F Pre** | ID **task tiền nhiệm** (task chỉ bắt đầu sau khi tiền nhiệm xong) |
| **G Assignee** | Người làm |
| **H Start Date** | Dòng cha: `=min(con)`. Task **không có Pre** → công thức lấy `PJT_Definition!B3`; **có Pre** → `WORKDAY(start tiền nhiệm, duration tiền nhiệm)`. Có thể nhập tay ngày bắt đầu cụ thể |
| **I Due Date** | `=WORKDAY(H, Duration-1)` (bỏ cuối tuần); cha: `=max(con)` |
| **J Duration** | `=E` (số ngày công) |
| **K Status**, **L PCT of Task Complete** | Trạng thái; % hoàn thành (1 = 100%) |
| **M Task Color** | Màu thanh Gantt; kế thừa từ task tiền nhiệm bằng `VLOOKUP`, hoặc nhập số màu |
| **N… (timeline)** | Các ngày làm việc liên tiếp tính từ `PJT_Definition!B2`, **bỏ thứ 7/ chủ nhật** — vùng vẽ Gantt |
| **BW… RACI** | Mỗi người một cột (mẫu: Mai Hà, Đông, Linh, Nam, V.Phong, N.Phong, Hương) — ghi R/A/C/I |
| **CF… Objectives** | Mục tiêu theo task |
→ **Chỉ nhập** các ô trắng (`No, Task, Notes, Est MH, Pre, Assignee, Status, PCT`); **không ghi đè ô công thức** (E, H, I, J, M, timeline).
*(Bản Copilot dùng WBS **đơn giản hơn**, không Gantt: `Layer, isTask, STT, Nhóm chức năng, Task, Ước lượng (MH/USP/UCP), Notes/Assumptions, Mục tiêu/ Kết quả mong đợi, Liên kết Component_Detail_Design, User-Story/Use-Case, Liên kết Function_RTM (No.), Trạng thái [Chưa bắt đầu/ Đang làm/ Chờ xác nhận/ Hoàn thành/ Chặn], Người duyệt, Ngày duyệt` — chia theo nhóm I Front-End/ II…; mỗi task nhỏ, ghi DoD.)*

## 6. `Actors_Peronas` — tác nhân / chân dung người dùng
Mỗi tác nhân **một khối cột**: hàng `Avatar` (dán ảnh — ghi chú "Copy Avatar From Here →"), `Name` (tên vai trò), `Description` (mô tả: vai trò, mục tiêu, thói quen; dạng gạch đầu dòng). Mẫu có 6 khối (Admin, Payment Manager, Basic/ Standard/ Free User, Cosmo Spencer) với chữ giả "Lorem ipsum" — **thay bằng nội dung thật**. Bản Copilot dùng: User, AI-Agent-Service, AI-Generator-Services, Memory-Storage-System, Business-Services (tác nhân là hệ thống).

## 7. `Function_RTM` — ma trận truy vết yêu cầu
Đầu sheet: tiêu đề, **Mã yêu cầu** (vd `P-06-002`), **Người thực hiện/ EPIC Leader**.
| Cột | Ý nghĩa |
|---|---|
| **Layer 1–5 (A–E)** | Đánh dấu **cấp phân rã** của dòng (1 = nhóm lớn như Front-End/ Backend-API/ Tools/ Services; 2, 3… = nhóm con; 5 = cấp sâu nhất) |
| **F No.** | Số thứ tự trong nhóm (cấp lá) |
| **G Yêu cầu** | Tên yêu cầu/ chức năng |
| **H Description/ GitLab Project's link** | Mô tả hoặc link repo GitLab |
| **Requirement and Design Documents:** I **BRD Reference** · J **SRS Reference/ Sheet URL** · K **UI Reference** · L **SS Reference** | Tham chiếu tài liệu nghiệp vụ, đặc tả (link tới Google Sheet này), giao diện, tài liệu thiết kế hệ thống |
| **Coding:** M **PS Reference** · N **Code Reference** | PS = *Program Structure Specification* (ghi chú ở H61 của mẫu: "-Program Structure Specification" là một phần tên file PS); Code = đường dẫn/ commit/ MR |
| **Testing:** O **Unit Test** · P **Integration Test** · Q **System Test** · R **User Acceptance Test Reference** | ID test case/ file test tương ứng |
Cách dùng: **mỗi chức năng một dòng ở cấp lá**, điền đủ đường từ yêu cầu → thiết kế → code → test. Dòng nào thiếu tham chiếu = lỗ hổng truy vết (chính là chỗ QA/ reviewer kiểm tra).
*(Bản Copilot thêm: `ADR Reference`, `Risk Reference (Risk_Register)`, `Trạng thái dòng`, `Xác nhận của con người (File-based) Yes/No`, `Ngày xác nhận`.)*

## 8. `Functions_Services_Detail_Desig` — thiết kế chi tiết từng chức năng/ service (sheet quan trọng nhất)
Dùng cho **một cửa sổ/ service/ user-story/ use-case**. Sáu phần:

**1. Mô tả Use-case** — chọn một: 
- **(a) Use-Case** — bảng: `TT` (B.1…) · `Tên Use-Case` · `Mô tả` · `Tên tác nhân chính` · `Tên tác nhân phụ` · `Tiền điều kiện` · `Mô tả trường hợp` gồm 3 cột **Luồng chính (hoặc Sequence Diagram) | Luồng thay thế | Luồng ngoại lệ** (mỗi bước một dòng, đánh số "1.1, 1.2…") · `Điều kiện sau khi hoàn thành` · `Mức độ cần thiết` (A/B/C) · `Mức độ của UC` · `Phân loại` (nhãn mỗi bước, vd "Dữ liệu đầu ra"). **Công thức:** *Mức độ của UC* tự tính theo **số bước (dòng)** của use-case: ≤3 = Đơn giản, 4–7 = Trung bình, >7 = Phức tạp — vì vậy đừng bỏ trống cột TT/ ID ở dòng đầu, các dòng bước phía dưới sẽ tự gắn vào use-case đó.
- **(b) User-Story** — `As a [role], I want to [goal] so that [benefits].` + **Acceptance Criteria** (A/C đánh số 1., 2., 3.; ví dụ mẫu: admin vô hiệu hóa user bị báo cáo).

**2. Thiết kế giao diện** — (a) **Mô giao diện người dùng**: ảnh giao diện + cột **Business Rules** (từng nút/ vùng: tìm kiếm nhanh, tìm nâng cao, phân trang, Add/Delete, ràng buộc dữ liệu liên quan như Tỉnh–Quận–Xã…); (b) **Mô tả service**: (i) danh sách service + mô tả chức năng; (ii) **từng service** gồm:
  - `REQUEST PARAM`: `PATHNAME` (vd `/quanlyhocvien/themmoihocvien`), `Method` (POST…), bảng `No · Param · Type · Duplicate · Mandatory (O) · Sample value · Description · Remark`;
  - `REQUEST SAMPLE` (JSON); `RESPONSE FIELD` (`FORMAT` JSON + bảng cùng cột `Item New…`); `RESPONSE SAMPLE` (JSON).

**3. Diagram** — (a) **Sequence Diagram** (bỏ qua nếu đã đưa vào use-case) + **Activities Diagram** (ảnh); (b) **ERD/ Biểu đồ lớp**.

**4. Yêu cầu phi chức năng** — bảng `TT · Yêu cầu · Mô tả · Giải pháp`: Hiệu năng (vd tải trang <2 giây, 1000 đăng nhập/phút), Bảo mật (mã hóa mật khẩu, chống SQL injection/ brute-force), Khả năng sử dụng, mã hoá dữ liệu, xác thực giao dịch, chống đánh lừa giao dịch, lưu nhật ký.

**5. Đánh giá tác động** — (a) **Các cấu phần kích hoạt code:** dev rà toàn bộ source (FE/ BE), liệt kê cấu phần (API mới…) và đánh dấu *"có thay đổi do yêu cầu phát triển?"*; (b) **Mức độ rủi ro:** bảng loại cấu phần thay đổi — *Source code, Library, Config/ Environments, Assets, Infrastructure* — mỗi loại ghi **Có/ Không thay đổi**, mô tả, ghi chú.

**6. Công nghệ sử dụng & yêu cầu cài đặt** — giống mục 5 của `Component_Detail_Design` (bảng công nghệ theo layer + gói cần cài).

## 9. `TDD-TestScenario` — kịch bản kiểm thử
Một sheet **cho một kịch bản** (đặt tên tiêu đề: vd "Kịch bản kiểm tra đa ngôn ngữ (i18n)"):
- **I. Yêu cầu kiểm thử:** 1. **Trình tự kiểm tra** (mô tả bằng gạch đầu dòng + sơ đồ luồng); 2. **Site map cần kiểm tra** (các trang phải đi qua).
- **II. Test planning and Assignment:** bảng `No · Module · Note · Estimate · Assign · Note` — chia việc kiểm thử theo module (ước lượng có công thức cộng nhóm, vd `=sum(D88:D116)`).
- **Bản Copilot** thêm dạng **Happy Path**: bảng `No · Thứ tự luồng (Bước 1…) · Test Case ID (HP_01, EC_05…) · Hành động của người dùng (UAT Tester) · Kết quả mong đợi (User Perspective)` — đúng tinh thần viết happy case "ngôn ngữ giao diện" (`.ai-rules/quy-trinh/qa-process.md`).

## 10. `TDD_TestCases` — danh sách test case (có dropdown)
| Cột | Cách điền |
|---|---|
| **ID issues** | Số thứ tự/ ID issue liên quan |
| **ID testcase** | Mẫu: `UAT_1`, `UAT_2.1`; bản Copilot: `HP_01` (happy path), `EC_05` (edge case) |
| **Name** | Tên ngắn "Kiểm tra …" |
| **Summary** | Mô tả mục đích |
| **Step** | Các bước đánh số 1., 2., 3. |
| **Expected results** | Kết quả mong đợi quan sát được |
| **Trạng thái test** | **Dropdown: `Pass` / `Fail` / `Not run`** (ô `G1:G5`) |
| **Trạng thái dev xử lý** | Vd "Đã xong" |
| **Ghi chú** | Xác nhận lại/ thay đổi sau khi trao đổi |
| *(bản Copilot)* **Use-Case Reference (ID)**, **Acceptance Criteria Ref** | Truy vết test → use-case → tiêu chí chấp nhận |
→ Khi import vào **TestLink** dùng mẫu XML ở `.ai-rules/quy-trinh/templates/` (mỗi bước một `<step>`); sheet này là bản làm việc/ báo cáo.

## 11. Các sheet chỉ có ở bản Copilot (mở rộng, không có trong mẫu v3.0)
| Sheet | Dùng để | Cột |
|---|---|---|
| **UserStories** | Bảng user story theo chức năng chính, ngoài ra chia phần "bên thứ 3 làm / team tự làm" (đặc thù AI) | STT · Link Use-Case · Chức năng · AI bên thứ 3 đảm nhiệm (% ) · phần team tự phát triển (%) · Ghi chú MVP |
| **Use-Case0X-…** | Mỗi use-case một sheet theo đúng khuôn mục 8.1(a) | như trên |
| **Risk_Register** | Sổ rủi ro (PMP) | STT · Risk ID (`RISK-01`) · Liên kết WBS Task · Liên kết Use-Case/ US · Mô tả rủi ro · Mức ảnh hưởng (Cao/TB/Thấp) · Xác suất · Hướng xử lý (Mitigation) · Rủi ro thứ cấp · Trạng thái · … |
| **ADR_Log** | Quyết định kiến trúc (≈ CMMI DAR) | STT · ADR ID (`ADR-01`) · Ngày · Liên kết (Function_RTM No./ Component) · Bối cảnh · Lựa chọn A/B/C kèm điểm · Tiêu chí & trọng số · Giải pháp được chọn · Lý do · Hệ quả |
| **Test_Execution_Report** | Báo cáo thực thi test (tổng hợp tự tính: số chạy/ Pass/ Fail/ % Pass) | STT · Ngày · Loại (Unit/ Integration/ System/ UAT) · Test Case/ Scenario ID · Liên kết UC/US · Mock/Sample Data (link JSON) · Kết quả · Log file (đưa lên ELK) · Người/ hệ thống thực thi · Ghi chú lỗi |

## 12. Thứ tự điền khi viết tài liệu cho **một chức năng** (đề xuất theo quy trình công ty)
1. `PJT_Definition` (một lần) → `DauMucTaiLieuCanLam` (chọn sheet/ mục dùng; lý do nếu chỉnh mẫu).
2. `Actors_Peronas` (tác nhân liên quan) → `Component_Detail_Design` 1–3 (nghiệp vụ, luồng, wireframe, user-story map).
3. `Functions_Services_Detail_Desig` cho chức năng đó: use-case **hoặc** user-story + A/C → giao diện + Business Rules → service/ API (param, sample) → sequence/ ERD → NFR → đánh giá tác động.
4. `WBS_Planning` (task, ước lượng MH, Pre, Assignee) → `Function_RTM` (một dòng/ chức năng, điền BRD/ SRS/ UI/ SS… đến test).
5. `TDD-TestScenario` → `TDD_TestCases` (happy case trước; ID liên kết use-case/ A/C) → TestLink.
6. Mỗi lần sửa: `NhatKyThayDoi`. Cuối kỳ: `Test_Execution_Report`, `Risk_Register`, `ADR_Log` (nếu dùng bản mở rộng).

## 13. Áp dụng cho GDT Accounting (gợi ý, **chưa chốt** — cần người dùng/ team quyết)
- SRS hiện tại (Google Doc `doc/yeu-cau/project-doc`) viết theo **Business Process → Mockup → User Story + A/C + BR → NFR → nghiệm thu**; khi chuyển sang mẫu này: *Yêu cầu nghiệp vụ/ business flow* → `Component_Detail_Design` 1; *mockup* → 3.b Wire Frame; *User Story + A/C + BR* → `Functions_Services_Detail_Desig` mục 1(b) + 2(a) Business Rules; *AC-xx nghiệm thu* → cột `Acceptance Criteria Ref` của `TDD_TestCases`.
- API thật của `accounting-service` (đường dẫn `/api/v1/...`, request/ response) điền vào mục 2(b) từng service — lấy từ code/ OpenAPI, **không đoán**.
- Mã trạng thái đơn dùng đúng `doc/thiet-ke/05-process-status`.
- Việc cần quyết trước khi viết: (1) ID dùng cho use-case/ user story; (2) dùng WBS có Gantt (mẫu) hay WBS đơn giản (Copilot); (3) có dùng các sheet mở rộng (Risk, ADR, Test_Execution) không; (4) ngôn ngữ (tiếng Việt như hiện tại).

---

# 14. Bài học từ file đã điền thật `_SRS_FDD_AI-Agent-Copilot.xlsx` (đọc toàn bộ ngày 2026-10-17)

## 14.1 Đây là dự án gì
**Embeddable Chat Widget** (frontend, ES Modules, không bundler) cho AI-Agent tạo nội dung của Toktak: người dùng chat → AI hỏi lại → form động (CustomForm, 24 loại `input_type`) → sinh kịch bản. Một use-case chính **UC-01 "Viết kịch bản tạo nội dung"** (User Story `US_01`, 13 story point, 6 tiêu chí AC), **14 task WBS** (13 task có ước lượng, tổng **71 man-hour**), 5 service backend (`/chat/send` Case 1–2, `/chat/history`, `/chat/search`, `/chat/interaction/context/<id>`, `/chat/interaction/feedback`). Test: `node --test` (unit/ integration) + kịch bản Playwright (tham khảo), backend thật chạy `localhost:8000`.
File này **không phải bản nộp một lần mà là tài liệu sống do Claude Code cập nhật theo từng task**, có "cổng" con người xác nhận. Quy trình chi tiết nằm ở các file **ngoài** workbook mà file này viện dẫn: `SDLC_WORKFLOW.md` (vòng lặp §2.8(c), quy tắc đánh số RTM §5.4, mục 0.3 định nghĩa Layer), `RTM_SHEETS_GUIDE.md` (mục 10), `CLAUDE.md` (thứ tự đọc 15 file `.md`), `ARCHITECTURE.md`, `API_SPEC.md`, `CUSTOM_VIEW_SPEC.md`, `CHATBOT_BEHAVIOR.md`, `COMPONENT_CONTRACT.md`, `WIDGET_EMBED.md`, `PROJECT.md`. **Các file này không có trong máy** (đã tìm) — nên xin từ người dùng nếu muốn áp dụng đúng quy trình đó.

## 14.2 Vòng lặp làm việc (suy ra từ `NhatKyThayDoi` 16 dòng + các sheet)
1. **AI đọc hết tài liệu** (docs `.md`, RTM, skill) theo thứ tự quy định, rồi tóm tắt (`CLAUDE_ONBOARDING_SUMMARY.md`) và **ghi nhật ký**.
2. **AI đề xuất**, không tự quyết: đề xuất task vào WBS (viết lại mô tả, ghi câu hỏi làm rõ vào cột Notes) → **con người duyệt** (điền `Người duyệt` + `Ngày duyệt` ở WBS) rồi mới được code.
3. **Mỗi lần chỉ làm đúng 1 task, theo thứ tự STT.** Phát hiện lỗi ở task cũ (đã Hoàn thành) → **không tự sửa**, ghi vào `Risk_Register` và báo (ví dụ RISK-02: backend trả 500 ngẫu nhiên ở Service 4).
4. Làm xong task → cập nhật **cả một chùm**: code + unit test (ID `UT_xx`/`EC_xx`) → `TDD_TestCases` → `TDD-TestScenario` (mục theo task) → `Function_RTM` (từng file code một dòng) → `Test_Execution_Report` (kèm log file) → `NhatKyThayDoi` → (nếu có quyết định kỹ thuật) `ADR_Log`.
5. **Dừng, chờ xác nhận của con người** ở `Function_RTM` (Yes + ngày) và `WBS.Trạng thái = Hoàn thành`. Xác nhận qua chat **không** thay thế; chỉ xác nhận **bằng file**. Nhật ký ghi rõ "xác nhận qua chat, chưa có xác nhận file-based (GATE)".
6. UI task: AI khởi động server local để **người dùng tự smoke-test/ UAT**, không tự ghi Pass cho phần cần mắt người.

## 14.3 Từng sheet được dùng thực tế ra sao (khác/ cụ thể hơn mẫu)
| Sheet | Cách dùng thực tế |
|---|---|
| `NhatKyThayDoi` | Mỗi lần làm là **một dòng dài** (làm gì, file nào, bao nhiêu test pass, quyết định gì), cột `Liên quan đến` ghi `UC-01…; WBS Task n; ADR-02`, `Trạng thái duyệt` Draft/Approved. Dùng cả để ghi lại điều đã thống nhất qua chat (để lưu vết) |
| `DauMucTaiLieuCanLam` | Thêm 2 cụm cột: **"Đề xuất của Claude Code"** (đề xuất Yes/No + lý do) và **"Xác nhận của con người (File-based)"** (Yes/No + ngày). Ví dụ: `Component_Detail_Design` đề xuất **No** vì nội dung hiện chỉ là mẫu không liên quan → **tạm dùng `ARCHITECTURE.md` (as-built) làm căn cứ thiết kế**; người dùng xác nhận 18/08/2026 |
| `Component_Detail_Design` | **Để nguyên mẫu "News System"**, không dùng (đúng như bản đề xuất ở trên). Thiết kế thật nằm ở các file `.md` |
| `Use-Case01-…` (thay cho `Functions_Services_Detail_Desig`) | Cùng khuôn nhưng **mở rộng**: mục 1 Use-case (UC-1, luồng chính/ thay thế/ ngoại lệ đánh số `1.1, 1.2…`; tác nhân phụ là các Node hệ thống), **2 User Story** (`US_01`, Title, As a/I want/So that, Story Points), **3 AC 1–6** (mỗi AC có tên + điều kiện kiểm chứng), **4 DoR** (UI/UX, Technical docs, Prompt Engineering, Dependencies), **5 DoD** (Code Quality, Testing, Acceptance, Performance, Documentation), **6 User Story Map** (Hoạt động → Nhiệm vụ → Release 1 MVP / Release 2), 7 ERD, **8 Giao diện + API** (mockup + Business Rules; từng service với PATHNAME/ Method/ bảng param/ REQUEST SAMPLE/ **lệnh curl thử**/ RESPONSE FIELD/ RESPONSE SAMPLE; Case 2 chia 4 bước), 9 NFR, 10 Đánh giá tác động (liệt kê cấu phần kích hoạt code, Source/Library/Config/Assets/Infra), 11 Công nghệ |
| `WBS` (bản gọn, thay `WBS_Planning`) | Layer I/ I.1/ I.2… (nhóm chức năng → gói) + dòng task (`isTask = x`); mỗi task: mô tả chi tiết **kèm điều kiện đã làm rõ**, ước lượng MH, Notes/Assumptions, **Mục tiêu/ Kết quả mong đợi** (file cần tạo, test phải xanh), **Liên kết Component_Detail_Design** (thực tế trỏ tới mục trong `.md`), `User-Story/Use-Case`, **`Liên kết Function_RTM (No.)`** (vd `#2.1…#2.5`), Trạng thái 5 mức, Người duyệt, Ngày duyệt. Không có Gantt/ công thức ngày |
| `Function_RTM` | **Mỗi file code/ hàm một dòng**: `No` dạng `<STT task WBS>.<chỉ số con>` (vd `3.4`; cấp trên là dòng tiêu đề task); `Yêu cầu` mô tả ngắn + (WBS Task n); `Description/ GitLab link` = **đường dẫn file**; `SRS Reference` = mục trong `.md` (vd `API_SPEC.md §2`); `Code Reference` = đường dẫn; **Unit Test Reference = file test + dải ID + số thứ tự trong `TDD_TestCases`** (vd `…test.js (UT_08-UT_11) — TDD_TestCases#20-23`); Integration/ System test = mục `TDD-TestScenario`; `ADR/Risk Reference`; `Trạng thái dòng` = "**Đã đối soát git**"; `Xác nhận (Yes/No)` + ngày. Trong code có header `@rtm-ref` để đối chiếu hai chiều RTM ↔ code |
| `TDD_TestCases` | ~96 dòng: **I. Happy Path (HP_xx), II. Edge Cases (EC_xx), III. Unit Test Specs, rồi IV–IX Unit Test Specs theo từng Task**; cột ID testcase có 3 loại `HP_`/`EC_`/`UT_` (≈ 6 / 12 / 68); `Use-Case Reference`, `Acceptance Criteria Ref` (ghi `N/A (infra/UI khung…)` khi không gắn trực tiếp AC); Trạng thái test `Pass`, dev `Done` |
| `TDD-TestScenario` | I. Happy Path (bảng Bước ↔ Test Case ID ↔ hành động của UAT tester ↔ kết quả mong đợi **theo góc nhìn người dùng**), II. Kịch bản lỗi/ dữ liệu rác (EC_01…06), **III–IX: mỗi task một khối**, thêm 2 cột `Playwright action()` / `assertion()` (kịch bản tham khảo; có ghi chú "chưa cài harness E2E, xác nhận bằng smoke-test tay"), kèm ghi chú đã smoke-test bằng backend thật |
| `Test_Execution_Report` | Một dòng mỗi lần chạy: ngày, loại (Unit/ Integration/ UAT-Manual), ID test, liên kết task, mock data (link JSON hoặc "N/A — inline"), **kết quả**, **đường dẫn log** (`logs/2026-08-20_task1_….log`), người chạy ("Claude Code (node --test)" hoặc "Claude Code + người dùng (smoke-test tay)"); phần tổng hợp Pass/Fail/% tự tính |
| `Risk_Register` | `RISK-01…`, liên kết WBS Task + Use-case, ảnh hưởng/ xác suất (Cao/TB/Thấp), mitigation, **rủi ro thứ cấp của chính mitigation**, trạng thái, người phụ trách, ngày cập nhật |
| `ADR_Log` | `ADR-01…`; **3 lựa chọn A/B/C có điểm**, tiêu chí có **trọng số** (vd "đơn giản hoá dev-workflow ×2"), lý do, hệ quả, và cột "**ÁN TẠI HỒ SƠ** — xác nhận con người Yes/No + ngày" |
| `UserStories` | Bảng 9 chức năng chính (input, hỏi lại đa lượt, lập kế hoạch, tool calling, nhất quán, cá nhân hoá, bảo mật/ thanh toán, output real-time, bộ nhớ) kèm `US/UC-1.1…`; **chia % phần do AI bên thứ 3 / do team** (đặc thù sản phẩm AI) |
| `Actors_Peronas` | Tên 5 tác nhân (User, AI-Agent-Service, AI-Generator-Services, Memory-Storage-System, Business-Services) nhưng **mô tả vẫn là "Lorem ipsum"** |

## 14.4 Điểm "chưa chỉnh" cần tránh khi viết cho GDT Accounting
- `Actors_Peronas` còn chữ giả; `Use-Case…` mục **9 NFR** và **10–11** vẫn giữ nguyên chữ của mẫu ("tải trang <2 giây; 1000 đăng nhập/phút", "mật khẩu được mã hóa"…) → **không sao chép NFR/ công nghệ mẫu**, phải viết theo hệ thống thật.
- `Component_Detail_Design` bỏ không dùng (có lý do ghi trong `DauMucTaiLieuCanLam`) — nếu bỏ sheet nào thì **ghi lý do ở đó** như vậy.
- Định dạng ngày trộn nhiều kiểu (`17/8/26`, `18/08/2026`, `2026-09-11`) → chọn **một kiểu** (đề xuất `dd/mm/yyyy`).
- `ADR-01` còn "VD" và `Function_RTM#--` — đừng để dòng ví dụ trong bản chính thức.

## 14.5 Áp dụng cho GDT Accounting — đề xuất cụ thể
- **Mỗi chức năng một `US_xx`/ `UC-xx`**, có A/C đánh số (lấy từ SRS: `AC-01…AC-25`), DoR/ DoD đúng 5 hạng mục trên.
- Kết nối với các thứ đã có: `Process Status` (05) → mã trạng thái trong A/C; `Cột hiển thị` (06) → Business Rules phần giao diện; `Master data` (07) → ràng buộc dữ liệu; mockup (03) → mục "Mô giao diện".
- Với code của `accounting-service`: RTM **một dòng mỗi controller/ service/ test** (đường dẫn thật), `Unit Test Reference` = tên lớp test thật (không đoán), gắn mã test case TestLink nếu có.
- Muốn **AI viết tài liệu theo đúng quy trình trên** → cần thêm `.ai-rules/quy-trinh/quy-trinh-tong-the.md` (vòng lặp đề xuất → người duyệt bằng file → 1 task/ lần → cập nhật chùm sheet → chờ xác nhận); nên có `SDLC_WORKFLOW.md` gốc của dự án Copilot để bám đúng thay vì suy đoán.
