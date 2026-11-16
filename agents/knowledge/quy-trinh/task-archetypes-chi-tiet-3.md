# Chi Tiết Gói Tri Thức Bó Theo Loại Việc (Phần 3: Gói 5 - 6)

> **Loại: tham khảo.**
> Nguồn: tách từ task-archetypes.md mục Gói 5 - 6.

## 5. Gói Điều Phối & Ủy Thác Subagent (`archetype-delegation`)

Áp dụng cho vai trò Lead khi bóc tách task, giao việc cho Dev/QA và thu gọn ngữ cảnh.

- **Tri thức & Tiêu chuẩn Bắt buộc**:
  1. `agents/protocols/context-budget.md`: Ba trần ngân sách token (Lead $\le$ 50k, Subagent $\le$ 30k, JIT Knowledge $\le$ 1.200).
  2. `agents/protocols/delegation-prompt.md`: Khuôn mẫu prompt ủy thác 8 thành phần, khóa kênh báo cáo.
  3. `agents/protocols/handoff-note.md`: Kiến trúc lưu trữ 4 tầng, lưu theo thư mục `inbox/<Task>/`.
  4. `scripts/notes-index.py`: Tra cứu và lọc báo cáo tự động bằng lệnh CLI `--task <Task>`.
- **Hành động cốt lõi**:
  - Bẻ task thành các subtasks hạt mịn (2–5 phút/phiên).
  - Không cho phép Subagent xả log thô ra chat chính (Zero-Chat Bleeding).
  - Flush trạng thái ra `BOARD.md` và kích hoạt `/compact` khi context $\ge 75\%$.

---

## 6. Gói Viết Đặc Tả & Tách Story (`archetype-spec`)

Áp dụng khi bóc tách User Story từ Task lớn, viết Tiêu chí chấp nhận (A/C) và thiết kế ma trận truy vết kiểm thử.

- **Tri thức & Tiêu chuẩn Bắt buộc (thứ tự đọc)**:
  1. `agents/knowledge/quy-trinh/danh-gia-user-story.md`: Đánh giá 4 tiêu chí và quy tắc tách story khi có 2 nhóm thao tác.
  2. `agents/knowledge/srs/srs-van-phong-ky-thuat.md`: Văn phong tài liệu đặc tả, bóc tách R-xxx và BR-xxx.
  3. `agents/knowledge/srs/srs-fdd-writing-standard.md` (lõi, mục C): Cấu trúc hồ sơ chức năng chuẩn.
  4. `agents/knowledge/quy-trinh/story-ac-test-cau-noi.md`: Chuỗi Task $\rightarrow$ US $\rightarrow$ A/C $\rightarrow$ Test Case và ma trận truy vết RTM hai chiều.
  5. `agents/protocols/test-cases.md`: Chuẩn thiết kế ca kiểm thử và bộ test case.
- **Khóa phạm vi (Scope Gating)**:
  - `scope_edit`: Chỉ file đặc tả trong `doc/features/<UC>/` hoặc tài liệu phân tích nghiệp vụ được giao.
  - `scope_deny`: Cấm sửa mã nguồn (`src/`), cấm sửa file kiến trúc chung.
- **Bằng chứng nghiệm thu**:
  - Bảng phân rã Story đạt 4 tiêu chí (phân loại + giải thích cụ thể), các story có 2 nhóm thao tác được tách riêng.
  - A/C đánh số đầy đủ bao phủ 100% quy tắc nghiệp vụ (BR-xx).
  - Ma trận truy vết RTM hai chiều `US -> BR -> AC -> TC` không có test case mồ côi hay A/C bị bỏ sót.
- **Hộp thư bàn giao**:
  - Ghi báo cáo vào: `doc/notes/inbox/<Task>/<Task>.<Subtask>-ba.md` hoặc `doc/notes/inbox/<Task>/<Task>-ban-giao-spec.md`.
