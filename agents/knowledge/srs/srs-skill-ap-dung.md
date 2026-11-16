> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục G

# Kỹ năng (Skill) áp dụng khi viết tài liệu thiết kế SRS_FDD (Mục G)

Skill nằm ở `~/.claude/skills`. Skill có `disable-model-invocation` chỉ chạy khi người dùng gõ tên (`/grill-me`...). Mọi skill phải theo các quy tắc của workspace: ghi tài liệu vào `doc/` (không vào thư mục service), không commit, không đăng lên issue tracker, văn phong kỹ thuật chuẩn mực.

| Bước | Skill | Cách dùng |
|---|---|---|
| Làm rõ yêu cầu | `grill-me`, `grill-with-docs` | Người dùng gọi. Phỏng vấn để chốt phạm vi. Nếu skill tạo ADR hoặc glossary, đặt vào `doc/` chứ không vào `docs/` của service. |
| Câu hỏi cho BA/ Kế toán | `to-questionnaire` | Biến mục "Câu hỏi mở" thành bảng câu hỏi gửi người khác. |
| Thuật ngữ, mô hình miền | `domain-modeling` | Chuẩn hoá thuật ngữ nghiệp vụ trước khi viết. File glossary đặt trong `doc/`. |
| API | `api-design` | Soát đặc tả API; quy ước `doc/architecture/engineering/api-conventions.md` thắng khi khác nhau. |
| Sơ đồ | `diagram-design`, `archify` | Sơ đồ kiến trúc, sequence, ER, state: xuất ảnh/ SVG để đính kèm. Sơ đồ nhỏ trong md vẫn dùng Mermaid. |
| Quyết định kiến trúc | `architecture-decision-records` | Cho sheet ADR. Đổi nơi lưu mặc định `docs/adr/` thành `doc/architecture/adr/`. |
| Chia task (WBS) | `to-tickets` | Chỉ ở chế độ file cục bộ. Không đăng lên tracker. |
| Test | `tdd`, `springboot-tdd`, `test-value` | Dùng ở bước code và unit test. Happy case vẫn theo `qa-process.md`. |
| Migration | `database-migrations` | Author changeset mới luôn là `ducnvh`. |
| Review code | `open-code-review`, `open-code-review-delegate` | Xem `ky-thuat/chuan-code-va-review.md` mục 5. Chỉ chạy khi người dùng đồng ý. |

Không dùng cho tài liệu này:
- `to-spec`: đăng spec lên issue tracker. Spec viết tay theo khung `srs-chuc-nang-template.md`.
- `writing-for-agents`: dành cho tài liệu để agent đọc (skill, CLAUDE.md), không phải SRS cho người đọc.
- `git-workflow`, `pr`, `implement`: quy tắc `agents/knowledge/quy-trinh/git-workflow.md` thắng; không commit, không tạo MR khi chưa được nói rõ.
