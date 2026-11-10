# Mẫu phân tích: sơ đồ gói (`type: package`)

## A. Sơ đồ trả lời câu hỏi gì
**Mã nguồn chia thành những gói nào và gói nào phụ thuộc gói nào** (để kiểm soát kiến trúc phân tầng và phát hiện phụ thuộc vòng). Nguồn khái niệm: `assets/uml/package-diagram/{spec,overview,package-import,element-import,package-merge}.md`.

### Ký hiệu và nghĩa
| Hình | Nghĩa | JSON |
|---|---|---|
| Hình thư mục có tên (kèm danh sách thành phần chứa) | Một gói (package) | `packages` (`contains`) |
| Mũi tên nét đứt đầu hở, không nhãn | Phụ thuộc "dùng" (use): gói nguồn dùng gói đích | `kind: use` |
| Mũi tên nét đứt «import» | Nhập CÔNG KHAI: các phần tử của gói đích thành phần tử của gói nguồn và hiện cho ai nhập gói nguồn | `kind: import` |
| Mũi tên nét đứt «access» | Nhập RIÊNG: dùng được phần tử gói đích nhưng không hiện ra ngoài | `kind: access` |
| Mũi tên nét đứt «merge» | Trộn: nội dung gói đích được trộn vào gói nguồn | `kind: merge` |

## B. Cách phân tích
1. **Gói là gói Java thật** (hoặc thư mục module) ở mức hợp lý (ví dụ `controller`, `service`, `repository`, `domain`), không phải từng lớp.
2. **Chứa gì:** ghi vài lớp tiêu biểu trong mỗi gói (tối đa khoảng 6), nói rõ nếu rút gọn.
3. **Phụ thuộc:** đọc các câu `import` giữa các gói (qua XERJ hoặc cấu trúc thư mục). Hướng mũi tên: từ gói đang `import` tới gói được `import`.
4. **Soát vòng:** hai gói phụ thuộc lẫn nhau là lỗi thiết kế; công cụ cảnh báo vòng.

## C. Phiếu phân tích cần điền
| Gói (tên đầy đủ) | Lớp tiêu biểu | Phụ thuộc vào gói nào | Loại (use, import, access, merge) | Nguồn (file:dòng của câu import) |
|---|---|---|---|---|

## D. Khung JSON
```json
{
  "type": "package",
  "title": "<UC-xx>: sơ đồ gói <phạm vi>",
  "note": "Mũi tên nét đứt: gói này phụ thuộc gói kia.",
  "out": "<UC-xx>-package.drawio",
  "png": "<UC-xx>-package.png",
  "packages": [
    {"id": "p1", "label": "<gói 1>", "col": 0, "row": 0, "contains": ["<Lớp1>", "<Lớp2>"]},
    {"id": "p2", "label": "<gói 2>", "col": 1, "row": 0, "contains": ["<Lớp3>"]}
  ],
  "dependencies": [{"from": "p1", "to": "p2", "kind": "use"}]
}
```
Trường: `col`, `row` (một cột khoảng 360 điểm, một hàng khoảng 190 điểm); `kind` mặc định `use`; `label` trên cạnh bỏ trống thì tự ghi «import», «access», «merge».

## E. Lỗi hay gặp
Vẽ từng lớp thay vì gói; bịa phụ thuộc không có trong câu import; đảo hướng mũi tên; bỏ sót phụ thuộc vòng; gói không có phụ thuộc nào.

## F. Công cụ chưa vẽ
Nhập từng phần tử (element import), gói lồng nhau, phụ thuộc có tên riêng. Ghi trong mô tả.

## G. Trước khi chạy
Mỗi mũi tên có câu `import` làm nguồn? Không có cảnh báo vòng chưa giải thích? `--check-only` đạt, đã xem ảnh.
