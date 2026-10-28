# Quy trình của công ty (ghi chú từ tài liệu hướng dẫn)

> **Loại: tham khảo.** Chép từ dự án gdt-workspace để làm tri thức cho agent, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Là ghi chú quy trình công ty; bảng mục 8 chỉ ra phần khung đã có hay đã bổ sung.

Nguồn: sáu bản tổng hợp ở `doc/quy-trinh/huong-dan/tong-hop/` của gdt-workspace (từ slide, PDF, Google Doc đã tải). Đây là **ngữ cảnh**, không thay `AGENTS.md`. Giới hạn của nguồn: video chưa xem được, hình và sơ đồ trong slide không đọc được, một số tài liệu chưa có quyền tải (Doc GitFlow guideline, mẫu SRS&WBS, RTM, Test plan).

## 1. Luồng chính (SDLC với Scrum và TDD)

1. Phân tích yêu cầu, rồi **Build Detail Design**: template SRS, business flow, UI, thiết kế module/hàm, ERD, activity, class, coding guideline.
2. **Solution-Pair** review nội bộ, rồi chia task list.
3. QA viết **test case** theo mẫu và cập nhật **RTM**.
4. Code, **họp phê duyệt** (PO/PM, SA/TA, CS, Epic Leader, QA), rồi **code review** theo checklist.
5. Build request, chạy test case, ghi issue log và lesson learned.

Nguyên tắc: "chất lượng tốt nếu **50% lỗi tìm ra ở giai đoạn thiết kế**" (V-Model). Làm việc theo cặp: *Architect/Solution pair* và *Code review pair*.

Trạng thái ticket: New, Ready for Technical Architect, Ready for Development, To Do, In Progress, In Quality Assurance, Release.

Vai: PO/PM (yêu cầu nghiệp vụ), BA (use case, UAT), SA/TA (giải pháp, tech stack), Dev (code, tự test kỹ), QA/QC (theo ISTQB, chạy UAT), Epic Leader/TL/EM (điều hành nhóm).

## 2. Điều kiện vào và ra

- **DoR** (vào sprint): PM có business case và AC; TA/SA có tích hợp, môi trường, tech stack; Front-end có UI design, test case, API cần; QA có use case cần test, môi trường UAT; Dev có danh sách reviewer, thiết kế (FDD, DDD, AC), WBS, test case.
- **DoD**: đặt lại tiêu đề issue, TDD/ATDD, tài liệu và RTM cập nhật.
- Giảm họp: xác nhận trên mô tả hoặc tài liệu (Jira, Confluence); họp chỉ để hỏi đáp nhanh.

## 3. Thiết kế và quản lý thay đổi

- Ba tầng yêu cầu: Business, Stakeholder, Solution (Functional và Non-Functional).
- Sơ đồ phải biết: BPMN, use case, sequence, activity, ER, component, deployment, user story map. Có **RTM**.
- **Quản lý thay đổi (CR):** CR Form, đánh giá tác động, CCB duyệt, cập nhật CI, RTM và Test report.
- Khung "thuyết minh giải pháp": tổng quan, hiện trạng, tiêu chuẩn, hạ tầng, cân bằng tải, phương án kỹ thuật, yêu cầu phi chức năng (bảo mật 4 lớp), đào tạo, sao lưu.

## 4. Lập kế hoạch dự án

- Lập kế hoạch là **bắt buộc**. Người thực thi phải tham gia lập kế hoạch.
- Thứ tự: issues list, tasks và milestones, chiến lược, scope và deadline, **WBS**, ước lượng, master plan.
- WBS không thể hiện trình tự. **Không ước lượng khi chưa biết ai làm.** Nêu % dung sai và giả định. Không dùng làm thêm giờ để bù, thêm người vào dự án trễ càng trễ hơn.
- Rủi ro: liệt kê, đánh khả năng và mức tác hại (H, M, L), chọn biện pháp, có dự phòng.
- Thay đổi kế hoạch có kiểm soát, chỉ khi tác động làm trệch hướng đáng kể.

## 5. Kiểm thử

Bảy bước: đọc đặc tả, viết happy case (người làm feature viết, QA rà), code kèm unit test, Dev chạy happy case trên dev, ghi kết quả, QA test đầy đủ (luồng chính, biên, dữ liệu sai, tích hợp, hồi quy), Dev fix rồi QA retest, đóng lỗi, cập nhật RTM.

- Happy path chạy trước; lỗi phát hiện càng muộn càng đắt.
- Bốn kỹ thuật ISTQB: phân vùng tương đương, giá trị biên, bảng quyết định, chuyển trạng thái.
- TestLink: Keyword là mã task; một Test Plan là một sprint. Mantis: mỗi bug gắn một case Failed, cùng case thì **Reopen**, **Dev chỉ resolve, chỉ QA mới close**. Mức độ: Crash, Major, Mid, Minor.

## 6. Dùng AI trong dự án

- Vấn đề: tốc độ ảo, nợ kỹ thuật, nghẽn review (sinh nhanh 5 lần thì review chậm 10 lần), trôi lệch kiến trúc, AI bịa thư viện.
- **Viết Spec và Interface trước** (code chạy đúng lần đầu tăng khoảng 30% lên 90%). Ba mẹo chống ảo giác: few-shot, **lập kế hoạch và phản biện (pseudo-code) trước khi sinh code**, khoanh vùng ngữ cảnh tối đa khoảng 3 file.
- **Thứ tự tài liệu AI đọc khi nhận task:** quy trình SDLC, kỹ năng đọc SRS, định nghĩa dự án và công nghệ, kỹ năng code/test, thiết kế chi tiết, SRS dạng Markdown, trình bày để người và AI cùng hiểu.
- **Vòng cộng tác người và AI:** người viết SRS/UC, lập và duyệt WBS, phân tích giải pháp (cập nhật ADR/DAR), viết unit test, AI code (test pass 100%, điền RTM, ghi nhật ký thay đổi), người kiểm tra và thêm bug, lặp lại. **Xác nhận trong RTM, không qua chat.**
- Bốn mô hình: AI-Led (chỉ prototype), AI-Assisted, **AI-Augmented/Agentic** (mô hình vàng cho lõi sản phẩm), AI-Governed (trong CI/CD). Dev viết 80/20: AI viết 80% code thô, dev dành 20% thời gian đọc hiểu 100% ("Trust but Verify").
- Multi-agent giao tiếp bằng tài liệu: Product, Architect, Coder, Review.
- An toàn: `.aiignore` chặn `.env` và mật khẩu, key qua biến môi trường, **human-in-the-loop** trước khi apply hay execute.
- Quản trị prompt như code: Prompt Registry (ID, version, bộ test), "golden prompts". Đánh dấu: `AI_Generated: [Prompt_ID] | Contribution_Level: Lvl 2`; reviewer tích "Checked AI-Code Quality". Đo bằng AI-Human Synergy Score, không đo bằng số dòng code.

## 7. Git và CI/CD

- Nhánh `<type>/<mô-tả>` (feature, fix, hotfix, release, chore, refactor, docs, devops), nhánh feature không xóa. Commit `<type>(scope): <tóm tắt>`. Tag Semantic Versioning, **deploy production luôn theo tag**.
- MR: merge Develop vào nhánh mình trước khi tạo MR; **2 approval (Tech Lead và PM)**; CI `scan-code` pass; mô tả có Ticket, tóm tắt, Test evidence; không push thẳng `main`.
- Nhánh và môi trường: `feature/*` chỉ scan; `develop` là test, tự động; `staging`/`release/*` là staging, tự động; `main` hoặc tag là production, **phê duyệt thủ công**. Image deploy phải đúng image đã test trên Staging.
- Tiêu chí approve production: unit và integration test 100%, không lỗi Critical/High ở scan code và bảo mật, TL/PM đã review.
- Lưu ý: pipeline ở nguồn là của dự án đào tạo (Python/JS, AWS). Pipeline GitLab thật của repo gdt chưa xác nhận.

## 8. Đối chiếu với agent-base (kiểm bằng tìm từ khóa, chưa đọc từng dòng)

| Nội dung của công ty | agent-base |
|---|---|
| Cổng chất lượng, vòng task, DoR | Đã có: `protocols/task-loop.md` (8 cổng, DoR) |
| Spec trước code, phản biện đề bài | Đã có: `protocols/challenger.md`, `protocols/spec-writing.md` |
| TestLink, ISTQB, happy case | Đã có một phần: `protocols/test-cases.md`, vai `qa` |
| Git, MR, release theo tag | Đã có: `protocols/git-rules.md` |
| RTM | Chỉ có trong từ điển và mẫu SRS_FDD, **chưa có quy trình giữ RTM** (chưa làm) |
| Quản lý thay đổi (CR Form, CCB) | Đã bổ sung: `protocols/change-request.md` |
| Đánh dấu code do AI sinh, Prompt Registry, `.aiignore` | Đã bổ sung: `protocols/ai-provenance.md` |
| Plan và Critique bằng pseudo-code trước khi sinh code | Đã bổ sung: `protocols/plan-critique.md` (khác `challenger.md`, vốn phản biện đề bài) |
| Review theo cặp (Solution-Pair, Code review pair) | Đã bổ sung: `protocols/pair-review.md` |
| Trạng thái ticket theo công ty (Ready for TA, In QA...) | Đã bổ sung bảng ánh xạ: `protocols/ticket-status.md` (không thêm trạng thái mới cho card) |
| Release note | Đã bổ sung: `protocols/release-note.md` |
| Lesson learned sau mỗi lần làm | Đã bổ sung: `protocols/lesson-learned.md` |
| Rủi ro 6 bước, ước lượng, WBS | Chỉ có trong mẫu; `protocols/risk-gate.md` là rủi ro hoàn tác, không phải rủi ro dự án |
