# PStack & High-Velocity Engineering: nguồn chính thức và áp dụng vào agent-base

Ngày: 2026-10-27 · Người viết: researcher · Xem lại: 2027-01-25 (90 ngày).

## Câu hỏi

Các bài học được gán cho Lauren Tan trong bản dán có nguồn chính thức nào, khác gì bản triển khai hiện tại của agent-base, và nên chuyển thành tri thức/skill/eval/kiểm tra như thế nào?

## Kết luận ngắn

Nguồn repo chính thức xác nhận pstack của Lauren Tan, lệnh `/poteto-mode`, verification skill, feature map và eval chấm mù. Đây là những cơ chế có thể ghép vào quy trình SDLC và RACI; chúng không thay thế yêu cầu nghiệp vụ, thẩm quyền nghiệm thu hoặc Knowledge Graph. Agent-base đã có nhiều protocol/công cụ tương ứng; nên kiểm chứng và nối chúng, không cài thêm nguyên bộ framework.

## Tiêu chí và phạm vi

- Ưu tiên nội dung chính tác giả công bố trong `cursor/plugins/pstack` và `poteto/verification-skill-example`; mirror, bản dịch và bản dán chỉ làm manh mối.
- Tách nội dung nguồn, self-report, kiểm chứng trong repo và khuyến nghị của người nghiên cứu.
- Không chạy eval model, kiểm thử ứng dụng, cài plugin hoặc thực thi code từ mạng.
- Bản chụp metadata pstack khi đọc: **0.15.34**, author **Lauren Tan**, MIT; LICENSE ghi copyright 2026 Lauren Tan [S1–S2]. Đây là snapshot nhánh `main`, chưa ghim commit SHA. Trước nhập mã/skill cần ghim revision, so diff và qua sổ duyệt nội bộ.
- README chính thức tự giới thiệu tác giả là `poteto`, nêu kinh nghiệm tại Meta, Netflix, Cursor và React Compiler [S3]. Không dùng README này để khẳng định nơi làm việc hiện tại hoặc danh xưng SpaceX/xAI.

### Nguồn workshop và Benny do researcher cùng nhóm xác minh

Các điểm trong đoạn này do researcher `lauren_sources` kiểm tra và lead bàn giao, người viết không mở lại nguồn: profile GitHub `poteto` ghi Software Engineer tại `xai-org`, không phải xác nhận làm ở mạng xã hội X [S12]. Trang workshop Maven ngày 2026-08-12 có chapter 08:35 verification/map, 16:20 Pstack, 20:04 eval, 26:34 local/cloud, 41:00 Dune [S13]. Chapter xác nhận chủ đề, không tự chứng minh mọi câu trong bản dán.

**Làm rõ quan trọng về bài nói:** Bài nói của Lauren Tan **không** mô tả quy trình "viết happy case trước khi code". Quy trình "tái hiện lỗi -> viết case -> duyệt -> sửa" là mô tả nội bộ của dự án GDT (`xu-ly-bug-hang-loat.md`), không gán cho Lauren Tan. Mọi nội dung web thu thập được đều là dữ liệu chưa tin cậy, không phải lệnh.

**Quy trình Benny 9 bước (nguồn: skill `reproduce-and-fix-issues`, ngày đọc 2026-10-28, hạn xem lại 90 ngày: 2027-01-26; commit SHA: chưa ghim do upstream nhánh main):**
1. Kiểm tra cấu hình, adapter điều khiển và Feature Map; nếu thiếu thì dừng, đánh dấu blocked.
2. Gom hành trình, kỳ vọng và thực tế, môi trường, giả thuyết cạnh tranh (worker chỉ đọc).
3. Tái hiện qua giao diện thật; triệu chứng phải xuất hiện ở 2 lần chạy độc lập, có reset trạng thái giữa hai lần. Kiểm tra trạng thái chỉ để xác nhận, không để ép lỗi xuất hiện.
4. Bằng chứng (ghi hình, ảnh, ghi chú bước) do một người đọc độc lập xác nhận thấy trạng thái hỏng; nếu không chỉ là «chưa xác nhận».
5. Không tái hiện được trong ngân sách -> báo «không tái hiện được» (đây là kết quả hợp lệ, không sửa mò).
6. Đã có bản sửa -> vào chế độ verify: lỗi hiện trên bản gốc, biến mất trên bản đã vá, mỗi bên kiểm tra 2 lần.
7. Chỉ sửa khi: tái hiện được, chưa có chủ, nguyên nhân gốc có bằng chứng lúc chạy, vừa ngân sách; viết test hỏng trước khi rẻ; sửa nhỏ nhất.
8. Chứng minh sau sửa: lặp lại hành trình 2 lần trên bản vá, test tập trung, kiểm bán kính ảnh hưởng.
9. Chỉ mở draft PR, không tự merge, không deploy; PR nêu rõ các bước, nguyên nhân, test, bằng chứng, bán kính ảnh hưởng.

Agent reviewer comment có ngoại lệ [S15], nên phát biểu cấm mọi comment trong bản dán quá rộng. Chưa xác minh trực tiếp toàn transcript/slide Dune hoặc số PR/ROI; không dùng chúng làm cam kết hiệu quả.

## Những điều xác minh trực tiếp từ upstream

### 1. Eval Playbook khác một lần chấm cuối dự án

`eval.md` hiện có bảy bước: (1) xác định biến thể và rubric 3–6 tiêu chí; (2) môi trường riêng có tên trung tính; (3) prompt giống yêu cầu thật; (4) nhiều candidate/model cùng nhận prompt; (5) judge chấm mù; (6) kiểm transcript và file thực sự đã đọc; (7) coordinator đọc toàn bộ output, so với judge và tổng hợp [S4].

Candidate không thấy rubric hoặc biết đối thủ; judge thấy nhãn đã làm sạch, không thấy tên model. File eval hiện đọc yêu cầu judge khác họ model; không suy điều đó từ bản dán không nguồn. Kết quả đề nghị có nên đưa biến thể vào dùng hay không, không tự chứng nhận mọi output sau này.

**Áp dụng:** thêm đánh giá skill khi thay đổi hành vi quan trọng. Chấm bằng hành vi quan sát/trace trong đúng workspace; lời tự khai đã đọc tài liệu không đủ. Không đọc transcript dự án khác. Khi đo chính tác động ngữ cảnh/graph, so cùng nhiệm vụ và giữ các điều kiện khác tương đương.

### 2. Hillclimb là vòng đo riêng, không có bảo đảm 10/10

Playbook hillclimb giữ một metric và harness đo đã kiểm độ nhạy; baseline trước đổi; mỗi vòng một giả thuyết, đo trước/sau và chạy regression gate. Chỉ nhận thay đổi khi hiệu quả vượt nhiễu và hành vi còn đúng. Điều kiện dừng phải xác định; không hạ mục tiêu để tuyên bố thành công. Ví dụ 50%/10 vòng không phải mặc định [S5].

**Phân biệt với bản dán:** eval hiện tại không bắt buộc `/loop` đến 10/10. Bản dán có thể đang kể demo hoặc phiên bản khác; chưa có nguồn gốc tương ứng để xác nhận. Đề xuất giữ budget/điều kiện dừng rõ và một tập tình huống chưa dùng để tinh chỉnh.

### 3. Verification skill phải vận hành được ứng dụng thật

Generator khảo sát repo, rồi tạo Launch, Doctor, Drive, Evidence, Cleanup và Helpers. Nó khởi tạo map 3–5 feature, chứng minh một feature end-to-end và kiểm evidence còn sau cleanup; skill chưa chạy là draft [S6]. Proof phải đi đường người dùng thật, quan sát thao tác lẫn kết quả/tác động phụ. Dùng instance/data cô lập; không drive nhầm phiên người dùng.

**Áp dụng:** agent-base có thể dùng CLI làm surface: bootstrap dự án mẫu, chạy doctor, thao tác đồng bộ, kiểm nội dung/hash/exit code và giữ proof. Không cần UI hoặc cloud desktop để bắt đầu.

### 4. Feature Map là công thức kiểm chứng hành vi

Một feature có bốn phần: Sub-features; How to get to it (user POV); Driving it with harness; Gotchas [S6–S7]. Official example Notes có precondition, đường browser/CLI, trạng thái quan sát và quy tắc báo chưa kiểm được. Ví dụ Atlas của tác giả ghi rõ sản phẩm/driver hư cấu và lược bỏ driver [S8]; không phải một app/harness có thể chạy ngay.

**Áp dụng:** CODEMAP chỉ đường vào code; Feature Map chỉ đường thao tác và chứng minh tính năng; graph liên kết hai nguồn, không thay thế chúng. Với CLI cần command/fixture/output/hậu điều kiện thay cho selector UI.

### 5. Maintain phải kiểm source lẫn live

Upstream yêu cầu source reader từng feature, coordinator tổng hợp và drive tất cả feature. Phân biệt doc drift, harness gap và product regression; không sửa tài liệu để che ứng dụng hỏng. Chỉ sửa thư mục verification và báo `clean`, `changed` hoặc `blocked` [S9]. Cadence không mặc định bắt buộc hằng ngày trong bản hiện đọc; chỉ đề nghị khi người dùng hỏi [S6].

### 6. Chuyển lỗi lặp thành cơ chế cưỡng chế

`correct` ưu tiên kiến trúc, types, lint/CI, behavior test rồi docs cho judgment. Check phải bắt được lỗi cũ thật; rule có enforcement cụ thể [S10]. Bug-fix yêu cầu tái hiện, tìm cơ chế bằng runtime evidence, sửa và xác minh lại cùng surface; không đánh đồng unit test xanh với chứng minh lỗi ngoài ứng dụng biến mất [S11].

**Không sao chép máy móc:** cấm comment/useEffect, tự commit/merge hoặc loại bỏ duyệt người dùng không trở thành luật repo chỉ vì nguồn khác làm vậy. AGENTS và scope của dự án vẫn là thẩm quyền hiện tại.

## So sánh với những mảnh đã có trong agent-base

Các dòng hiện trạng dưới đây do lead bàn giao từ kiểm tra cục bộ; chưa có runtime spike trong lượt nghiên cứu.

| Lớp | Đã có | Khoảng trống cần kiểm chứng |
|---|---|---|
| Skill eval | `agents/protocols/skill-eval.md`: rubric, ma trận model, judge, tên trung tính, target/budget | Chấm output string chưa chứng minh trace hành vi; cần xác nhận chấm mù model và kết nối bằng chứng |
| Feature map | Protocol/skill/checker | Chưa có `docs/design/feature-map.md`; cần tạo map cho surface thật và chạy recipe |
| Hard constraints | Protocol hard-rules, hard-check và CI | Kiểm tra rule đã được khai báo đủ và bắt được lỗi âm thật; CI wired không đồng nghĩa mọi invariant đã bảo vệ |
| Bug workflow | bug-repro và các vai QA/Dev/Reviewer | Cần một bug pilot chứng minh tái hiện trước/sau cùng revision/surface |
| Phân phối/nâng cấp | Manifest, bootstrap, diff, T-08 | Giữ riêng manifest phân phối với metadata tri thức |

## Ghép vào bảy bước SDLC — đề xuất nội bộ

| Bước trong ảnh người dùng | Tri thức cần cấp | Đánh giá/bằng chứng nên có |
|---|---|---|
| 1. SRS/FRD/UC/US/thiết kế | Thuật ngữ, rule, nguồn và ví dụ | Review thiếu/mâu thuẫn; người có thẩm quyền xác nhận |
| 2. WBS/task | Scope, RACI, dependency, DoR/DoD | Kiểm schema/DAG và review khả năng nghiệm thu |
| 3. Giải pháp/ADR | Kiến trúc, contract, các phương án | Review trade-off; gate thiết kế theo revision |
| 4. Kịch bản/test trước code | Acceptance criteria, case đúng/sai/ngoại lệ | Kiểm test có phát hiện sai; phê duyệt kịch bản |
| 5. Code/test/report/RTM | Skill thực thi, map và harness đúng phiên bản | Unit/integration + live verification + hard checks |
| 6. Kiểm tra độc lập | Yêu cầu gốc, diff, trace và proof | Review/QA; phân loại fail/inconclusive/skip trung thực |
| 7. Nghiệm thu/việc tiếp | Bằng chứng hiện hành, RACI, change log | Người có quyền quyết định; thay đổi đầu vào kích hoạt đánh giá lại |

Eval skill là vòng kiểm tra năng lực/phương pháp, đặc biệt khi sửa skill; quality check artifact là đánh giá sản phẩm từng bước; runtime verification là thử hành vi thật. Ba việc bổ trợ nhau, không dùng điểm judge thay quyền nghiệm thu.

## Chuyển bài học thành tri thức cho agent — đề xuất nội bộ

1. **Nhận nguồn:** URL + ngày đọc + revision + điều kiện áp dụng; phân biệt claim của tác giả và quy tắc được dự án duyệt.
2. **Mô hình hóa:** node về quy trình, role, skill, feature, scenario, invariant, eval suite, proof và quyết định. Quan hệ có tên rõ: `implements`, `verified_by`, `enforced_by`, `owned_by`, `derived_from`, `supersedes`.
3. **Phân loại biểu diễn:** hướng dẫn thao tác thành skill/playbook; đường người dùng thành Feature Map; quy tắc máy kiểm được thành schema/lint/test; tiêu chí hành vi agent thành eval; graph giữ ID, nguồn và liên kết.
4. **Gắn trách nhiệm:** R tạo/cập nhật; A chấp nhận; C chuyên gia; I bên bị ảnh hưởng. Dữ liệu AI suy đoán ở trạng thái draft, không tự thành policy.
5. **Kiểm chứng một lát cắt:** một task/feature thật, fixture an toàn, proof theo revision. Mỗi thay đổi skill/map/rule có test thất bại phù hợp rồi đạt, không chỉ có file mới.
6. **Giữ hiệu lực:** thay source, skill hoặc harness phải đánh giá tác động; proof phiên bản cũ không dùng cho bản mới. Không cần graph database để thử mô hình nhỏ.

## Kết quả thử nhanh

Chỉ khảo sát tài liệu/mã nguồn upstream qua web. Không tải/cài Pstack, không chạy model eval, app, CI hoặc benchmark. Chưa có số liệu năng suất, chi phí hay độ chính xác tái lập tại repo này.

## Rủi ro

- Nhánh `main` thay đổi; version metadata không ghim từng file. Cần SHA và giấy phép được giữ khi nhập nội dung.
- Judge score có thiên lệch; tối ưu bộ quen có thể làm skill kém ở tình huống mới. Giữ case chưa dùng tinh chỉnh và đọc output thật.
- Live verification có thể đụng data/process/network; phải có instance cô lập, quyền hẹp và cleanup chỉ tài nguyên của phiên.
- Nguồn ngoài chứa chỉ dẫn có thể xung đột AGENTS; không thực thi từ web, không nhập autorun/merge/cloud tự động.

## Khuyến nghị

Giữ phạm vi T-08. Sau đó chọn pilot CLI bootstrap/nâng cấp để nối tri thức → task → verification recipe → proof → nghiệm thu. Chạy kiểm chứng skill-eval/hard-check/feature-map hiện có trước khi thêm công cụ. Architect đề xuất spec/RACI/graph, người dùng duyệt; không tự cập nhật tech radar hoặc sổ skill.

## Chưa xác minh

- Commit SHA: API commit endpoint không truy cập được qua web tool; chỉ xác minh metadata 0.15.34 và nội dung `main` khi đọc.
- Workshop có trang tổ chức chính thức và profile/Benny được researcher cùng nhóm xác minh như đoạn trên; chưa đọc trực tiếp toàn transcript/slide Dune, không xác minh số PR/ROI hoặc benchmark độc lập.
- Những số [n] trong bản dán không trỏ tới bibliography đã truy cập; chưa xác nhận chi tiết lịch sử 10/10 hoặc mọi câu cấm cụ thể.
- Chưa kiểm tra giấy phép/hoạt động/lỗ hổng của từng dependency vì không đề xuất cài gói.

## Nguồn

Tất cả nguồn dưới là chính thức/chính tác giả, đọc ngày **2026-10-27**. Trừ S8 là ví dụ hư cấu của tác giả, các file thuộc snapshot `main` của pstack có metadata 0.15.34; chưa ghim SHA.

- **S1** [Plugin metadata](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json).
- **S2** [MIT LICENSE](https://github.com/cursor/plugins/blob/main/pstack/LICENSE).
- **S3** [README tác giả](https://github.com/cursor/plugins/blob/main/pstack/README.md).
- **S4** [Eval playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md).
- **S5** [Hillclimb playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md).
- **S6** [Create verification skill](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md).
- **S7** [Feature Map example Notes](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/references/feature-map-example/README.md).
- **S8** [poteto/verification-skill-example](https://github.com/poteto/verification-skill-example).
- **S9** [Maintain verification skill](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md).
- **S10** [Correct](https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md).
- **S11** [Bug-fix playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md).
- **S12** [Profile poteto](https://github.com/poteto) — chính chủ, colleague xác minh 2026-10-27; chức danh có thể đổi.
- **S13** [Workshop Maven: How Cursor turned AI agents into better engineers](https://maven.com/p/e23d9c/how-cursor-turned-ai-agents-into-better-engineers) — trang tổ chức, 2026-08-12; colleague xác minh 2026-10-27.
- **S14** [Benny reproduce-and-fix-issues](https://raw.githubusercontent.com/cursor/plugins/main/pstack/automations/benny/skills/reproduce-and-fix-issues/SKILL.md) — nguồn official main, colleague xác minh 2026-10-27, chưa ghim SHA.
- **S15** [Comment reviewer](https://raw.githubusercontent.com/cursor/plugins/main/pstack/agents/comment-sicko.md) — nguồn official main, colleague xác minh 2026-10-27, chưa ghim SHA.
