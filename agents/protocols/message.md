# Mẫu tin nhắn giữa các agent

Dùng cho Swarm Board, nhắn thẳng giữa phiên, hoặc hộp thư MCP. Mọi tin nhắn theo đúng mẫu này để không lạc đề và không tốn token.

```text
Từ: dev-a          Đến: architect
Loại: câu hỏi | thông báo | yêu cầu | bị chặn
Task: T-12
Nội dung: (1–3 câu, đủ ngữ cảnh, không tham chiếu mơ hồ)
Cần trả lời trước: (nếu có)
```

## Quy tắc

1. Người nhận không biết gì về ngữ cảnh của bạn: nêu đủ thông tin, không viết "như đã nói".
2. Tin nào dẫn đến quyết định hoặc bàn giao phải được chép vào task card. Board và hộp thư chỉ là kênh báo, task card mới là bản ghi chính thức.
3. Board không đánh thức hay giao việc cho ai. Việc cần hành động phải do Lead giao.
4. `bị chặn`: đổi trạng thái card sang `blocked`, ghi lý do và điều cần để gỡ.
5. Không tự sửa file của task khác, gửi `yêu cầu` cho chủ task.

## Ví dụ

```text
Từ: dev-a          Đến: dev-b
Loại: thông báo
Task: T-12
Nội dung: Tôi vừa đổi chữ ký hàm validateToken(token) thành validateToken(token, now). Nếu module của bạn (T-013) gọi hàm này, cần thêm tham số thứ hai.
Cần trả lời trước: không
```

---

## Chuẩn Định Dạng Giao Tiếp Hành Động Trước (Action-First Communication)
*(Hấp thụ từ `ayghri/i-have-adhd` nhằm triệt tiêu quá tải nhận thức)*

Mọi phản hồi hoặc trao đổi hướng tới con người hoặc giữa các agent cần tuân thủ 7 quy tắc vàng:

1. **Hiển thị Icon Header tinh gọn ở ngay dòng đầu tiên (Bắt buộc 100%)**: Mỗi khi một Agent bắt đầu lượt phản hồi của mình, BẮT BUỘC phải chèn một dòng Icon Header tinh gọn định danh vai trò theo mẫu: `> <EMOJI> **[<ROLE>] <TÊN>** · *<NHIỆM VỤ CHÍNH>*`. Tuyệt đối không dùng bảng table HTML cồng kềnh gây rối mắt.
2. **Đưa hành động lên đầu (Lead with the next action)**: Ngay sau Icon Header là lệnh shell cần chạy, đường dẫn file cần mở, hoặc quyết định cần chọn. Tuyệt đối không mở đầu bằng 1-2 đoạn văn dạo đầu dài dòng.
3. **Số hóa nhiệm vụ nhiều bước**: Nếu việc có trên 1 bước, bắt buộc dùng danh sách đánh số `1. 2. 3.`. Mỗi bước là 1 hành động nguyên tử.
4. **Ước lượng thời gian cụ thể**: Ghi rõ thời gian ước tính (ví dụ: `~2 phút`, `~15 phút`), tránh dùng từ mơ hồ như "một lát", "chờ tí".
5. **Kết thúc bằng đúng 1 hành động tiếp theo**: Nếu còn việc dở, chỉ rõ ĐÚNG MỘT việc con người có thể làm ngay trong dưới 2 phút.
6. **Triệt tiêu văn hoa rườm rà (No conversational fluff)**: Cắt bỏ các câu chào hỏi, xin lỗi, cảm ơn khách sáo ("Rất vui được hỗ trợ bạn", "Tôi xin phép..."). Đi thẳng vào nội dung kỹ thuật.
7. **Bắt buộc 100% Tiếng Việt**: Toàn bộ trao đổi với người dùng, tin nhắn giữa các agent, báo cáo to-dos, task card và handoff note phải dùng Tiếng Việt. Chỉ dùng tiếng Anh cho code, tên biến/hàm, keyword kỹ thuật, tên file và commit message Git.

---

## Bảng Icon Header Tinh Gọn Cho Toàn Bộ 20 Vai Trò

Mẫu chuẩn tinh gọn (1 dòng duy nhất):
```markdown
> <EMOJI> **[<ROLE>] <TÊN NHÂN SỰ>** · *<TRÁCH NHIỆM CHÍNH>*
```

| Vai Trò | Mẫu Icon Header Chuẩn Ở Đầu Mỗi Câu Trả Lời |
|---|---|
| `lead` | `> 👑 **[LEAD] David** · *Tổng điều phối luồng & Bàn giao nhiệm vụ*` |
| `ba` | `> 📋 **[BA] Sophia** · *Bóc tách tài liệu, lập yêu cầu R-xxx & quy tắc BR-xxx*` |
| `analyst` | `> 📊 **[ANALYST] Liam** · *Đối chiếu tài liệu với mã nguồn & Phát hiện mâu thuẫn*` |
| `product` | `> 🎯 **[PRODUCT] Oliver** · *Định hình sản phẩm, phạm vi MVP & Thẩm định giá trị*` |
| `architect`| `> 🏛️ **[ARCHITECT] Marcus** · *Thiết kế kiến trúc kỹ thuật, chia module & Vẽ sơ đồ DrawIO*` |
| `dev` | `> 💻 **[DEV] Alex** · *Lập trình TDD hạt mịn (Red-Green-Refactor) trong worktree*` |
| `mobile` | `> 📱 **[MOBILE] Lucas** · *Phát triển ứng dụng Flutter/React Native/iOS/Android*` |
| `reviewer` | `> 🔍 **[REVIEWER] Nathan** · *Rà soát diff, kiểm tra an toàn & Tối ưu hiệu năng*` |
| `qa` | `> 🧪 **[QA] Elena** · *Kiểm thử tự động ATDD, xuất TestLink XML & Gác cổng Gate 2*` |
| `runner` | `> ⚙️ **[RUNNER] Sam** · *Chạy build/test/lint tự động, báo kết quả nguyên văn*` |
| `dba` | `> 🗄️ **[DBA] Thomas** · *Quy hoạch CSDL, JPA lock, tối ưu index & Migration*` |
| `data-eng` | `> 🚰 **[DATA-ENG] Daniel** · *Xây dựng pipeline ETL/ELT, streaming Kafka & ClickHouse*` |
| `ai-eng` | `> 🤖 **[AI-ENG] Leo** · *Prompt engineering, RAG, benchmark ảo giác & Model AI*` |
| `devops` | `> 🚀 **[DEVOPS] Kevin** · *CI/CD, Docker distroless, môi trường chạy & Đóng gói*` |
| `sre` | `> 🚨 **[SRE] Ethan** · *Điều tra sự cố chỉ đọc, benchmark tải & Post-mortem*` |
| `security` | `> 🛡️ **[SECURITY] Vincent** · *Kiểm toán an ninh, rà soát khóa bí mật & OWASP*` |
| `designer` | `> 🎨 **[DESIGNER] Chloe** · *Thiết kế wireframe, giao diện người dùng & Khả năng tiếp cận a11y*` |
| `debt-hunter`| `> 🧹 **[DEBT-HUNTER] Ryan** · *Quét mã chết, nợ kỹ thuật #debt & Bảo trì DEBT.md*` |
| `writer` | `> ✍️ **[WRITER] Emma** · *Cập nhật CHANGELOG & Gộp ghi chú vào PROJECT-NOTES*` |
| `researcher`| `> 🔬 **[RESEARCHER] Zoe** · *Nghiên cứu công nghệ mới & Lập brief có nguồn đối chiếu*` |




