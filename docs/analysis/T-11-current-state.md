> Task: T-11 · Epic: E1 · Vai: analyst

# T-11.1 — Hiện trạng tri thức, workflow, verification và eval

Ngày kiểm: 2026-10-27. Phạm vi: kiểm tra tĩnh working tree, không chạy test, không cài đặt, không web. Báo cáo này là đầu vào thiết kế, chưa phải nghiệm thu runtime. Nguồn là file hiện tại; HEAD theo card T-11 là `f12b1a23169da79ec8490b64d51a90c685b8f76f` và không đại diện đầy đủ cho nhiều thay đổi chưa commit.

## Kết luận phục vụ chốt spec

| Tác động | Phát hiện và mức chắc chắn | Căn cứ |
|---|---|---|
| Chặn thiết kế contract | **Chắc chắn:** eval chỉ nhận output text, dọn sandbox trước judge; chưa có artifact/trace bền vững trong contract `Runner`, `Judge`, `CellResult`. Điểm hiện tại chưa chứng minh hành vi thực. | `agent_core/eval/skill_eval.py:25–30,69–74,159–175` |
| Chặn thống nhất task | **Chắc chắn:** frontier quét một cấp; board/audit quét card lồng epic. Parser frontier đọc dòng chứa `Status`/`Trạng thái` và enum uppercase, không đọc YAML `status: doing/review/done`; regex ID không hỗ trợ đầy đủ subtask có dấu chấm. | `agent_core/cli.py:62–68`; `scripts/task-board.py:74–96`; `scripts/card-audit.py:65–72`; `agent_core/workflow/tracer_bullet.py:36–57` |
| Ảnh hưởng thiết kế | **Chắc chắn:** `DependencyGraph` là đồ thị ticket, có dangling check/cycle/topological/critical path; không phải knowledge graph có nguồn, version và approval. | `agent_core/workflow/tracer_bullet.py:81–109,125,162,195` |
| Ảnh hưởng thiết kế | **Chắc chắn:** handoff router có vai và hướng chuyển; chuyển không hợp lệ chỉ in cảnh báo rồi vẫn tạo note. Không có RACI theo activity hay quyền duyệt trong API này. | `agent_core/workflow/handoff.py:26–54,67–78` |
| Ảnh hưởng thiết kế | **Chắc chắn:** sandbox hiện tại là subprocess có cwd/timeout và lọc environment; không có cơ chế giới hạn đường dẫn filesystem trong implementation đã đọc. CLI skill-eval gọi subprocess riêng với bản sao toàn bộ environment, không tái dùng bộ lọc SandboxRunner. | `agent_core/core/sandbox.py:35–75,79–85`; `scripts/skill-eval.py:60–69` |
| Ảnh hưởng verification | **Chắc chắn:** proof hiện là dict command/exit/stdout/stderr/duration/passed; validator chỉ kiểm exit=0 và passed=True, chưa ràng buộc revision/task/hash/artifact. `ExecutionResult.artifacts` có field nhưng run_command không điền. | `agent_core/core/telemetry.py:16–65`; `agent_core/core/sandbox.py:16–28,88–95` |
| Chặn quy ước test | **Chắc chắn:** Python stack yêu cầu pytest; hard rules cấm import pytest và bare test functions; CI vẫn chạy unittest discover. CI đã cài .[dev] nếu pyproject phù hợp, nên lý do hard rule “chỉ cài pyyaml” không còn luôn đúng. | `agents/stacks/python.md:14,34–38`; `docs/HARD-RULES.json:4–17`; `.github/workflows/check.yml:24–34,138–140`; `pyproject.toml:12–22` |

➡️ Đề xuất cho Lead: giữ unittest.TestCase làm tiêu chuẩn lát cắt T-11 để tương thích discovery hiện tại; ghi rõ trong spec/card. Việc thống nhất PROJECT/stack/hard-rule prose cần owner và scope riêng, không tự sửa AGENTS/roles.

## Bản đồ module đã kiểm

| Vị trí | Trách nhiệm/điểm vào đã kiểm | Hướng gọi và giới hạn |
|---|---|---|
| `agent_core/cli.py` | argparse: debt, frontier, scan, convert | Import debt ledger, ticket graph, redteam và ingest ở dòng 20–24; chưa có knowledge/workflow/verification command (dòng 31–45). |
| `agent_core/workflow/` | `tracer_bullet.py`, `handoff.py` | Ticket dependency và handoff data; không thấy SDLC bảy bước trong hai module đã đọc. `expand_contract.py` chưa đọc sâu. |
| `agent_core/core/` | `sandbox.py`, `telemetry.py` | Có primitive subprocess/proof; persistence và trust boundary chưa có trong API đã đọc. Các module resilience/json/wait chỉ kiểm tên file. |
| `agent_core/eval/` | `skill_eval.py`, `runner.py` | Matrix + injected model adapter; EvalRunner assertions trên response đã có sẵn, không tự thực thi candidate (`runner.py:12–22,39–62`). |
| `scripts/` | bootstrap/diff, task-board/audit/next, skill-eval | CLI riêng đang tồn tại song song unified CLI. `next.py:36–41` nạp card-audit; nên dùng một thư viện discovery rồi giữ wrapper tương thích. |
| `schemas/` | `skills-config.schema.json` | Inventory hiện chỉ có schema skill directory/quarantine; không có schema knowledge/RACI/evidence/SDLC trong thư mục này. |
| `agents/` | protocol, role, knowledge, manifest | Tài liệu governance; registry skill là dữ liệu duyệt bởi người dùng. Không đồng nhất văn bản với enforcement runtime. |
| `tests/` | unittest cho core/sandbox/workflow/skill-eval và scripts | Có test mock matrix + cleanup (`tests/test_skill_eval.py:58–70`), CLI external command (`:111`); chưa chạy nên không kết luận PASS. |

Ba luồng đã kiểm: `agent-base frontier → TicketParser → DependencyGraph`; `skill-eval run → runner subprocess → run_matrix cleanup → judge subprocess → markdown report`; `manifest → bootstrap copy/fresh/mkdir → .agent-base.json hashes → agent-base-diff classification/copy`.

Không dựng `docs/CODEMAP.md` vì ownership T-11.1 chỉ cấp hai file báo cáo/note. Tại thời điểm kiểm, CODEMAP, Graphify report và feature-map đều không tồn tại (kiểm Test-Path); không có đồ thị Graphify để kết luận quan hệ.

## API bootstrap, nâng cấp và phân phối

- **Chắc chắn:** bootstrap có `--target`, `--mode git|hidden`, `--dry-run` (`scripts/bootstrap-project.py:97–102`); bỏ qua file đã tồn tại (`:132–139`), fresh tạo mẫu (`:142–151`), ghi metadata source/commit/mode/date/hash (`:159–167`), hidden thêm git exclude (`:169–177`). API này cần fixture kiểm no-overwrite và idempotency.
- **Chắc chắn:** metadata được ghi lại mỗi lần bootstrap; `record` chỉ nhận các file copy mới trong vòng lặp trên. **Suy đoán:** chạy lại target có sẵn có thể làm mất baseline hash cũ trong metadata; cần test fixture xác nhận trước thiết kế migration (`:133–141,159–167`).
- **Chắc chắn:** diff có `--base`, `--push FILE...`, `--pull FILE...`, `--mark-synced` (`scripts/agent-base-diff.py:59–64`); phân loại bằng hash baseline (`:110–134`). Push/pull tên file là copy trực tiếp (`:84–98`), không có guard conflict tương ứng trong nhánh mutation đã đọc; cần verification âm cho customized/both-changed. Không thực thi các mutation trong inventory.
- **Chắc chắn:** manifest là manifest **phân phối**, có copy/template/generated/gitonly/fresh/mkdir; copy rộng agents/scripts/agent_core/examples/schemas nhưng nội dung docs chỉ tạo trống (`agents/manifest.txt:1–14,16–73`). Tách knowledge manifest khỏi manifest này; nếu knowledge data đặt trong docs thì phải thiết kế phân phối explicit, không giả định đã copy.
- **Chắc chắn:** pyproject cung cấp entrypoint `agent-base = agent_core.cli:main`, Python >=3.11 (`pyproject.toml:9,15–19`). Manifest không liệt kê pyproject/tests (danh sách `agents/manifest.txt:16–73`), nên fixture project nhận framework không mặc nhiên nhận package metadata hay bộ test framework.

## Evidence, rubric và gate cần giữ tương thích

- **Đã có, chắc chắn:** rubric validate nonempty/unique IDs/positive weight; judge không trùng model và mặc định khác family; score clamp 0..10; hill climb giữ bản tốt hơn (`skill_eval.py:45–58,129–156,204–229`). Matrix pass dùng min của điểm trung bình theo model (`:81–101`): một task/tiêu chí critical có thể bị các điểm khác bù; chưa có critical-failure veto.
- **Đã có, chắc chắn:** runner chỉ được truyền model/skill/prompt/sandbox; rubric được ghi ở judge adapter (`scripts/skill-eval.py:147–161`). **Chưa xác minh:** khả năng giữ rubric kín với candidate trên host thật; cwd và file name ngẫu nhiên không phải filesystem isolation.
- **Thiếu trong phạm vi API đã đọc:** run ID/task revision, structured tool trace, artifact hash/path validation, durable evidence store, deterministic verification assertions trước judge, model-blind evidence envelope. Cần thiết kế trước khi sửa Runner return type vì test và CLI phụ thuộc string.
- **Chắc chắn:** CI wired board, hard-check PR changed files, feature-map PR changed files, unittest, adapter/index, skill links, registry, CSO và doctor (`.github/workflows/check.yml:115–168`). Đây là wiring tĩnh, không chứng minh pipeline mới nhất xanh hoặc verification end-to-end đã chạy.
- **Chưa xác minh:** runtime lease/authorization, approval identity bên ngoài quyền AI, knowledge context pack/source freshness và SDLC bảy state có thực thi. Tìm trong agent_core không thấy implementation những tên này; không khẳng định về host hoặc hệ thống ngoài repo. Handoff role mapping không đủ thay thế RACI.

## Phạm vi implementation gợi ý cho Architect

1. Thư viện discovery/parser canonical có adapter giữ CLI hiện tại; hỗ trợ nested epic, lowercase states, subtask ID, duplicate/dangling/cycle và trạng thái không runnable. Để CLI, board, audit/next dùng cùng contract; test regression legacy card.
2. Module knowledge riêng + schema/version/source/hash/review-state/role-task links; context resolver deterministic, kiểm stale/missing/dangling/cycle; draft không tự thành policy. Phân phối knowledge data explicit.
3. Workflow activity/RACI/7-step assessment riêng; một A/activity, proof gắn transition. Tách model dữ liệu và validation khỏi enforcement authorization chưa được cấp.
4. Evidence record/persistence và verification fixture bootstrap/diff; archive proof trước cleanup, relative artifact validation, command/result/revision/hash, redaction và retention rõ.
5. Eval adapter tương thích legacy string, structured candidate result; deterministic proof checks trước judge, chấm mù, rubric không đưa candidate, critical fail veto; phân biệt mock/offline test với live model eval.
6. Integration scope riêng cho `agents/manifest.txt`, `.github/workflows/check.yml`, `pyproject.toml` và protocol dùng chung. Không để nhiều worker cùng sửa những file này.

## Working tree và phần chưa phân tích

Snapshot `git status --short` được lấy trước khi T-11.1 ghi file. **Chắc chắn:** đã dirty các vùng `agent_core/debt/`, `agent_core/eval/cso_scanner.py`, `agent_core/workflow/handoff.py`, scripts checker/doctor/merge-gate/sync, CI, root docs, role/adapter/stack/protocol; các file mới skill_eval, bootstrap/diff, manifest/schema/pyproject, task tooling và tests đã untracked. Không gán những thay đổi này cho T-11.1. Danh sách đầy đủ ngay dưới là snapshot phục vụ tách commit; các agent khác có thể bổ sung file trong khi inventory chạy.

RK-2/card T-11 ghi dọn cookie/experimental scripts đã xử lý. Status hiện có deletion cookie examples/tools/tests và gemini research; inventory không dọn lại, không khôi phục và không đọc nội dung bí mật.

**Chưa phân tích:** toàn bộ diff cũ, tính đúng code reviewer/CSO/ingest/debt, tài liệu source PDF, runtime model/network, permissions host, branch mutation, bootstrap/diff fixture thật, CI remote. Baseline/final test thuộc runner; không tái dùng PASS từ T-10. PROJECT.md vẫn là mẫu chưa khai báo stack/lệnh (`PROJECT.md:7–26`), cần Lead chốt trong spec thay vì tự chọn pytest.

### Snapshot dirty trước khi ghi báo cáo

```text
 M .agents/rules/agents-core.md
 M .agents/rules/role-ai-eng.md
 M .agents/rules/role-analyst.md
 M .agents/rules/role-architect.md
 M .agents/rules/role-ba.md
 M .agents/rules/role-data-eng.md
 M .agents/rules/role-dba.md
 M .agents/rules/role-debt-hunter.md
 M .agents/rules/role-designer.md
 M .agents/rules/role-dev.md
 M .agents/rules/role-devops.md
 M .agents/rules/role-mobile.md
 D .agents/rules/role-orchestrator.md
 M .agents/rules/role-product.md
 M .agents/rules/role-qa.md
 M .agents/rules/role-researcher.md
 M .agents/rules/role-reviewer.md
 M .agents/rules/role-runner.md
 M .agents/rules/role-security.md
 M .agents/rules/role-sre.md
 M .agents/rules/role-writer.md
 M .agents/skills/archify/SKILL.md
 M .agents/skills/browse/SKILL.md
 M .agents/skills/diagram-design/SKILL.md
 D .agents/skills/gemini-deep-research/SKILL.md
 M .agents/skills/subagent-driven-development/SKILL.md
 M .githooks/pre-push
 M .github/copilot-instructions.md
 M .github/pull_request_template.md
 M .github/workflows/check.yml
 M .gitignore
 M .kilo/agents/ai-eng.md
 M .kilo/agents/analyst.md
 M .kilo/agents/architect.md
 M .kilo/agents/ba.md
 M .kilo/agents/data-eng.md
 M .kilo/agents/dba.md
 M .kilo/agents/debt-hunter.md
 M .kilo/agents/designer.md
 M .kilo/agents/dev.md
 M .kilo/agents/devops.md
 M .kilo/agents/mobile.md
 D .kilo/agents/orchestrator.md
 M .kilo/agents/product.md
 M .kilo/agents/qa.md
 M .kilo/agents/researcher.md
 M .kilo/agents/reviewer.md
 M .kilo/agents/runner.md
 M .kilo/agents/security.md
 M .kilo/agents/sre.md
 M .kilo/agents/writer.md
 M AGENTS.md
 M CLAUDE.md
 M CODEX.md
 M GEMINI.md
 M README.md
 M agent_core/debt/ledger.py
 M agent_core/debt/parser.py
 M agent_core/eval/cso_scanner.py
 M agent_core/workflow/handoff.py
 M agents/knowledge/skills.md
 M agents/knowledge/tech-radar.md
 M agents/models.txt
 M agents/protocols/definition-of-done.md
 M agents/protocols/handoff-note.md
 M agents/protocols/mcp-policy.md
 M agents/protocols/message.md
 M agents/protocols/model-policy.md
 M agents/protocols/onboarding.md
 M agents/protocols/risk-gate.md
 M agents/protocols/skills-policy.md
 M agents/protocols/task-card.md
 M agents/roles/analyst.md
 M agents/roles/architect.md
 M agents/roles/ba.md
 M agents/roles/dba.md
 M agents/roles/designer.md
 M agents/roles/dev.md
 D agents/roles/orchestrator.md
 M agents/roles/qa.md
 M agents/roles/researcher.md
 M agents/roles/reviewer.md
 M agents/roles/runner.md
 M agents/roles/writer.md
 M agents/stacks/python.md
 D cookies/README.md
 D cookies/all_accounts.example.json
 M docs/DEBT.md
 D gemini_cookies.example.json
 M scripts/check-skills.py
 M scripts/convert-docs.py
 M scripts/cso.py
 M scripts/doctor.py
 M scripts/fetch-skills.py
 D scripts/gemini-research.py
 M scripts/merge-gate.py
 M scripts/simulate-agent-lifecycle.py
 M scripts/sync-adapters.py
 M tasks/_template.md
 D tests/test_cookie_rotation.py
 M tests/test_cso_scanner.py
 M tests/test_debt.py
 M tests/test_merge_gate_e2e.py
 M tests/test_security_rules.py
 D tools/cookie_rotation/__init__.py
 D tools/cookie_rotation/account_manager.py
 D tools/cookie_rotation/cookie_rotator.py
?? .agents/rules/role-lead.md
?? .agents/skills/codebase-map/
?? .agents/skills/diagram-design/references/layout-and-components.md
?? .agents/skills/diagram-design/references/pre-output-checklist.md
?? .agents/skills/diagram-design/references/svg-primitives.md
?? .agents/skills/feature-map/
?? .agents/skills/subagent-driven-development/references/
?? .claude/agents/
?? .codex/
?? .kilo/agents/lead.md
?? .qoder/
?? agent_core/eval/skill_eval.py
?? agents/manifest.txt
?? agents/protocols/agent-base-sync.md
?? agents/protocols/atomic-changes.md
?? agents/protocols/bug-repro.md
?? agents/protocols/deploy.md
?? agents/protocols/feature-map.md
?? agents/protocols/full-workflow.md
?? agents/protocols/hard-rules.md
?? agents/protocols/skill-eval.md
?? agents/protocols/task-branch.md
?? agents/protocols/ui-fidelity.md
?? agents/roles/lead.md
?? archify
?? archify.cmd
?? docs/HARD-RULES.json
?? docs/HARD-RULES.md
?? docs/analysis/T-09-ai-sdlc-application.md
?? docs/analysis/T-11-current-state.md
?? docs/notes/INDEX.md
?? docs/notes/inbox/RK-2-lead.md
?? docs/notes/inbox/T-02-orchestrator.md
?? docs/notes/inbox/T-03-dev.md
?? docs/notes/inbox/T-04-dev.md
?? docs/notes/inbox/T-05-dev.md
?? docs/notes/inbox/T-06-lead.md
?? docs/notes/inbox/T-06-reviewer.md
?? docs/notes/inbox/T-06.1-dev.md
?? docs/notes/inbox/T-06.2-dev.md
?? docs/notes/inbox/T-06.3-dev.md
?? docs/notes/inbox/T-06.4-dev.md
?? docs/notes/inbox/T-06.5-dev.md
?? docs/notes/inbox/T-06.6-devops.md
?? docs/notes/inbox/T-06.7-qa.md
?? docs/notes/inbox/T-07-lead.md
?? docs/notes/inbox/T-08-lead.md
?? docs/notes/inbox/T-08-reviewer.md
?? docs/notes/inbox/T-09-analyst.md
?? docs/notes/inbox/T-09-lead.md
?? docs/notes/inbox/T-10-lauren-researcher.md
?? docs/notes/inbox/T-10-lead.md
?? docs/notes/inbox/T-10-pstack-researcher.md
?? docs/notes/inbox/sync-claude-agents-claude.md
?? docs/research/2026-10-18-graphify.md
?? docs/research/2026-10-19-lauren-tan-talk-anh-xa.md
?? docs/research/2026-10-27-lauren-tan-primary-sources.md
?? docs/risk/RK-1.md
?? docs/risk/RK-2.md
?? examples/hard-rules/
?? examples/skill-eval/
?? pyproject.toml
?? schemas/
?? scripts/agent-base-diff.ps1
?? scripts/agent-base-diff.py
?? scripts/agent-base-diff.sh
?? scripts/bootstrap-project.ps1
?? scripts/bootstrap-project.py
?? scripts/bootstrap-project.sh
?? scripts/card-audit.py
?? scripts/deploy.py
?? scripts/feature-map-check.py
?? scripts/generate-dashboard.py
?? scripts/hard-check.py
?? scripts/link-skills.py
?? scripts/next.py
?? scripts/notes-index.py
?? scripts/run-archify.mjs
?? scripts/setup-skills.ps1
?? scripts/setup-skills.py
?? scripts/setup-skills.sh
?? scripts/skill-eval.py
?? scripts/task-board.ps1
?? scripts/task-board.py
?? scripts/task-board.sh
?? scripts/task-branch.py
?? scripts/toggle-permissions.ps1
?? scripts/toggle-permissions.py
?? scripts/watch-swarm.py
?? setup.bat
?? setup.ps1
?? setup.sh
?? skills.config.json
?? tasks/BOARD.md
?? tasks/E1-nen-tang/
?? tasks/EPICS.md
?? tasks/T-02.md
?? tests/test_check_skills.py
?? tests/test_feature_map_check.py
?? tests/test_hard_check.py
?? tests/test_link_skills.py
?? tests/test_notes_index.py
?? tests/test_skill_eval.py
?? tests/test_sync_adapters.py
?? tests/test_viewer.py
?? tools/viewer/
```

## Câu hỏi thiết kế gửi Lead

- **Round 1 — discovery:** dùng frontmatter canonical với legacy parser fallback, hay ép migrate card? ➡️ Đề xuất: canonical + fallback có cảnh báo, không migrate hàng loạt.
- **Round 1 — verification/eval:** có cần live model run ở MVP hay mock/offline harness đủ cho nghiệm thu hạ tầng? ➡️ Đề xuất: nghiệm thu hạ tầng offline; live eval là bước riêng có model/chi phí/quyền rõ. Không gọi mock là live.
- **Round 1 — RACI:** ai cung cấp approval identity đáng tin? ➡️ Đề xuất: MVP kiểm cấu trúc và artifact binding; enforcement chỉ tuyên bố khi có thành phần ngoài quyền sửa AI.
