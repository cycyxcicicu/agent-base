> summary: Hoàn thành T-21 trích xuất ngữ cảnh tri thức theo vai và ngân sách token với CLI knowledge.py.
# Handoff Note: T-21 — Ngữ cảnh theo vai và task (Context CLI)

- **Task**: T-21
- **Agent**: dev
- **Ngày**: 2026-10-28

## 1. Việc đã làm
- Cài đặt `agent_core/knowledge/context.py`:
  - `build_context`: Lọc tri thức theo vai, task và luật bắt buộc bằng BFS đồ thị.
  - Phụ lục `appendix`: Tách bạch tài liệu `draft/review` khi bật `--include-draft`.
  - Ngân sách token: Ước lượng bảo thủ `ceil(bytes/3)`, ghi nhận `omitted_ids`, báo lỗi khi luật vượt ngân sách.
- Cài đặt CLI `scripts/knowledge.py` hỗ trợ hai lệnh con `validate` và `context` với đầy đủ 4 mã thoát tiêu chuẩn.
- Bổ sung bộ test `tests/test_knowledge_context.py` (5 tests) kiểm thử lọc vai, phụ lục draft, giới hạn ngân sách, tính tất định và gọi CLI.

## 2. Ghi chú cho agent sau
- Đã hoàn tất lát cắt pilot I2. Tiếp tục triển khai T-23 (`claim_task`).

Skill đã chọn & áp dụng: sparc-methodology
Checklist đã tuân thủ:
- Không sử dụng LLM hay thư viện bên ngoài.
- Đáp ứng đầy đủ các yêu cầu R-03 và R-04.
