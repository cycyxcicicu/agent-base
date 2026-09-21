# Quy tắc Git

Nguồn: bài giảng "GitFlow CI/CD" của người dùng (33 slide), cộng quy tắc riêng của `agent-base`. Chỗ nào là suy luận của tôi hoặc bài giảng chưa rõ đều ghi ở mục 13.

## 0. Quy tắc số 1: AI chỉ xem git, người dùng làm mọi thao tác ghi

| Ai | Được | Không được |
|---|---|---|
| **AI (mọi agent, kể cả Claude)** | `git status`, `diff`, `log`, `show`, `blame`, `branch --list`, `ls-files`, `rev-parse`, `merge-base`, `rev-list`. Sửa file trong thư mục làm việc. **Viết kế hoạch commit** | `add`, `commit`, `push`, `pull`, `fetch`, `merge`, `rebase`, `reset`, `checkout`, `switch`, `restore`, `stash`, `tag`, `cherry-pick`, `revert`, `rm`, `mv`, `clean`, `worktree add`, `config`, `init`, `clone` |
| **Người dùng** | Tất cả: tạo nhánh, commit, rebase, push, tạo Merge Request, merge, tag | Vi phạm quy tắc ở các mục dưới (hook và CI sẽ chặn) |

- Quyền của AI được **ép ở công cụ** (Kilo chặn các lệnh trên qua `scripts/sync-adapters.ps1`), không chỉ ghi trên giấy.
- Khi làm xong, AI ghi **kế hoạch commit** vào task card (mẫu `agents/protocols/commit-plan.md`): danh sách lệnh `git add` và `git commit` chia theo chức năng, cộng lệnh rebase và push. Người dùng đọc, sửa nếu cần, rồi tự chạy.
- Việc AI làm mà cần git ghi (tạo worktree, hoàn tác) cũng viết thành lệnh cho người dùng chạy. Việc có thể làm mất code hay dữ liệu còn phải qua **cổng rủi ro** (`agents/protocols/risk-gate.md`). Vòng đời worktree từ tạo đến dọn: `agents/protocols/worktree-lifecycle.md`.

## 1. Nhánh (GitFlow)

| Nhánh | Tách từ | Merge vào | Mục đích | Môi trường |
|---|---|---|---|---|
| `main` (`master`) | — | — | Mã sẵn sàng triển khai cho khách hàng | production |
| `develop` | `main` | `main` | Mã tích hợp từ các tính năng, bản dựng gần nhất đã qua kiểm tra cơ bản | test / UAT |
| `release/*` | `develop` | `main` và `develop` | Chuẩn bị một lần release. Chỉ nhánh `fix/*` của lần release đó được merge vào | staging |
| `feature/*` | `develop` | `develop` | Tính năng mới hoặc sửa lỗi nhỏ | |
| `fix/*` | `release` | `release` | Sửa lỗi trên release | |
| `hotfix/*` | `main` | `main` (và `develop`) | Khắc phục lỗi nghiêm trọng trên production ngay | |

`main`, `develop`, `release/*` là **nhánh dùng chung, được bảo vệ**: không ai commit hay push thẳng, mọi thay đổi vào đó phải qua Merge Request.

## 2. Tên nhánh

Dạng: `<type>/<ticket>-<mô-tả-ngắn>`, viết thường, nối bằng dấu gạch ngang.

Loại: `feature`, `bugfix`, `hotfix`, `release`, `chore`, `refactor`, `docs`, `test`, `devops` (và `fix` cho lỗi trên release).

Ví dụ: `feature/43-create-thumbnail-from-s3`, `bugfix/26-count-creating-credit`, `hotfix/113-dont-update-x`, `devops/256-edit-docker-stuffs`. Nhánh release: `release/1.2.0`.

**Ticket = số của task card.** Ticket 12 ↔ `tasks/T-12.md` ↔ nhánh `feature/12-token-check`.

## 3. Commit

Dạng: `<type>(scope): <tóm tắt ngắn>`, tối đa 72 ký tự, scope bắt buộc.

Loại: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `ci`, `build`, `perf`.

Ví dụ: `feat(payment): Add API receive invoice`, `fix(invoice): Edit invoice model`, `chore(service): Format source`, `test(auth): Add login test`.

**Một commit là một thay đổi logic.** Commit từng phần, không gom một cục. Tách riêng: refactor, tính năng, đổi tên, format, cấu hình, test. Lý do (theo bài giảng): dễ thấy mục đích, dễ review, dễ merge và rebase.

## 4. Merge và rebase

| Dùng **merge** khi | Dùng **rebase** khi |
|---|---|
| Tích hợp nhánh dùng chung | Cập nhật nhánh cá nhân (feature) cho theo kịp nhánh gốc |
| Nhánh đã push, làm việc nhóm | **Trước khi tạo Merge Request** |
| `release → main`, `hotfix → main` và `develop` | Làm sạch lịch sử commit |

- **Không bao giờ rebase nhánh dùng chung** (`develop`, `release/*`, `main`).
- Quy trình một nhánh `feature` (theo slide 19 và 20):
  1. `git rebase develop` để dời commit của nhánh lên đầu `develop` mới nhất (commit D, E thành D', E').
  2. Tạo Merge Request vào `develop`; chỉ merge khi đạt chính sách ở mục 7.
- Không dùng `git merge develop` vào nhánh feature của bạn, vì sẽ sinh merge commit rác trong nhánh cá nhân.

## 5. Sửa lịch sử commit và đẩy lại

Khi nhánh có quá nhiều commit lộn xộn, làm lại cho gọn:

| Cách | Lệnh | Đặc điểm | Dùng khi |
|---|---|---|---|
| **Squash** | `git rebase -i HEAD~n` (hoặc theo mã commit) | Phức tạp, nhiều thao tác, giữ dòng thời gian của các commit | Làm chung một nhánh |
| **Reset --soft** | `git reset --soft HEAD~n` rồi commit lại | Nhanh, đơn giản, mất dòng thời gian | Một mình một nhánh |

Sau khi rebase hoặc sửa lịch sử phải đẩy lại nhánh **cá nhân**:
- Dùng `git push --force-with-lease`: chỉ được nhận nếu remote chưa có ai đẩy thêm.
- **Không** dùng `git push --force`: ép remote bằng bản của bạn dù remote đã có thay đổi khác.
- Chỉ đẩy ghi đè trên nhánh cá nhân của chính bạn, không bao giờ trên `main`, `develop`, `release/*`.

## 6. Tag

- Dạng `v<MAJOR>.<MINOR>.<PATCH>` (Semantic Versioning): **Major** khi thay đổi phá vỡ (API hay hành vi cũ không còn chạy), **Minor** khi thêm chức năng tương thích ngược, **Patch** khi sửa lỗi tương thích ngược. Hậu tố cho bản thử: `-rc`, `-prerelease`.
- **Mỗi lần release là một lần tag.** Triển khai production theo tag.
- Chủ yếu tag trên `main`, hiếm khi tag trên nhánh khác.
- Tag là điểm cố định gắn với một commit, khác nhánh là quá trình đang phát triển. Không sửa hay xóa tag đã công bố.

## 7. Merge Request

- **Mọi thay đổi vào `main`, `release/*`, `develop` đều phải qua Merge Request.**
- Tiêu đề: `<type>(scope): <tóm tắt ngắn>`.
- Chính sách để được merge:
  - Tối thiểu **2 người duyệt** (theo bài giảng).
  - Tên nhánh đúng dạng ở mục 2.
  - Commit đúng dạng ở mục 3.
  - **CI qua**.
- Mô tả bắt buộc có: link ticket, tóm tắt thay đổi, bằng chứng kiểm thử (link test case hoặc ảnh, kết quả).
- Trưởng dự án có quyền **từ chối** Merge Request không đạt chuẩn.
- Mục đích: kiểm soát chất lượng, đúng yêu cầu, chia sẻ kiến thức, ít lỗi hơn trên release/main, dễ truy nguồn gốc lỗi.

## 8. `.gitignore`

- Mục đích: không commit file cục bộ, file sinh tự động, giảm kích thước repo, giảm xung đột merge, giảm nguy cơ lộ khóa bí mật.
- Đặt `.gitignore` ở gốc và ở từng thư mục con khi cần (`frontend/`, `backend/`, `terraform/`...). Quy tắc gần file hơn bổ sung hoặc ghi đè quy tắc cấp trên; dùng `!` để bỏ loại trừ.
- `.gitignore` chỉ áp dụng cho file **chưa được track**. Muốn bỏ track file đã commit: `git rm --cached <file>`.
- Tối thiểu phải loại trừ: `.env`, `.env.local`, thư mục IDE và công cụ AI (`.idea/`, `.vscode/`, `.claude/`, `.codex/`, `.cursor/`), `*.log`, `node_modules/`, `dist/`, `target/`, `*.class`.
- Ngoại lệ có chủ ý trong `agent-base`: `.kilo/agents/` và `.agents/rules/` **được commit** (là file sinh ra cho công cụ, CI kiểm tra chúng khớp nguồn).

## 9. CI/CD

- **CI** (mỗi lần push hoặc Merge Request): build tự động, test, lint, kiểm tra bảo mật, quét giấy phép.
- **CD**: build image sẵn sàng deploy, tự động deploy (Delivery: bấm duyệt để deploy; Deployment: tự động hoàn toàn).
- Lợi ích: phát hiện lỗi sớm khi push, release nhanh hơn, deploy nhất quán, dễ rollback.
- Trong repo này: `.github/workflows/check.yml` kiểm tra file sinh ra còn khớp, tên nhánh, tên commit và phạm vi file của task (`merge-gate`). Bước build, test, deploy của dự án thật do `devops` bổ sung theo từng dự án.

## 10. Hook trên máy (giúp bạn khỏi sai)

Bật bằng `scripts/install-hooks.ps1`.

| Hook | Chặn khi |
|---|---|
| `pre-commit` | commit bởi danh tính `(agent)`; commit thẳng lên `main`/`master`/`develop`/`release/*` (trừ khi đang kết thúc một merge); tên nhánh sai dạng; có file `.env*`, `.pem`, `.key`; file > 5 MB; dòng thêm vào trông như khóa hay mật khẩu; đã đổi vai trò hoặc `AGENTS.md` mà file sinh ra chưa khớp |
| `commit-msg` | tiêu đề không phải `<type>(scope): <tóm tắt>` hoặc dài quá 72 ký tự; commit hoàn tác hoặc xóa từ 10 file thiếu dòng `Risk-Approved: RK-<số>` hợp lệ (phiếu `docs/risk/RK-<số>.md` phải có `Status: APPROVED`) |
| `pre-push` | push thẳng lên nhánh được bảo vệ; xóa nhánh được bảo vệ; push ghi đè nhánh được bảo vệ. **Cảnh báo** (không chặn) nếu nhánh cá nhân chưa rebase lên `origin/develop` |

Ghi đè có chủ ý một lần: `ALLOW_PROTECTED_COMMIT=1`, `ALLOW_PROTECTED_PUSH=1`, `ALLOW_FORCE_PUSH=1` (đặt biến môi trường trước lệnh). Ví dụ lúc khởi tạo repo lần đầu, khi `develop` chưa tồn tại trên GitHub.

**Giới hạn**: hook nằm trên máy và bỏ qua được bằng `--no-verify`. Chốt chặn thật là CI và bảo vệ nhánh trên GitHub (mục 11). Với AI, chốt chặn là quyền công cụ (mục 0).

## 11. Bảo vệ ở phía GitHub (người dùng cài một lần)

Tôi không cài được vì cần quyền quản trị GitHub. Trong repo: **Settings → Branches → Add branch ruleset (hoặc branch protection rule)** cho `main`, `develop` và mẫu `release/*`, bật:

1. Require a pull request before merging, với 2 lượt duyệt.
2. Require status checks to pass: chọn kiểm tra `agent-base` từ workflow `check.yml`.
3. Block force pushes và restrict deletions.
4. Require review from Code Owners (`.github/CODEOWNERS` đã có).

Với repo riêng tư, tính năng này có thể cần gói GitHub trả phí (chưa xác minh với tài khoản của bạn).

## 12. Hoàn tác

Người dùng gộp một task bằng Merge Request nên có một merge commit. Quay lại một task = `git revert -m 1 <mã merge commit>` trên nhánh mới (bỏ `-m 1` nếu merge kiểu squash), chạy test, rồi Merge Request. Ghi mã merge commit vào task card sau khi merge. AI chỉ **viết lệnh** cho người dùng chạy, và **chỉ sau khi qua cổng rủi ro** (`agents/protocols/risk-gate.md`): đánh giá bằng lệnh chỉ đọc, phiếu rủi ro, người dùng chấp thuận rõ ràng. Commit hoàn tác mang dòng `Risk-Approved: RK-<số>`. Git không hoàn tác được thay đổi cơ sở dữ liệu, dữ liệu đã ghi và deploy: task nào đụng các thứ đó phải có "Kịch bản hoàn tác" trong card.

## 13. Điều tôi chưa chắc, bạn xác nhận

1. **Lịch sử bán tuyến tính (semi-linear)**: slide 6 tiêu đề "Semi-Linear" và slide 19–20 dạy rebase feature rồi merge, nên tôi hiểu đây là kiểu bạn chọn (trong 4 trường phái ở slide 3). Nếu sai (ví dụ dùng squash-and-merge), quy tắc merge ở mục 4 và 12 cần đổi.
2. **`fix/*` và `bugfix/`**: slide 9 gọi nhánh sửa lỗi trên release là `fix/*`, slide 21 liệt kê loại `bugfix/`. Tôi coi `bugfix/` là sửa lỗi thường (tách từ `develop`) và `fix/` là sửa lỗi trên release.
3. **Hai người duyệt**: repo cá nhân chỉ có một người nên chưa thể có 2 lượt duyệt. Bạn cần chọn: hạ xuống 1, hoặc thêm người duyệt.
4. **Tên tag**: slide dùng mẫu `v<MAJOR>.<MINOR>.<PATCH>` nhưng ví dụ ghi `v.1.0.1`. Tôi lấy theo mẫu (không có dấu chấm sau `v`).
5. **`hotfix → main và develop`**: slide 9 chỉ ghi merge vào `main`, slide 19 ghi cả hai. Tôi chọn cả hai.
6. **Slide 27 "Demo", 30 "Frontend", 31 "Backend"** là hình ảnh, tôi không đọc được nội dung quy trình CI/CD cụ thể của từng phần.
