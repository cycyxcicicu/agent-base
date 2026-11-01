---
id: 325
title: "AI - Người Bạn Đồng Hành Của Business Analyst: Nâng Tầm Hiệu Quả Thay Vì Thay Thế"
author: "Đậu Thị Ngọc Ánh"
created_at: "2025-08-02T01:05:46.000Z"
source_url: "https://m2mba.com/blog/articles/ai-nng-tm-hiu-qu-cho-business-analyst"
---

# AI - Người Bạn Đồng Hành Của Business Analyst: Nâng Tầm Hiệu Quả Thay Vì Thay Thế

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2025-08-02T01:05:46.000Z*

Trong thời đại mà AI phát triển chóng mặt, nhiều Business Analyst (BA) lo lắng rằng vai trò của mình sẽ bị mờ nhạt và sớm bị thay thế. Thực tế, điều này chỉ đúng với những BA ngại học hỏi và không biết thích ứng. Ngược lại, AI đang mở ra cơ hội vàng giúp BA thoát khỏi những công việc lặp đi lặp lại, tập trung vào những giá trị cốt lõi mà chỉ con người mới có thể mang lại.

Bài viết này sẽ khám phá cách AI hỗ trợ công việc BA và những khía cạnh mà AI khó có thể thay thế trong tương lai gần.

**1. Những Lợi Ích Vượt Trội Của AI Trong Công Việc BA**

**1.1. Khơi Gợi Yêu Cầu - "Stakeholder Ảo" Không Bao Giờ Mệt Mỏi**

Lợi ích đầu tiên và rõ ràng nhất là khả năng hỗ trợ khơi gợi yêu cầu, đặc biệt khi BA bước vào một domain hoàn toàn mới.

**Trước đây**: BA phải google, đọc tổng hợp từ nhiều nguồn khác nhau, mất rất nhiều thời gian.

**Hiện tại với AI**: Chỉ cần đặt câu hỏi và nhận được câu trả lời tức thì. AI hoạt động như một "stakeholder ảo" - luôn sẵn sàng trả lời mà không bao giờ cảm thấy bị quấy rầy bởi những câu hỏi "ngớ ngẩn".

**Quy trình thực hiện hiệu quả:**

Khi tìm hiểu một bài toán kinh doanh mới, hãy yêu cầu AI phân tích **Business Model Canvas** của bài toán kinh doanh tương ứng và tập trung vào các thông tin sau:

**Key Activities (Hoạt động cốt lõi):**

- Những hoạt động chính của doanh nghiệp để vận hành kinh doanh sản phẩm dịch vụ đó là gì.
- Từ đó chúng ta sẽ hiểu được các quy trình công việc, stakeholder liên quan=>Sau đó sẽ là cơ sở để các bạn khơi gợi yêu cầu từ các stakeholder thật của doanh nghiệp
- Việc đó cũng giúp các bạn hình dung sản phẩm phần mềm cần hỗ trợ những hoạt động nào của doanh nghiệp?
Lưu ý quan trọng: Giải pháp cuối cùng phải dựa trên hoạt động thực tế của doanh nghiệp, không phải chỉ dựa vào thông tin từ AI.

**Key Partners (Đối tác chiến lược):**

- Để vận hành sản phẩm kinh doanh dịch vụ tương ứng, Doanh nghiệp phải làm việc với bên partner nào, ví dụ như Nhà cung cấp sản phẩm, Đối tác thanh toán, đối tác vận chuyển
- Từ các thông tin này cũng giúp các bạn hình dung được phần mềm sẽ cần xử lý ntn với các partner này: ví dụ như quản lý các thông tin gì của họ, có thể tích hợp với các đối tác này giúp giảm bớt công việc thủ công cho stakeholder không? Tất nhiên cuối cùng mọi yêu cầu đều phải làm rõ với stakeholder thật nhé
**Cost Structure & Revenue Stream:**

Revenue Stream (Nguồn thu):

- Các nguồn thu chính của mô hình kinh doanh, ví dụ như phí vận chuyển, phí chuyển tiền, doanh thu bán hàng từ các sản phẩm
- Công thức tính toán nguồn thu (phí vận chuyển, phí chuyển tiền, các kiểu thiết lập giá của SP, combo sản phẩm...)
- Từ đó giúp khơi gợi để tư duy cách cấu hình các công thức này trong phần mềm
Cost Structure (Cơ cấu chi phí):

- Tập trung vào chi phí đặc thù của sản phẩm/dịch vụ, không tập trung vào các chi phí chung như chi phí lương cho NV, chi phí điện nước…
- Ví dụ như các chi phí trả partner, đại lý, CTV
- Từ đó tìm hiểu công thức tính chi phí cần thiết lập trong hệ thống
**1.2. Hỗ Trợ Viết Tài Liệu - Từ Ý Tưởng Đến Thực Thi**

**User Stories và Use Cases:**

- AI có thể nhanh chóng tạo ra draft cho các user story phổ biến
- Tiết kiệm thời gian gõ text đáng kể
- Gợi ý các acceptance criteria cơ bản
**Business Rules và Validation:**

- Đề xuất các rule cần validate dựa trên context
- Gợi ý các case ngoại lệ có thể xảy ra
- Hỗ trợ viết test scenarios
Promt mẫu (bạn có thể tự đưa ra promt theo nhu cầu cấu trúc bạn muốn viết, quan trọng nhất bạn nêu đươc ngữ cảnh, các yêu cầu mà stakeholder cung cấp càng chi tiết càng tốt

Role: Senior Business Analyst

Context: Ứng dung cho thuê quần áo

Task: Viết user story cho tính năng Đăng quần áo cho thuê

Format yêu cầu:

- As a [user type]

- I want [functionality] 

- So that [business value]

 

Acceptance Criteria:

- Given [context]

- When [action]

- Then [expected result]

 

Lưu ý: Tài liệu AI tạo ra thường ở mức tổng quát. BA cần chi tiết hóa để dev và tester có thể thực hiện chính xác.

**1.3.Thiết kế màn hình**

Trong quá trình phân tích, đặc biệt là khi mô tả **giao diện người dùng (UI)**, BA thường gặp các thách thức:

- Không biết dùng công cụ thiết kế UI
- Không rõ layout thế nào là hợp lý với tính năng
- Mất thời gian phác thảo layout
- Khó mô tả rõ ràng cho dev nếu không có hình
**→ AI có thể hỗ trợ rất hiệu quả các công việc này.**

**Lợi ích khi nhờ AI hỗ trợ thiết kế màn hình**
Thiết kế màn hình từ mô tả tính năngAI tạo bản HTML/CSS demo để BA hình dung layoutTạo layout form, table, popupAI tạo markup kèm gợi ý UI elementVẽ sơ đồ UI flowAI sinh sơ đồ user flow bằng Mermaid hoặc PlantUMLTạo prompt để đưa vào công cụ designAI sinh prompt tiếng Anh để dùng với Miro, Figma AI...Mô tả các control trên UIAI liệt kê rõ các input field, validation, flow điều hướng
Cách sử dụng AI hiệu quả để thiết kế màn hình
**Bước****Hoạt động****Mô tả chi tiết / Prompt ví dụ**1Xác định mục tiêu và chức năng của màn hình“Thiết kế màn hình đăng ký nghỉ phép với các trường: loại nghỉ, ngày bắt đầu, ngày kết thúc, lý do nghỉ, nút gửi.”2Nhờ AI tạo giao diện HTML/CSS demo“Thiết kế trang HTML cho màn hình đăng ký nghỉ phép với các trường: loại nghỉ, ngày bắt đầu, ngày kết thúc, lý do nghỉ, nút gửi.”3Nhờ AI liệt kê và mô tả các control (trường thông tin)Thực hiện mô tả các trường trên MH với bảng gồm các thông tin: Tên control, Loại control,  Required, Mô tả control trong có có thể có thêm các ràng buộc và  thông báo lỗi nếu không thỏa mãn ràng buộc đó.”4Sinh prompt tiếng Anh để dùng với công cụ như Figma AI, Miro AI“Generate a design prompt for Figma AI: Design a leave request form for HR app. Fields: leave type, start date, end date, reason. Submit/Cancel buttons. Modern design.”5Nhờ AI gợi ý sơ đồ hóa User Flow (flow điều hướng giữa các màn hình)“Create a user flow diagram using Mermaid that shows the user journey from leave request form submission to approval confirmation.”6Kiểm tra lại layout và đề nghị AI cải tiến (responsive, UX, phân nhóm logic)“Refactor the layout to group personal information and request details separately. Make it mobile responsive.”
Một số output do AI tạo ra 

 

 

**1.4. Tích Hợp Đối Tác - Đọc Hiểu và Visualization**

AI có thể:

- Đọc hiểu tài liệu API integration của đối tác
- Vẽ sequence diagram dựa trên mô tả tích hợp khi bạn cung cấp ngữ cảnh của công ty mình + link tài liệu đặc tả tích hợp
- Từ đó đề xuất luồng tích hợp phù hợp với ngữ cảnh công ty
- Export ra các công cụ như sequencediagram.org hoặc Mermaid
Dưới đây là 1 output do AI tạo ra khi vẽ luồng tích hợp giữa ứng dụng cho thuê quần áo và hệ thống Momo

## 1.5. Hỗ trợ vẽ Flow

AI hiện nay có thể hỗ trợ **vẽ flow công việc** dưới dạng các **activity đơn tuyến** khá tốt, như:

- Vẽ luồng thao tác theo từng bước của người dùng (user flow)
- Biểu diễn quy trình xử lý logic trong hệ thống (process flow)
Tuy nhiên, **AI vẫn còn hạn chế** khi vẽ các loại flow nâng cao như:

- **BPMN (Business Process Model and Notation)** – biểu diễn quy trình với nhiều tác nhân/stakeholder
- **Business flow đa vai trò** – thể hiện rõ các lane cho từng đối tượng (User, System, Partner…)
Vì vậy, BA vẫn cần tự tay hiệu chỉnh hoặc sử dụng công cụ chuyên dụng (như Draw.io, Bizagi, Lucidchart...) để vẽ **các flow phức tạp liên quan đến nhiều bên và luồng phối hợp**.

Ví dụ user flow đăng ký khóa học trên trang Trung tâm đao tạo

## Những kỹ năng mà AI khó có thể thay thế ở BA

### 1. Kỹ năng giao tiếp & thấu hiểu con người (Emotional Intelligence)

- BA giỏi không chỉ nghe mà còn “đọc vị” được stakeholder qua thái độ, cảm xúc.
- Họ biết điều chỉnh cách nói chuyện, tạo niềm tin, xử lý mâu thuẫn và kết nối các bên.
- Trong các buổi workshop, BA cần dẫn dắt, đặt câu hỏi đúng trọng tâm và giúp nhóm đi đến đồng thuận.
=>AI không thể cảm nhận cảm xúc hoặc xử lý mối quan hệ phức tạp như con người.
### 2. Tư duy phản biện & đánh giá kinh doanh (Critical Thinking)

- BA cần hiểu rõ ngữ cảnh doanh nghiệp để đề xuất giải pháp thực tế.
- Không chỉ phân tích kỹ thuật, mà còn cân nhắc chiến lược kinh doanh và tính khả thi triển khai.
- Ưu tiên yêu cầu nào? Có phù hợp với mục tiêu dài hạn? Đó là vai trò của BA.
=> AI chỉ phân tích dữ liệu – còn việc đưa ra quyết định sáng suốt vẫn cần con người.
### 3. Giải quyết vấn đề sáng tạo (Creative Problem Solving)

- AI giỏi tổng hợp dữ liệu quá khứ, nhưng khó hiểu hết môi trường thực tế hoặc tự đưa ra ý tưởng đột phá.
- BA có thể “đổi góc nhìn”, đảo quy trình và tìm ra hướng đi mới mà AI không ngờ tới.
- BA biết cân bằng giữa các bên liên quan: user, dev, kinh doanh, vận hành…
=> AI không thể “đứng vào nhiều vai” như BA để tìm giải pháp hài hòa.
## Làm thế nào để dùng AI hiệu quả?

### 1. Tin nhưng cần kiểm chứng (Trust but verify)

- Kiểm tra thông tin AI trả về với stakeholder hoặc tài liệu gốc.
- Không dựa 100% vào AI cho các quyết định quan trọng.
### 2. Viết prompt rõ ràng, đúng cấu trúc

- Context: Mô tả ngữ cảnh
- Role: Vai trò AI cần đóng
- Task: Nhiệm vụ cụ thể
- Format: Output mong muốn
- Constraints: Ràng buộc (nếu có)
### 3. Tinh chỉnh nhiều vòng (Iterative refinement)

- Bắt đầu bằng câu hỏi rộng, sau đó hỏi sâu dần.
- BA càng biết hỏi tốt, kết quả AI trả về càng hữu ích.
### Lộ Trình Phát Triển Của BA Trong Thời Đại AI

- Giai đoạn 1: Nâng Cấp Kỹ Năng Nền Tảng (Upskill Ngay Lập Tức)** Kỹ năng kỹ thuật cần trang bị****Mục tiêu học****Gợi ý học nhanh****AI Tools (ChatGPT, Claude, Copilot)**Nắm vững cách đặt prompt để tận dụng AI trong việc viết tài liệu, brainstorming ý tưởng, và hỗ trợ coding.Thực hành qua việc sử dụng các công cụ này hàng ngày. Luyện tập đặt câu hỏi rõ ràng và cụ thể.**Data Analysis**Hiểu và phân tích dữ liệu để rút ra insight, giúp hỗ trợ ra quyết định kinh doanh.Học cách sử dụng Excel nâng cao, SQL và Power BI/Looker Studio.**No-code / Low-code Platforms**Tạo ra prototype và workflow một cách nhanh chóng mà không cần kiến thức lập trình sâu.
Khám phá Bubble, Retool, Glide và Zapier. Tham gia khóa học trực tuyến.

Những cái này là cái mà chính admin cũng cần trang bị
**API & Integration cơ bản**Hiểu cách tích hợp các dịch vụ và xác định thông tin cần lấy từ các đối tác.Đọc tài liệu Swagger và thực hành gọi API bằng Postman.
** Kỹ năng mềm cần phát triển:**
**Kỹ năng****Ý nghĩa****Giao tiếp & thuyết trình**Khả năng truyền đạt yêu cầu rõ ràng, thuyết phục stakeholders.**Facilitation & Coaching**Kỹ năng dẫn dắt workshop, hỗ trợ và phát triển đội ngũ junior.**Tư duy hệ thống và chiến lược**Khả năng nhìn nhận tổng thể vấn đề, đánh giá giải pháp dài hạn.
- **Giai đoạn 2: Chuyển Vai Trò Sang Giá Trị Cao Hơn (High-Value Activities)****Mục tiêu****Ví dụ cụ thể****Phân tích chiến lược**Hỗ trợ phát triển mô hình kinh doanh mới và thúc đẩy chuyển đổi số.**Tư duy thiết kế giải pháp toàn diện**Cân bằng giữa UX, Dev effort và các mục tiêu kinh doanh.**Giải quyết bài toán phức tạp**Tham gia vào dự án yêu cầu sự hợp tác từ nhiều stakeholder.**Xây dựng năng lực chuyên môn sâu**Trở thành chuyên gia trong lĩnh vực như Fintech, HRTech, Logistics.
#### **Giai đoạn 3: Trở Thành BA Biết Tận Dụng AI (AI-Savvy BA)**
**Năng lực cần có****Vai trò****Hiểu rõ AI làm được gì & không làm được gì**Tránh ảo tưởng và phụ thuộc vào AI, biết khi nào nên sử dụng AI.**Biết cách prompt hiệu quả**Tạo ra yêu cầu rõ ràng để AI cung cấp kết quả hữu ích.**Tận dụng AI trong công việc hàng ngày**Sử dụng AI để viết mô tả màn hình, xây dựng use case.**Giải thích, định hướng lại output từ AI**Chuyển đổi đầu ra chung chung của AI thành nội dung chuẩn chỉnh cho dev/test.**Truyền cảm hứng cho team**Hướng dẫn các thành viên trong team cách sử dụng AI hiệu quả.
### ✅ Tổng Kết 

Trong thời đại AI, BA sẽ cần kết hợp AI, con người, công nghệ và chiến lược để tạo ra giải pháp tối ưu. Sự phát triển liên tục về kỹ năng và tư duy sẽ là chìa khóa để BA thành công trong môi trường làm việc hiện đại.