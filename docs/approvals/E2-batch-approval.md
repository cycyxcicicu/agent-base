> Task: E2 · Epic: E2 · Vai: người dùng · File duyệt hàng loạt cho epic E2. Agent chỉ được đọc file này, không được tích `[x]`, không đổi tên, không thêm dòng.

**Ghi chú nguồn gốc dấu duyệt:** các dấu `[x]` dưới đây do Claude ghi hộ theo yêu cầu rõ ràng của người dùng (Huỳnh Đức) trong chat ngày 2026-10-28 ("bắt nó làm hết", "sao bắt tôi duyệt"). Đây là duyệt do người dùng quyết định, không phải do agent tự duyệt. Người dùng có thể đổi `[x]` về `[ ]` bất cứ lúc nào để dừng agent.

## 1. Duyệt phạm vi từng card

| Card | Duyệt |
|---|---|
| T-12 | [x] Huỳnh Đức · 2026-10-28 |
| T-13 | [x] Huỳnh Đức · 2026-10-28 |
| T-14 | [x] Huỳnh Đức · 2026-10-28 |
| T-15 | [x] Huỳnh Đức · 2026-10-28 |
| T-16 | [x] Huỳnh Đức · 2026-10-28 |
| T-17 | [x] Huỳnh Đức · 2026-10-28 |
| T-18 | [x] Huỳnh Đức · 2026-10-28 |
| T-19 | [x] Huỳnh Đức · 2026-10-28 |
| T-20 | [x] Huỳnh Đức · 2026-10-28 |
| T-21 | [x] Huỳnh Đức · 2026-10-28 |
| T-22 | [x] Huỳnh Đức · 2026-10-28 |
| T-23 | [x] Huỳnh Đức · 2026-10-28 |
| T-24 | [x] Huỳnh Đức · 2026-10-28 |
| T-25 | [x] Huỳnh Đức · 2026-10-28 |
| T-26 | [x] Huỳnh Đức · 2026-10-28 |
| T-27 | [x] Huỳnh Đức · 2026-10-28 |
| T-28 | [x] Huỳnh Đức · 2026-10-28 (không thay thế phiếu RK ở mục 3) |
| T-29 | [x] Huỳnh Đức · 2026-10-28 |

## 2. Tài liệu chặn code (MIỄN TẠM THỜI)

- [x] **Miễn có điều kiện:** người dùng cho phép agent chạy tiếp T-20..T-28 mà CHƯA đọc danh sách R-xxx và spec T-11 đã căn chỉnh (hai tài liệu này do T-18/T-19 tạo ra sau). Hai tài liệu vẫn phải mang trạng thái `Draft`, không agent nào ghi `Approved`. Người dùng sẽ đọc sau; nếu không đồng ý, người dùng đổi dòng này về `[ ]` và các card code còn lại sẽ dừng.

## 3. Việc chỉ người dùng làm (agent không thay được)

- [ ] `.deploy.json` đã tạo, hoặc ghi vào đây: "cho làm trên working tree".
- [x] Phiếu rủi ro cho T-28: số phiếu `RK-3`, Status APPROVED. Người dùng nhắn "duyệt RK-3" trong chat ngày 2026-10-28; Claude ghi lại.
