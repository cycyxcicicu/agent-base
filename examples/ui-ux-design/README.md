# Ví Dụ Mẫu: Hệ Thống UI/UX Thiết Kế Chuẩn & Biên Dịch Tokens

Thư mục này chứa các dự án mẫu và hệ thống Design Tokens thực thi được trích xuất và tối ưu từ `ui-ux-pro-max-skill`.

## Cấu Trúc Thành Phần
1. `tokens.json`: Định nghĩa Design Token 3 tầng chuẩn W3C DTCG:
   - **Primitive Tokens**: Bảng màu thô, kích thước khoảng cách, bo góc.
   - **Semantic Tokens**: Biến ngữ nghĩa (`bg-canvas`, `text-primary`, `accent`, `container-padding`).
   - **Component Tokens**: Biến gán riêng cho từng thành phần (`btn-primary`, `card`, `badge`).
2. `tokens.css`: File CSS Variables tự động sinh ra bởi trình biên dịch token `generate-tokens.cjs`.
3. `saas-landing.html`: Trang Landing Page SaaS hoàn chỉnh (Dark mode, glow badge, pricing card, micro-interactions).
4. `healthcare-dashboard.html`: Trang Dashboard Y tế / Bệnh án điện tử hoàn chỉnh (Patient telemetry, vitals chart, metric cards, data tables).

## Cách Thực Thi & Kiểm Tra
Biên dịch tokens từ JSON sang CSS:
```bash
node .agents/skills/ui-ux-pro-max/scripts/generate-tokens.cjs --config examples/ui-ux-design/tokens.json -o examples/ui-ux-design/tokens.css
```

Quét kiểm tra vi phạm hardcoded tokens:
```bash
node .agents/skills/ui-ux-pro-max/scripts/validate-tokens.cjs -d examples/ui-ux-design
```
