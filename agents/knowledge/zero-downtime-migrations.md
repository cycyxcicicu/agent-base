# Cẩm Nang Di Chuyển Cơ Sở Dữ Liệu Không Gián Đoạn (Zero-Downtime Database Migrations)

> **Tài liệu chuẩn kỹ thuật dành cho DBA, Architect và Backend Dev**  
> **Nguồn tri thức:** Trích xuất và tối ưu hóa từ `affaan-m/ECC` (Database Migration Patterns)

---

## 1. Năm Nguyên Tắc Bất Biến

1. **Mọi thay đổi đều phải là migration** — Tuyệt đối không bao giờ can thiệp sửa trực tiếp DB production bằng tay.
2. **Migration trên production chỉ đi tiến (Forward-Only)** — Muốn rollback thì tạo migration mới để tiến lên trạng thái mong muốn.
3. **Tách biệt DDL và DML** — Không bao giờ trộn lẫn việc thay đổi cấu trúc bảng (DDL) và cập nhật dữ liệu (DML) trong cùng một tệp migration.
4. **Kiểm thử trên tập dữ liệu tương đương production** — Migration chạy mượt trên 100 dòng test có thể làm treo cứng (Table Lock) hệ thống khi chạy trên 10 triệu dòng thật.
5. **Migration là bất biến (Immutable)** — Không sửa đổi nội dung file migration một khi đã được áp dụng lên production.

---

## 2. Checklist Kiểm Tra An Toàn Trước Khi Áp Dụng

- [ ] Migration có đủ cả hai chiều UP và DOWN (hoặc được đánh dấu rõ ràng là irreversible).
- [ ] Không gây khóa bảng toàn phần (`ACCESS EXCLUSIVE`) trên các bảng lớn trong giờ cao điểm.
- [ ] Mọi cột mới thêm vào bắt buộc phải là `NULLABLE` hoặc có giá trị `DEFAULT` an toàn.
- [ ] Chỉ mục (Index) trên bảng hiện có bắt buộc phải được tạo đồng thời (`CONCURRENTLY`).
- [ ] Các tác vụ cập nhật dữ liệu hàng loạt (Data Backfill) được chia thành nhiều mẻ nhỏ (Batching).
- [ ] Đã có kế hoạch hoàn tác (Rollback Plan) được ghi rõ trong task card.

---

## 3. Các Mẫu PostgreSQL Thực Chiến (Zero-Downtime Patterns)

### A. Thêm Cột Mới An Toàn

```sql
-- CHUẨN: Cột Nullable, không khóa bảng, chạy tức thì
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- CHUẨN: Cột có DEFAULT (Từ PostgreSQL 11 trở lên chạy tức thì, chỉ cập nhật metadata)
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- CẤM: NOT NULL mà không có DEFAULT trên bảng lớn (Gây khóa bảng toàn diện và viết lại mọi dòng)
-- ALTER TABLE users ADD COLUMN role TEXT NOT NULL;
```

### B. Tạo Chỉ Mục Không Gián Đoạn (Concurrent Indexing)

```sql
-- CẤM: Khóa toàn bộ thao tác ghi (INSERT/UPDATE/DELETE) trên bảng lớn trong thời gian build index
-- CREATE INDEX idx_users_email ON users (email);

-- CHUẨN: Không khóa bảng, cho phép các thao tác ghi diễn ra bình thường
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users (email);

-- LƯU Ý: Lệnh CONCURRENTLY không được đặt trong transaction block (BEGIN...COMMIT).
```

### C. Đổi Tên Cột Bằng Kỹ Thuật Expand - Contract (4 Bước)

Tuyệt đối không chạy `ALTER TABLE users RENAME COLUMN old_name TO new_name;` vì sẽ làm gãy ngay lập tức các phiên bản ứng dụng cũ đang chạy. Hãy làm theo 4 bước:

1. **Bước 1 (Migration 001 - Expand)**: Thêm cột mới.
   ```sql
   ALTER TABLE users ADD COLUMN display_name TEXT;
   ```
2. **Bước 2 (Migration 002 - Backfill)**: Đổ dữ liệu từ cột cũ sang cột mới.
   ```sql
   UPDATE users SET display_name = username WHERE display_name IS NULL;
   ```
3. **Bước 3 (Code Deploy)**: Cập nhật ứng dụng để đọc/ghi đồng thời vào cả 2 cột. Deploy ứng dụng an toàn.
4. **Bước 4 (Migration 003 - Contract)**: Khi ứng dụng mới đã chạy ổn định 100%, xóa cột cũ.
   ```sql
   ALTER TABLE users DROP COLUMN username;
   ```

### D. Cập Nhật Dữ Liệu Lớn Bằng Kỹ Thuật Batching (Tránh Khóa DB)

```sql
-- CHUẨN: Cập nhật từng mẻ 10.000 dòng, giải phóng khóa sau mỗi mẻ
DO $$
DECLARE
  batch_size INT := 10000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE users
    SET normalized_email = LOWER(email)
    WHERE id IN (
      SELECT id FROM users
      WHERE normalized_email IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    RAISE NOTICE 'Đã cập nhật % dòng...', rows_updated;
    EXIT WHEN rows_updated = 0;
    COMMIT;
  END LOOP;
END $$;
```
