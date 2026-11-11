# Mẫu phân tích: sơ đồ triển khai (`type: deployment`)

## A. Sơ đồ trả lời câu hỏi gì
**Phần mềm (artifact) chạy trên những máy hoặc môi trường nào, các máy nối nhau bằng gì.** Nguồn khái niệm: `assets/uml/deployment-diagram/{spec,overview,node,artifact}.md`. Lưu ý của nguồn: trong UML 2 artifact được triển khai lên nút; component chỉ được triển khai gián tiếp qua artifact.

### Ký hiệu và nghĩa
| Hình | Nghĩa | JSON |
|---|---|---|
| Hình hộp 3D «device» | Thiết bị vật lý (máy chủ, máy người dùng) | `stereo: device` |
| Hình hộp 3D «execution environment» | Môi trường chạy phần mềm (JVM, Docker, Kubernetes, trình duyệt) | `stereo: executionEnvironment` |
| Hộp 3D không từ khóa | Nút chung | `stereo: node` |
| Hộp «artifact» nằm trong nút | Tệp được triển khai (jar, war, ảnh Docker, tệp cấu hình, bảng) | `artifacts` |
| Nút nằm trong nút | Lồng nhau (môi trường chạy trên máy) | `children` |
| Đường liền giữa hai nút, nhãn giao thức | Đường truyền (communication path) | `paths` |

## B. Cách phân tích
1. **Liệt kê máy và môi trường thật** từ docker-compose, manifest K8s, tài liệu hạ tầng (không đoán). Máy vật lý hoặc máy ảo là `device`; JVM, container, trình duyệt là `executionEnvironment` lồng trong máy.
2. **Artifact nào chạy ở đâu:** mỗi dịch vụ hoặc cơ sở dữ liệu thành một artifact trong nút của nó (tên tệp hoặc ảnh thật).
3. **Đường truyền:** nút nào nói chuyện với nút nào qua giao thức gì (HTTPS, JDBC, AMQP) và cổng nếu quan trọng.

## C. Phiếu phân tích cần điền
| Nút | Loại | Nằm trong nút nào | Artifact chạy trên đó | Nối tới nút nào, giao thức | Nguồn (compose, manifest, tài liệu) |
|---|---|---|---|---|---|

## D. Khung JSON
```json
{
  "type": "deployment",
  "title": "<UC-xx>: sơ đồ triển khai <môi trường>",
  "note": "Nút hình hộp 3D. Artifact nằm trong nút được triển khai. Đường liền ghi giao thức.",
  "out": "<UC-xx>-deployment.drawio",
  "png": "<UC-xx>-deployment.png",
  "nodes": [
    {"id": "n1", "label": "<Máy 1>", "stereo": "device", "col": 0, "row": 0, "artifacts": [{"id": "a1", "label": "<tệp>"}]},
    {"id": "n2", "label": "<Máy 2>", "stereo": "device", "col": 1, "row": 0, "children": ["env"]},
    {"id": "env", "label": "<Môi trường chạy>", "stereo": "executionEnvironment", "artifacts": [{"id": "a2", "label": "<tệp>"}]}
  ],
  "paths": [{"from": "n1", "to": "n2", "label": "<giao thức>"}]
}
```
Trường: nút cấp trên có `col`, `row`; nút con (id trong `children` của nút khác) KHÔNG có `col`, `row`; `artifact.id` duy nhất toàn sơ đồ.

## E. Lỗi hay gặp
Vẽ thành phần trực tiếp lên nút (nên là artifact); bịa tên máy hoặc phiên bản; nút không có đường nối; thiếu giao thức trên đường; một nút nằm trong hai nút cha.

## F. Công cụ chưa vẽ
Quan hệ manifestation (artifact thể hiện component), triển khai bằng mũi tên «deploy», thể hiện (instance) gạch chân tên, nhiều thể hiện của một nút. Ghi trong mô tả.

## G. Trước khi chạy
Mỗi nút và artifact có nguồn trong hạ tầng thật? Mỗi đường có giao thức? `--check-only` đạt, đã xem ảnh.
