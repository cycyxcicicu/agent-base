# Mẫu phân tích: sơ đồ thành phần (`type: component`)

## A. Sơ đồ trả lời câu hỏi gì
**Hệ thống chia thành những thành phần phần mềm nào, mỗi thành phần cung cấp giao diện gì và cần giao diện của thành phần nào.** Nguồn khái niệm: `assets/uml/component-diagram/{spec,component,port}.md`.

### Ký hiệu và nghĩa
| Hình | Nghĩa | JSON |
|---|---|---|
| Hộp có nhãn «component» | Một thành phần (module phần mềm có ranh giới rõ) | `components` (`stereo` đổi từ khóa, ví dụ `service`) |
| Chấm tròn nối vào cạnh hộp ("kẹo mút") | Giao diện CUNG CẤP (provided): thành phần thực hiện giao diện đó | `provides: ["TênGiaoDiện"]` |
| Mũi tên nét đứt «use» từ thành phần tới chấm tròn | Giao diện CẦN (required): thành phần này dùng giao diện đó (UML chỉ định required interface bằng usage dependency) | `connections` `kind: uses` + `interface` |
| Mũi tên nét đứt giữa hai hộp | Phụ thuộc chung chung | `connections` `kind: dependency` |
| Khung chữ nhật có tên | Ranh giới hệ thống hoặc nhóm | `boundaries` |

## B. Cách phân tích
1. **Chọn mức:** thành phần ở mức module hoặc service (ví dụ `accounting-service`, `iam-service`, thư viện `ws-library`, giao diện `ws-acct-frontend`), không phải từng lớp (đó là sơ đồ lớp).
2. **Cung cấp gì:** mỗi thành phần phơi ra giao diện nào (API, interface, topic). Chỉ ghi giao diện có thành phần khác dùng.
3. **Cần gì:** thành phần gọi hoặc phụ thuộc thành phần nào, qua giao diện nào (REST client, Feign, thư viện).
4. **Ranh giới:** thành phần nào thuộc cùng một hệ thống (khung), thành phần nào là hệ thống ngoài.

## C. Phiếu phân tích cần điền
| Thành phần | Loại (service, thư viện, giao diện...) | Giao diện cung cấp | Thành phần nó cần, qua giao diện nào | Nguồn (cấu hình, mã, tài liệu) |
|---|---|---|---|---|

## D. Khung JSON
```json
{
  "type": "component",
  "title": "<UC-xx>: sơ đồ thành phần <phạm vi>",
  "note": "Chấm tròn là giao diện cung cấp; mũi tên nét đứt «use» là thành phần cần giao diện đó.",
  "out": "<UC-xx>-component.drawio",
  "png": "<UC-xx>-component.png",
  "components": [
    {"id": "c1", "label": "<Thành phần 1>", "col": 0, "row": 0},
    {"id": "c2", "label": "<Thành phần 2>", "col": 1, "row": 0, "provides": ["<TênGiaoDiện>"]}
  ],
  "boundaries": [{"label": "<Hệ thống>", "members": ["c1", "c2"]}],
  "connections": [
    {"from": "c1", "to": "c2", "kind": "uses", "interface": "<TênGiaoDiện>", "label": "<giao thức>"}
  ]
}
```
Trường: `col`, `row` đặt vị trí (một cột khoảng 380 điểm); `pside` (`left` hoặc `right`) ép phía chấm tròn, mặc định tự chọn phía thành phần dùng; `kind` mặc định `uses` (bắt buộc `interface` và `to` phải `provides` nó).

## E. Lỗi hay gặp
Vẽ từng lớp thay vì module; giao diện không có ai dùng; thành phần cô lập; mũi tên xuyên qua hộp khác (đổi vị trí cột); quên ranh giới hệ thống nên không phân biệt thành phần của mình với hệ thống ngoài.

## F. Công cụ chưa vẽ
Cổng (port), connector lắp ghép (assembly) dạng kẹo mút khớp ổ cắm, ủy quyền (delegation), thành phần lồng nhau. Ghi trong mô tả.

## G. Trước khi chạy
Mỗi thành phần và giao diện có nguồn? Mỗi giao diện cung cấp có người dùng? `--check-only` đạt, đã xem ảnh.
