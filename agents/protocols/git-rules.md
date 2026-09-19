# Quy tắc Git

Áp dụng cho mọi agent và cho cả người dùng, trừ chỗ ghi rõ "chỉ agent". Được ép bằng hook trong `.githooks/` (cài bằng `scripts/install-hooks.ps1`), bằng `scripts/merge-gate.ps1`, và ở phía GitHub bằng CI cùng bảo vệ nhánh (mục 7).

## 1. Nhánh

| Nhánh | Dùng cho | Ai được commit và push |
|---|---|---|
| `main` | bản đã duyệt | **chỉ người dùng** |
| `integration` | (tùy chọn) gộp các task của một việc lớn để chạy test | **chỉ người dùng** |
| `feat/T-xxx`, `fix/T-xxx`, `chore/T-xxx`, `docs/T-xxx` | một task, một nhánh, một worktree | agent của task đó |

Không có nhánh sống lâu ngoài `main` và `integration`. Nhánh task xóa sau khi merge.

## 2. Commit

Tiêu đề: `type(scope): nội dung`, tối đa 72 ký tự. Loại hợp lệ: `feat fix docs test refactor chore ci perf build style`.

**Chỉ agent** phải có đủ hai dòng ở cuối:

```
feat(auth): thêm kiểm tra token hết hạn

Task: T-012
Agent: dev-a
```

- Mỗi commit một ý, đủ nhỏ để `git revert` riêng.
- Dùng tên tác giả `dev-a (agent)` (script `new-worktree.ps1` cài sẵn). Hook nhận ra agent qua hậu tố `(agent)`.
- Người dùng: sai định dạng chỉ bị cảnh báo.

## 3. Merge và tag

- Nhánh task gộp vào `integration` (hoặc thẳng `main` với việc nhỏ) bằng **squash**: một task, một commit.
- Sau khi merge, gắn tag `T-xxx` trên commit đó. Nhờ vậy "quay lại T-012" là một lệnh `git revert`.
- Người dùng là người merge vào `main`. Không agent nào tự merge.
- Trước khi merge chạy `scripts/merge-gate.ps1`. Ghi chú `docs/notes/inbox/` của task đi cùng nhánh, và Tech Writer gộp vào sổ tay sau merge.

## 4. Cấm

- Agent commit hoặc push vào `main`, `master`, `integration`.
- `git push --force` (kể cả `--force-with-lease`) lên nhánh được bảo vệ. Người dùng có thể ghi đè có chủ đích bằng `ALLOW_FORCE_PUSH=1`.
- Xóa nhánh được bảo vệ.
- `git reset --hard`, `git rebase` hay viết lại lịch sử trên nhánh đã push hoặc dùng chung.
- `--no-verify` (bỏ qua hook): agent không được dùng.
- Commit khóa bí mật, file `.env*`, `*.pem`, `*.key`, file lớn hơn 5 MB, thư mục phụ thuộc (`node_modules`, `.venv`...).
- Sửa migration hay tag đã công bố. Cần sửa thì tạo mới.

## 5. Hook làm gì

| Hook | Chặn khi |
|---|---|
| `pre-commit` | agent commit trên `main`/`master`/`integration`; có file `.env*`, `.pem`, `.key`; file > 5 MB; dòng thêm vào trông như khóa hoặc mật khẩu; đã đổi vai trò hoặc `AGENTS.md` mà file sinh ra chưa khớp |
| `commit-msg` | agent: tiêu đề sai định dạng, dài quá 72, thiếu `Task:` hoặc `Agent:` |
| `pre-push` | agent push lên nhánh được bảo vệ; ai đó xóa hoặc push ghi đè (không phải fast-forward) lên nhánh được bảo vệ |

## 6. Giới hạn của hook (đọc kỹ)

- Hook chỉ nhận ra agent **có tên tác giả `(agent)`**. Agent làm việc trong thư mục chính bằng tên của người dùng sẽ không bị coi là agent. Vì vậy mỗi agent nên chạy trong worktree riêng.
- Hook nằm trên máy, bỏ qua được bằng `--no-verify` và không có tác dụng nếu chưa chạy `install-hooks.ps1`. Chốt chặn thật sự là bước 7 và `merge-gate`.
- Quét khóa bí mật bằng mẫu chữ có thể báo nhầm hoặc bỏ sót. Nó không thay được việc xem diff.

## 7. Bảo vệ ở phía GitHub (người dùng cài, một lần)

Tôi không cài được phần này vì cần quyền quản trị trên GitHub. Trong repo trên GitHub: **Settings → Branches → Add branch ruleset (hoặc branch protection rule)** cho `main` (và `integration` nếu dùng), bật:

1. Require a pull request before merging (kèm yêu cầu tối thiểu 1 lượt duyệt).
2. Require status checks to pass: chọn kiểm tra `agent-base` từ workflow `.github/workflows/check.yml`.
3. Block force pushes.
4. Restrict deletions.
5. (Tùy chọn) Require review from Code Owners: `.github/CODEOWNERS` đã có.

Lưu ý: tính năng này với repo **riêng tư** có thể cần gói GitHub trả phí (chưa xác minh với tài khoản của bạn).

## 8. Hoàn tác

Xem `AGENTS.md` mục "Hoàn tác": `git revert` commit của task, trên nhánh mới, chạy test, người dùng duyệt.
