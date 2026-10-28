> Task: T-07 · Epic: E1 · Vai: dev

# Hộp thư ghi chú — INDEX

Sinh tự động bởi `scripts/notes-index.py`. Không sửa tay.
Agent chỉ mở note khớp task/module (tối đa 3), không đọc cả hộp.

| Note | Task | Summary |
|---|---|---|
| `docs/notes/inbox/E2-planning-lead.md` | — | Lead lập epic E2 và 18 card T-12..T-29 từ báo cáo phân tích; chưa duyệt, chưa thực thi, không ai tự đóng dấu duyệt. |
| `docs/notes/inbox/RK-2-lead.md` | — | (không có summary) |
| `docs/notes/inbox/RK-3-lead.md` | — | Lập phiếu rủi ro RK-3 cho việc sửa đổi 4 file dùng chung trong T-28 và dừng tại Điểm dừng B chờ phê duyệt. |
| `docs/notes/inbox/T-02-orchestrator.md` | T-02 | T-02 batch 100 demo + tích hợp 10 repo prompt: kết quả, bàn giao cho orchestrator/prompt/catalog |
| `docs/notes/inbox/T-03-dev.md` | T-03 | T-03 CI xanh trên clone sạch + nối cổng task/board: cách giữ --strict và miễn trừ có lý do |
| `docs/notes/inbox/T-04-dev.md` | T-04 | T-04 sổ nợ kỹ thuật: lọc 109 mục giả, tách luật quét khỏi nội dung tài liệu |
| `docs/notes/inbox/T-05-dev.md` | T-05 | T-05 adapter Qoder từ Humana: sweep_stale, đối chiếu 676 file khung, chuẩn hóa CRLF |
| `docs/notes/inbox/T-06-lead.md` | T-06 | T-06 lead: phân rã subtask skill compliance và điều phối cầu nối .claude/.qoder |
| `docs/notes/inbox/T-06-reviewer.md` | T-06 | T-06 reviewer: duyệt diff cổng T-06, kết luận đạt/trả lại |
| `docs/notes/inbox/T-06.1-dev.md` | T-06.1 | T-06.1: cầu nối junction .claude/skills và .qoder/skills trỏ về .agents/skills |
| `docs/notes/inbox/T-06.2-dev.md` | T-06.2 | T-06.2: test hành vi scripts/link-skills.py (idempotent, cấm rmtree) |
| `docs/notes/inbox/T-06.3-dev.md` | T-06.3 | T-06.3: check-skills.py bắt link gãy (ERROR) và SKILL.md >500 dòng (WARN) |
| `docs/notes/inbox/T-06.4-dev.md` | T-06.4 | T-06.4: diagram-design/SKILL.md về <=500 dòng bằng cách tách references/ |
| `docs/notes/inbox/T-06.5-dev.md` | T-06.5 | T-06.5: subagent-driven-development tách §Rationalizations sang references, sửa link gãy |
| `docs/notes/inbox/T-06.6-devops.md` | T-06.6 | T-06.6: setup 1-click gọi link-skills trước doctor + step CI kiểm cầu nối skill |
| `docs/notes/inbox/T-06.7-qa.md` | T-06.7 | T-06.7: QA nghiệm thu độc lập 8/8 tiêu chí T-06 |
| `docs/notes/inbox/T-07-lead.md` | T-07 | T-07 lead: chiến lược junction đã bác vì .qoder/agents là bản sinh; cải tạo thật nằm ở nguồn AGENTS.md + sync-adapters |
| `docs/notes/inbox/T-08-lead.md` | T-08 | T-08 mới là kế hoạch cấu trúc; giữ launcher, không chuyển cookie thật, cần kiểm kê trước RK. |
| `docs/notes/inbox/T-08-reviewer.md` | T-08 | T-08 reviewer: duyệt roadmap sau tách subtask; spec, scope card con và RK vẫn chưa được duyệt. |
| `docs/notes/inbox/T-09-analyst.md` | T-09 | T-09 đối chiếu SDLC: có merge gate, chưa chứng minh runtime gate; tách manifest tri thức khỏi phân phối. |
| `docs/notes/inbox/T-09-lead.md` | T-09 | T-09 đã đọc PDF 49 trang; đề xuất củng cố evidence/RTM/context trước lease và runtime gate. |
| `docs/notes/inbox/T-10-lauren-researcher.md` | T-10 | T-10 xác minh Lauren Tan/pstack bằng nguồn chính chủ; phân biệt source hiện tại với bài nói tháng 8. |
| `docs/notes/inbox/T-10-lead.md` | T-10 | T-10 xác minh Lauren Tan/pstack; ưu tiên trace-backed eval và verification harness, không thêm framework. |
| `docs/notes/inbox/T-10-pstack-researcher.md` | T-10 | T-10 nguồn official pstack 0.15.34: eval bảy bước, verification phải chạy thật; chưa ghim SHA hoặc benchmark. |
| `docs/notes/inbox/T-11-architect.md` | T-11 | T-11 spec balanced còn PROPOSED; giữ legacy eval, proof trước cleanup và approval ngoài quyền AI. |
| `docs/notes/inbox/T-11-baseline-qa.md` | T-11 | T-11 QA: hai lỗi skill-eval do dấu ngoặc nhọn trong đường dẫn TEMP; baseline chưa xanh. |
| `docs/notes/inbox/T-11-inventory-analyst.md` | T-11 | T-11 inventory: discovery lệch, eval dọn trước judge, proof chưa bền vững và CI unittest còn áp dụng. |
| `docs/notes/inbox/T-12-lead.md` | T-12 | T-12 chốt nền: baseline 247 test OK, sạch tasks/*.py qua RK-2, cập nhật T-08/09/10, mở khóa chạy trên worktree. |
| `docs/notes/inbox/T-13-architect.md` | T-13 | T-13 hoàn thành: ban hành protocol approval.md, ADR-13, cập nhật mẫu card và DoD, reviewer APPROVED. |
| `docs/notes/inbox/T-14-writer.md` | T-14 | T-14 hoàn thành: ban hành delegation-prompt.md, source-precedence.md, spec-writing.md, giới hạn note <= 80 dòng. |
| `docs/notes/inbox/T-15-architect.md` | T-15 | T-15 hoàn thành: ban hành task-loop.md, test-cases.md, nâng cấp bug-repro.md, reviewer APPROVED. |
| `docs/notes/inbox/T-16-analyst.md` | T-16 | T-16 hoàn thành: ban hành tệp đề xuất 6 nội dung cho AGENTS.md và roles, reviewer APPROVED, không sửa file đích. |
| `docs/notes/inbox/T-17-writer.md` | T-17 | T-17 hoàn thành: PROJECT.md thật, ban hành CODEMAP.md, sạch link README, attribution tùy chỉnh, reviewer APPROVED. |
| `docs/notes/inbox/T-18-ba.md` | T-18 | T-18 hoàn thành: ban hành R-pilot (14 yêu cầu, 8 nhóm, Draft), từ điển 12 thuật ngữ, phân tích mâu thuẫn. |
| `docs/notes/inbox/T-19-architect.md` | T-19 | Hoàn tất phân rã lát cắt T-11 thành 10 card E2 và cập nhật spec 8 cổng kiểm soát. |
| `docs/notes/inbox/T-20-dev.md` | T-20 | Hoàn thành T-20 danh mục tri thức và validator 11 quy tắc V00-V10 với 12 test mới xanh. |
| `docs/notes/inbox/T-21-dev.md` | T-21 | Hoàn thành T-21 trích xuất ngữ cảnh tri thức theo vai và ngân sách token với CLI knowledge.py. |
| `docs/notes/inbox/T-22-dev.md` | T-22 | Hoàn thành T-22 thống nhất cơ chế khám phá task card đệ quy cho frontier, Board, audit và next. |
| `docs/notes/inbox/T-23-dev.md` | T-23 | Hoàn thành T-23 kiểm điều kiện nhận task claim_task bản cố vấn độc lập với 5 tiêu chí G0, SEQ, DoR, BLK, PLAN. |
| `docs/notes/inbox/T-24-dev.md` | T-24 | Hoàn thành T-24 sinh ma trận truy vết Function_RTM từ card và requirements, 14 yêu cầu liên kết đầy đủ. |
| `docs/notes/inbox/T-25-dev.md` | T-25 | Hoàn thành T-25 kiểm chứng chạy thật trên fixture bootstrap và nâng cấp (proof), xuất proof bundle chuẩn. |
| `docs/notes/inbox/T-26-dev.md` | T-26 | Hoàn tất harness tái hiện lỗi 2 lần có reset, verify mode bản gốc/vá, Feature Map và runbook CLI verification. |
| `docs/notes/inbox/T-27-dev.md` | T-27 | Hoàn thành khung eval v2: thu thập bằng chứng trước khi xóa sandbox, chấm mù, bắt critical fail và mở rộng CLI. |
| `docs/notes/inbox/T-28-devops.md` | T-28 | Hoàn thành chuẩn hóa phân phối manifest, tích hợp CI check.yml và nâng cấp bảo toàn tùy chỉnh dự án. |
| `docs/notes/inbox/T-29-reviewer.md` | T-29 | Hoàn thành rà soát độc lập toàn diện Epic E2 (A4 Process & Technical QA): Đạt 100% Cổng 6, sẵn sàng cho nghiệm thu Cổng 7. |
| `docs/notes/inbox/sync-claude-agents-claude.md` | — | Việc nhỏ: thêm .claude/agents/<vai>.md vào sync-adapters, bỏ vai lead khỏi danh sách |
