> Task: T-18 · Epic: E2 · Vai: ba

# Từ điển thuật ngữ miền dự án (Domain Glossary)

Tài liệu này chuẩn hóa định nghĩa các khái niệm cốt lõi trong quy trình phát triển phần mềm có AI hỗ trợ (AI in SDLC) tại `agent-base`. Mỗi thuật ngữ được quy định rõ: **Nghĩa là gì** và **KHÔNG PHẢI là gì** để tránh nhầm lẫn trong giao tiếp và thực thi.

---

## 1. Task (Nhiệm vụ)
- **Nghĩa là**: Một đơn vị công việc hoàn chỉnh có quy mô từ vài giờ đến 1 ngày công (<= 6.4 giờ), được ghi nhận bằng một tệp task card chính thức `tasks/<epic>/T-<ticket>.md` với đầy đủ mục tiêu, phạm vi (`scope_edit`), tiêu chí xong và kế hoạch commit.
- **KHÔNG PHẢI**: Không phải là một câu lệnh chat đơn lẻ, không phải là một subtask ngắn 2 phút, và không phải là một commit git riêng lẻ.

## 2. Ticket (Mã định danh công việc)
- **Nghĩa là**: Số nguyên dương duy nhất gắn liền với task card và nhánh git (ví dụ: ticket 12 ↔ `T-12.md` ↔ nhánh `docs/12-...`).
- **KHÔNG PHẢI**: Không phải là mã định danh subtask (như 12.1), không phải là issue ID trên Jira/GitHub nếu chưa được ánh xạ chính thức.

## 3. Subtask (Nhiệm vụ con hạt mịn)
- **Nghĩa là**: Một bước phân rã nhỏ của task card, được thực hiện bởi một subagent trong một phiên ngắn (2–5 phút, tối đa 8–10 tool calls), tập trung vào đúng một mục đích duy nhất và có file bàn giao riêng (`docs/notes/inbox/<Task>/<Task>.<m>-<vai>.md`).
- **KHÔNG PHẢI**: Không phải là một task độc lập có nhánh riêng, không có quyền tự đổi trạng thái task cha sang `done`.

## 4. Gate (Cổng kiểm soát)
- **Nghĩa là**: Điểm chốt chặn bắt buộc trước khi chuyển pha (ví dụ: Cổng phê duyệt kế hoạch, Cổng rủi ro RK, Merge Gate, Gate G0–G7). Cổng chỉ mở khi có bằng chứng khách quan hoặc dấu duyệt bằng file của con người.
- **KHÔNG PHẢI**: Không phải là lời dặn chung chung trong prompt, không phải câu trả lời "ok" trong hội thoại chat, và không phải là đánh giá tự duyệt của chính agent đang làm.

## 5. RTM (Requirements Traceability Matrix - Ma trận truy vết yêu cầu)
- **Nghĩa là**: Bảng ánh xạ hai chiều liên kết chặt chẽ: `Yêu cầu (R-xxx) ↔ Task (T-xxx) ↔ File sở hữu ↔ Test Case ↔ Bằng chứng kiểm thử`, được sinh tự động từ frontmatter và manifest.
- **KHÔNG PHẢI**: Không phải là một tệp Excel ghi tay song song thiếu đồng bộ, không phải là lời tuyên bố tự nhận "đã đáp ứng yêu cầu".

## 6. Lease (Quyền sở hữu tác vụ tạm thời)
- **Nghĩa là**: Bản ghi cam kết phạm vi và thời gian khi tác tử nhận việc (`claim_task`), ghi nhận tác tử chịu trách nhiệm, commit mốc và danh sách tệp được phép sửa đổi trong phiên.
- **KHÔNG PHẢI**: Không phải là quyền sửa đổi vĩnh viễn, không cho phép tác tử tự ý sửa các tệp ngoài phạm vi đã đăng ký.

## 7. Proof (Bằng chứng kiểm chứng thực thi)
- **Nghĩa là**: Dữ liệu đầu ra thật thu thập từ môi trường runtime (lệnh đã chạy, exit code, log output, hash commit, ảnh chụp màn hình hoặc trace CDP) chứng minh tính năng hoạt động hoặc lỗi đã bị loại bỏ.
- **KHÔNG PHẢI**: Không phải là lời khẳng định tự tin của AI ("tôi đã sửa xong"), không phải là suy đoán tĩnh từ mã nguồn khi chưa chạy lệnh.

## 8. Eval (Đánh giá năng lực kỹ năng)
- **Nghĩa là**: Quy trình kiểm thử có đối chứng nhằm đánh giá hiệu quả của một kỹ năng (skill) hoặc prompt theo rubric đa tiêu chí, thực hiện trong môi trường trung tính và chấm mù bởi mô hình độc lập.
- **KHÔNG PHẢI**: Không phải là unit test của mã nguồn ứng dụng, không phải là thẩm quyền thay thế nghiệm thu của con người.

## 9. Knowledge Graph (Đồ thị tri thức)
- **Nghĩa là**: Cấu trúc dữ liệu có quan hệ kiểu (typed edges) biểu diễn mối liên kết giữa các thực thể tri thức (tài liệu, quy trình, vai trò, quy tắc, mã nguồn), phục vụ truy xuất tối thiểu đúng ngữ cảnh.
- **KHÔNG PHẢI**: Không phải là cơ sở dữ liệu vector RAG nhồi nhét toàn văn, không phải là sơ đồ vẽ tay tùy tiện.

## 10. Knowledge Manifest (Bản kê khai tri thức)
- **Nghĩa là**: Tệp cấu hình tập trung duy nhất (`knowledge.manifest.json`) khai báo danh mục các node tài liệu, quyền truy cập của từng vai trò và quy tắc phụ thuộc. Mọi đồ thị và ngữ cảnh đều sinh từ manifest này.
- **KHÔNG PHẢI**: Không phải là manifest phân phối tệp của khung (`agents/manifest.txt`).

## 11. Feature Map (Bản đồ tính năng bề mặt)
- **Nghĩa là**: Tài liệu mô tả cách người dùng hoặc harness tiếp cận, vận hành và kiểm chứng từng tính năng của hệ thống (gồm Sub-features, How to get to it, Driving it with harness, Gotchas).
- **KHÔNG PHẢI**: Không phải là tài liệu kiến trúc code bên trong, không phải là danh sách API thô.

## 12. Reviewer Verdict (Ý kiến thẩm định chuyên môn)
- **Nghĩa là**: Nhận xét tư vấn kỹ thuật độc lập của tác tử Reviewer (APPROVED, CHANGES_REQUESTED) dựa trên checklist khách quan và bằng chứng diff.
- **KHÔNG PHẢI**: Tuyệt đối **KHÔNG PHẢI là dấu duyệt của con người**. Verdict của Reviewer không cấp quyền đóng task sang `done` và không thay thế chữ ký của người dùng.
