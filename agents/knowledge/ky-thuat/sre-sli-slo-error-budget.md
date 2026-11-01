# Chuyên Đề Google SRE: Định Lượng SLI, Thiết Lập SLO & Quản Trị Error Budget

**Loại: tham khảo.**
> **Phân vùng**: Site Reliability Engineering (SRE), Operations & Monitoring  
> **Phân quyền truy cập (RBAC)**: `["sre", "architect", "lead", "devops"]`  
> **Nguồn đối chuẩn**: The Site Reliability Engineering Book (Google SRE), The Site Reliability Workbook, PromQL Best Practices  

---

## 1. Khung Đo Lường Chuẩn SRE: SLI vs SLO vs SLA
- **Sự khác biệt cốt tử**:
  - **SLI (Service Level Indicator)**: Chỉ số đo lường định lượng thực tế phản ánh hành vi hệ thống từ góc nhìn người dùng.
    $$\text{SLI} = \frac{\text{Số sự kiện tốt (Good Events)}}{\text{Tổng số sự kiện hợp lệ (Valid Events)}} \times 100\%$$
    *Ví dụ*: Tỷ lệ các request HTTP GET `/api/orders` trả về mã $200$ trong thời gian $< 250\text{ms}$.
  - **SLO (Service Level Objective)**: Mục tiêu cam kết nội bộ của đội ngũ kỹ thuật. Thường đặt cao hơn SLA.
    *Ví dụ*: SLI phải đạt $\ge 99.9\%$ tính trung bình theo chu kỳ lăn (Rolling Window) 30 ngày.
  - **SLA (Service Level Agreement)**: Cam kết pháp lý và thương mại với khách hàng hoặc đối tác bên ngoài, có điều khoản phạt tiền hoặc hoàn tiền (Service Credits) nếu vi phạm. Thường đặt thấp hơn SLO để có vùng đệm an toàn (vd: $99.5\%$).

---

## 2. Quản Trị Ngân Sách Lỗi (Error Budget Policy)
- **Công thức tính toán**:
  $$\text{Error Budget} = 100\% - \text{SLO}$$
  - Với SLO $99.9\%$, Error Budget là $0.1\%$.
  - Trong 30 ngày (tương đương $43.200$ phút), tổng thời gian gián đoạn tối đa được phép là **43.2 phút**.

### Bảng Cơ Chế Đóng Băng Tính Năng (Release Freeze Policy)
| Mức tiêu hao Error Budget | Trạng thái hệ thống | Hành động bắt buộc của Đội ngũ (Team Policy) |
|---|---|---|
| **$< 50\%$** | Xanh (Bình thường) | Tiếp tục phát triển và release các tính năng mới bình thường. |
| **$50\% - 80\%$** | Vàng (Cảnh báo) | Siết chặt quy trình review code, tăng tỷ lệ kiểm thử tự động, hoãn các release mạo hiểm. |
| **$> 100\%$ (Cạn kiệt)** | Đỏ (Đóng băng) | **DỪNG TOÀN BỘ RELEASE TÍNH NĂNG MỚI (Feature Freeze)**. 100% nhân lực Dev và SRE chuyển sang sửa bug hạ tầng, refactor code và nâng cấp hệ thống giám sát. |

---

## 3. PromQL Thực Chiến: Đo Độ Trễ P90/P99 & Tỷ Lệ Lỗi (Error Rate)

### Đo Tỷ Lệ Request Thành Công (Availability SLI)
```promql
sum(rate(http_requests_total{status=~"2..|3.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

### Đo Độ Trễ Phân Vị P99 (Latency SLI)
```promql
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket{service="payment-api"}[5m])) by (le)
)
```

### Cấu Hình Prometheus Alertmanager Chuẩn (Chống Báo Động Giả - Alert Fatigue)
```yaml
groups:
  - name: SRE_SLO_Alerts
    rules:
      - alert: CriticalErrorBudgetBurn
        # Cảnh báo nếu tỷ lệ lỗi trong 1h cao gấp 14 lần mức cho phép (đốt 2% ngân sách lỗi trong 1h)
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[1h]))
            /
            sum(rate(http_requests_total[1h]))
          ) > (1 - 0.999) * 14
        for: 2m
        labels:
          severity: page
        annotations:
          summary: "Error Budget đang bị đốt nhanh bất thường (14x burn rate)"
          description: "Service {{ $labels.service }} đang tiêu tốn ngân sách lỗi tháng với tốc độ nguy hiểm."
```

