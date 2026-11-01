# Chuyên Đề Kubernetes Probes & Graceful Shutdown Không Downtime

**Loại: tham khảo.**
> **Phân vùng**: DevOps, SRE & Kubernetes Production Infrastructure  
> **Phân quyền truy cập (RBAC)**: `["devops", "sre", "architect", "dev"]`  
> **Nguồn đối chuẩn**: Kubernetes Official Documentation, Google Cloud Architecture Center, Spring Boot Production Guide  

---

## 1. Phân Biệt Ba Loại Probes Trong Kubernetes

```
Khởi động Pod
      │
      ▼
[Startup Probe] ──(Thất bại liên tục)──> K8s Kill & Restart Pod
      │ (Thành công lần đầu)
      ├────────────────────────┬────────────────────────┐
      ▼                        ▼                        ▼
[Readiness Probe]       [Liveness Probe]         (Tải bình thường)
      │                        │
(Thất bại)               (Thất bại)
      ▼                        ▼
Tạm ngừng nhận traffic    K8s Kill & Restart Pod
(Loại khỏi Service Endpoints)
```

| Loại Probe | Mục đích cốt lõi | Hành vi khi thất bại | Cấu hình khuyến nghị |
|---|---|---|---|
| **Startup Probe** | Chờ ứng dụng nạp bộ nhớ/cache lúc ban đầu (Spring Boot, Java JVM nạp context). | K8s sẽ kiên nhẫn chờ, không kích hoạt Liveness để tránh kill nhầm pod. | `failureThreshold: 30`, `periodSeconds: 10` (Chờ tối đa 300s). |
| **Readiness Probe** | Xác nhận ứng dụng đã sẵn sàng tiếp nhận lượt truy cập của người dùng (DB pool đã kết nối, cache ấm). | **Không restart Pod**. Chỉ tạm thời xóa Pod khỏi danh sách IP của Kubernetes Service. | `periodSeconds: 5`, `timeoutSeconds: 2`. |
| **Liveness Probe** | Phát hiện ứng dụng rơi vào trạng thái chết lâm sàng (Deadlock, OOM treo luồng). | **K8s tự động gửi tín hiệu KILL và khởi động lại Pod**. | `periodSeconds: 15`, `failureThreshold: 3`. |

---

## 2. Kỹ Thuật Graceful Shutdown 30 Giây (Zero-Downtime Deployment)
- **Vấn đề ngầm định**: Khi một Pod bị chấm dứt (Rolling Update), K8s đồng thời:
  1. Gửi tín hiệu `SIGTERM` tới ứng dụng.
  2. Bắt đầu cập nhật `iptables`/IPVS trên toàn bộ các Node để gỡ IP của Pod.
  - *Rủi ro*: Quá trình cập nhật mạng mất từ 1–3 giây. Nếu ứng dụng tắt ngay lập tức khi nhận `SIGTERM`, các request đang bay trên đường truyền sẽ bị lỗi kết nối (**HTTP 502 Bad Gateway / Connection Refused**).
- **Giải pháp 3 bước hoàn hảo**:
  1. Thêm hook `preStop` chạy lệnh `sleep 5` để chờ iptables cập nhật xong trước khi truyền `SIGTERM`.
  2. Cấu hình Spring Boot / Node.js đóng kết nối êm ái (`graceful`), chờ các request đang dở hoàn tất trong 25 giây.
  3. Đặt `terminationGracePeriodSeconds: 35`.

---

## 3. Bản Mẫu Kubernetes Pod Spec Hoàn Chỉnh

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-deployment
spec:
  replicas: 3
  template:
    spec:
      terminationGracePeriodSeconds: 35 # Cho phép tổng thời gian dừng tối đa 35s
      containers:
        - name: order-service
          image: internal-registry.company.com/order-service:v2.1.0
          lifecycle:
            preStop:
              exec:
                # Trì hoãn 5s để kube-proxy và Ingress Controller kịp ngắt traffic
                command: ["/bin/sh", "-c", "sleep 5"]
          ports:
            - containerPort: 8080
          startupProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            failureThreshold: 30 # 30 x 5s = 150s chờ khởi động
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            periodSeconds: 5
            timeoutSeconds: 2
            failureThreshold: 2
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            periodSeconds: 10
            timeoutSeconds: 3
            failureThreshold: 3
```

### Cấu Hình Spring Boot `application.yml`
```yaml
server:
  shutdown: graceful # Bật chế độ đóng kết nối êm ái

spring:
  lifecycle:
    timeout-per-shutdown-phase: 25s # Tối đa 25s để xử lý nốt các request dở dang
```

