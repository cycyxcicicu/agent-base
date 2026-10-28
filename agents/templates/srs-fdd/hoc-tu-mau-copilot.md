# Học từ file mẫu đã điền: SRS_FDD AI-Agent-Copilot

Nguồn: `doc/quy-trinh/template/04-srs-fdd-copilot-da-dien/goc/_SRS_FDD_AI-Agent-Copilot.xlsx` (14 sheet, 13 hình). Đây là bản đã điền thật của một dự án khác, dùng làm mẫu về cách trình bày. Đọc ngày 18/10/2026, đọc hết chữ và xem cả 13 hình. Đọc file này trước khi dựng hoặc sửa file Excel SRS_FDD của dự án.

## 1. Các sheet và việc của từng sheet

| Sheet | Việc | Ghi chú cách làm |
|---|---|---|
| NhatKyThayDoi | Nhật ký sửa tài liệu | Thêm cột "Liên quan đến (Use-Case/Component ID)" và "Trạng thái duyệt (Draft/Approved)" |
| DauMucTaiLieuCanLam | Chọn mục thiết kế nào dùng | Mỗi mục có Yes/No, lý do đổi so với mẫu, phê duyệt của SEPG, đề xuất của AI và xác nhận của người |
| Component_Detail_Design | Thiết kế tổng thể: nghiệp vụ, kiến trúc, công nghệ | 5 hình, xem mục 2 |
| WBS | Chia việc theo lớp | Mỗi task có mục tiêu, liên kết Component, Use-Case, RTM, trạng thái, người duyệt |
| Function_RTM | Ma trận truy vết yêu cầu | |
| Actors_Peronas | Tác nhân | |
| UserStories | Danh sách user story, phần việc bên thứ ba và tự làm | Có tỷ lệ phần trăm, ghi chú cho MVP |
| Use-Case01-... | Thiết kế chi tiết một use-case | 6 hình, xem mục 3. Mỗi use-case một sheet |
| TDD-TestScenario | Kịch bản test, nhóm Happy Path trước | Cột: thứ tự luồng, mã case, hành động của người test, kết quả mong đợi |
| TDD_TestCases | Từng case | Cột: mã case, tên, tóm tắt, bước, kết quả, trạng thái test, trạng thái dev xử lý, tham chiếu Use-Case và tiêu chí chấp nhận (AC) |
| Risk_Register | Sổ rủi ro | Mã rủi ro, liên kết WBS và Use-Case, ảnh hưởng, xác suất, hướng xử lý, rủi ro thứ cấp, trạng thái |
| ADR_Log | Quyết định kiến trúc | 3 phương án A, B, C, mỗi phương án có điểm; tiêu chí và trọng số; phương án chọn, lý do, hệ quả; người xác nhận |
| Test_Execution_Report | Tổng hợp kết quả chạy test | Ô tổng hợp tự tính từ bảng chi tiết |
| 20210620 | Mô tả một màn hình (kiểu Nhật) | Xem mục 4 |

## 2. Component_Detail_Design: thứ tự mục và 5 hình

Thứ tự: 1. Yêu cầu nghiệp vụ (a. mô tả, b. luồng nghiệp vụ) · 2. Yêu cầu chức năng · 3. Thiết kế tổng quan luồng chức năng (luồng màn hình, wireframe, bản đồ user story hoặc use-case diagram) · 4. Thiết kế hệ thống (a. component, b. deployment, c. system architect, d. software architect gồm tổng quan và chi tiết từng lớp) · 5. Công nghệ mỗi lớp (a. bảng lớp, mô tả, công nghệ, giải thích, best practice; b. các gói cần cài).

| Hình | Vẽ gì | Cách đọc |
|---|---|---|
| Luồng nghiệp vụ tổng quát | Sơ đồ các khối (người dùng, front-end, back-end, AI Agent, cache, DB, admin), mũi tên có số 1 đến 13 | Số thứ tự là thứ tự luồng. Mỗi số có giải thích ở sheet |
| Sơ đồ chức năng theo module | Khung lớn "AI Content Generators", "AI Agent", "System", "ML", "Data"; trong mỗi khung là các component nhỏ | Cho thấy module nào chứa component nào, module nào nói chuyện với module nào |
| Component theo lớp | Các lớp: Interaction, Orchestrator, Existing components, dịch vụ ngoài (AWS) | Dấu tích xanh đánh dấu phần đã có hoặc làm trước |
| Package và component chi tiết | Cây package (agents, core, apps, db, config) tới từng class; 12 bước đánh số ở phía trên; hai khung chữ "chức năng cần chuyên sâu" và "API cần xây dựng" | Hình lớn, có chú thích chữ ngay trong hình |
| Luồng theo đội | Khung chấm chấm theo đội (Data, ML, AI, Content), mũi tên đánh số | Dùng để chia việc theo đội |

## 3. Use-Case01: thứ tự mục và 6 hình

1. Mô tả use-case: bảng một dòng (tên, mô tả, tác nhân chính và phụ, tiền điều kiện, luồng chính, luồng thay thế, luồng ngoại lệ, điều kiện sau, mức cần thiết, mức độ, phân loại). Luồng chính đánh số 1.1, 2.1... luồng thay thế ghi "2.1 Nếu thiếu thì ...".
2. Sequence diagram, Activity diagram, Data flow diagram: ba hình xếp dọc, mỗi hình có cột "Ghi chú" bên phải đánh số.
3. User story: ID, Title, As a, I want to, So that, Story Points.
4. Tiêu chí chấp nhận: AC 1, AC 2... mỗi AC có tên ngắn trong ngoặc, ví dụ "AC 1 (Nhận diện loại nội dung)".
5. Definition of Ready (đã có mockup, tài liệu API, prompt đã thử, môi trường sẵn sàng) và Definition of Done (code review, unit test và integration test, QA xác nhận trên staging, ngưỡng hiệu năng, cập nhật tài liệu).
6. User Story Map: hàng Hoạt động, Nhiệm vụ, rồi Release 1 (MVP), Release 2.
7. ERD hoặc biểu đồ lớp: một hình, sau đó mỗi bảng một khối "b.1, b.2..." gồm bảng cột: No, Cột, Kiểu dữ liệu, Giải thích, Dùng làm gì, Ghi chú hoặc Index khuyến nghị.
8. Thiết kế giao diện và API: "Mô giao diện" (hình wireframe có chú thích) rồi "Mô tả service".
9. Yêu cầu phi chức năng: bảng Yêu cầu, Mô tả, Giải pháp.
10. Đánh giá tác động: (a) các cấu phần kích hoạt code, (b) mức độ rủi ro theo Source code, Library, Config, Assets, Infrastructure.
11. Công nghệ và gói cài đặt.

| Hình | Vẽ gì |
|---|---|
| Sequence | Cột người dùng, UI, API, các Node, trạng thái agent, AI. Chia thành các "transaction" bằng khung bên trái có ghi mục tiêu ("Lặp lại cho đến khi ..."). Mỗi thông điệp đánh số 1.1, 1.2 ... 5.2 |
| Activity | Bơi làn (User, ChatUI, các Agent, BE, LLM). Có Start, End, hình thoi, nhãn nhánh Y/N, vòng lặp "chưa đạt" |
| Data flow chi tiết | Các bước đánh số 1 đến 4, mỗi bước kèm đoạn chữ mô tả đầu vào, xử lý, đầu ra; bên cạnh là các class dữ liệu (AgentState, UserProfile...) |
| ERD và class | Hai nhóm khung (MongoDB, AgentState), quan hệ 1-1, 0..n, mỗi bảng liệt kê cột và kiểu |
| Wireframe có chú thích | Màn hình giữa, xung quanh là các khung chữ giải thích quy tắc, mũi tên tới ô số 1 đến 7 là API |
| Danh sách API | Một khối "Chat-Form" nối ra từng endpoint, mỗi endpoint có số, tên và đoạn mô tả |

Mỗi service mô tả theo một khuôn cố định: tên service và mục đích, các case, rồi cho mỗi case: REQUEST PARAM (đường dẫn, method, bảng No, Param, Type, Duplicate, Mandatory, Sample value, Description, Remark), REQUEST SAMPLE (có lệnh curl chạy thử), RESPONSE FIELD (bảng cột tương tự), RESPONSE SAMPLE. Case nhiều bước viết từng bước "Case 2 - Bước 1, Bước 2...".

## 4. Sheet mô tả một màn hình (kiểu Nhật, sheet `20210620`)

Khung: Screen ID, tên màn, người cập nhật, ngày · Screen Image (ảnh màn, kèm hình khung đánh số các ô) · Wireframe (link Figma) · Feature Requirements (song ngữ) · Related issues · Screen Items (bảng: No, tên ô, loại ô như Label, Textbox, Listbox, Button, Link, IOE là Input hay Output hay Event, bắt buộc, kiểu dữ liệu, số ký tự min max, giá trị mặc định, ghi chú) · Data Source (ô nào ghi vào API nào, khoá) · Event (với mỗi ô: sự kiện click, focus out; từng trường hợp 1), 2), 3) và hành vi từng nhánh: chuyển màn, gọi API, hiện thông báo lỗi hay thành công, trạng thái ô) · Notices.
Thông báo lỗi và thành công ghi nguyên văn, kèm loại hiển thị (Snackbar trái, Error hoặc Success).

## 5. Quy tắc trình bày rút ra

1. Mỗi hình đặt đúng dưới tiêu đề mục của nó, bên cạnh có cột ghi chú đánh số khớp với số trong hình.
2. Hình nào cũng có số thứ tự trong hình và lời giải thích cùng số bên cạnh, không để hình trơ.
3. Luồng nhiều bước chia thành transaction, mỗi transaction có mục tiêu và điều kiện lặp.
4. Mô tả API theo đúng khuôn 4 phần (tham số, mẫu gửi, trường trả về, mẫu trả về) và có lệnh chạy thử.
5. Mỗi cột bảng dữ liệu có hai cột "Giải thích" (là gì) và "Dùng làm gì" (để làm gì), thêm cột index.
6. Tiêu chí chấp nhận có nhãn ngắn và được tham chiếu từ test case (cột Acceptance Criteria Ref).
7. Có Definition of Ready và Definition of Done cho mỗi story.
8. Phần đề xuất của AI luôn đi kèm cột xác nhận của người và ngày xác nhận.

## 6. Khác với bản Excel hiện tại của dự án (`doc/srs/xlsx/SRS_FDD_UC-01_UC-02.xlsx`)

Có sẵn tương đương: component, sequence, class, ERD từng màn, activity, bảng happy case.
Chưa có: use-case diagram hoặc user story map, deployment diagram, kiến trúc phần mềm theo lớp, bảng công nghệ theo lớp và gói cài đặt, wireframe có chú thích kèm số API, mô tả API theo khuôn 4 phần, sheet mô tả màn kiểu Screen Items và Event, Definition of Ready và Done, Risk_Register và ADR_Log đủ cột, Test_Execution_Report.
Chưa đưa vào kế hoạch: sheet `UserStories` kiểu phần việc bên thứ ba (đặc thù dự án AI).
