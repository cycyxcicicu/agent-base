> summary: T-10 xác minh Lauren Tan/pstack bằng nguồn chính chủ; phân biệt source hiện tại với bài nói tháng 8.

Task: T-10        Agent: researcher        Ngày: 2026-10-27

## Đã làm
- Xác minh Lauren Tan là @poteto, khác Garry Tan. GitHub hiện ghi kỹ sư @xai-org/React compiler; workshop Maven 12/08/2026 giới thiệu Member of Technical Staff tại Cursor. Không suy rằng làm tại mạng xã hội X.
- Đọc source primary create/maintain verification, Benny repro, feature-map example, principle-prove-it-works và encode-lessons-in-structure. Không cài hoặc chạy code ngoài.

## Nguồn và định vị
- https://github.com/poteto — profile tác giả, đọc 27/10/2026.
- https://maven.com/p/e23d9c/how-cursor-turned-ai-agents-into-better-engineers — workshop 12/08/2026; chapter 08:35 verification/map, 20:04 eval, 26:34 local/cloud, 41:00 CI/Dune.
- https://raw.githubusercontent.com/cursor/plugins/main/pstack/plugin.json — tại ngày đọc raw main ghi 0.15.34, Lauren Tan/MIT; chưa pin commit.
- https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md — Launch/Doctor/Drive/Evidence/Cleanup, feature map và tự chạy skill được sinh trước bàn giao.
- https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md — đọc source và chạy live; phân biệt doc drift, harness gap, product regression.
- https://github.com/cursor/plugins/blob/main/pstack/automations/benny/skills/reproduce-and-fix-issues/SKILL.md — source Benny hiện hành, không confirmed repro thì không author fix; đã có fix thì verify mode. Không coi mọi chi tiết hiện tại là nội dung workshop tháng 8.
- https://github.com/cursor/plugins/blob/main/pstack/agents/comment-sicko.md — có ngoại lệ giữ comment; pasted text cấm tuyệt đối là quá rộng.

## Lưu ý cho agent sau
- Chỉ thấy title/shell YouTube, chưa đọc transcript primary. Timestamp trên là chapter host Maven công bố, không gán sang bản reupload khác.
- Chưa xem source Dune nội bộ hoặc tái lập thành tích PR/ROI. Không khẳng định có/không quy tắc ba lần review ở mọi nơi.
- Bản ví dụ https://github.com/poteto/verification-skill-example ghi rõ sản phẩm hư cấu; dùng để học cấu trúc, không coi là benchmark.
- Graph đề xuất có thể nối Requirement/Feature/Scenario/Journey/Harness/Evidence; đây là đề xuất áp dụng, không phải kiến trúc chính chủ đã xác minh.
- Không nhập policy comment, quyền auto-merge hoặc automation vào repo; giữ AGENTS/RACI và cổng rủi ro hiện có. Nguồn main thay đổi; xem lại trước dùng, hạn đề xuất 25/01/2027.

## Việc dở dang và thay đổi dùng chung
Không sửa code/quy tắc/tech-radar. Researcher tổng hợp report sở hữu file riêng; note này chỉ lưu provenance và caveat.

Skill đã chọn & áp dụng: không áp dụng skill chuyên biệt.
Checklist đã tuân thủ: primary sources; không cài/chạy code ngoài hoặc gửi thông điệp dịch vụ; phân biệt current source với workshop; không đọc bí mật; chỉ ghi đúng note được giao.
