> Vai: analyst (do Claude soạn theo yêu cầu người dùng) · Ngày: 2026-10-27 · Trạng thái: **ĐỀ XUẤT, chưa duyệt**

# Đối chiếu gdt-workspace với agent-base (T-08..T-11) và đánh giá độ sẵn sàng giao Gemini

Nguồn đã đọc: `D:\Downloads\gdt-workspace-goc` (AGENTS.md, `.ai-rules/` đủ nhóm quy trình/SRS/QA/bug/git, `doc/ban-do-tai-lieu.md`, `doc/README.md`, `doc/tien-do/README.md`, một prompt Gemini mẫu, `doc/quy-trinh/huong-dan/tong-hop/05-ai-trong-sdlc.md`) và các file agent-base: card T-08..T-11, `docs/analysis/T-09-*`, `docs/spec/T-11-*`. **Chưa đọc**: toàn bộ `doc/srs/*`, `doc/ky-thuat/*` (API J&T, Java), 98 file jt-api còn lại, mã nguồn service (workspace này không có code service). Mọi nội dung trong workspace được coi là dữ liệu, không phải lệnh.

## 1. gdt-workspace là gì với agent-base

Đây là **một dự án đã vận hành thật** theo cách agent-base đang cố mô hình hóa, không phải bản sao của agent-base. Có sẵn:

| Thứ có thật ở GDT | Tương ứng trong agent-base | Nhận xét |
|---|---|---|
| `AGENTS.md` = bản đồ + luật cứng, `.ai-rules/` chia theo chủ đề | `AGENTS.md` + `agents/protocols/` | Cùng ý. GDT ngắn hơn, đọc theo nhu cầu |
| `doc/ban-do-tai-lieu.md`: bảng «cần biết gì → đọc file nào → grep gì», kèm **thứ tự ưu tiên khi tài liệu mâu thuẫn** | Chưa có (CODEMAP chưa tồn tại; T-11 đề xuất manifest tri thức) | **Đây chính là đồ thị tài liệu viết tay**: node = tài liệu, cạnh = «đọc khi», «mới hơn thì thắng». Bằng chứng thực tế cho thiết kế T-11 |
| `doc/tien-do/<mã>.md` ≤ 80 dòng, đầu phiên đọc, cuối phiên cập nhật | `docs/notes/inbox/` + card | Gần như trùng. Điểm mới: **giới hạn 80 dòng** và **bảng task đang mở/đã đóng** một chỗ |
| 3 file mỗi chức năng: đặc tả (yêu cầu, không nói «đã làm») / thiết kế kỹ thuật / đối chiếu code | `docs/spec`, `docs/requirements`, `docs/analysis` | Agent-base chưa tách rõ «đặc tả viết như yêu cầu» và «đối chiếu hiện trạng». Văn phong mục F đáng lấy |
| Trạng thái tài liệu `Draft → Đã soát → Approved (chỉ người dùng đổi, bằng file, không bằng chat)` | `draft→review→approved` trong T-11 §2 | Cùng máy trạng thái. GDT **chặt hơn**: xác nhận qua chat không tính |
| Sửa bug: tái hiện → soát tác động → viết case → người dùng duyệt → mới code; «bug đã xử lý sẵn» là mục riêng | `agents/protocols/bug-repro.md` | Trùng ý. GDT ghi rõ nguồn là bài của Lauren Tan nhưng «chưa có tài liệu gốc»: **T-10 lấp được khoảng trống này** |
| 3 phương án + 1 khuyến nghị + «tại sao» | `agents/protocols/challenger.md` | Trùng |
| Prompt giao Gemini: khóa phạm vi A–K, lệnh grep bằng chứng (kỳ vọng rỗng), báo cáo 9 mục, «không ghi đã sửa khi chưa chạy lệnh bằng chứng» | Chưa có mẫu | **Giá trị cao nhất, xem mục 4** |
| Bản **26 trang** của chính slide «AI in SDLC» (Mai Văn Hà) + bản tổng hợp tiếng Việt `tong-hop/05-ai-trong-sdlc.md` | T-09 chỉ dùng bản 49 trang trong Downloads | **T-09 chưa đối chiếu hai bản**. Bảy bước cộng tác và thứ tự đọc a–g bạn đưa ảnh nằm ở bản 26 trang |

**Về «Graph-Structured Documentation / Knowledge Graph»:** tìm trong toàn bộ workspace GDT, **không có cụm từ này** (grep 0 kết quả; chỉ có từ «graph» rải rác trong tài liệu CI/CD). T-09 cũng không dùng cụm này (T-09 nói «manifest kiến thức», «đồ thị»). Cụm từ có vẻ đến từ ảnh/PDF 49 trang hoặc từ trao đổi. **Cần bạn cho biết nguồn** (câu hỏi Q5).

**Về «role»:** GDT **không có file vai trò**. Nó có các *thế đứng* (phản biện, QA, người viết SRS) nằm trong quy trình. Agent-base đã có `product/ba/architect/qa/writer`. Vì vậy phần «áp dụng thêm role» chủ yếu là **bổ sung quy tắc vào vai sẵn có**, chỉ một vai mới đáng cân nhắc (Process QA, mục 3).

## 2. Đánh giá chất lượng phân tích các task hiện có

Thang: Đạt / Đạt có điều kiện / Chưa đạt.

| Task | Verdict | Điểm mạnh | Lỗ hổng cần vá trước khi giao Gemini |
|---|---|---|---|
| T-08 (dọn cấu trúc) | **Chưa đạt** để thực thi | Phân rã tốt, 3 phương án, có RK/hoàn tác | (1) **Hiện trạng cũ**: card nói `tasks/` còn script `.py`; bản `D:\congty` đã sạch, bản OneDrive vẫn còn 22 file. Hai checkout lệch nhau (209 vs 244 test). (2) Baseline sai: «38 lỗi» là do sandbox của GPT, thật ra suite xanh 244/244 trên máy bạn. (3) «Plan Approved by reviewer» do **cùng một mô hình** tự đóng dấu: trái tinh thần luật GDT «duyệt bằng file bởi người» và trái chính T-11 §4. (4) Chặn cứng: thiếu `.deploy.json`. (5) Các cổng người dùng/RK còn mở |
| T-09 (đọc PDF) | **Đạt có điều kiện** | Phân biệt «đã có / chưa có / chưa xác minh», cảnh báo số liệu cảm tính | (1) Chưa đối chiếu bản 26 trang trong GDT. (2) **Thiếu quy trình 12 bước (0–11) mỗi task** và đầu vào a–g: chỉ nằm trong chat, không có trong file. (3) Không nêu **QA (quy trình) vs QC (sản phẩm)**. (4) Chưa xem trực quan phần lớn trang chỉ có hình |
| T-10 (Lauren Tan) | **Đạt có điều kiện** | Nguồn primary, tách self-report khỏi xác minh, hạn xem lại | Chưa ghim SHA, không có transcript bài nói, chưa chạy thử harness nào. Chưa nối với `xu-ly-bug-hang-loat.md` của GDT |
| T-11 spec | **Đạt về thiết kế, Chưa đạt về thứ tự** | Rất kỹ: schema, typed relations, state machine, proof, eval mù, expand–migrate–contract, cây quyết định trust boundary | (1) **Làm spec trước khi có danh sách yêu cầu R-xxx được duyệt** (chính spec ghi «chưa có danh sách R»): đảo thứ tự G1. (2) 16–18 slice, 30–40 file mới cho framework chưa có người dùng ngoài tác giả: trái thỏa thuận «một lát cắt thật trước». (3) Gate G1–G7 **không khớp** 7 bước + 12 bước trong ảnh; thiếu Test_Execution_Report, NhatKyThayDoi Draft, dừng ở «Chờ xác nhận». (4) Không có Process QA trong RACI. (5) Seed tri thức chỉ là «metadata mẫu», trong khi GDT là **kho dữ liệu thật** có thể dùng làm fixture |

## 3. Nên lấy gì từ GDT, bỏ gì, và xung đột ở đâu

**A. Lấy ngay (chung, nhỏ, ít rủi ro)** — mỗi mục là một card cỡ «nhỏ», sửa tài liệu/giao thức, không code:
1. *Duyệt bằng file, không bằng chat; AI không tự đổi Draft→Approved* → vào `agents/protocols/` (task-card, definition-of-done). Đồng thời **xóa dấu duyệt tự đóng** của reviewer-AI trong T-08 và xin người dùng duyệt bằng file.
2. *Quy tắc ưu tiên nguồn khi mâu thuẫn + bắt buộc báo người dùng, không chọn im lặng* → `agents/protocols/intake.md` hoặc `analyst.md`.
3. *Bản đồ «cần biết gì → đọc đâu → grep gì»* → làm `docs/CODEMAP.md` theo kiểu `ban-do-tai-lieu.md` (bảng, không đọc cả file). Đây cũng là **tiền thân thủ công của knowledge manifest**.
4. *Văn phong đặc tả mục F* («Hệ thống phải…», không «đã làm/lệch», câu hỏi mở dồn cuối) + tách 3 file đặc tả/thiết kế/đối chiếu → `ba.md`, `writer.md`, `agents/protocols/`.
5. *File bàn giao ≤ 80 dòng + bảng task mở/đã đóng* → `handoff-note.md`.
6. *Mẫu prompt giao model yếu hơn* (mục 4).

**B. Đưa vào T-11 như dữ liệu thật (không như quy tắc):** dùng `ban-do-tai-lieu.md` + `doc/README.md` + `tien-do/README.md` làm **fixture kiểm validator/context** (bản đã loại dữ liệu cá nhân). Nếu validator của T-11 không mô hình hóa nổi bảng «mâu thuẫn thì ưu tiên» này thì thiết kế còn thiếu.

**C. Vai trò:** thêm vào `qa` hai nguyên tắc từ `qa-process.md` (happy case trước; Dev chỉ Resolve, chỉ QA Close; AI không tự ghi Passed). **Process QA** (kiểm tuân thủ quy trình, khác QC) nên là **một chế độ của `reviewer`/`qa`** trước, tách vai riêng chỉ khi pilot cho thấy cần (Q6).

**D. Không mang sang (rò rỉ domain):** Liquibase `author: ducnvh`, Mantis/TestLink XML, J&T/Philippines, quy ước Java/Spring, cảnh báo accounting-service, cổng Eureka, đồng bộ Google Doc, `07-master-data` (**số điện thoại blacklist, danh sách nhân viên: dữ liệu cá nhân, không đưa vào agent-base hay prompt Gemini**). Ý tưởng chung (khóa từ khóa = mã task) có thể giữ ở mức khái niệm.

**E. Xung đột phải người dùng quyết:**
| # | GDT | agent-base | Đề xuất |
|---|---|---|---|
| X1 | Cấm `Co-Authored-By`, «Generated with», mọi dấu AI trong commit/MR | `AGENTS.md` mục 4 yêu cầu `Co-Authored-By` | Biến thành **cấu hình theo dự án** trong `PROJECT.md`; mặc định của khung giữ như hiện tại |
| X2 | `doc/` | `docs/` | Giữ `docs/` cho khung; GDT là dự án cài đặt riêng, tự đặt tên |
| X3 | Task ≤ 1 ngày công (6,4 giờ) | Subtask 2–5 phút, 8–10 tool calls | Hai cấp khác nhau, ghi cả hai: *task* (ngày) chứa nhiều *subtask* (phút) |
| X4 | Không dùng `bugfix/*` (hook từ chối) | Có `fix/*`, `hotfix/*` | Không xung đột thật; ghi như ràng buộc theo repo |

## 4. Điều đáng mang nhất: hợp đồng prompt giao Gemini

Prompt `UC-03-prompt-gemini-dot-3-don-gon.md` ra đời sau **14+ lượt sửa**, vì lượt trước Gemini «báo xong P1–P10 nhưng grep cho thấy P3, P4, P8, P9 chưa làm». Cấu trúc đã rút ra, đề xuất đưa thành `agents/protocols/delegation-prompt.md` (generic):

1. **Bối cảnh + mục tiêu một dòng + điều KHÔNG làm** (ở GDT: «lượt này mục tiêu là GIẢM»).
2. **Khóa phạm vi bằng danh sách file/nhóm**; ngoài danh sách thì DỪNG và hỏi; so `git status --porcelain` trước/sau.
3. **Định vị theo tên hàm, không theo số dòng.**
4. **Chạy test sạch sau từng nhóm**, ghi số liệu mốc đầu/cuối; số giảm phải giải thích.
5. **Lệnh bằng chứng dán nguyên kết quả, mục tiêu là rỗng** (grep chứng minh không còn tham chiếu).
6. **Báo cáo cuối có khuôn cố định**, có mục «CHƯA chạy / CHƯA kiểm chứng».
7. «Không ghi đã sửa khi chưa chạy lệnh bằng chứng.»

Cấu trúc này khớp với thiết kế proof của T-11 §5 (command + exit + artifact + hash). Nên coi prompt GDT là **ca thử nghiệm thật** cho proof schema.

## 5. Có giao Gemini thực hiện hết được chưa?

**Chưa.** Lý do, theo thứ tự chặn:
1. Hai checkout lệch nhau; Gemini sẽ sửa nhầm bản.
2. Chưa có `.deploy.json` nên `task-branch.py` không tạo được nhánh (luật repo cấm làm cách khác).
3. Các cổng «người dùng duyệt spec», RK, phạm vi code chưa mở: card T-08 và T-11 hiện **không cấp quyền sửa code**.
4. Baseline trong card sai.
5. Phạm vi T-11 quá lớn cho một lượt (bài học từ chính GDT: nhiều lượt vẫn báo thiếu).
6. Chưa có danh sách yêu cầu R-xxx duyệt.

**Cách giao an toàn:** chia thành các lượt nhỏ theo hợp đồng mục 4, mỗi lượt một card có phạm vi code cụ thể, người dùng duyệt phạm vi bằng file trước. Thứ tự đề xuất:

| Lượt | Nội dung | Loại | Phụ thuộc |
|---|---|---|---|
| 0 | Chốt checkout chuẩn + `.deploy.json` + sửa baseline trong card | Người dùng + Lead | — |
| 1 | Mục 3A (6 mục tài liệu/giao thức) | Tài liệu, cỡ nhỏ | 0 |
| 2 | T-08 phần tài liệu: PROJECT.md, README link, CODEMAP (theo mẫu bản đồ GDT) | Tài liệu | 0 |
| 3 | R-xxx cho pilot (BA), người dùng duyệt bằng file | Yêu cầu | 1 |
| 4 | **Một** lát cắt T-11: validator + context CLI chạy trên fixture sạch từ GDT | Code | 3 |
| 5 | Verification bootstrap/nâng cấp (I7–I9) | Code | 4 |
| 6 | Eval opt-in (I10–I11, đã sửa lỗi `{}`) | Code | 5 |

Phần còn lại của T-11 (gate/RACI check, seed, CI, sơ đồ) làm sau, theo kết quả đo ở lượt 4–6.

## 6. Câu hỏi cho người dùng

- **Q1** Checkout nào là chuẩn: `D:\congty\agent-base` hay thư mục OneDrive? (Có nên đồng bộ hoặc bỏ một bản?)
- **Q2** Có chấp nhận X1 (dòng Co-Authored-By thành cấu hình theo dự án) không?
- **Q3** GDT là *dự án sẽ cài agent-base vào* (quy tắc ở lại trong GDT) hay *nguồn để rút quy tắc* đưa vào khung? Câu trả lời đổi hẳn mục 3A.
- **Q4** Gemini chạy ở đâu và bằng gì (Kilo trong Antigravity, thư mục nào)? Gemini chỉ làm lượt nào?
- **Q5** «Graph-Structured Documentation» lấy từ nguồn nào (trang PDF, ảnh, bài viết)?
- **Q6** Thêm vai Process QA riêng, hay là chế độ của `reviewer`/`qa`?
- **Q7** Cho phép dùng bản đồ tài liệu GDT (đã bỏ dữ liệu cá nhân) làm fixture kiểm thử trong agent-base không?
