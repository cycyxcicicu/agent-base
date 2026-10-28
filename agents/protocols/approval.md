> Task: T-13 · Epic: E2 · Vai: architect

# Giao thức duyệt bằng file bởi con người (File-Based Approval Protocol)

Quy tắc nền tảng: **AI không bao giờ tự quyết định duyệt; con người quyết định.** Người dùng nói đồng ý rõ ràng trong chat thì có hiệu lực: agent ghi dấu vào file thay họ, kèm trích nguyên văn câu họ nói (mục 2b). Trạng thái Draft, ô để trống, hoặc câu chung chung không nêu rõ việc gì ("ok", "làm đi" khi chưa có đề nghị cụ thể) thì CHƯA DUYỆT: hỏi lại một câu. Mọi đánh giá, nhận xét (verdict) của các tác tử AI chỉ mang tính chất tư vấn kỹ thuật.

---

## 1. Vòng đời trạng thái tài liệu

Tài liệu đặc tả (SRS/FDD), thiết kế (Architecture/ADR), kế hoạch (Plan/Task Card) và nghiệm thu phải tuân thủ nghiêm ngặt máy trạng thái:

```
[Draft / Soạn thảo]  --->  [Đã soát / Reviewed]  --->  [Approved / Đã duyệt]
       ^                                                      |
       |--------------- (Khi có sửa đổi nội dung) ------------|
```

- **Draft (Soạn thảo)**: Trạng thái khởi tạo mặc định của mọi tài liệu do AI hoặc con người soạn thảo.
- **Đã soát (Reviewed)**: Trạng thái sau khi chuyên viên phản biện / Reviewer / QA rà soát diff, kiểm tra checklist và ghi nhận nhận xét tư vấn (verdict). AI chỉ được phép đưa tài liệu tới trạng thái này.
- **Approved (Đã duyệt)**: chỉ đổi sang trạng thái này khi **con người đã đồng ý** (sửa file hoặc nói rõ trong chat, mục 2b). Cấm tác tử AI tự đóng dấu khi người dùng chưa nói đồng ý.

---

## 2. Định dạng dấu duyệt chuẩn

Dấu duyệt của con người phải được ghi trực tiếp vào phần frontmatter hoặc bảng/mục phê duyệt của tệp theo mẫu:

```markdown
- [x] **Người dùng duyệt <phạm vi/hạng mục>**: <Tên Người Duyệt> · <YYYY-MM-DD> [digest: <8 ký tự hash đầu hoặc tóm tắt>]
```

Ví dụ hợp lệ (dữ liệu mẫu):
```markdown
- [x] **Người dùng duyệt phạm vi**: Alex Nguyen · 2026-10-28 [digest: e3b0c442]
- [x] **Người dùng duyệt thiết kế**: Sarah Tran · 2026-10-28 [digest: 4a8b1c9d]
```

### 2b. Người dùng đồng ý trong chat: agent ghi hộ

Điều kiện: câu của người dùng (1) nêu rõ hạng mục, hoặc (2) trả lời thẳng một đề nghị cụ thể mà agent vừa nêu (ví dụ "Duyệt cả 40 nút", "đồng ý phương án A"). Agent ghi dấu kèm trích nguyên văn, ngày, và ghi rõ là ghi hộ:

```markdown
- [x] **Người dùng duyệt <hạng mục>**: <Tên> (xác nhận qua chat, AI ghi hộ) · <YYYY-MM-DD> · "<câu nguyên văn của người dùng>"
```

Định dạng này vẫn khớp `claim_check` (tên, dấu `·`, ngày). Câu mập mờ thì hỏi lại một câu, không đoán.

---

## 3. Cơ chế vô hiệu hóa dấu duyệt khi nội dung thay đổi (Stale Invalidation)

- Dấu duyệt gắn liền với phiên bản nội dung (digest hoặc git revision).
- Khi có bất kỳ thay đổi nào đối với tài liệu sau thời điểm duyệt (thay đổi yêu cầu, thêm bớt subtask, đổi phạm vi `scope_edit`, thay đổi mã nguồn tham chiếu):
  1. Dấu duyệt cũ **tự động mất hiệu lực (STALE)**.
  2. Trạng thái tài liệu lập tức quay về `Draft` hoặc `Đã soát`.
  3. Tác tử AI phải dừng thực thi các hành động phụ thuộc và yêu cầu con người tái duyệt (re-approval).

---

## 4. Danh mục các ô phê duyệt cần con người đồng ý

Các hạng mục kiểm soát then chốt mà AI không được tự quyết; chỉ ký khi người dùng đã đồng ý (sửa file hoặc nói rõ trong chat, mục 2b):

1. **Duyệt phạm vi task card (`scope_edit`)**: Dòng `Người dùng duyệt phạm vi bằng file` trong task card hoặc bảng duyệt hàng loạt.
2. **Duyệt tài liệu thiết kế, đặc tả và kiến trúc**: Chấp thuận đặc tả SRS/FDD, sơ đồ module, tài liệu ADR.
3. **Duyệt phiếu rủi ro (Risk Gate)**: Chuyển trạng thái phiếu `docs/risk/RK-*.md` từ `PENDING` sang `APPROVED`.
4. **Nghiệm thu đóng task (Sign-off & Done)**: Chuyển trạng thái card từ `review` sang `done`. Chỉ con người quyết định hoàn thành và đóng task.

---

## 5. Giới hạn trung thực & Biện pháp kiểm soát bổ trợ

- **Bản chất kỹ thuật**: Trong môi trường làm việc cục bộ, tác tử AI có quyền ghi file nên dấu duyệt dạng văn bản trong file Markdown chưa thể chống giả mạo tuyệt đối về mặt mật mã học (cryptographic non-repudiation). Mục đích chính của giao thức là định hình ranh giới trách nhiệm, ngăn chặn việc AI tự suy diễn hoặc tự bỏ qua cổng kiểm soát.
- **Biện pháp đối soát**: Việc chứng minh danh tính người duyệt và kiểm soát gian lận được thực hiện hậu kỳ thông qua:
  - Kiểm tra `git blame` / `git log` để đối chiếu tác giả commit thật của con người.
  - Cổng kiểm tra tự động trước khi nhận việc (`claim_task` ở T-23) và cổng tích hợp (`merge-gate`).
