# Sáu Gói Tri Thức Bó Theo Loại Việc (Task Archetype Bundles)

> **Loại: tham khảo.** Tổng hợp đóng gói các quy chuẩn và kỹ năng theo 6 loại tác vụ điển hình để tra cứu nhanh, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó.

Quy định và tiêu chuẩn trong hệ thống rất nhiều (148+ nodes tri thức, 40+ protocols và skills). Để Agent và lập trình viên không phải tìm kiếm thủ công từng file, toàn bộ quy chuẩn thực tế được đóng gói thành **6 Gói Phản Ứng Nhanh (Task Archetypes)**.

Khi nhận task thuộc loại nào, Agent tra cứu trực tiếp mã gói tương ứng qua lệnh:
`python3 scripts/knowledge.py query -q "archetype-<loại>" --budget 1200`

---

## Bảng Tóm Tắt & Chỉ Mục 6 Gói Tri Thức

| STT | Mã gói | Tên gói nghiệp vụ | Áp dụng khi | File chi tiết |
|---|---|---|---|---|
| 1 | `archetype-bug` | Sửa Lỗi & Tái Hiện Bug | Fix bug, hotfix, defect Mantis | `task-archetypes-chi-tiet-1.md` mục 1 |
| 2 | `archetype-database` | Cơ Sở Dữ Liệu & Migration | Schema DB, index, Liquibase | `task-archetypes-chi-tiet-1.md` mục 2 |
| 3 | `archetype-api` | Xây Dựng & Tối Ưu API | Endpoint REST, Service layer | `task-archetypes-chi-tiet-2.md` mục 3 |
| 4 | `archetype-srs` | Đặc Tả SRS & Thiết Kế Kỹ Thuật | Hồ sơ UC, Excel 14 sheets, Gate 2 | `task-archetypes-chi-tiet-2.md` mục 4 |
| 5 | `archetype-delegation` | Điều Phối & Ủy Thác Subagent | Lead bóc task, khoanh context | `task-archetypes-chi-tiet-3.md` mục 5 |
| 6 | `archetype-spec` | Viết Đặc Tả & Tách Story | Tách US, chuẩn A/C, nối test case | `task-archetypes-chi-tiet-3.md` mục 6 |

---

## Hướng dẫn sử dụng cho Agent

1. **Xác định loại việc:** Đối chiếu task được giao với cột "Áp dụng khi".
2. **Nạp tri thức JIT:** Đọc file chi tiết tương ứng hoặc tra cứu theo mã gói để lấy đúng danh sách tài liệu bắt buộc và phạm vi khóa.
3. **Tuân thủ Scope Gating:** Chỉ sửa file trong `scope_edit`, tuyệt đối không vi phạm `scope_deny`.
