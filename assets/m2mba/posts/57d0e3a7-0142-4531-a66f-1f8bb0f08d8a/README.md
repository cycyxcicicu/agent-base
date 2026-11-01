---
id: 297
title: "Requirements Life Cycle Management"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-08-07T00:16:45.000Z"
source_url: "https://m2mba.com/blog/articles/57d0e3a7-0142-4531-a66f-1f8bb0f08d8a"
---

# Requirements Life Cycle Management

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-08-07T00:16:45.000Z*

## 1.Giới thiệu chung

Vùng kiến thức "Requirements Life Cycle Management" mô tả các nhiệm vụ mà BA thực hiện để quản lý và duy trì các yêu cầu và  thiết kế từ khi bắt đầu đến khi kết thúc. Những nhiệm vụ này mô tả việc thiết lập các mối quan hệ giữa các yêu cầu và thiết kế, đánh giá phạm vi ảnh hưởng đối với yêu cầu và thiết kế khi có đề xuất thay đổi, phân tích, đánh giá các đề xuất thay đổi và đạt dược sự đồng thuận về các yêu cầu thay đổi đó

Mục đích của "Requirements Life Cycle Management" là để đảm bảo sự thống nhất giữa các yêu cầu và thiết kế của doanh nghiệp, các bên liên quan, và giải pháp được triển khai. Nó liên quan đến việc kiểm soát và quản lý các yêu cầu, nhằm đảm bảo chúng được thực hiện đúng trong giải pháp cuối cùng. Ngoài ra, việc quản lý vòng đời yêu cầu còn giúp lưu trữ và bảo quản thông tin phân tích kinh doanh, để có thể sử dụng trong tương lai

Vòng đời của yêu cầu có thể được mô tả như sau:

- **Bắt đầu** với việc thể hiện một nhu cầu kinh doanh (need) dưới dạng yêu cầu cụ thể (requirement).
- **Tiếp tục** thông qua quá trình phát triển và xây dựng một giải pháp để đáp ứng các yêu cầu đó.
- **Kết thúc** khi một giải pháp và các yêu cầu đại diện cho nó bị ngừng sử dụng
Quản lý yêu cầu không kết thúc khi một giải pháp được triển khai. Trong suốt vòng đời của một giải pháp, các yêu cầu tiếp tục mang lại giá trị khi chúng được quản lý một cách thích hợp.

Khái niệm về vòng đời của yêu cầu là tách biệt với phương pháp luận hoặc quy trình được sử dụng để quản lý công việc phân tích kinh doanh. Vòng đời của yêu cầu đề cập đến sự tồn tại của các giai đoạn hoặc trạng thái khác nhau mà các yêu cầu trải qua như một phần của bất kỳ thay đổi nào. Các yêu cầu có thể ở nhiều trạng thái cùng một lúc.

Tóm lại, quản lý yêu cầu là một công việc liên tục, không kết thúc khi một giải pháp được triển khai. Các yêu cầu tiếp tục có giá trị và cần được quản lý thích hợp trong suốt vòng đời của giải pháp.

Quá trình Quản lý Vòng Đời Yêu Cầu như được minh họa trong hình:

**Assess (Đánh giá):**

- Ở giai đoạn này, các yêu cầu tiềm năng được xem xét và đánh giá.
- Các yêu cầu này có thể được đề xuất bởi các bên liên quan, như khách hàng, người dùng, các nhóm phát triển, v.v.
- Việc đánh giá này giúp xác định tính phù hợp và tính khả thi của các yêu cầu.
**Approval/Consensus (Phê duyệt/Đạt được sự đồng thuận):**

- Sau khi đánh giá, các yêu cầu sẽ được đưa vào quy trình phê duyệt.
- Điều này bao gồm việc đạt được sự đồng thuận từ các bên liên quan về tính cấp thiết và tính khả thi của yêu cầu.
- Quá trình phê duyệt này đảm bảo rằng các yêu cầu được chấp nhận và có thể được triển khai.
**Manage (Quản lý):**

- Sau khi được phê duyệt, các yêu cầu sẽ được quản lý trong suốt vòng đời của giải pháp.
- Các hoạt động quản lý bao gồm theo dõi (Trace) để theo dõi tiến độ, duy trì (Maintain) để đảm bảo tính nhất quán, và ưu tiên hóa (Prioritize) để xác định thứ tự triển khai.
- Quá trình quản lý này đảm bảo rằng các yêu cầu tiếp tục mang lại giá trị trong suốt vòng đời của giải pháp.
Quá trình này được thể hiện bằng mũi tên "Bring Forward", cho thấy rằng các yêu cầu tiềm năng có thể được đưa lên để đánh giá, phê duyệt và quản lý liên tục. Điều này nhấn mạnh rằng quản lý yêu cầu không kết thúc khi một giải pháp được triển khai, mà là một quy trình liên tục.

Requirements Life Cycle Management bao gồm các task sau

**Theo dõi Yêu cầu (Trace Requirements): **Trong dự án, có rất nhiều thông tin liên quan như yêu cầu (requirement), thiết kế (design), thành phần giải pháp (solution component), và trường hợp kiểm thử (test case). Những thông tin này sẽ có mối quan hệ chặt chẽ với nhau. Nhà phân tích kinh doanh (BA) cần quản lý các mối liên hệ này để đảm bảo rằng việc quản lý yêu cầu được thực hiện một cách toàn diện, đồng thời giúp việc phân tích tác động khi có thay đổi yêu cầu trở nên dễ dàng hơn.

**Duy trì Yêu cầu (Maintain Requirements): **Đảm bảo rằng các yêu cầu và thiết kế luôn chính xác và được cập nhật trong suốt vòng đời và tạo điều kiện để tái sử dụng yêu cầu khi phù hợp.

**Ưu tiên Yêu cầu (Prioritize Requirements): **Trong dự án, có rất nhiều yêu cầu khác nhau. BA sẽ cần đánh giá độ ưu tiên để biết yêu cầu nào cần thực hiện trước. Việc đánh giá ưu tiên sẽ cần dựa vào đánh giá giá trị, tính cấp thiết của yêu cầu hoặc mức độ rủi ro liên quan đến các yêu cầu, thiết kế cụ thể. Việc này giúp đảm bảo công việc BA thực hiện trên các yêu cầu quan trọng nhất tại mỗi thời điểm

**Đánh Giá Thay Đổi Yêu cầu (Assess Requirements Changes): **Trong quá trình thực hiện dự án, BA sẽ tiếp nhận các yêu cầu thay đổi. BA sẽ có nhiệm vụ đánh giá các yêu cầu mới và thay đổi của các stakeholder, xác định xem các thay đổi này có cần thực hiện trong phạm vi của dự án hay không, và nếu thực hiện thì xác định phạm vi ảnh hưởng liên quan tới yêu cầu đó

**Phê Duyệt Yêu cầu (Approve Requirements): **Với các yêu cầu để thực hiện áp dụng cho các phần sau, BA cần phải phối hợp với các bên liên quan (những người có vai trò phê duyệt yêu cầu) để thống nhất và phê duyệt yêu cầu

## 2.BACCM
**Core Concept**
**Requirements Life Cycle Management,**

**business analysts....**

**Change**: the act of

transformation in response to a need.
BA cần thực hiện quản lý việc đánh giá các thay đổi được đề xuất đối với yêu cầu và thiết kế trong một dự án
**Need**: a problem or opportunity

to be addressed.

BA thực hiện truy vết, ưu tiên và duy trì các yêu cầu để đảm bảo nhu cầu được đáp ứng

 

**Solution**: a specific way of

satisfying one or more needs in a

context.
BA thực hiện truy vết các yêu cầu và thiết kế đến các thành phần của giải pháp để đảm bảo rằng giải pháp đáp ứng được nhu cầu
**Stakeholder**: a group or

individual with a relationship to

the change, the need, or the

solution.
BA cần làm việc chặt chẽ với các bên liên quan chính để duy trì sự hiểu biết, thống nhất và phê duyệt của các yêu cầu và thiết kế
**Value**: the worth, importance, or

usefulness of something to a

stakeholder within a context.
BA duy trì các yêu cầu để tái sử dụng nhằm mở rộng giá trị vượt ra ngoài dự án hiện tại
**Context**: the circumstances that

influence, are influenced by, and

provide understanding of the

change.
BA phân tích ngữ cảnh nhằm hỗ trợ các hoạt động truy vết và xác định mức độ ưu tiên
## **3.Input**

## **Competencies**

- Analytical Thinking and Problem Solving 
- Creative Thinking.