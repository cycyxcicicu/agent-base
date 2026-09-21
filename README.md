# agent-base

Bộ khung dùng lại cho nhiều dự án: một "phòng ban" agent có vai trò và quy tắc rõ ràng, chạy song song trong các worktree riêng, để lại dấu vết đầy đủ và **ghi chú cho agent sau**. Thiết kế cho Kilo Code chạy trong Antigravity, nhưng nguồn quy tắc là file markdown thuần nên công cụ khác cũng đọc được.

## Có gì trong đây

```
AGENTS.md            quy tắc chung (nguồn duy nhất, chỉ người sửa)
CLAUDE.md            nhập AGENTS.md cho Claude Code
GEMINI.md            SINH RA từ AGENTS.md (cho Gemini)
CODEX.md             SINH RA từ AGENTS.md (cho OpenAI Codex / ChatGPT)
.github/             chứa copilot-instructions.md (SINH RA từ AGENTS.md)
PROJECT.md           phần riêng của từng dự án (điền khi bắt đầu dự án mới)
agents/
  roles/             20 vai trò (nguồn duy nhất), xem bảng bên dưới
  models.txt         ánh xạ tầng model (strong/standard/fast) sang model cụ thể
  protocols/         mẫu task card, tin nhắn, ghi chú bàn giao, brief nghiên cứu,
                     nhập tài liệu, định nghĩa hoàn thành
  stacks/            quy ước theo ngôn ngữ: java, python, node, dotnet (+ _template)
  knowledge/         tech-radar.md dùng chung giữa các dự án
.kilo/agents/        SINH RA cho Kilo Code
.agents/rules/       SINH RA cho Antigravity
infra/               docker-compose.dev.yml mẫu (Postgres, Redis, RabbitMQ)
scripts/             Lõi Python đa nền tảng (.py) kèm wrapper PowerShell (.ps1) và Bash (.sh)
tasks/               task card, quick-log
docs/
  PROJECT-NOTES.md   sổ tay dự án: bộ nhớ chung cho mọi agent (chỉ writer sửa)
  notes/inbox/       ghi chú của từng agent sau mỗi việc, chờ writer gộp
  source/            tài liệu gốc (không sửa)
  converted/         bản chuyển sang md
  requirements/      danh sách yêu cầu R-xxx
  analysis/          báo cáo của analyst
  research/  spec/  adr/  design/  security/  db/  runbooks/
agent_core/          mã nguồn lõi bộ khung (sandbox, eval, cso, ingest)
src/                 code ứng dụng dự án (để trống cho dự án mới)
tests/               bộ kiểm thử tự động
```

## 20 vai trò

| Vai trò | Việc chính | Được sửa |
|---|---|---|
| `orchestrator` | phân cỡ, tách card, HARD-GATE, điều phối subagent, hoàn tác | `tasks/`, `docs/risk/` |
| `product` | Plan CEO Review, phân tích người dùng, phạm vi MVP, viết spec | `docs/product/`, `docs/roadmap/`, `docs/spec/`, `tasks/` |
| `ba` | nhập tài liệu, rút yêu cầu R-xxx, Domain Glossary | `docs/converted/`, `docs/requirements/`, `tasks/` |
| `analyst` | phân tích lại tài liệu, đối chiếu tài liệu với code, Gap Report | `docs/analysis/`, `tasks/` |
| `researcher` | nghiên cứu công nghệ, thử nhanh (spikes), Tech Radar | `docs/research/`, `agents/knowledge/`, `tasks/` |
| `architect` | spec, chia module (Deep Modules), khai báo phạm vi, ADR Nygard | `docs/spec/`, `docs/adr/`, `tasks/` |
| `designer` | luồng người dùng, wireframe, 41 loại sơ đồ SVG (`diagram-design`) | `docs/design/`, `tasks/` |
| `dev` | lập trình Bite-Sized TDD 2-5m, Systematic Debugging, gắn `# debt:` | theo `scope_edit` của card |
| `mobile` | phát triển ứng dụng di động (Flutter/Native), 60/120 FPS, Offline-first | `mobile/`, `apps/mobile/`, `docs/mobile/`, `tasks/` |
| `ai-eng` | Prompt Engineering, RAG pipeline, LLM Red-Teaming, kiểm thử ảo giác | `ai/`, `prompts/`, `docs/ai/`, `tasks/` |
| `data-eng` | luồng dữ liệu (ETL/ELT), Dead-Letter Queue, schema OLAP | `data/`, `etl/`, `docs/data/`, `tasks/` |
| `dba` | Zero-Downtime Migration (Expand-Contract), concurrent index | `db/`, `**/migrations/`, `docs/db/`, `tasks/` |
| `devops` | CI/CD, đóng gói, deploy, runbook, an toàn chuỗi cung ứng | `.github/`, `infra/`, `deploy/`, `Dockerfile*`, `docs/runbooks/` |
| `sre` | Read-Only Forensics, điều tra sự cố (5 Whys), benchmark tải, Post-Mortem | `docs/postmortems/`, `docs/runbooks/`, `tasks/` |
| `security` | kiểm toán CSO 4-Scope Audit, rà lỗ hổng LLM, bộ lọc lệnh `/careful` | `docs/security/`, `tasks/` |
| `reviewer` | đọc diff, duyệt/trả lại theo 5 Rubrics, kiểm tra cờ `# debt:` | chỉ ghi kết quả vào card |
| `qa` | Happy Path trước, 4 kỹ thuật test ISTQB, đóng lỗi độc quyền | `tests/`, `tasks/` |
| `runner` | **chỉ chạy lệnh** (The Iron Law of Verification) và báo kết quả nguyên văn | không sửa được file nào |
| `debt-hunter` | quét comment nợ `# debt:`, duy trì sổ nợ [`docs/DEBT.md`](file:///d:/OneDrive%20-%20concutobu/tiktok/fteck/agent-base/docs/DEBT.md), đề xuất refactor | `docs/DEBT.md`, `tasks/` |
| `writer` | CHANGELOG, Progressive Disclosure, **gộp ghi chú vào sổ tay** | `docs/`, `README.md`, `CHANGELOG.md`, `tasks/` |

Mọi vai đều được ghi ghi chú vào `docs/notes/inbox/`.

**Xem bảng quyền thật của từng vai** (chạy được trên Windows, macOS, Linux):

```
python scripts/show-permissions.py
# Hoặc: powershell -File scripts/show-permissions.ps1  (Windows)
# Hoặc: ./scripts/show-permissions.sh                  (Linux / macOS)
```

Ba lớp quyền, đều khai báo trong phần đầu của file vai trò rồi được `sync-adapters` sinh cho Kilo:

- **`edit_allow` / `edit_deny`**: vai được sửa file nào (mẫu đường dẫn).
- **`bash`**: `none` (không shell), `readonly` (chỉ `git status/diff/log/show`), `full` (mọi lệnh, trừ lệnh phải hỏi và lệnh bị chặn). Mọi vai `full` đều hỏi lại trước `git push`, publish, deploy, và bị chặn `push --force`, `reset --hard`, `rebase`, `--no-verify`, xóa hàng loạt. Vai có thêm `bash_ask` thì hỏi thêm (ví dụ `dba` hỏi trước khi chạy `psql`, `mysql`...).
- **`web`**: `allow` / `ask` / `deny` cho `webfetch`, `websearch`, `codesearch`. Mặc định `deny`; chỉ `researcher` là `allow`, `security` là `ask`.

Vai `readonly` còn có thêm `bash_allow` (lệnh được thêm, ví dụ `runner` được chạy test và lint, `reviewer` được chạy merge-gate) và `bash_deny` (mẫu cấm, ví dụ `--fix`, `--write`). Vai `runner` không có quyền sửa file nào: chỉ chạy lệnh trong danh sách cho phép.

**Model**: mỗi vai có tầng `model_tier` (`strong` / `standard` / `fast`), ánh xạ sang model cụ thể ở `agents/models.txt` (đã cấu hình sẵn tiền tố phân tầng chuẩn Kilo/Anthropic/Gemini và có thể tùy biến). Khi nào dùng tầng nào: `agents/protocols/model-policy.md`.

Chưa giới hạn: vai nào được gọi vai nào (quyền `task`), và MCP (mặc định không cài).

## Ghi chú cho agent sau

Sau khi xử lý xong, mỗi agent viết một file `docs/notes/inbox/<Task>-<agent>.md` (mẫu `agents/protocols/handoff-note.md`): bẫy gặp phải, quyết định và lý do, khu vực dễ vỡ, giả định chưa kiểm chứng, việc dở dang, ảnh hưởng tới task khác. Sau mỗi merge, `writer` gộp chúng vào `docs/PROJECT-NOTES.md`. Agent bắt đầu việc đọc cả hai nơi.

Vì mỗi agent ghi vào một file riêng, các nhánh chạy song song **không xung đột** ở bước này.

## Git: người dùng làm việc ghi, hoặc nhờ AI làm và duyệt từng lệnh

Theo bài giảng GitFlow (chi tiết `agents/protocols/git-rules.md`):

- AI tự chạy được `status`, `diff`, `log`, `show`... Khi bạn nói "commit hộ tôi", AI chạy `git add <đường dẫn>`, `git commit`, `git push` (nhánh cá nhân, không ép) và **công cụ hỏi bạn duyệt từng lệnh**; commit dùng danh tính của bạn kèm `Co-Authored-By: Claude`. `rebase`, `merge`, `tag`, push ép, push vào `main`/`develop`/`release/*`, `add -A`, `commit --amend`, `--no-verify` luôn do **người dùng** chạy. AI viết **kế hoạch commit** (`agents/protocols/commit-plan.md`) vào task card: các lệnh chia commit theo chức năng, kèm rebase và đẩy.
- Nhánh `main`, `develop`, `release/*`, `feature/*`, `fix/*`, `hotfix/*`. Tên nhánh `<type>/<ticket>-<mô-tả>` (ví dụ `feature/12-token-check`). Commit `<type>(scope): <tóm tắt>`, một commit một thay đổi logic.
- Nhánh cá nhân **rebase** trước khi tạo Merge Request, không rebase `develop`/`release`, đẩy lại bằng `--force-with-lease`. Tag `v<MAJOR>.<MINOR>.<PATCH>`.
- Mọi thay đổi vào `main`/`develop`/`release/*` qua Merge Request (CI qua, tiêu đề và mô tả đúng mẫu `.github/pull_request_template.md`).
- **Cổng rủi ro** (`agents/protocols/risk-gate.md`): hoàn tác hoặc bất cứ việc gì có thể làm mất code, dữ liệu, công việc phải có đánh giá, phiếu `docs/risk/RK-<số>.md` và **người dùng chấp thuận rõ ràng** trước khi AI viết lệnh. Commit hoàn tác hoặc xóa từ 10 file trở lên phải có dòng `Risk-Approved: RK-<số>`; hook và CI kiểm.
- **Worktree** (`agents/protocols/worktree-lifecycle.md`): người dùng tạo bằng `scripts/new-worktree.ps1` (`-Root` để đặt ngoài OneDrive); bản cuối là kết quả đã merge vào `develop`, người dùng tự cập nhật nhánh hiện tại.

## Kỹ năng (29 Skills Tích Hợp)

Hệ thống đã tích hợp sẵn 29 kỹ năng chuẩn hóa (đặc tả Markdown quy chuẩn đặt tại `.agents/skills/<tên>/SKILL.md` kèm các script tiện ích an toàn đã kiểm duyệt được đăng ký tại `agents/knowledge/skills.md`):

### 1. Phương pháp luận & Quy trình Cốt lõi
- `subagent-driven-development`: Điều phối subagents độc lập, dọn sạch context window, cơ chế Rulings.
- `systematic-debugging`: 4 pha cô lập nguyên nhân gốc rễ, Condition-Based Waiting (không dùng `sleep()` tĩnh).
- `codebase-design`: Deep Modules, Information Hiding, Seams theo GS. John Ousterhout.
- `diagram-design`: Thư viện 41 mẫu sơ đồ kỹ thuật và UI thuần vector SVG.
- `domain-modeling`: Xây dựng từ điển nghiệp vụ Domain Glossary, phân định ranh giới Context.
- `grilling`: Kỹ thuật phỏng vấn đào sâu ranh giới kỹ thuật theo Cây Quyết Định (Frontier Questioning).
- `writing-for-agents`: Kỹ thuật viết tài liệu Progressive Disclosure, Visual Anchors, Leading Words.
- `ponytail-debt`: Chuẩn hóa cú pháp comment `# debt:` và quy trình thu hoạch nợ tự động vào `docs/DEBT.md`.
- `architecture-decision-records`: Định dạng ghi chép quyết định kiến trúc chuẩn Michael Nygard.
- `to-spec`: Chuyển đổi ý tưởng, thảo luận thành tài liệu đặc tả có cấu trúc (`docs/spec/SPEC-<name>.md`).
- `to-tickets`: Phân rã đặc tả thành các phiếu task card thực thi độc lập (`tasks/T-<number>.md`).

### 2. Kỹ thuật, Kiểm thử & Đánh giá Nâng cao
- `careful`: Cổng kiểm tra trước khi chạy lệnh phá hủy hoặc thao tác diện rộng.
- `browse`: Tự động hóa trình duyệt web headless bằng Playwright.
- `qa-web`: Kiểm thử giao diện web, chụp ảnh đối chiếu, xác nhận trạng thái form và DOM.
- `ship`: Đóng gói và phát hành an toàn với checklist kiểm tra rủi ro.
- `cso`: Đánh giá an toàn tĩnh và kiểm tra rò rỉ mã nguồn theo tiêu chuẩn Chief Security Officer.
- `open-code-review`: Quy trình đọc và phản biện mã nguồn theo rubrics chất lượng đa ngôn ngữ.
- `test-driven-development`: Chu trình TDD Red-Green-Refactor theo phương pháp luận Kent Beck.
- `sparc-methodology`: Khung phát triển 5 pha Specification - Pseudocode - Architecture - Refine - Completion.
- `devex-review`: Đánh giá trải nghiệm nhà phát triển và tính công thái học của API/SDK.
- `ui-ux-pro-max`: Hệ thống quy tắc thiết kế UI/UX, bảng màu, typography và micro-interactions.

Nếu bạn bổ sung skill mới: đặt ở **`.agents/skills/<tên>/SKILL.md`**, chạy `python scripts/check-skills.py`, ghi vào `agents/knowledge/skills.md`, rồi commit qua Merge Request. Hướng dẫn đầy đủ: `agents/protocols/skills-policy.md`.

## Dùng cho dự án mới

1. Copy cả thư mục `agent-base` sang thư mục dự án mới (bỏ `.git`, rồi `git init -b main`). Dự án có `node_modules` hay `.venv` nặng thì đặt **ngoài OneDrive**.
2. **Khởi tạo và nhận diện dự án**:
   - **Cách 1 (Tự động nhận diện code có sẵn)**: Chạy lệnh dưới đây để tự quét stack, CSDL, lệnh test và tự điền `PROJECT.md`:
     ```
     powershell -File scripts/detect-project.ps1 -FillProjectMd
     ```
   - **Cách 2 (Nhờ AI làm theo mô tả ý tưởng)**: Giao việc cho AI theo quy trình `agents/protocols/onboarding.md`. AI sẽ tự bóc tách yêu cầu `R-xxx`, điền `PROJECT.md` và chuẩn bị `infra/docker-compose.dev.yml`.
   - **Cách 3 (Thủ công)**: Tự điền `PROJECT.md` và chọn file stack trong `agents/stacks/` (`java.md`, `python.md`, `node.md`, `dotnet.md`).
3. Nếu sửa vai trò hoặc `AGENTS.md`, chạy lại:
   ```
   powershell -File scripts/sync-adapters.ps1
   ```
5. Bật hook quy tắc Git (một lần cho mỗi bản clone):
   ```
   powershell -File scripts/install-hooks.ps1
   ```
   Quy tắc nhánh, commit và bảo vệ nhánh nằm ở `agents/protocols/git-rules.md`. Bảo vệ nhánh phía GitHub bạn cài tay một lần (Settings → Branches).
6. **Mở đúng thư mục chứa `.kilo/`** làm workspace trong Antigravity (Kilo chỉ tìm vai trò ở workspace, không tìm ở thư mục cha), cài extension Kilo Code, giao việc cho `orchestrator`.

Kiểm tra file sinh ra còn khớp nguồn không (dùng được trong CI hoặc trước khi commit):

```
powershell -File scripts/sync-adapters.ps1 -Check
```

## Chạy song song

```
powershell -File scripts/new-worktree.ps1 -Ticket 12 -Slug token-check
powershell -File scripts/merge-gate.ps1 -Branch feature/12-token-check -Card tasks/T-12.md -Base develop
```

- **Người dùng chạy** `new-worktree`: tạo `../<tên-repo>-worktrees/T-12` và nhánh `feature/12-token-check` từ `develop` (`hotfix` tách từ `main`). AI không chạy được script này và không commit: AI chỉ sửa file rồi viết kế hoạch commit vào card.
- `merge-gate` từ chối nếu có file thay đổi ngoài `scope_edit` (hoặc trong `scope_deny`) của card. Card và ghi chú `docs/notes/inbox/<Task>-*.md` luôn được phép.
- Kilo Agent Manager cũng tự tạo worktree cho từng phiên. Script chỉ cần khi làm ngoài nó.
- Bắt đầu với 2 Dev song song. Chỉ giao song song các task không chung file.

## Đã kiểm chứng và chưa kiểm chứng

**Đã kiểm chứng** (bằng `kilo agent list` của Kilo 7.7.5 cài trong Antigravity, ngày 2026-09-19):
- Kilo đọc đủ các vai trò từ `.kilo/agents/*.md` khi workspace là thư mục chứa `.kilo/`, và hiểu đúng phần `permission` (mẫu đường dẫn cho `edit`, mẫu lệnh cho `bash`, quy tắc khớp cuối cùng thắng).
- Ba script chạy đúng trên Windows PowerShell 5.1.
- Hook Git (`.githooks/`) đã thử 23 tình huống trong một repo tạm riêng: chặn commit trên `main`/`develop`/`release/*`, tên nhánh sai, tiêu đề commit sai dạng hoặc quá 72 ký tự, danh tính `(agent)`, `.env` và dòng giống mật khẩu; chặn push thẳng, push ghi đè và xóa nhánh dùng chung; cảnh báo nhánh chưa rebase lên `develop`; cho qua commit đúng và push tag.
- Quyền git của AI: vai `full` được hỏi duyệt cho `add <đường dẫn>`, `commit`, `push` không ép, các lệnh git ghi khác bị cấm cứng; vai `readonly` không ghi được gì; lệnh đọc luôn dùng được. Đã kiểm bằng cách mô phỏng quy tắc "khớp cuối cùng thắng" trên các file sinh ra (Kilo CLI trên máy đang lỗi tạo thư mục tạm nên không dùng được lần cuối).
- Kilo 7.7.5 có công cụ Swarm Board (`board_post`, `board_read`) trong danh sách quyền của agent.

**Chưa cài và chưa thử**: CI (`.github/workflows/check.yml`) và bảo vệ nhánh phía GitHub. MCP: mặc định không cài, xem `agents/protocols/mcp-policy.md`.

**Chưa kiểm chứng** (cần thử ở giai đoạn 2, trong giao diện thật):
1. Vai trò hiện đúng trong danh sách chọn agent của giao diện Antigravity, và Agent Manager, Swarm Board dùng được.
2. Quyền theo đường dẫn được **ép** khi agent chạy thật, không chỉ được đọc đúng.
3. Antigravity có đọc `GEMINI.md` ở gốc repo không, và chế độ kích hoạt của từng file trong `.agents/rules/` (chọn trong giao diện). Giới hạn mỗi file 12.000 ký tự, script cảnh báo nếu vượt.
4. Antigravity có đọc `AGENTS.md` không (tài liệu tra được không nhắc tới).
5. Kilo Agent Manager (tính năng giao diện của extension) có thể tự chạy git (ví dụ tạo worktree) ngoài quyền shell của agent: cần thử để chắc AI không tự commit qua đường đó.
6. Researcher có công cụ tìm web sẵn hay phải gắn MCP.

Vai có `bash: full` có thể chạy lệnh shell để sửa file ngoài phạm vi `edit` của mình. `scripts/merge-gate.ps1` là chốt chặn cuối cho việc này.

## Nguyên tắc

- Một nguồn sự thật: sửa vai trò trong `agents/roles/`, rồi sinh lại.
- Bằng chứng và trí nhớ nằm trong repo (git, task card, sổ tay dự án), không dựa vào lịch sử chat của công cụ.
- Người dùng là người duyệt cuối. Không agent nào tự merge vào `main`.
- Việc nhỏ đi đường nhanh, việc lớn đi đủ quy trình.
- Chưa chắc thì ghi "chưa xác minh", không đoán.
