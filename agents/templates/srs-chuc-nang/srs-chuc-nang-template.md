<!--
KHUNG SRS MỘT CHỨC NĂNG (dạng md) — ánh xạ từng mục sang sheet của mẫu SRS_FDD_Template-v3.0.
Cách dùng: sao chép file này thành doc/srs/<mã>-<slug>.md rồi điền. Quy tắc viết: agents/knowledge/srs/srs-fdd-writing-standard.md
Quy ước: bỏ các chú thích <!-- --> khi xong; chỗ chưa rõ ghi "(chưa xác nhận — hỏi: …)"; KHÔNG tự điền ô "Người duyệt/ Xác nhận".
-->

# SRS — <Tên chức năng>

| Trường | Giá trị |
|---|---|
| **Mã chức năng** | `UC-<nn>` (và `US_<nn>` nếu dùng user story) |
| **Phạm vi** | <màn hình/ service/ module thuộc chức năng này> |
| **Dự án / Epic** | GDT Accounting / <epic> |
| **Trạng thái tài liệu** | Draft <!-- Draft → Đã soát → Approved (chỉ người dùng đổi) --> |
| **Người soạn / Người duyệt** | <tên> / *(để trống cho người duyệt)* |
| **Ngày tạo / cập nhật** | dd/mm/yyyy |
| **Căn cứ** | <SRS mục …; file 05/06/07; code: `…`> |

## 0. Nhật ký thay đổi *(sheet `NhatKyThayDoi`)*
| No. | Ngày | Người sửa | Phần | Nội dung | Ghi chú | Trạng thái duyệt |
|---|---|---|---|---|---|---|
| 1 | dd/mm/yyyy | | Create new | Tạo tài liệu | | Draft |

## 1. Chọn hạng mục thiết kế *(sheet `DauMucTaiLieuCanLam`)*
| Mục | Dùng? (đề xuất) | Hiệu chỉnh mẫu? | Lý do (nếu hiệu chỉnh/ không dùng) | Người duyệt |
|---|---|---|---|---|
| Yêu cầu nghiệp vụ / Business flow | Yes | No | | |
| Wire frame / Luồng màn hình | Yes | No | | |
| User-Story Map **hoặc** Use-Case Diagram | <chọn một> | | | |
| Use-case **hoặc** User Story | <chọn một> | | | |
| Sequence / Activity diagram | | | | |
| ERD / Biểu đồ lớp | | | | |
| Đặc tả service/ API | | | | |
| NFR | Yes | | | |
| Đánh giá tác động | Yes | | | |
| RTM / WBS / Test | Yes | | | |

## 2. Tác nhân *(sheet `Actors_Peronas`)*
| Tác nhân | Mô tả (vai trò, quyền, mục tiêu trên chức năng này) | Nguồn |
|---|---|---|
| <Kế toán / Telesale / CSKH / Kho / …> | | SRS mục 2.3 |

## 3. Bối cảnh & yêu cầu nghiệp vụ *(sheet `Component_Detail_Design` 1–3)*
### 3.1 Yêu cầu nghiệp vụ
- <mỗi dòng một yêu cầu: cái gì, cho ai>
### 3.2 Luồng nghiệp vụ (Business flow)
<mô tả từng bước chính; dẫn tới sơ đồ: `doc/thiet-ke/03-…` hoặc ảnh `doc/yeu-cau/project-doc/…`>
### 3.3 Màn hình & wireframe
| ID màn hình | Tên | Nguồn mockup | Ghi chú |
|---|---|---|---|
### 3.4 User-Story Map *(nếu chọn)*
| Hoạt động | Nhiệm vụ | Release 1 (MVP) | Release 2 |
|---|---|---|---|

## 4. Use-case / User Story *(sheet `Functions_Services_Detail_Desig` mục 1)*
<!-- Chọn MỘT kiểu và dùng thống nhất. -->
### 4A. Use-case
| Trường | Nội dung |
|---|---|
| Mã / Tên | `UC-<nn>` — |
| Mô tả | |
| Tác nhân chính / phụ | |
| Tiền điều kiện | |
| Điều kiện sau khi hoàn thành | |
| Mức độ cần thiết / Phân loại | |

**Luồng chính**
1.1 …
1.2 …

**Luồng thay thế**
- 2.1 …

**Luồng ngoại lệ** *(bắt buộc: lỗi hệ thống, hết phiên, dữ liệu sai)*
- 3.1 …

### 4B. User Story
- **ID:** `US_<nn>`  **Tiêu đề:** 
- **As a** <vai trò>, **I want to** <mục tiêu> **so that** <lợi ích>.
- **Story points:** *(đề xuất)*

**Tiêu chí chấp nhận (A/C)** — mỗi A/C kiểm chứng được, lấy từ SRS (`AC-xx`)
| A/C | Nội dung | Nguồn |
|---|---|---|
| AC 1 | | SRS … |

**DoR (sẵn sàng làm)** *(đề xuất)*: UI/UX ☐ · Tài liệu kỹ thuật ☐ · Dữ liệu mẫu ☐ · Phụ thuộc ☐
**DoD (hoàn thành)** *(đề xuất)*: Code review ☐ · Test ☐ · Nghiệm thu A/C ☐ · Hiệu năng ☐ · Tài liệu ☐

## 5. Thiết kế giao diện *(mục 2a)*
### 5.1 Màn hình <ID>
<ảnh/ mô tả bố cục>

**Business Rules**
| Vùng/ nút/ ô | Quy tắc (bắt buộc, định dạng, ràng buộc, nhãn trạng thái) | Nguồn |
|---|---|---|

## 6. Đặc tả service / API *(mục 2b)*
### 6.1 <Tên service> — `<METHOD> /api/v1/…`
**Request**
| No | Param | Type | Bắt buộc | Ví dụ | Mô tả | Ghi chú |
|---|---|---|---|---|---|---|

```json
{ "mẫu request": "…" }
```
**Response**
| No | Item | Type | Bắt buộc | Ví dụ | Mô tả | Ghi chú |
|---|---|---|---|---|---|---|

```json
{ "mẫu response": "…" }
```
**Lỗi:** <mã/ thông báo> | **Nguồn code:** `presentation.api.<domain>.<Controller>`

## 7. Sơ đồ *(mục 3)*
- **Sequence:** <mermaid hoặc mô tả theo bước; bỏ nếu đã đủ trong luồng use-case>
- **Activity:** <khi có rẽ nhánh>
- **ERD / Lớp:** bảng/ entity thật: `<EntityName>` (bảng `…`) — quan hệ …

## 8. Yêu cầu phi chức năng *(mục 4)*
| TT | Yêu cầu | Mô tả (đo được) | Giải pháp |
|---|---|---|---|
<!-- Đối chiếu hệ thống thật; không dùng NFR mẫu/ mục II của SRS nếu chưa kiểm chứng. -->

## 9. Đánh giá tác động *(mục 5)*
**Cấu phần kích hoạt code**
| STT | Cấu phần (file/ module thật) | Mô tả | Thay đổi do yêu cầu? |
|---|---|---|---|

| Phạm vi | Thay đổi? | Mô tả | Ghi chú/ rủi ro hồi quy |
|---|---|---|---|
| Source code | | | |
| Library | | | |
| Config/ Environments | | | |
| Assets | | | |
| Infrastructure | | | |
| CSDL (Liquibase) | | | |

## 10. Công nghệ & cài đặt *(mục 6 — chỉ phần thay đổi)*
| Layer | Công nghệ | Vì sao | Best practice |
|---|---|---|---|

## 11. Kế hoạch (WBS) *(sheet `WBS_Planning`)*
| No | Task | Ghi chú/ Giả định | Est (MH) | Pre | Assignee | Kết quả nghiệm thu | Trạng thái | Người duyệt |
|---|---|---|---|---|---|---|---|---|
<!-- 1 task ≈ ≤ 1 MD (6,4 giờ), một kết quả kiểm chứng được. Ước lượng là đề xuất. -->

## 12. Truy vết yêu cầu (RTM) *(sheet `Function_RTM`)*
| No | Yêu cầu | SRS/ A/C ref | UI ref | Code ref (đường dẫn thật) | Unit test ref | Integration/ System test ref | UAT ref | Xác nhận (người) |
|---|---|---|---|---|---|---|---|---|

## 13. Kịch bản kiểm thử *(sheet `TDD-TestScenario`)*
**Happy path**
| No | Thứ tự | Test case ID | Hành động của người dùng | Kết quả mong đợi (góc nhìn người dùng) |
|---|---|---|---|---|

**Lỗi/ dữ liệu sai/ ngoại lệ** — cùng bảng.

## 14. Test case *(sheet `TDD_TestCases`)*
| ID | Name | Summary | Step | Expected results | Trạng thái test | Dev xử lý | UC ref | A/C ref |
|---|---|---|---|---|---|---|---|---|
<!-- ID: HP_xx / EC_xx / UT_xx. Trạng thái test: Pass | Fail | Not run — không tự ghi Pass. Mỗi A/C ≥ 1 case. -->

## 15. Rủi ro & quyết định *(sheet mở rộng — dùng khi cần)*
**Rủi ro:** `RISK-<nn>` — mô tả · ảnh hưởng/ xác suất · mitigation · người phụ trách.
**Quyết định kiến trúc:** `ADR-<nn>` — bối cảnh · phương án A/B (điểm, trọng số) · chọn · lý do · hệ quả.

## 16. Câu hỏi chờ xác nhận
- [ ] <câu hỏi 1>
