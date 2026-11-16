# Chuẩn viết tài liệu thiết kế theo mẫu SRS_FDD (File Lõi)

> **Loại: tham khảo.** Nguồn gdt-workspace, bổ sung cho dự án dùng mẫu Excel SRS_FDD (`protocols/srs-workflow.md`).

Áp dụng khi viết tài liệu thiết kế theo mẫu `SRS_FDD_Template-v3.0.xlsx` hoặc mẫu Copilot.

## 1. Bảng Chỉ Dẫn "Làm Việc X Đọc File Y"

| Cần làm gì | Đọc file |
|---|---|
| **Văn phong**: Câu "Hệ thống phải...", A/C "Khi... thì...", từ ngữ chuẩn | [`srs-van-phong-ky-thuat.md`](srs-van-phong-ky-thuat.md) |
| **Sheet tổng quan**: `NhatKyThayDoi`, `PJT_Definition`, `Component_Detail_Design` | [`srs-fdd-tung-sheet-1.md`](srs-fdd-tung-sheet-1.md) |
| **Sheet chức năng**: Use-Case/US, UI, API endpoint, Diagram, NFR | [`srs-fdd-tung-sheet-2.md`](srs-fdd-tung-sheet-2.md) |
| **Kế hoạch & Test**: `WBS_Planning`, `Function_RTM`, Actor, Test TDD | [`srs-fdd-tung-sheet-3.md`](srs-fdd-tung-sheet-3.md) |
| **Khung 3 file md**: Cấu trúc `doc/features/<UC>/` (`<UC>.md`, `thiet-ke`, `doi-chieu`) | [`srs-quy-trinh-md-va-xuat-excel-1.md`](srs-quy-trinh-md-va-xuat-excel-1.md) |
| **Lệnh xuất Excel**: Chạy `srs_md_to_xlsx.py` và ánh xạ sheet | [`srs-quy-trinh-md-va-xuat-excel-2.md`](srs-quy-trinh-md-va-xuat-excel-2.md) |
| **Theo màn & Hỏi**: `MAN-<nn>`, ERD theo màn, file câu hỏi BA/Kế toán | [`srs-quy-trinh-md-va-xuat-excel-3.md`](srs-quy-trinh-md-va-xuat-excel-3.md) |
| **Sơ đồ 1..7**: Chuẩn sơ đồ, dòng neo kiến trúc & hạ tầng | [`srs-so-do-va-vi-tri-neo-1.md`](srs-so-do-va-vi-tri-neo-1.md) |
| **Sơ đồ 8..13**: Dòng neo Use Case, cấm ghi đè ô công thức | [`srs-so-do-va-vi-tri-neo-2.md`](srs-so-do-va-vi-tri-neo-2.md) |
| **Đóng gói 11 sheet**: Chuẩn Copilot, cổng DoR nhận task, DoD bàn giao | [`srs-dor-dod-va-dong-goi.md`](srs-dor-dod-va-dong-goi.md) |
| **Skill áp dụng**: `grill-me`, `domain-modeling`, `api-design`, `archify`... | [`srs-skill-ap-dung.md`](srs-skill-ap-dung.md) |

## 2. Rút Gọn Mục A: Nguyên Tắc Bắt Buộc
1. **May đo:** Mẫu 11 sheet cho Enterprise; dự án nhỏ dùng Markdown theo `srs-workflow.md`.
2. **Lưu cục bộ:** Ghi file trong `doc/features/<UC>/`, không ghi Google Docs/Sheets.
3. **Không bịa:** API, bảng DB phải từ code thật. Chưa rõ ghi `(chưa xác nhận — hỏi: …)`.
4. **Duyệt bằng file:** Ô "Người duyệt/Xác nhận" để trống cho người điền bằng file.
5. **Định danh:** Gói là `UC-<nn>`, Story con là `US_<nn>_<mm>`.
6. **Đơn nhiệm:** Mỗi lần làm 1 task; ghi nhật ký `NhatKyThayDoi`.
7. **Bỏ chữ mẫu:** Thay text mẫu (News System, Lorem ipsum) bằng dữ liệu thật.
8. **Tư duy BA:** Đọc code thật, bao phủ ca biên, phản biện trung thực.

## 3. Mục C: Checklist Trước Khi Bàn Giao
- [ ] Có ID chức năng ở: Use-case/US, WBS, RTM, TestCases.
- [ ] A/C đánh số, mỗi A/C có ít nhất 1 test case.
- [ ] Story đã đánh 4 tiêu chí; cần 2 nhóm thao tác hoặc vượt ngưỡng thì tách (`danh-gia-user-story.md`).
- [ ] API, bảng DB, mã trạng thái đối chiếu khớp code thật.
- [ ] Không còn chữ mẫu rác ("News System", "Lorem ipsum", NFR mẫu).
- [ ] Luồng ngoại lệ & lỗi có đủ; NFR đối chiếu thực tế.
- [ ] `NhatKyThayDoi` đã ghi; ô duyệt để trống cho người.
- [ ] Chưa tự đánh Pass / Hoàn thành / Approved.
- [ ] Điểm chưa rõ liệt kê tại `doc/features/<UC>/cau-hoi-ke-toan.md`.
