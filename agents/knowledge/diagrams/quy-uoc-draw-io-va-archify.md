# Quy ước vẽ và sửa sơ đồ bằng draw.io và archify

> **Loại: tham khảo.** Tổng hợp từ cách làm đã dùng trong dự án thực tế (tool-agnostic), không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Nói **dùng công cụ nào, file nguồn ở đâu**; loại sơ đồ nào và quy tắc nội dung nằm ở `srs/chuan-ve-so-do.md`. Các script `ve_lai.py`, `json_to_drawio.py`, `theo_doi_drawio.py` là của dự án gdt, **không nằm trong khung**.

## 1. Nguyên tắc: mỗi sơ đồ một nguồn

Một sơ đồ chỉ có **một** file nguồn là sự thật. Ảnh `.png`, `.svg` luôn là bản xuất, không sửa tay.

| Loại | Công cụ nguồn | File nguồn | Người sửa bằng tay |
|---|---|---|---|
| Hoạt động (bơi làn), use case, luồng màn hình, thành phần và triển khai muốn tự chỉnh | draw.io | `<tên>.drawio` | Có (draw.io Desktop) |
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
1. **Sơ đồ hoạt động chỉ có MỘT chấm kết thúc**; mọi nhánh dồn về đó.
2. `id` duy nhất; ô tiền tố `n_`, mũi tên `e`. Mũi tên **luôn có `source` và `target`** để kéo ô thì đường đi theo.
3. Nhãn có `& < > "` phải escape. Xuống dòng trong nhãn: `&#xa;` và `html=0`.
4. Mỗi làn một màu; quyết định cam (`#fff7ed`, viền `#ea580c`); bắt đầu và kết thúc đen. Không dùng màu làm nghĩa duy nhất, nhánh lỗi phải có nhãn chữ.
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

- Sơ đồ hoạt động bơi làn: đường nối dùng `orthogonalEdgeStyle` tự định tuyến; muốn đường gọn thì xếp ô vào **làn và hàng liền kề**. Mỗi sơ đồ 3 đến 5 làn, làn không có ô thì bỏ. Nhánh quyết định dài (nhiều ô rẽ liên tiếp) nên tách thành sơ đồ khác.
- archify sequence: nhãn participant ngắn (dưới khoảng 13 đơn vị), tối đa 7 đến 9 participant, **không có self-message**, nhãn mũi tên vừa khung. archify architecture: `boundary` không chứa ô không thuộc nó. archify lifecycle: khai `mainPath`, mỗi trạng thái một `type`.
- Sơ đồ phải khớp quá trình **đang chốt**. Khi quyết định đổi, vẽ lại sơ đồ trước khi sửa tài liệu, rồi xuất ảnh và nhìn từng ảnh.
- Khi tạo sơ đồ mới: chọn loại theo `chuan-ve-so-do.md`, chọn công cụ theo mục 1, ghi vào chỉ mục sơ đồ của dự án (tên, loại, nguồn, dùng ở đâu), dẫn ảnh vào md kèm mô tả hoạt động, xuất ảnh và đối chiếu checklist.
- Đường cắt nhau nổi vòng (line jumps): thêm `jumpStyle=arc;jumpSize=10;` vào `style` mũi tên. **Chưa kiểm chứng** ảnh xuất có hiện đúng không.
