# Quy ước vẽ và sửa sơ đồ bằng draw.io và archify

> **Loại: tham khảo.** Tổng hợp từ cách làm đã dùng trong dự án thực tế (tool-agnostic), không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Nói **dùng công cụ nào, file nguồn ở đâu**; loại sơ đồ nào và quy tắc nội dung nằm ở `srs/chuan-ve-so-do.md`. Các script `ve_lai.py`, `json_to_drawio.py`, `theo_doi_drawio.py` là của dự án gdt, **không nằm trong khung**.

## 1. Nguyên tắc: mỗi sơ đồ một nguồn

Một sơ đồ chỉ có **một** file nguồn là sự thật. Ảnh `.png`, `.svg` luôn là bản xuất, không sửa tay.

| Loại | Công cụ nguồn | File nguồn | Người sửa bằng tay |
|---|---|---|---|
| Activity, class, sequence, ERD, use case | `ve-so-do.py` (JSON trước, rồi ra `.drawio`) | `<tên>.spec.json` | Có: sửa JSON; hoặc sửa `.drawio` rồi `--lay-tu-drawio` |
| Luồng màn hình, thành phần và triển khai muốn tự chỉnh | draw.io | `<tên>.drawio` | Có (draw.io Desktop) |
| ERD, sequence, vòng đời (trạng thái), kiến trúc sinh từ dữ liệu | archify | `<tên>.json` | Không: sửa JSON rồi vẽ lại |
| Sơ đồ nhỏ trong tài liệu | Mermaid | khối mã trong md | Có (sửa chữ) |

- Cùng một tên có nhiều file: **`.drawio` thắng** (chỉ có khi ai đó đã chỉnh tay).
- **Không bao giờ sinh lại `.drawio` từ JSON rồi ghi đè** file người đã sửa tay. Bộ chuyển phải từ chối nếu file đã có, trừ khi người dùng bảo ghi đè.
- Khung xem md thường không vẽ Mermaid, nên luôn kèm ảnh hoặc mô tả chữ (`mo-ta-hoat-dong-so-do.md`).

## 2. File nhiều trang

- Một chức năng một file `.drawio` nhiều trang (mỗi sơ đồ một tab), tên trang = tên ảnh.
- Gộp file lẻ thành nhiều trang: **mỗi `<diagram>` phải có `id` riêng** (`p1`, `p2`...). Trùng id sẽ báo "Duplicate page ID" và không mở được. `diagram-describe.py --check` bắt lỗi này.

## 3. Viết file `.drawio` bằng tay (AI tự tạo)

**Ưu tiên:** khai báo cấu trúc (làn, hàng, nút, cạnh có nhãn) và để script hoặc bộ dàn trang tính tọa độ, vì mô hình ngôn ngữ tính tọa độ 2D kém (`diagrams-cheatsheet-and-decision-matrix.md` mục 1). Viết XML tay chỉ cho sơ đồ nhỏ hoặc khi sửa file đã có.

File là XML **không nén**:

```xml
<mxfile host="app.diagrams.net"><diagram name="Tên" id="p1">
  <mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" page="0" pageWidth="1000" pageHeight="800">
    <root>
      <mxCell id="0"/><mxCell id="1" parent="0"/>
      <mxCell id="n_a" value="Nhãn" style="rounded=1;whiteSpace=wrap;fillColor=#dcfce7;strokeColor=#16a34a;" vertex="1" parent="1">
        <mxGeometry x="100" y="100" width="200" height="50" as="geometry"/>
      </mxCell>
      <mxCell id="e1" value="có" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;" edge="1" parent="1" source="n_a" target="n_b">
        <mxGeometry relative="1" as="geometry"/>
      </mxCell>
    </root>
  </mxGraphModel>
</diagram></mxfile>
```

Quy tắc:
1. **Sơ đồ hoạt động theo làn lớp (`type: activity` của `ve-so-do.py`) được nhiều chấm bắt đầu và kết thúc**; `flow` và `swimlane` cũ vẫn một chấm kết thúc. Chuẩn: `quy-trinh-ve-so-do-bang-json.md` mục 4.6. Ưu tiên sinh bằng `ve-so-do.py`, chỉ viết XML tay khi chưa có công cụ.
2. `id` duy nhất; ô tiền tố `n_`, mũi tên `e`. Mũi tên **luôn có `source` và `target`** để kéo ô thì đường đi theo.
3. Nhãn có `& < > "` phải escape. Xuống dòng trong nhãn: `&#xa;` và `html=0`.
4. Mặc định ĐEN TRẮNG (người dùng chốt 09/11/2026): hộp nền trắng viền đen, đầu và cuối chấm đen. Không dùng màu làm nghĩa duy nhất; nhánh lỗi viền đậm kèm nhãn chữ.
5. Tọa độ bội 10; ô cách nhau tối thiểu 30px; đường nối không đi xuyên ô khác.
6. Một trang một sơ đồ; tiêu đề là ô `text` ở góc trên trái.
7. Làn có thể vẽ bằng hai hình chữ nhật (khung nền `fillColor=none` và ô tiêu đề tô màu sát cạnh khung) hoặc bằng `swimlane`; `diagram-describe.py` nhận cả hai.

| Phần tử | `style` | Ghi chú |
|---|---|---|
| Hoạt động: việc | `rounded=1;arcSize=20;whiteSpace=wrap;fillColor=…;strokeColor=…` | đã dùng thực tế |
| Hoạt động: quyết định | `rhombus;whiteSpace=wrap;fillColor=#fff7ed;strokeColor=#ea580c` | đã dùng thực tế |
| Bắt đầu, kết thúc | `ellipse;fillColor=#0f172a` ; `ellipse;shape=endState;fillColor=#0f172a` | đã dùng thực tế |
| Use case: tác nhân | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1` | đã dùng thực tế |
| Use case: include, extend | mũi tên `dashed=1;endArrow=open`, nhãn `«include»`, `«extend»` | đã dùng thực tế |
| Thành phần, triển khai | hình chữ nhật bo góc, `swimlane` làm ranh giới | theo mxGraph, kiểm lại bằng cách xuất ảnh |

## 4. Đọc và sửa `.drawio` đã có

- Kiểm tra không nén: `head -c 200 file.drawio` thấy `<mxGraphModel`. Thấy chuỗi dài lạ trong `<diagram>` là file nén: nhờ người bỏ tích `File > Properties > Compressed` rồi lưu lại.
- Hiểu luồng: `python scripts/diagram-describe.py <file.drawio>` (xem `mo-ta-hoat-dong-so-do.md`). Tự đọc XML thì dùng `xml.etree.ElementTree`, không dùng sed.
- Sửa nhãn, thêm ô, thêm mũi tên: giữ `id` cũ; **không đổi tọa độ ô người đã kéo tay** trừ khi được yêu cầu.
- Sau khi sửa: xuất lại ảnh và **nhìn ảnh**.
- Chữ "Electron" trong `host=` không phải dấu hiệu lỗi: đó là bản draw.io Desktop ghi khi lưu.

## 5. Xuất ảnh và bài học với draw.io Desktop

- Xuất: `draw.io -x -f png -s 2 -b 10 -o ra.png vao.drawio` (macOS: `/Applications/draw.io.app/Contents/MacOS/draw.io`). Cài: `brew install --cask drawio`. Lệnh xuất chọn trang theo số thứ tự.
- Lệnh xuất treo khi còn tiến trình draw.io mắc kẹt: `pkill -f draw.io` rồi chạy lại. Luôn chạy có `timeout`.
- Hộp thoại `process.cwd failed ... operation not permitted` trên macOS: cấp quyền Files and Folders cho draw.io trong thư mục Documents.
- Muốn người dùng xem: `pkill -f draw.io; sleep 3; open -a draw.io <file>`; lần mở đầu có thể không hiện file, mở lại lần hai.
- Chưa thử mở `.drawio` trên máy không có draw.io Desktop (lệnh xuất sẽ báo thiếu).

## 6. Bài học khi vẽ bộ sơ đồ

- Sơ đồ Activity (Swimlane): đường nối dùng `orthogonalEdgeStyle` tự định tuyến; muốn đường gọn thì xếp ô vào **làn (lane) và hàng liền kề**. Mỗi sơ đồ 3 đến 5 làn, làn không có ô thì bỏ. Nhánh quyết định dài (nhiều ô rẽ liên tiếp) nên tách thành sơ đồ khác.
- archify sequence: nhãn participant ngắn (dưới khoảng 13 đơn vị), tối đa 7 đến 9 participant, **không có self-message**, nhãn mũi tên vừa khung. archify architecture: `boundary` không chứa ô không thuộc nó. archify lifecycle: khai `mainPath`, mỗi trạng thái một `type`.
- Sơ đồ phải khớp quá trình **đang chốt**. Khi quyết định đổi, vẽ lại sơ đồ trước khi sửa tài liệu, rồi xuất ảnh và nhìn từng ảnh.
- Khi tạo sơ đồ mới: chọn loại theo `chuan-ve-so-do.md`, chọn công cụ theo mục 1, ghi vào chỉ mục sơ đồ của dự án (tên, loại, nguồn, dùng ở đâu), dẫn ảnh vào md kèm mô tả hoạt động, xuất ảnh và đối chiếu checklist.
- Đường cắt nhau nổi vòng (line jumps): thêm `jumpStyle=arc;jumpSize=10;` vào `style` mũi tên. **Chưa kiểm chứng** ảnh xuất có hiện đúng không.

## 7. Vòng vẽ, xem, sửa và lỗi bố cục thường gặp (bổ sung 02/11/2026)

Rút ra khi vẽ 3 sơ đồ (Activity Swimlane, sequence, use case) của chức năng "ghi nhận kế toán khi Check trùng" trong dự án gdt. **Lần vẽ đầu hầu như luôn có lỗi bố cục; sơ đồ đẹp là kết quả của vòng lặp, không phải của lần vẽ đầu** (sơ đồ hoạt động phải vẽ lại 3 lần mới sạch).

### 7.1 Vòng lặp bắt buộc
1. Viết hoặc sửa **file nguồn** (JSON hoặc `.drawio`). Không sửa ảnh.
2. Sinh `.drawio` hoặc PNG.
3. **Mở ảnh PNG ra xem** và liệt kê lỗi: đường cắt ngang ô, nhãn bị đè, ô chồng nhau, chữ tràn ô, hai đường nhập thành một đoạn khó phân biệt.
4. Sửa nguồn, sinh lại. Lặp đến khi hết lỗi (thường 2 đến 3 vòng).
5. Kiểm cấu trúc: `python scripts/diagram-describe.py <file.drawio> --page "<tên trang>" --check`.

Agent **không xem được ảnh**: bỏ bước 3, dựa vào bước 5 và bảng lỗi dưới đây, và nói rõ với người dùng là chưa kiểm tra bằng mắt. Đừng báo "sơ đồ đẹp" khi chưa nhìn.

### 7.2 Lỗi nhìn thấy, nguyên nhân, cách sửa (đã gặp thật)
| Lỗi nhìn thấy | Nguyên nhân | Cách sửa |
|---|---|---|
| Đường từ nút ở làn này sang nút ở làn kế bên đi ngang **xuyên qua** một nút khác cùng hàng | Hai nhánh dồn về một nút, một nhánh phải đi qua làn của nhánh kia; bộ định tuyến tự động đi theo hàng | Hạ nút của nhánh thứ hai xuống **một hàng** để đường đi qua hàng trống. Hoặc đặt nút quyết định kế tiếp cùng làn với nhánh dài hơn (ví dụ "Ghi DB thành công?" đặt ở làn service thay vì làn DB) |
| Đường về nút kết thúc cắt ngang các nút cuối (nút hiển thị kết quả, nút lỗi) | Nút kết thúc nằm ở làn ngoài cùng, đường đi ngang đúng hàng của các nút cuối | Đặt các nút đi về kết thúc ở **các hàng khác nhau**, giữ làn ngoài cùng trống, để đường đi theo lề |
| Nhãn "có", "không" nằm đè lên ô hoặc lên đường khác | Hai nhánh dùng chung một đoạn nằm ngang | Chấp nhận khi vẫn đọc được; nếu không thì tách hai nút nhánh ra hai hàng |
| Use case: hai tác nhân chồng lên nhau, nhãn bị che | Hai tác nhân cùng bên và gần nhau | Đổi một tác nhân sang bên kia (`"side": "right"`) |
| Use case: nhãn dài xuống 3 dòng trong hình elip | Nhãn quá dài | Còn đọc được thì giữ; nếu chật thì rút ngắn nhãn (dưới khoảng 30 ký tự) |
| Sequence: nhãn thông điệp bị đường lifeline của participant ở giữa cắt qua | Thông điệp dài đi ngang một participant không liên quan | Bỏ participant không cần (gộp tên vào nhãn thông điệp), xếp các participant hay nói chuyện với nhau cạnh nhau |
| Nút lỗi không có màu đỏ | Bộ chuyển JSON sang drawio chỉ tô màu theo làn, không có loại nút lỗi | Hậu xử lý XML: đổi `fillColor` và `strokeColor` của nút lỗi và của các cạnh vào ra nó. Luôn kèm chữ "LỖI" trong nhãn (màu không là nghĩa duy nhất) |

### 7.3 Mở được bằng draw.io
- **Đã kiểm chứng:** file `.drawio` nhiều trang, mỗi `<diagram>` có `id` và `name` bằng tên sơ đồ, XML không nén; xuất PNG bằng CLI `draw.io -x -f png -p <số trang tính từ 1> -s 2 -b 10 -o ra.png vao.drawio` chạy đúng; `diagram-describe.py --check` báo "Đạt".
- **Chưa kiểm chứng:** mở cửa sổ draw.io Desktop (giao diện) với các trang mới. Xuất PNG bằng dòng lệnh thành công **không chứng minh** mở bằng giao diện được; nhờ người dùng mở một lần và báo lại.
- Thêm trang vào file nhiều trang: xóa trang cùng tên trước khi thêm (tránh trùng tên và id), rồi đọc lại danh sách trang để biết số thứ tự xuất ảnh.

### 7.4 Script của dự án gdt còn trỏ đường dẫn cũ
- `json_to_drawio.py`, `ve_lai.py`, `drawio_nhom.py` còn trỏ `doc/srs/hinh` (cấu trúc cũ); dự án đã chuyển sang `doc/features/<UC>/hinh/`. Cách vòng qua: viết script phụ `import json_to_drawio as J`, gọi `J.activity(spec)` hoặc `J.sequence(spec)` để lấy trang XML, tự ghép vào file nhóm rồi xuất ảnh bằng CLI draw.io. Hoặc sửa hằng `HINH` trong các script.
- Use case: `python3 scripts/usecase_png.py <đường dẫn đầy đủ tới .usecase.json>` ghi `.svg` và `.png` cạnh file nguồn (cần Chrome và Pillow).
- Mẫu nguồn đã chạy được (xem làm khuôn, đổi sang dữ liệu của chức năng mình):
  - Hoạt động: `doc/features/TMP-dong-bo-user/hinh/TMP-dong-bo-user-hoat-dong-ghi-nhan-ke-toan.activity.json` (làn, nút `start`/`action`/`decision`/`end` gán `lane` và `row`, cạnh có nhãn).
  - Sequence: `.../TMP-dong-bo-user-sequence-ghi-nhan-ke-toan.json` (`participants`, `messages` có `y` cách nhau 44).
  - Use case: `.../TMP-dong-bo-user-use-case.usecase.json` (`usecases`, `actors` có `side` và `near`, `links`, `relations`).
