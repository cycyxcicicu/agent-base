# Mẫu tài liệu

Khi cần viết một loại tài liệu, mở đúng mẫu dưới đây rồi bám cấu trúc của nó. Không đọc cả thư mục.

| Cần viết | Mẫu | Ghi chú |
|---|---|---|
| Đặc tả một chức năng (md) | `srs-chuc-nang/srs-chuc-nang-template.md` | Khung chính cho giai đoạn thiết kế. Văn phong: `agents/knowledge/srs/srs-fdd-writing-standard.md` |
| Thiết kế kỹ thuật một chức năng (lớp, hàm, luồng) | `srs-chuc-nang/thiet-ke-ky-thuat-template.md` | Cặp với đặc tả ở trên |
| Đổ đặc tả vào Excel SRS_FDD | `srs-fdd/huong-dan-tung-sheet.md` | Ý nghĩa từng sheet, từng cột trong mẫu v3.0 |
| Chọn và vẽ sơ đồ theo mẫu SRS_FDD | `srs-fdd/so-do-trong-mau.md` | Loại sơ đồ trong mẫu, dùng khi nào |
| Học cách trình bày từ bản đã điền thật | `srs-fdd/hoc-tu-mau-copilot.md` | Khuôn mô tả API, sheet màn hình, 13 hình |
| SRS dạng Word của công ty | `srs-word/SRS-He-thong-quan-ly.md` | Bản chuyển sang md, chỉ có chữ, bỏ 60 ảnh |
| Báo cáo kiểm thử | `test-report/Template_TestReport.xlsx`, `test-report/Info.md` | `Info.md` là tab Info đã chuyển sang md |
| File import TestLink (XML) | `testlink/testlink-import-mau.xml` | Mẫu cấu trúc; nội dung là bộ case màn hình Theo dõi hành trình đơn của gdt. Để `internalid=""` thì TestLink tạo case mới |

## Bản gốc (xlsx, docx)

Dùng khi cần xuất Excel hoặc Word đúng khuôn. Đọc hướng dẫn md ở bảng trên trước, chỉ mở bản gốc khi thật sự cần.

| File | Kích thước | Là gì |
|---|---|---|
| `srs-fdd/SRS_FDD_Template-v3.0.xlsx` | khoảng 14 MB | mẫu gốc SRS_FDD v3.0 |
| `srs-fdd/_SRS_FDD_AI-Agent-Copilot.xlsx` | khoảng 4,6 MB | bản đã điền thật để học cách trình bày |
| `srs-word/SRS-He-thong-quan-ly.docx` | khoảng 3 MB | mẫu SRS dạng Word |
| `test-report/Template_TestReport.xlsx` | khoảng 1 MB | mẫu báo cáo kiểm thử |

Các file md trong `srs-fdd/` còn nhắc đường dẫn `doc/quy-trinh/template/...`: đó là vị trí cũ trong dự án gdt-workspace, bản trong thư mục này là cùng nội dung.
