# Vòng đời worktree: tạo, làm, đưa về nhánh hiện tại, dọn

Worktree là một **thư mục làm việc thứ hai** của cùng một repo, mỗi cái đang đứng trên **một nhánh riêng** và dùng chung `.git`. Dùng để nhiều agent làm song song mà không đè file của nhau. Quy tắc chung: `agents/protocols/git-rules.md`.

```
tra cứu sổ bộ → tạo worktree ngoài repo → đăng ký registry → AI sửa file & test → commit plan → đẩy & Merge Request → merge → dọn worktree
```

## 0. Quy tắc cốt lõi bắt buộc (100%)
1. **Vị trí duy nhất**: Mọi Git Worktree **PHẢI** nằm tại thư mục worktree tập trung ngoài workspace (ví dụ: `$WORKTREES_DIR/<service>-<slug>` hoặc `../worktrees/<service>-<slug>`). Tuyệt đối **KHÔNG** tạo worktree bên trong workspace hoặc bên trong thư mục con của service.
2. **Sổ bộ đăng ký (Worktree Registry)**: Mọi worktree khi tạo hoặc xóa bắt buộc phải được khai báo vào sổ bộ đăng ký (`worktree-registry.json` hoặc tài liệu registry của dự án) qua công cụ `python3 scripts/worktree-manager.py add|remove|sync`.
3. **Tra cứu trước khi làm**: Trước khi code, Dev/QA BẮT BUỘC chạy `python3 scripts/worktree-manager.py list` để chọn đúng worktree hiện có phục vụ task, tránh tạo trùng lặp.

## 1. Tạo và đăng ký (người dùng hoặc AI)

Sử dụng công cụ quản lý worktree chuẩn:
```bash
# Xem danh sách các worktree hiện có và mục đích sử dụng
python3 scripts/worktree-manager.py list

# Tạo worktree mới ra thư mục ngoài và tự động đăng ký vào sổ bộ
python3 scripts/worktree-manager.py add --service <tên-service> --name <service>-<task>-dev --branch feature/<task>-<slug> --task <TASK-ID> --purpose "<Mô tả tính năng>"
```

- Nhánh `feature/*` tách từ `develop` (`hotfix` tách từ `main`).
- Mỗi task một worktree, mỗi nhánh chỉ mở ở **một** worktree (Git không cho mở cùng một nhánh ở hai nơi).

## 2. AI làm việc

- Mở **thư mục worktree** làm workspace của AI (không mở thư mục chính).
- AI chỉ **sửa file** trong phạm vi task card, chạy test, rồi viết **kế hoạch commit** vào card. AI chỉ commit khi người dùng yêu cầu rõ và duyệt từng lệnh (`AGENTS.md` quy tắc 4).
- Task card và ghi chú `docs/notes/inbox/` của task nằm trong nhánh của worktree và đi cùng nhánh.

## 3. Commit (người dùng hoặc AI khi được duyệt)

Chạy kế hoạch commit **trong thư mục worktree** (`cd` vào đó, hoặc thêm `git -C <đường-dẫn>` trước mỗi lệnh). Các commit nằm trên nhánh của worktree, chưa ảnh hưởng nhánh nào khác.

## 4. Cập nhật và đẩy

Trong worktree:

```bash
git fetch origin
git rebase origin/develop
git push -u origin feature/<ticket>-<slug>
```

Rồi tạo Merge Request vào `develop`.

## 5. Dọn worktree (sau khi Merge Request đã merge)

Sau khi nhánh đã merge thành công, dọn dẹp worktree và tự động cập nhật lại sổ bộ:

```bash
python3 scripts/worktree-manager.py remove --name <tên-worktree>
```

Công cụ sẽ tự động:
1. Dừng tiến trình nếu service trong worktree đang chạy.
2. Thực hiện `git worktree remove`.
3. Cập nhật và làm sạch sổ bộ đăng ký `worktree-registry.json`.
