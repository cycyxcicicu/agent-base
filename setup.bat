@echo off
chcp 65001 >nul
echo ================================================================================
echo 🚀 KHỞI ĐỘNG THIẾT LẬP DỰ ÁN (SETUP WIZARD)
echo ================================================================================
echo Quy trình này sẽ chuẩn bị đầy đủ môi trường trước khi khởi động bất kỳ Agent nào:
echo.

echo 👉 [BƯỚC 1/4] Cấu hình kho kỹ năng & tải repository kiểm dịch...
python "%~dp0scripts\setup-skills.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Cài đặt kỹ năng bị gián đoạn hoặc gặp lỗi. Vui lòng thử lại!
    exit /b %ERRORLEVEL%
)

echo.
echo 👉 [BƯỚC 2/4] Đồng bộ hóa vai trò và quy tắc Agent...
python "%~dp0scripts\sync-adapters.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Lỗi khi đồng bộ adapter!
    exit /b %ERRORLEVEL%
)

echo.
echo 👉 [BƯỚC 3/4] Tạo cầu nối kỹ năng cho Claude Code và Qoder...
python "%~dp0scripts\link-skills.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Không tạo được cầu nối kỹ năng (.claude/skills, .qoder/skills)!
    exit /b %ERRORLEVEL%
)

echo.
echo 👉 [BƯỚC 4/4] Chạy chẩn đoán toàn diện hệ thống...
python "%~dp0scripts\doctor.py"

echo.
echo ================================================================================
echo 🎉 HOÀN TẤT THIẾT LẬP DỰ ÁN! BÂY GIỜ BẠN ĐÃ SẴN SÀNG:
if exist "%~dp0run-frontend.bat" (
    echo   - Chạy frontend: run-frontend.bat
)
echo   - Bắt đầu làm việc với AI: Mở Antigravity / Kilo / Claude Code và chọn vai Lead
echo ================================================================================
echo.
