# Quản lý thay đổi yêu cầu (Change Request, CR)

Áp dụng khi **yêu cầu, thiết kế hoặc phạm vi đã được duyệt mà phải đổi**. Nguồn: quy trình công ty (`agents/knowledge/quy-trinh/quy-trinh-cong-ty.md` mục 3) và `agents/knowledge/quy-trinh/baccm-yeu-cau-va-cr.md` mục IV. Không áp dụng cho sửa lỗi chính tả hay làm rõ chữ nghĩa không đổi hành vi.

## Khi nào phải lập CR

- Sửa A/C, R-xxx, đặc tả hoặc thiết kế đã `Approved` (xem `approval.md`).
- Thêm hoặc bớt chức năng so với task card đã duyệt.
- Cần sửa file ngoài `scope_edit` của card (thay vì tự sửa, xem `AGENTS.md` mục 4).

## Các bước

1. **Lập phiếu** `docs/changes/CR-<số>.md` (tạo thư mục khi cần), trạng thái `Draft`, ghi: người đề xuất, lý do, nguyên văn yêu cầu cũ và mới, tài liệu và task bị ảnh hưởng.
2. **Đánh giá tác động** (analyst hoặc architect): tài liệu phải sửa, task phải làm lại, test case phải đổi, dòng RTM, ước lượng thêm, rủi ro. Không sửa gì trước khi có kết luận.
3. **CCB duyệt** (Hội đồng Kiểm soát Thay đổi, là con người): thành phần đầy đủ gồm Product Owner, Tech Lead, PM, QA Lead; dự án nhỏ thì chỉ người dùng. Ghi một trong ba quyết định kèm ngày vào phiếu: `Approved` (đưa vào sprint kế tiếp), `Rejected` (ghi lý do, lưu hồ sơ), `Deferred` (hoãn sang backlog). AI không tự ghi quyết định.
4. **Cập nhật**: sau khi `Approved`, sửa tài liệu, task card, test case theo danh sách ở bước 2; cập nhật RTM bằng `python scripts/rtm.py`; phân rã task mới vào WBS. Ghi mã CR vào card và vào ghi chú bàn giao.
5. **Đóng phiếu**: đủ mọi mục ở bước 4, trạng thái `Closed`.

## Mẫu phiếu

```markdown
# CR-<số>: <tên>
Trạng thái: Draft | Approved | Rejected | Deferred | Closed        Ngày: YYYY-MM-DD
Người đề xuất:
## Thay đổi
Cũ: ...    Mới: ...    Lý do: ...
## Tác động
- Tài liệu: ...   - Task: ...   - Test case: ...   - RTM: ...   - Ước lượng thêm: ...
## Quyết định
(người dùng ghi, kèm ngày)
```
