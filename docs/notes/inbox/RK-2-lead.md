# Ghi chú bàn giao: Dọn dẹp gemini-api & cookie_rotation theo RK-2

- **Task**: RK-2 (Dọn dẹp module gemini-api, cookie_rotation, cookies và script tạm trong tasks/)
- **Người thực hiện**: lead
- **Ngày**: 2026-10-27

## Việc đã làm
1. Đã xóa hoàn toàn các thư mục/tệp liên quan đến gemini-api:
   - `tools/gemini-api/`
   - `tools/cookie_rotation/`
   - `cookies/`
   - `gemini_cookies.example.json`
   - `scripts/gemini-research.py`
   - `.agents/skills/gemini-deep-research/`
   - `tests/test_cookie_rotation.py`
2. Đã dọn sạch toàn bộ 22 script tạm và ảnh `.png` trong `tasks/`. Thư mục `tasks/` hiện tại chỉ chứa đúng cấu trúc Scrum Markdown chuẩn.
3. Đã làm sạch các file build cache (`build/`, `agent_base.egg-info/`, `.pytest_cache/`).
4. Cập nhật `.gitignore`, `agents/roles/researcher.md`, `scripts/simulate-agent-lifecycle.py`, `scripts/doctor.py`.
5. Đã sửa link tuyệt đối OneDrive trong `README.md`.
6. Đã chạy lại `scripts/sync-adapters.py` để đồng bộ toàn bộ 20 vai trò và adapters trên mọi công cụ.

## Kết quả kiểm tra
- `python scripts/doctor.py`: PASS, 100% xanh, không còn cảnh báo cookies.
- `python scripts/hard-check.py`: PASS (820 files scanned, 0 errors).
- `pytest tests/test_core.py tests/test_debt.py tests/test_eval.py tests/test_design.py tests/test_ingest.py`: 44/44 passed.

## Lưu ý cho agent sau
- Hệ thống hoàn toàn không còn phụ thuộc vào `gemini_webapi` hay `tools/gemini-api`.
- Nghiên cứu web của vai `researcher` giờ đây sử dụng các công cụ web chuẩn (Google Search API, DuckDuckGo hoặc công cụ tìm kiếm của môi trường IDE).
