> Task: T-13 · Epic: E2 · Vai: architect

# ADR-13: Cơ chế phê duyệt bằng file và phân định thẩm quyền người - AI

- **Trạng thái**: Proposed
- **Ngày**: 2026-10-28
- **Tác giả**: Architect

---

## 1. Ngữ cảnh & Vấn đề

Trong quy trình phát triển phần mềm có AI hỗ trợ (AI in SDLC), ranh giới giữa tư vấn kỹ thuật của mô hình ngôn ngữ và quyết định pháp lý/nghiệp vụ của con người thường xuyên bị xóa nhòa. Thực tế ghi nhận các rủi ro:
1. Agent AI tự đóng dấu phê duyệt thay người dùng (như trường hợp reviewer-AI tự ký `Plan Approved by reviewer` trong T-08).
2. Phê duyệt qua kênh chat ("ok", "làm đi", "duyệt") thiếu tính truy vết và không neo được vào trạng thái cụ thể của mã nguồn hay tài liệu.
3. Trong `AGENTS.md` §16 có quy định đóng dấu `[x] Plan Approved by <vai>`. Điều này gây hiểu lầm rằng AI đóng vai trò thẩm định có quyền cho phép triển khai code mà không cần người dùng duyệt.

---

## 2. Các phương án xem xét (Ma trận 3 Phương án)

| Tiêu chí | Phương án 1: Dấu trong file (Đề xuất) | Phương án 2: Git commit có chữ ký GPG | Phương án 3: Hệ thống Web/Issue ngoài (Jira/GitHub PR) |
|---|---|---|---|
| **Cơ chế** | Ghi dòng text có cấu trúc kèm tên, ngày, digest vào file Markdown | Con người commit dấu duyệt bằng khóa GPG bí mật | Duyệt qua nút bấm trên UI hệ thống quản lý bên ngoài |
| **Ưu điểm** | Đơn giản, hoàn toàn cục bộ (offline), không thêm phụ thuộc, tích hợp ngay vào task card | Chống giả mạo tuyệt đối về mật mã học | Ranh giới trust boundary tách biệt hoàn toàn khỏi AI |
| **Nhược điểm** | AI có quyền ghi file nên về lý thuyết có thể mạo danh (cần tool đối soát) | Phức tạp, phụ thuộc cấu hình GPG cá nhân, khó tự động hóa | Cần kết nối mạng, thêm dependency bên ngoài, chậm |
| **Độ phù hợp** | Cao nhất cho giai đoạn pilot | Phù hợp khi lên CI/CD production | Phù hợp dự án enterprise quy mô lớn |

---

## 3. Quyết định đề xuất (Khuyến nghị)

- Chọn **Phương án 1: Dấu duyệt trong file** làm chuẩn thực thi cốt lõi.
- **Phương án hiệp thương xử lý mâu thuẫn AGENTS.md §16**:
  - Giữ chuỗi `[x] Plan Approved by <vai>` đóng vai trò **nhận xét tư vấn (Reviewer Verdict)**.
  - Thêm dòng bắt buộc `- [x] **Người dùng duyệt phạm vi bằng file**: <tên> · <ngày>` làm **điều kiện tiên quyết (Hard Gate)**.
  - Đề xuất cập nhật câu chữ trong `AGENTS.md` và các vai trò sẽ được tổng hợp bàn giao cho người dùng qua task **T-16** (AI không tự ý sửa `AGENTS.md`).

---

## 4. Rủi ro & Biện pháp giảm thiểu

- **Rủi ro**: AI mạo danh người dùng tự ghi dòng duyệt.
  - **Giảm thiểu**: Cổng `claim_task` (T-23) và `merge-gate` sẽ kiểm tra chéo commit log/git blame; quy định xử phạt vi phạm luật cứng dừng phiên ngay lập tức nếu AI tự tiện tích ô người dùng.
- **Rủi ro**: Tài liệu thay đổi nhưng dấu duyệt cũ vẫn giữ nguyên (stale approval).
  - **Giảm thiểu**: Đính kèm digest ngắn của nội dung tại thời điểm duyệt. Nếu diff không khớp digest, dấu duyệt tự động bị coi là hết hiệu lực.
