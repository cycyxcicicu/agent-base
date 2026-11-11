# Mẫu phân tích: sơ đồ bảng dữ liệu ERD (`type: erd`)

## A. Sơ đồ trả lời câu hỏi gì
**Dữ liệu của UC nằm ở những bảng nào, mỗi bảng có những cột nào dùng tới, các bảng nối nhau bằng khóa nào, cột nào có chỉ mục.** ERD không phải sơ đồ UML; ký hiệu là "chân quạ" (crow's foot). Quy ước dự án: `quy-trinh-ve-so-do-bang-json.md` mục 4.4 và 4.8. Kiến thức nền tiếng Việt: `assets/m2mba/posts/moi-quan-he-giua-cac-bang-trong-csdl/README.md`, `moi-quan-he-nhieu-nhieu-trong-thiet-ke-CSDL`, `kha-chnh-primary-key--ngha-v-vai-tr-trong-csdl`.

### Ký hiệu và nghĩa
| Hình | Nghĩa | JSON |
|---|---|---|
| Hộp có tên bảng ở đầu, mỗi hàng ba ô: tên cột, kiểu, khóa | Một bảng thật | `tables` |
| `PK` | Khóa chính | cột thứ ba của hàng |
| `FK` | Khóa ngoại | cột thứ ba |
| `UQ` | Duy nhất (unique) | cột thứ ba (ví dụ `"FK, UQ"` khi vừa khóa ngoại vừa duy nhất) |
| Hàng nền xám đậm, chữ đậm | Cột có chỉ mục (do Liquibase tạo) hoặc cột nhấn mạnh | `hot` |
| Đường từ cột PK (đầu `||`, "một") tới cột FK (đầu chân quạ, "nhiều") | Quan hệ: một hàng bên PK ứng nhiều hàng bên FK | `relations` |

## B. Cách phân tích
1. **Bảng nào:** các bảng mà hàm trong luồng đọc hoặc ghi (xem repository, DAO, entity). Mỗi bảng một lần.
2. **Cột nào:** chỉ cột liên quan luồng (cột lọc, cột trả ra, khóa nối) cộng khóa chính và khóa ngoại. Không liệt kê hết cột nếu không cần; ghi rõ "rút gọn".
3. **Tên và kiểu thật:** từ entity (`@Table`, `@Column`) và Liquibase; xác nhận với DB bằng truy vấn chỉ đọc (`information_schema.columns`, `pg_indexes`). Đừng suy ra kiểu từ tên.
4. **Khóa:** `PK`, `FK` và `UQ` lấy từ ràng buộc thật, không đoán.
5. **Chỉ mục:** chỉ đánh `hot` cho cột có chỉ mục thật (Liquibase hoặc `pg_indexes`).
6. **Quan hệ:** mỗi khóa ngoại một quan hệ từ CỘT khóa chính của bảng được tham chiếu tới CỘT khóa ngoại. Nhiều khóa ngoại cùng trỏ về một khóa chính (ví dụ sáu cột nhân viên) thì dùng `to_col` là danh sách.

## C. Phiếu phân tích cần điền
| Bảng | Cột | Kiểu | Khóa (PK/FK/UQ) | Có chỉ mục? | Cột này dùng ở bước nào của luồng | Nguồn (entity, Liquibase, DB) |
|---|---|---|---|---|---|---|

Quan hệ: | Bảng PK | Cột PK | Bảng FK | Cột FK | Nhãn ghi gì | Nguồn |

## D. Khung JSON
```json
{
  "type": "erd",
  "title": "<UC-xx>: ERD các bảng <chức năng> đọc và ghi",
  "note": "Chỉ cột liên quan và khóa. PK khóa chính, FK khóa ngoại, UQ duy nhất. Hàng xám đậm: cột có chỉ mục.",
  "out": "<UC-xx>-erd.drawio",
  "png": "<UC-xx>-erd.png",
  "tables": [
    {"id": "t_main", "col": 1, "name": "<bảng chính>", "hot": ["<cột có chỉ mục>"],
     "columns": [["id", "integer", "PK"], ["<cột>", "<kiểu>", ""], ["<cột khóa ngoại>", "integer", "FK"]]},
    {"id": "t_ref", "col": 0, "name": "<bảng được tham chiếu>",
     "columns": [["id", "integer", "PK"], ["<cột>", "<kiểu>", ""]]}
  ],
  "relations": [
    {"from": "t_ref", "from_col": "id", "to": "t_main", "to_col": "<cột khóa ngoại>", "label": "<tên cột FK hoặc: N khóa: ...>"}
  ]
}
```
Trường: `col` là cột đặt bảng (0 trái, 1 giữa, 2 phải); bảng chính ở giữa, bảng tham chiếu hai bên; `from` là bảng chứa khóa chính, `to` là bảng chứa khóa ngoại; `to_col` có thể là danh sách; nhãn ngắn (tên cột thật hoặc "N khóa: nhân viên").

## E. Bố trí
Hai bảng liên quan đặt ở hai cột khác nhau (công cụ báo lỗi nếu chồng nhau theo chiều ngang). Mỗi quan hệ một đường dọc riêng, nên không đặt hai bảng quan hệ cách nhau quá hẹp. Cảnh báo "đường cắt qua hộp" nghĩa là có bảng nằm giữa đường đi: dời bảng sang cột khác.

## F. Công cụ chưa vẽ
Quan hệ nhiều-nhiều qua bảng trung gian vẽ tay là hai quan hệ một-nhiều; quan hệ tùy chọn (0..1); khóa chính ghép; khóa ngoại tới bảng thuộc DB khác (ghi chú bằng chữ, ví dụ bảng ở iam-service).

## G. Lỗi hay gặp
- Nối bảng với bảng (không có cột) hoặc nhãn quan hệ không phải tên cột thật (`area_id` trong khi cột thật là `receiver_province_id`...).
- Liệt kê thiếu khóa ngoại thực sự dùng, hoặc cột UQ.
- Đánh dấu chỉ mục cho cột không có chỉ mục.
- Hai quan hệ khác nhau dùng chung một đường dọc (công cụ nay cảnh báo và tự tách).
- Dùng bảng thuộc DB khác (ví dụ `users` ở iam) mà không ghi rõ vì không có khóa ngoại thật giữa hai DB.

## H. Trước khi chạy
- Mỗi cột trong hình có trong phiếu với nguồn?
- Mỗi quan hệ nối đúng cột khóa chính tới cột khóa ngoại?
- Không có cảnh báo; đã xem ảnh.
