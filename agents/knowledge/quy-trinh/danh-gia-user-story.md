# Đánh giá User Story theo 4 tiêu chí (Độ đủ & Khi nào tách)

> **Loại: tham khảo.** Rút từ bảng "Đặc điểm" tab `gid=533583442` (Sheet `Planning`). Khác `AGENTS.md` thì theo protocols (`source-precedence.md`).
> **Không tự gán điểm:** Sheet tính điểm bằng công thức riêng. Tài liệu chỉ chuẩn hóa tiêu chí và ngưỡng tách.

## 1. Nguyên tắc cốt lõi

- **1 dòng phân việc = 1 story.** Đánh đủ 4 tiêu chí: **phân loại + giải thích**.
- **Thiếu giải thích là chưa đủ:** Chỉ chọn loại mà không giải thích cụ thể là chưa xong.
- Giải thích phải cụ thể: tên màn hình, trường dữ liệu, ràng buộc thực, không nói chung chung.

## 2. Bốn tiêu chí đánh giá

### 2.1 Loại tương tác (chọn 1)
- **Giao diện rõ ràng:** UI/hành vi cố định, schema API chuẩn, hiển thị đúng API. *Giải thích:* Nêu màn hình, UI hoặc API.
- **Giao diện động:** UI đổi theo dữ liệu/thao tác (thêm node, sắp xếp). *Giải thích:* Nêu phần tử đổi và điều kiện nhận.
- **Tương tác với người:** Hệ thống chờ phản hồi/xác nhận. *Giải thích:* Nêu điểm chờ, lựa chọn, xử lý khi không phản hồi.

### 2.2 Quy tắc nghiệp vụ (chọn `1`, `1-3` hoặc `> 3`)
- Quy tắc là ràng buộc kiểm chứng được (vd: "tối đa 10 ảnh", "key hết hạn"). Đếm mỗi ràng buộc là 1 quy tắc.
- **Giải thích:** Liệt kê tên từng quy tắc (khớp mức chọn). Mỗi quy tắc có ít nhất 1 A/C ("Khi ... thì ...").

### 2.3 Thực thể (chọn `1`, `1-3` hoặc `> 3`)
- Thực thể là đối tượng dữ liệu story đọc/ghi (vd: Node, Workflow, Execution, Model, Key).
- **Giải thích:** Liệt kê tên từng thực thể (mức `> 3` nêu $\ge 4$ tên, `1-3` nêu 1-3 tên). Phải có trong data model, API, RTM.

### 2.4 Loại thao tác dữ liệu (chọn duy nhất 1 nhóm)
- **Tạo:** Tạo mới dữ liệu/bản ghi/file. *Giải thích:* Nêu tạo gì.
- **Cập nhật:** Sửa dữ liệu sẵn có. *Giải thích:* Nêu sửa trường nào.
- **Đọc, Xóa:** Chỉ đọc/hiển thị hoặc xóa (nguồn gộp Đọc và Xóa). *Giải thích:* Nêu xem hay xóa gì.

> **Quy tắc cứng:** Mỗi story chỉ thuộc 1 nhóm thao tác. Cần 2 nhóm (vừa tạo vừa sửa) thì **bắt buộc tách story**.

## 3. Khi nào tách story

Tách story khi gặp một trong các dấu hiệu:
1. **Khác nhóm thao tác:** Vừa Tạo vừa Sửa hoặc vừa Đọc vừa Tạo.
2. **Quy tắc > 3 hoặc Thực thể > 3:** Cân nhắc tách theo luồng độc lập (vd: Login tách form, token, SSO, quên mật khẩu).
3. **Phạm vi quá rộng:** Giải thích quá dài, vượt quá mục tiêu người dùng đơn nhất ("Tôi muốn ... để ...").

*Sau khi tách:* Đánh giá lại 4 tiêu chí cho từng story mới. Mỗi story chẻ thành task kỹ thuật WBS $\le 1$ ngày công.

## 4. Hai mốc "đủ" cần phân biệt

- **Đủ để định nghĩa (Ready for Dev):** 4 tiêu chí đều có phân loại và giải thích cụ thể.
- **Đủ để xong (DoD):** 8 tiêu chí chuẩn:
  1. Code đủ module, UI; commit chạy tốt trên dev.
  2. Review chéo đạt; Unit test pass 100%.
  3. Deploy & pass system/integration test; tài liệu cấu hình/deploy đủ.
  4. Cập nhật SRS/FDD; remaining hours về 0.
