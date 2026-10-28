> Task: T-07 · Epic: E1 · Vai: lead

# Full workflow — toàn văn §§3, 15–17 (nguyên bản AGENTS.md trước 2026-10-27)

AGENTS.md giữ luật cứng §§1–4, 11–13 từng chữ; §§3 (bảng vai chi tiết) và §§15–17 chỉ còn cổng tóm tắt ở đây. Vai thực thi (dev, mobile, ai-eng, dba, data-eng, devops, designer, ba, architect...) **phải đọc file này trước khi bắt đầu task từ cỡ "vừa"**; lead đọc khi cần chọn vai.

## 3 (chi tiết). Bảng vai trò và luồng việc lớn

| Vai trò | Gọi khi |
|---|---|
| `lead` | luôn: phân cỡ, tách card, giao việc, viết lệnh hoàn tác, điều phối subagent |
| `product` | định hình sản phẩm, thẩm định giá trị kinh doanh, phạm vi MVP, Plan CEO Review |
| `ba` | có tài liệu mới cần nhập và rút yêu cầu, bóc tách OCR tài liệu |
| `analyst` | tài liệu đổi, nhận dự án có sẵn, hoặc nghi tài liệu lỗi thời: phân tích lại, đối chiếu tài liệu với code |
| `researcher` | có công nghệ chưa rõ cần chọn |
| `architect` | việc lớn: spec, chia module sâu (Deep Modules), khai báo phạm vi, quản lý ADR |
| `designer` | có giao diện, vẽ sơ đồ kiến trúc 41 loại SVG |
| `dev` | luôn: cài đặt một task bằng chu trình TDD hạt mịn 2-5 phút, Systematic Debugging |
| `mobile` | phát triển ứng dụng di động đa nền tảng (Flutter, React Native, SwiftUI) |
| `ai-eng` | phát triển module AI/LLM, tối ưu prompt, RAG pipeline, kiểm thử an toàn AI |
| `data-eng` | xây dựng luồng dữ liệu lớn (Kafka/RabbitMQ), pipeline ETL/ELT, kho dữ liệu phân tích OLAP |
| `dba` | có cơ sở dữ liệu, tối ưu truy vấn hoặc di chuyển Zero-Downtime Migration |
| `devops` | CI/CD, môi trường Docker đa tầng, Kubernetes, deploy cloud |
| `sre` | điều tra sự cố môi trường đang chạy chỉ bằng lệnh đọc (Forensics), đo tải benchmark, Post-Mortem |
| `security` | đổi xác thực, gói phụ thuộc, dữ liệu nhạy cảm, hoặc kiểm toán an ninh 4 chiều (CSO) |
| `reviewer`, `qa` | từ cỡ "vừa": rà soát diff theo 5 lăng kính chuyên gia, kiểm thử tự động không flakey |
| `runner` | cần chạy build, test, lint, merge-gate và nhận kết quả thật mà không cho ai sửa gì: chỉ chạy lệnh, không sửa file |
| `debt-hunter` | định kỳ quét comment nợ kỹ thuật `# debt:`, cập nhật sổ nợ `DEBT.md`, đề xuất dọn code rác |
| `writer` | sau mỗi merge: CHANGELOG, tài liệu sống (Living Docs), gộp ghi chú vào sổ tay dự án |

Luồng việc lớn: Người dùng → Lead ↔ Product → BA / Analyst (nếu có tài liệu) → Researcher (nếu cần) → Architect (+ Designer, DBA, Data-Eng, AI-Eng nếu cần) → Dev / Mobile song song (mỗi task một nhánh) → Reviewer + QA (+ Security, SRE nếu cần) → Debt-Hunter rà nợ → kế hoạch commit → **người dùng commit, rebase, đẩy, tạo Merge Request** → Merge gate và CI → Writer gộp ghi chú → người dùng duyệt merge.

## 15. Frontend Patterns & Phản Biện Đề Bài

- **Giao thức phản biện** (`agents/protocols/challenger.md`): Không nhận việc thụ động. Bóc tách XY Problem, rủi ro, và xuất trình **Ma trận 3 Phương án** (Lean MVP / Cân bằng / Toàn diện) trước khi code.
- **Chuẩn Frontend** (`agents/knowledge/frontend-patterns.md`): Ranh giới Server/Client (RSC), vòng đời Store an toàn, Compound Components và Surgical Diffs.

## 16. Phân Rã Subtasks Kiểu Scrum & Cổng Duyệt Kế Hoạch Cho Toàn Bộ Agent

- **Phạm Vi Áp Dụng**: Bắt buộc với **mọi vai trò thực thi** (`dev`, `mobile`, `ai-eng`, `dba`, `data-eng`, `devops`, `designer`, `ba`, `architect`, v.v.).
- **Cấm Bắt Tay Làm Việc Ngay**: Khi nhận task từ cỡ "vừa" trở lên, agent thực thi **tuyệt đối không bắt tay viết code, tài liệu lớn hay chạy lệnh ngay**. Bắt buộc phân tích và bóc tách thành **Subtasks hạt mịn**: mỗi Subtask một mục đích, độc lập, kiểm tra được, vừa một phiên ngắn (2–5 phút); số file chỉ để ước lượng. Mỗi Subtask phải có **Mục đích cụ thể** (làm gì để đạt gì) kèm tiêu chí nghiệm thu rõ ràng.
- **Cổng Duyệt Kế Hoạch Bắt Buộc (Plan Review Gate)**:
  1. Agent thực thi / Lead gửi danh sách Subtasks cho **Người thẩm định chuyên trách** tương ứng:
     * Code nghiệp vụ / Tính năng: `reviewer`
     * Cơ sở dữ liệu / Migration / RLS: `dba` hoặc `reviewer`
     * Hạ tầng / Docker / CI/CD: `devops` hoặc `sre`
     * Module AI / LLM / RAG / Prompts: `ai-eng` hoặc `architect`
     * Kiến trúc lớn & Ranh giới Module: `architect`
     * Quyết định tối cao: `lead` hoặc `Người dùng`.
  2. Người thẩm định kiểm tra: Subtask có quá to không? Có nguy cơ chạy quá 8–10 bước làm phình context không? Thứ tự phụ thuộc có hợp lý không?
  3. **Nếu từ chối (Chưa chuẩn / Còn to)**: Chỉ rõ điểm còn to, gợi ý phương án chia nhỏ hơn (Lean MVP / Surgical Slices); Agent thực thi bắt buộc hiệu chỉnh lại kế hoạch cho đến khi đạt `Plan Approved`.
  4. **Nếu duyệt (Chuẩn)**: Đóng dấu `[x] Plan Approved by <vai-thẩm-định>` trong card, mới được phép cấp Subtask cho Subagent bắt đầu làm.
- **Quy Tắc Thực Thi Subagent (Fresh Subagent per Subtask)**:
  1. **Quy chuẩn mã Subtask**: Đánh số theo dạng `T-<ticket>.<số_thứ_tự>` (ví dụ: `T-57.1`, `T-57.2`). Mỗi Subtask được giao cho một **Subagent mới tinh** với ngữ cảnh cách ly (Clean Context). CẤM giao nguyên cả task card lớn cho 1 subagent chạy liên tục.
  2. **Trần số bước & Micro Handoff Note**: Mỗi Subagent chỉ được chạy tối đa **8 – 10 tool calls**. Hoàn thành subtask hoặc chạm trần là phải dừng, tạo ghi chú bàn giao siêu gọn (3–5 dòng) tại `docs/notes/inbox/<Task>.<Subtask>-<agent>.md` (ví dụ `T-57.1-dev.md`) theo `agents/protocols/handoff-note.md` rồi đóng phiên.
  3. **Xử lý sự cố tràn ngữ cảnh (`Compaction exhausted` / `gateway_timeout`)**: TUYỆT ĐỐI CẤM resume session cũ. Coi phiên đó đã kết thúc, mở phiên mới tinh cho bước kế tiếp hoặc Lead tự nghiệm thu bằng lệnh chỉ đọc.
  4. **Nén Output (Output Bounding)**: Mọi lệnh terminal bắt buộc chạy chế độ rút gọn (`pytest -q --tb=short`, `git status -s`, `docker compose ps`). Không in file lớn (>200 dòng) ra terminal, chỉ đọc bằng slice dòng (`StartLine`/`EndLine`).
  5. **Quy tắc sửa file chéo (Cross-Subtask Edits - 7 Kịch bản)**: Cấm sửa lan man file của subtask khác. Tuân thủ nghiêm ngặt 7 kịch bản (`definition-of-done.md`): (1) File subtask đã xong: chỉ surgical patch + chạy lại regression test; (2) File subtask chưa làm: chỉ stub/mock, cấm code hộ; (3) File config/init: chỉ append/register, cấm xóa/sửa dòng cũ; (4) Breaking Change: DỪNG LẠI NGAY $\rightarrow$ `BLOCKED` báo Lead/Reviewer; (5) File DB Migration: cấm sửa migration cũ, luôn tạo revision mới nối tiếp head; (6) File Test dùng chung (`conftest.py`): chỉ thêm fixture mới, cấm đổi behavior fixture cũ; (7) File Spec (`docs/spec/`): đóng băng đối với Dev, cấm tự sửa spec để hợp thức hóa code.
  6. **Phản hồi Chat 3 dòng của Subagent**: Sau khi ghi file handoff note, Subagent bắt buộc chỉ phản hồi chat đúng 3 dòng: Đã làm / Kết quả test / Đường dẫn file bàn giao, tuyệt đối cấm in code thừa ra chat.

## 17. Tự Động Chọn & Áp Dụng Skill (Skill Auto-Selection Gate)

- **Bắt buộc**: Mọi Agent/Subagent trước khi thực thi task phải tự đối chiếu với danh mục Skills tại `agents/knowledge/skills.md` và đọc tệp `SKILL.md` tương ứng trước khi code.
- **Ánh xạ chính**: Debug/lỗi $\rightarrow$ `systematic-debugging`; Code/refactor $\rightarrow$ `codebase-design`; Review $\rightarrow$ `open-code-review`; UI/CSS $\rightarrow$ `ui-ux-pro-max`; Bảo mật $\rightarrow$ `cso`; Docker/Release $\rightarrow$ `careful` + `ship`; Sơ đồ $\rightarrow$ `archify` / `diagram-design`.
- **Bằng chứng**: Handoff note (`docs/notes/inbox/`) bắt buộc có 2 dòng: (1) `Skill đã chọn & áp dụng: <tên>`, (2) `Checklist đã tuân thủ: <2-3 điểm cụ thể>`. Thiếu dòng này Lead/Reviewer từ chối nghiệm thu ngay.