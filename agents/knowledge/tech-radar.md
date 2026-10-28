# Bản đồ công nghệ (tech radar)

Dùng chung giữa các dự án. Researcher đề xuất, **người dùng duyệt** rồi mới ghi vào đây. Mỗi dòng có ngày kiểm tra gần nhất và nguồn (brief trong `docs/research/`). Quá hạn 90 ngày thì phải kiểm tra lại trước khi dựa vào.

Bốn mức:

- **Dùng**: đã thử, đủ tin cậy, dùng mặc định.
- **Thử**: đáng thử ở dự án nhỏ, chưa thành mặc định.
- **Theo dõi**: chưa thử, đáng để mắt.
- **Tránh**: đã có lý do không dùng (ghi lý do).

## Dùng

| Công nghệ | Dùng cho | Phiên bản | Kiểm tra lần cuối | Brief |
|---|---|---|---|---|
| Git Worktrees | Cô lập nhánh cho từng agent chạy song song | | | |

## Thử

Các mục skill chỉ được cài **chọn lọc** sau khi đã đọc nội dung thật và quét cục bộ (xem brief, bản 2). Chưa ghim phiên bản vì chưa tải về.

| Công nghệ | Dùng cho | Phiên bản | Kiểm tra lần cuối | Brief |
|---|---|---|---|---|
| MarkItDown (dòng lệnh cục bộ, không dùng gói MCP) | ba, analyst: chuyển tài liệu sang markdown | chưa ghim | 2026-09-19 | `docs/research/2026-09-19-danh-gia-skill-ben-thu-ba.md` |
| diagram-design (chỉ thư mục skill; có script Python cần đọc) | designer, architect, ba, analyst: sơ đồ HTML/SVG | chưa ghim | 2026-09-19 | như trên |
| Graphify (`graphifyy`, chỉ `--code-only`, người dùng tự cài, agent chỉ đọc) | analyst, architect, dev: bản đồ codebase lạ qua skill `codebase-map` | 0.9.92 (commit 86c57be) | 2026-10-18 | `docs/research/2026-10-18-graphify.md` |
| archify (thư mục `archify/`, bỏ `archify.zip`, tắt kiểm tra cập nhật, không dùng `brands capture`; cần quyền chạy `node` hẹp) | architect: sơ đồ kiến trúc | chưa ghim | 2026-09-19 | như trên |
| superpowers: chỉ 3 skill (`verification-before-completion`, `test-driven-development`, `systematic-debugging`), không chạy bộ cài | dev, qa | chưa ghim | 2026-09-19 | như trên |
| mattpocock/skills: 6 skill (`writing-for-agents`; `grill-with-docs` + `grilling` + `domain-modeling`; `improve-codebase-architecture` + `codebase-design`) | analyst, architect, writer | chưa ghim | 2026-09-19 | như trên |
| open-code-review (chỉ chế độ Delegation, chỉ vai reviewer; người dùng tự cài và cấu hình; không dùng skill gốc nguyên bản) | reviewer: bổ sung phát hiện lỗi trên diff. Nhận xét chỉ là tham khảo | chưa ghim | 2026-09-19 | như trên, mục 4c |

## Theo dõi

| Công nghệ | Dùng cho | Phiên bản | Kiểm tra lần cuối | Brief |
|---|---|---|---|---|
| ponytail | Tối giản code. Hạ từ "Thử": chỉ yêu cầu một kiểm tra nhỏ cho logic không tầm thường, không bộ test theo hàm trừ khi được yêu cầu, lệch với TDD và định nghĩa hoàn thành; kèm 12 file hook | chưa ghim | 2026-09-19 | `docs/research/2026-09-19-danh-gia-skill-ben-thu-ba.md` |
| promptfoo | Thử prompt và skill có chống được chèn chỉ dẫn không (giai đoạn 3). **Telemetry bật mặc định**: đặt `PROMPTFOO_DISABLE_TELEMETRY=1` | chưa ghim | 2026-09-19 | như trên |
| google/skills | devops, dba, security khi dự án dùng Google Cloud; đọc từng skill, `gcloud*` ở mức hỏi | chưa ghim | 2026-09-19 | như trên |
| i-have-adhd | lead: kiểu trả lời ngắn, người dùng tự gọi; chỉ `SKILL.md`, không hook | chưa ghim | 2026-09-19 | như trên |
| E2B | Sandbox đám mây cho mã không tin cậy (Docker cục bộ đủ lúc này) | chưa ghim | 2026-09-19 | như trên, mục 4b |
| Langfuse | Ghi vết agent, đo chi phí theo tầng model (giai đoạn 4, chưa xác minh với Kilo 7) | chưa ghim | 2026-09-19 | như trên |
| WebMCP | API trình duyệt cho trang web công bố công cụ cho agent; chỉ liên quan khi làm ứng dụng web | bản xem trước sớm | 2026-09-19 | như trên |

## Tránh

| Công nghệ | Lý do | Kiểm tra lần cuối | Brief |
|---|---|---|---|
| AutoGen (bản gốc của Microsoft) | Đã ở chế độ bảo trì, không còn phát triển tính năng mới | 2026-09-19 | (chưa có brief, xem KE-HOACH) |
| gstack (cài bằng bộ cài) | Bộ cài chạy script, đăng ký hook, sửa `CLAUDE.md`; kiểm toán ghi nhận quét thư mục phiên của các agent khác và ghi dấu dùng skill dù telemetry tắt; có lệnh git và deploy; trùng vai trò. Chỉ tham khảo | 2026-09-19 | `docs/research/2026-09-19-danh-gia-skill-ben-thu-ba.md` |
| ECC (cài nguyên khối) | Là một hệ vai trò và quy tắc thứ hai, mâu thuẫn `AGENTS.md`; 292 skill làm phình ngữ cảnh (phàn nàn số một). Chỉ tham khảo | 2026-09-19 | như trên |
| ruflo | 27 hook git, tiến trình chạy nền, CSDL, mạng liên kết; trái quy tắc git; kiểm toán nội bộ nói nhiều hệ số hiệu năng là chuỗi cứng, có con số tạo lúc chạy, có lỗi đảo dấu phần thưởng | 2026-09-19 | như trên |
| webcmd (mặc định) | Điều khiển trình duyệt có phiên đăng nhập thật; xung đột chính sách web. Chỉ cân nhắc cho qa trên `localhost` | 2026-09-19 | như trên |
