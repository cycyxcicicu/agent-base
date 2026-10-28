> summary: Hoàn thành T-23 kiểm điều kiện nhận task claim_task bản cố vấn độc lập với 5 tiêu chí G0, SEQ, DoR, BLK, PLAN.
# Handoff Note: T-23 — Kiểm điều kiện nhận task (Claim Check) bản cố vấn

- **Task**: T-23
- **Agent**: dev
- **Ngày**: 2026-10-28

## 1. Việc đã làm
- Cài đặt `agent_core/workflow/claim_check.py`:
  - `check_task_claim`: Đánh giá 5 tiêu chí nhận task:
    - G0: Xác thực chữ ký con người bằng file (`- [x] **Người dùng duyệt...**` hoặc batch approval).
    - SEQ: Đảm bảo toàn bộ task phụ thuộc đã `done`.
    - DoR: Đảm bảo mục tiêu, tiêu chí xong, scope_edit và subtasks có handoff.
    - BLK: Phát hiện và chặn nếu có >= 2 phương án kiến trúc mà thiếu ADR.
    - PLAN: Phát hiện xung đột phạm vi `scope_edit` với các task đang ở trạng thái `doing`.
- Cài đặt CLI `scripts/task-claim-check.py` với thông báo chẩn đoán cố vấn minh bạch và 3 mã thoát (0, 1, 2).
- Tạo bộ kiểm thử `tests/test_claim_check.py` (5 tests) bao phủ 100% các tiêu chí và trường hợp âm/dương.

## 2. Ghi chú cho agent sau
- Đã hoàn tất T-23. Chuyển sang thực hiện T-24 sinh RTM.

Skill đã chọn & áp dụng: sparc-methodology
Checklist đã tuân thủ:
- Phân biệt rõ ràng giữa chẩn đoán cố vấn và cưỡng chế cấp host.
- TDD đúng chuẩn, không thêm dependency.
