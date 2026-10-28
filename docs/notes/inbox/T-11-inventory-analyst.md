> summary: T-11 inventory: discovery lệch, eval dọn trước judge, proof chưa bền vững và CI unittest còn áp dụng.

Task: T-11.1 | Agent: analyst | Ngày: 2026-10-27

Đã làm: kiểm tra tĩnh module/CLI/schema/bootstrap/diff/CI và viết `docs/analysis/T-11-current-state.md`; không chạy test, không cài, không web. Tất cả phát hiện có nguồn và mức chắc chắn; snapshot dirty ghi trong report.
Lưu ý: CI hiện cài .[dev] nếu pyproject hợp lệ, nên câu hard-rule “chỉ cài pyyaml” đã cũ; discovery vẫn unittest. Eval xóa sandbox trước judge. Frontier một cấp và parser legacy không khớp YAML trạng thái/nested card. Bootstrap rerun có nguy cơ mất baseline metadata (suy đoán, cần fixture).
Bàn giao: Architect/Lead chốt contract discovery/evidence và phạm vi file dùng chung; runner xác minh baseline. RK-2 đã dọn cookie/tasks, không dọn lại. Không sửa CODEMAP vì ngoài ownership; chưa có Graphify report.
Thay đổi dùng chung cho agent-base: không có; chỉ report và note thuộc T-11.
Skill đã chọn & áp dụng: codebase-map (kiểm kê module trong report theo scope), writing-for-agents (kết luận trước, nguồn cạnh phát hiện).
Checklist đã tuân thủ: đọc PROJECT/notes/card/role/registry; không đọc bí mật; code chỉ đọc; không chạy test/git ghi; không revert thay đổi người khác; ghi giới hạn và câu hỏi cho Lead.
