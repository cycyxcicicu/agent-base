> summary: T-11 QA: hai lỗi skill-eval do dấu ngoặc nhọn trong đường dẫn TEMP; baseline chưa xanh.

Task: T-11 | Agent: qa | Ngày: 2026-10-27

## Đã làm và bằng chứng trực tiếp
- Chạy `python -m unittest tests.test_skill_eval -q`: exit 1, 17 tests trong 7.546s, 2 failures, không error/skip; 15 tests còn lại qua. Không chạy lại full suite.
- TÁI HIỆN ĐƯỢC trên working tree hiện tại, chưa trên main sạch: `tests.test_skill_eval.TestCli.test_run_end_to_end_with_external_commands` (tests/test_skill_eval.py:116) và `tests.test_skill_eval.TestExamplesAndDisguise.test_agent_under_test_never_sees_eval_in_paths` (:224).
- Cả hai trace kết thúc `AssertionError: 1 != 0 : LỖI: '3a6989c8-9c48-4fb5-948b-913e5142d8bb'`. Kỳ vọng CLI exit 0 và hoàn tất báo cáo; thực tế CLI exit 1 trước hoàn tất.

## Chẩn đoán và mức chắc chắn
- **Mid — lỗi tương thích đường dẫn của CLI có kích hoạt bởi môi trường**, không phải bằng chứng model-family hỏng: `scripts/skill-eval.py:61` gọi `tok.format(**values)` cho mọi token lệnh, bao gồm đường dẫn tuyệt đối của runner/probe do fixture tạo trong TEMP (`tests/test_skill_eval.py:114`, :222). TEMP của tiến trình kiểm tra có dạng `.../Packages/sandbox.{UUID}/AC/Temp`. Formatter hiểu `{UUID}` là tên placeholder, nhưng mapping ở `scripts/skill-eval.py:151` chỉ chứa model/skill_file/prompt_file/sandbox, nên phát sinh KeyError; catch :195–197 in UUID rồi exit 1. UUID thay đổi theo tiến trình sandbox; không coi giá trị UUID cụ thể là invariant.
- Kiểm tra `Get-Command python` cho đường dẫn executable thông thường không chứa dấu ngoặc nhọn. `TEMP` và `TMP` có ngoặc nhọn. Các test example dùng runner trong repo, còn TEMP được truyền qua giá trị placeholder, đã qua: phù hợp với cơ chế formatter chỉ diễn giải trực tiếp template.
- `TestCore.test_model_family`, `TestCore.test_judge_must_be_independent`, `TestCli.test_plan_rejects_same_family_judge` đều qua trong lượt trên. Parser tại `agent_core/eval/skill_eval.py:123–136` không được gọi tại chỗ lỗi format. Chưa đánh giá tính đầy đủ của thuật toán nhận họ model cho các tên ngoài fixture.
- **Lỗi môi trường baseline do runner báo, chưa tái chạy/xác nhận từng case ở lượt QA này:** full suite 234 tests, 38 failures, 3 errors, 1 skip; nhiều fixture git init bị từ chối ghi `.git/config`, mklink bị từ chối. Kiểm tra tĩnh xác nhận các fixture cần git init/config tại tests/test_git_hooks.py:62–65, tests/test_hard_check.py:135–137, tests/test_feature_map_check.py:113–115, tests/test_merge_gate_e2e.py:38–41. `tests/test_link_skills.py:54–75` tạo junction rồi symlink, thất bại cả hai thì SkipTest. Không thể suy ra toàn bộ 38 failures/3 errors đều do môi trường nếu chưa đối chiếu từng trace.

## Bàn giao và giới hạn
- Lead/Dev cần scope/card và test hồi quy riêng cho literal braces trong command path trước sửa CLI. Không sửa code/test để làm baseline xanh, không chuyển TEMP hoặc vượt sandbox. Không đóng lỗi; chưa kiểm tra main sạch/phiên bản khác.
- Working tree có rất nhiều thay đổi từ trước; chỉ tạo note này, không hoàn tác hoặc nhận ownership thay đổi người khác. Không git ghi, cài đặt, mạng, dữ liệu thật hoặc đọc bí mật.
- Thay đổi dùng chung cho agent-base: không có.

Skill đã chọn & áp dụng: systematic-debugging — đọc lỗi, tái hiện tối thiểu, lần ngược template/path và so sánh test đang qua; dừng trước sửa.
Checklist đã tuân thủ: đọc PROJECT/stack/card/role/registry/notes; chỉ sở hữu note; ghi command/exit/trace/nguồn; phân biệt bằng chứng trực tiếp với runner báo và chưa xác minh; không tuyên bố toàn suite qua.
