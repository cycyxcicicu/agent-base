> summary: T-04 sổ nợ kỹ thuật: lọc 109 mục giả, tách luật quét khỏi nội dung tài liệu
Task: T-04        Agent: dev        Ngày: 2026-10-24

Skill đã chọn & áp dụng: `systematic-debugging` (đo 109 mục giả trước khi sửa), `codebase-design` (tách luật quét khỏi nội dung tài liệu).

Checklist đã tuân thủ:
- Mọi kết luận có lệnh + số liệu thật; số 109 đo khi loại card T-04 tự khớp để không trôi.
- Không sửa tài liệu nguồn/AGENTS/roles; không đụng `.kilo/worktrees`; chỉ loại khỏi phép quét.
- Mọi thay đổi nằm trong `scope_edit`; `docs/DEBT.md` sinh lại bằng chính ledger.

## Đã làm
- `DebtParser` chỉ quét đuôi mã nguồn/cấu hình có comment + tên file không đuôi; loại `.agents/.claude/.codex/.kilo/docs/tasks` và giữ `tests/scripts` trong exclude.
- Thẻ đủ 3 trường nhận mọi vị trí; thẻ dị dạng chỉ nhận ở đầu dòng comment.
- Sửa header `agent_core/debt/ledger.py`; sinh lại `docs/DEBT.md` = 0 mục.
- Thêm 8 test hồi quy (docs/README/generated bị bỏ, prose không phải nợ, dị dạng đầu dòng vs inline, header, idempotence).
- Toàn bộ suite: 224 test pass; CSO/board/hard/card-audit exit 0.

## Lưu ý cho agent sau
- **Bẫy số liệu**: chính card T-04 chứa chuỗi `# debt:` nên harvest tăng theo nội dung card. Khi đo phải loại `tasks/E1-nen-tang/T-04.md` hoặc chốt số 109; đừng dùng con số "đo gồm card".
- **Trade-off đã chốt**: thẻ dị dạng inline (`x = 1  # debt: hack`) bị bỏ qua; chỉ thẻ đủ 3 trường mới bắt inline. Muốn bắt lại phải thiết kế thêm luật, đừng nới regex tràn lan.
- **Giới hạn**: `scripts/` và `tests/` vẫn bị loại khỏi phép quét; `.cmd/.bat` chưa hỗ trợ comment `REM/::`; `.json` không có comment nên loại. Ghi thành nợ sau nếu cần.
- **DEBT.md**: không được để ledger quét chính nó; test idempotence dùng target tạm, không ghi đè file thật.
- **Trạng thái git**: chưa có nhánh `feature/04-debt-ledger-noise`; thay đổi đang ở working tree `main`. Người dùng tạo nhánh rồi commit theo mục 7 (đã tách commit test).

## Việc dở dang hoặc nợ kỹ thuật
- Chưa hỗ trợ comment `REM`/`::` của `.cmd/.bat`; chưa quét nợ trong `scripts/`.
- Diff Review đã APPROVED; QA đã PASS (11/11 test_debt, 224/224 suite, harvest 0); chờ người dùng tạo nhánh và commit.

## Ảnh hưởng đến task khác
- `debt-hunter` giờ chạy trên sổ sạch; mọi thẻ nợ thật phải nằm trong file mã nguồn được whitelist.
- Không đổi API công khai của `DebtParser`/`DebtLedger`; `scan_directory` vẫn nhận `exclude_dirs` nhưng luôn cộng thêm baseline.

## Đề xuất cập nhật quy ước hoặc tài liệu
- Ghi rõ cú pháp thẻ nợ và giới hạn quét vào `agents/roles/debt-hunter.md` (cần người dùng duyệt vì thuộc `agents/`).
