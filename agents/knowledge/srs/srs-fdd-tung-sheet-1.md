> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục B

# Chuẩn viết từng sheet SRS_FDD — Phần 1: Nhật ký, Định nghĩa & Thiết kế tổng thể

Nguồn quy tắc: mẫu v3.0 + file đã điền thật `doc/governance/templates/04-srs-fdd-copilot-da-dien/goc/_SRS_FDD_AI-Agent-Copilot.xlsx`. Mục đánh dấu **[ĐỀ XUẤT]** là suy ra từ file Copilot, chưa được team GDT chốt — hỏi người dùng nếu ảnh hưởng kết quả.

### `NhatKyThayDoi`
- Một dòng mỗi lần làm. `updated info` = **làm gì + ở đâu + kết quả** (vd "Thêm Use-case UC-05, 3 service, 8 test case; chờ duyệt").
- `updated part`: `Create new` | `Update`. `updated by`: ghi người duyệt chịu trách nhiệm; nếu AI soạn ghi "AI (tên công cụ), người xác nhận: …".
- `Liên quan đến`: ID chức năng/ task. `Trạng thái duyệt`: để `Draft` cho tới khi người dùng đổi.

### `PJT_Definition`
- Chỉ `B2` (Project Start Date) và `B4` (StartSprint). **Không sửa `B3`** (`=B2`). Hỏi người dùng giá trị thật, không đoán.

### `DauMucTaiLieuCanLam`
- Cột AI điền: **"Đề xuất"** (Yes/No + lý do). Cột "Xác nhận"/ "Phê duyệt" **để trống cho người**.
- Mặc định Yes cho mục có trong mẫu; chọn **User-Story Map hoặc Use-Case Diagram** (một trong hai). Sửa mẫu → bắt buộc có lý do.

### `Component_Detail_Design` (bức tranh lớn — làm **một lần cho cả epic/ hệ thống**, không lặp cho từng chức năng)
- 1.a Yêu cầu nghiệp vụ: gạch đầu dòng, mỗi dòng một yêu cầu, nói **cái gì/ cho ai**, không nói công nghệ.
- 1.b Business Flow: ghi tên ảnh/ file sơ đồ + mô tả bước chính (pool/ lane = bộ phận/ actor). Lấy từ `doc/yeu-cau/project-doc` mục 1–2 và `doc/references/thiet-ke-goc/03-business-process-mockup`.
- 3.b Wire Frame: dẫn tới mockup có sẵn (`doc/references/thiet-ke-goc/03-business-process-mockup`), ghi ID màn hình.
- 5 Công nghệ mỗi layer: **bảng đủ 7 cột**; mỗi công nghệ ghi *Explain (vì sao)* + *Best practice*. Lấy từ stack thật của repo (`pom.xml`, `package.json`, `docker-compose`).
