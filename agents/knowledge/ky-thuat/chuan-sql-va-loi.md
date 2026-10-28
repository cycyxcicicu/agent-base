# Chuẩn SQL và xử lý lỗi cơ sở dữ liệu

> **Loại: tham khảo.** Chép từ dự án gdt-workspace để làm tri thức cho agent, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Còn nhắc Liquibase theo cấu hình của gdt.

Bổ sung cho `doc/ky-thuat/engineering/persistence-conventions.md` và `liquibase-conventions.md`. Khi khác nhau, các file đó thắng. Các mục "Đề xuất" là chưa có quy định chính thức.

## 1. Nguyên tắc

**Việc cơ sở dữ liệu làm tốt thì làm ở truy vấn, không kéo dữ liệu lên service rồi xử lý bằng vòng lặp.** Lý do: DB có chỉ mục, tối ưu truy vấn và chạy gần dữ liệu; kéo lên service tốn mạng, bộ nhớ và chậm khi dữ liệu tăng.

| Việc | Nơi làm | Cách làm | Lý do |
|---|---|---|---|
| Lọc, sắp xếp, phân trang | DB | `Specification`, derived query, `Pageable` | DB dùng chỉ mục; service chỉ nhận một trang |
| Đếm, tổng, nhóm (KPI) | DB | JPQL `group by`, `count`, `sum`, projection | Không `findAll` rồi `stream` |
| Lấy một số cột | DB | Projection, đọc theo vị trí cột | Tránh nạp entity đầy đủ |
| Ghép dữ liệu liên quan | DB | `join`, entity graph; hoặc một truy vấn gộp theo danh sách id của trang | Tránh N+1 |
| Toàn vẹn dữ liệu | DB | `UNIQUE`, `FK`, `NOT NULL`, `CHECK` | Chốt chặn cuối khi có đồng thời |
| Chống trùng, tạo nếu chưa có | DB | Ràng buộc unique và xử lý vi phạm | "Kiểm tra rồi chèn" ở service có lỗ hổng đồng thời |
| Quy tắc nghiệp vụ nhiều nhánh | Service | Use case | DB không hợp để biểu diễn |
| Gọi hệ thống ngoài | Service | Adapter, ngoài giao dịch | Giao dịch phải ngắn |
| Nhãn hiển thị, dịch, định dạng | Service/ Frontend | Mapper, i18n | Không thuộc dữ liệu |

## 2. Quy tắc truy vấn

1. **Không `nativeQuery`** trong repository. Dùng derived query, JPQL, `Specification`, entity graph, `@Lock`, `Pageable`. Nếu thật sự không diễn đạt được, hỏi người dùng và ghi ADR trước khi dùng (đề xuất).
2. **Mọi kết quả có thể không giới hạn đều phân trang.** Bảng lớn (đơn hàng): lấy danh sách id theo thứ tự một lần, rồi đọc từng trang theo id.
3. **Chỉ lấy cột cần.** Màn có chọn cột thì join bảng phụ chỉ khi cột được chọn.
4. **Tránh N+1:** nạp liên quan bằng một truy vấn gộp theo danh sách id.
5. **Danh sách `IN` lớn thì chia lô** (đề xuất: tối đa vài nghìn phần tử mỗi lô).
6. **Không dùng hàm trên cột lọc** khi làm mất chỉ mục (ví dụ `lower(col) = ...` khi cột có chỉ mục thường).
7. **Chỉ mục:** thêm chỉ mục cho cột lọc và sắp xếp thường dùng; kiểm tra bằng `EXPLAIN` trên dữ liệu đủ lớn trước khi chốt.
8. **Không đếm tổng nếu không cần.** Đếm trên bảng rất lớn tốn kém.
9. **Truy vấn tham số hoá;** không nối chuỗi.
10. **Đọc lâu thì đặt giới hạn thời gian truy vấn** và `readOnly`.
11. **Câu `@Query` dài hơn một dòng viết bằng text block `"""..."""`**, mỗi mệnh đề (`SELECT`, `FROM`, `WHERE`, `ORDER BY`...) một dòng; **không nối chuỗi bằng `+`**. Áp dụng cho mọi repository, code mới và cả code cũ khi sửa tới. Ví dụ:
   ```java
   @Query("""
       SELECT s FROM StaffEntity s
       WHERE s.iamUserId IN :ids
       ORDER BY s.id ASC
       """)
   ```
   Ngoại lệ có chủ ý về `nativeQuery` (ví dụ `FOR UPDATE SKIP LOCKED` kèm `LIMIT` ở `UserEventOutboxRepositoryJPA` của iam) vẫn viết bằng text block.

## 3. Giao dịch

- Đặt ở tầng application, ngắn, rõ phạm vi. Đọc dùng `@Transactional(readOnly = true)`.
- Không gọi mạng (Pancake, J&T, address-parser) trong giao dịch.
- Khoá bi quan chỉ cho bất biến thật sự cần; kiểm tra lại điều kiện sau khi lấy khoá.
- Ghi dữ liệu hàng loạt theo lô, dọn bộ nhớ phiên sau mỗi lô.

## 4. Lỗi cơ sở dữ liệu

Nguyên tắc: **bắt và chuyển đổi ở một nơi** (bộ xử lý lỗi chung của controller hoặc adapter), không `try/catch` rải rác; không nuốt lỗi; không trả thông điệp gốc của DB ra người dùng.

| Lỗi | Ý nghĩa | Xử lý | Phản hồi người dùng |
|---|---|---|---|
| Vi phạm unique (`DataIntegrityViolationException`) | Trùng dữ liệu | Chuyển thành lỗi nghiệp vụ theo tên ràng buộc | 409, thông điệp nghiệp vụ tiếng Việt (ví dụ "Đơn đã tồn tại") |
| Vi phạm khoá ngoại, `NOT NULL` | Dữ liệu tham chiếu thiếu hoặc lỗi đầu vào | Nếu do đầu vào: 400. Nếu do lỗi code: log và 500 | Thông điệp chung, không lộ tên bảng, cột |
| Khoá lạc quan (`OptimisticLockingFailureException`) | Dữ liệu bị người khác sửa | 409 | "Dữ liệu đã thay đổi, vui lòng tải lại" |
| Deadlock, hết thời gian chờ khoá | Tranh chấp | Thử lại tối đa 3 lần nếu thao tác idempotent (đề xuất); không thì báo thử lại | "Hệ thống đang bận, vui lòng thử lại" |
| Hết thời gian truy vấn, mất kết nối | Hạ tầng | Không thử lại mù; log; 503 | "Hệ thống tạm thời không phản hồi" |
| Lỗi cú pháp, ánh xạ (`BadSqlGrammar`, mapping) | Lỗi code hoặc migration | Là bug: log đầy đủ, 500, sửa code | Thông điệp chung |

Quy tắc:
1. **Đặt tên ràng buộc có quy ước** để ánh xạ được: `uk_<bảng>_<cột>`, `fk_<bảng>_<bảng-tham-chiếu>`, `ck_<bảng>_<ý>`.
2. **Mỗi ràng buộc người dùng có thể chạm tới có thông điệp nghiệp vụ riêng.**
3. **Log:** ghi loại lỗi, tên ràng buộc, mã yêu cầu hoặc mã đơn. Không ghi giá trị cá nhân.
4. **Giao dịch rollback đúng:** ngoại lệ đã kiểm tra (checked) mặc định không rollback; khai báo `rollbackFor` khi cần.
5. **Hàng loạt:** lỗi một dòng không làm hỏng cả lô nếu nghiệp vụ cho phép; trả danh sách dòng lỗi.
6. **Idempotent:** thao tác có thể bị gọi lại (webhook, job, người dùng bấm hai lần) phải an toàn khi lặp, dựa vào ràng buộc unique.
7. **Test** có ít nhất một test cho mỗi ánh xạ lỗi người dùng chạm tới (Testcontainers cho ràng buộc thật).

## 5. Liquibase và dữ liệu

- Theo `liquibase-conventions.md`: changeset mới, không sửa changeset đã chạy, `author: ducnvh`, có `.rollback.sql`.
- Thay đổi lớn theo mẫu mở rộng rồi thu gọn: thêm cột, ghi cả hai, chuyển, xoá cột cũ ở lần sau.
- Tạo chỉ mục trên bảng lớn: dùng `CREATE INDEX CONCURRENTLY` ở changeset không nằm trong giao dịch (đề xuất; cần kiểm tra trên PostgreSQL thật).
- Điền dữ liệu bù (backfill) theo lô, không một câu lệnh khoá cả bảng.
- Skill hỗ trợ: `database-migrations`, `postgres-patterns`, `jpa-patterns`.

## 6. Checklist

- [ ] Lọc, sắp xếp, nhóm, phân trang nằm trong truy vấn.
- [ ] Không N+1; chỉ lấy cột cần; có chỉ mục phù hợp.
- [ ] Không `nativeQuery`, hoặc có ADR được duyệt.
- [ ] Giao dịch ngắn, không gọi mạng bên trong.
- [ ] Ràng buộc unique, khoá ngoại, `NOT NULL` có ở DB.
- [ ] Mỗi lỗi DB người dùng chạm tới có ánh xạ và thông điệp tiếng Việt.
- [ ] Không lộ tên bảng, cột, câu SQL ra người dùng.
- [ ] Có test cho lỗi chính.

## 7. Câu hỏi mở

Đã chốt (18/10/2026): xử lý ở SQL những gì DB làm tốt, không kéo dữ liệu lên service để xử lý bằng code (mục 1).

1. `nativeQuery` bị cấm: có cho ngoại lệ khi báo cáo nặng không?
2. Số lần thử lại và kích thước lô có số cụ thể của công ty không?
