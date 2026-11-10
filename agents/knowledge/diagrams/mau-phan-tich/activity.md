# Mẫu phân tích: sơ đồ hoạt động (`type: activity`)

## A. Sơ đồ trả lời câu hỏi gì
**Việc diễn ra theo thứ tự nào, LỚP hoặc THÀNH PHẦN nào làm từng bước, rẽ nhánh ở đâu, lỗi đi đâu.** Nó là sơ đồ duy nhất cho thấy ĐẦY ĐỦ nhánh của luồng. Nguồn khái niệm: `assets/uml/activity-diagram/{spec,actions,controls,objects}.md`; cách xây dựng: SourceMaking "Constructing Activity Diagrams" (`assets/sourcemaking-uml/pages/modeling-business-systems/constructing-activity-diagrams/README.md`, `.../modeling-for-system-integration/activity-diagrams/README.md`).

### Ký hiệu và nghĩa
| Hình hoặc đường | Nghĩa | JSON |
|---|---|---|
| Chấm đen | Điểm bắt đầu. Được phép nhiều điểm bắt đầu (mỗi luồng chạy độc lập: HTTP, job, listener có điểm riêng) | `kind: start` |
| Chấm đen trong vòng tròn | Kết thúc (activity final). Được phép nhiều điểm kết thúc | `kind: end` (`note` ghi kết quả) |
| Hộp bo góc | Một bước làm (action) | `kind: proc` |
| Hộp bo góc viền đậm | Bước xử lý lỗi (dự án) | `kind: err` |
| Hình thoi | Rẽ nhánh (decision): một vào nhiều ra, mỗi nhánh có điều kiện `[...]`. Cũng dùng hình thoi cho điểm gộp (merge) | `kind: dec` (nhánh ra ghi `label`) |
| Chấm tròn nhỏ | Điểm nối để các nhánh gộp về trước khi tiếp | `kind: junc` |
| Làn (cột) | MỘT lớp hoặc thành phần chạy mã làm bước đó | `lanes` |
| Mũi tên liền | Trình tự điều khiển trong cùng một làn | tự động |
| Mũi tên nét đứt sang làn khác | Lời gọi hoặc message giữa các làn (QUY ƯỚC của mẫu anhbv, không phải UML gốc) | tự động; nhãn ngắn bắt buộc |
| Chưa có: fork và join (song song), object flow | Có trong nguồn (`controls.md`, `objects.md`) | ghi trong mô tả |

## B. Cách phân tích (từ SourceMaking, áp dụng cho mã nguồn)
1. **Tìm điểm vào** của mọi luồng chạy: HTTP controller, `@Scheduled`, `@RabbitListener`, sự kiện. Mỗi điểm vào là một điểm bắt đầu.
2. **Lấy chuỗi lời gọi** từ sequence đã phân tích (cùng nguồn), đi qua MỖI hàm thật.
3. **Tìm mọi điểm rẽ:** `if/else`, `switch`, `throw`, `try/catch`, vòng lặp `for/while`, kiểm tra null. Mỗi điểm rẽ là một hình thoi; mỗi `throw` là một nhánh lỗi tới nơi bắt (lớp bắt lỗi chung) rồi tới nơi trả lỗi (mã HTTP, mã lỗi).
4. **Vòng lặp** là nhánh quay lại (dùng `via` để đường vòng đi sát mép làn).
5. **Gán làn:** mỗi bước nằm ở làn của LỚP thực hiện nó. Lời gọi sang lớp khác là mũi tên nét đứt có nhãn.
6. **Ghi kết quả ở điểm kết thúc** (`note`): "trả HTTP 200", "trả HTTP 400 mã ...".

## C. Phiếu phân tích cần điền
| STT | Lớp (làn) | Bước làm (một việc) | Rẽ nhánh? điều kiện, ghi `[Có]/[Không]` | Nhánh lỗi tới đâu (lớp bắt, mã) | Nguồn (file:dòng) |
|---|---|---|---|---|---|

## D. Khung JSON
```json
{
  "type": "activity",
  "title": "<UC-xx>: sơ đồ hoạt động <luồng>",
  "note": "Mỗi làn là một lớp hoặc thành phần. Nét đứt là lời gọi sang làn khác. Mã lỗi nội bộ để trong tài liệu.",
  "out": "<UC-xx>-activity.drawio",
  "png": "<UC-xx>-activity.png",
  "lanes": [
    {"id": "ui", "name": "Giao diện\n(<ứng dụng>)"},
    {"id": "ctl", "name": "<Controller>\n(<TênLớp>)"},
    {"id": "svc", "name": "<Service>\n(<TênLớp>)"},
    {"id": "db", "name": "PostgreSQL"}
  ],
  "nodes": [
    {"id": "s1", "kind": "start", "lane": "ui", "row": 0},
    {"id": "a1", "kind": "proc", "lane": "ui", "row": 1, "label": "<bước đầu của người dùng>"},
    {"id": "a2", "kind": "proc", "lane": "ctl", "row": 2, "label": "<nhận yêu cầu>"},
    {"id": "d1", "kind": "dec", "lane": "svc", "row": 3, "label": "<điều kiện hợp lệ?>"},
    {"id": "x1", "kind": "err", "lane": "svc", "sub": 1, "row": 3, "label": "<ném lỗi gì>"},
    {"id": "e1", "kind": "end", "lane": "svc", "sub": 1, "row": 4, "note": "Kết thúc: <HTTP, mã lỗi>"},
    {"id": "a3", "kind": "proc", "lane": "db", "row": 5, "label": "<truy vấn>"},
    {"id": "e2", "kind": "end", "lane": "ui", "row": 6, "note": "Kết thúc: <kết quả>"}
  ],
  "edges": [
    {"from": "s1", "to": "a1"},
    {"from": "a1", "to": "a2", "label": "<gọi API>"},
    {"from": "a2", "to": "d1", "label": "<gọi service>"},
    {"from": "d1", "to": "x1", "label": "Không"},
    {"from": "x1", "to": "e1"},
    {"from": "d1", "to": "a3", "label": "Có", "first": "v"},
    {"from": "a3", "to": "e2", "label": "<kết quả>", "first": "v"}
  ]
}
```
Trường: `row` (số thực được; một hàng khoảng 115 điểm, đặt theo thứ tự thời gian), `sub` (cột con trong làn; nhánh phụ đặt `sub: 1` cùng hàng với hình thoi), nhãn nút quyết định tối đa khoảng 60 ký tự, nút việc tối đa khoảng 120. Cạnh khác cột: mặc định đi ngang rồi xuống; `first: "v"` đi xuống trước rồi rẽ ngang; `via: <x>` vòng qua đường dọc tại x (vòng lặp, đặt sát mép trái của làn).

## E. Quy tắc làn
Mỗi làn đúng MỘT lớp hoặc thành phần chạy mã (hoặc "Người dùng", "Giao diện" ở đầu). KHÔNG tạo làn "Nhánh lỗi", "Kết thúc", "Chung". Thứ tự làn theo thứ tự gọi; hai lớp gọi nhau liên tục đặt kề nhau.

## F. Công cụ chưa vẽ
Fork và join (song song), object flow, partition lồng nhau, khung vùng ngắt (interruptible region). Mô tả trong tài liệu.

## G. Lỗi hay gặp
- Làn không phải lớp (làn "Nhánh lỗi và kết thúc" ở UC-06); gộp "Người dùng & Trình duyệt".
- Thu một chuỗi kiểm tra thành một ô "hợp lệ?" và bỏ các nhánh con (số điều kiện, thiếu, trùng, ngoài danh mục...).
- Nhánh lỗi dừng ở "Ném lỗi" mà không tới nơi bắt lỗi và trả lỗi; thiếu nhánh lỗi hệ thống (HTTP 500).
- Cạnh liên làn không có nhãn; nhãn quá dài đè hộp.
- Vẽ `[Có]/[Không]` nhưng thiếu một nhánh.
- Bịa con số (kích thước trang, giới hạn) không có trong tài liệu hoặc cấu hình.

## H. Trước khi chạy
- Mỗi `if`, `throw` trong các hàm đã đi qua có một hình thoi hoặc một nhánh lỗi?
- Mỗi hình thoi đủ nhánh có nhãn? Mỗi nút (trừ kết thúc) có đường ra? Mỗi điểm bắt đầu tới được một điểm kết thúc?
- Mỗi làn là một lớp thật? Không có cảnh báo "đè hộp", "chồng nhãn"?
- Đã xem ảnh.
