# Ví Dụ Mẫu: Phản Biện Kế Hoạch & Thẩm Định Phiếu Công Việc (Plan Review Gate)

Thừa hưởng từ các kỹ thuật thẩm định chặt chẽ của `gstack` (`plan-ceo-review` & `plan-eng-review`), thư mục này cung cấp bộ khung phản biện 2 lớp và công cụ tự động hóa kiểm định:

## Các Thành Phần
1. `ceo-eng-rubric.md`: Cẩm nang 10 câu hỏi cốt tử chia làm 2 bộ lọc:
   - **CEO Review**: Thẩm vấn về giá trị người dùng, bẫy Scope Creep và chỉ số thành công.
   - **Eng Review**: Thẩm vấn về Blast Radius, Rollback strategy, Database safety và Idempotence.
2. `review_gate.py`: Script Python tự động thẩm định xem Task Card hoặc Kế hoạch có đáp ứng đủ 5 trụ cột bắt buộc (Blast Radius, Rollback, Vertical Slice, Acceptance Criteria, Blocked By) trước khi được duyệt chuyển sang trạng thái Coding.

## Cách Thực Thi Kiểm Định Kế Hoạch / Task
```bash
python examples/plan-reviews/review_gate.py tasks/T-01.md
```
