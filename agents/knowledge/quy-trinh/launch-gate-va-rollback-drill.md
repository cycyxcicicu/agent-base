# Cổng Phát Hành 20% & Diễn Tập Hoàn Tác (Launch Gate & Rollback Drill)

> **Loại: tham khảo.** Quy chuẩn hoàn tất 20% còn lại trước khi mở traffic Production, diễn tập Kill-switch và Rollback CSDL.
> Liên quan: `agents/protocols/launch-readiness.md`, `agents/protocols/risk-gate.md`, `scripts/launch-gate.py`.

## 1. Quy Tắc 80/20: Merge-Ready $\neq$ Launch-Ready

- **Merge-Ready (80%):** Code pass unit test, code review đạt, CI/CD build xanh, sẵn sàng gộp vào nhánh `main`/`release`.
- **Launch-Ready (100%):** Hoàn thành kiểm toán 20% còn lại để đảm bảo an toàn tuyệt đối khi đưa traffic người dùng thật vào hệ thống.

```
[Merge-Ready (80%)] ──> [Launch Gate (20%)] ──> [Canary 5%] ──> [Production 100%]
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
  [1. Diễn tập Rollback]  [2. Diễn tập Kill-Switch]  [3. Kiểm toán CSO & N+1]
```

## 2. Diễn Tập Hoàn Tác CSDL (Database Rollback Drill)

Mọi thay đổi CSDL (Liquibase/Flyway) có rủi ro từ mức Vừa trở lên bắt buộc phải trải qua diễn tập rollback trên môi trường Staging:
1. **Chạy Migration Up:** Áp dụng changeset mới trên DB Staging có dữ liệu mô phỏng.
2. **Kiểm tra ghi dữ liệu:** Thực hiện thao tác CRUD trên bảng mới/cột mới.
3. **Chạy Migration Down (Rollback):** Kích hoạt lệnh rollback của changeset:
   `./mvnw liquibase:rollback -Dliquibase.rollbackCount=1`
4. **Kiểm tra tính toàn vẹn:** Xác nhận CSDL quay về trạng thái cũ an toàn, không có orphan record, không bị table lock kéo dài gây nghẽn kết nối.

## 3. Diễn Tập Tắt Cờ Tính Năng (Kill-Switch Drill)

Mọi tính năng Leaf mới đều bắt buộc bọc sau cờ tính năng (Feature Flag, default = OFF):
- **Kịch bản diễn tập:**
  1. Bật cờ (Flag = ON) trên Staging: Kiểm tra tính năng mới chạy đúng.
  2. Giả lập lỗi runtime hoặc sự cố: Kích hoạt tắt cờ (Flag = OFF).
  3. **Tiêu chí nghiệm thu:** Hệ thống phải tự động fallback về luồng cũ trong vòng $\le 30$ giây mà không sinh mã lỗi 500 và không cần redeploy ứng dụng.

## 4. Kế Hoạch Mở Traffic Canary & Giám Sát SRE

Khi mở cờ tính năng trên Production, áp dụng chiến lược mở dần (Canary Rollout):
- **Giai đoạn 1 (Canary 5%):** Mở cho 5% người dùng nội bộ hoặc ngẫu nhiên. Giám sát APM trong 30 phút.
- **Giai đoạn 2 (Canary 25%):** Nâng lên 25% traffic. Theo dõi P99 latency và số lượng ngoại lệ.
- **Giai đoạn 3 (Full Rollout 100%):** Mở toàn bộ traffic khi không có cảnh báo vi phạm SLO/Error Budget.
- **Quy tắc Rollback khẩn cấp:** Nếu P99 latency tăng $> 50\%$ hoặc Error Rate $> 1\%$, lập tức tắt cờ tính năng về OFF.
