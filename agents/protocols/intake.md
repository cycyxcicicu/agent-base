# Quy trình nhập tài liệu (doc, xlsx, pdf, ảnh)

Chuyển sang md **không chuẩn hóa được 100%**. Quy trình này có mục đích là không để mất yêu cầu mà không ai biết.

## Các bước

1. **Lưu bản gốc**: đặt nguyên vẹn vào `docs/source/`. Không sửa, không đổi tên, không xóa.
2. **Chuyển đổi**: sang md vào `docs/converted/<tên>.md`.
   - DOCX, XLSX, PPTX: MarkItDown thường đủ.
   - PDF nhiều bảng, công thức, nhiều cột, hoặc PDF dạng scan: Docling (có OCR).
   - Ảnh: mô tả lại bằng chữ, giữ ảnh gốc.
3. **Báo cáo chuyển đổi** (`docs/converted/<tên>.report.md`): trang rỗng, bảng vỡ, công thức mất, ô gộp, biểu đồ, ảnh không đọc được.
4. **Đối chiếu**: BA mở bản gốc, so với bản md ở các chỗ dễ lỗi (bảng, số liệu, công thức).
5. **Rút yêu cầu**: `docs/requirements/requirements.md`, mỗi dòng một yêu cầu R-001, R-002... kèm nguồn.
6. **Không chắc / mâu thuẫn**: liệt kê riêng, mỗi mục một câu hỏi cụ thể cho người dùng.
7. **Người dùng duyệt** danh sách R-xxx và trả lời các mục không chắc. Chưa duyệt thì chưa ai bắt tay làm.
8. **Truy vết**: mỗi task card ghi `requirements: [R-xxx]`.

## Lưu ý theo loại tệp

| Loại | Dễ mất | Cách xử lý |
|---|---|---|
| XLSX | công thức, ô gộp, nhiều sheet, biểu đồ | kiểm tra thủ công với bản gốc, ghi rõ trong báo cáo |
| PDF thường | bảng, nhiều cột, công thức | dùng Docling, đối chiếu bảng quan trọng |
| PDF scan | toàn bộ chữ nếu không có OCR | dùng công cụ có OCR, kiểm tra số liệu |
| Ảnh | chữ nhỏ, số, ảnh nghiêng, chi tiết tinh tế | mô tả bằng chữ, người dùng xác nhận, số liệu quan trọng nên có bản văn bản |

## Mẫu dòng yêu cầu

```
R-003 | Người dùng đăng nhập bằng email và mật khẩu | nguồn: spec.pdf, trang 4, mục 2.1 | mức: bắt buộc
```
