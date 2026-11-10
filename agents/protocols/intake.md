# Quy trình nhập tài liệu (doc, xlsx, pdf, ảnh)

Chuyển sang md **không chuẩn hóa được 100%**. Quy trình này có mục đích là không để mất yêu cầu mà không ai biết.

## Các bước

1. **Lưu bản gốc**: đặt nguyên vẹn vào `docs/source/` (hoặc `doc/features/<UC>/` theo cấu trúc dự án). Khi có **bản mới thay thế bản cũ**, thực hiện đúng `agents/protocols/source-precedence.md` §2: đẩy bản cũ vào `archive/` (hoặc gắn đầu file `STATUS: SUPERSEDED BY: ...`), cập nhật `Active Source` và chạy `scripts/doc-preflight.py` kiểm `mtime` trước khi code.
2. **Chuyển đổi tự động**: Chạy kịch bản chuẩn của hệ thống (hỗ trợ cả Windows, macOS, Linux):
   - **Trên Windows (PowerShell)**:
     - Chuyển toàn bộ: `powershell -File scripts/convert-docs.ps1 -All`
     - Chuyển kèm đọc ảnh (LLM Vision OCR): `powershell -File scripts/convert-docs.ps1 -All -EnableOcr`
   - **Trên Linux / macOS / WSL (Bash)**:
     - Chuyển toàn bộ: `./scripts/convert-docs.sh --all`
     - Chuyển kèm đọc ảnh (LLM Vision OCR): `./scripts/convert-docs.sh --all --enable-ocr`
   - **Hoặc chạy trực tiếp qua Python**:
     - `python scripts/convert-docs.py --all [--enable-ocr]`
   - DOCX, XLSX, PPTX, PDF, HTML, CSV: MarkItDown tự động bóc tách heading, list, table.
   - Ảnh, biểu đồ, PDF scan: LLM Vision OCR trích xuất nội dung văn bản, bảng và luồng nghiệp vụ thành khối `*[Image OCR] ... [End OCR]*`.
3. **Báo cáo đối chiếu** (`docs/converted/<tên>.report.md`): Sinh tự động, ghi nhận dung lượng, phương thức xử lý, cảnh báo bảng biểu hoặc ảnh không đọc được.
4. **Đối chiếu**: BA mở bản gốc, so với bản md ở các chỗ dễ lỗi (bảng, số liệu, công thức).
5. **Phản biện đề bài (Challenger Gate - theo `agents/protocols/challenger.md`)**:
   - Bóc tách bản chất bài toán vs giải pháp đề xuất (XY Problem).
   - Đánh giá bán kính tác động (Blast Radius): hiệu năng, rủi ro bảo mật, nợ kỹ thuật và chi phí token.
   - Cắt tỉa phạm vi (Scope-Cut): loại bỏ chi tiết rườm rà, tập trung đòn bẩy 80/20.
   - Trình bày **Ma trận 3 Phương án** (Lean MVP vs Cân bằng vs Toàn diện) kèm đề xuất cụ thể (`➡️ Đề xuất của AI: ...`).
6. **Rút yêu cầu**: `docs/requirements/requirements.md`, mỗi dòng một yêu cầu R-001, R-002... kèm nguồn.
7. **Không chắc / mâu thuẫn**: liệt kê riêng, mỗi mục một câu hỏi cụ thể theo skill `grilling`.
8. **Người dùng duyệt**: Người dùng lựa chọn phương án đối trọng, duyệt danh sách R-xxx và trả lời các mục không chắc. Chưa duyệt thì chưa ai bắt tay làm.
9. **Truy vết**: mỗi task card ghi `requirements: [R-xxx]`.

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
