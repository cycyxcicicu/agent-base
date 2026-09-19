# agent-base

Bộ khung dùng lại cho nhiều dự án: một "phòng ban" agent có vai trò và quy tắc rõ ràng, chạy song song trong các worktree riêng, để lại dấu vết đầy đủ và **ghi chú cho agent sau**. Thiết kế cho Kilo Code chạy trong Antigravity, nhưng nguồn quy tắc là file markdown thuần nên công cụ khác cũng đọc được.

## Có gì trong đây

```
AGENTS.md            quy tắc chung (nguồn duy nhất, chỉ người sửa)
CLAUDE.md            nhập AGENTS.md cho Claude Code
GEMINI.md            SINH RA từ AGENTS.md
PROJECT.md           phần riêng của từng dự án (điền khi bắt đầu dự án mới)
agents/
  roles/             13 vai trò (nguồn duy nhất), xem bảng bên dưới
  protocols/         mẫu task card, tin nhắn, ghi chú bàn giao, brief nghiên cứu,
                     nhập tài liệu, định nghĩa hoàn thành
  stacks/            quy ước theo ngôn ngữ: python, node, dotnet (+ _template)
  knowledge/         tech-radar.md dùng chung giữa các dự án
.kilo/agents/        SINH RA cho Kilo Code
.agents/rules/       SINH RA cho Antigravity
scripts/             sync-adapters, merge-gate, new-worktree (PowerShell)
tasks/               task card, quick-log
docs/
  PROJECT-NOTES.md   sổ tay dự án: bộ nhớ chung cho mọi agent (chỉ writer sửa)
  notes/inbox/       ghi chú của từng agent sau mỗi việc, chờ writer gộp
  source/            tài liệu gốc (không sửa)
  converted/         bản chuyển sang md
  requirements/      danh sách yêu cầu R-xxx
  analysis/          báo cáo của analyst
  research/  spec/  adr/  design/  security/  db/  runbooks/
src/  tests/         code của dự án
```

## 13 vai trò

| Vai trò | Việc chính | Được sửa |
|---|---|---|
| `orchestrator` | phân cỡ, tách card, giao việc, hoàn tác | `tasks/` |
| `ba` | nhập tài liệu, rút yêu cầu R-xxx | `docs/converted`, `docs/requirements` |
| `analyst` | **phân tích lại tài liệu**, đối chiếu tài liệu với code, báo cáo lệch | `docs/analysis` |
| `researcher` | nghiên cứu công nghệ, thử nhanh | `docs/research`, `agents/knowledge` |
| `architect` | spec, chia module, khai báo phạm vi, ADR | `docs/spec`, `docs/adr`, `tasks` |
| `designer` | luồng người dùng, wireframe, nội dung chữ | `docs/design` |
| `dev` | cài đặt một task | theo `scope_edit` của card |
| `dba` | migration, lược đồ, kịch bản hoàn tác dữ liệu | `db/`, `**/migrations/`, `docs/db` |
| `devops` | CI/CD, đóng gói, deploy, runbook | `.github/`, `infra/`, `deploy/`, `Dockerfile*`, `docs/runbooks` |
| `security` | rà lỗ hổng, khóa bí mật, gói phụ thuộc | `docs/security` |
| `reviewer` | đọc diff, duyệt hoặc trả lại | chỉ ghi kết quả vào card |
| `qa` | viết và chạy test | `tests/` |
| `writer` | CHANGELOG, tài liệu, **gộp ghi chú vào sổ tay** | `docs/`, `README`, `CHANGELOG` |

Mọi vai đều được ghi ghi chú vào `docs/notes/inbox/`.

**Xem bảng quyền thật của từng vai** (đọc thẳng từ `agents/roles/*.md`):

```
powershell -File scripts/show-permissions.ps1
```

Ba lớp quyền, đều khai báo trong phần đầu của file vai trò rồi được `sync-adapters` sinh cho Kilo:

- **`edit_allow` / `edit_deny`**: vai được sửa file nào (mẫu đường dẫn).
- **`bash`**: `none` (không shell), `readonly` (chỉ `git status/diff/log/show`), `full` (mọi lệnh, trừ lệnh phải hỏi và lệnh bị chặn). Mọi vai `full` đều hỏi lại trước `git push`, publish, deploy, và bị chặn `push --force`, `reset --hard`, `rebase`, `--no-verify`, xóa hàng loạt. Vai có thêm `bash_ask` thì hỏi thêm (ví dụ `dba` hỏi trước khi chạy `psql`, `mysql`...).
- **`web`**: `allow` / `ask` / `deny` cho `webfetch`, `websearch`, `codesearch`. Mặc định `deny`; chỉ `researcher` là `allow`, `security` là `ask`.

Chưa giới hạn: vai nào được gọi vai nào (quyền `task`), và MCP (mặc định không cài).

## Ghi chú cho agent sau

Sau khi xử lý xong, mỗi agent viết một file `docs/notes/inbox/<Task>-<agent>.md` (mẫu `agents/protocols/handoff-note.md`): bẫy gặp phải, quyết định và lý do, khu vực dễ vỡ, giả định chưa kiểm chứng, việc dở dang, ảnh hưởng tới task khác. Sau mỗi merge, `writer` gộp chúng vào `docs/PROJECT-NOTES.md`. Agent bắt đầu việc đọc cả hai nơi.

Vì mỗi agent ghi vào một file riêng, các nhánh chạy song song **không xung đột** ở bước này.

## Dùng cho dự án mới

1. Copy cả thư mục `agent-base` sang thư mục dự án mới (bỏ `.git`, rồi `git init -b main`). Dự án có `node_modules` hay `.venv` nặng thì đặt **ngoài OneDrive**.
2. Điền `PROJECT.md`.
3. Chọn file trong `agents/stacks/` đúng ngôn ngữ (hoặc sao chép `_template.md` cho stack mới), xóa các file stack không dùng nếu muốn.
4. Nếu sửa vai trò hoặc `AGENTS.md`, chạy lại:
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
powershell -File scripts/new-worktree.ps1 -Task T-012 -Agent dev-a
powershell -File scripts/merge-gate.ps1 -Branch feat/T-012 -Card tasks/T-012.md
```

- `new-worktree` tạo `../<tên-repo>-worktrees/T-012`, nhánh `feat/T-012`, và tên tác giả git riêng cho agent.
- `merge-gate` từ chối nếu có file thay đổi ngoài `scope_edit` (hoặc trong `scope_deny`) của card. Card và ghi chú `docs/notes/inbox/<Task>-*.md` luôn được phép.
- Kilo Agent Manager cũng tự tạo worktree cho từng phiên. Script chỉ cần khi làm ngoài nó.
- Bắt đầu với 2 Dev song song. Chỉ giao song song các task không chung file.

## Đã kiểm chứng và chưa kiểm chứng

**Đã kiểm chứng** (bằng `kilo agent list` của Kilo 7.7.5 cài trong Antigravity, ngày 2026-09-19):
- Kilo đọc đủ các vai trò từ `.kilo/agents/*.md` khi workspace là thư mục chứa `.kilo/`, và hiểu đúng phần `permission` (mẫu đường dẫn cho `edit`, mẫu lệnh cho `bash`, quy tắc khớp cuối cùng thắng).
- Ba script chạy đúng trên Windows PowerShell 5.1.
- Hook Git (`.githooks/`) đã thử 14 tình huống với danh tính agent trong worktree: chặn commit sai định dạng hoặc thiếu `Task:`/`Agent:`, chặn `.env` và dòng giống mật khẩu, chặn agent commit hoặc push vào `main`, chặn push ghi đè và xóa `main`, cho qua commit đúng và push nhánh task.
- Kilo 7.7.5 có công cụ Swarm Board (`board_post`, `board_read`) trong danh sách quyền của agent.

**Chưa cài và chưa thử**: CI (`.github/workflows/check.yml`) và bảo vệ nhánh phía GitHub. MCP: mặc định không cài, xem `agents/protocols/mcp-policy.md`.

**Chưa kiểm chứng** (cần thử ở giai đoạn 2, trong giao diện thật):
1. Vai trò hiện đúng trong danh sách chọn agent của giao diện Antigravity, và Agent Manager, Swarm Board dùng được.
2. Quyền theo đường dẫn được **ép** khi agent chạy thật, không chỉ được đọc đúng.
3. Antigravity có đọc `GEMINI.md` ở gốc repo không, và chế độ kích hoạt của từng file trong `.agents/rules/` (chọn trong giao diện). Giới hạn mỗi file 12.000 ký tự, script cảnh báo nếu vượt.
4. Antigravity có đọc `AGENTS.md` không (tài liệu tra được không nhắc tới).
5. Researcher có công cụ tìm web sẵn hay phải gắn MCP.

Vai có `bash: full` có thể chạy lệnh shell để sửa file ngoài phạm vi `edit` của mình. `scripts/merge-gate.ps1` là chốt chặn cuối cho việc này.

## Nguyên tắc

- Một nguồn sự thật: sửa vai trò trong `agents/roles/`, rồi sinh lại.
- Bằng chứng và trí nhớ nằm trong repo (git, task card, sổ tay dự án), không dựa vào lịch sử chat của công cụ.
- Người dùng là người duyệt cuối. Không agent nào tự merge vào `main`.
- Việc nhỏ đi đường nhanh, việc lớn đi đủ quy trình.
- Chưa chắc thì ghi "chưa xác minh", không đoán.
