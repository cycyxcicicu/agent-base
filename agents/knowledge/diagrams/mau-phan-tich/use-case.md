# Mẫu phân tích: sơ đồ use case (`type: usecase`)

## A. Sơ đồ trả lời câu hỏi gì
**Ai (bên NGOÀI hệ thống) dùng hệ thống để đạt giá trị gì?** Nó cho biết phạm vi chức năng, không cho biết chạy thế nào (đó là việc của activity và sequence). Nguồn khái niệm: `assets/uml/use-case-diagram/{how-to,subject,actor,use-case,actor-association,include,extend}.md`; cách xây dựng: SourceMaking "Constructing Use Case Diagrams" (`assets/sourcemaking-uml/pages/modeling-business-systems/constructing-use-case-diagrams/README.md`).

### Ký hiệu và nghĩa
| Hình hoặc đường | Nghĩa | JSON |
|---|---|---|
| Hình chữ nhật lớn có tên | Hệ thống (subject), ranh giới: trong khung là của hệ thống, ngoài khung là bên ngoài | `system` |
| Người que | Tác nhân: vai của một thực thể BÊN NGOÀI hệ thống (người hoặc hệ thống khác) | `actors` |
| Hình elip | Use case: một đơn vị chức năng hoàn chỉnh, hữu ích, do tác nhân khởi động; tên "động từ + danh từ" | `usecases` |
| Đường liền không mũi tên | Tác nhân tham gia use case (association) | `links` |
| Nét đứt đầu hở, nhãn «include», từ use case GỐC tới use case được gọi | Gốc luôn cần phần được gọi, bắt buộc, không điều kiện | `relations` `type: include` |
| Nét đứt đầu hở, nhãn «extend», từ use case MỞ RỘNG tới use case GỐC | Phần mở rộng tùy chọn, có điều kiện và điểm mở rộng | `relations` `type: extend` |
| Nét liền, tam giác rỗng (tác nhân con tới tác nhân cha) | Tác nhân con kế thừa tác nhân cha | `generalizations` |

## B. Cách phân tích (4 bước của `how-to.md`, bổ sung bằng checklist SourceMaking)
1. **Hệ thống và ranh giới.** Hệ thống nào đang mô tả? Thành phần nào nằm TRONG (ví dụ giao diện, backend, dịch vụ nội bộ) thì KHÔNG phải tác nhân; hệ thống bên ngoài gọi vào hoặc được gọi ra (J&T, Pancake...) mới là tác nhân.
2. **Tác nhân = vai thật.** Lấy từ tài liệu yêu cầu và bảng vai trò của IAM (ví dụ Kế toán, CSKH, Telesale, Nhân viên kho, Quản trị viên), không đặt "User". Hai vai khác nhau thì hai tác nhân; hai vai có phần chung thì dùng tác nhân cha ("Người dùng hệ thống") và kế thừa.
3. **Use case = mục tiêu hoàn chỉnh của tác nhân.** Hỏi "tác nhân muốn đạt được gì khi dùng hệ thống?", không hỏi "bấm nút nào". Mỗi use case phải có tác nhân khởi động hoặc là phần được `include` hoặc `extend` từ use case khác.
4. **Quan hệ.** Hai use case trở lên lặp một đoạn thì tách thành use case được `include`. Có nhánh tùy chọn có điều kiện thì `extend`. Không dùng `include` cho nhánh tùy chọn.

## C. Phiếu phân tích cần điền
| Vai (tên thật) | Nguồn của vai | Use case của vai đó (động từ + danh từ) | Nguồn (tài liệu mục) | `include` nào | `extend` nào, điều kiện |
|---|---|---|---|---|---|

## D. Khung JSON (copy rồi điền; xóa dòng thừa)
```json
{
  "type": "usecase",
  "title": "<UC-xx>: sơ đồ use case <tên chức năng>",
  "system": "<tên hệ thống đang mô tả>",
  "note": "<một câu: ranh giới hệ thống, vai nào là tác nhân>",
  "out": "<UC-xx>-use-case.drawio",
  "png": "<UC-xx>-use-case.png",
  "usecases": [
    {"id": "u1", "label": "<UC-xx.01 động từ + danh từ>"},
    {"id": "u2", "label": "<UC-xx.02 ...>"}
  ],
  "actors": [
    {"id": "a1", "label": "<Vai thật 1>", "side": "left"},
    {"id": "a2", "label": "<Vai thật 2>"}
  ],
  "generalizations": [],
  "links": [["a1", "u1"], ["a2", "u2"]],
  "relations": []
}
```
Trường: `side` = `left` hoặc bỏ trống (bên phải); `near` = id use case để đặt tác nhân gần đó; `generalizations` = `[["con","cha"], ...]` (tác nhân con xếp cột trái, cha ở giữa, cha phải `side: left`); `relations` = `{"from","to","type"}`: `include` thì `from` là use case gốc, `extend` thì `from` là use case mở rộng.

## E. Bố trí
Use case xếp dọc theo thứ tự trong `usecases` (đặt use case gốc cạnh use case được `include`). Mỗi quan hệ một đường dọc riêng bên phải khung. Tác nhân tự đặt theo use case đã nối.

## F. Công cụ chưa vẽ (ghi trong mô tả tài liệu)
Điều kiện và điểm mở rộng của `extend`; use case trừu tượng; quan hệ kế thừa giữa use case; stereotype của use case.

## G. Lỗi hay gặp
- Coi giao diện hoặc backend là tác nhân (nằm trong hệ thống). Ghi tên một thành phần vừa nằm trong khung hệ thống vừa là tác nhân (lỗi đã gặp ở UC-06: `iam-service`).
- Gộp hai vai vào một tác nhân ("CSKH hoặc kho"): tách thành hai tác nhân.
- Use case là một thao tác nhỏ (bấm nút, mở hộp thoại) hoặc là chức năng kỹ thuật bên trong (kiểm tra hợp lệ, phân trang) mà không phải mục tiêu của tác nhân: chỉ giữ nếu là phần `include`.
- Dùng `include` cho nhánh tùy chọn, hoặc đảo chiều mũi tên.
- Tên tác nhân chung chung "User".

## H. Trước khi chạy
- Mọi tác nhân nằm ngoài hệ thống? Mọi use case có tác nhân hoặc quan hệ?
- Tên vai khớp bảng vai trò thật? Hướng `include` và `extend` đúng?
- `ve-so-do.py <spec> --check-only` đạt, đã xem ảnh.
