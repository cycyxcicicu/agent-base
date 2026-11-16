# Ma Trận Rủi Ro PRISMA & Kiểm Thử Hiệu Năng (Risk & Performance Testing)

> **Loại: tham khảo.**
> Nguồn: tách từ test-estimation-and-risk.md mục 3, 5.
> Tiêu chuẩn: Rex Black (PRISMA/PRAM), John D. C. Little (Little's Law), Neil Gunther (USL).

## 1. Ma Trận Quản Trị Rủi Ro Sản Phẩm (PRISMA & PRAM)

Định lượng mức độ ưu tiên kiểm thử:
$$\text{Rủi Ro Sản Phẩm } (\text{Risk}) = \text{Xác Suất Lỗi } (\text{Likelihood}) \times \text{Mức Độ Thiệt Hại } (\text{Impact})$$

| Vùng rủi ro | Mức độ | Đặc điểm | Chiến lược kiểm thử |
|---|---|---|---|
| **Vùng 1: Chí Mạng** | High Likelihood $\times$ High Impact | Thanh toán tiền, trừ kho, bảo mật token | Đầu tư 70% công sức, vét cạn biên, Branch 100%, tự động hóa |
| **Vùng 2: Tiềm Ẩn** | Low Likelihood $\times$ High Impact | Sập kết nối Core Bank, hỏng ổ cứng DB | Kiểm thử cơ chế Failover, Rollback, Circuit Breaker |
| **Vùng 3: Lỗi Vặt** | High Likelihood $\times$ Low Impact | Lệch màu CSS, format ngày hiển thị | Smoke test nhanh, sửa khi có thời gian rảnh |
| **Vùng 4: Thấp** | Low Likelihood $\times$ Low Impact | Tính năng hiếm dùng, rủi ro không đáng kể | Chấp nhận rủi ro dư thừa, không viết test tự động |

## 2. Mô Hình Toán Học Kiểm Thử Hiệu Năng & Chịu Tải

### 2.1 Định Luật Little (Little's Law)
Trong hệ thống hàng đợi ổn định, mối quan hệ giữa Concurrency ($L$), Throughput ($\lambda$) và Response Time ($W$):
$$L = \lambda \times W \implies \lambda = \frac{L}{W}$$
- *Ví dụ:* Cam kết chịu tải $L = 1000$ concurrent users với Response Time $W = 0.5$s $\implies$ Target Throughput tối thiểu phải đạt $\lambda = \frac{1000}{0.5} = 2000 \text{ TPS}$.

### 2.2 Định Luật Mở Rộng Phổ Quát (Universal Scalability Law - USL)
$$C(N) = \frac{N}{1 + \alpha(N - 1) + \beta N(N - 1)}$$
- $\alpha$: Tranh chấp tài nguyên (Contention - xếp hàng chờ lock DB).
- $\beta$: Tổn thất đồng bộ (Coherency penalty - cache invalidation).
- Khi tăng thread/node, hệ thống sẽ đạt đỉnh trần và sụt giảm hiệu năng nếu $\beta > 0$ (hiện tượng thrashing).

### 2.3 Năm Loại Hình Kiểm Thử Chịu Tải
1. **Load Testing:** Chạy tải ở mức thiết kế bình thường để xác nhận SLA.
2. **Stress Testing:** Ép tải vượt giới hạn thiết kế để tìm điểm gãy (Breaking Point).
3. **Spike Testing:** Đột ngột tăng tải gấp 10 lần trong 5 giây (Flash Sale) để kiểm tra Auto-scaling.
4. **Soak / Endurance Testing:** Chạy tải liên tục trong 24–72 giờ để phát hiện rò rỉ bộ nhớ (Memory Leak).
5. **Breakpoint Testing:** Tăng tải bậc thang (Ramp-up) cho đến khi hệ thống sập để đo trần hạ tầng.
