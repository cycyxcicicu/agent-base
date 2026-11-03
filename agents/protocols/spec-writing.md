> Task: T-14 · Epic: E2 · Vai: writer

# Tiêu chuẩn viết tài liệu đặc tả (Specification Writing Protocol)

Quy chuẩn văn phong và cấu trúc tài liệu đặc tả giúp đảm bảo tính rõ ràng, khách quan và phục vụ làm việc phối hợp giữa con người và AI.

---

## 1. Tám nguyên tắc văn phong đặc tả chuẩn

1. **Mệnh lệnh khẳng định chuẩn mực**: Dùng cấu trúc *"Hệ thống phải [hành động] khi [điều kiện]"*. Tránh dùng giọng văn tường thuật, phỏng đoán hoặc kể chuyện quá khứ.
2. **Không trộn lẫn trạng thái triển khai vào đặc tả**: Đặc tả viết về mục tiêu hệ thống PHẢI đạt được. Tuyệt đối không ghi các câu như "module này đã code xong", "hàm này hiện đang lệch", "chưa kịp làm".
3. **Tiêu chí nghiệm thu (A/C) chuẩn hóa**: Viết theo mẫu điều kiện hành vi rõ ràng: *"Khi [ngữ cảnh/hành động] thì [kết quả mong đợi cụ thể]"*.
4. **Dồn toàn bộ câu hỏi mở về cuối**: Mọi điểm chưa rõ, điểm nghi vấn hay giả định chưa kiểm chứng phải gom vào mục cuối *"Câu hỏi mở cho BA/Khách hàng"*, không để rải rác giữa chừng.
5. **Nêu CÁI GÌ, không gò ép NHƯ THẾ NÀO**: Đặc tả nghiệp vụ tập trung vào giá trị và quy tắc, không nhồi nhét chi tiết thư viện, framework hay thuật toán cụ thể.
6. **Tuân thủ Từ điển miền (Domain Glossary)**: Dùng đúng thuật ngữ thống nhất trong `docs/requirements/glossary.md`. Không tự bịa từ đồng nghĩa gây mơ hồ.
7. **Lượng hóa tuyệt đối, tránh tính từ cảm tính**: Cấm dùng từ ngữ chung chung ("phản hồi nhanh", "giao diện trực quan", "bảo mật cao"). Phải lượng hóa ("phản hồi trong < 200ms", "đạt chuẩn tương phản WCAG 2.1 AA").
8. **Tách biệt Quy tắc nghiệp vụ (BR) và Ca sử dụng (Use Case)**: Quy tắc nghiệp vụ tồn tại độc lập với giao diện; Use Case mô tả luồng thao tác cụ thể qua các bước.
9. **Tư duy BA thực chiến — Suy diễn trường thực tế & Bao phủ Edge Cases**:
   - Đặc tả không bao giờ chỉ dừng lại ở kịch bản lý tưởng (Happy Path). BA/Agent phải đặt mình vào vị trí người vận hành đời thực để suy diễn các trường hợp biên.
   - *Ví dụ điển hình (Chia đơn):* Chia đều cho nhân viên $\rightarrow$ nhân viên làm sáng, chiều nghỉ đột xuất $\rightarrow$ đặc tả phải có cơ chế: thu hồi đơn chưa xử lý, chia lại cho nhân viên đang active, cơ chế khóa đơn (Locking) chống xung đột khi đang thao tác, và ghi vết lịch sử kiểm toán (Audit Trail).
10. **Bám sát hiện trạng mã nguồn (Code Reality)**:
    - Nếu hệ thống đã có code chạy, trước khi viết đặc tả/FDD bắt buộc phải đọc controller, service, repository, enum để xác định: Cái gì đã có, cái gì chưa có, cái gì bị ảnh hưởng. Tuyệt đối không bịa đặt hoặc suy diễn tách rời mã nguồn.
11. **Phản biện trung thực & Độc lập kỹ thuật (Anti-Flattery)**:
    - Kỹ sư/Agent không được xu nịnh, vuốt đuôi hoặc chiều theo phương án chưa tối ưu của người dùng nếu nó dẫn đến nợ kỹ thuật hoặc vỡ kiến trúc. Khi người dùng nói sai hoặc đưa giải pháp rủi ro, bắt buộc phải phản biện dứt khoát kèm 3 phương án lựa chọn, lý do và cách khắc phục rủi ro.

---

## 2. Bộ ba file chuẩn cho mỗi tính năng (Tách biệt mối quan tâm)

Thư mục và tên file do `agents/protocols/srs-workflow.md` quy định (`Thư mục SRS` đọc từ `PROJECT.md`; tài liệu của dự án nằm trong dự án, không nằm trong khung). File này chỉ giữ phần văn phong.

Mỗi phân hệ hoặc chức năng phức tạp được tách thành 3 tài liệu độc lập:

| File | Đường dẫn quy ước | Mục đích & Nội dung |
|---|---|---|
| **Đặc tả nghiệp vụ** | `<Thư mục SRS>/UC-<nn>-<loại>-<mô tả>.md` | Hệ thống PHẢI làm gì (User Stories, BR, A/C, kịch bản tương tác). |
| **Thiết kế kỹ thuật** | `<Thư mục SRS>/UC-<nn>-<loại>-<mô tả>-thiet-ke.md` (quyết định lớn: `<Thư mục tài liệu>/adr/`) | Hệ thống ĐƯỢC XÂY NHƯ THẾ NÀO (Data schema, API contracts, sequence diagram, ADR). |
| **Đối chiếu hiện trạng** | `<Thư mục SRS>/UC-<nn>-<loại>-<mô tả>-doi-chieu.md` | Hiện trạng code THẬT SO VỚI ĐẶC TẢ (chênh lệch, nợ kỹ thuật, kế hoạch bù đắp). |

---

## 3. Ví dụ minh họa Đúng vs Sai

| Tiêu chí | ❌ SAI (Tường thuật, mơ hồ, sai chỗ) | ✅ ĐÚNG (Khẳng định, lượng hóa, đúng chuẩn) |
|---|---|---|
| **Văn phong** | *"Hôm trước chúng ta đã bàn về việc đăng nhập, hiện tại dev đang làm dở chức năng khóa tài khoản nếu bấm sai nhiều lần."* | *"Hệ thống phải tự động khóa tài khoản tạm thời 15 phút khi người dùng nhập sai mật khẩu quá 5 lần liên tiếp."* |
| **Tiêu chí A/C** | *"Hệ thống xử lý file đính kèm phải mượt và không bị lỗi."* | *"Khi người dùng tải lên tệp PDF có kích thước <= 10MB, hệ thống phải hoàn tất lưu trữ và hiển thị preview trong vòng 2 giây."* |
| **Trạng thái** | *"Tính năng xuất Excel đã hoàn thiện ở commit trước nhưng chưa viết test."* | *"Hệ thống phải xuất danh sách đơn hàng ra tệp định dạng .xlsx với đầy đủ 8 cột nghiệp vụ chuẩn."* |
