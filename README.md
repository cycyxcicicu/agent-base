# agent-base

Bộ khung dùng lại cho nhiều dự án: một "phòng ban" agent có vai trò và quy tắc rõ ràng, chạy song song trong các worktree riêng, để lại dấu vết đầy đủ. Thiết kế cho Kilo Code chạy trong Antigravity, nhưng nguồn quy tắc là file markdown thuần nên công cụ khác cũng đọc được.

## Có gì trong đây

```
AGENTS.md            quy tắc chung (nguồn duy nhất, chỉ người sửa)
CLAUDE.md            nhập AGENTS.md cho Claude Code
GEMINI.md            SINH RA từ AGENTS.md
PROJECT.md           phần riêng của từng dự án (điền khi bắt đầu dự án mới)
agents/
  roles/             8 vai trò (nguồn duy nhất): orchestrator, ba, researcher,
                     architect, dev, reviewer, qa, writer
  protocols/         mẫu task card, tin nhắn, brief nghiên cứu, nhập tài liệu, DoD
  stacks/            quy ước theo ngôn ngữ: python, node, dotnet (+ _template)
  knowledge/         tech-radar.md dùng chung giữa các dự án
.kilo/agents/        SINH RA cho Kilo Code
.agents/rules/       SINH RA cho Antigravity
scripts/             sync-adapters, merge-gate, new-worktree (PowerShell)
tasks/               task card, quick-log
docs/                source (bản gốc), converted, requirements, research, adr, spec
src/  tests/         code của dự án
```

## Dùng cho dự án mới

1. Copy cả thư mục `agent-base` sang thư mục dự án mới (bỏ `.git`, rồi `git init -b main`). Đặt **ngoài OneDrive**.
2. Điền `PROJECT.md`.
3. Chọn file trong `agents/stacks/` đúng ngôn ngữ (hoặc sao chép `_template.md` cho stack mới), xóa các file stack không dùng nếu muốn.
4. Nếu sửa vai trò hoặc `AGENTS.md`, chạy lại:
   ```
   powershell -File scripts/sync-adapters.ps1
   ```
5. Mở thư mục trong Antigravity, cài extension Kilo Code, giao việc cho `orchestrator`.

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
- `merge-gate` từ chối nếu có file thay đổi ngoài `scope_edit` (hoặc trong `scope_deny`) của card.
- Kilo Agent Manager cũng tự tạo worktree cho từng phiên. Script chỉ cần khi làm ngoài nó.
- Bắt đầu với 2 Dev song song. Chỉ giao song song các task không chung file.

## Những điều chưa xác minh (cần thử ở giai đoạn 2)

Đây là bộ khung mới tạo, chưa chạy thử với công cụ thật. Các điểm sau chưa được kiểm chứng:

1. Định dạng phần `permission` trong `.kilo/agents/*.md` (mẫu đường dẫn cho `edit`, mẫu lệnh cho `bash`): script sinh theo tài liệu Kilo, cần kiểm tra Kilo có nhận đúng và ép được không.
2. Kilo Code chạy trong Antigravity: Agent Manager, Swarm Board và quyền theo đường dẫn có hoạt động đủ không.
3. Antigravity có đọc `GEMINI.md` ở gốc repo không, và cần chọn chế độ kích hoạt (luôn bật / thủ công / theo file) cho từng file trong `.agents/rules/` ở giao diện. Giới hạn mỗi file là 12.000 ký tự, script cảnh báo nếu vượt.
4. Antigravity có đọc `AGENTS.md` không (tài liệu tra được không nhắc tới).
5. Researcher có công cụ tìm web sẵn hay phải gắn MCP.
6. Kilo hiển thị được các vai trò tùy chỉnh trong Agent Manager không.

Những chỗ Kilo không ép được thì `scripts/merge-gate.ps1` là chốt chặn cuối.

## Nguyên tắc

- Một nguồn sự thật: sửa vai trò trong `agents/roles/`, rồi sinh lại.
- Bằng chứng nằm trong repo (git + task card), không dựa vào lịch sử chat của công cụ.
- Người dùng là người duyệt cuối. Không agent nào tự merge vào `main`.
- Việc nhỏ đi đường nhanh, việc lớn đi đủ quy trình.
- Chưa chắc thì ghi "chưa xác minh", không đoán.
