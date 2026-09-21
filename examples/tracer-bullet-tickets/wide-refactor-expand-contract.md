---
id: "WR-01"
title: "Tái Cấu Trúc Toàn Diện (Wide Refactor): Chuyển đổi Khóa Tài Khoản từ AccountNumber sang AccountUUID"
status: "in-progress"
pattern: "expand-contract"
blast_radius: "54 files, 180 call sites across 4 services"
---

# Tái Cấu Trúc Toàn Diện (Wide Refactor): Mẫu Expand-Contract

Khi một thay đổi có **Blast Radius (bán kính ảnh hưởng)** lan khắp toàn bộ hệ thống, việc cố gắng nhồi nhét vào một vertical slice duy nhất sẽ khiến CI bị đỏ hàng loạt hoặc phá vỡ các pull request song song. Thay vào đó, quy trình tuân thủ mô hình **Expand-Contract** 3 giai đoạn:

```
[Phase 1: EXPAND] ───────► [Phase 2: MIGRATE BATCHES] ───────► [Phase 3: CONTRACT]
Tạo trường mới song song    Di chuyển từng gói/module nhỏ        Xóa trường cũ khi
Hệ thống hỗ trợ cả 2        Mỗi batch 1 ticket riêng, CI xanh   call sites = 0
```

---

## Giai đoạn 1: EXPAND (Mở rộng song song) - Ticket `WR-01-EXPAND`
- **Blocked by**: None
- **Hành động**:
  - Thêm cột `account_uuid` vào database (nullable hoặc có default UUID).
  - Thêm getter/setter song song trong Model: `getAccountNumber()` và `getAccountUUID()`.
  - Giữ nguyên toàn bộ logic cũ không đổi.
- **Cam kết**: CI hoàn toàn **XANH** (Green) sau khi merge.

---

## Giai đoạn 2: MIGRATE BATCHES (Di chuyển theo lô an toàn)
Mỗi batch đại diện cho một domain boundary độc lập, kích thước vừa vặn một Context Window của AI Agent:

### Ticket `WR-02-BATCH-A`: Chuyển đổi Auth & Session Service
- **Blocked by**: `WR-01-EXPAND`
- **Scope**: `src/auth/*` (12 call sites)
- **Kiểm định**: Test suite của `auth` chạy độc lập chuyển sang sử dụng `account_uuid`.

### Ticket `WR-02-BATCH-B`: Chuyển đổi Billing & Invoice Service
- **Blocked by**: `WR-01-EXPAND`
- **Scope**: `src/billing/*` (25 call sites)
- **Kiểm định**: Toàn bộ unit test và integration test tính toán tiền tệ chuyển sang `account_uuid`.

### Ticket `WR-02-BATCH-C`: Chuyển đổi Frontend Client & Adapters
- **Blocked by**: `WR-01-EXPAND`
- **Scope**: `src/client/*`, `src/adapters/*` (17 call sites)
- **Kiểm định**: Giao diện người dùng và API calls gửi nhận `account_uuid`.

---

## Giai đoạn 3: CONTRACT (Thu hẹp & Dọn dẹp) - Ticket `WR-03-CONTRACT`
- **Blocked by**: `WR-02-BATCH-A`, `WR-02-BATCH-B`, `WR-02-BATCH-C`
- **Hành động**:
  - Chạy script kiểm tra grep toàn bộ codebase: đảm bảo số lượng `AccountNumber` còn lại là `0`.
  - Xóa bỏ deprecated method `getAccountNumber()`.
  - Chạy migration biến `account_uuid` thành `NOT NULL, UNIQUE`.
  - Xóa cột cũ `account_number` khỏi database.
- **Cam kết**: Codebase sạch sẽ, không nợ kỹ thuật (technical debt), CI xanh ở mọi bước.
