# Nhánh theo card: agent tự tạo nhánh và tự gộp về main khi đạt

Người dùng cho phép (2026-09-30) với điều kiện: **không bao giờ đẩy lên remote**. Đây là ngoại lệ của `AGENTS.md` mục 4, **chỉ qua `scripts/task-branch.py`**. Mọi việc ghi git khác vẫn theo `AGENTS.md`.

## Vòng đời một card code

1. **Bắt đầu** (Dev, hoặc Lead giao): `python scripts/task-branch.py start --ticket <n> --slug <mô-tả> [--type feat]`. Tạo nhánh `<type>/<n>-<mô-tả>` từ `main` ngay trong thư mục hiện tại. Mỗi card đúng một nhánh; chỉ làm một card tại một thời điểm.
2. **Làm**: Dev sửa trong nhánh đó, đặt card `review` khi xong (không tự `done`).
3. **Kiểm** (QA/Reviewer): đứng trên nhánh, kiểm theo `agents/protocols/ui-fidelity.md` (card giao diện: ảnh chụp 375/768/1440px, `docs/qa/<Task>-visual.md` có dòng `KẾT QUẢ: ĐẠT`). Đạt thì đặt card `done`; không đạt trả `doing`.
4. **Gộp** (QA, Reviewer hoặc Lead, không phải Dev): `python scripts/task-branch.py finish --ticket <n> -m "<type>(scope): <tóm tắt>"`. Script chỉ gộp khi: đang đứng đúng nhánh card; `card-audit --need-done` đạt; không có file staged ngoài `paths`; không nghi bí mật; build (và test nếu khai trong `.deploy.json`) qua. Sau đó commit trên nhánh rồi `merge --no-ff` vào `main`. Merge lỗi thì tự hủy và quay lại nhánh card.
5. **Đẩy lên remote**: chỉ khi người dùng báo "deploy", bằng `scripts/deploy.py` (`agents/protocols/deploy.md`). Script nhánh card **không có lệnh push**.

## Cấm

- Không dùng `git switch`, `checkout`, `merge` trực tiếp; không `--force`, `reset`.
- Không gộp card chưa `done`; không sửa `card-audit.py` hay `task-branch.py` để gộp cho được.
- Dev không chạy `finish` cho card của chính mình.
- Bị script từ chối thì sửa theo lý do nó nêu, không tìm cách né; kẹt thì báo Lead.

## Hoàn tác

Gộp sai thì lập phiếu rủi ro `docs/risk/RK-<n>.md`, xin người dùng chấp thuận, rồi `git revert -m 1 <mã merge>` (script in mã merge ở cuối lệnh `finish`).

## Chế độ worktree (chạy song song nhiều card code)

Người dùng đã mở quyền cho thư mục `D:\congviec\humana-wt\` (Kilo: `external_directory`). Dùng khi cần nhiều Dev cùng lúc.

1. **Bắt đầu** (Lead hoặc Dev): `python scripts/task-branch.py start --ticket <n> --slug <mô-tả> --worktree`. Tạo thư mục `D:\congviec\humana-wt\T-<n>` với nhánh `feature/<n>-<mô-tả>` từ `main` và cài phụ thuộc frontend (`--no-install` để bỏ qua). Mỗi card một worktree.
2. **Dev làm việc TRONG worktree**: sửa code bằng đường dẫn tuyệt đối dưới thư mục đó; chạy lệnh bash với `workdir` là thư mục đó. Chỉ sửa file thuộc `scope_edit` của card. **Không sửa `tasks/`, `docs/`** trong worktree: card và tài liệu nằm ở thư mục chính. Đặt card `review` ở thư mục chính.
3. **QA** làm ở thư mục chính: chạy ứng dụng của worktree bằng bash với `workdir` là worktree, ghi bằng chứng vào `docs/qa/` ở thư mục chính, đặt card `done`.
4. **Gộp**: `python scripts/task-branch.py finish --ticket <n> -m "<type>(scope): <tóm tắt>"`. Script nhận ra worktree, kiểm card, kiểm file ngoài `paths`, kiểm bí mật, chạy build trong worktree, commit, gộp `--no-ff` vào `main`, rồi gỡ worktree. Xung đột thì hủy gộp và giữ worktree để sửa. Gộp **tuần tự từng card**, thư mục chính phải ở `main`.
5. **Điều kiện song song**: các card chạy cùng lúc phải có `scope_edit` không chồng nhau; file dùng chung (`package.json`, `pnpm-lock.yaml`, `layout`, dữ liệu giả dùng chung) chỉ một card sửa. Tối đa 3 worktree cùng lúc.
