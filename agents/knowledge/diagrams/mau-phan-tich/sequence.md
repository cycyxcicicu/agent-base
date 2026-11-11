# Mẫu phân tích: sơ đồ tuần tự (`type: sequence`)

## A. Sơ đồ trả lời câu hỏi gì
**Theo THỜI GIAN, đối tượng nào gọi đối tượng nào, thông điệp gì, nhận lại gì, cho MỘT kịch bản.** Không trả lời "có những nhánh nào" (đó là activity). Nguồn khái niệm: `assets/uml/sequence-diagram/{spec,messages,fragments,interaction}.md`; cách xây dựng: SourceMaking "Constructing Sequence Diagrams" (`assets/sourcemaking-uml/pages/modeling-it-systems/constructing-sequence-diagrams/README.md`).

### Ký hiệu và nghĩa
| Hình hoặc đường | Nghĩa | JSON |
|---|---|---|
| Hộp ở đầu cột + đường đứt dọc | Một đối tượng (lifeline); cột trái sang phải theo thứ tự gọi | `participants` |
| Mũi tên liền, đầu đặc | Gọi ĐỒNG BỘ: gửi và chờ kết quả | `messages` `kind: call` (mặc định) |
| Mũi tên liền, đầu hở | Gọi BẤT ĐỒNG BỘ: gửi rồi chạy tiếp, không chờ | `kind: async` |
| Mũi tên nét đứt, đầu hở | Trả về (reply) | `kind: return` |
| Mũi tên vòng lại chính nó | Tự gọi | `kind: self` |
| Số thứ tự trước nhãn | Thứ tự gọi (không đánh số cho `return`) | tự động |
| Chưa có: khung `alt`/`opt`/`loop`/`par`, create, delete, lost, found | Có trong nguồn (`fragments.md`, `messages.md`) | ghi nhánh bằng nhãn "[điều kiện]" và nói trong mô tả |

## B. Cách phân tích (từ SourceMaking, áp dụng cho mã nguồn)
1. **Chọn MỘT kịch bản** (thường là đường chính, ví dụ "lọc danh sách thành công"). Nhánh lỗi để activity lo.
2. **Điểm vào:** hàm đầu tiên nhận yêu cầu (controller, job `@Scheduled`, listener). Đó là đối tượng thứ hai sau "Trình duyệt" hoặc tác nhân.
3. **Đi theo lời gọi:** dùng `xerj_def` tìm hàm, đọc thân hàm, ghi mỗi lần gọi sang LỚP KHÁC (không ghi gọi hàm cùng lớp trừ khi đáng chú ý, khi đó dùng `self`). Chỉ cần đối tượng thật sự có mặt (xem mục G).
4. **Trả về:** chỉ vẽ `return` khi trả dữ liệu đáng chú ý hoặc khi bước đó là mốc của luồng. Đừng vẽ `return` rỗng cho mọi lời gọi.
5. **Lớp gọi đúng:** ghi lớp thực sự là người gọi (ví dụ lớp service, không phải lớp builder được service gọi).

## C. Phiếu phân tích cần điền
| STT | Từ (lớp thật) | Tới (lớp thật) | Hàm hoặc việc làm | Tham số, kết quả đáng chú ý | Nguồn (file:dòng) | Đồng bộ? |
|---|---|---|---|---|---|---|

## D. Khung JSON
```json
{
  "type": "sequence",
  "title": "<UC-xx>: sơ đồ tuần tự <kịch bản>",
  "note": "<một câu: kịch bản nào, nhánh lỗi xem sơ đồ hoạt động>",
  "out": "<UC-xx>-sequence.drawio",
  "png": "<UC-xx>-sequence.png",
  "participants": [
    {"id": "ui", "name": "Trình duyệt\n(<ứng dụng giao diện>)"},
    {"id": "ctl", "name": "<Vai trò ngắn>\n(<TênLớpThật>)"},
    {"id": "db", "name": "PostgreSQL"}
  ],
  "messages": [
    {"from": "ui", "to": "ctl", "label": "<hành động: gọi API gì>"},
    {"from": "ctl", "to": "ctl", "kind": "self", "label": "<việc tự xử lý đáng chú ý>"},
    {"from": "ctl", "to": "db", "label": "<câu truy vấn hoặc hàm>"},
    {"from": "db", "to": "ctl", "kind": "return", "label": "<kết quả>"},
    {"from": "ctl", "to": "ui", "kind": "return", "label": "<kết quả trả ra>"}
  ]
}
```
Trường: `participants[].name` có thể hai dòng ("vai trò\n(Tên lớp)"); `messages` đi theo thứ tự thời gian từ trên xuống; `color` bỏ trống (đen trắng).

## E. Bố trí
Đối tượng xếp trái sang phải theo thứ tự lần đầu xuất hiện trong luồng gọi. Một đối tượng không nằm ở giữa hai đối tượng mà nó không gọi: nếu mũi tên đi qua nhiều cột, xem lại thứ tự cột.

## F. Công cụ chưa vẽ
Khung `alt`, `opt`, `loop`, `par`, `break`; thông điệp create, delete; vạch kích hoạt (activation bar). Mô tả bằng chữ dưới hình.

## G. Lỗi hay gặp
- Người gọi sai (bỏ lớp trung gian): đọc lại thân hàm.
- Đối tượng ghi bằng chức năng chung ("Generic Engine") thay vì lớp thật, hoặc gộp hai lớp thành một cột mà không ghi rõ.
- Gộp nhiều kịch bản vào một hình; vẽ cả nhánh lỗi.
- Bịa tên hàm không có trong mã (đã gặp: `getSourceOrders` trong khi thật là `findRows`).
- Dán `return` cho mọi lời gọi làm hình dài mà không có thông tin.

## H. Trước khi chạy
- Mỗi hàng của phiếu có nguồn? Thứ tự gọi khớp thân hàm?
- Mỗi cột (đối tượng) có ít nhất một mũi tên đi vào và ra?
- `--check-only` đạt, đã xem ảnh.
