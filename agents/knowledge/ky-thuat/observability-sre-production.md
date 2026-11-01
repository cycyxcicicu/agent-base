# Cẩm Nang Observability, SRE Production & Kubernetes Reliability

**Loại: tham khảo.**
> **Phân vùng**: Site Reliability Engineering (SRE), Monitoring & Observability  
> **Phân quyền truy cập (RBAC)**: `["sre", "devops", "architect", "dev"]`  
> **Nguồn đối chuẩn**: Google SRE Books, OpenTelemetry Specification, Prometheus & CNCF Best Practices  

---

## 1. Khung Vận Hành Google SRE: SLI, SLO, SLA & Error Budget
- **Định nghĩa chuẩn mực**:
  - **SLI (Service Level Indicator)**: Chỉ số đo lường định lượng thực tế. Ví dụ: *Tỷ lệ request HTTP trả về mã 2xx thành công trong $< 200\text{ms}$*.
    $$\text{SLI} = \frac{\text{Số request hợp lệ đạt chuẩn}}{\text{Tổng số request hợp lệ}} \times 100\%$$
  - **SLO (Service Level Objective)**: Mục tiêu cam kết nội bộ của đội ngũ kỹ thuật. Ví dụ: *SLI đạt $99.9\%$ trong chu kỳ 30 ngày*.
  - **SLA (Service Level Agreement)**: Hợp đồng pháp lý với khách hàng kèm mức phạt tài chính nếu vi phạm (thường thấp hơn SLO, vd: $99.5\%$).
  - **Error Budget (Ngân sách lỗi)**: Dung sai thất bại được phép có:
    $$\text{Error Budget} = 100\% - \text{SLO}$$
    Với SLO 99.9%, hệ thống được phép có tối đa 43.8 phút downtime/tháng. Khi cạn kiệt Error Budget, đóng băng tính năng mới (Freeze releases) để tập trung 100% vá lỗi hạ tầng và kiểm thử.

---

## 2. Chuẩn OpenTelemetry (OTel) & Lan Truyền Ngữ Cảnh (Context Propagation)
- **Vấn đề**: Trong hệ thống Microservices, 1 thao tác mua hàng đi qua 8 dịch vụ khác nhau. Khi xảy ra lỗi timeout, không thể xác định điểm nghẽn nếu thiếu Distributed Tracing.
- **W3C TraceContext Specification**:
  - Mọi request HTTP giữa các service bắt buộc truyền kèm header chuẩn:
    ```http
    traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
    ```
    - `00`: Phiên bản giao thức (version).
    - `4bf92f3577b34da6a3ce929d0e0e4736`: **Trace ID** (32 ký tự hex) xuyên suốt toàn bộ vòng đời request từ Gateway đến DB.
    - `00f067aa0ba902b7`: **Parent Span ID** (16 ký tự hex) đại diện cho bước gọi cha.
    - `01`: Trace Flags (`01` = Sampled, được ghi nhận log).
- **Nguyên tắc triển khai**:
  - Mỗi service sinh một Span ID mới cho nghiệp vụ cục bộ nhưng giữ nguyên Trace ID.
  - Sử dụng OTel Auto-Instrumentation hoặc Manual Span để đính kèm metadata: `user.id`, `http.status_code`, `db.statement`.

---

## 3. PromQL Thực Chiến: Đo Độ Trễ Phân Vị P90/P99 & Quy Tắc Cảnh Báo
- **Vì sao không dùng thời gian phản hồi trung bình (Average Latency)?**
  - Giá trị trung bình che giấu hoàn toàn các điểm dị biệt (Outliers). 95% người dùng mất 50ms nhưng 5% người dùng mất 10 giây thì mức trung bình vẫn trông có vẻ ổn.
- **Công thức PromQL tính độ trễ P99 chuẩn xác**:
  ```promql
  histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
  ```
- **Quy tắc cấu hình Alertmanager (Tránh báo động giả - Alert Fatigue)**:
  - Cảnh báo chỉ kích hoạt khi P99 vượt ngưỡng liên tục trong cửa sổ thời gian nhất định:
  ```yaml
  alert: HighLatencyP99
  expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)) > 0.5
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Service {{ $labels.service }} P99 latency > 500ms trong 5 phút"
  ```

---

## 4. Vòng Đời Kubernetes Probes & Graceful Shutdown Không Downtime
- **Bộ 3 Probes bắt buộc trong Pod Spec**:
  1. **Startup Probe**: Dành cho ứng dụng khởi động chậm (Spring Boot, Java nạp bean). Ngăn không cho K8s giết nhầm container khi đang init:
     ```yaml
     startupProbe:
       httpGet: { path: /actuator/health/liveness, port: 8080 }
       failureThreshold: 30
       periodSeconds: 10
     ```
  2. **Readiness Probe**: Kiểm tra container đã sẵn sàng nhận traffic người dùng chưa (đã kết nối DB, nạp xong cache). Nếu fail, K8s tạm thời ngắt Pod khỏi Service Endpoint mà KHÔNG khởi động lại Pod.
  3. **Liveness Probe**: Kiểm tra Pod có còn phản hồi không (phát hiện deadlock). Nếu fail liên tục, K8s kill và tái tạo Pod mới.
- **Quy trình Graceful Shutdown chuẩn (30s)**:
  1. K8s gửi tín hiệu `SIGTERM` tới ứng dụng và đồng thời xóa Pod khỏi Service Endpoints.
  2. Ứng dụng kích hoạt hook shutdown: Ngừng nhận request mới, hoàn tất các request đang xử lý dở trong hàng đợi, đóng connection pool DB.
  3. Cấu hình `preStop` sleep 5s để đảm bảo toàn bộ kube-proxy iptables kịp cập nhật trước khi app tắt hẳn:
     ```yaml
     lifecycle:
       preStop:
         exec:
           command: ["/bin/sh", "-c", "sleep 5"]
     ```

