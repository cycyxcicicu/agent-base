> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục B (sheet Functions_Services_Detail_Desig)

# Chuẩn viết từng sheet SRS_FDD — Phần 2: Chi tiết Chức năng & Dịch vụ

### `Functions_Services_Detail_Desig` — mỗi chức năng một khối (sheet quan trọng nhất)
1. **Use-case hoặc User Story** (chọn một, thống nhất trong cả tài liệu):
   - Use-case: `Tên`, `Mô tả`, tác nhân chính/ phụ, `Tiền điều kiện`, **luồng chính/ thay thế/ ngoại lệ — mỗi bước một dòng đánh số `1.1, 1.2…`**, `Điều kiện sau khi hoàn thành`. Luồng ngoại lệ **bắt buộc** nêu: lỗi hệ thống, hết phiên, dữ liệu sai.
   - User Story: `As a [vai trò], I want to [mục tiêu] so that [lợi ích]` + **A/C đánh số**, mỗi A/C **kiểm chứng được** (có điều kiện, kết quả quan sát). Lấy A/C từ SRS (`AC-xx`) — không tự thêm A/C mới mà không báo.
   - **[ĐỀ XUẤT]** thêm `Story Points`, **DoR** (UI/UX, tài liệu kỹ thuật, dữ liệu mẫu, phụ thuộc) và **DoD** (Code review, Testing, Acceptance, Performance, Documentation).
2. **Giao diện:** ảnh/ ID màn hình + bảng **Business Rules** từng nút/ vùng/ ô (bắt buộc, định dạng, ràng buộc). Cột/ nhãn lấy từ `06-cot-hien-thi`, trạng thái từ `05-process-status`.
3. **Service/ API:** với mỗi endpoint: `PATHNAME` (đường dẫn thật `/api/v1/…`), `Method`, bảng param (`No, Param, Type, Mandatory, Sample value, Description, Remark`), `REQUEST SAMPLE` (JSON thật, có lệnh `curl` thử nếu chạy được), `RESPONSE FIELD`, `RESPONSE SAMPLE`. **Lấy từ controller/ DTO thật** (`presentation.api.*`), không suy đoán. Ghi rõ mã lỗi/ thông báo.
4. **Diagram:** Sequence (hoặc nhúng vào use-case), Activity nếu có rẽ nhánh, ERD/ class: ghi **tên bảng/ entity thật** (`core.entity`). Dữ liệu không có ảnh → mô tả bằng bảng/ danh sách.
5. **NFR:** bảng `Yêu cầu/ Mô tả/ Giải pháp` — lấy từ SRS mục II **nhưng đối chiếu hệ thống thật** (mục II của SRS GDT có vẻ từ tài liệu tuyển dụng, **không dùng nguyên văn**).
6. **Đánh giá tác động:** liệt kê **file/ module thật sẽ đổi** (FE, BE, Liquibase, config), đánh dấu Source/ Library/ Config/ Assets/ Infra: Có/ Không thay đổi, kèm rủi ro hồi quy.
7. Công nghệ & gói cài: chỉ ghi phần **thay đổi** so với `Component_Detail_Design`.
