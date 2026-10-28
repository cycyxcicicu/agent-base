# Vòng đời worktree: tạo, làm, đưa về nhánh hiện tại, dọn

Worktree là một **thư mục làm việc thứ hai** của cùng một repo, mỗi cái đang đứng trên **một nhánh riêng** và dùng chung `.git`. Dùng để nhiều agent làm song song mà không đè file của nhau. Quy tắc chung: `agents/protocols/git-rules.md`.

```
tạo (bạn hoặc AI) → AI sửa file → commit → rebase → đẩy + Merge Request → merge vào develop → bạn cập nhật nhánh hiện tại → dọn worktree
```

## 1. Tạo (người dùng hoặc AI đều làm được)

```
powershell -File scripts/new-worktree.ps1 -Ticket 12 -Slug token-check
```

- Tạo nhánh `feature/12-token-check` từ `develop` (`hotfix` tách từ `main`).
- **Nơi tạo**: mặc định thư mục cạnh repo, `<tên-repo>-worktrees\T-12`. Đổi nơi bằng `-Root`, ví dụ `-Root D:\worktrees\agent-base`.
- **Đừng đặt trong OneDrive** (repo hiện nằm trong OneDrive nên mặc định sẽ rơi vào OneDrive): mỗi worktree là một bản checkout đầy đủ các file, OneDrive sẽ đồng bộ rất chậm và đôi khi làm lỗi file. Đặt ở ổ khác hoặc thư mục ngoài OneDrive bằng `-Root`.
- Mỗi ticket một worktree, mỗi nhánh chỉ mở ở **một** worktree (Git không cho mở cùng một nhánh ở hai nơi).

## 2. AI làm việc

- Mở **thư mục worktree** làm workspace của AI (không mở thư mục chính).
- AI chỉ **sửa file** trong phạm vi task card, chạy test, rồi viết **kế hoạch commit** vào card. AI chỉ commit khi người dùng yêu cầu rõ và duyệt từng lệnh (`AGENTS.md` quy tắc 4); AI không tạo hay xóa worktree.
- Task card và ghi chú `docs/notes/inbox/` của task nằm trong nhánh của worktree và đi cùng nhánh.

## 3. Commit (người dùng)

Chạy kế hoạch commit **trong thư mục worktree** (`cd` vào đó, hoặc thêm `git -C <đường-dẫn>` trước mỗi lệnh). Các commit nằm trên nhánh của worktree, chưa ảnh hưởng nhánh nào khác.

## 4. Cập nhật và đẩy

Trong worktree:

```
git fetch origin
git rebase origin/develop
git push -u origin feature/12-token-check
```

Rồi tạo Merge Request vào `develop`. Trước đó chạy `scripts/merge-gate.ps1` (mặc định so với `develop`).

## 5. Đưa bản cuối về nhánh hiện tại của bạn

**Bản cuối là kết quả đã merge vào `develop`.** Không có gì tự đẩy về nhánh bạn đang đứng, đó là bước của bạn:

| Nhánh hiện tại của bạn | Cách nhận bản cuối |
|---|---|
| `develop` (thư mục chính) | Sau khi Merge Request được merge: `git switch develop`, rồi `git pull --ff-only` |
| Một nhánh cá nhân khác (ví dụ feature khác đang làm) | `git fetch origin`, rồi `git rebase origin/develop` để nhận thay đổi mới |
| Muốn nhận **thẳng** vào nhánh hiện tại, không chờ Merge Request | Chỉ được khi nhánh hiện tại là **nhánh cá nhân** (không phải `main`, `develop`, `release/*`). Rebase nhánh task lên nhánh hiện tại, rồi ở nhánh hiện tại chạy `git merge --ff-only feature/12-token-check` |
| `main`, `develop`, `release/*` | **Không** nhận thẳng. Bắt buộc qua Merge Request |

## 6. Nhiều worktree chạy song song

- Gộp **từng nhánh một**, không gộp cùng lúc.
- Sau mỗi lần merge: nhánh kế tiếp `git rebase origin/develop` để nhận thay đổi vừa merge, nhờ `runner` chạy test, rồi mới tạo Merge Request. Xung đột do bạn xử lý (AI không rebase).
- Các task song song không được sửa cùng file (`scope_edit` không chồng nhau, xem `agents/protocols/task-card.md`), nên xung đột thường ít.

## 7. Dọn worktree (sau khi Merge Request đã merge)

Từ thư mục chính:

```
git -C <đường-dẫn-worktree> status --short
git worktree remove <đường-dẫn-worktree>
git branch -d feature/12-token-check
git push origin --delete feature/12-token-check
```

- Lệnh đầu phải **không in gì** (sạch). Có thay đổi chưa commit thì chúng **sẽ mất** khi xóa worktree: xử lý trước, hoặc coi là việc rủi ro (`agents/protocols/risk-gate.md`).
- `git branch -d` (chữ `d` thường) chỉ xóa khi nhánh đã merge, nên an toàn. Đừng dùng `-D` khi chưa chắc.
- Xóa nhánh trên GitHub cũng làm được bằng nút trên trang Merge Request.
- Đừng xóa thư mục worktree bằng tay. Lỡ xóa thì chạy `git worktree prune`.

## 8. Lưu ý

- Hook trong `.githooks/` dùng chung qua cấu hình của repo, nhưng file hook lấy từ nhánh của mỗi worktree.
- Windows: đường dẫn dài và khoảng trắng trong đường dẫn dễ gây lỗi, dùng dấu nháy khi gõ lệnh và đặt worktree ở đường dẫn ngắn.
