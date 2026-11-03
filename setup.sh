#!/usr/bin/env bash
# setup.sh - Khởi tạo toàn diện môi trường dự án cho macOS / Linux (1 command)
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_NAME="$(basename "$DIR")"
if [ -f "$DIR/PROJECT.md" ]; then
    PARSED_NAME=$(grep -E '\|\s*Tên dự án\s*\|' "$DIR/PROJECT.md" | head -n 1 | awk -F'|' '{print $3}' | tr -d '[:space:]')
    if [ -n "$PARSED_NAME" ]; then
        PROJECT_NAME="$PARSED_NAME"
    fi
fi

echo "================================================================================"
echo "🚀 KHỞI ĐỘNG THIẾT LẬP DỰ ÁN: $PROJECT_NAME (SETUP WIZARD)"
echo "================================================================================"
echo "Quy trình này sẽ chuẩn bị đầy đủ môi trường trước khi khởi động bất kỳ Agent nào:"
echo ""

echo "👉 [BƯỚC 1/4] Cấu hình kho kỹ năng & tải repository kiểm dịch..."
python3 "$DIR/scripts/setup-skills.py"

echo ""
echo "👉 [BƯỚC 2/4] Đồng bộ hóa vai trò và quy tắc Agent..."
python3 "$DIR/scripts/sync-adapters.py"

echo ""
echo "👉 [BƯỚC 3/4] Tạo cầu nối kỹ năng cho Claude Code và Qoder..."
if ! python3 "$DIR/scripts/link-skills.py"; then
    echo ""
    echo "❌ Không tạo được cầu nối kỹ năng (.claude/skills, .qoder/skills)!"
    exit 1
fi

echo ""
echo "👉 [BƯỚC 4/4] Chạy chẩn đoán toàn diện hệ thống..."
python3 "$DIR/scripts/doctor.py"

echo ""
echo "================================================================================"
echo "🎉 HOÀN TẤT THIẾT LẬP DỰ ÁN: $PROJECT_NAME!"
echo "Bây giờ bạn đã sẵn sàng:"
if [ -f "$DIR/run-frontend.sh" ]; then
    echo "  - Khởi chạy frontend: ./run-frontend.sh"
elif [ -d "$DIR/frontend-v1-nextjs" ]; then
    echo "  - Khởi chạy frontend: cd frontend-v1-nextjs && npm run dev"
fi
echo "  - Bắt đầu làm việc với AI: Mở Antigravity / Kilo / Claude Code và chọn vai Lead"
echo "================================================================================"
echo ""
