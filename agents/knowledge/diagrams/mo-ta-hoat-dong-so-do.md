# Mô tả hoạt động đi kèm sơ đồ (để agent hiểu hết sơ đồ)

> **Loại: tham khảo.** Cách làm đã dùng trong dự án thực tế, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Bổ sung cho `srs/chuan-ve-so-do.md` mục 2 (quy tắc 2: số bước trong sơ đồ bằng số bước trong văn bản). File này nói **viết phần chữ đó thế nào** cho từng loại sơ đồ.

## 1. Vì sao phải có phần chữ

Agent đọc được chữ, không "nhìn" được ảnh `.png` hay `.svg`. Một sơ đồ chỉ có nghĩa với agent khi có **mô tả hoạt động bằng chữ**: ai làm gì, theo thứ tự nào, rẽ nhánh khi nào, đọc và ghi dữ liệu gì, kết thúc ra sao. Người đọc cũng cần phần này để đối chiếu code với sơ đồ. Nguồn thật của sơ đồ (`.drawio`, JSON, Mermaid) cho biết hình, còn phần mô tả cho biết **nghĩa nghiệp vụ**.

## 2. Quy tắc chung (mọi loại sơ đồ)

1. Mỗi sơ đồ có một phần mô tả chữ ngay dưới ảnh trong tài liệu, kèm đường dẫn tới file nguồn.
2. **Đánh số bước giống hệt sơ đồ** (`1.1`, `1.2`, ...). Đổi số trong sơ đồ thì đổi số trong mô tả.
3. Mỗi bước một hành động: **ai** (làn hoặc tác nhân), **làm gì**, **với dữ liệu nào**, **dẫn tới bước nào**.
4. Quyết định phải nêu **đủ mọi nhánh** kèm điều kiện ("có", "không", "timeout"...). Không để nhánh nào không có đích.
5. Ghi **trạng thái trước và sau** khi một bước đổi dữ liệu (mã trạng thái, cột, bảng), dùng đúng tên trong code và tài liệu.
6. Luôn có **đường lỗi** và nêu xử lý: từ chối, hết hạn, không có phản hồi.
7. Sơ đồ hoạt động có **một điểm kết thúc**. Ghi kết quả cuối của từng nhánh dồn về điểm đó.
8. Dùng số liệu và tên thật (giới hạn, ngưỡng, endpoint, bảng). Không dùng ví dụ của dự án khác.
9. Chưa chắc điều gì thì ghi "chưa xác minh" ở đúng bước đó, không đoán.

## 3. Khuôn theo loại sơ đồ

| Loại | Phần chữ cần có | Cột hoặc mục tối thiểu |
|---|---|---|
| Activity (Swimlane) | Bảng bước + mô tả rẽ nhánh | Bước, Lane/Actor, Hành động, Điều kiện rẽ, Dữ liệu đọc/ghi, Đi tới |
| Sequence | Bảng thông điệp | Số, từ, đến, nội dung, đồng bộ hay bất đồng bộ, phản hồi, lỗi |
| Trạng thái (vòng đời) | Bảng chuyển trạng thái | Từ, sự kiện hoặc điều kiện, tác nhân, sang, việc đi kèm |
| ERD | Bảng thực thể | Bảng, cột chính, khóa, quan hệ và bội số, ai ghi, ai đọc |
| Use case | Bảng tác nhân và use case | Tác nhân, use case, quan hệ include hoặc extend, điều kiện |
| Luồng màn hình | Bảng màn hình | Mã màn, hành động của người dùng, điều kiện, màn kế tiếp |
| Thành phần, triển khai | Bảng thành phần | Thành phần, trách nhiệm, gọi ai, giao thức, ranh giới |

## 4. Mẫu: sơ đồ hoạt động

Ví dụ trung lập, thay bằng dữ liệu thật của chức năng:

```markdown
![Hoạt động: đặt hàng](hinh/UC-01-hoat-dong-dat-hang.png)

Nguồn (sửa bằng draw.io): [`hinh/UC-01.drawio`](hinh/UC-01.drawio), trang `UC-01-hoat-dong-dat-hang`.

| Bước | Làn | Hành động | Dữ liệu | Đi tới |
|---|---|---|---|---|
| 1.1 | Người dùng | Chọn sản phẩm, bấm "Đặt hàng" | giỏ hàng | 1.2 |
| 1.2 | Hệ thống | Kiểm tra tồn kho và địa chỉ | `product.stock`, `address` | có: 1.3; không: 1.5 |
| 1.3 | Hệ thống | Tạo đơn, trạng thái `NEW`, trừ kho | `orders` (ghi), `product.stock` (ghi) | 1.4 |
| 1.4 | Hệ thống | Trả mã đơn cho người dùng | - | Kết thúc |
| 1.5 | Hệ thống | Hết hàng hoặc thiếu địa chỉ: trả lỗi 400, không ghi gì | - | Kết thúc |

**Rẽ nhánh 1.2:** "có" khi `stock >= số lượng` và địa chỉ đủ; "không" trong mọi trường hợp còn lại.
**Kết quả:** đơn `NEW` (nhánh 1.3 và 1.4) hoặc không có thay đổi (nhánh 1.5).
```

## 5. Cách agent đọc một sơ đồ rồi viết mô tả

1. **`.drawio`**: chạy `python scripts/diagram-describe.py <file.drawio> [--page "<tên trang>"]` để lấy bảng bước, làn, nhánh có nhãn. Thêm `--json` nếu muốn xử lý tiếp, `--check` để kiểm quy tắc (id trang không trùng, một nút kết thúc, quyết định đủ nhánh có nhãn, không nút mồ côi). File phải không nén (xem `quy-uoc-draw-io-va-archify.md`).
2. **JSON của archify**: đọc trực tiếp các khóa nút và cạnh theo `diagram_type`.
3. **Mermaid**: đọc thẳng khối mã trong tài liệu.
4. **Ảnh `.png`, `.svg`**: không dùng làm nguồn mô tả, vì chỉ là bản xuất.
5. Bảng từ script chỉ có **hình**. Bổ sung phần nghĩa: điều kiện cụ thể, dữ liệu, mã trạng thái, bước lỗi, lấy từ code và đặc tả. Rồi ghi vào tài liệu theo mục 3.
6. Khi người dùng đổi nghiệp vụ: vẽ lại sơ đồ trước, rồi sửa mô tả, rồi chạy lại `--check`.

## 6. Checklist

- [ ] Mỗi nút trong sơ đồ có đúng một bước trong mô tả, số bước khớp.
- [ ] Mỗi nhãn mũi tên xuất hiện trong cột điều kiện.
- [ ] Mọi quyết định có đủ nhánh và nhánh nào cũng có đích.
- [ ] Có đường lỗi và xử lý của nó.
- [ ] Có đúng một điểm kết thúc (sơ đồ hoạt động).
- [ ] Trạng thái, bảng, endpoint là tên thật.
- [ ] Có đường dẫn file nguồn và tên trang.
- [ ] `diagram-describe.py --check` báo đạt (với `.drawio`).
