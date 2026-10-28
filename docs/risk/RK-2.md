# RK-2: Dọn dẹp module gemini-api, cookie_rotation và 22 script tạm trong tasks/

Status: APPROVED
Ngày lập: 2026-10-27        Người lập: lead
Mốc kiểm tra: nhánh main, HEAD f12b1a2
Yêu cầu nguyên văn của người dùng: "Dọn sạch toàn bộ (Khuyên dùng): Xóa cả tools/gemini-api, tools/cookie_rotation, cookies/, toàn bộ 22 script thử nghiệm trong tasks/ và cập nhật lại config để repo hoàn toàn tinh gọn và chuẩn mực."

## Đã xác minh (kèm lệnh đã dùng)
- `tools/gemini-api/`: Kho lưu trữ mã nguồn bên thứ 3 clone về, đã nằm trong `.gitignore` dòng 57.
- `tools/cookie_rotation/`: Chứa `account_manager.py`, `cookie_rotator.py` dùng để xoay vòng token cho gemini-api.
- `cookies/`: Chứa file `README.md`, `all_accounts.example.json` và `gemini_cookies.example.json` (tại root).
- `scripts/gemini-research.py`: CLI gọi `tools/gemini-api`.
- `.agents/skills/gemini-deep-research/`: Kỹ năng Deep Research dựa trên gemini-api.
- `tests/test_cookie_rotation.py`: Bộ unit test cho `cookie_rotation`.
- `tasks/`: Chứa 22 file script `.py` và file ảnh `.png` thử nghiệm tạm bợ không thuộc task card.
- Bộ khung lõi `agent_core/` hoạt động độc lập 100%, không phụ thuộc runtime vào `gemini-api`.

## Sẽ mất hoặc bị xóa
1. **Các thư mục & tệp của module gemini-api**:
   - `tools/gemini-api/`
   - `tools/cookie_rotation/`
   - `cookies/`
   - `gemini_cookies.example.json`
   - `scripts/gemini-research.py`
   - `.agents/skills/gemini-deep-research/`
   - `tests/test_cookie_rotation.py`
2. **22 tệp script thử nghiệm và ảnh tạm trong `tasks/`**:
   - `tasks/check_accounts.py`
   - `tasks/check_env.py`
   - `tasks/deep_search_reftoken.py`
   - `tasks/extract_chrome_cookies.py`
   - `tasks/find_key.py`
   - `tasks/inspect_gemini_page.py`
   - `tasks/list_token_files.py`
   - `tasks/quick_search.py`
   - `tasks/run_batch_100.py`
   - `tasks/gemini_page.png`
   - `tasks/test_9router.py`
   - `tasks/test_9router_auth.py`
   - `tasks/test_account_4_full.py`
   - `tasks/test_full_cookies.py`
   - `tasks/test_live_gemini_generation.py`
   - `tasks/test_live_upload.py`
   - `tasks/test_oauth_refresh.py`
   - `tasks/test_profile_cookies.py`
   - `tasks/test_raw_account_auth.py`
   - `tasks/test_raw_cookies.py`
   - `tasks/test_rotate_cookies.py`
   - `tasks/test_saved_profile.py`
   - `tasks/test_text_to_image.py`

## Sẽ được sửa đổi (để đồng bộ và dọn sạch liên kết cũ)
- `.gitignore`: Bỏ các dòng nhắc tới `cookies/`, `gemini_cookies.json`, `tools/gemini-api/`.
- `agents/roles/researcher.md`: Bỏ lệnh cấp quyền chạy `python tools/gemini-api/cli.py*`.
- `scripts/simulate-agent-lifecycle.py`: Xóa import thừa `tools.cookie_rotation`.
- `scripts/doctor.py`: Tối giản hóa, lược bỏ phần hướng dẫn cấu hình token/cookies Google.
- Chạy `python scripts/sync-adapters.py` để cập nhật lại các file adapters.

## Chấp thuận
- Người dùng đã phê duyệt rõ ràng: "Dọn sạch toàn bộ (Khuyên dùng): Xóa cả tools/gemini-api, tools/cookie_rotation, cookies/, toàn bộ 22 script thử nghiệm trong tasks/ và cập nhật lại config để repo hoàn toàn tinh gọn và chuẩn mực."
