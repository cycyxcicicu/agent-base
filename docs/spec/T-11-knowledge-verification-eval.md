> Task: T-11 · Epic: E1 · Vai: architect

# T-11 — Tri thức, trách nhiệm và kiểm chứng có bằng chứng

Status: **PROPOSED — chờ người dùng duyệt spec và reviewer duyệt card triển khai**. Ngày: 2026-10-27. Không có chức năng nào dưới đây được tuyên bố đã triển khai. Mọi đường dẫn ghi «mới» là đề xuất, chưa phải file có sẵn. Không cấp quyền sửa AGENTS.md, roles, nguồn gốc, bí mật hoặc thay đổi có trước T-11.

## 1. Bối cảnh và lựa chọn

Nguồn nội bộ: [brief primary Lauren Tan](../research/2026-10-27-lauren-tan-primary-sources.md), [đối chiếu SDLC](../analysis/T-09-ai-sdlc-application.md), card T-11 và code được đọc ngày 2026-10-27. Brief upstream là snapshot main 0.15.34 chưa ghim SHA; không nhập mã/skill, không lấy ROI làm tiêu chí. PROJECT.md còn placeholder. CI thật hiện chạy `python -m unittest discover -s tests -v`; test mới phải được discovery này chạy được, không tự đổi stack hoặc thêm dependency.

| Phương án | Giá trị | Chi phí / ảnh hưởng | Quyết định đề xuất |
|---|---|---|---|
| Lean: nối Markdown + checklist thủ công | Ít file, học nhanh | Không kiểm link/version/context/proof nhất quán | Không đủ mục tiêu «thực hiện tất cả» |
| Balanced: JSON nguồn, validator và graph trong bộ nhớ, CLI fixture, proof và eval tương thích | Kiểm chứng được ngay, không DB/network mới | Khoảng 30–40 file mới/sửa, chia batch; approval vẫn phụ thuộc người/host | **Đề xuất** |
| Full: graph DB, identity gateway, lease và mọi tool qua broker | Có khả năng cưỡng chế runtime khi trust boundary đúng | Hạ tầng, auth, bypass và vận hành mới; chưa có brief/duyệt | Chỉ thiết kế tiếp sau duyệt trust boundary riêng |

Quyết định balanced là đề xuất có thể đảo ngược. Không tạo ADR «accepted» trước duyệt. Sơ đồ Archify JSON + HTML + index, CODEMAP và ADR quan trọng là deliverable riêng do Lead cấp scope; spec này không thay thế chúng. `docs/CODEMAP.md` chưa tồn tại lúc đọc, nên không khẳng định ranh giới đã được tài liệu hóa.

## 2. Từ điển và bounded contexts

| Entity | Nghĩa và trường riêng bắt buộc |
|---|---|
| Requirement | Điều phải thỏa; `acceptance_criteria`, không tự coi mọi đề xuất là yêu cầu đã duyệt |
| Rule | Invariant/quy tắc; `authority_ref`, `enforcement_refs`; thiếu enforcement phải ghi `advisory` |
| Design | Giải pháp/contract; `alternatives`, `decision_status` |
| Task | Lát cắt có scope và DoD; `card_path`, `blocked_by`, `requirement_refs` |
| Feature | Hành vi qua surface người dùng; `entrypoint`, `scenario_refs` |
| Scenario | Precondition → hành động → quan sát; `fixture`, `recipe`, `expected`, `negative` |
| Skill | Hướng dẫn thao tác đã có registry; `skill_path`, `registry_ref`, `eval_suite_refs` |
| EvalSuite | Đo phương pháp/skill; `case_refs`, `rubric_ref`, `critical_checks`, `budget`, `holdout_refs` |
| Proof | Kết quả một lần kiểm có revision/hash và artifact; `bundle_path`, `result`, `input_digest` |
| Approval | Quyết định trên artifact digest cụ thể; `activity`, `subject_digest`, `identity_evidence_ref` |
| Role | Chức trách RACI, không phải tài khoản/auth; `role_ref` trỏ vai hiện có |
| Source | Nguồn provenance; `locator`, `read_at`, `revision`, `license_or_unknown`, `review_due_at`, `claims` |

Knowledge context quản metadata/link; Workflow context quản card, RACI và gate; Verification context thực thi recipe fixture và giữ proof; Evaluation context quản candidate/judge và score. Các context dùng ID/digest qua interface, không import parser/private state của nhau. Không tạo lớp pass-through cho từng entity.

Tất cả node: `schema_version:1`, `id` duy nhất dạng `TYPE:slug`, `kind`, `title`, `state`, `version` số nguyên tăng, `content_ref` đường dẫn tương đối an toàn, `content_sha256`, `provenance:[Source ID]`, `owner_role`, `updated_at` UTC, `review_due_at`, `relations`. Metadata không chứa toàn văn bí mật hoặc chỉ dẫn thực thi từ nguồn ngoài. Hash tính trên bytes file; JSON digest dùng canonical UTF-8 sort keys, separators cố định. `revision` là commit SHA nếu có; working tree dirty có manifest hashes riêng, không giả rằng HEAD mô tả mọi byte đang chạy.

Typed relations (đầu → cuối): `derived_from:any→Source`; `refines:Requirement→Requirement`; `constrains:Rule→Requirement|Design|Task|Skill`; `implements:Task|Design|Feature→Requirement`; `realizes:Task→Design`; `verified_by:Requirement|Feature→Scenario`; `executed_by:Scenario→Skill`; `evaluated_by:Skill→EvalSuite`; `evidenced_by:Scenario|Task|EvalSuite→Proof`; `approved_by:any trừ Approval→Approval`; `owned_by:any trừ Role→Role`; `supersedes:cùng kind→cùng kind`; `depends_on:Task→Task`. Validator kiểm đầu/cuối, node dangling, ID trùng, self edge, cycle của depends_on/refines/supersedes. Cycle thông thường khác chỉ cảnh báo có giới hạn traversal, không cấm mọi graph cycle.

State machine: `draft→review→approved`; review có thể về draft; approved→stale khi hash/source/approval hết hạn hoặc dependency thay đổi; stale→review sau cập nhật; draft/review/approved/stale→deprecated với lý do/replacement. Không đi thẳng draft→approved. `deprecated` không được context mặc định chọn. Đổi nội dung tạo version mới và invalidates approval/proof liên quan; không sửa lịch sử proof. Validator có thể báo trạng thái stale hiệu lực ngay cả khi file chưa được viết lại. Human policy gốc giữ thẩm quyền cao hơn graph; node approved sai hoặc giả không cấp quyền.

## 3. Interface và context theo vai

Các module mới đề xuất: `agent_core/knowledge/` với interface `load_catalog(root) -> Catalog`, `validate(catalog, as_of) -> Diagnostics`, `build_context(catalog, request) -> ContextBundle`; `agent_core/workflow/task_discovery.py` với `discover_tasks(root) -> cards`; `agent_core/verification/` với `verify(request) -> ProofBundle`. Module knowledge ẩn parsing, traversal, freshness, ranking; callers không tự chọn glob hoặc suy policy.

Nguồn tri thức mới `agents/knowledge/knowledge-manifest.json` khác trách nhiệm `agents/manifest.txt` (phân phối). Manifest tri thức chỉ allowlist nguồn, typed node/link, schema version và quyền sử dụng theo vai; không tự quét toàn repo hoặc đọc docs/source/bí mật. Source chưa ghim revision được ghi `unverified_revision`, không dùng làm policy đã duyệt. Seed chỉ metadata dẫn đến nguồn nội bộ có thật; mẫu đề xuất giữ draft, không tự tạo phê duyệt.

CLI mới `scripts/knowledge.py validate|context --root ... --role ... --task ... --as-of ... --budget ... --format json`. Exit 0 hợp lệ, 1 lỗi nội dung/freshness cần thiết, 2 lỗi đầu vào, 3 thiếu approval tin cậy. `--as-of` bắt buộc trong fixture, mặc định UTC hiện tại khi dùng thật và ghi vào output. Context chọn: mandatory policy refs + task + dependencies + approved relevant nodes; draft/review chỉ ở appendix có nhãn khi `--include-draft`, không làm instruction. Thứ tự deterministic `(priority, kind, id, version)`, traversal breadth-first với visited set, ID tie-break. Không LLM retrieval ở pha đầu.

Token budget v1 là **đơn vị ước lượng bảo thủ**, `ceil(UTF8_bytes/3)`; output ghi `budget_method`, `estimated_tokens`, `omitted_ids`, lý do và input digests; không gọi là tokenizer chính xác. Không cắt giữa node. Nếu mandatory context vượt budget thì fail rõ, không bỏ policy âm thầm. Cùng catalog bytes/request/as_of cho output bytes giống nhau. Task discovery recursive `T-*.md` có frontmatter ID, bao gồm epic/subtask, bỏ template/BOARD; ID/path trùng, symlink thoát root hoặc card malformed phải lỗi, không âm thầm ghi đè. CLI frontier và Board phải dùng cùng discovery interface sau migration.

Task status canonical là YAML lowercase `todo/doing/review/done/blocked`; adapter hỗ trợ uppercase legacy hiện có, báo lỗi nếu YAML và legacy mâu thuẫn. ID chấm như T-11.2 được discovery/parser hỗ trợ, không vì vậy khẳng định branch tool hỗ trợ. I3 sở hữu thêm `agent_core/workflow/tracer_bullet.py` (hiện có) để mở parser có regression tests giữ callers cũ. Source locator phải allowlist cả path và section/anchor; thiếu section cần thiết là missing source, không tự tìm thay thế ngoài allowlist.

## 4. RACI và bảy cổng SDLC

Mỗi activity có đúng một A, ít nhất một R, C/I có thể rỗng; người giữ nhiều vai vẫn không tự làm independent review phần mình. Mapping vai trong JSON chỉ mô tả trách nhiệm. Approval hợp lệ phải có bằng chứng danh tính từ người dùng/host ngoài quyền ghi của AI, binding activity + input/subject digest + thời điểm + quyết định; YAML `approved:true`, tên người tự gõ hoặc hash-chain do AI sửa không xác thực được người. Pha balanced trả `unverified`/exit 3 khi thiếu verifier đáng tin; không tạo auth giả. Người dùng quyết định qua kênh tin cậy hiện có, Lead lưu reference; reviewer check vẫn có giới hạn thủ công được ghi rõ.

## 4. Hệ thống 8 Cổng kiểm soát và Trách nhiệm (Căn chỉnh theo task-loop.md)

> *Ghi chú căn chỉnh (T-19.1)*: Đổi cấu trúc 7 gate cũ (G1–G7) sang chuẩn **8 Cổng kiểm soát (Cổng 0–7)** của quy trình *AI in SDLC* (trang 21–22) và `agents/protocols/task-loop.md`. Đổi vì: chuẩn 8 cổng phân định rõ các chốt chặn của con người, tách biệt Cổng 6 (Hoàn thành kỹ thuật) và Cổng 7 (Nghiệm thu nghiệp vụ), đồng thời bổ sung cổng Actor (Cổng 4) và chế độ kiểm tuân thủ độc lập A4.

| Cổng kiểm soát | Hoạt động & Nội dung | Người thực hiện (R) | Người chịu trách nhiệm (A) | Kiểm tra sản phẩm và bằng chứng |
|---|---|---|---|---|
| **Cổng 0** | Nhật ký thay đổi phiên trước | dev / writer | con người (Lead/User) | Trạng thái `Approved` trong file nhật ký; AI cấm tự đóng |
| **Cổng 1** | Duyệt đầu mục tài liệu & yêu cầu R-xxx | ba | con người (User/PO) | Cột `Xác nhận = Yes` trong RTM; AC đo được, nguồn rõ ràng |
| **Cổng 2** | Duyệt thiết kế kỹ thuật chi tiết / spec | architect | con người (Tech Lead/User) | Trạng thái `Approved` trong file spec/ADR; reviewer verdict |
| **Cổng 3** | Duyệt ADR khi có >= 2 lựa chọn | architect | con người (User/Lead) | Bảng 3 phương án, đánh đổi, rủi ro, hoàn tác |
| **Cổng 4** | Duyệt Actor, phân quyền và hệ thống ngoài | ba / security | con người (User/Security) | Danh sách actor/role được kiểm toán, không lộ bí mật |
| **Cổng 5** | Duyệt WBS (người chịu trách nhiệm + ngày) | lead | con người (User) | Card phân rã hợp lệ, scope không chồng, SEQ tuần tự |
| **Cổng 6** | Xác nhận hoàn thành kỹ thuật (Technical Sign-off) | qa / reviewer | **CHỈ CON NGƯỜI GHI** | Toàn bộ test 100% PASS, bằng chứng chạy thật, A4 audit PASS |
| **Cổng 7** | Nghiệm thu chức năng (Business Acceptance) | lead / ba | **CHỈ CON NGƯỜI GHI** | Cột `Function_RTM.Xác nhận = Yes`; người dùng nghiệm thu trên local |

Gate evaluation ở chế độ cố vấn (advisory diagnostic) trước khi có runtime hook. Mỗi cổng gắn với digest nội dung; bất kỳ thay đổi nào làm stale dấu duyệt thì cổng downstream tự động chuyển sang `pending`. Kiểm tra tuân thủ độc lập (**Chế độ A4**) do `reviewer` hoặc `qa` thực hiện đối soát diff ↔ kế hoạch ↔ RTM; chỉ A4 có quyền xác nhận "Đã đối soát qua công cụ".

## 5. Proof và verification thật trên fixture

Schema mới `schemas/proof.schema.json` theo JSON Schema draft 2020-12; runtime validator bằng stdlib cho tập contract dùng thật, không tuyên bố full JSON Schema engine hoặc thêm package khi chưa duyệt. `additionalProperties:false` tại envelope; `schema_version`, `run_id`, `scenario_id`, `phase:baseline|final`, `started_at`, `ended_at`, `result:pass|fail|inconclusive|skipped`, `repo_revision`, `dirty_input_manifest`, `input_digest`, `tool_versions`, `commands`, `assertions`, `artifacts`, `trace`, `cleanup`, `limitations` bắt buộc. Timestamp ISO UTC; SHA 64 hex; enums và cross-field validation được test.

Command record: `sequence`, argv list (không shell string), cwd tương đối fixture, timeout, exit code hoặc timeout/launch error, duration_ms, stdout/stderr artifact refs và hash. Artifact: relative path dưới evidence root, sha256, byte_count, media_type, producer command sequence; từ chối absolute/`..`/symlink escape. Trace: event sequence, actor loại, action, path/action target, result, timestamp, evidence ref; mỗi event có `capture:observed|reported`. Self-report không đáp ứng required read/write/command assertion. `assertions` ghi expected/observed/pass và proof refs, không chỉ text «đã chạy». Redact hoặc không thu môi trường/secret; output có secret nghi ngờ thì fail export, giữ thông báo giới hạn thay vì in nội dung.

Evidence root nằm ngoài sandbox tạm. Trình tự: launch fixture → doctor → drive command thật → kiểm hậu điều kiện → chụp/hash/validate/export proof → judge (nếu cần) → cleanup chỉ run-owned resources → re-open toàn bộ proof và hash xác nhận còn đọc được. Cleanup failure có field riêng, không che primary failure và không báo clean. Baseline/final riêng run IDs cùng scenario/input origin, ghi revision và byte hashes riêng; bản fail không được thay bằng bản pass. Local hashes phát hiện thay đổi, không chống được người có quyền viết lại toàn bộ store.

CLI mới `scripts/verify.py bootstrap|upgrade --evidence-root <dir> [--keep-fixture]`: không nhận target dự án thật ở pilot; harness tự tạo fixture `TemporaryDirectory` với ownership sentinel, không dùng HOME, Downloads, cookies, user repo hoặc network. Giao diện CLI là user surface thay UI; mỗi slice đi đủ fixture data → Python interface → CLI output → unittest end-to-end.

Harness chỉ chạy argv local do card/spec giao, allowlist executable/operation, không execute command string lấy từ knowledge manifest, web, artifact hoặc source text. Offline fixture/subprocess là mặc định; model adapter giả lập chỉ xác minh protocol.

Bootstrap recipe: cài framework qua CLI hiện có vào fixture trống → doctor theo contract thực tế → kiểm file manifest distribution, file fresh trống, template không mang nội dung repo, generated từ nguồn đúng. Upgrade recipe: bootstrap phiên bản fixture baseline → sửa template dự án + copy file tạo conflict → chạy diff/upgrade flow hiện có theo chế độ được duyệt → kiểm preserve customization, báo conflict, dry-run không đổi bytes, rerun idempotent. Không phát minh lệnh upgrade nếu code chưa có: adapter recipe bọc flow hiện hành; hành vi mới cần card riêng. Launch thất bại, output sai exit 0, artifact mất, timeout, stale input, escaping path đều là case fail, không skip thành pass.

## 6. Eval migration không phá callers

Hiện `run_matrix(skill_text,tasks,models,judge_model,rubric,runner,judge,sandbox_base=None,allow_same_family=False)` nhận Runner trả str; Judge nhận output str; `CellResult` có 5 positional fields; `MatrixResult.passed` dựa trung bình theo model; cleanup trước judge. Giữ chữ ký và nghĩa legacy trong Expand, thêm field có default sau fields cũ. Không thay positional callback/string thành object âm thầm.

Thêm opt-in `run_matrix_with_evidence(request, candidate_runner, evidence_judge, collector)` trong cùng module; `CandidateResult` gồm output, trace/manifest/artifact refs, capture limitations. Collector chỉ thu fixture allowlist trước cleanup và export; judge nhận **sanitized bundle**, không model name, provider, path/tên file gợi model, rubric leak từ candidate output hoặc metadata không cần thiết. Candidate chỉ thấy skill/prompt/fixture; rubric, expected assertions và holdout nằm ngoài candidate workspace. Nhãn ngẫu nhiên A/B ánh xạ trong coordinator-only store, làm sạch cả output/trace. Đây là giao thức chấm mù; subprocess cùng OS user không phải security isolation và có thể đọc ngoài cwd. Eval đối kháng thực sự chỉ được gọi «isolated» khi host/container ACL có chứng minh.

Kiểm deterministic assertions trước judge; thiếu observed trace bắt buộc → inconclusive, fabricated proof/path escape/forbidden write → critical fail. Pass v2 cần đủ required cells, zero critical fail, từng case đạt `case_min_score`, từng criterion required đạt ngưỡng và từng model mean đạt target; missing case/judge malformed/NaN/out-of-range/error/timeout không được clamp thành pass. Tối thiểu pilot 6 case: happy path, conflict preservation, stale/missing knowledge, fabricated artifact, cleanup persistence, forbidden path; có ít nhất 2 holdout khác prompt tuning. Report giữ baseline/final, lowest case, counts fail/inconclusive/critical, score và capture limitations. Mock callback tests là contract tests, không gọi live model eval. Paid/live run cần model adapter và budget riêng được duyệt; không bắt CI gọi model.

`scripts/skill-eval.py` giữ rubric/plan/run và placeholders cũ; opt-in `--evidence-mode --evidence-root` dùng v2; hill_climb legacy giữ nguyên, v2 chỉ nhận candidate khi critical checks không lùi, hết budget/round/patience thì dừng, không tự ghi SKILL.md. Tests legacy và examples phải còn chạy. Contract chỉ xóa API cũ sau khi tìm mọi caller, migration, deprecation được duyệt; không nằm pilot.

I11 phải có regression riêng cho literal `{UUID}` trong đường dẫn lệnh/TEMP: hiện `tok.format(**values)` hiểu chúng như placeholder và QA đã tái hiện hai failure CLI; chỉ thay placeholders được hỗ trợ, giữ literal braces và phát hiện placeholder thiếu có chủ ý. Không sửa TEMP để né lỗi; không gộp các failure fixture Git/mklink chưa phân loại thành bug implementation.

## 7. Phân rã và sở hữu file đề xuất

Mỗi hàng là card độc lập, một subagent mới tối đa 8–10 tool calls; nếu vượt phải bàn giao và chia tiếp, không gộp nguyên feature lớn. Tất cả đường dẫn mới dưới đây **proposed**. Scope deny chung: AGENTS.md, agents/roles/**, docs/source/**, .env*, generated adapters, mọi file không trong hàng, mọi dirty change cũ. Card/note riêng tự được phép. Task chạy lại cùng file phải tuần tự; không cấp scope wildcard cả scripts/ hoặc tests/.

## 7. Phân rã lát cắt Pilot và Ánh xạ sang Epic E2 (T-20..T-29)

> *Ghi chú căn chỉnh (T-19.2)*: Thu hẹp phạm vi spec T-11 thành một lát cắt pilot kiểm chứng được trong Epic E2. Các slice được ánh xạ trực tiếp sang các task card T-20..T-29. Slice I6 (gate/RACI runtime check), I12 (kho seed tri thức mở rộng) và I14 (sơ đồ Archify tương tác) được **hoãn sau pilot** (lý do: ưu tiên hoàn thiện bề mặt kiểm chứng CLI và contract thực tế trước khi phát triển runtime gatekeeper phức tạp).

| Slice | Card E2 phụ trách | scope_edit chính xác | blocked_by | Yêu cầu R-xxx & Tiêu chí nghiệm thu |
|---|---|---|---|---|
| **I1 catalog validate** | **T-20** | `agent_core/knowledge/__init__.py`, `agent_core/knowledge/catalog.py`, `schemas/knowledge.schema.json`, `tests/test_knowledge_catalog.py` | T-12, T-19 | **R-01, R-02**: validate fixture catalog node/state/typed links, reject malformed/dangling/cycle (11 rule V00-V10) |
| **I2 context CLI** | **T-21** | `agent_core/knowledge/context.py`, `scripts/knowledge.py`, `tests/test_knowledge_context.py` | T-20 | **R-03, R-04**: CLI trích xuất ngữ cảnh theo vai/task, giới hạn ngân sách token tất định (`ceil(bytes/3)`) |
| **I3–I5 task discovery** | **T-22** | `agent_core/workflow/task_discovery.py`, `agent_core/cli.py`, `scripts/task-board.py`, `scripts/card-audit.py`, `scripts/next.py`, tests liên quan | T-12, T-19 | **R-05**: Hỗ trợ đồng nhất card lồng `tasks/E*-*/` trên toàn bộ CLI và frontier |
| *(Mới) claim_task* | **T-23** | `scripts/claim-task.py`, `schemas/claim-lease.schema.json`, `tests/test_claim_task.py` | T-13, T-22 | **R-06, R-07**: Chẩn đoán tiền điều kiện nhận task (G0-G5, SEQ, DoR, cam kết file có băm SHA) |
| *(Mới) RTM generator* | **T-24** | `scripts/generate-rtm.py`, `docs/RTM.md`, `tests/test_generate_rtm.py` | T-18, T-22 | **R-08, R-09**: Tự động sinh bảng RTM hai chiều từ card/manifest, phát hiện thiếu độ bao phủ |
| **I7–I9 proof & verify** | **T-25** | `agent_core/verification/**`, `schemas/proof.schema.json`, `scripts/verify.py`, `tests/test_verify_bootstrap.py`, `tests/test_verify_upgrade.py` | T-12, T-19, T-17 | **R-10, R-14**: Chạy kiểm chứng thực tế bootstrap/upgrade trên fixture cô lập, xuất proof bundle |
| *(Mới) repro harness* | **T-26** | `scripts/verify.py` (mở rộng), `docs/design/feature-map.md`, `docs/runbooks/verification-cli.md`, `tests/test_bug_harness.py` | T-25, T-15 | **R-11, R-12**: Harness tái hiện lỗi độc lập 2 lần có reset (Benny/GDT) và Feature Map cho CLI |
| **I10–I11 eval v2** | **T-27** | `agent_core/eval/skill_eval.py`, `scripts/skill-eval.py`, `tests/test_skill_eval_evidence.py` | T-25 | **R-13**: Khung eval chấm mù có bằng chứng, đã vá lỗi format chuỗi `{}` trong môi trường TEMP |
| **I15 phân phối & CI** | **T-28** | `agents/manifest.txt`, `.github/workflows/check.yml`, `scripts/bootstrap-project.py`, `scripts/agent-base-diff.py`, seed tối thiểu | T-21, T-23, T-24, T-26, T-27 | **R-14**: Tích hợp CI và phân phối an toàn (chỉ thực hiện sau khi có phiếu rủi ro RK APPROVED) |
| **I16 audit & QA E2** | **T-29** | card/note riêng, không sửa code implementation | T-22, T-23, T-24, T-26, T-27, T-28 | **Nghiệm thu E2**: Rà soát độc lập toàn diện quy trình, kiểm tra tính tuân thủ và hồi quy |
| *I6 gate runtime check* | *(Hoãn)* | `agent_core/workflow/gates.py` | Sau pilot | *Hoãn sau pilot*: chuyển sang dùng T-23 cố vấn trước khi xây dựng runtime engine chặn ghi |
| *I12 seed tri thức lớn* | *(Hoãn)* | `agents/knowledge/knowledge-manifest.json` | Sau pilot | *Hoãn sau pilot*: sử dụng fixture nhỏ trong pilot, tránh phình dữ liệu chưa kiểm chứng |
| *I14 sơ đồ Archify* | *(Hoãn)* | `docs/diagrams/T-11-system.html` | Sau pilot | *Hoãn sau pilot*: CODEMAP.md (T-17) đã đáp ứng định hướng tài liệu ban đầu |

Điều chỉnh ownership I3 chính thức gồm cả `agent_core/workflow/tracer_bullet.py`; không task khác được sửa file đó song song. Chưa thống nhất discovery ở audit/next: sau I5 thêm I5b sở hữu `scripts/card-audit.py`, `scripts/next.py` (hiện có), `tests/test_audit_discovery.py`, blocked_by I3,I5; chỉ migrate discovery và giữ validation/CLI hiện hành. I16 chờ thêm I5b. Đây là phạm vi chính xác để Lead chuyển thành card, không cấp scope ngầm.

I15a và I15b là hai phiên bắt buộc, không giao chung một subagent. Nếu bootstrap/diff có bug cần sửa trước I9, tạo card corrective riêng và tuần tự bàn giao I15b, không cho I9 tự sửa ngoài scope. Catalog fixtures đặt inline ở test ban đầu để tránh shared fixture churn. Các schema đi cùng executable user slice, không task DB-only/API-only. Không DB nên «DB» trong vertical slice là JSON fixture persistence. Mọi tài liệu proposed có owner ở I13/I14; ADR tương lai chỉ được tạo qua card mới scope chính xác sau duyệt, chưa có ADR accepted. BA chuẩn bị danh sách R riêng, người dùng duyệt rồi mới map vào slices; Lead điều phối mapping, không thay thẩm quyền duyệt nghiệp vụ.

## 8. Expand–Migrate–Contract, an toàn và nghiệm thu

Blast radius >10 file và shared interface nên bắt buộc ba pha. Expand: I1–I3,I6–I8,I10 thêm opt-in, legacy CI xanh, không đổi layout root. Batch migrate: I4/I5 callers discovery; I9/I11 recipe/eval; I12/I13 docs và seed; I15 phân phối. Contract: chỉ sau inventory import/callers và downstream upgrade fixture xanh; không xóa launcher/API cũ, không di chuyển cookie hoặc làm lại RK-2. Thay layout launcher là T-08 riêng, cần compatibility wrapper và manifest diff được duyệt; T-11 không ngầm nhận scope đó.

**Hardblock trước code:** Lead đã chạy task-branch dry-run nhưng thiếu `.deploy.json`; architect/Lead không được tạo config hoặc sửa protected script để né. Tool hiện chỉ nhận ticket số nguyên, không ID chấm. Lead cần người dùng thiết lập cấu hình qua quy trình hợp lệ và chốt mapping: T-11.n là ID chuẩn bị/conceptual, mỗi leaf triển khai dùng card top-level ID số nguyên mới liên kết `parent:T-11`, tên nhánh do task-branch tạo. Nếu muốn branch trực tiếp ID chấm thì cần người dùng chốt ngoại lệ/quy trình mới trước code. Không tự git switch/checkout hoặc dùng một nhánh main cho code. Card child chưa có nhánh hợp lệ phải blocked dù spec được duyệt.

Baseline runner báo 234 tests/38 failures/3 errors/1 skip; chưa xác minh từng failure. QA đã cô lập 2/17 skill-eval tests lỗi literal braces; phần Git config/mklink có dấu hiệu bị môi trường chặn. Hard-check và adapter check pass không làm full suite xanh; notes-index còn RK-2 summary fail ngoài scope. Đầu vào kiểm chứng chi tiết là `docs/analysis/T-11-current-state.md` và `docs/notes/inbox/T-11-baseline-qa.md`; không tái gán dirty bytes cũ cho T-11.

Phân phối: copy knowledge schema/module/script theo manifest distribution hiện hành, nhưng project knowledge seed phải template/fresh với tham chiếu framework riêng, không mang card/proof/approval/nguồn project agent-base sang dự án mới. Quy tắc precedence template/fresh trước copy được test. Upgrade phải xác định base hashes, preserve tùy chỉnh, báo conflict và không overwrite nếu không đủ approval; không tự thêm chế độ destructive. Compatibility test cài từ snapshot fixture trước và hiện tại, không git checkout hoặc sửa thư mục người dùng.

10x: thử 10.000 node/50.000 edge, traversal O(V+E), index ID một lần, bounded context output, giới hạn input bytes/nodes và output artifact. Benchmark ghi máy/dataset/thời gian thực, mục tiêu pilot validate/context ≤5s và ≤256MB trên Windows CI; fail mục tiêu thì tối ưu/điều chỉnh qua review, không tự đổi ngưỡng. Không DB/DDL/table lock, không migration dữ liệu thật. Idempotence: validate/context không ghi; run_id riêng, publish evidence atomic temp→rename trong run-owned root, không overwrite run có sẵn; bootstrap/upgrade rerun preserve/conflict deterministic. Log JSON run_id/stage/event/result/duration, counts stale/missing/critical/cleanup; CLI nonzero là alert CI, chưa có daemon/monitoring.

Rollback mục tiêu dưới 60s chỉ là dừng opt-in CLI và quay về flow legacy chưa đổi; đo bằng fixture. Không cam kết phục hồi data ngoài fixture. Hoàn tác code, ghi đè, mass move/delete, shared files ngoài scope hoặc triển khai phải có phiếu risk mới đúng HEAD/hash, không dùng RK-2. Không cung cấp lệnh destructive trong spec. Chưa chạy load test/rollback drill/live model eval ở pha thiết kế.

DoD: mọi R-xxx được BA/Lead duyệt phải có mapping sang slice (hiện chưa có danh sách R mới được duyệt, không tự gán ID giả); required catalog link/source/hash/state đúng; seven gates và RACI check fail đúng âm; baseline/final proof còn sau cleanup và replay; legacy eval/import/CLI giữ tương thích; v2 critical fail không bị mean che; bootstrap/upgrade fixture không chạm user dirs; manifest phân phối đúng và preserve customization; full unittest CI, hard-check, adapter/skills/notes freshness và merge gate theo card pass hoặc ghi rõ blocker; reviewer/QA độc lập; user xem diff và duyệt spec/risks; handoff có skill/checklist. Scope kiểm chứng phải phân biệt protocol, advisory validator, host enforcement. Không tuyên bố «permissions enforced» đến khi mọi write/exec/network/path route đi qua gateway đã được threat-model, test bypass và người dùng duyệt.

Cây quyết định mở cho pha sau: cần chặn trước ghi thực sự? Nếu không → balanced và ghi limitation. Nếu có → host có identity/ACL ngoài AI và broker cover mọi route? Không → blocked trust-boundary design; có → researcher/security/architect thiết kế gateway + leases có expiry/revocation/atomic scope acquisition và approval riêng. Không dùng YAML lease hoặc sandbox cwd để giả bảo vệ filesystem.
