> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục I

# Quy trình soạn thảo Markdown & Xuất Excel SRS_FDD — Phần 2: Lệnh Xuất & Ánh Xạ Sheet

## I. Xuất sang Excel theo mẫu SRS_FDD (chốt 18/10/2026)

File md là nguồn thật; Excel là bản xuất để nộp hoặc nhập vào bộ tài liệu của công ty. Không sửa tay file Excel (bị ghi đè khi xuất lại).

Lệnh (từ gốc workspace): `python3 scripts/srs_md_to_xlsx.py UC-01 UC-02` ghi `doc/features/SRS_FDD_UC-01_UC-02.xlsx` (hoặc `doc/features/<UC>/SRS_FDD_<UC>.xlsx`).

| Sheet | Lấy từ |
|---|---|
| `NhatKyThayDoi` | Mục 0 của đặc tả |
| `PJT_Definition` | Bảng đầu của đặc tả (mã, phạm vi, nguồn, trạng thái) |
| `DauMucTaiLieuCanLam` | Mục 1 |
| `Component_Detail_Design` | Mục 2, 3 (yêu cầu, luồng nghiệp vụ, màn hình), kèm ảnh |
| `WBS_Planning` | Phạm vi và mục 4 của file đối chiếu |
| `Actors_Peronas` | Mục 2 |
| `Function_RTM` | Mục 5 của file đối chiếu |
| `Functions_Services_Detail_Desig` | Mục 4 đến 9 của đặc tả, và toàn bộ thiết kế kỹ thuật (mục "6. Công nghệ và cài đặt"), kèm ảnh |
| `TDD-TestScenario`, `TDD_TestCases` | Mục 13, 14 (bước và kết quả gộp theo mã test case) |
| `Theo_Man_Hinh` | Toàn bộ `UC-01-02-theo-man-hinh.md` (sheet thêm ngoài mẫu); happy case của từng màn cũng được gộp vào `TDD-TestScenario`, `TDD_TestCases` |
| `Rui_Ro`, `Cau_Hoi_Mo` | Mục 15, 16 (sheet thêm ngoài mẫu) |

Quy ước để xuất đúng: giữ tiêu đề mục và tên cột bảng như các file mẫu `UC-01`; mỗi bảng có hàng tiêu đề; ảnh dùng `![](hinh/...png)`. File Excel dựng lại theo tên sheet và cột của mẫu, không phải bản sao ô-theo-ô của mẫu (mẫu có nhiều ô gộp và hình vẽ). Cột ước lượng, người làm, ngày trong WBS và các cột phê duyệt để trống cho người điền.
