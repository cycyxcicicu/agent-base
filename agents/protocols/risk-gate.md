# Cổng rủi ro và quy trình hoàn tác

Áp dụng cho **mọi việc có thể làm mất code, dữ liệu hoặc công việc đang làm**. AI không bao giờ tự quyết những việc này. Thứ tự luôn là: **đánh giá → trình bày rủi ro → người dùng chấp thuận rõ ràng → mới thực hiện**. Việc git thì AI chỉ *viết lệnh*, người dùng chạy (`agents/protocols/git-rules.md`).

## 1. Việc nào phải qua cổng

| Nhóm | Ví dụ |
|---|---|
| Hoàn tác | `git revert`, quay lại một task, một release |
| Xóa | xóa file, thư mục, nhánh, tag, worktree; xóa từ 10 file trở lên trong một thay đổi |
| Ghi đè hoặc sinh lại | ghi đè file có nội dung của người khác, sinh lại file thay bản đang có, thay thế module |
| Hàng loạt | đổi tên, di chuyển, định dạng lại hàng loạt |
| Sửa lịch sử | rebase, squash, `reset`, đẩy ghi đè |
| Dữ liệu và triển khai | migration, thay đổi cơ sở dữ liệu, deploy, publish, đổi cấu hình môi trường |
| Phụ thuộc và dùng chung | nâng phiên bản gói, sửa file dùng chung ngoài phạm vi task |
| Quyền và quy tắc | sửa `AGENTS.md`, vai trò, quyền, hook |

Nghi ngờ việc nào đó có thuộc nhóm này không thì **coi là có** và hỏi.

## 2. Năm bước

1. **Đánh giá** (mục 3): xác minh bằng lệnh chỉ đọc chính xác thứ cần đổi, và liệt kê cái sẽ mất.
2. **Lập phiếu rủi ro** `docs/risk/RK-<số>.md` theo mẫu (mục 4), trạng thái `Status: PENDING`. Trình bày cho người dùng bằng chữ dễ hiểu.
3. **Chờ chấp thuận** (mục 5). Chưa có thì **không viết lệnh** và không sửa gì.
4. **Thực hiện**: việc sửa file thì làm đúng trong phạm vi phiếu; việc git thì viết lệnh (mục 6) cho người dùng chạy. Commit dạng này phải có dòng `Risk-Approved: RK-<số>`.
5. **Kiểm tra sau**: chạy test (nhờ `runner`), ghi kết quả vào phiếu và task card, viết ghi chú cho agent sau.

## 3. Đánh giá hoàn tác: phải xác minh, không được đoán

| Câu hỏi | Cách xác minh (lệnh chỉ đọc) | Nếu không rõ |
|---|---|---|
| Đúng commit nào cần quay lại? | mã merge commit trong task card; `git log --oneline --merges -20`; `git show --stat <mã>` | Hỏi người dùng, không chọn hộ |
| Merge kiểu nào? | `git show --no-patch --format=%P <mã>`: hai mã cha là merge commit (dùng `-m 1`); một mã cha là squash hoặc rebase (dùng `git revert <mã>`, **không** `-m`) | Dừng, hỏi |
| Sẽ mất gì? | `git diff --stat <mã>^1 <mã>` (merge) hoặc `git show --stat <mã>`; liệt kê file, hàm, hành vi cụ thể | Không kết luận |
| Ai phụ thuộc vào nó? | `git log --oneline <mã>..HEAD -- <file>` (commit sau đã sửa cùng file); `git grep` các tên hàm hoặc lớp bị bỏ | Ghi vào "chưa xác minh" |
| Việc đang chạy có dựa vào nó không? | `git worktree list`, `git branch -a --no-merged`, các card `doing` | Hỏi Orchestrator |
| Có thay đổi chưa commit ở worktree khác? | `git -C <đường-dẫn> status --short` cho từng worktree | Báo người dùng |
| Đã phát hành chưa? | `git tag --contains <mã>` | Nếu đã lên production: đi đường `hotfix`, hỏi người dùng |
| Có phần ngoài git không? | có file migration trong thay đổi? dữ liệu đã ghi? đã deploy? dịch vụ ngoài? card có "Kịch bản hoàn tác"? | Nêu rõ là **không hoàn tác được bằng git** |
| Từng revert nhánh này chưa? | `git log --oneline --grep="hoan tac" -i` | Nếu rồi: merge lại nguyên nhánh cũ sẽ **không** đem lại thay đổi, phải revert bản revert |
| Trạng thái kiểm thử hiện tại? | nhờ `runner` chạy test làm mốc trước | Ghi "chưa có mốc" |

Ghi lại **mã HEAD** tại lúc đánh giá vào phiếu. Đó là mốc để biết chấp thuận còn hiệu lực hay không.

## 4. Mẫu phiếu rủi ro `docs/risk/RK-<số>.md`

```markdown
# RK-3: Hoàn tác T-12 (feature/12-token-check)

Status: PENDING
Ngày lập: YYYY-MM-DD        Người lập: orchestrator
Mốc kiểm tra: nhánh develop, HEAD <mã>
Yêu cầu nguyên văn của người dùng: "..."

## Đã xác minh (kèm lệnh đã dùng)
- Merge commit: <mã> (2 mã cha, dùng -m 1) — `git show --no-patch --format=%P <mã>`

## Sẽ mất hoặc bị đổi
- (liệt kê file, hàm, hành vi cụ thể)

## Bị ảnh hưởng
- (task, nhánh, worktree, commit sau đó chạm cùng file)

## Ngoài git (không hoàn tác được bằng git)
- (migration, dữ liệu đã ghi, deploy, dịch vụ ngoài) hoặc "không có"

## Xung đột dự kiến
- (file nào, vì sao)

## Mức rủi ro: thấp | vừa | cao
(lý do một hai câu)

## Cách giảm rủi ro
- Nhánh sao lưu trước khi làm, chạy test trước và sau, hoàn tác từng phần...

## Phương án khác
- (sửa tiến thay vì lùi, hoàn tác một phần, tắt tính năng bằng cờ...)

## Chưa xác minh
- (điều tôi chưa kiểm được và vì sao)

## Câu hỏi cần bạn trả lời
1. ...

## Chấp thuận
(để trống. Chỉ điền khi người dùng đã chấp thuận bằng văn bản: chép **nguyên văn** câu của họ và ngày)
```

Giá trị `Status`: `PENDING`, `APPROVED`, `REJECTED`, `EXPIRED`. Chỉ đổi sang `APPROVED` sau khi người dùng chấp thuận rõ ràng (mục 5).

## 5. Chấp thuận

- Chỉ **người dùng** chấp thuận, **bằng văn bản** và **nêu số phiếu** (ví dụ "Chấp thuận RK-3"). Im lặng, "ok" chung chung, hay AI tự suy ra ý người dùng **không tính**.
- Chấp thuận chỉ áp dụng cho **đúng nội dung phiếu và đúng mốc HEAD**. Nếu phiếu đổi, HEAD đổi, hoặc có commit mới chạm các file liên quan thì phiếu chuyển `EXPIRED`, phải đánh giá lại.
- Mức **cao**: AI nêu lại bằng chữ đơn giản thứ sẽ mất và hỏi lần hai ("Xác nhận lần cuối RK-3?") trước khi viết lệnh.
- Bị từ chối hoặc chưa chấp thuận: AI không viết lệnh. AI chỉ được đề xuất phương án an toàn hơn.
- Một chấp thuận không dùng lại cho việc khác.

## 6. Lệnh hoàn tác mẫu (chỉ viết sau khi phiếu `APPROVED`)

AI ghi các lệnh này vào mục "Kế hoạch commit" của task card, người dùng chạy từng dòng:

```
git status
git switch develop
git pull --ff-only
git branch backup/RK-3
git switch -c bugfix/12-revert-token-check
git revert -m 1 <mã-merge-commit> --no-commit
```

Chạy test (nhờ `runner`, hoặc tự chạy lệnh test của dự án), xem `git diff --cached`, rồi:

```
git commit -m "fix(auth): hoan tac T-12 token-check" -m "Risk-Approved: RK-3"
```

Sau đó rebase, đẩy và tạo Merge Request như thường lệ (mọi thay đổi vào `develop` đều qua Merge Request). Nếu thay đổi cần sửa cả production thì dùng nhánh `hotfix/<ticket>-...` tách từ `main`.

- Merge kiểu squash: bỏ `-m 1`.
- Có xung đột khi revert: dừng, báo người dùng, không tự chọn bên.
- Nhánh `backup/RK-3` là dấu mốc trước khi làm; người dùng xóa sau khi hài lòng.

## 7. Sau khi hoàn tác

- Ghi vào task card ("Sau khi merge") mã commit hoàn tác.
- Viết ghi chú cho agent sau: nhánh nào đã bị hoàn tác và **không** merge lại nguyên nhánh cũ; nếu muốn đưa tính năng trở lại, làm nhánh mới hoặc revert bản revert (qua cổng rủi ro mới).
- Cập nhật phiếu: `Status` giữ `APPROVED`, thêm kết quả thực tế.

## 8. Móc kỹ thuật

- Hook `commit-msg`: commit có tiêu đề chứa "revert" hoặc "hoan tac", hoặc xóa từ **10 file** trở lên, bắt buộc có dòng `Risk-Approved: RK-<số>`, và `docs/risk/RK-<số>.md` phải tồn tại với dòng `Status: APPROVED`.
- CI (`.github/workflows/check.yml`) kiểm điều tương tự trên mỗi Merge Request.
- `scripts/merge-gate.ps1` luôn cho phép `docs/risk/RK-*.md` đi cùng nhánh.
- **Giới hạn**: máy chỉ kiểm dòng trailer và trạng thái trong phiếu, không kiểm được ai đã chấp thuận. Phần đó dựa vào bạn. Hook bỏ qua được bằng `--no-verify`, và mẫu "10 file" chỉ là ngưỡng thực dụng, không phải mọi việc rủi ro đều có dấu hiệu đó.
