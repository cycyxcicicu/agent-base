# Mẫu phân tích: sơ đồ trạng thái (`type: statemachine`)

## A. Sơ đồ trả lời câu hỏi gì
**Một đối tượng (ví dụ đơn hàng) có những trạng thái nào trong vòng đời, sự kiện nào đổi trạng thái nào, và chuyển nào KHÔNG được phép.** Nguồn khái niệm: `assets/uml/state-machine-diagram/{spec,examples}.md`; cách xây dựng: SourceMaking "Constructing Statechart Diagrams" (`assets/sourcemaking-uml/pages/modeling-it-systems/constructing-statechart-diagrams/README.md`, `.../the-life-of-an-object/README.md`).

### Ký hiệu và nghĩa
| Hình | Nghĩa | JSON |
|---|---|---|
| Chấm đen nhỏ | Trạng thái bắt đầu (initial pseudostate): tối đa một mỗi vùng, đúng một chuyển đi ra, không có chuyển đi vào | `kind: initial` |
| Hộp bo góc, tên đậm | Một trạng thái. Ngăn dưới (tùy chọn): hoạt động bên trong `entry / ...`, `do / ...`, `exit / ...` | `kind: state`, `label`, `actions` |
| Hình thoi | Nút chọn (choice): nhiều chuyển ra, mỗi chuyển có điều kiện `[...]`, nên có nhánh `[else]` | `kind: choice` |
| Chấm đen trong vòng tròn | Trạng thái kết thúc (final): không có chuyển đi ra | `kind: final` |
| Khung bao nhiều trạng thái con | Trạng thái ghép (composite): đặt `parent` cho các trạng thái con | `parent` |
| Mũi tên có nhãn `sự_kiện [điều_kiện] / hành_động` | Chuyển trạng thái: khi có sự kiện, nếu điều kiện đúng thì đổi trạng thái và làm hành động | `transitions[].label` |

## B. Cách phân tích (SourceMaking, áp dụng cho mã nguồn)
1. **Lấy danh sách trạng thái thật** từ enum hoặc bảng mã trạng thái (ví dụ `doc/thiet-ke/05-process-status`); không tự đặt tên.
2. **Tìm mọi nơi đổi trạng thái** trong mã (hàm gán trạng thái, job, listener): mỗi nơi là một mũi tên; sự kiện là điều gây ra việc đổi.
3. **Nhóm theo vòng đời:** sinh ra (initial), sống, kết thúc (final).
4. **Với mỗi sự kiện hỏi:** được phép ở những trạng thái nào, ở trạng thái nào thì KHÔNG? Sau sự kiện thì vào trạng thái nào? Điều kiện (guard) là gì?
5. **Hành động đi kèm:** việc hệ thống làm khi chuyển (ghi nhật ký, gửi tin, hoàn kho).

## C. Phiếu phân tích cần điền
| Trạng thái hiện tại | Sự kiện (tác nhân gây ra) | Điều kiện | Trạng thái tiếp theo | Hành động | Nguồn (hàm, file:dòng) |
|---|---|---|---|---|---|
Cuối phiếu thêm danh sách **chuyển bị cấm quan trọng** (ví dụ không đi từ "Đã giao" về "Đang giao") để ghi vào mô tả.

## D. Khung JSON
```json
{
  "type": "statemachine",
  "title": "<UC-xx>: máy trạng thái của <đối tượng>",
  "note": "Chuyển ghi: sự_kiện [điều_kiện] / hành_động. Trạng thái lấy từ enum thật.",
  "out": "<UC-xx>-statemachine.drawio",
  "png": "<UC-xx>-statemachine.png",
  "states": [
    {"id": "i", "kind": "initial", "col": 0, "row": 0},
    {"id": "s1", "label": "<Trạng thái 1 (tên enum)>", "col": 0, "row": 1.2, "actions": ["entry / <việc làm khi vào>"]},
    {"id": "s2", "label": "<Trạng thái 2>", "col": 1.3, "row": 1.2},
    {"id": "s3", "label": "<Trạng thái 3>", "col": 1.3, "row": 3},
    {"id": "f", "kind": "final", "col": 0, "row": 4.3}
  ],
  "transitions": [
    {"from": "i", "to": "s1"},
    {"from": "s1", "to": "s2", "label": "<sự kiện> [<điều kiện>] / <hành động>"},
    {"from": "s2", "to": "s3", "label": "<sự kiện khác>"},
    {"from": "s3", "to": "f", "label": "<sự kiện kết thúc>"}
  ]
}
```
Trường: `col`, `row` (số thực được; một cột khoảng 300 điểm, một hàng khoảng 130 điểm), `actions` (các dòng hoạt động trong), `parent` (id trạng thái ghép), `via` (x của đường vòng), `first: "v"` (đi xuống trước).

## E. Bố trí
Đặt các trạng thái theo trục thời gian trái sang phải; các trạng thái kết thúc nhánh phụ (hủy, lỗi) xuống hàng dưới; trạng thái cuối ở cuối cùng. Chuyển quay ngược dùng `via` để đường vòng không cắt hộp. Trạng thái ghép: đặt các con sát nhau rồi dùng `parent`; khung bao tự dựng, đừng đặt trạng thái khác vào trong khung.

## F. Công cụ chưa vẽ
Fork, join, history (H), vùng trực giao (nhiều region), điểm vào ra (entry/exit point), chuyển nội bộ. Ghi trong mô tả tài liệu.

## G. Lỗi hay gặp
Tự đặt tên trạng thái; thiếu trạng thái kết thúc hoặc trạng thái đầu; trạng thái cụt (không có chuyển ra mà không phải final); nhãn mũi tên chỉ ghi sự kiện mà không ghi điều kiện và hành động; hai chuyển cùng sự kiện từ một trạng thái không có điều kiện phân biệt; không nêu chuyển bị cấm.

## H. Trước khi chạy
Mỗi trạng thái có tên đúng enum? Mỗi mũi tên có dòng trong phiếu với nguồn? Mọi trạng thái với tới được từ initial? `--check-only` đạt, đã xem ảnh.
