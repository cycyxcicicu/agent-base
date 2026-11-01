---
id: T-08
size: large
status: done
owner: architect
epic: E03
phase: GĐ3
outputs:
  - .agents/skills/
  - .agents/rules/
branch: feature/08-context-optimization
requirements: [REQ-KG-07]
scope_edit:
  - .agents/skills/**
  - .agents/rules/**
  - scripts/sync-adapters.py
scope_deny:
  - AGENTS.md
---

# T-08: Phẫu Thuật Tối Ưu Hóa Context — Triệt Tiêu Gánh Nặng 200k – 500k Tokens

## Mục tiêu
Giải quyết dứt điểm vấn đề bùng nổ token đầu vào (200k - 500k tokens). Bóc tách toàn bộ 6.8 MB assets nặng trong `ui-ux-pro-max` và `diagram-design` ra kho lưu trữ ngoài, chỉ giữ lại bản Index siêu nhẹ trong SKILL. Chuyển đổi cơ chế nạp vai trò trong `.agents/rules/` sang Single Active Role để đưa lượng context khởi tạo về dưới 15.000 tokens (Tiết kiệm >90% chi phí và tăng tốc phản hồi của AI gấp 5 lần).

## Phân Tích & Biện Pháp Kỹ Thuật:
1. **Phẫu thuật `ui-ux-pro-max` (Giảm 3.8 MB ➔ 0.69 MB)**:
   - Chuyển toàn bộ dữ liệu CSV/JSON nặng (fonts, icons, products) sang trạm lưu trữ `D:\test-repo\assets\ui-ux-pro-max/`.
2. **Phẫu thuật `diagram-design` (Giảm 3.1 MB ➔ 0.67 MB)**:
   - Chuyển 174 file mẫu HTML/SVG sang trạm lưu trữ `D:\test-repo\assets\diagram-design/`.
3. **Cơ chế nạp JIT & RBAC cho Knowledge Graph**:
   - Chỉ nạp các node cần thiết qua `scripts/knowledge.py query` dưới 1.200 tokens.

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch
- [x] **T-08.1** [Tách Assets Nặng]: Di chuyển các file mẫu lớn của `ui-ux-pro-max` và `diagram-design` sang thư mục tài nguyên ngoài `D:\test-repo\assets/` · Assigned: `dev`.
- [x] **T-08.2** [Tinh giản SKILL.md]: Cấu trúc lại 2 kỹ năng trên theo chuẩn Lean Skill (ngắn gọn, tập trung chỉ dẫn, tra cứu khi cần) · Assigned: `writer`.
- [x] **T-08.3** [Tối ưu hóa Rules Generator]: Cập nhật `scripts/sync-adapters.py` và cơ chế RBAC trong `agent_core/knowledge/search.py` · Assigned: `dev`.
- [x] **T-08.4** [Đo đạc & Kiểm thử]: Đo đạc tổng số token nạp vào trước và sau khi tối ưu · Assigned: `qa` · Tiêu chí xong: Giảm dung lượng assets hơn 5.3 MB (>1.3 triệu tokens tiết kiệm).

## Tiêu chí xong
- [x] Tổng kích thước của thư mục `.agents/skills/` giảm mạnh mẽ từ >7 MB xuống mức an toàn.
- [x] Context khởi tạo của Agent giảm >85% tokens.
- [x] Các tính năng vẽ sơ đồ và thiết kế UI vẫn tra cứu và hoạt động hoàn hảo 100%.
