> Vai: analyst (Claude soạn theo yêu cầu người dùng) · Ngày: 2026-10-28 · Trạng thái: **ĐỀ XUẤT, chưa duyệt**
> Nối tiếp: [gdt-workspace-mapping-2026-10-27.md](gdt-workspace-mapping-2026-10-27.md), [T-09](T-09-ai-sdlc-application.md), [T-11 spec](../spec/T-11-knowledge-verification-eval.md)

# Quy trình hợp nhất: AI in SDLC (49 trang) + Graph/Markdown + Lauren Tan + dự án GDT

## 0. Cách đọc và độ tin cậy

- **PDF 49 trang:** đã xem **bằng ảnh toàn bộ 49 trang** (hai trang một ảnh). Trang 22 (quy trình chính) đã phóng to 3,2 lần. Các trang 20, 23 chữ nhỏ, đọc ở độ phân giải thường nên **một số nhãn chưa chắc chắn**.
- **Số liệu trong PDF** (27 node, 130 liên kết, 97 test, 87 test, 7/14 task…) là số **tác giả tự báo cáo**, nguồn ghi ở trang 14 là `knowledge.manifest.yaml`, `rtm_gatekeeper.py`, `RTM.xlsx`. **Chưa thấy mã nguồn của họ** nên chưa kiểm chứng.
- **Lauren Tan:** nguồn là transcript trên cho.sh, bài phân tích của redreamality và hai file Pstack trên GitHub (nhánh main, không ghim SHA). **Chưa xem video.** Chi tiết mục 3.
- **Graph tài liệu:** tìm trên web, chưa chạy công cụ nào.

## 1. Quy trình trong PDF, đọc lại từ ảnh

### 1.1 Kiến trúc (trang 11, 15–16, 19, 23–25, 29)

Tri thức = **Quy trình tổ chức** (CMMI L3, PMBOK/PMP + Scrum, TDD và ATDD) + **Chuyên môn** (BA, Senior/Leader, Staff, QC, QA) + **Ngữ cảnh dự án** (yêu cầu, thiết kế, WBS, RTM, nhật ký thay đổi).

Hai vấn đề được giải: (1) AI khó đọc tài liệu cho người → mô hình hóa thành **Graph + Markdown**; (2) cần buộc AI tuân thủ → **manifest, gatekeeper, gate**.

```
27 tài liệu Markdown + RTM.xlsx          knowledge.manifest.yaml  (NGUỒN DUY NHẤT, "sửa đúng 1 chỗ")
        └──────────── build_knowledge_graph.py + validator V00–V10 ────────────┘
                              │
              graph.json (27 node, 130 cạnh)   agent_context/<agent>.json
                              │
   Orchestrator ──► A1 BA · A2 Thiết kế · A3 Coding · A4 QA (kiểm tuân thủ độc lập)
                              │  (qua lớp MCP: FileSystem / Spreadsheet / DB: "đang thực hiện, thí điểm")
                    rtm_gatekeeper.py + agent_policy.yaml  ──►  RTM.xlsx / kho mã
```

Ba lớp ở trang 29: **lời dặn** (CLAUDE.md, SDLC_WORKFLOW.md) → **cổng chặn trong mã** (mặc định từ chối, ô «chỉ con người», lease, kế hoạch file trước khi code, token riêng từng agent) → **đối soát bằng chứng** (reconcile git diff ↔ kế hoạch ↔ RTM, sweep quét kho tìm tệp mồ côi, nhật ký audit nối chuỗi băm). Câu then chốt: *lớp sau không phụ thuộc agent có «nghe lời» lớp trước hay không*.

Mỗi agent chỉ nạp 28–59% kho tri thức, mỗi mục ghi «đọc phần nào, vì sao», ngân sách token tính trước từ manifest (trang 25, ước lượng bytes/3,5, chưa đo chất lượng câu trả lời).

### 1.2 Quy trình mỗi task (trang 21, 22, 28)

**Tám cổng người duyệt** (xác nhận chỉ hợp lệ khi có giá trị thật trong đúng ô RTM; **«ok» trong chat không đủ**; Draft hay để trống đều tính là chưa duyệt):

| Cổng | Nội dung |
|---|---|
| 0 | Nhật ký thay đổi trước đó đã được người có thẩm quyền gán Approved |
| 1 | Duyệt đầu mục tài liệu (cột «Xác nhận» = Yes) |
| 2 | Duyệt thiết kế chi tiết mới/sửa |
| 3 | Duyệt ADR khi có ≥ 2 lựa chọn |
| 4 | Duyệt Actor (tác nhân, phòng ban, hệ thống ngoài) |
| 5 | Duyệt WBS (người chịu trách nhiệm + ngày) |
| 6 | **Con người** tự đặt «Hoàn thành» |
| 7 | Nghiệm thu: `Function_RTM.Xác nhận` = Yes |

**Vòng lặp đúng 1 task, đủ 13 bước, đúng thứ tự** (trang 22):

| Nhóm | Bước | Việc | Ghi chú đáng chú ý |
|---|---|---|---|
| ① Phân tích và test trước | 1–3 | Phân tích, ADR_Log nếu ≥ 2 lựa chọn (chờ cổng 3); `TDD_TestCases` **trước khi code**; `TDD-TestScenario` (BDD) | Test viết trước khi thực thi |
| ② Nhận task | 4 | `claim_task`: khai báo kế hoạch file + dòng `Function_RTM` «Dự kiến» | **Cổng tự động**: G0 (cổng 0–5 đều có giá trị thật), SEQ đúng thứ tự STT, DoR #1–#7, BLK (ADR chặn), PLAN (kế hoạch file). Đạt thì cấp lease + ghi kế hoạch + commit gốc; **trượt thì BLOCKED** |
| ③ Thực thi | 5 | Chỉ làm công việc và tài liệu đã khai báo, có header `@rtm-ref`; ngoài kế hoạch thì `amend_plan` có lý do | |
| ④ Test và báo cáo | 6–8 | Unit và Integration pass 100%, cập nhật `Test_Execution_Report` | |
| ⑤ RTM và đối soát | 9–10 | A3 đặt `Function_RTM` = «Đã thực hiện»; A4 reconcile độc lập; **chỉ A4 được đặt «Đã đối soát qua tools»** | Người làm không tự đối soát mình |
| ⑥ Nhật ký và dừng | 11–13 | `NhatKyThayDoi` trạng thái Draft, báo hoàn thành + chạy server local, WBS = **«Chờ xác nhận» rồi DỪNG** | Task kế bị khóa theo SEQ |

Sau đó con người kiểm tra thực tế trên server local và **tự tay** ghi cổng 7 và cổng 6. Có lỗi/đổi yêu cầu → tạo **sub-task `STT_cha_Bug` hoặc `ChangeRequest_NN` chạy lại đủ 13 bước** (không rút gọn vì «lỗi nhỏ»).

**Agent 4 (kiểm tuân thủ độc lập):** chạy cuối module, trước nghiệm thu, trước khi tin ô Xác nhận. Gồm `audit-human`, `audit-verify`, checklist CMMI/PMBOK (trang 30: **70 mục** chia 8 nhóm R4·K6·T7·G9·D10·C10·P12·S12; trang 22 ghi 58 mục: **PDF mâu thuẫn nội bộ**), kết quả PASS / PASS_WITH_PENDING / FAIL.

### 1.3 Các điểm đáng nhớ khác

- Trang 5–9: tốc độ ảo, nợ kỹ thuật, trôi lệch kiến trúc; giảm ảo giác bằng few-shot, lập kế hoạch và đánh giá (pseudo-code trước), **khoanh vùng ngữ cảnh ≤ 3 file**.
- Trang 17–18: **RAG cho văn bản không cấu trúc; Graph + Markdown cho tri thức có quan hệ** (code→class→hàm→API, bảng→quy trình, luật nghiệp vụ). Kết hợp được. «Hiệu quả so với RAG: chưa đo».
- Trang 21, 27–28: **«SRS Excel → Markdown»** để AI hiểu; 4 file mẫu `API_SPEC.md`, `EXAMPLES.md`, `CHATBOT_BEHAVIOR.md`, `CUSTOM_VIEW_SPEC.md`.
- Trang 31–35: các con số năng suất đều «cảm tính», cần LAB đo có đối chứng (8 chỉ số, trang 35).
- Trang 37–41: mở rộng sang nội dung số, làng nghề, du lịch, y tế: **ngoài phạm vi agent-base**.
- Trang 43–48: MCP, `.aiignore`, giao tiếp bằng tài liệu (Product → Architect → Coder → Review), «Plan & Critique», «viết Interface trước».

### 1.4 Dùng Python được không? **Được, với một giới hạn quan trọng**

Tên file trong PDF (`build_knowledge_graph.py`, `rtm_gatekeeper.py`) cho thấy hệ thống gốc **viết bằng Python**; agent-base cũng là Python, CI chạy `unittest`. Phân loại theo khả năng:

| Thành phần | Python thuần (stdlib) làm được? | Ghi chú |
|---|---|---|
| Manifest + sinh graph + validator (link gãy, vòng, phiên bản lệch) | **Có** | Dùng JSON như T-11 để khỏi thêm PyYAML |
| `agent_context/<vai>.json` + ngân sách token | **Có** | `ceil(bytes/3)` như T-11 §3 |
| RTM (yêu cầu→task→file→test→bằng chứng) | **Có** | Sinh từ frontmatter card và manifest; **không cần xlsx** (xlsx cần `openpyxl`, GDT đã dùng cho xuất Excel) |
| `claim_task` (kiểm G0, SEQ, DoR, BLK, PLAN) | **Có**, như kiểm tra chẩn đoán | Là script đọc card |
| reconcile / sweep (diff ↔ kế hoạch ↔ RTM, tệp mồ côi) | **Có** | `merge-gate.py` đã làm một phần |
| Nhật ký audit nối chuỗi băm | **Có**, nhưng chỉ phát hiện sửa | Không chống ghi lại toàn bộ (T-09 đã nêu) |
| **Ép** agent phải đi qua cổng, chặn ghi ngoài kế hoạch | **Không tự làm được** | Cần hook/MCP của công cụ chủ. Chính PDF ghi lớp MCP «đang thực hiện, thí điểm». Chưa kiểm chứng Kilo/Antigravity hỗ trợ |
| Xác thực «ai» duyệt | **Không** | Cần bằng chứng ngoài tầm ghi của AI; ô RTM do người điền chỉ đáng tin nếu AI không có quyền ghi vào ô đó |

Nghĩa là: **bản «cố vấn + kiểm tra hậu kỳ» làm hoàn toàn bằng Python ngay**; bản «cưỡng chế thật» phụ thuộc host. Khớp với T-11 §4 và cây quyết định ở §8.

## 2. Graph-Structured Documentation / Knowledge Graph

**Không có chuẩn hay thuật ngữ chính thức tên «Graph-Structured Documentation».** Trong PDF cách gọi là «Knowledge Graph + Markdown». Các công cụ cùng ý tưởng đã tìm thấy (đều trẻ, 2026, chưa kiểm adoption):

| Công cụ | Ý tưởng | Dùng được với agent-base? |
|---|---|---|
| [lat.md](https://github.com/1st1/lat.md) | Thư mục `lat.md/` các file Markdown nối nhau bằng `[[file#Mục]]`; Markdown trỏ vào mã `[[src/x.ts#hàm]]`; mã trỏ ngược `# @lat: [[mục]]`; **`lat check`** bắt link gãy và test spec thiếu backlink | **Mượn ý, không phụ thuộc:** cần Node/npm. Python dùng chú thích `# @lat:` |
| [IWE](https://iwe.md/blog/markdown-knowledge-graph-for-humans-and-agents/) | Link đứng riêng một dòng = cạnh cha→con; `iwe retrieve --expand-includes N --max-tokens N` **tất định, không embedding** | **Mượn ý:** khớp «Graph traversal» p17 và ngân sách token |
| GraphMD, Graphify | Markdown thành đồ thị «thực thi được»; đồ thị mã + tài liệu | Đã thấy qua tìm kiếm; chưa đọc, **không đề xuất** |
| [arXiv SMART](https://arxiv.org/abs/2609.05364) | Kho gần như chỉ có design doc, thành DAG, agent sinh lại mã từ doc | Bản preprint (4/9/2026), chưa phản biện, chỉ đọc phần tóm tắt: **ý tưởng tham khảo** |

**Điều rút ra áp dụng ngay:**
1. **Một nguồn duy nhất** khai báo node/cạnh (manifest), đồ thị là **bản sinh**. Sửa tay đồ thị là sai (PDF p24).
2. **Markdown giữ nội dung; graph giữ quan hệ máy kiểm tra được.** Không nhồi toàn văn vào manifest.
3. **Validator là phần giá trị nhất**, không phải hình vẽ: link gãy, node mồ côi, vòng phụ thuộc, tài liệu đổi mà task phụ thuộc chưa đánh dấu cũ. PDF nói «11 validator báo ngay chỗ lệch».
4. **Backlink hai chiều giữa tài liệu và mã/test** (ý của lat.md) chính là **RTM tự sinh**: mỗi yêu cầu có test/mã trỏ về; thiếu là báo.
5. **Truy xuất tất định theo quan hệ trước, RAG sau** và chỉ khi kho văn bản lớn.

**Điều chưa biết:** hiệu quả thực của graph so với đọc phẳng trong dự án của bạn **chưa có số đo**. Cần pilot nhỏ (T-11 lượt 4) có chỉ số: số file agent phải đọc, token, lỗi thiếu ngữ cảnh.

## 3. Lauren Tan: điều thật sự được nói, và phần cần chỉnh lại

> **Chỉnh lại nhận định đã dùng ở trao đổi trước.** Nguồn chính (transcript) cho thấy bài nói **không** mô tả quy trình «viết happy case trước rồi mới code». Phần «tái hiện lỗi → viết case → duyệt → sửa» của GDT (`xu-ly-bug-hang-loat.md`) là **mô tả của chính bạn**, GDT cũng ghi vậy. Nên coi đó là quy tắc GDT lấy cảm hứng, **không gán cho Lauren**.

**Có trong nguồn (đã đọc):**

| Chủ đề | Nội dung | Nguồn |
|---|---|---|
| Trust trước, song song sau | Không mở thêm agent khi chưa tin được đầu ra; 100 agent không có trust = «đống PR rác» | bài redreamality; transcript |
| Verification skill | Agent **chạy thật ứng dụng** (CDP, mô phỏng), lấy trace/ảnh/console, tự đóng vòng. Không có thì người thành nút thắt | transcript |
| Feature Map | Cách tới từng tính năng, phím tắt, selector; để agent hiểu báo lỗi mơ hồ và tái hiện | transcript; skill create-verification |
| Sửa ở tầng cao nhất | (1) kiến trúc khiến sai không thể xảy ra, (2) lint/CI, (3) rule/skill, (4) style guide/review, (5) verification skill | bài redreamality |
| Eval như unit test cho skill | Coordinator viết rubric, subagent chạy trong thư mục tên trung tính, judge **khác họ model** | transcript |
| Benny (tái hiện lỗi) | Chỉ làm khi có **kết luận triage đáng tin**; dừng nếu đã có người nhận hoặc đã có bản sửa | skill reproduce-and-fix-issues |

**Quy trình Benny**, đọc từ file `reproduce-and-fix-issues/SKILL.md` (không ghim SHA, không ngày):
1. Kiểm cấu hình, adapter điều khiển và feature map; thiếu thì **dừng, đánh dấu blocked**.
2. Gom hành trình, kỳ vọng và thực tế, môi trường, giả thuyết cạnh tranh (worker chỉ đọc).
3. **Tái hiện qua giao diện thật; triệu chứng phải xuất hiện ở 2 lần chạy độc lập, có reset trạng thái giữa hai lần.** Kiểm tra trạng thái chỉ để xác nhận, không để ép lỗi xuất hiện.
4. Bằng chứng (ghi hình, ảnh, ghi chú bước) **do một người đọc độc lập xác nhận thấy trạng thái hỏng**; không thì chỉ là «chưa xác nhận».
5. Không tái hiện được trong ngân sách → báo **«không tái hiện được»** (kết quả hợp lệ).
6. Đã có bản sửa → chế độ **verify**: lỗi hiện trên bản gốc, mất trên bản đã vá, mỗi bên 2 lần.
7. Chỉ sửa khi: tái hiện được, chưa có chủ, **nguyên nhân gốc có bằng chứng lúc chạy**, vừa ngân sách. «Viết test hỏng trước **khi rẻ**»; sửa nhỏ nhất.
8. Chứng minh sau sửa: lặp lại hành trình 2 lần trên bản vá, test tập trung, kiểm bán kính ảnh hưởng.
9. **Chỉ mở draft PR, không merge, không deploy**; PR có các bước, nguyên nhân, test, bằng chứng, bán kính.

**Điểm bổ sung lớn so với quy trình bug của GDT:** hai lần tái hiện độc lập có reset, người xác nhận bằng chứng độc lập, kết quả «không tái hiện được» hợp lệ, chế độ verify khi đã có bản sửa, điều kiện dừng rõ. GDT đã có sẵn: kiểm tra «bug đã xử lý sẵn», soát tác động, case duyệt bằng file trước khi code.

**Chưa xác nhận:** các số 2.000/2.500 PR, ROI, chi tiết «ba lần review» (đã ghi ở T-10). Bài nói và skill có thể đã đổi; nguồn là snapshot.

## 4. Quy trình hợp nhất đề xuất

Ghép bốn nguồn: **PDF (8 cổng + 13 bước + 3 lớp)**, **Lauren (tái hiện, verify, tầng sửa)**, **GDT (giai đoạn 0–8, QA happy case, văn phong đặc tả, bàn giao ≤ 80 dòng)**, **agent-base (card, scope, merge-gate, T-11 proof)**.

### 4.1 Vòng đời một task (ghép 13 bước PDF với giai đoạn GDT)

| Bước PDF | GDT | agent-base hiện có | Còn thiếu |
|---|---|---|---|
| Cổng 0–5 (nhật ký, đầu mục, thiết kế, ADR, Actor, WBS) | Giai đoạn 0–3, cổng «người duyệt thiết kế» | Card, `Plan Approved`, ADR, merge-gate | **Duyệt bằng file bởi người** (hiện reviewer-AI tự đóng dấu); cổng Actor/RACI |
| 1–3 phân tích + test trước | Giai đoạn 1, 2, 4 (happy path, happy case, ISTQB) | `challenger.md`, `qa`, TDD của `dev` | Mẫu `TDD_TestCases` / kịch bản; **case duyệt trước code** |
| 4 `claim_task` | — | `scope_edit`, `task-branch.py` | **Kiểm G0/SEQ/DoR/BLK/PLAN thành script**; kế hoạch file có chữ ký |
| 5 thực thi, `@rtm-ref`, `amend_plan` | Giai đoạn 5 | `scope_edit`, merge-gate chặn sửa scope | Header truy vết trong file; quy trình `amend_plan` |
| 6–8 test + báo cáo | Giai đoạn 5, 6 | test, `runner` | `Test_Execution_Report` gắn revision (T-11 proof) |
| 9–10 RTM + reconcile | RTM, WBS | **Chưa có RTM**; merge-gate là reconcile một phần | RTM sinh từ card; reconcile diff↔kế hoạch↔RTM; **A4 độc lập** |
| 11–13 nhật ký, DỪNG «Chờ xác nhận» | `doc/tien-do` cuối phiên | handoff note, trạng thái `review` | Trạng thái **chờ xác nhận người**, khóa task kế |
| Cổng 6–7 (người tự ghi) | Nghiệm thu A/C bởi PO/Kế toán | «Plan Approved» ghi bởi AI | **Ô chỉ người ghi**, kiểm tra AI không sửa được |
| Bug/CR → sub-task chạy lại đủ bước | `xu-ly-bug-hang-loat` | `bug-repro.md`, quy tắc đánh số T-x.y | Quy tắc «sub-task bug chạy lại đủ vòng» |

### 4.2 Vòng xử lý bug và test (ghép Lauren + GDT)

| # | Bước | Nguồn | Điều kiện qua |
|---|---|---|---|
| B1 | Nhận danh sách, lọc, gom nhóm, xếp ưu tiên; **chưa sửa gì** | GDT §1–3 | Báo cáo gom nhóm, người chọn |
| B2 | Kiểm xem **đã có bản sửa** chưa → nếu có thì vào chế độ verify | GDT «đã xử lý sẵn» + Benny | Hash commit, test, hành vi hiện tại |
| B3 | Đọc đủ mô tả, lập giả thuyết cạnh tranh | Benny, GDT §6.1 | |
| B4 | **Tái hiện qua bề mặt thật, 2 lần, reset giữa hai lần** | Benny | Bằng chứng; **người đọc độc lập** xác nhận |
| B5 | Không tái hiện được → báo, **không sửa mò** | GDT §6.2, Benny | Kết quả hợp lệ |
| B6 | Soát tác động (mọi nơi dùng chung) | GDT §6.3 | Danh sách màn/chức năng ảnh hưởng |
| B7 | **Viết happy case + case hồi quy trước khi code**, chạy trên code cũ (đỏ), **người duyệt bằng file** | GDT §6.4, PDF bước 2–3 | Mỗi bug ≥ 1 case sai trên code cũ |
| B8 | Test tự động hỏng đúng lý do (khi rẻ) | Benny, GDT §6.5 | Đỏ đúng lý do |
| B9 | Sửa tối thiểu, nguyên nhân gốc có bằng chứng lúc chạy | Benny, GDT §6.6 | |
| B10 | Chứng minh: 2 lần trên bản vá + so bản gốc/bản vá + hồi quy | Benny | Proof bundle (T-11 §5) |
| B11 | Lặp lại lỗi → **sửa ở tầng cao nhất có thể** (kiến trúc > kiểu > lint/CI > rule > hướng dẫn) | Lauren | Quy tắc mới bắt được lỗi cũ thật |
| B12 | **Người** đóng bug; AI không đổi trạng thái | GDT, PDF cổng 6 | |

Ghi chú: B4 và B10 cần «bề mặt chạy thật» (Feature Map + harness). Với agent-base, bề mặt là **CLI** (`bootstrap`, `upgrade`); với GDT là ứng dụng web và API. Cùng quy trình, khác harness: đây là lý do harness phải là **cấu hình theo dự án**.

## 5. Điều cần sửa ở các task hiện có (kết luận)

| Task | Cần làm |
|---|---|
| **T-08** | Cập nhật hiện trạng theo checkout `D:\congty`; sửa baseline (244 test OK); gỡ dấu duyệt do AI tự đóng; xin duyệt người bằng file |
| **T-09** | Bổ sung mục 1.2 (13 bước, 8 cổng, claim_task) và nêu mâu thuẫn trong PDF (58 vs 70 mục, 11 vs 13 bước giữa hai bản). Đối chiếu bản 26 trang trong GDT |
| **T-10** | Chỉnh lại: bài nói không có «viết happy case trước»; thêm quy trình Benny chi tiết (mục 3). Ghim SHA khi có thể |
| **T-11** | Đổi gate G1–G7 thành **8 cổng + vòng 13 bước** của PDF (hoặc bảng ánh xạ); thêm `claim_task`, `@rtm-ref`, RTM sinh từ card, A4 độc lập, trạng thái «chờ xác nhận»; thu hẹp xuống **một lát cắt** (validator + context + claim_task check) trước; thêm quy trình bug mục 4.2 vào phạm vi verification |
| **Mới** | Card tài liệu: `delegation-prompt.md`, quy tắc duyệt bằng file, bản đồ tài liệu/CODEMAP, văn phong đặc tả (đã nêu ở báo cáo trước) |

## 6. Việc chưa chắc, cần người dùng chốt

- **Q8.** RTM của agent-base là **file sinh từ card/manifest** (đề xuất) hay bạn muốn giữ dạng bảng Excel như PDF?
- **Q9.** Khi có công cụ chủ cho phép (hook/MCP), có muốn thử **cưỡng chế thật** `claim_task` trong một pilot, hay chỉ làm bản kiểm tra hậu kỳ?
- **Q10.** Cổng 5 «Duyệt WBS (người + ngày)» và cổng Actor: ai là người duyệt thật trong agent-base (chỉ bạn)? GDT có người khác (PO, Kế toán)?
- **Q11.** Ngưỡng «task» và «subtask»: giữ hai cấp (ngày / phút) như đề xuất X3?
- **Q12.** Có muốn mình tạo bộ card (nhỏ, có phạm vi cụ thể) từ báo cáo này để giao Gemini từng lượt không?
