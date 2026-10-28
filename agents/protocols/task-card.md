# Mẫu task card

Sao chép nội dung dưới đây thành `tasks/<thư mục epic>/T-<ticket>-<slug>.md` (xem mục "Nhóm việc và tài liệu"). Số ticket dùng luôn trong tên nhánh: ticket 12 ↔ `tasks/T-12.md` ↔ `feature/12-token-check`. Phần giữa hai dòng `---` được script đọc (`scripts/merge-gate.ps1`), giữ đúng tên khóa và định dạng danh sách.

```markdown
---
id: T-12
size: medium
status: todo
owner: dev-a
epic: E1
phase: GĐ1
outputs: []
branch: feature/12-token-check
requirements: [R-003, R-004]
scope_edit:
  - src/auth/**
  - tests/auth/**
scope_deny:
  - package.json
---

# T-12: <tiêu đề ngắn>

## Mục tiêu
(1–3 câu: làm gì, để đạt gì)

## Tài liệu tham chiếu & Sơ đồ (Dev bắt buộc đọc trước khi code)
- **Yêu cầu chức năng**: `docs/requirements/<file>.md` (khớp với mã trong `requirements: [...]`)
- **Sơ đồ kiến trúc / nghiệp vụ (Archify)**: `docs/diagrams/index.html` (chỉ rõ file sơ đồ cụ thể, ví dụ: `docs/diagrams/<hệ-thống>-archify.html` hoặc `docs/diagrams/flow-<tên>.html`)
- **Đặc tả API / Dữ liệu liên quan**: `docs/spec/<file>.md` hoặc `docs/db/<file>.md`

## Contract & Happy Path (Đặc tả trước khi code)
- **Đầu vào (Input)**: (cấu trúc dữ liệu, request payload, parameters)
- **Đầu ra (Output)**: (response payload, status code, format)
- **Kịch bản Happy Path**: (input cụ thể -> kết quả mong đợi cụ thể có thể quan sát được)

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch (Plan Review Gate - AGENTS.md §16)
- **Quy chuẩn mã Subtask**: Đặt tên theo dạng `T-<ticket>.<số_thứ_tự>` (ví dụ: `T-12.1`, `T-12.2`, `T-12.3`...).
- **Cấu trúc mỗi Subtask**: Bắt buộc có **Mục đích cụ thể** (Làm gì, để giải quyết gì), **Phạm vi file**, **Người làm** và **Tiêu chí xong**:
  - [ ] **T-12.1** [Mục đích: <làm gì, để đạt kết quả gì>]: Scope: `<file1>`, `<file2>` · Assigned: `dev` · Tiêu chí xong: `pytest -q <file> PASS` · Handoff: `docs/notes/inbox/T-12/T-12.1-dev.md`
  - [ ] **T-12.2** [Mục đích: <làm gì, để đạt kết quả gì>]: Scope: `<file3>` · Assigned: `dev` · Tiêu chí xong: `pytest -q <file> PASS` · Handoff: `docs/notes/inbox/T-12/T-12.2-dev.md`
  - [ ] **T-12.3** [Mục đích: <kiểm thử nghiệm thu độc lập>]: Lệnh: `pytest -q <path>` · Assigned: `qa` · Tiêu chí xong: `100% PASS` · Handoff: `docs/notes/inbox/T-12/T-12.3-qa.md`
- **Cổng phê duyệt kế hoạch (Bắt buộc trước khi code)**:
  - [ ] Reviewer verdict (tư vấn): (Ghi rõ ngày và verdict tư vấn kỹ thuật của Reviewer/vai thẩm định; chưa có verdict cấm chuyển `doing`)
  - [ ] **Người dùng duyệt phạm vi bằng file**: (Bắt buộc dấu [x] do con người ghi trực tiếp trong file kèm tên và ngày; AI tuyệt đối không tự đóng)

## Tiêu chí xong
- [ ] Happy Path Unit Test chạy PASS 100%
- [ ] ...
- [ ] ...

## Phụ thuộc
(task nào phải xong trước, hoặc "không")

## Ghi chú bàn giao
(thêm ở cuối, mỗi mục ghi ngày và tên agent)

## Nhật ký phiên
(đã làm gì, quyết định gì, còn dang dở gì)

## File đã đổi
(danh sách, kèm lý do)

## Kết quả test
(lệnh đã chạy và kết quả)

## Kế hoạch commit (người dùng chạy hoặc nhờ AI chạy)
(agent viết theo `agents/protocols/commit-plan.md`; agent KHÔNG tự chạy)

## Chấp thuận rủi ro
(nếu task có việc mất code, dữ liệu hay công việc: số phiếu RK-<n> và trạng thái. Xem `agents/protocols/risk-gate.md`. Không có thì ghi "không có")

## Sau khi merge
- Mã merge commit: (người dùng điền, dùng để hoàn tác bằng `git revert -m 1`)

## Kịch bản hoàn tác
(bắt buộc nếu đụng cơ sở dữ liệu, dữ liệu thật hoặc deploy. Nếu không: "chỉ cần git revert -m 1 <merge commit>")
```

**Card giao diện** (frontend, mobile) thêm mục "Mẫu tham chiếu" và "Kiểm tra bằng mắt", và chỉ được `done` khi QA/Reviewer kiểm bằng mắt: xem `agents/protocols/ui-fidelity.md`. Dev chỉ đặt `review`, không tự đặt `done`, không sửa mục tiêu và tiêu chí của card.

## Giá trị hợp lệ

| Khóa | Giá trị |
|---|---|
| `size` | `small`, `medium`, `large` |
| `epic` | mã epic trong `tasks/EPICS.md` (E0, E1...). **Bắt buộc** |
| `phase` | phase của epic đó trong `tasks/EPICS.md` (PT, GĐ1, GĐ2). **Bắt buộc** |
| `outputs` | danh sách đường dẫn tài liệu task tạo ra (ADR, spec, báo cáo...). **Bắt buộc với task viết tài liệu**, task code để `[]` |
| `blocked_by` | danh sách id task phải `done` trước, ví dụ `[T-2]` |
| `status` | `todo`, `doing`, `review`, `done`, `blocked` |
| `branch` | `<type>/<ticket>-<mô-tả-ngắn>` theo `agents/protocols/git-rules.md` |
| `scope_edit` | mẫu đường dẫn tính từ gốc repo, dùng `*` (trong một thư mục) và `**` (nhiều cấp) |
| `scope_deny` | mẫu đường dẫn, luôn thắng `scope_edit` |

## Đặt tên task (nhìn tên là biết làm gì)

Mã số không nói được việc gì. Mã `T-<số>` chỉ là **khóa ổn định** (script, `blocked_by`, nhánh đều dựa vào nó, không đổi sau khi tạo); **tên** thì luôn kèm nghĩa.

**Tên task = loại việc + việc gì**, giống tên nhánh: đọc `T-13-fix-loi-xuat-excel` là biết ngay đây là sửa lỗi xuất Excel.

| Loại việc (từ đầu của slug) | Dùng khi | Nhánh tương ứng |
|---|---|---|
| `feat` | thêm hoặc đổi chức năng | `feature/...` (hoặc `feat/...`) |
| `fix` | sửa lỗi | `fix/...` (hoặc `bugfix/...`) |
| `hotfix` | sửa lỗi gấp trên bản đang chạy | `hotfix/...` |
| `refactor` | tổ chức lại mã, không đổi hành vi | `refactor/...` |
| `docs` | viết hoặc sửa tài liệu | `docs/...` |
| `test` | thêm hoặc sửa test | `test/...` |
| `chore`, `devops`, `perf` | việc vặt, hạ tầng và CI, hiệu năng | cùng tên |

| Thứ | Quy tắc | Ví dụ |
|---|---|---|
| Tên file card | `T-<số>-<loại>-<mô tả>.md` | `T-13-fix-loi-xuat-excel.md` |
| Slug (phần sau số) | chữ thường không dấu, số, gạch ngang, tối đa 40 ký tự; bắt đầu bằng **loại việc**, rồi **động từ + đối tượng**; cấm chữ vô nghĩa (`update`, `misc`, `task-moi`) | `feat-them-cot-an-hien`, `docs-chuan-hoa-ten-task` |
| Tiêu đề (dòng `# T-13: ...`) | tiếng Việt có dấu, một câu tối đa 70 ký tự, nói rõ **kết quả** người dùng thấy, không bắt đầu bằng mã | `# T-13: Sửa lỗi xuất Excel mất dòng cuối` |
| Nhánh | `<loại nhánh>/<số>-<mô tả>` (mô tả bỏ từ loại vì đã nằm ở tên nhánh) | `fix/13-loi-xuat-excel` |
| Thư mục worktree | `T-<số>-<loại>-<mô tả>` | `T-13-fix-loi-xuat-excel` |
| Ghi chú bàn giao | `T-<số>-<loại>-<mô tả>-<vai>.md` | `T-13-fix-loi-xuat-excel-dev.md` |
| Subtask | `T-<số>.<n>-<loại>-<mô tả>` | `T-13.1-test-viet-kiem-tra` |
| Mã khác (rủi ro, thay đổi) | mã + mô tả | `RK-3-xoa-hang-loat-nhat-ky.md`, `CR-2-doi-dinh-dang-xuat.md` (`ADR-13-file-approval.md` đã đúng) |

- **Cùng một cái tên** cho card, nhánh, worktree và ghi chú, để lần theo bằng mắt và bằng lệnh `grep`.
- Trong văn bản, lần nhắc đầu viết `T-13 (sửa lỗi xuất Excel)`, sau đó chỉ `T-13`.
- `python scripts/task-board.py --check` **cảnh báo** (chưa chặn) khi tên file chỉ có mã, slug sai dạng hoặc không bắt đầu bằng loại việc, hoặc thiếu tiêu đề thật. Card cũ đổi tên khi có dịp; đổi tên file không đổi `id` nên không làm hỏng `blocked_by`.

## Nhóm việc và tài liệu

- Mỗi card thuộc đúng **một epic** và **một phase** trong `tasks/EPICS.md`. Chưa có epic phù hợp thì Lead thêm vào `tasks/EPICS.md` và báo người dùng, không để trống.
- **Card nằm trong thư mục của epic**: `tasks/<Thư mục>/T-<số>-<slug>.md` (cột "Thư mục" trong `tasks/EPICS.md`), ví dụ `tasks/E2-tuyen-dung-cv/T-12.md`. Số `T-<số>` vẫn tăng dần duy nhất cho cả dự án, không đánh lại theo từng thư mục. Merge gate chấp nhận card ở `tasks/T-<số>.md` hoặc `tasks/<thư mục>/T-<số>.md`.
- Dự án mới: **trước khi tạo card đầu tiên**, Lead thay bảng mẫu trong `tasks/EPICS.md` bằng epic thật của dự án và trình người dùng duyệt.
- Task viết tài liệu phải liệt kê **từng file** trong `outputs` (không dùng `**`). Mỗi file tài liệu đó mở đầu bằng dòng:
  `> Task: T-<n> · Epic: E<n> · Vai: <vai>`
  để từ tài liệu tra ngược được về card.
- Sau khi tạo card hoặc đổi `status`, chạy `python scripts/task-board.py` để cập nhật `tasks/BOARD.md` và `python scripts/generate-dashboard.py` để cập nhật bảng điều khiển ở `build/viewer/` (thư mục sinh ra, đã `.gitignore`). **Không sửa `BOARD.md` và `build/viewer/` bằng tay.**
- Muốn biết đang ở đâu, việc gì làm được ngay: đọc `tasks/BOARD.md` hoặc mở `build/viewer/index.html` trên trình duyệt (hoặc chạy `python scripts/watch-swarm.py` rồi vào http://localhost:4200/dashboard.html).
- Card chỉ được chuyển `done` khi mọi file trong `outputs` đã tồn tại (script báo lỗi nếu thiếu).

Card của chính task (`tasks/<id>.md`) luôn được phép sửa, không cần khai báo.
Hai task chạy song song không được có `scope_edit` chồng nhau. File dùng chung chỉ đưa vào `scope_edit` của một task duy nhất.
