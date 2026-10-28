# Ghi chú bàn giao: T-27

> summary: Hoàn thành khung eval v2: thu thập bằng chứng trước khi xóa sandbox, chấm mù, bắt critical fail và mở rộng CLI.

- **Từ**: dev
- **Đến**: lead, qa, reviewer
- **Loại**: bàn giao task
- **Task**: T-27 (Eval có bằng chứng v2, opt-in — pilot I10–I11)
- **Skill đã chọn & áp dụng**: sparc-methodology
- **Checklist đã tuân thủ**:
  - Giao thức chấm mù tách biệt danh tính candidate, rubric và holdout
  - Thu thập trace/artifacts vào `evidence_root` trước khi sandbox tạm thời bị xóa
  - Phát hiện lỗi nghiêm trọng (path escapes, forbidden writes) và ngăn điểm trung bình che giấu case rớt qua `case_min_score`
  - Giữ nguyên vẹn 100% hợp đồng legacy `run_matrix` và các test hồi quy template `{}`

## Bẫy và hành vi bất ngờ
- Khi chấm mù, `SanitizedBundle` phải loại bỏ tên model khỏi cả output và metadata.
- Điểm NaN từ judge ngoài tầm kiểm soát phải lập tức biến thành trạng thái `inconclusive` và từ chối `passed_v2`.

## Quyết định và lý do
- Cung cấp cờ opt-in `--evidence-mode` trong `scripts/skill-eval.py` thay vì sửa đổi ép buộc, đảm bảo tương thích 100% với các kịch bản đang chạy.
- Toàn bộ bài kiểm tra sử dụng mock deterministic contracts theo đúng tinh thần test đơn vị stdlib.

## Khu vực dễ vỡ
- Không có.

## Việc dở dang
- Không có. 27 tests đạt 100% PASS.
