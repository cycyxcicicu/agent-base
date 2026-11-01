---
id: 337
title: "Vì sao BA nên hiểu MCP? — Câu chuyện từ một người từng dùng AI như... cái máy"
author: "Đậu Thị Ngọc Ánh"
created_at: "2026-07-09T02:36:29.000Z"
source_url: "https://m2mba.com/blog/articles/59f693ac-29c6-4c44-b677-d77ce9a9f645"
---

# Vì sao BA nên hiểu MCP? — Câu chuyện từ một người từng dùng AI như... cái máy

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2026-07-09T02:36:29.000Z*

## Vì sao BA nên hiểu MCP? — Câu chuyện từ một người từng dùng AI như... cái máy

Thời gian đầu dùng MCP, mình thú thật là dùng như một cái máy. Thấy hướng dẫn bảo cài MCP Server này vào Cursor thì cài, bảo connect Jira thì connect. Chạy được là mừng rồi, chẳng buồn hỏi bên trong nó hoạt động ra sao.

Dần dần mình nhận thấy nhu cầu các doanh nghiệp xây dựng AI Agent sẽ ngày càng nhiều. Nếu không hiểu bản chất, mình sẽ không thể phân tích requirement chính xác được. Từ đó mình bắt đầu ngồi bóc tách từng lớp một để hiểu cách AI Agent thực sự hoạt động.

Và một trong những kiến thức mình thấy thú vị nhất chính là **MCP (Model Context Protocol)**.

## Bắt đầu từ một câu hỏi rất đời thường

Hãy tưởng tượng khách hàng chat với AI CSKH của công ty bạn:

"Đơn hàng của tôi đang ở đâu?"

Nghe đơn giản đúng không? Nhưng nếu AI chỉ có mỗi LLM thì nó sẽ... bó tay. Vì thông tin đơn hàng nằm trong hệ thống OMS của doanh nghiệp, LLM làm sao biết được.

Tương tự, nhân viên chat: "Tạo giúp tôi đơn nghỉ phép thứ Sáu." AI không thể tự tạo nếu không kết nối được với hệ thống HR.

Hay chính BA chúng ta chat: "Tạo task Jira cho lỗi Login." AI phải biết gọi Jira API mới làm được.

Nói chung, AI muốn **làm được việc** chứ không chỉ **nói chuyện hay**, thì phải kết nối được với các hệ thống bên ngoài.

## Nỗi khổ trước khi MCP ra đời

Ngày trước, mỗi AI Agent muốn kết nối tới Jira, Confluence, CRM... thì đội phát triển phải tự viết từng đầu nối riêng. Đọc tài liệu API, xử lý xác thực, gọi API, parse dữ liệu... rồi lại lặp lại quy trình tương tự cho từng hệ thống khác.

Anthropic nhìn thấy vấn đề này và đưa ra một chuẩn chung là **MCP (Model Context Protocol)**.

Thay vì AI Agent phải hiểu API của từng hệ thống, mỗi hệ thống chỉ cần cung cấp một **MCP Server**. AI Agent chỉ cần giao tiếp theo chuẩn MCP là có thể sử dụng các Tool mà hệ thống cung cấp.

LLM là bộ não — người suy nghĩ.
MCP là đôi tay — giúp AI thao tác với thế giới bên ngoài.

## Bóc tách: Bên trong có 3 nhân vật

- **MCP Client (Host)** – Ứng dụng AI Agent.
- **MCP Server** – Hub trung gian kết nối tới hệ thống.
- **Hệ thống ngoài** – HR, CRM, Jira... cung cấp API.
Quá trình kết nối gồm ba bước:

- **Init**: Khởi tạo kết nối.
- **Tools/List**: Lấy danh sách Tool và Input Schema.
- **Tools/Call**: Gọi Tool với dữ liệu đúng Schema.
Đọc đến đây bạn sẽ thấy rất giống với đặc tả API mà BA vẫn làm hằng ngày. Chỉ khác là lần này người đọc tài liệu không phải Developer mà là LLM.

## Vậy ai quyết định gọi Tool nào?

Khi người dùng chat: "Tạo giúp tôi task Jira."

- AI Agent gửi nội dung chat, lịch sử hội thoại và danh sách Tool (name + description) sang LLM.
- LLM phân tích yêu cầu và chọn Tool phù hợp, ví dụ **create_jira_issue**.
- AI Agent gửi tiếp Input Schema của Tool đó sang LLM.
- LLM kiểm tra Schema, phát hiện thiếu **projectKey** nên yêu cầu AI Agent hỏi lại người dùng.
- Sau khi người dùng bổ sung thông tin, AI Agent gửi lại đầy đủ Context và Schema.
- LLM sinh request theo đúng Input Schema.
- AI Agent gọi **tools/call** tới MCP Server.
- MCP Server thực thi nghiệp vụ, gọi API hệ thống ngoài.
- Kết quả trả về LLM để diễn giải thành ngôn ngữ tự nhiên.
- AI Agent hiển thị kết quả cho người dùng.
Điều quan trọng là **Schema và Description của Tool càng rõ thì AI càng hoạt động chính xác.**

## Và đây là lúc BA bước vào câu chuyện

Khi doanh nghiệp bắt đầu xây dựng AI Agent, BA sẽ không chỉ phân tích requirement cho Web hay Mobile mà còn phải phân tích requirement cho AI Agent.

Một số câu hỏi BA cần trả lời:

- AI Agent cần kết nối với những hệ thống nào?
- Mỗi hệ thống cần cung cấp những Tool gì?
- Input Schema gồm những trường nào?
- Trường nào bắt buộc? Trường nào tùy chọn?
- AI được phép đọc hay cập nhật dữ liệu?
- Xác thực và phân quyền được thực hiện như thế nào?
## Bài học mình rút ra

BA không cần trở thành người code MCP Server. Nhưng BA nên hiểu cách MCP hoạt động để có thể phân tích requirement đúng ngay từ đầu.

Theo mình, sự khác biệt trong vài năm tới sẽ không nằm ở việc ai biết dùng AI, mà nằm ở việc ai hiểu cách AI vận hành để thiết kế giải pháp tốt hơn.