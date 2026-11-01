# Chuyên Đề OpenTelemetry (OTel), Chuẩn W3C TraceContext & Distributed Tracing

**Loại: tham khảo.**
> **Phân vùng**: Observability, SRE & Microservices Tracing  
> **Phân quyền truy cập (RBAC)**: `["sre", "architect", "devops", "dev"]`  
> **Nguồn đối chuẩn**: OpenTelemetry Specification (CNCF), W3C Recommendation for Trace Context, Jaeger Tracing  

---

## 1. Cấu Trúc W3C TraceContext & Lan Truyền Ngữ Cảnh (Context Propagation)
- **Vấn đề**: Trong kiến trúc Microservices phân tán, 1 request từ người dùng (vd: Bấm nút Thanh Toán) có thể kích hoạt chuỗi 10 cuộc gọi nội bộ qua HTTP/gRPC/Kafka. Nếu không có mã định danh xuyên suốt, việc tra cứu nguyên nhân gây chậm (Bottleneck) hay lỗi 500 là bất khả thi.
- **Tiêu chuẩn W3C Header (`traceparent`)**:
  Mọi cuộc gọi giữa các dịch vụ bắt buộc phải đính kèm header HTTP chuẩn:
  ```http
  traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
  ```
  - `00`: **Version** (Hiện tại là `00`).
  - `4bf92f3577b34da6a3ce929d0e0e4736`: **Trace ID** (16 bytes / 32 ký tự hex) duy nhất cho toàn bộ chuỗi hành trình.
  - `00f067aa0ba902b7`: **Parent Span ID** (8 bytes / 16 ký tự hex) đại diện cho bước gọi cha ngay trước đó.
  - `01`: **Trace Flags** (`01` nghĩa là Sampled - dữ liệu này được chọn để ghi vào cơ sở lưu trữ Jaeger/Tempo).

```
[API Gateway]               Span A (Trace ID: 4bf92f..., Span ID: aaa1)
      │
      ▼ (HTTP Header: traceparent: 00-4bf92f...-aaa1-01)
[Order Service]             Span B (Trace ID: 4bf92f..., Span ID: bbb2, Parent: aaa1)
      │
      ▼ (HTTP Header: traceparent: 00-4bf92f...-bbb2-01)
[Payment Service]           Span C (Trace ID: 4bf92f..., Span ID: ccc3, Parent: bbb2)
```

---

## 2. Phân Biệt Trace, Span & Baggage
1. **Trace**: Là cây phân cấp (Directed Acyclic Graph) đại diện cho toàn bộ vòng đời của một request qua nhiều hệ thống.
2. **Span**: Là một đơn vị công việc độc lập trong một service (vd: một câu lệnh truy vấn SQL, một lệnh gọi HTTP, hoặc một hàm xử lý mã hóa). Span có thời gian bắt đầu, thời gian kết thúc, trạng thái (OK/Error) và các thuộc tính (Attributes).
3. **Baggage**: Là các cặp key-value mang tính ngữ cảnh nghiệp vụ (vd: `tenant_id=vn_hcm`, `user_tier=platinum`) được tự động lan truyền qua toàn bộ các service con mà không cần can thiệp vào payload nghiệp vụ.

---

## 3. Kiến Trúc OpenTelemetry Collector Pipeline

```
[App 1 (OTel SDK)] ──OTLP/gRPC──┐
[App 2 (OTel SDK)] ──OTLP/gRPC──┼──> [OTel Collector (Agent/Gateway)]
[App 3 (OTel SDK)] ──OTLP/gRPC──┘           │
                                       ┌─────┴────────────────┐
                                 (Receivers)             (Processors)
                                       │                   - Batch
                                       │                   - Memory Limiter
                                       │                   - Filter
                                       ▼                      │
                                 (Exporters) <────────────────┘
                                  ├──> [Jaeger / Grafana Tempo (Traces)]
                                  ├──> [Prometheus (Metrics)]
                                  └──> [OpenSearch / Loki (Logs)]
```

---

## 4. Mã Nguồn Mẫu Thủ Công Tạo Span & Attributes (Java / OpenTelemetry API)

```java
public class OrderProcessingService {

    private static final Tracer tracer = GlobalOpenTelemetry.getTracer("order-service", "1.0.0");

    public void processOrder(Order order) {
        Span span = tracer.spanBuilder("ProcessOrderLogic")
                          .setSpanKind(SpanKind.INTERNAL)
                          .startSpan();

        try (Scope scope = span.makeCurrent()) {
            // Đính kèm các metadata quan trọng hỗ trợ điều tra sự cố
            span.setAttribute("order.id", order.getId());
            span.setAttribute("order.amount", order.getTotalAmount().doubleValue());
            span.setAttribute("customer.id", order.getCustomerId());

            executeDatabaseUpdate(order);

        } catch (Exception ex) {
            span.recordException(ex);
            span.setStatus(StatusCode.ERROR, "Lỗi cập nhật đơn hàng: " + ex.getMessage());
            throw ex;
        } finally {
            span.end(); // Kết thúc span để tính thời gian thực thi chính xác
        }
    }
}
```

