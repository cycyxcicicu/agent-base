# Cẩm Nang Phản Biện Kế Hoạch (Plan Review Rubric) - Thừa hưởng từ `gstack`

Trước khi bắt tay vào gõ code, một AI Agent chuyên nghiệp (đặc biệt là vai trò SA và Dev Lead) phải tự phản biện kế hoạch thông qua 2 bộ lọc: **CEO Review** (Tầm nhìn & Trải nghiệm) và **Eng Review** (Độ bền kỹ thuật & Rủi ro).

---

## 1. CEO Review Checklist (Bộ Lọc Sản Phẩm & Trải Nghiệm)
1. **Outcome First**: Kế hoạch này giải quyết nỗi đau gì của người dùng cuối, hay chỉ là "thích thì refactor"?
2. **10x Differentiator**: Giải pháp này có mang lại trải nghiệm vượt trội rõ rệt không?
3. **Do-Nothing Test**: Điều tồi tệ gì xảy ra nếu chúng ta không làm tính năng này trong 3 tháng tới?
4. **Scope Creep Trap**: Có phần nào đang bị "over-engineering" hoặc vẽ thêm việc không cần thiết cho MVP?
5. **Clear Success Metric**: Làm sao đo lường được tính năng này thành công (thời gian, tỷ lệ chuyển đổi, độ hài lòng)?

---

## 2. Eng Review Checklist (Bộ Lọc Kiến Trúc & Vận Hành)
1. **Blast Radius**: Thay đổi này ảnh hưởng bao nhiêu file/dịch vụ? Có nguy cơ vỡ toàn hệ thống không?
2. **Rollback Strategy**: Nếu triển khai gặp lỗi nghiêm trọng, kế hoạch hoàn tác (revert) trong 60 giây là gì?
3. **Data Migration Safety**: Có đụng chạm schema database không? Có tuân thủ quy tắc Expand-Contract không?
4. **Failure Modes & Idempotence**: Các lệnh gọi API/Worker có tính chất lũy kế (Idempotent) không? Nếu timeout có bị duplicate dữ liệu?
5. **Observability**: Hệ thống có log, metric và alert đủ để biết tính năng đang chạy tốt hay hỏng hóc?
