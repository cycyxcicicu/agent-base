# Mẫu phân tích: sơ đồ lớp (`type: class`)

## A. Sơ đồ trả lời câu hỏi gì
**Các kiểu (lớp, interface, enum) nào tham gia luồng của UC và chúng liên hệ nhau về CẤU TRÚC ra sao** (ai giữ ai, ai kế thừa ai, ai dùng ai). Không cho biết thứ tự chạy (sequence) hay nhánh (activity). Nguồn khái niệm: `assets/uml/class-diagram/{spec,classifier,association,generalization,dependency,interface,multiplicity}.md`; cách xây dựng: SourceMaking "Constructing Class Diagrams" (`assets/sourcemaking-uml/pages/modeling-it-systems/constructing-class-diagrams/README.md`).

### Ký hiệu và nghĩa (và `kind` trong JSON)
| Đường hoặc hình | Nghĩa | `kind` |
|---|---|---|
| Hộp ba ngăn: tên, thuộc tính, hàm | Một lớp. `+` công khai, `-` riêng tư. `stereo`: `interface`, `enumeration`, `Abstract` | `classes` |
| Nét liền, tam giác rỗng, mũi tên về lớp CHA | Kế thừa (`extends`, is-a): `from` là lớp con | `ext`, nhãn `Extends` |
| Nét đứt, tam giác rỗng, về interface | Cài đặt (`implements`): `from` là lớp cài đặt | `ext`, nhãn `implements` (dự án vẽ cùng kiểu `ext`) |
| Nét liền, thoi RỖNG ở phía lớp chứa | Aggregation: lớp này CÓ lớp kia, lớp kia sống độc lập | `agg` (`from` là lớp chứa) |
| Nét liền, thoi ĐẶC ở phía lớp chứa | Composition: lớp con chết theo lớp chứa | `comp` (`from` là lớp chứa) |
| Nét liền, mũi tên đặc | Liên kết: lớp này giữ tham chiếu tới lớp kia (QUY ƯỚC dự án; UML gốc dùng đầu hở) | `assoc` |
| Nét đứt, đầu hở | Phụ thuộc: lớp này chỉ dùng tạm lớp kia (tham số, biến cục bộ); từ client tới supplier | `dep` |

## B. Cách phân tích (từ SourceMaking, áp dụng cho mã nguồn)
1. **Chọn lớp:** chỉ các lớp xuất hiện trong luồng đã phân tích (sequence). Dùng `xerj_def` để lấy định nghĩa.
2. **Thuộc tính:** các field của lớp, kiểu thật. Chỉ ghi field liên quan luồng (tối đa khoảng 6 mỗi lớp) và ghi rõ nếu rút gọn.
3. **Hàm:** các hàm công khai mà luồng gọi (tên và kiểu tham số thật).
4. **Quan hệ:** (a) `extends` và `implements` trong khai báo lớp; (b) field có kiểu là lớp khác: xét vòng đời để chọn `agg`, `comp` hoặc `assoc` (nếu không chắc thì dùng `assoc`); (c) lớp khác chỉ xuất hiện trong thân hàm hoặc tham số: `dep`.
5. **Hai nửa nếu hai module:** thư viện dùng chung và service, đặt tách thật bằng `y` khác nhau; hộp tham chiếu cho lớp của module kia ghi rõ ("lớp của <module>").

## C. Phiếu phân tích cần điền
| Lớp (tên thật) | Module hoặc gói | Loại (class, interface, enum, abstract) | Thuộc tính (tên : kiểu) | Hàm (chữ ký) | Quan hệ tới lớp nào, loại, hướng | Nguồn (file:dòng) |
|---|---|---|---|---|---|---|

## D. Khung JSON
```json
{
  "type": "class",
  "title": "<UC-xx>: sơ đồ lớp <phạm vi>",
  "note": "Thoi rỗng: chứa. Mũi tên đặc: dùng. Mũi tên đứt: phụ thuộc. Tam giác rỗng: Extends hoặc implements.",
  "out": "<UC-xx>-class.drawio",
  "png": "<UC-xx>-class.png",
  "classes": [
    {"id": "i1", "x": 40, "y": 100, "w": 420, "stereo": "interface", "name": "<TênInterface>", "sub": "<nghĩa tiếng Việt>",
     "methods": ["+ <hàm>(<kiểu tham số>) : <kiểu trả về>"]},
    {"id": "c1", "x": 40, "y": 400, "w": 420, "name": "<TênLớp>", "sub": "<nghĩa tiếng Việt>",
     "attrs": ["- <tên> : <kiểu>"], "methods": ["+ <hàm>(<kiểu>) : <kiểu>"]},
    {"id": "c2", "x": 560, "y": 400, "w": 420, "name": "<TênLớpKhác>", "sub": "<nghĩa>",
     "attrs": ["- <tên> : <kiểu>"]}
  ],
  "relations": [
    {"from": "c1", "to": "i1", "kind": "ext", "label": "implements"},
    {"from": "c1", "to": "c2", "kind": "agg", "label": "<ghi chú ngắn>"}
  ]
}
```
Trường: `x`, `y`, `w` đặt vị trí và độ rộng (bội 10; ít lớp thì có thể dùng `col` thay `x`,`y`); `abstract: true` in nghiêng tên; `attrs`, `methods` bỏ trống thì hộp chỉ có tên (hộp tham chiếu).

## E. Bố trí
Cùng một nhóm lớp liên hệ chặt đặt cạnh nhau; lớp cha và interface ở trên lớp con; lớp trung tâm có nhiều quan hệ đặt giữa. Chừa khoảng trống rộng (tối thiểu 80 điểm) giữa các hộp có đường nối để nhãn không đè hộp. Nếu thấy cảnh báo "đè hộp" hoặc "chồng nhãn", dời hộp chứ đừng rút bớt quan hệ.

## F. Công cụ chưa vẽ
Bội số (1, 0..*) trên đường (luật dự án: ghi bằng chữ trong mô tả); vai trò tại đầu đường; khả năng điều hướng (dấu x); lớp mẫu (template); gói (package) bao quanh.

## G. Lỗi hay gặp
- Thiếu lớp có thật trong luồng (đã gặp: thiếu `GenericQueryEngine`, `InvalidFilterCriteriaException`) hoặc thêm lớp không dùng.
- Mọi quan hệ thành mũi tên đứt `dep`; không bao giờ dùng `agg`, `comp`, `ext`.
- Ghi chú "nửa trên, nửa dưới" nhưng vị trí không đúng như vậy.
- Đảo chiều: `ext` phải `from` lớp con `to` lớp cha; `agg` phải `from` lớp chứa.
- Bịa thuộc tính hoặc hàm không có trong mã; tên interface nhầm với lớp cài đặt.
- Ghi tên chung ("Generic Engine") thay vì tên lớp thật.

## H. Trước khi chạy
- Mỗi lớp trong hình có trong luồng của sequence? Mỗi quan hệ có dòng trong phiếu?
- Chiều và loại quan hệ đúng khai báo trong mã?
- Không có cảnh báo; đã xem ảnh.
