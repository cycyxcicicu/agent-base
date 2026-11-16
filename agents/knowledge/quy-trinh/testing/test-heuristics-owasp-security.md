# Danh Mục Bẫy Lỗi, OWASP API Security & UI/UX (Defect Taxonomy & Security)

> **Loại: tham khảo.**
> Nguồn: tách từ test-heuristics-and-oracles.md mục 4, 5, 6.
> Tiêu chuẩn: Boris Beizer, OWASP API Security Top 10, W3C WCAG 2.1 AA.

## 1. Danh Mục Bẫy Lỗi Kinh Nghiệm (Defect Taxonomy)

| Nhóm bẫy lỗi | Biểu hiện lỗi thực tế | Giá trị hoặc hành vi test đặc trị |
|---|---|---|
| **1. Ký tự dị & Encoding** | Sập Parser JSON, SQLi, XSS, lỗi font | `' OR '1'='1`, `<script>alert(1)</script>`, `undefined`, `null`, `NaN`, Emoji 🔥, BiDi `\u202E` |
| **2. Giới hạn kiểu dữ liệu** | Tràn số nguyên (Overflow), sai số float | $-2^{31} (-2.147.483.648)$ và $2^{31}-1 (2.147.483.647)$. Float: $0.1 + 0.2 \neq 0.3$ |
| **3. Idempotency & Mạng lặp** | Double click, Webhook bắn trùng | Gửi cùng payload với cùng `Idempotency-Key` 3 lần liên tiếp trong $100$ms |
| **4. Concurrency & Race** | 2 user cùng rút tiền hoặc mua món hàng cuối | Bắn 10 requests đồng thời bằng đa luồng tại cùng 1 mili-giây |
| **5. Timezone & Năm nhuận** | Đổi giờ mùa hè (DST), ngày 29/2, lệch GMT+7 | Set giờ server giả lập vào: `2024-02-29 23:59:59`, `2024-12-31 23:59:59` |

## 2. Heuristic Kiểm Thử An Toàn API (OWASP API Top 10)

1. **BOLA (Broken Object Level Authorization):** Thay ID tài nguyên trên URL (`GET /api/orders/{other_user_id}`) bằng token user hiện tại $\rightarrow$ Bắt buộc chặn 403 Forbidden.
2. **BFLA (Broken Function Level Authorization):** Gọi endpoint quản trị (`DELETE /api/users/{id}`) bằng token user thường $\rightarrow$ Bắt buộc chặn 403.
3. **Mass Assignment:** Gửi thêm trường nhạy cảm trong payload (`"isAdmin": true`, `"role": "SUPERADMIN"`) $\rightarrow$ Backend bắt buộc phải lọc bỏ, cấm ghi đè DB.
4. **Rate Limit:** Gửi liên tục 100 requests trong 1 giây $\rightarrow$ Hệ thống bắt buộc trả về HTTP 429 Too Many Requests.

## 3. Heuristic Kiểm Thử Giao Diện & Trải Nghiệm (UI/UX)

1. **Ma Trận Màn Hình (Viewports):**
   - *Mobile (375px):* Kiểm tra vỡ layout, tràn ngang (Horizontal Scrollbar), menu hamburger.
   - *Tablet (768px):* iPad portrait.
   - *Desktop (1440px):* Laptop / Desktop widescreen.
2. **Khả Năng Tiếp Cận (Accessibility - WCAG 2.1 AA):**
   - *Tap Target Size:* Nút bấm cảm ứng trên mobile $\ge 48 \times 48$ CSS pixels.
   - *Color Contrast:* Độ tương phản màu chữ với nền $\ge 4.5:1$ (chữ thường) và $\ge 3:1$ (chữ lớn $\ge 18$pt).
   - *Keyboard Navigation:* Dùng phím `Tab`, `Enter`, `Esc` duyệt toàn bộ form, không bị kẹt con trỏ (Focus Trap).
3. **Console Log Sạch:** Dùng Chrome DevTools Protocol (CDP) quét toàn bộ log: **Console Error = 0**.
