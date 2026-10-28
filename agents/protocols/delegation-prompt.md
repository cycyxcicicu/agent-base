> Task: T-14 · Epic: E2 · Vai: writer

# Khuôn mẫu prompt ủy thác và giao việc cho mô hình (Delegation Prompt Protocol)

Giao thức này quy chuẩn hóa hợp đồng giao việc giữa các tác tử (đặc biệt khi giao việc cho mô hình khác hoặc subagent), giúp ngăn ngừa tình trạng báo cáo khống ("báo xong nhưng chưa làm"), trôi lệch phạm vi và ảo giác.

---

## 1. Bảy thành phần bắt buộc của một Prompt giao việc

1. **Bối cảnh & Điều KHÔNG làm**: Nêu bối cảnh 1-2 câu, mục tiêu cốt lõi, và danh sách điều CẤM (ví dụ: không git ghi, không sửa file ngoài scope, không thêm dependency).
2. **Khóa phạm vi (Scope Gating)**: Liệt kê tường minh danh sách file được sửa (`scope_edit`) và file cấm chạm (`scope_deny`). Ngoài danh sách này BẮT BUỘC DỪNG và hỏi, không tự tiện sửa.
3. **Định vị không phụ thuộc số dòng**: Định vị vị trí cần can thiệp bằng tên hàm, tên lớp, interface hoặc block logic đặc trưng. Tuyệt đối không dùng số dòng tuyệt đối vì dễ lệch khi diff.
4. **Mốc kiểm thử đầu - cuối**: Ghi rõ số lượng test mốc đầu và mốc cuối; sau mỗi nhóm thay đổi phải chạy test rút gọn (`pytest -q`, `unittest -q`) để xác nhận không gây hồi quy.
5. **Lệnh bằng chứng với kết quả kỳ vọng**: Lệnh kiểm chứng độc lập (ví dụ `git status -s`, `grep`, test exit code). Dán nguyên văn kết quả thật.
6. **Mục bắt buộc "CHƯA chạy / CHƯA kiểm chứng" trong báo cáo**: Mọi điểm chưa có lệnh kiểm tra thực tế phải liệt kê trung thực tại mục này; cấm tự suy đoán là "đã chạy ngầm".
7. **Nguyên tắc vàng**: *"Tuyệt đối không ghi đã sửa / đã xong / PASS khi chưa chạy lệnh bằng chứng và dán output thật."*

---

## 2. Mẫu Prompt giao việc chuẩn (Ví dụ trung lập)

```markdown
Bạn là dev thực thi trong repo `my-project`. Nhiệm vụ: chuẩn hóa hàm xử lý token `normalize_payload` trong `src/auth/token.py`.

== 1. LUẬT CỨNG ==
- KHÔNG thêm thư viện bên ngoài.
- KHÔNG sửa file ngoài phạm vi: chỉ sửa `src/auth/token.py` và `tests/test_token.py`.
- KHÔNG ghi "đã sửa" khi chưa chạy lệnh bằng chứng.

== 2. MỐC TEST BAN ĐẦU ==
- Chạy `python -m unittest discover -s tests -q` -> Mốc đầu phải là 45 test OK.

== 3. VIỆC CẦN LÀM ==
1. Viết unit test mới trong `tests/test_token.py`: kiểm tra hàm `normalize_payload` khi nhận chuỗi rỗng thì trả về dict rỗng `{}`. Chạy test thấy FAIL đúng lý do.
2. Tại `src/auth/token.py`, định vị hàm `normalize_payload`, thêm điều kiện guard check `if not payload: return {}`.
3. Chạy lại test suite: mốc cuối phải là 46 test OK.

== 4. LỆNH BẰNG CHỨNG & BÁO CÁO ==
- Chạy: `git status --porcelain` (chỉ hiển thị 2 file trong phạm vi).
- Chạy: `python -m unittest discover -s tests -q` (46 tests OK).
- Báo cáo gồm: (1) Đã làm gì; (2) Lệnh và output; (3) Mục CHƯA chạy/CHƯA kiểm chứng.
```
