# Kế hoạch commit (AI viết; người dùng chạy hoặc nhờ AI chạy)

AI viết kế hoạch này vào mục "Kế hoạch commit" của task card. Sau đó có hai đường:

- **Người dùng tự chạy** từng lệnh (như trước).
- **Người dùng nhờ AI chạy** ("commit hộ tôi"): AI chạy đúng các lệnh `git add <đường dẫn>`, `git commit`, `git push` trong kế hoạch. Công cụ hỏi người dùng duyệt **từng lệnh**; commit dùng danh tính git của người dùng. Việc thêm dòng trailer `Co-Authored-By:` được quyết định theo cấu hình mục **Attribution commit** trong `PROJECT.md` (mặc định là `co-authored-by`; nếu dự án đặt `none` thì không thêm trailer này).

AI **không bao giờ** chạy `git add -A`/`.`/`-f`, `commit --amend`, `--no-verify`, push ép hoặc push vào `main`/`develop`/`release/*`, `rebase`, `reset`, `merge`, `tag` (những việc này người dùng làm). Quy tắc gốc: `agents/protocols/git-rules.md`.

### Khi được nhờ chạy: các bước

1. `git status` và `git diff --stat` (chỉ đọc); xác nhận đang ở nhánh cá nhân đúng tên (`<type>/<ticket>-<mô-tả>`), không phải `main`/`develop`/`release/*`.
2. Với mỗi commit: `git add` **từng đường dẫn** (không dùng `-A`, `.`), rồi `git diff --cached --stat` để người dùng thấy đúng file sắp vào commit; có file lạ, file bí mật hoặc file quá lớn thì dừng và báo.
3. `git commit -m "<type>(scope): <tóm tắt>"` (nếu `PROJECT.md` cấu hình attribution là `co-authored-by`, thêm `-m "Co-Authored-By: Claude <noreply@anthropic.com>"`; nếu là `none` thì bỏ qua). Hook sẽ chặn tiêu đề sai dạng hoặc dòng giống bí mật: sửa nội dung rồi commit lại, **không** dùng `--no-verify`.
4. Chỉ `git push -u origin <nhánh-cá-nhân>` nếu người dùng nói rõ là cần đẩy. Bị hook hoặc công cụ chặn thì báo người dùng, không tìm cách né.

## Cách AI lập kế hoạch

1. Chạy `git status` và `git diff --stat` (chỉ đọc) để biết chính xác file nào đã đổi.
2. Nhóm file theo **mục đích**, mỗi nhóm là **một commit = một thay đổi logic**. Thứ tự nên theo:
   `chore` / `build` (cấu hình, phụ thuộc) → `refactor` → `feat` hoặc `fix` → `test` → `docs` → `ci`.
   Đổi tên và format tách riêng, đặt trước phần thay đổi logic.
3. Mỗi commit liệt kê **đường dẫn cụ thể** cho `git add`. Cấm `git add -A` và `git add .`.
4. File có nhiều mục đích lẫn nhau: dùng `git add -p <file>` và ghi rõ hunk nào thuộc commit nào. Không gom cả file vào một commit sai mục đích.
5. Đặt tiêu đề đúng dạng `<type>(scope): <tóm tắt>` (loại: feat fix chore refactor docs test ci build perf; tối đa 72 ký tự).
6. Không đưa vào file không được commit: khóa bí mật, `.env*`, file lớn, file sinh ra không thuộc quy ước. Thấy thì cảnh báo người dùng.
7. Với file sinh tự động (ví dụ `.kilo/agents/`, `GEMINI.md`) đặt chung commit với nguồn của chúng hoặc ngay sau, và ghi rõ đã chạy `scripts/sync-adapters.ps1`.
8. Kết thúc bằng bước kiểm tra chỉ đọc và các lệnh đẩy.

## Mẫu (dán vào task card)

````markdown
## Kế hoạch commit (người dùng chạy)

Nhánh: feature/12-token-check    Gốc: develop

### 0. Chuẩn bị
```
git switch develop
git pull --ff-only
git switch -c feature/12-token-check
```
(Nếu nhánh đã tồn tại: `git switch feature/12-token-check`, rồi `git rebase develop`.)

### 1. Commit theo chức năng
Commit 1 — refactor: tách hàm kiểm tra token khỏi controller
```
git add src/auth/token.ts src/auth/index.ts
git commit -m "refactor(auth): tách hàm kiểm tra token"
```
Commit 2 — feat: thêm kiểm tra token hết hạn
```
git add src/auth/validate.ts
git commit -m "feat(auth): thêm kiểm tra token hết hạn"
```
Commit 3 — test
```
git add tests/auth/validate.test.ts
git commit -m "test(auth): thêm test token hết hạn"
```

### 2. Kiểm tra trước khi đẩy (chỉ đọc)
```
git status
git log --oneline develop..HEAD
git diff --stat develop...HEAD
powershell -File scripts/merge-gate.ps1 -Branch feature/12-token-check -Card tasks/T-12.md -Base develop
```

### 3. Rebase và đẩy
```
git fetch origin
git rebase origin/develop
git push -u origin feature/12-token-check
```
Nếu đã đẩy trước đó rồi mới rebase lại: `git push --force-with-lease` (không dùng `--force`).

### 4. Merge Request vào develop
- Tiêu đề: `feat(auth): thêm kiểm tra token hết hạn`
- Link ticket: (điền)
- Tóm tắt thay đổi: (điền)
- Bằng chứng kiểm thử: (link test case hoặc kết quả `npm test`)

### 5. Sau khi merge
- Ghi mã merge commit vào card: (điền)
- File ghi chú đã được Tech Writer gộp, xóa: `git rm docs/notes/inbox/T-12-dev-a.md`
````

## Việc người dùng nên tự kiểm tra

- Mỗi commit đọc lên chỉ nói về **một** việc? Nếu phải dùng chữ "và" trong tiêu đề, tách ra.
- Chạy `git diff --cached` trước mỗi lần `git commit` để chắc không lẫn file lạ.
- Hook `commit-msg` sẽ chặn tiêu đề sai dạng. Hook `pre-commit` chặn commit trên `main`/`develop`/`release/*`.
