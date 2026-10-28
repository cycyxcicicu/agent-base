# setup.ps1 - Khởi tạo toàn diện môi trường dự án cho máy mới (1 click)
$ErrorActionPreference = "Stop"

# Tự động đọc tên dự án từ PROJECT.md hoặc thư mục hiện tại
$ProjectName = (Split-Path -Leaf $PSScriptRoot)
$ProjectMd = Join-Path $PSScriptRoot "PROJECT.md"
if (Test-Path $ProjectMd) {
    $matched = Select-String -Path $ProjectMd -Pattern "\|\s*Tên dự án\s*\|\s*([^\|]+)\s*\|" | Select-Object -First 1
    if ($matched -and $matched.Matches[0].Groups[1].Value.Trim()) {
        $ProjectName = $matched.Matches[0].Groups[1].Value.Trim()
    }
}

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "🚀 KHỞI ĐỘNG THIẾT LẬP DỰ ÁN: $ProjectName (SETUP WIZARD)" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Quy trình này sẽ chuẩn bị đầy đủ môi trường trước khi khởi động bất kỳ Agent nào:`n"

# 1. Cấu hình kho kỹ năng & quarantine (hỏi người dùng trước, cấm ổ C)
Write-Host "👉 [BƯỚC 1/4] Cấu hình kho kỹ năng & tải repository kiểm dịch..." -ForegroundColor Yellow
python "$PSScriptRoot\scripts\setup-skills.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Cài đặt kỹ năng bị gián đoạn hoặc gặp lỗi. Vui lòng thử lại!" -ForegroundColor Red
    exit $LASTEXITCODE
}

# 2. Đồng bộ hóa adapter cho các Agent (Kilo, Antigravity, Claude Code, Gemini)
Write-Host "`n👉 [BƯỚC 2/4] Đồng bộ hóa vai trò và quy tắc Agent..." -ForegroundColor Yellow
python "$PSScriptRoot\scripts\sync-adapters.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Lỗi khi đồng bộ adapter!" -ForegroundColor Red
    exit $LASTEXITCODE
}

# 3. Tạo cầu nối skill cho Claude Code (.claude/skills) và Qoder (.qoder/skills)
Write-Host "`n👉 [BƯỚC 3/4] Tạo cầu nối kỹ năng cho Claude Code và Qoder..." -ForegroundColor Yellow
python "$PSScriptRoot\scripts\link-skills.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Không tạo được cầu nối kỹ năng (.claude/skills, .qoder/skills)!" -ForegroundColor Red
    exit $LASTEXITCODE
}

# 4. Chạy kiểm tra chẩn đoán toàn diện (doctor)
Write-Host "`n👉 [BƯỚC 4/4] Chạy chẩn đoán toàn diện hệ thống..." -ForegroundColor Yellow
python "$PSScriptRoot\scripts\doctor.py"

Write-Host "`n================================================================================" -ForegroundColor Green
Write-Host "🎉 HOÀN TẤT THIẾT LẬP DỰ ÁN: $ProjectName!" -ForegroundColor Green
Write-Host "Bây giờ bạn đã sẵn sàng:" -ForegroundColor Green
if (Test-Path (Join-Path $PSScriptRoot "run-frontend.ps1")) {
    Write-Host "  - Khởi chạy frontend: .\run-frontend.ps1" -ForegroundColor White
}
Write-Host "  - Bắt đầu làm việc với AI: Mở Antigravity / Kilo / Claude Code và chọn vai Lead" -ForegroundColor White
Write-Host "================================================================================`n" -ForegroundColor Green
