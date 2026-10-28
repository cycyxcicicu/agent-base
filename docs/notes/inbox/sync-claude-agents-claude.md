> summary: Việc nhỏ: thêm .claude/agents/<vai>.md vào sync-adapters, bỏ vai lead khỏi danh sách
Task: (việc nhỏ, chưa có card)        Agent: claude        Ngày: 2026-10-18

## Đã làm
Thêm đầu ra `.claude/agents/<vai>.md` vào `scripts/sync-adapters.py` (hàm `build_claude`), nên Claude Code thấy 19 vai như subagent. Bỏ vai `lead` (mode `primary`).

## Lưu ý cho agent sau
- Bẫy hoặc hành vi bất ngờ: Claude Code chỉ giới hạn được CÔNG CỤ (`tools:`), không giới hạn theo đường dẫn như `edit_deny` của Kilo. Phạm vi sửa file và bash chỉ-đọc của vai trong Claude Code là luật bằng chữ (có ghi chú đầu thân file), không bị máy ép. Lưới cuối là `.claude/settings.json` (cấm git ghi) và `scripts/merge-gate.py`.
- Quyết định và lý do: `lead` không đăng ký vì subagent của Claude Code không gọi được subagent khác; phiên chính đóng vai lead. `model: inherit` thay vì ánh xạ tầng sang `opus/sonnet/haiku` để không tự đổi model của vai (AGENTS.md mục 14).
- Giả định chưa kiểm chứng: danh sách subagent chỉ hiện sau khi mở lại phiên Claude Code; chưa thử gọi từng vai. Định dạng lấy từ tài liệu code.claude.com/docs/en/sub-agents (đọc 2026-10-18).

## Việc dở dang hoặc nợ kỹ thuật
Chưa làm đầu ra cho Cursor, Copilot (chỉ có `copilot-instructions.md`).

## Cập nhật: Codex và Antigravity (2026-10-18)
- Codex: thêm `.codex/agents/<vai>.toml` (`build_codex`: name, description, developer_instructions; bỏ `lead`). Codex không cho agent riêng đổi sandbox/approval (kế thừa phiên chính), nên quyền vai chỉ là luật bằng chữ. Nguồn: learn.chatgpt.com/docs/agent-configuration/subagents (đọc 2026-10-18).
- **Antigravity: lỗi cũ.** Tài liệu (antigravity.google/docs/rules, đọc 2026-10-18) nói file trong `.agents/rules/` PHẢI có frontmatter `trigger` (`always_on|model_decision|glob|manual`), thiếu thì bị BỎ IM LẶNG. Các file `role-*.md` và `agents-core.md` sinh ra trước đây không có frontmatter nên Antigravity đã bỏ qua. Đã sửa: `role-*.md` dùng `trigger: model_decision` + `description`; `agents-core.md` dùng `trigger: manual` vì Antigravity đã đọc sẵn `AGENTS.md` ở gốc repo (không frontmatter) và `GEMINI.md`.
- Giới hạn 12.000 ký tự: tài liệu ghi 24 KB/file, ta giữ 12.000 cho an toàn và tính trên nội dung, không tính frontmatter.
- Chưa kiểm chứng bằng cách mở Antigravity thật. `GEMINI.md` và `AGENTS.md` cùng nội dung có thể bị nạp trùng.

## Ảnh hưởng đến task khác
Không.

## Đề xuất cập nhật quy ước hoặc tài liệu
README mục cấu trúc thư mục nên thêm dòng `.claude/agents/` (SINH RA).

## Đồng bộ ngược từ Humana (2026-10-18)
Đưa ngược bằng `agent-base-diff.py --push` từ `D:\congviec\Humana-Handover-Package\Humana-Handover`, đã sao lưu 27 file agent-base trước khi ghi (thư mục scratchpad của phiên, không nằm trong repo).
- Quy tắc/quy trình: `AGENTS.md` (thêm §16 Scrum subtasks + Plan Review Gate, §17 Skill Auto-Selection, rút gọn §13/§14/§15), `agents/protocols/` (definition-of-done, handoff-note, message, model-policy, skills-policy, task-card), `agents/stacks/python.md`, `agents/knowledge/skills.md`.
- Vai trò: architect, ba, dba, designer, dev, lead, reviewer, runner (archify, Plan Review, chống resume phiên lỗi).
- Script: merge-gate, task-branch, deploy, doctor, bootstrap-project, fetch-skills; mới: generate-dashboard, watch-swarm, run-archify.mjs, setup-skills.py/.ps1/.sh, `setup.*`, `archify`, `archify.cmd`, `schemas/`, `skills.config.json`.
- Skill: archify, browse. `manifest.txt` thêm các mục trên; `ANTIGRAVITY_LIMIT` 12000 → 16000.
- Đã sửa trong agent-base sau khi đẩy: `task-card.md` thay đường dẫn riêng Humana (`doc/0x-...`, `humana-system-archify.html`) bằng đường dẫn chung.
- Giữ bản agent-base (là tập cha): `sync-adapters.py` (có Claude/Codex/trigger Antigravity) và `manifest.txt` (đã gộp tay mục của Humana). Chưa kéo về Humana, chưa `--mark-synced`.
- Không đưa về (riêng Humana): `scripts/ops/*`, `test_*`, `seed_*`, `inspect_*`, `check_*`, các file figma, `*vps*`, `package_backend_release.py`, `rebuild-archify-diagrams.mjs`.
- Còn sót cũ: `scripts/task-branch.py` và `agents/protocols/task-branch.md` của agent-base còn chữ `humana-wt` / `D:\congviec\...` (có từ trước, chưa sửa).

## Tái cấu trúc bảng điều khiển → tools/viewer (2026-10-18)
- `scripts/generate-dashboard.py` (2216 dòng, xuất 1 file 6,3 MB) tách thành: `tools/viewer/dashboard/collect.py` (thu thập), `render.py` (dựng site), `tools/viewer/assets/` (`dashboard.css`, `dashboard.js`, `index.template.html`, `monitor.html`). Script cũ chỉ còn là điểm vào mỏng.
- Đầu ra mới ở `build/viewer/` (đã `.gitignore`): `index.html` + `data.js` + `docs/<id>.js` + `cards/<id>.js` + `cards/_search.js`. Nội dung tài liệu/card nạp khi mở, chỉ mục tìm toàn văn nạp khi gõ tìm kiếm; mở thẳng file:// vẫn chạy. Đo trên dữ liệu Humana (161 card, 201 tài liệu): tải đầu ~230 KB thay vì 6,3 MB; không lỗi console, mở tài liệu, mở card, tìm kiếm toàn văn đều chạy (thử trên trình duyệt).
- Đã bù `agent-monitor.html` (nay là `tools/viewer/assets/monitor.html`). Số sơ đồ ở nút đầu trang tính thật (trước đây ghi cứng "53").
- **Sửa an ninh trong `scripts/watch-swarm.py`** (lỗi có sẵn trong bản Humana): máy chủ nghe `0.0.0.0` và phục vụ MỌI file dưới gốc dự án (kể cả `.env`, `.git`), không chặn `..`. Nay: mặc định `127.0.0.1` (`--host` để đổi), chỉ phục vụ `/viewer/*` (build/viewer) và `/docs/*` với kiểm tra thoát thư mục và danh sách đuôi file cho phép. Test: `tests/test_viewer.py`.
- Biến `VIEWER_ROOT` / `VIEWER_OUT` cho phép quét dự án khác hoặc ghi ra chỗ khác (dùng để thử; liên kết về docs/ chỉ đúng khi ra `build/viewer`).
- **Chưa làm**: sơ đồ Archify vẫn nhúng ~800 KB engine/CSS/font vào mỗi file HTML (60 sơ đồ ≈ 48 MB ở Humana); tách engine dùng chung là bước sau. Chưa kéo tools/viewer, watch-swarm mới sang Humana.
- Humana vẫn đang chạy bản watch-swarm cũ (lộ mọi file qua mạng LAN khi chạy) cho đến khi kéo bản mới sang.

## Áp dụng bài "Trust Curve / Dune" (2026-10-18)
Đối chiếu bài với agent-base và làm cả 5 mục: (1) luật cứng, (2) cỡ thay đổi, (3) dẫn chứng, (4) Feature Map, (5) Eval cho skill. Không lấy: cấm `useEffect`, cấm comment, automerge, Cloud Agents (xem phân tích trong phiên).
- `agents/protocols/hard-rules.md` (mới): bảng luật cứng/mềm; Reviewer gặp góp ý lặp lần 2 thì lập "Đề xuất luật cứng" trong card; sổ `docs/HARD-RULES.md` (Writer tạo khi cần).
- `agents/protocols/atomic-changes.md` (mới) + `scripts/merge-gate.py`: cảnh báo khi số dòng đổi > ngưỡng (mặc định 600, không tính lockfile/build/card/ghi chú). Đổi ngưỡng: `--max-lines`, `MERGE_GATE_MAX_LINES`, hoặc dòng `| Giới hạn dòng thay đổi | N |` trong `PROJECT.md`; `--strict-size` để chặn. Mặc định chỉ WARN nên không làm vỡ quy trình đang chạy.
- `agents/protocols/definition-of-done.md`: mục "Dẫn chứng bắt buộc khi kết luận". `agents/roles/reviewer.md` thêm checklist 8–10; `agents/roles/dev.md` thêm 2 điều cấm. Có sửa file vai trò theo yêu cầu rõ của người dùng.
- `agents/protocols/feature-map.md` (mới, kèm mẫu), trỏ từ `ui-fidelity.md`. Chưa tạo Feature Map cho dự án nào.
- `agent_core/eval/skill_eval.py`, `scripts/skill-eval.py`, `agents/protocols/skill-eval.md` (mới): rubric, ma trận model, thư mục tạm tên ngẫu nhiên, trọng tài khác họ (từ chối nếu cùng họ), leo núi chỉ giữ bản tốt hơn, không tự ghi đè SKILL.md. **Chưa chạy với model thật**, mới thử bằng runner/judge giả (tests/test_skill_eval.py, 9 test).
- **Sửa lỗi có sẵn**: `merge-gate.py` dùng `ROOT` chưa định nghĩa ở bước cập nhật bảng điều khiển, nên luôn lỗi âm thầm (bị `except` nuốt). Đã định nghĩa `ROOT`, và chỉ cập nhật khi cổng chạy trên chính dự án chứa script (tránh đụng repo khác khi test).
- Sửa `agents/roles/reviewer.md`: chữ `runner` bị hỏng thành xuống dòng + `unner` ở mục Quyền hạn.
- Test: 177 passed trước khi thêm 2 test CLI; test e2e merge-gate thêm 5 ca về cỡ thay đổi.
- **Kiểm lại với CI (2026-10-19), tìm ra 2 chỗ hở và đã sửa:**
  1. CI (`.github/workflows/check.yml`) chạy `python -m unittest discover -s tests`, mà `tests/test_viewer.py` và `tests/test_skill_eval.py` tôi viết kiểu pytest (hàm trần, `tmp_path`, `import pytest`) nên **CI không chạy 12 test này** (167 thay vì 179) và còn có thể lỗi import vì CI chỉ cài `pyyaml`. Đã viết lại bằng `unittest.TestCase` + `tempfile`; nay CI chạy đủ 179. (Đính chính 2026-10-19: ghi chú trước nói `tests/test_debt.py` cũng dùng pytest là SAI; file đó dùng unittest, chỉ có biến tên `tmp_path`. Mọi test hiện đều là unittest.)
  2. `scripts/doctor.py` (bản kéo từ Humana) thoát mã 1 khi không thấy thư mục kiểm dịch `skills.config.json`, mà máy chủ CI không có thư mục đó nên bước "Repository Health Diagnostic" sẽ đỏ. Đã đổi thành cảnh báo khi có biến môi trường `CI`; đã thử: không CI thoát 1, `CI=true` thoát 0.

## Graphify → skill `codebase-map` (2026-10-18)
- Theo quy trình `skills-policy.md`: thêm Graphify vào danh bạ `QUARANTINE_REPOS` của `scripts/fetch-skills.py`, clone nông bằng `--clone-all` vào `D:\skills-quarantine\graphify` (các repo kia đã có nên bị bỏ qua). Chỉ tải về, không cài, không chạy mã.
- Đọc bản tải về: gói `graphifyy` 0.9.92, commit `86c57be8204673c2a1b9849a3292a7dd3ab373d8`, Apache-2.0/MIT. Skill gốc `graphify/skill.md` (44 KB) tự cài gói bằng pip (cả `--break-system-packages`), dùng `python -c` (bị cấm trong agent-base) và ép dùng subagent, nên **không dùng nguyên văn**. Brief: `docs/research/2026-10-18-graphify.md`.
- Thay vào đó viết skill **tự viết** `.agents/skills/codebase-map/SKILL.md`: cấp 0 là `docs/CODEMAP.md` (bản đồ thư mục chuẩn, không cần công cụ), cấp 1 tùy chọn là agent chỉ ĐỌC đồ thị Graphify do người dùng tự cài và build `--code-only`. Cấm agent: `graphify install`, `hook install`, `add <url>`, `--mcp`, `--watch`, `*-push`, build kèm tài liệu/ảnh. Cạnh `INFERRED` phải mở file thật xác nhận.
- Liên quan: sổ skill (`skills.md`), `tech-radar.md` (mức Thử), `onboarding.md` (bước 4 Brownfield), vai analyst/architect/dev (bullet skill; analyst và architect được thêm quyền sửa đúng một file `docs/CODEMAP.md`), `.gitignore` (`graphify-out/`).
- **Chưa kiểm chứng**: chưa cài hay chạy Graphify, chưa thử đồ thị trên dự án thật; con số sao/token là từ README, chưa kiểm độc lập. Cảnh báo cho người dùng: tên gói PyPI có HAI chữ y (`graphifyy`), kiểm nhà phát hành trước khi cài.
- Humana chưa nhận thay đổi này.

## Rà các chỗ còn cũ hoặc lệch và đồng bộ lần cuối (2026-10-19)
- Sửa chỗ cũ: `AGENTS.md` mục 17 ghi "29 Skills" (bỏ con số), `README.md` "29 Skills" (đúng là 31; thêm mục skill `codebase-map`/`feature-map` và mục "Chất lượng: luật cứng, eval, tái hiện lỗi"), `scripts/doctor.py` in `/29 skills` (bỏ con số cứng), `agents/roles/reviewer.md` có mục cho phép `python agent_core/eval/code_reviewer.py*` mà file đó không có lệnh chạy (đổi thành `python scripts/ocr.py*`; đã đọc `ocr.py`, chỉ gọi lệnh git đọc, không ghi file).
- Thêm vào mẫu: `tasks/_template.md` mục 3c "Card sửa lỗi: Phiếu lỗi" (nguyên văn báo lỗi, F-xx, trạng thái tái hiện, nguyên nhân gốc kèm `file:dòng`, đề xuất luật cứng); `.github/pull_request_template.md` 3 ô mới (hard-check, Feature Map, sửa lỗi có tái hiện) và ghi chú WARN cỡ thay đổi.
- Humana: đã kéo `AGENTS.md`, `lead.md`, `reviewer.md`, `handoff-note.md`, `doctor.py`, `tasks/_template.md`; sửa tay `.github/pull_request_template.md` (thêm 3 ô) và `.gitignore` (`graphify-out/`) của Humana; `sync-adapters --check` sạch; mốc đồng bộ 602 file. Backup bản cũ ở `backup-humana4` (scratchpad). Humana và agent-base nay khớp nhau về khung (chỉ `task-card.md` khác có chủ ý).
- `README.md` không thuộc manifest nên không kéo sang Humana (README của Humana là của dự án).

## Luật cứng đầu tiên cho chính agent-base từ lỗi lặp thật (2026-10-19)
Câu hỏi của người dùng: "đã áp dụng cái không lặp lại lỗi chưa". Trước đó mới có giao thức và công cụ, **chưa luật cứng nào được tạo từ một lỗi thật**. Lỗi lặp có thật: viết test kiểu pytest 2 lần trong cùng ngày (CI chỉ chạy unittest nên bỏ qua 12 test). Đã thêm `docs/HARD-RULES.json` (2 luật: cấm `import pytest` và cấm `def test_` cấp module trong `tests/`) và sổ `docs/HARD-RULES.md`. Kiểm: quét cả repo 0 vi phạm; thử trên một file test kiểu pytest giả thì cả 2 luật báo đúng `file:dòng`; CI chạy trên file đổi của PR. Luật "ROOT chưa định nghĩa" (merge-gate) chưa thành luật cứng, ghi trong sổ để thêm nếu lặp lại.

## Làm rõ quy tắc chia Subtask (2026-10-19, người dùng cho phép sửa AGENTS.md rõ ràng)
Câu "chạm 1–3 file hoặc 1 luồng hẹp" dễ bị đọc là điều kiện cứng về số file. Đổi thành: mỗi Subtask một mục đích, độc lập, kiểm tra được, vừa một phiên ngắn (2–5 phút); số file chỉ để ước lượng. Sửa đồng bộ ở `AGENTS.md` mục 16, `agents/roles/lead.md` (nguyên tắc 8), `agents/roles/reviewer.md` (mục H: hơn 3 file vẫn duyệt nếu là một luồng hẹp một mục đích; ít file mà nhiều mục đích thì yêu cầu tách), `agents/protocols/handoff-note.md`. Chạy lại `sync-adapters` (GEMINI.md, CODEX.md, copilot, agents-core). Lưu ý: `agents-core.md` đã sát giới hạn 16.000 ký tự của script (bản đầu của chỉnh sửa này vượt 39 ký tự nên phải rút gọn câu); thêm chữ vào `AGENTS.md` nữa sẽ lại vượt. Chưa kéo sang Humana (Humana vẫn giữ câu cũ).

## Kéo lô còn lại sang Humana (2026-10-19, người dùng: "cái gì áp dụng được thì áp dụng đi")
- Đã kéo 35 file (giao thức bug-repro/hard-rules/atomic-changes/feature-map/skill-eval/DoD/onboarding, skill codebase-map và feature-map, hard-check, feature-map-check, skill-eval, doctor, fetch-skills, các vai trò, examples, sổ skill, tech-radar). Sao lưu bản cũ ở `backup-humana3` (scratchpad, ngoài repo). `task-card.md` cố ý không kéo; `scripts/sync_patch_to_vps.py` là của riêng Humana, bỏ qua.
- Kiểm ở Humana: `sync-adapters --check` sạch, `check-skills` 31 skill 0 lỗi, `doctor.py` PASS, `hard-check` và `feature-map-check` thoát 0 (Humana chưa có `docs/HARD-RULES.json` và Feature Map). Mốc đồng bộ: 602 file khớp.
- Đã thêm 2 bước (hard-check, feature-map-check) vào `.github/workflows/check.yml` của **Humana** (file riêng của dự án, chưa commit).
- **Chưa làm cho Humana** (cần người dùng quyết hoặc thử với ứng dụng thật): luật cứng cô lập tenant (`docs/HARD-RULES.json`; regex không đủ tin cậy để ép "mọi truy vấn lọc theo tenant", nên nên viết test cô lập tenant chạy trong CI thay vì lint chữ), Feature Map cho frontend Next.js (cần chạy ứng dụng để kiểm).
- Không thêm review tự động vào CI: `scripts/ocr.py` là quét tĩnh offline chưa đo độ nhiễu trên mã cũ; cần chạy thử trước. Ghi chú: mục `python agent_core/eval/code_reviewer.py*` trong `reviewer.md` trỏ tới module không có lệnh chạy (CLI thật là `scripts/ocr.py`), chưa sửa vì chưa xác minh `ocr.py` không ghi file.

## Đối chiếu với transcript gốc của bài nói (2026-10-19)
Người dùng dán transcript (bản chép tự động) của video; đã đối chiếu với các tóm tắt NotebookLM trước đó. Chi tiết trong `docs/research/2026-10-19-lauren-tan-talk-anh-xa.md` (mục "Đối chiếu transcript"). Điểm đáng nhớ:
- Đoạn đầu transcript thứ nhất ("best use of AI is pair programming...") là của **người dẫn khác**, không phải Lauren: đừng gán cho Lauren.
- Tóm tắt NotebookLM nhìn chung đúng ý; không phát hiện claim nào của agent-base bị transcript bác bỏ (cỡ PR không trần cứng, không có giới hạn 3 lần review, cấm comment, Benny, Eval đều khớp).
- Bổ sung từ transcript: (1) **cấu trúc quy ước chặt là lớp ràng buộc mạnh nhất** (agent thích sao chép mẫu) → thêm loại luật `path_must_match` vào `scripts/hard-check.py` (ép vị trí file) + ví dụ + 2 test; (2) lý do cấm comment là comment kể chuyện trò chuyện → chỉ lấy phiên bản hẹp `no-conversation-comments` (warn) trong `examples/hard-rules/`, **không** cấm mọi comment; (3) cách thứ ba "loại bỏ vấn đề bằng thiết kế" → `hard-rules.md` mục 2b; (4) Feature Map có **tính năng phụ** → thêm trường tùy chọn `Tính năng phụ` (máy kiểm không đòi); (5) `codebase-map` ghi nguyên tắc colocation.
- Lauren nói Dune **không mã nguồn mở** (chỉ là ý tưởng và nguyên tắc), Pstack công khai nhưng chưa xem mã; ông không khuyên tin mù quáng, khuyên bắt đầu ở local.
- Test: 209 qua theo `unittest discover`.

## Feature Map tạo/duy trì và luật cứng chạy được (2026-10-19)
Đối chiếu bản tóm tắt thứ tư (create/maintain verification skill, Eval, tái hiện lỗi, "giới hạn review 3 lần?"). Bản tóm tắt chính nó nói **không có giới hạn review 3 lần** trong bài; ngưỡng "lần thứ hai thì lập luật cứng" ở `hard-rules.md` là lựa chọn của agent-base, không phải của bài. Chi tiết về Pstack là tóm tắt thứ cấp, chưa xác minh.
- `scripts/hard-check.py` + `docs/HARD-RULES.json` (mẫu `examples/hard-rules/`): luật cứng **khai báo bằng JSON** (`forbid_regex` gồm cấm import chéo ranh giới, `max_file_lines`), báo `file:dòng`, `--changed-against` để PR không đỏ vì code cũ, `hard-ignore: <id> <lý do>` (thiếu lý do vô hiệu). Biến "comment review → luật" thành thao tác một dòng JSON thay vì viết linter. Thoát 0/1/2.
- `scripts/feature-map-check.py`: kiểm Feature Map còn khớp mã (file nguồn tồn tại, `data-testid` còn trong mã, đủ trường bắt buộc, trùng mã F-xx) và cảnh báo file giao diện đổi nhưng không thuộc mục nào. Chỉ đọc. Dự án không có bản đồ thì thoát 0.
- Skill tự viết `feature-map` (`create` rồi kiểm trên ứng dụng thật; `maintain` chỉ sửa mục bị ảnh hưởng); đã vào sổ skill, gắn vào designer/qa/dev; reviewer thêm checklist 11 và được chạy 2 script mới; runner được chạy 2 script mới.
- CI `.github/workflows/check.yml`: thêm 2 bước (chỉ PR): `hard-check --changed-against origin/<nhánh gốc>` và `feature-map-check --changed-against ...`. Dự án chưa có file luật hoặc bản đồ thì cả hai thoát 0, nên không làm đỏ.
- Giao thức cập nhật: `hard-rules.md` (đường khai báo JSON, bỏ qua có lý do), `feature-map.md` (skill + máy kiểm lệch), `skill-eval.md` (làm ở máy nội bộ trước).
- Test: 205 qua theo `unittest discover` (thêm 18). **Chưa thử trên dự án giao diện thật** (Humana) và chưa thử CI thật trên GitHub (chỉ chạy lệnh cục bộ).
- `AGENTS.md` mục 17 và README còn ghi "29 Skills" trong khi thư mục có 31; `AGENTS.md` chỉ người dùng sửa được nên chưa cập nhật.

## Eval cho skill: đối chiếu bài thứ ba và hoàn thiện (2026-10-19)
Đối chiếu 5 bước của Eval Playbook trong bài với bản đã làm, tìm 4 chỗ thiếu/sai và sửa:
- **Rò "đang bị eval"**: thư mục tạm của `scripts/skill-eval.py` đặt tên `skill-eval-xxxx` và file `skill.md`, `prompt.txt` nên agent bị thử nhìn thấy chữ "eval" trong đường dẫn lệnh. Đã đổi sang thư mục ngẫu nhiên + `guide.md`/`ask.txt`, dọn sau khi chạy; test `test_agent_under_test_never_sees_eval_in_paths` giữ điều này.
- **Rubric do agent điều phối soạn**: thêm lệnh `rubric` (`--rubric-cmd`), tên skill lấy theo thư mục, từ chối ngoài 3–8 tiêu chí, ghi rõ là BẢN NHÁP để người duyệt (không tự chấm bằng thước do chính model đặt).
- **Độ ổn định giữa các model**: báo cáo ghi model yếu nhất và chênh lệch giữa model, cảnh báo khi chênh > 1.5.
- **Ví dụ chạy được ngay**: `examples/skill-eval/` (runner/trọng tài/người cải thiện/rubric giả, không tốn token). Chạy README ra 2.67 → 10.0 sau một vòng.
- **Lỗi tìm thấy khi thử**: lệnh runner chạy trong thư mục tạm nên đường dẫn tương đối trong README (`examples/skill-eval/demo_runner.py`) không tìm thấy file; đã đổi đường dẫn tương đối tới file có thật thành tuyệt đối theo thư mục đang đứng. Đường dẫn có dấu cách trong lệnh phải đặt trong nháy kép (đã ghi trong README và giao thức).
- Test: 187 qua theo `unittest discover` như CI (thêm 8 test cho Eval). **Vẫn chưa chạy với model thật** (mới giả lập), chưa có số liệu token/chi phí thật.

## Giao thức tái hiện lỗi `bug-repro` (2026-10-19)
- `agents/protocols/bug-repro.md` (mới): 6 bước: phiếu lỗi (giữ nguyên văn người báo, hỏi lại tối đa một lượt) → định vị bằng Feature Map (hoặc CODEMAP) → **tái hiện trên `main`** ở worktree sạch, dữ liệu giả, ra 1 trong 3 trạng thái kèm dẫn chứng ở `docs/qa/bugs/<Mã>/` → Lead phán quyết (sửa theo test đỏ rồi xanh / đã được sửa bởi commit nào, tái hiện ở phiên bản người báo dùng để biết / không tái hiện thì hỏi thêm rồi đóng "cần thêm thông tin") → QA xác minh đúng kịch bản và là người duy nhất đóng lỗi → ghi học được, lần 2 thì đề xuất luật cứng.
- Gắn vào: `lead.md` (nguyên tắc 9), `qa.md` (đầu ra và điều cấm "không đóng lỗi chỉ vì không thấy"), `dev.md` (không sửa lỗi chưa tái hiện); trỏ từ `feature-map.md` và `definition-of-done.md`.
- Là phiên bản **cục bộ** của việc "Cloud Agent tái hiện lỗi" trong bài; không có agent chạy ngầm trên đám mây. Chưa thử trên một báo lỗi thật. Chưa kéo sang Humana (cùng với codebase-map, doctor, fetch-skills, 2 file test).

## Thay đổi dùng chung cho agent-base
- `scripts/sync-adapters.py`: thêm `build_claude` và đầu ra `.claude/agents/`, thêm thư mục này vào kiểm file cũ. Dùng chung được.
- `agents/manifest.txt`: thêm dòng `generated  .claude/agents/` và `generated  .codex/agents/`. Dùng chung được.
- `tools/viewer/**` (mới), `scripts/generate-dashboard.py` (thành điểm vào mỏng), `scripts/watch-swarm.py` (siết quyền phục vụ file, `--host`), `agents/protocols/task-card.md` (đường dẫn dashboard mới), `agents/manifest.txt` (`copy tools/viewer/`), `tests/test_viewer.py`. Dùng chung được.
- `scripts/sync-adapters.py` (bổ sung): `build_codex`, frontmatter `trigger` cho `.agents/rules/`, tính giới hạn không kể frontmatter. Dùng chung được.
