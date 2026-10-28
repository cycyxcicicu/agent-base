# Cẩm Nang Kiểm Thử Playwright (E2E) & Grafana K6 (Load/Performance Testing)

> **Loại: tham khảo.**  
> **Mã định danh:** `playwright-and-k6-testing`  
> **Chuyên mục:** Kiểm thử Phần mềm, Tự động hóa E2E & Đo kiểm Hiệu năng Tải  
> **Nguồn gốc:** Playwright Official Docs (Microsoft), Grafana K6 Official Documentation  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. Playwright — Chuẩn Mực Kiểm Thử Đầu Cuối (E2E Testing) Hiện Đại

Playwright (Microsoft) là framework kiểm thử tự động hóa trình duyệt nhanh, tin cậy và đa nền tảng (Chromium, Firefox, WebKit) chạy song song với cơ chế **Auto-Waiting** độc quyền.

### 1.1. Bốn Nguyên Tắc Vàng Của Playwright
1. **Ưu tiên User-Facing Locators (Định vị theo giác quan người dùng):**
   - ❌ Tránh XPath hoặc CSS class dễ gãy: `page.locator("div > button.btn-primary.submit-btn-2")`
   - ✅ Dùng Locators ngữ nghĩa:
     - `page.getByRole("button", { name: "Xác nhận đặt hàng" })`
     - `page.getByLabel("Số điện thoại nhận hàng")`
     - `page.getByPlaceholder("Nhập mã giảm giá")`
     - `page.getByTestId("order-total-amount")`
2. **Không dùng `sleep` tùy tiện (Auto-Waiting):** Playwright tự động chờ phần tử xuất hiện, hiển thị, có thể click và dừng chuyển động trước khi thao tác.
3. **Cô lập trạng thái kiểm thử (Browser Context Isolation):** Mỗi test case chạy trong một Browser Context hoàn toàn mới (cookie, localStorage sạch), tốc độ khởi tạo chỉ mất vài mili-giây.
4. **Sử dụng Trace Viewer khi debug:** Khi test fail trong CI/CD, xuất file `trace.zip` ghi lại toàn bộ DOM snapshot, network logs và video chuyển động từng hành động.

### 1.2. Kịch Bản Test Mẫu: Đặt Hàng & Kiểm Tra Đơn Trên Web

```typescript
// tests/e2e/order-flow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Luồng Đặt Hàng & Thanh Toán', () => {
  test('Khách hàng đặt hàng thành công và thấy mã đơn', async ({ page }) => {
    // 1. Mở trang sản phẩm
    await page.goto('/products/sp-001');

    // 2. Thao tác chọn số lượng & thêm vào giỏ
    await page.getByLabel('Số lượng').fill('2');
    await page.getByRole('button', { name: 'Thêm vào giỏ hàng' }).click();

    // 3. Chuyển sang giỏ hàng & thanh toán
    await page.getByRole('link', { name: 'Giỏ hàng' }).click();
    await expect(page.getByTestId('cart-item-count')).toHaveText('2');
    await page.getByRole('button', { name: 'Tiến hành đặt hàng' }).click();

    // 4. Điền thông tin giao nhận
    await page.getByLabel('Họ và tên').fill('Nguyễn Văn A');
    await page.getByLabel('Số điện thoại').fill('0912345678');
    await page.getByLabel('Địa chỉ giao hàng').fill('Tòa nhà GDT, Hà Nội');

    // 5. Chọn phương thức thanh toán COD & bấm Đặt hàng
    await page.getByRole('radio', { name: 'Thanh toán khi nhận hàng (COD)' }).check();
    await page.getByRole('button', { name: 'Xác nhận đặt hàng' }).click();

    // 6. Kiểm chứng kết quả (Assertions)
    await expect(page.getByRole('heading', { name: 'Đặt hàng thành công!' })).toBeVisible();
    const orderCode = page.getByTestId('success-order-code');
    await expect(orderCode).toHaveText(/^ORD-\d{8}-\w{4}$/);
  });
});
```

---

## 2. Grafana K6 — Kiểm Thử Tải & Đánh Giá Năng Lực Chịu Tải (Load & Stress Testing)

K6 là công cụ kiểm thử tải thế hệ mới được viết bằng Go, kịch bản viết bằng JavaScript, tối ưu tài nguyên vượt trội so với JMeter (1 máy tính có thể sinh hàng chục ngàn Virtual Users - VUs).

### 2.1. Các Mô Hình Kiểm Thử Tải (Test Types)
1. **Smoke Test:** Kiểm tra tối thiểu (1–2 VUs) để xác thực script chạy đúng.
2. **Load Test:** Tăng dần tải đến mức kỳ vọng giờ cao điểm (Peak Traffic) và giữ ổn định để đo độ trễ và thông lượng (RPS).
3. **Stress Test:** Tăng tải vượt ngưỡng thiết kế để tìm điểm gãy (Breaking Point) của hệ thống và xem hệ thống phục hồi ra sao khi giảm tải.
4. **Spike Test:** Đột ngột tăng vọt lượng người dùng trong thời gian cực ngắn (Flash Sale) để kiểm tra cơ chế Auto-scaling và Rate Limiter.

### 2.2. Kịch Bản K6 Mẫu Kèm Ngưỡng Cam Kết SLA (Thresholds)

```javascript
// load-tests/order-api-load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

// Cấu hình các giai đoạn tải (Stages) và tiêu chí chất lượng (Thresholds)
export const options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp-up lên 50 VUs trong 30 giây
    { duration: '1m',  target: 50 },  // Giữ tải ổn định 50 VUs trong 1 phút
    { duration: '20s', target: 200 }, // Spike lên 200 VUs trong 20 giây (giờ cao điểm)
    { duration: '1m',  target: 200 }, // Giữ tải 200 VUs
    { duration: '30s', target: 0 },   // Ramp-down về 0
  ],
  thresholds: {
    // 95% số request phải phản hồi dưới 300ms
    http_req_duration: ['p(95)<300'],
    // 99% số request phải phản hồi dưới 600ms
    http_req_duration: ['p(99)<600'],
    // Tỷ lệ lỗi toàn bộ kịch bản phải dưới 1%
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const url = 'http://api.gdttech.net/api/v1/orders';
  const payload = JSON.stringify({
    customerId: 1002,
    items: [
      { productId: 45, quantity: 2, unitPrice: 150000 }
    ],
    shippingMethod: 'JNT_EXPRESS'
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-jwt-token-benchmarking'
    },
  };

  // 1. Gửi request tạo đơn hàng
  const res = http.post(url, payload, params);

  // 2. Kiểm chứng kết quả phản hồi (Checks)
  check(res, {
    'Trạng thái là 201 Created': (r) => r.status === 201,
    'Có mã đơn hàng trả về': (r) => JSON.parse(r.body).orderCode !== undefined,
    'Thời gian xử lý < 250ms': (r) => r.timings.duration < 250,
  });

  // Tạm dừng ngẫu nhiên từ 1 đến 2 giây giữa các thao tác người dùng
  sleep(Math.random() * 1 + 1);
}
```
