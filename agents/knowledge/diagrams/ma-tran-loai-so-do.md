# Ma trận các loại sơ đồ: câu hỏi, công cụ, JSON, mẫu, mức ưu tiên

> **Loại: tham khảo.** Phân tích toàn bộ loại sơ đồ có trong kho tri thức (10/11/2026). Khái niệm gốc: `agents/knowledge/srs/uml-diagrams-mastery.md`. Công cụ: `scripts/ve-so-do.py`. Mẫu phân tích và khung JSON: `agents/knowledge/diagrams/mau-phan-tich/`.

## 1. Loại ĐÃ có công cụ python và JSON (đủ chuẩn để agent làm theo)
| Sơ đồ | Câu hỏi nó trả lời | `type` | Mẫu phân tích | JSON mẫu | Ảnh mẫu |
|---|---|---|---|---|---|
| Use case | Ai (ngoài hệ thống) dùng hệ thống để đạt giá trị gì | `usecase` | `use-case.md` | `mau/usecase.json` | `assets/uml/use-case-diagram/template.png` |
| Activity | Việc diễn ra theo thứ tự nào, lớp nào làm, rẽ nhánh và lỗi ở đâu | `activity` | `activity.md` | `mau/activity.json` | `assets/uml/activity-diagram/template.png` |
| Sequence | Theo thời gian, ai gọi ai, thông điệp gì (một kịch bản) | `sequence` | `sequence.md` | `mau/sequence.json` | `assets/uml/sequence-diagram/template.png` |
| Class | Những kiểu nào tham gia và liên hệ cấu trúc ra sao | `class` | `class.md` | `mau/class.json` | `assets/uml/class-diagram/template.png` |
| ERD | Dữ liệu nằm ở bảng nào, nối bằng khóa nào | `erd` | `erd.md` | `mau/erd.json` | (mẫu `mau/erd.json`) |
| State machine | Đối tượng có trạng thái nào, sự kiện nào đổi trạng thái | `statemachine` | `state-machine.md` | `mau/statemachine.json` | `assets/uml/state-machine-diagram/template.png` |
| Component | Hệ thống chia thành thành phần nào, giao diện nào | `component` | `component.md` | `mau/component.json` | `assets/uml/component-diagram/template.png` |
| Deployment | Phần mềm chạy trên máy và môi trường nào | `deployment` | `deployment.md` | `mau/deployment.json` | `assets/uml/deployment-diagram/template.png` |
| Package | Mã chia thành gói nào, gói nào phụ thuộc gói nào | `package` | `package.md` | `mau/package.json` | `assets/uml/package-diagram/template.png` |
| Cả bộ một UC | (đóng gói) | `bundle` | `00-quy-trinh-mot-uc.md` | `mau/bundle.json` | |
| Lưu đồ một làn, activity theo vai (cũ) | Thuật toán một lớp; luồng nhiều vai | `flow`, `swimlane` | (cũ) | `mau/flow.json`, `mau/swimlane.json` | |

## 2. Loại CHƯA có công cụ (quyết định và lý do)
| Sơ đồ | Câu hỏi | Vì sao chưa làm công cụ | Khi nào nên làm |
|---|---|---|---|
| Communication | Đối tượng cộng tác thế nào, nhấn vào liên kết | Sequence đã trả lời cùng thông tin theo thời gian | Khi một UC cần nhấn vào cấu trúc liên kết chứ không phải thời gian |
| Object | Ảnh chụp các đối tượng cụ thể tại một lúc | Trang nguồn trong kho bị lỗi 404; ít dùng với dự án này | Khi cần minh họa dữ liệu mẫu, nên bổ sung trang nguồn trước |
| Composite structure | Cấu trúc bên trong của một lớp | Hiếm dùng; sơ đồ lớp và thành phần đủ | Khi cần mô tả cổng và phần bên trong |
| Timing | Trạng thái theo trục thời gian (thời gian thực) | Dự án không có ràng buộc thời gian thực | Khi có yêu cầu thời gian nghiêm ngặt |
| Interaction overview | Tổng quan luồng nối các tương tác | Activity theo làn lớp đã bao phủ | Khi có luồng nối nhiều sequence |
| Profile | Mở rộng UML bằng stereotype | Không cần cho tài liệu UC | Khi định nghĩa quy ước stereotype riêng |
| Information flow | Thông tin chảy giữa các thực thể | Ít dùng; activity có luồng thông điệp | Khi cần mô tả luồng thông tin nghiệp vụ trừu tượng |
| Manifestation | Artifact thể hiện thành phần nào | Một phần của deployment | Khi cần ánh xạ component tới artifact chi tiết |
| Model | Góc nhìn trừu tượng của hệ thống | Gần với package | Khi trình bày kiến trúc phân tầng ở mức mô hình |
| Network architecture | Mạng, thiết bị, kết nối | Một dạng deployment | Khi cần sơ đồ mạng chi tiết (vùng, tường lửa) |
| Protocol state machine | Giao thức sử dụng một thành phần | Một dạng state machine | Khi mô tả thứ tự gọi hợp lệ của một API |
| User story map | Backlog theo giá trị | Bảng đủ dùng | Khi lập kế hoạch release |
| Mockup giao diện | Màn hình | Có script riêng `ve_mockup_uc04.py` (UC-04) | Khi có UC mới cần mockup: đưa vào `ve-so-do.py` |
| Kiến trúc hệ thống, cache, thanh toán, Kafka | Kiến trúc tổng thể | Dùng archify hoặc component và deployment | |

Quy tắc: loại nào gặp LẦN THỨ HAI trong một UC thật thì thêm `type` vào `ve-so-do.py` (cùng mẫu phân tích, JSON mẫu, template, và chạy `kiem-bo-so-do.py`), không viết script riêng.

## 3. Khuôn của một loại mới (để người sau thêm cho đúng chuẩn)
1. Đọc khái niệm trong `assets/uml/<loại>/spec.md` (tải thêm trang thiếu từ uml-diagrams.org nếu cần) và bài "Constructing …" của SourceMaking.
2. Thiết kế JSON (id, nút, quan hệ, vị trí bằng `col`/`row`), mọi trường đều có mặc định hợp lý.
3. Viết `run_<loại>` trong `ve-so-do.py`: kiểm hình thức (id trùng, trỏ không có, thiếu nhãn, mồ côi, vòng), bố trí, kiểm đè hộp và chồng nhãn (`check_boxes`, `check_labels`), vẽ đen trắng.
4. Thêm mẫu vào `MAU`, in ra `agents/knowledge/diagrams/mau/<loại>.json`; sinh `template.*` trong `assets/uml/<loại>/`.
5. Viết `mau-phan-tich/<loại>.md` (ký hiệu, cách phân tích, phiếu, khung JSON đã chạy `--check-only` đạt, lỗi hay gặp).
6. Cập nhật bảng ở `quy-trinh-ve-so-do-bang-json.md` mục 0, mục tra cứu `uml-diagrams-mastery.md`, `00-quy-trinh-mot-uc.md` mục 6; dựng lại catalog.
