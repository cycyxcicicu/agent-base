Loại việc: sơ đồ · Model gợi ý: gemini-3.8-flash-medium
Xem luật chung tại [quy-trinh-ve-so-do-bang-json.md](file:///Users/ducnvh/Documents/agent-base/agents/knowledge/diagrams/quy-trinh-ve-so-do-bang-json.md) và [delegation-prompt.md](file:///Users/ducnvh/Documents/agent-base/agents/protocols/delegation-prompt.md).

## 1. Mục tiêu và Tiêu chí xong
- Mục tiêu: <Thiết kế sơ đồ kiến trúc hoặc luồng xử lý cho ca sử dụng X>.
- Tiêu chí xong: Viết spec JSON chuẩn, check pass, sinh đủ .drawio và .png; cấm viết XML tay hoặc Mermaid thô; vẽ cả nhánh lỗi/từ chối/hết quota, không chỉ đường thành công; mỗi khung lặp/rẽ nhánh có nhãn điều kiện.
- Tên giao thức, đường dẫn, cờ, mã thoát: chép nguyên văn từ `--help` hoặc mã nguồn, không diễn đạt lại; chưa chắc thì ghi chưa kiểm chứng.

## 2. Phạm vi
- File được tạo: `doc/diagrams/<ten>.spec.json`, `doc/diagrams/<ten>.drawio`, `doc/diagrams/<ten>.png`. Cấm glob.
- File cấm chạm: Toàn bộ mã nguồn `src/`, file sơ đồ khác ngoài `<ten>.*`.

## 3. Định vị
- Điểm can thiệp: Node `<NodeId>`, nhóm `<GroupId>`, kết nối `<EdgeId>` trong spec JSON. Cấm dùng số dòng.

## 4. Lệnh bằng chứng
- Lệnh kiểm tra spec (python3): `python3 ~/Documents/agent-base/scripts/ve-so-do.py doc/diagrams/<ten>.spec.json --check-only`
- Lệnh sinh sơ đồ (python3): `python3 ~/Documents/agent-base/scripts/ve-so-do.py doc/diagrams/<ten>.spec.json`
- Gọi bridge với: --allow-write doc/diagrams/<ten>.spec.json doc/diagrams/<ten>.drawio doc/diagrams/<ten>.png --allow-cmd python3

## 5. Báo cáo
- Chi tiết ghi vào: `docs/notes/inbox/<Task>/<Task>-agy.md` kèm output check/render và mục "CHƯA kiểm chứng".
- Chat chỉ 3 dòng: (1) Sơ đồ đã sinh, (2) Kết quả lệnh ve-so-do.py, (3) Đường dẫn ảnh PNG.
