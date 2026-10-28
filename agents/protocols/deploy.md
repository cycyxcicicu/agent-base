# Deploy: commit và đẩy code để hệ thống tự build

Người dùng báo **"deploy"** (hoặc "đẩy lên", "build lại") thì agent chạy **một lệnh duy nhất**:

```
python scripts/deploy.py -m "<type>(scope): <tóm tắt>"
```

Ví dụ: `python scripts/deploy.py -m "feat(frontend): thêm trang chi tiết ứng viên"`.

## Quy tắc

1. **Chỉ dùng script này** để commit và đẩy. Không tự chạy `git add`, `git commit`, `git push`, không đụng `git config`. Script đã làm đủ, và tự kiểm tra an toàn (nhánh, thư mục cho phép, khóa bí mật, build, dạng commit).
2. Cấu hình ở `.deploy.json` (gốc dự án, **không commit**): nhánh, thư mục được đẩy (`paths`), các remote, danh tính tác giả commit, lệnh build. Agent **không sửa** file này. Muốn đổi, báo người dùng.
3. Trước khi gọi, chạy test và lint theo `PROJECT.md` (hoặc nhờ `runner`). Chỉ deploy khi đã xong việc của card và test qua.
4. Thông điệp commit đúng dạng `<type>(scope): <tóm tắt>` tối đa 72 ký tự, `type` thuộc: feat, fix, chore, docs, refactor, test, style, perf, build, ci, revert. Thêm `--co-author "Tên <email>"` nếu muốn ghi công agent.
5. **Script dừng thì báo người dùng, không tìm cách né.** Cấm: `--force`, sửa `.deploy.json`, tự `git add` file ngoài `paths`, chạy lại với `--skip-build` để lách lỗi build. Lỗi build thì sửa lỗi rồi deploy lại.
6. Muốn xem trước không ghi git: thêm `--dry-run`.
7. Chỉ build lại không có thay đổi mới: `python scripts/deploy.py -m "chore: trigger build" --allow-empty`.

## Sau khi deploy

- Script đẩy lên mọi remote trong `.deploy.json`, hệ thống build (vd Vercel) tự chạy. Script **không** chờ kết quả build.
- Kiểm tra kết quả: dùng connector Vercel nếu có (`list_deployments`), hoặc hỏi người dùng. Build lỗi thì ghi vào card và báo người dùng kèm dòng lỗi cuối.
- Ghi vào task card mục "Nhật ký phiên": mã commit và remote đã đẩy.

## Phạm vi của ngoại lệ này

Người dùng cho phép ngoại lệ này chỉ cho việc commit và đẩy **qua script**, theo đúng `.deploy.json`. Mọi việc ghi git khác vẫn theo `AGENTS.md` mục 4 (hỏi duyệt từng lệnh, cấm `push --force`, `rebase`, `reset`, `merge`...).
