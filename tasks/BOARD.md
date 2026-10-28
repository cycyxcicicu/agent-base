# Bảng tổng task

> SINH TỰ ĐỘNG bởi `scripts/task-board.py` từ `tasks/<thư mục epic>/T-*.md` và `tasks/EPICS.md`. Không sửa tay, sửa card rồi chạy lại script.

Ký hiệu: ✅ done · 👀 review · 🔄 doing · ⬜ todo · ⛔ blocked · 🚫 cancelled (không tính vào tiến độ) · 📄 tài liệu đã có · ⭕ tài liệu chưa có

## Làm được ngay

- **T-08** (lead, E1) Chuẩn hóa cấu trúc multiagent và khả năng nâng cấp

## GĐ1  █░░░░░░░░░ 2/27 xong

### E1 Nền tảng: khung dự án, xác thực, cấu hình  (2/9)  · `tasks/E1-nen-tang/`

- 👀 **T-03** Làm xanh CI trên bản clone sạch và nối cổng task/board · _dev_
- 👀 **T-04** Sổ nợ kỹ thuật chỉ bắt nợ thật · _dev_
- 👀 **T-05** Đưa lớp adapter Qoder từ Humana về agent-base · _dev_
  - 📄 `.qoder/agents/`
  - 📄 `.qoder/rules/00-agent-loader.md`
- 👀 **T-06** Skill tuân 100% spec Agent Skills trên mọi IDE/AI · _dev_
  - 📄 `scripts/link-skills.py`
- 👀 **T-07** Giảm context mở màn, giữ đủ thông tin (progressive disclosure chuẩn) · _lead_
- ⬜ **T-08** Chuẩn hóa cấu trúc multiagent và khả năng nâng cấp · _lead_
- ✅ **T-09** Đọc tài liệu AI in SDLC và đánh giá áp dụng · _analyst_
  - 📄 `docs/analysis/T-09-ai-sdlc-application.md`
- ✅ **T-10** Xác minh nguồn Lauren Tan và ứng dụng vào tri thức cho agent · _researcher_
  - 📄 `docs/research/2026-10-27-lauren-tan-primary-sources.md`
- 🔄 **T-11** Triển khai nền tri thức, RACI, verification và eval có bằng chứng · _lead_ · chờ T-12, T-18
  - 📄 `docs/analysis/T-11-current-state.md`
  - 📄 `docs/spec/T-11-knowledge-verification-eval.md`

### E2 Tri thức, quy trình hợp nhất và kiểm chứng (đồ thị tài liệu, duyệt bằng file, vòng 13 bước, tái hiện lỗi, eval có bằng chứng)  (0/18)  · `tasks/E2-tri-thuc-quy-trinh/`

- 👀 **T-12** Chốt nền — sửa sự thật sai trong card/báo cáo cũ, mở khóa nhánh · _lead_
- 👀 **T-13** Duyệt bằng file bởi người, AI chỉ tư vấn · _architect_ · chờ T-12
  - 📄 `agents/protocols/approval.md`
  - 📄 `docs/adr/ADR-13-file-approval.md`
- 👀 **T-14** Giao thức giao việc cho model khác, xử lý nguồn mâu thuẫn, viết đặc tả · _writer_ · chờ T-12
  - 📄 `agents/protocols/delegation-prompt.md`
  - 📄 `agents/protocols/source-precedence.md`
  - 📄 `agents/protocols/spec-writing.md`
- 👀 **T-15** Vòng đời task 13 bước + 8 cổng, vòng xử lý bug và viết test hợp nhất · _architect_ · chờ T-13
  - 📄 `agents/protocols/task-loop.md`
  - 📄 `agents/protocols/test-cases.md`
- 👀 **T-16** Đề xuất thay đổi AGENTS.md và vai trò (người dùng tự áp dụng) · _analyst_ · chờ T-13, T-14, T-15
  - 📄 `docs/proposals/roles-and-rules-2026-10-28.md`
- 👀 **T-17** PROJECT.md thật, CODEMAP kiểu "cần biết gì đọc đâu", README di động, cấu hình attribution · _writer_ · chờ T-12
  - 📄 `docs/CODEMAP.md`
- 👀 **T-18** Danh sách yêu cầu R-xxx cho pilot và từ điển thuật ngữ · _ba_ · chờ T-12
  - 📄 `docs/requirements/R-pilot-knowledge-verification.md`
  - 📄 `docs/requirements/glossary.md`
- 👀 **T-19** Thu hẹp và căn chỉnh spec T-11 theo 8 cổng, 13 bước và danh sách R đã duyệt · _architect_ · chờ T-15, T-18
  - 📄 `docs/adr/ADR-19-t11-rescope.md`
- 👀 **T-20** Danh mục tri thức (catalog) và validator — lát cắt pilot I1 · _dev_ · chờ T-12, T-19
- 👀 **T-21** Ngữ cảnh theo vai và task (context CLI) — lát cắt pilot I2 · _dev_ · chờ T-20
- 👀 **T-22** Thống nhất cách tìm card (card lồng thư mục epic) — lát cắt pilot I3–I5 · _dev_ · chờ T-12, T-19
- 👀 **T-23** Kiểm điều kiện nhận task (`claim_task`) — bản cố vấn · _dev_ · chờ T-13, T-22
- 👀 **T-24** RTM sinh từ card — yêu cầu → task → file → test → bằng chứng · _dev_ · chờ T-18, T-22
- 👀 **T-25** Kiểm chứng chạy thật trên fixture — bootstrap và nâng cấp (proof) — pilot I7–I9 · _dev_ · chờ T-12, T-19, T-17
- 👀 **T-26** Harness tái hiện lỗi hai lần, so bản gốc và bản vá, Feature Map · _dev_ · chờ T-25, T-15
  - 📄 `docs/design/feature-map.md`
  - 📄 `docs/runbooks/verification-cli.md`
- 👀 **T-27** Eval có bằng chứng (v2, opt-in) — pilot I10–I11 · _dev_ · chờ T-25
- 👀 **T-28** Phân phối, CI và seed tri thức — gom file dùng chung vào một chủ · _devops_ · chờ T-21, T-23, T-24, T-26, T-27
- 👀 **T-29** Review và QA độc lập toàn bộ E2 (A4: kiểm tuân thủ quy trình) · _reviewer_ · chờ T-22, T-23, T-24, T-26, T-27, T-28

## Chưa gán phase  ██████████ 1/1 xong

### — Chưa gán epic  (1/1)

- ✅ **T-02** Tích Hợp 10 Repo Prompt và Chạy Batch Test 100 Sản Phẩm Thực Tế · _orchestrator_
