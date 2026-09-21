# Ví Dụ Mẫu: Quy Trình Gỡ Lỗi Hệ Thống 4 Pha (Systematic Debugging Loop)

Thừa hưởng từ `pocock-skills` (`diagnosing-bugs`), quy trình này loại bỏ hoàn toàn việc "đoán mò code" mà ép AI tuân thủ kỷ luật nghiêm ngặt:

## 5 Pha Gỡ Lỗi Cốt Lõi
1. **Pha 1: Xây Dựng Vòng Lặp Phản Hồi (Tight Feedback Loop)**
   - Tạo một lệnh kiểm thử duy nhất, chạy trong vòng < 0.1 giây.
   - **Bắt buộc**: Test phải tạo ra **TÍN HIỆU ĐỎ (RED)** chính xác trên bug này, không phải lỗi crash chung chung.
2. **Pha 2: Tái Hiện & Thu Nhỏ (Reproduce + Minimise)**
   - Cắt bỏ mọi dữ liệu và thành phần thừa cho đến khi chỉ còn những nhân tố cấu thành lỗi.
3. **Pha 3: Đưa Ra 3–5 Giả Thuyết Bác Bỏ Được (Falsifiable Hypotheses)**
   - Cấu trúc: *"Nếu X là nguyên nhân, thì sửa Y sẽ hết lỗi / tăng Z sẽ lỗi nặng hơn."*
4. **Pha 4: Cài Đặt Thiết Bị Đo / Log Cô Lập (Instrument)**
   - In giá trị biến trung gian hoặc dựng assert điểm chặn để xác thực giả thuyết nào đúng.
5. **Pha 5: Sửa Lỗi & Xác Nhận Tín Hiệu XANH (Fix & Verify)**
   - Chạy lại đúng feedback loop ở Pha 1, kiểm tra trạng thái chuyển sang **XANH (GREEN)**.

## Thực Thi Kiểm Thử
Chạy tái hiện lỗi (Tín hiệu ĐỎ):
```bash
python examples/systematic-debugging/test_repro.py --mode buggy
```

Chạy xác minh sau khi sửa (Tín hiệu XANH):
```bash
python examples/systematic-debugging/test_repro.py --mode fixed
```
