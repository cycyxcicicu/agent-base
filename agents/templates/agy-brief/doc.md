Loại việc: tài liệu · Model gợi ý: gemini-3.8-flash-medium
Xem luật chung tại [delegation-prompt.md](file:///Users/ducnvh/Documents/agent-base/agents/protocols/delegation-prompt.md) và [spec-writing.md](file:///Users/ducnvh/Documents/agent-base/agents/protocols/spec-writing.md).

## 1. Mục tiêu và Tiêu chí xong
- Mục tiêu: <Soạn thảo hoặc cập nhật tài liệu đặc tả nghiệp vụ/kỹ thuật cho module X>.
- Tiêu chí xong: Không bịa thông tin; qua cổng doc-preflight.py và verify-gate.py; chỗ chưa rõ ghi "chưa kiểm chứng"; mọi con số (mã thoát, dòng, token) phải lấy từ output lệnh thật.
- Tên giao thức, đường dẫn, cờ, mã thoát: chép nguyên văn từ `--help` hoặc mã nguồn, không diễn đạt lại; chưa chắc thì ghi chưa kiểm chứng.

## 2. Phạm vi
- File được tạo/sửa: `<doc/path/to/spec.md>`. Đường dẫn chính xác, cấm dùng glob.
- File cấm chạm: Toàn bộ mã nguồn `src/`, tài liệu gốc `docs/source/`, `AGENTS.md`.

## 3. Định vị
- Điểm can thiệp: Heading `## <Ten_Muc>`, bảng `<Ten_Bang>`, section `<Section_Name>`. Cấm dùng số dòng.

## 4. Lệnh bằng chứng
- Lệnh kiểm tra tiền trạm (python3): `python3 ~/Documents/agent-base/scripts/doc-preflight.py --root . --uc <UC>`
- Lệnh kiểm tra cổng đặc tả (python3): `python3 ~/Documents/agent-base/scripts/verify-gate.py --doc <doc/path/to/spec.md>`
- Gọi bridge với: --allow-write <doc/path/to/spec.md> --allow-cmd python3

## 5. Báo cáo
- Chi tiết ghi vào: `docs/notes/inbox/<Task>/<Task>-agy.md` kèm output cổng kiểm và mục "CHƯA kiểm chứng".
- Chat chỉ 3 dòng: (1) Tài liệu đã tạo/sửa, (2) Kết quả doc-preflight/verify-gate, (3) Đường dẫn báo cáo.
