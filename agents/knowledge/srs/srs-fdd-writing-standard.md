# Chuẩn viết tài liệu thiết kế theo mẫu SRS_FDD (cho AI)

Áp dụng khi người dùng bảo **viết tài liệu cho chức năng cần làm** theo mẫu `SRS_FDD_Template-v3.0.xlsx`.
Giải thích đầy đủ từng sheet/ cột + ví dụ thật: `doc/quy-trinh/template/03-srs-fdd-template-v3/md/huong-dan-tung-sheet.md` (đọc mục cần dùng, không đọc cả file).
Nguồn quy tắc: mẫu v3.0 + file đã điền thật `doc/quy-trinh/template/04-srs-fdd-copilot-da-dien/goc/_SRS_FDD_AI-Agent-Copilot.xlsx`. Mục đánh dấu **[ĐỀ XUẤT]** là suy ra từ file Copilot, chưa được team GDT chốt — hỏi người dùng nếu ảnh hưởng kết quả.

## A. Nguyên tắc chung (bắt buộc)
1. **Chỉ ghi ở máy** (file md/ xlsx trong `doc/`); **không ghi vào Google Sheet/ Doc**. Người dùng tự đưa lên. Nội dung chưa đưa lên ghi ở file bổ sung, xem `AGENTS.md`.
2. **Không bịa.** Mọi API, tên bảng, tên file, mã trạng thái, tên màn hình phải lấy từ **code thật hoặc tài liệu đã tải** (`doc/yeu-cau/project-doc`, `doc/thiet-ke`, `doc/uat`). Không có căn cứ → ghi `(chưa xác nhận — hỏi: …)` thay vì đoán.
3. **AI đề xuất, người duyệt.** Không tự điền "Người duyệt", "Ngày duyệt", "Xác nhận của con người", trạng thái `Approved/ Hoàn thành`. Những ô này chỉ người dùng điền, **bằng file** (không tính xác nhận qua chat).
4. **Một chức năng = một ID** (`UC-xx` hoặc `US_xx`) xuyên suốt: Use-case/ User Story → WBS → RTM → TestCases. ID mới phải hỏi người dùng nếu chưa có quy ước. **[ĐỀ XUẤT]** WBS `STT`; RTM `No` dạng `<STT task>.<chỉ số con>`.
5. **Mỗi lần làm một chức năng/ task**, xong dừng chờ duyệt rồi mới làm tiếp. Phát hiện lỗi ngoài phạm vi → ghi `Risk_Register`/ báo người dùng, **không tự sửa** task khác.
6. **Mọi thay đổi ghi `NhatKyThayDoi`.** Sửa cấu trúc mẫu → ghi lý do ở `DauMucTaiLieuCanLam`. Sheet không dùng → đánh `No` **kèm lý do**.
7. **Không sao chép chữ mẫu.** Ví dụ trong mẫu (News System, trung tâm anh văn, Toktak i18n, "Lorem ipsum", NFR "<2 giây/ 1000 đăng nhập") là của dự án khác — thay bằng nội dung thật hoặc để trống có ghi chú. Không để dòng "VD:" trong bản chính thức.
8. Ngôn ngữ: tiếng Việt, câu ngắn, dùng đúng tên trên giao diện/ trong code. Ngày `dd/mm/yyyy`. Không đưa SĐT, tên khách thật vào ví dụ (dùng dữ liệu giả rõ ràng).
9. Quy tắc commit/ Liquibase/ kiến trúc vẫn theo `git-workflow.md`, `engineering-conventions.md`; test theo `qa-process.md`.

## B. Chuẩn viết từng sheet

### `NhatKyThayDoi`
- Một dòng mỗi lần làm. `updated info` = **làm gì + ở đâu + kết quả** (vd "Thêm Use-case UC-05, 3 service, 8 test case; chờ duyệt").
- `updated part`: `Create new` | `Update`. `updated by`: ghi người duyệt chịu trách nhiệm; nếu AI soạn ghi "AI (tên công cụ), người xác nhận: …".
- `Liên quan đến`: ID chức năng/ task. `Trạng thái duyệt`: để `Draft` cho tới khi người dùng đổi.

### `PJT_Definition`
- Chỉ `B2` (Project Start Date) và `B4` (StartSprint). **Không sửa `B3`** (`=B2`). Hỏi người dùng giá trị thật, không đoán.

### `DauMucTaiLieuCanLam`
- Cột AI điền: **"Đề xuất"** (Yes/No + lý do). Cột "Xác nhận"/ "Phê duyệt" **để trống cho người**.
- Mặc định Yes cho mục có trong mẫu; chọn **User-Story Map hoặc Use-Case Diagram** (một trong hai). Sửa mẫu → bắt buộc có lý do.

### `Component_Detail_Design` (bức tranh lớn — làm **một lần cho cả epic/ hệ thống**, không lặp cho từng chức năng)
- 1.a Yêu cầu nghiệp vụ: gạch đầu dòng, mỗi dòng một yêu cầu, nói **cái gì/ cho ai**, không nói công nghệ.
- 1.b Business Flow: ghi tên ảnh/ file sơ đồ + mô tả bước chính (pool/ lane = bộ phận/ actor). Lấy từ `doc/yeu-cau/project-doc` mục 1–2 và `03-business-process-mockup`.
- 3.b Wire Frame: dẫn tới mockup có sẵn (`doc/thiet-ke/03-…`), ghi ID màn hình.
- 5 Công nghệ mỗi layer: **bảng đủ 7 cột**; mỗi công nghệ ghi *Explain (vì sao)* + *Best practice*. Lấy từ stack thật của repo (`pom.xml`, `package.json`, `docker-compose`).

### `Functions_Services_Detail_Desig` — mỗi chức năng một khối (sheet quan trọng nhất)
1. **Use-case hoặc User Story** (chọn một, thống nhất trong cả tài liệu):
   - Use-case: `Tên`, `Mô tả`, tác nhân chính/ phụ, `Tiền điều kiện`, **luồng chính/ thay thế/ ngoại lệ — mỗi bước một dòng đánh số `1.1, 1.2…`**, `Điều kiện sau khi hoàn thành`. Luồng ngoại lệ **bắt buộc** nêu: lỗi hệ thống, hết phiên, dữ liệu sai.
   - User Story: `As a [vai trò], I want to [mục tiêu] so that [lợi ích]` + **A/C đánh số**, mỗi A/C **kiểm chứng được** (có điều kiện, kết quả quan sát). Lấy A/C từ SRS (`AC-xx`) — không tự thêm A/C mới mà không báo.
   - **[ĐỀ XUẤT]** thêm `Story Points`, **DoR** (UI/UX, tài liệu kỹ thuật, dữ liệu mẫu, phụ thuộc) và **DoD** (Code review, Testing, Acceptance, Performance, Documentation).
2. **Giao diện:** ảnh/ ID màn hình + bảng **Business Rules** từng nút/ vùng/ ô (bắt buộc, định dạng, ràng buộc). Cột/ nhãn lấy từ `06-cot-hien-thi`, trạng thái từ `05-process-status`.
3. **Service/ API:** với mỗi endpoint: `PATHNAME` (đường dẫn thật `/api/v1/…`), `Method`, bảng param (`No, Param, Type, Mandatory, Sample value, Description, Remark`), `REQUEST SAMPLE` (JSON thật, có lệnh `curl` thử nếu chạy được), `RESPONSE FIELD`, `RESPONSE SAMPLE`. **Lấy từ controller/ DTO thật** (`presentation.api.*`), không suy đoán. Ghi rõ mã lỗi/ thông báo.
4. **Diagram:** Sequence (hoặc nhúng vào use-case), Activity nếu có rẽ nhánh, ERD/ class: ghi **tên bảng/ entity thật** (`core.entity`). Dữ liệu không có ảnh → mô tả bằng bảng/ danh sách.
5. **NFR:** bảng `Yêu cầu/ Mô tả/ Giải pháp` — lấy từ SRS mục II **nhưng đối chiếu hệ thống thật** (mục II của SRS GDT có vẻ từ tài liệu tuyển dụng, **không dùng nguyên văn**).
6. **Đánh giá tác động:** liệt kê **file/ module thật sẽ đổi** (FE, BE, Liquibase, config), đánh dấu Source/ Library/ Config/ Assets/ Infra: Có/ Không thay đổi, kèm rủi ro hồi quy.
7. Công nghệ & gói cài: chỉ ghi phần **thay đổi** so với `Component_Detail_Design`.

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

## C. Checklist trước khi giao một chức năng
- [ ] Có ID chức năng và có mặt ở: Use-case/ US, WBS, RTM, TestCases.
- [ ] A/C đánh số, mỗi A/C có test case.
- [ ] API/ bảng/ file/ mã trạng thái **đối chiếu với code hoặc tài liệu đã tải** (ghi nguồn).
- [ ] Không còn chữ mẫu ("News System", "Lorem ipsum", "VD:", NFR mẫu).
- [ ] Luồng ngoại lệ & lỗi có đủ; NFR đã đối chiếu thực tế.
- [ ] `NhatKyThayDoi` đã ghi; ô "Người duyệt/ Xác nhận" để trống cho người.
- [ ] Chưa tự đánh Pass/ Hoàn thành/ Approved.
- [ ] Mục chưa rõ liệt kê thành danh sách câu hỏi cho người dùng.

## D. Định dạng md, nơi lưu, quy ước (chuẩn hiện hành)
- **Giai đoạn này viết ra file md**, chưa đổ vào xlsx. Khung: `agents/templates/srs-chuc-nang/srs-chuc-nang-template.md` (16 mục, mỗi mục ghi rõ ứng với sheet nào của mẫu SRS_FDD) — **sao chép khung rồi điền, không tự đổi cấu trúc**; mục không dùng → ghi "Không áp dụng — <lý do>".
- **Nơi lưu:** `doc/srs/<mã>-<slug>.md`, **một file một chức năng**; cập nhật bảng ở `doc/srs/README.md` (mã, tên, trạng thái, căn cứ, ngày).
- **Mã chức năng:** `UC-<nn>` (hỏi người dùng nếu chưa có quy ước; mặc định đề xuất, chưa chốt). Trạng thái: `Draft` → `Đã soát` → `Approved` (**chỉ người dùng đổi**).
- **Khi bắt đầu một SRS:** (1) xác nhận với người dùng tên chức năng, phạm vi, đã code hay chưa; (2) đọc nguồn: `doc/yeu-cau/project-doc` (mục liên quan), `doc/ban-do-tai-lieu.md` → file 05/06/07; code thật của service; (3) soạn bản **Draft** từng mục, đánh dấu **câu hỏi chờ xác nhận** ở mục 16; (4) báo người dùng soát — không tự chuyển trạng thái.
- Về sau nếu chuyển sang xlsx: nội dung mỗi mục md copy sang đúng sheet theo chú thích `*(sheet …)*`.

## E. Sơ đồ
- Các loại sơ đồ của mẫu + cách vẽ chuẩn: `doc/quy-trinh/template/03-srs-fdd-template-v3/md/so-do-trong-mau.md` (mục 3). Quy tắc chính: **số bước trong sơ đồ khớp số bước trong bảng use-case; số vòng trong mockup khớp số service**; sequence gom bước thành *transaction* có ghi chú; ERD dùng tên bảng/ cột thật; không dùng ví dụ của dự án khác.
- SRS dạng md: **ưu tiên Mermaid** (`flowchart`, `sequenceDiagram`, `erDiagram`, `stateDiagram-v2`) cho sơ đồ mới; hỏi người dùng nếu chưa chắc trình xem md hiển thị được. Sơ đồ có sẵn (drawio/ ảnh) thì **dẫn đường dẫn**, không mô tả bịa lại.
- Tối thiểu mỗi chức năng: luồng (use-case/ activity), sequence (≥ 2 thành phần gọi nhau), ERD các bảng chạm tới, wireframe (dẫn mockup), state diagram nếu đổi trạng thái đơn.


## F. Văn phong kỹ thuật (bắt buộc)

Tài liệu thiết kế được viết **trước khi code**, để Dev, QA và Kế toán cùng đọc. Viết như một đặc tả kỹ thuật do người viết, không như bản tường thuật.

1. **Viết yêu cầu, không viết hiện trạng.** Dùng "Hệ thống phải…", "Hệ thống cho phép…", thì hiện tại, một ý một câu. Tài liệu thiết kế không chứa: "Đạt", "Lệch", "theo code", "Not run", "đã làm", "đề xuất". Đối chiếu với code đã có đặt ở file riêng `doc/srs/<mã>-doi-chieu.md`.
2. **A/C dạng điều kiện → kết quả**, kiểm chứng được: "Khi … thì …". Không dùng từ chung chung (nhanh, dễ dùng, phù hợp).
3. **Giá trị cụ thể:** giới hạn, số lượng, định dạng, thông báo ghi đúng nguyên văn. Chưa có giá trị thì ghi vào mục Câu hỏi mở, không viết vào nội dung.
4. **Thuật ngữ nghiệp vụ và nhãn giao diện** đúng như trên màn hình/ SRS. Tên class/ biến chỉ xuất hiện ở mục API, tác động và RTM.
5. **Không giải thích cách làm tài liệu** (không "Cách đọc", "Căn cứ suy ra", ghi chú về phương pháp). Nguồn ghi một dòng trong bảng đầu tài liệu.
6. **Phần chưa chốt dồn vào mục Câu hỏi mở** (mục cuối). Nội dung chính chỉ chứa điều đã chốt.
7. **Định dạng gọn:** bảng cho dữ liệu có cấu trúc, câu ngắn cho phần còn lại. Không emoji, không in đậm tràn lan, không gạch ngang dài làm dấu ngắt câu.
8. **Một thuật ngữ một nghĩa** trong toàn tài liệu.

## G. Skill áp dụng khi viết tài liệu thiết kế

Skill nằm ở `~/.claude/skills`. Skill có `disable-model-invocation` chỉ chạy khi người dùng gõ tên (`/grill-me`...). Mọi skill phải theo các quy tắc của workspace: ghi tài liệu vào `doc/` (không vào thư mục service), không commit, không đăng lên issue tracker, văn phong mục F.

| Bước | Skill | Cách dùng |
|---|---|---|
| Làm rõ yêu cầu | `grill-me`, `grill-with-docs` | Người dùng gọi. Phỏng vấn để chốt phạm vi. Nếu skill tạo ADR hoặc glossary, đặt vào `doc/` chứ không vào `docs/` của service. |
| Câu hỏi cho BA/ Kế toán | `to-questionnaire` | Biến mục "Câu hỏi mở" thành bảng câu hỏi gửi người khác. |
| Thuật ngữ, mô hình miền | `domain-modeling` | Chuẩn hoá thuật ngữ nghiệp vụ trước khi viết. File glossary đặt trong `doc/`. |
| API | `api-design` | Soát đặc tả API; quy ước `doc/ky-thuat/engineering/api-conventions.md` thắng khi khác nhau. |
| Sơ đồ | `diagram-design`, `archify` | Sơ đồ kiến trúc, sequence, ER, state: xuất ảnh/ SVG để đính kèm. Sơ đồ nhỏ trong md vẫn dùng Mermaid. |
| Quyết định kiến trúc | `architecture-decision-records` | Cho sheet ADR. Đổi nơi lưu mặc định `docs/adr/` thành `doc/srs/adr/`. |
| Chia task (WBS) | `to-tickets` | Chỉ ở chế độ file cục bộ. Không đăng lên tracker. |
| Test | `tdd`, `springboot-tdd`, `test-value` | Dùng ở bước code và unit test. Happy case vẫn theo `qa-process.md`. |
| Migration | `database-migrations` | Author changeset mới luôn là `ducnvh`. |
| Review code | `open-code-review`, `open-code-review-delegate` | Xem `ky-thuat/chuan-code-va-review.md` mục 5. Chỉ chạy khi người dùng đồng ý. |

Không dùng cho tài liệu này:
- `to-spec`: đăng spec lên issue tracker. Spec viết tay theo khung `srs-chuc-nang-template.md`.
- `writing-for-agents`: dành cho tài liệu để agent đọc (skill, CLAUDE.md), không phải SRS cho người đọc.
- `git-workflow`, `pr`, `implement`: quy tắc `agents/knowledge/quy-trinh/git-workflow.md` thắng; không commit, không tạo MR khi chưa được nói rõ.

## H. Ba file cho mỗi chức năng (chốt 18/10/2026)

| File | Trả lời câu hỏi | Mẫu |
|---|---|---|
| `doc/srs/UC-<nn>-<slug>.md` | Hệ thống phải làm gì (yêu cầu, A/C, giao diện, API, test) | `templates/srs-chuc-nang-template.md` |
| `doc/srs/UC-<nn>-thiet-ke-ky-thuat.md` | Làm bằng công nghệ gì, từng class và hàm làm gì, luồng chạy ra sao, mở rộng thế nào | `templates/thiet-ke-ky-thuat-template.md` |
| `doc/srs/UC-<nn>-doi-chieu.md` | Code hiện có khớp hay lệch đặc tả, việc còn lại, RTM | Xem `UC-01-doi-chieu.md` |

Thiết kế kỹ thuật ứng với các mục "Công nghệ và cài đặt", sơ đồ mức lớp và hàm, đặc tả service của mẫu SRS_FDD (sheet `Functions_Services_Detail_Desig` mục 2b, 3 và 6). Viết sau đặc tả và trước code (chức năng mới) hoặc sau khi đọc code (chức năng đã có). Mỗi hàm quan trọng phải có: vào, ra, logic từng bước, ngoại lệ. Mỗi thuật toán không hiển nhiên phải giải thích lý do chọn.

## I. Xuất sang Excel theo mẫu SRS_FDD (chốt 18/10/2026)

File md là nguồn thật; Excel là bản xuất để nộp hoặc nhập vào bộ tài liệu của công ty. Không sửa tay file Excel (bị ghi đè khi xuất lại).

Lệnh (từ gốc workspace): `python3 scripts/srs_md_to_xlsx.py UC-01 UC-02` ghi `doc/srs/xlsx/SRS_FDD_UC-01_UC-02.xlsx`.

| Sheet | Lấy từ |
|---|---|
| `NhatKyThayDoi` | Mục 0 của đặc tả |
| `PJT_Definition` | Bảng đầu của đặc tả (mã, phạm vi, nguồn, trạng thái) |
| `DauMucTaiLieuCanLam` | Mục 1 |
| `Component_Detail_Design` | Mục 2, 3 (yêu cầu, luồng nghiệp vụ, màn hình), kèm ảnh |
| `WBS_Planning` | Phạm vi và mục 4 của file đối chiếu |
| `Actors_Peronas` | Mục 2 |
| `Function_RTM` | Mục 5 của file đối chiếu |
| `Functions_Services_Detail_Desig` | Mục 4 đến 9 của đặc tả, và toàn bộ thiết kế kỹ thuật (mục "6. Công nghệ và cài đặt"), kèm ảnh |
| `TDD-TestScenario`, `TDD_TestCases` | Mục 13, 14 (bước và kết quả gộp theo mã test case) |
| `Theo_Man_Hinh` | Toàn bộ `UC-01-02-theo-man-hinh.md` (sheet thêm ngoài mẫu); happy case của từng màn cũng được gộp vào `TDD-TestScenario`, `TDD_TestCases` |
| `Rui_Ro`, `Cau_Hoi_Mo` | Mục 15, 16 (sheet thêm ngoài mẫu) |

Quy ước để xuất đúng: giữ tiêu đề mục và tên cột bảng như các file mẫu `UC-01`; mỗi bảng có hàng tiêu đề; ảnh dùng `![](hinh/...png)`. File Excel dựng lại theo tên sheet và cột của mẫu, không phải bản sao ô-theo-ô của mẫu (mẫu có nhiều ô gộp và hình vẽ). Cột ước lượng, người làm, ngày trong WBS và các cột phê duyệt để trống cho người điền.

## J. Tài liệu theo từng màn hình và ERD (chốt 18/10/2026)

Mẫu SRS của dự án có cho **mỗi màn**: UI Form, User Story, ERD, Component diagram. Chức năng chạm nhiều màn (như xuất Excel, ẩn/hiện cột) phải có thêm phần theo màn.

1. **File theo màn:** `doc/srs/UC-<nn>-<nn>-theo-man-hinh.md`, mỗi màn một mục `## MAN-<nn> <tên màn>` gồm: bảng thông tin màn (đường dẫn, khoá màn, API), 1 Giao diện (mockup trong SRS và bảng thành phần với nhãn đúng giao diện), 2 Cột hiển thị, 3 phần riêng của chức năng, 4..., 5 ERD, 6 Component, 7 Happy path, 8 Happy case, 9 Câu hỏi mở.
2. **ERD là bắt buộc kể cả khi không thêm bảng:** vẽ các bảng mà màn đọc hoặc ghi, chỉ các cột màn dùng, kèm bảng "Cột | Kiểu | Giải thích | Dùng làm gì" như SRS. Lấy tên bảng, cột, kiểu từ Entity và Liquibase, không đoán. Không ghi "ERD: Không".
3. **Component diagram theo màn:** vẽ bằng archify (loại `architecture`): thành phần giao diện, API, service, DB, dịch vụ ngoài của đúng màn đó; dịch vụ ngoài đặt ngoài khung ranh giới.
4. **Happy path và happy case theo màn:** viết trong mục 7, 8 của file theo màn; bảng happy case có cột `Mã case | Tên case | Điều kiện | Bước | Hành động | Kết quả mong đợi | Mức`, mỗi hàng một bước, theo `quy-trinh/qa-process.md` (ngôn ngữ giao diện, nhãn kiểm chứng từ code hoặc locale).
5. **Sinh file import TestLink:** `python3 scripts/srs_md_to_testlink.py [--keyword MÃ-TASK]` ghi `doc/srs/testlink/MAN-<nn>_<tên>.xml` theo mẫu `quy-trinh/templates/testlink-import-sample-tracking.xml`. Chưa có mã task thì để trống Keyword và nhắc gắn tay trên TestLink.
6. **Viết thử 2 màn trước, duyệt cách viết rồi mới nhân ra các màn còn lại.**

## K. Câu hỏi gửi Kế toán, BA (chốt 18/10/2026)

Gộp các câu hỏi mở thành một file `doc/srs/cau-hoi-ke-toan.md` (một bảng: Mã, Nhóm, Màn, Câu hỏi, Bối cảnh, Phương án A, B, C, Khuyến nghị). Quy tắc: câu hỏi bằng ngôn ngữ nghiệp vụ (không tên class, hàm); mỗi câu 3 phương án và một khuyến nghị có lý do; bỏ câu đã quyết; câu kỹ thuật chuyển sang "hỏi BA và Dev". Bản Excel có ô chọn: `python3 scripts/srs_questions_to_xlsx.py`.
