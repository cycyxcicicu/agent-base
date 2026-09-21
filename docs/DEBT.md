# Sổ Cái Nợ Kỹ Thuật (Technical Debt Ledger)

> Tự động thu hoạch bởi `src/debt/ledger.py` theo triết lý Ponytail.
> Tổng số khoản nợ được ghi nhận: **10**

| Vị trí (File:Dòng) | Đi Tắt (Shortcut) | Trần Chịu Đựng (Ceiling) | Lộ Trình Nâng Cấp (Upgrade) |
| :--- | :--- | :--- | :--- |
| `.agents\rules\role-dev.md:29` | <giải pháp> | **<ngưỡng>** | <khi nào sửa>`. |
| `.agents\rules\role-reviewer.md:66` | `**: Nếu Dev dùng giải pháp đi tắt tạm thời, bắt buộc phải có comment chuẩn: `# debt: <giải pháp> | **<ngưỡng>** | <khi nào sửa>`. |
| `.kilo\agents\dev.md:115` | <giải pháp> | **<ngưỡng>** | <khi nào sửa>`. |
| `.kilo\agents\reviewer.md:99` | `**: Nếu Dev dùng giải pháp đi tắt tạm thời, bắt buộc phải có comment chuẩn: `# debt: <giải pháp> | **<ngưỡng>** | <khi nào sửa>`. |
| `agents\roles\dev.md:47` | <giải pháp> | **<ngưỡng>** | <khi nào sửa>`. |
| `agents\roles\reviewer.md:80` | `**: Nếu Dev dùng giải pháp đi tắt tạm thời, bắt buộc phải có comment chuẩn: `# debt: <giải pháp> | **<ngưỡng>** | <khi nào sửa>`. |
| `docs\research\deep-dive-18-repos-analysis.md:138` | <giải pháp đi tắt> | **<ngưỡng chịu đựng>** | <mốc thời gian sửa chữa>`. |
| `tasks\_template.md:38` | <giải pháp> | **<ngưỡng>** | <khi nào sửa>` |
| `tests\test_debt.py:10` | dùng sqlite thay vì postgres để test nhanh | **50 requests/s** | chuyển sang postgres pool" |
| `tests\test_debt.py:23` | hardcode timeout 10s | **100 users** | đọc từ env config\n" |
