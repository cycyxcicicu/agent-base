---
id: 336
title: "Tại sao cùng 1 model AI nhưng mỗi agent lại cho output khác nhau?"
author: "Đậu Thị Ngọc Ánh"
created_at: "2026-04-01T04:22:34.000Z"
source_url: "https://m2mba.com/blog/articles/8ebaf3fd-c35a-4be6-8405-35e2ed55350a"
---

# Tại sao cùng 1 model AI nhưng mỗi agent lại cho output khác nhau?

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2026-04-01T04:22:34.000Z*

## Hiểu đúng bản chất trước

Nhiều người nghĩ: **AI agent = model LLM**. Nhưng thực ra model chỉ là một mảnh nhỏ trong cả hệ thống gồm có giao diện người dùng (FE), BE của các AI agent, LLM.

Khi bạn nhắn tin với một AI agent, có rất nhiều thứ xảy ra **trước khi** câu hỏi của bạn chạm đến LLM. Và chính những thứ đó tạo ra sự khác biệt. Mỗi lần để gen ra câu trả lời cho user, BE sẽ cần gọi API tới LLM tương ứng, LLM xử lý mỗi API độc lập với nhau, ko phụ thuộc vào API trước bên BE đã gọi, LLM chỉ phụ thuộc vào payload mà BE gửi sang

Điểm mấu chốt chỉ có một:

Ai kiểm soát payload → người đó kiểm soát output.

## Luồng thực tế từng bước

Khi bạn gõ một tin nhắn và bấm gửi, đây là những gì thực sự xảy ra:

### Bước 1 — Bạn gửi tin nhắn lên FE

Bạn nhập prompt, bấm gửi. Giao diện (FE) nhận tin nhắn và gọi lên BE kèm session_id để BE biết đây là cuộc hội thoại nào.

Đây là lớp duy nhất bạn nhìn thấy.

### Bước 2 — BE lắp ráp payload (quan trọng nhất)

Đây là bước tạo ra toàn bộ sự khác biệt giữa các agent — và người dùng không bao giờ nhìn thấy nó.

BE không chuyển thẳng câu hỏi của bạn lên LLM. BE phải **xây dựng một payload hoàn chỉnh** trước, bao gồm:

**a) Lấy system prompt**

System prompt là đoạn text được viết sẵn, định nghĩa agent là ai, làm được gì, nói chuyện như thế nào. Nó nằm trong trường system của payload.

 

Agent A — system prompt: "Bạn là trợ lý phân tích dữ liệu. Luôn trả lời ngắn gọn, có số liệu. Không đưa ý kiến cá nhân." Agent B — system prompt: "Bạn là người bạn đồng hành sáng tạo. Trả lời thân thiện, dùng ví dụ thực tế, khuyến khích người dùng suy nghĩ thêm."

Cùng câu hỏi "Tôi nên học gì?" — hai system prompt trên cho ra hai câu trả lời hoàn toàn khác nhau về tone, độ dài và hướng tiếp cận.

**b) Lấy lịch sử hội thoại (history)**

LLM không có bộ nhớ thật sự. Mỗi lần gọi, BE phải đưa lại lịch sử hội thoại vào messages[] để LLM "nhớ" context. Nhưng mỗi agent quản lý history theo cách khác nhau:

Agent A nhớ đầy đủ nhưng tốn token. Agent B có thể quên context cũ. Agent C tiết kiệm nhưng summary có thể mất thông tin.

**c) Query RAG và inject tài liệu (nếu có)**

RAG (Retrieval-Augmented Generation) cho phép agent tìm kiếm tài liệu liên quan rồi nhét vào messages[] trước câu hỏi của bạn — như một nhân viên được phép mở tài liệu công ty trong lúc trả lời.

 

**d) Xác định tools available (tool này chính là các MCP server mà từng AI agent cấu hình kết nối tới hoặc những tool có sẵn của AI agent)**

BE khai báo danh sách tools LLM được phép dùng trong trường tools[]. LLM chỉ biết đến tool nào được liệt kê ở đây — không hơn.

### Bước 3 — BE gọi LLM với payload đã chuẩn bị

Sau khi lắp ráp xong, BE gọi API của LLM. Payload trông như thế này:

 

### Bước 4 — LLM xử lý và quyết định

LLM đọc toàn bộ payload rồi quyết định một trong hai:

- **Trường hợp 1 — Trả lời thẳng: **LLM đủ thông tin → trả về text trực tiếp → BE nhận → chuyển về FE.
- **Trường hợp 2 — Yêu cầu dùng tool (ví dụ web search): **Đây là điểm nhiều người hiểu sai. Web search không phải LLM tự chạy — mà là một quy trình 3 bước:
 

Tóm gọn:
 Ai làm?Quyết định có cần search khôngLLMQuyết định search query là gìLLMThực sự gọi Search APIBEDùng kết quả để sinh câu trả lờiLLM
LLM không có khả năng tự gọi HTTP request ra ngoài. Nó chỉ "ra lệnh" cho BE thông qua định dạng tool_use. BE mới là người thực sự chạm vào internet.

### Bước 5 — BE post-process output

Output từ LLM chỉ là "nháp thô". BE có thể xử lý thêm trước khi trả về FE:

 

Đây là lý do cùng Claude nhưng trên claude.ai, qua API thô, và nhúng trong app bên thứ ba có thể trông **rất khác nhau** — dù LLM trả về cùng một nội dung.

### Bước 6 — FE hiển thị cho bạn

Kết quả cuối cùng hiện ra trên màn hình — có thể là streaming (chữ hiện dần) hoặc full response tùy FE implement.

Bạn chỉ thấy bước này. Nhưng đằng sau là 5 bước đã xảy ra.

## Minh họa tổng hợp

Cùng câu hỏi "Tóm tắt dự án cho tôi" — 3 agent khác nhau chuẩn bị 3 payload khác nhau:

## Tổng kết
Yếu tốNằm ở đâu trong payloadMức độ ảnh hưởngSystem promptsystem⭐⭐⭐⭐⭐History strategymessages[]⭐⭐⭐⭐⭐RAG / inject tài liệumessages[]⭐⭐⭐⭐Temperature & configtemperature, top_p...⭐⭐⭐⭐Tools availabletools[]⭐⭐⭐Post-processingNgoài payload — BE xử lý sau⭐⭐
### Hàm ý thực tế

- **Output tệ không phải do model kém** — hãy xem lại payload BE đang gửi lên
- **Muốn cải thiện output** → tối ưu system và cách inject context là đòn bẩy mạnh nhất
- **Web search không phải LLM tự làm** — LLM ra lệnh, BE thực thi, LLM dùng kết quả
- **Benchmark agent phải cùng payload** — so sánh payload khác nhau là so sánh táo với cam
- **Cùng model, payload khác = sản phẩm khác** — đây là lý do các AI agent tạo ra trải nghiệm rất khác nhau dù build trên cùng nền tảng
Tài liệu phù hợp cho BA, PM, và những ai muốn hiểu kiến trúc AI agent để làm việc hiệu quả hơn.