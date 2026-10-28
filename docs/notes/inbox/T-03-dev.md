> summary: T-03 CI xanh trên clone sạch + nối cổng task/board: cách giữ --strict và miễn trừ có lý do
Task: T-03        Agent: dev        Ngày: 2026-10-24

Skill đã chọn & áp dụng: `systematic-debugging` (truy nguyên nhân CI đỏ trước khi sửa), `cso` (giữ `--strict`, miễn trừ có lý do), `codebase-design` (sửa tại cổng thay vì hạ chuẩn).

Checklist đã tuân thủ:
- Mỗi lỗi CI có lệnh + đầu ra thật trước khi sửa; không đoán.
- Không hạ chuẩn bảo mật: vẫn `--strict`, 4 miễn trừ ghi rõ trust boundary ngay tại dòng.
- Không sửa card lịch sử, không xóa dữ liệu; mọi thay đổi nằm trong `scope_edit`.

## Đã làm
- Thêm `pyproject.toml` (deps/pytest/entry point), guard test cookie (`ImportError`/`ModuleNotFoundError`), directive `# cso: allow` (bắt buộc lý do, chỉ nhận comment thật, in truy vết từng finding), board bỏ qua card lịch sử, CI tìm card đệ quy + cài deps có điều kiện.
- Chạy 8 cổng + unittest/pytest: tất cả exit 0, 216 test pass; CSO in 4 dòng miễn trừ kèm file:dòng:rule.

## Lưu ý cho agent sau
- **Bẫy gitignore**: `.codex/` ignore cả thư mục nên negation `!.codex/agents/**` vô hiệu. Đã đổi thành `.codex/*` rồi mở negation. Đừng đổi ngược lại.
- **Bẫy trạng thái git**: `scripts/task-branch.py`, `scripts/deploy.py`, `scripts/task-board.py`, `scripts/hard-check.py`, `scripts/feature-map-check.py` đang untracked (`??`); `check.yml` cũng đang chứa sẵn 2 step Hard rules/Feature Map của khối migration và `.gitignore` có `graphify-out/`. Phải commit khối migration trước (hoặc `git add -p`), nếu không commit T-03 sẽ trộn việc không thuộc task.
- **Cú pháp directive CSO**: chỉ áp dụng cho file `.py`; phải có lý do không rỗng; neo ở dòng call hoặc dòng ngay trên. Với call nhiều dòng, AST báo dòng mở call nên đặt directive ở dòng `shell=True` bên trong sẽ **không** có hiệu lực.
- **Quyết định**: giữ `shell=True` + `# cso: allow INJ-02 <lý do>` thay vì `shlex.split`, vì `pnpm` trên Windows là `.cmd` và lệnh build là hợp đồng từ `PROJECT.md`, không phải input runtime. Directive thiếu lý do **không** có hiệu lực.
- **File dễ vỡ**: `.github/workflows/check.yml` được copy sang dự án khác (`gitonly` trong `manifest.txt`). Mọi lệnh Python-specific phải có điều kiện (cài deps, board check, merge-gate card lookup).
- **Giả định chưa kiểm chứng**: CI trên clone sạch chưa chạy được vì T-03 chưa commit; cần người dùng commit khối 172 thay đổi + adapter rồi xác nhận `git ls-files .claude/agents .codex/agents | wc -l` = 38 (19 vai × 2 adapter, trừ `lead` là primary).

## Việc dở dang hoặc nợ kỹ thuật
- `pytest` còn 1 warning `PytestCollectionWarning` từ `agent_core/eval/runner.py` (không chặn CI).
- `docs/DEBT.md` vẫn còn false positive (ngoài phạm vi T-03).

## Ảnh hưởng đến task khác
- T-01/T-02 không sửa; `task-board.py` bỏ qua card `done`/`cancelled`/`is_example`.
- Task sau muốn thêm cổng CI phải nhớ workflow dùng chung cho mọi stack.

## Đề xuất cập nhật quy ước hoặc tài liệu
- Ghi directive `# cso: allow <RULE-ID> <lý do>` vào `agents/protocols/hard-rules.md` hoặc tài liệu security để agent sau dùng đúng cú pháp.

## Thay đổi dùng chung cho agent-base
- `scripts/task-board.py`, `scripts/cso.py`, `agent_core/eval/cso_scanner.py`, `scripts/task-branch.py`, `scripts/deploy.py`: dùng chung được, nằm trong `copy scripts/` và `copy agent_core/` của manifest.
- `.github/workflows/check.yml`, `.gitignore`: `gitonly`; đã giữ tương thích dự án không có `pyproject.toml`.
- `pyproject.toml`: **không** thêm vào manifest vì là packaging riêng của repo agent-base; dự án tự có manifest riêng.
