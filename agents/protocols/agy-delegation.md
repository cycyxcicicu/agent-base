# Giao thức ủy thác cho Antigravity qua agy-bridge (agy-delegation)

Khuôn mẫu prompt: xem [delegation-prompt.md](file:///Users/ducnvh/Documents/agent-base/agents/protocols/delegation-prompt.md). Tầng model: xem [model-policy.md](file:///Users/ducnvh/Documents/agent-base/agents/protocols/model-policy.md). `model-policy.md` ánh xạ tầng strong/standard/fast sang model của Kilo qua `agents/models.txt`; mục 3 dưới đây chọn model của `agy` và độc lập với bảng đó. Hai bên khớp ở ba nguyên tắc: nâng tầng sau 2 lần thất bại, không hạ tầng cho review/bảo mật, reviewer không yếu hơn người viết.

## 1. Vai trò
| Bên | Làm | Không làm |
|---|---|---|
| AI chỉ đạo (Claude, Codex, Gemini...) | Hiểu yêu cầu, viết brief ngắn ra file, chọn model, chạy MỘT lệnh bridge, đọc 3 dòng kết quả, chạy cổng kiểm bằng máy, báo người dùng ngắn gọn | Không tự viết tài liệu/mã/sơ đồ dài, không đọc log dài, không đổi luật khi agy đang chạy, không dọn/xóa/commit khi người dùng chưa nói rõ |
| `agy` | Làm việc nặng (tài liệu, plan, sơ đồ, code, test) trong worktree riêng, dùng cấu hình dự án sẵn có | Không push, không ghi ngoài `--allow-write`, không đọc file bí mật theo tên |
| Người dùng | Quyết định, duyệt, đổi tài khoản `agy` khi hết quota | |

## 2. Vòng làm việc (6 bước)
1. Brief: viết `brief.md` từ `agents/templates/agy-brief/{code,doc,plan,diagram,review}.md`.
2. Chọn model theo mục 3 và ghi `--model` rõ.
3. Chạy một lệnh, chạy nền, luôn có `--worktree`:
`python3 ~/Documents/agent-base/scripts/agy-acp-bridge.py run --dir <repo> --task-file <brief.md> --worktree [--seed <file>...] --allow-write <đường dẫn chính xác>... [--apply] --model <m>`
4. Đọc 3 dòng stdout: `STATUS` (`ok|warn|fail|quota`, kèm `DOI-TAI-KHOAN-AGY` khi hết quota), `FILES` (số file đổi, `VIOLATION`, `wt=`, `applied=`), `REPORT` (đường dẫn báo cáo).
5. Kiểm bằng máy (mục 6). Không tin lời agy tự báo "xong".
6. Báo người dùng: kết quả thật, phần chưa kiểm chứng, bước tiếp. Không commit trừ khi người dùng yêu cầu.
- **Mã thoát**: `0` ok/warn; `2` agy thất bại; `3` vi phạm ghi ngoài phạm vi; `4` xung đột lock; `5` xung đột apply; `6` lỗi worktree; `7` hết quota.
- **Phải dừng và báo ngay**: mã 7 (bảo người dùng đổi tài khoản), `VIOLATION` hoặc mã 3/5/6 (báo nguyên văn, không tự sửa).
- Một lượt giao việc chạy xong rồi mới đổi luật hay chạy lượt khác; không dừng/chạy lại giữa chừng.

## 3. Chọn model theo độ khó
Hạn mức của `agy` không phải tiêu chí chọn model.
| Loại việc | Model |
|---|---|
| Đơn giản, rõ ràng (sửa chữ, đổi tên, tài liệu ngắn) | `gemini-3.8-flash-medium` |
| Viết mã, test, sơ đồ, plan nhiều ràng buộc | `gemini-3.8-flash-high` |
| Khó về an ninh/logic, review | Model mạnh nhất có trong `agy`, suy luận cao ngay từ đầu. Đã dùng cho review: `gemini-4-argon-medium` |
- Review luôn dùng phiên mới và model khác model đã viết.
- Thất bại hai lần ở một tầng: nâng tầng, không thử lại cùng model.
- **Chưa kiểm chứng**: có model mạnh hơn `gemini-4-argon-medium` hay không; chưa đo chất lượng giữa các model. Xem danh sách thật bằng `agy --help`.

## 4. Quyền của agy
Mặc định cho phép; chỉ chặn nhóm nguy hiểm. Agy không bị dừng giữa phiên vì thiếu quyền: lệnh bị chặn được báo lại kèm lý do để agy tự đổi cách (tối đa 3 lần), STATUS `warn`.
| Nhóm | Quy tắc |
|---|---|
| Đọc, phân tích, build, test | Cho phép mặc định |
| Git đọc | Cho phép đủ: `log show diff blame reflog rev-parse ls-files cat-file`, kể cả `HEAD~3`, `REV:path` |
| Git cục bộ | Cho phép: `add <path>`, `commit`, `branch`, `merge`, `tag`, `cherry-pick`, `revert`. Với `--worktree` còn `checkout`, `switch`, `stash`, `restore`, `reset`, `rebase`, `add -A`. Không `--worktree`: chặn `reset --hard`, `clean`, `stash`, `restore .`, `checkout .`, `add -A`, đổi nhánh, `rebase` (tránh xóa thay đổi dở của phiên khác) |
| Git lấy về | Cho phép: `fetch`, `ls-remote`, `remote -v`, `pull --ff-only` (`pull` trần chỉ với `--worktree`) |
| Chặn mọi chế độ | `git push`, `git config` ghi, đổi remote, `--no-verify`, lệnh git nhắm repo ngoài thư mục làm việc; `rm -r`, `sudo`, `curl`, `wget`, cài gói, `docker`; đọc `.env*`, `*.pem`, `*.key`, `id_rsa*`, `*credentials*` theo tên |
| Ghi file | Chỉ trong `--allow-write` (đường dẫn chính xác, cấm glob) |
| Commit của agy | Không còn là vi phạm; bridge ghi số commit và SHA vào báo cáo. Message commit chỉ mô tả thay đổi, không ghi thông tin AI |

**Giới hạn đã biết (đọc trước khi tin):** chính sách lệnh là best-effort. Bốn vòng review độc lập đều tìm ra cách lách mới (glob, biến, nháy, cờ dính). Lớp chắc chắn là: worktree riêng, `--sandbox` (chặn ghi ngoài workspace), kiểm HEAD/lịch sử, phát hiện `VIOLATION`, và `--apply` chỉ chép file trong `--allow-write`. Đọc bí mật bằng glob/biến không bị chặn.

## 5. Quản lý phiên
| Tình huống | Làm gì |
|---|---|
| Task mới, khác chủ đề | Phiên mới |
| Sửa nhỏ tiếp cho task vừa xong | `--session <id>`, tối đa 2–3 lượt |
| Review | Luôn phiên mới, model khác phiên viết |
| Quá 3 lượt hoặc nghỉ lâu | Phiên mới, đưa tóm tắt từ file báo cáo (lượt n tốn xấp xỉ n × 24k token) |
| `quota` (mã 7) | Đổi tài khoản `agy`, chạy lại phiên mới |

## 6. Cổng kiểm bằng máy
| Loại việc | Cổng |
|---|---|
| Code | `git -C <repo> diff --stat` và test đơn vị có lọc |
| Tài liệu | `doc-preflight.py`, `verify-gate.py` |
| Sơ đồ | `ve-so-do.py <spec> --check-only`, mở xem ảnh PNG |
| Review | Phiên `agy` MỚI, model khác phiên viết |

## 7. Điều cấm tuyệt đối
- `git push`; cờ `--dangerously-skip-permissions`; đọc/in/commit file bí mật; ghi ngoài `--allow-write`.
- AI chỉ đạo không tự commit/push/xóa worktree/nhánh khi người dùng chưa nói rõ.
- Chính sách mục 4 đã nằm trong `scripts/agy-acp-bridge.py` (kiểm 2026-11-15: 139 test OK, bảng 26 lệnh cho phép và 40 lệnh chặn đúng). Chưa sửa: khi mọi lệnh bị từ chối, STATUS vẫn có thể là `ok` thay vì `warn`; luôn đọc `denied=` và `FILES`.
- Dọn worktree `~/Documents/worktrees/agy/<repo>-<slug>-<ts>` và nhánh `agy/*` sau mỗi lượt đã kiểm và đã `--apply`, khi người dùng cho phép dọn. Bridge không tự xóa.
