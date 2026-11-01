---
id: 90
title: "Context Diagram"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-03T02:59:58.000Z"
source_url: "https://m2mba.com/blog/articles/context-diagram-la-gi-va-tai-sao-can-xay-dung"
---

# Context Diagram

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-03T02:59:58.000Z*

## **1.Context Diagram là gì?**

     Không có một hệ thống nào đứng riêng lẻ mà luôn cần tương tác với các thế giới bên ngoài để mang lại giá trị và **bức tranh tổng thể với hệ thống là trung tâm**, tương tác với các tác nhân, yếu tố bên ngoài được gọi là môi trường hay **ngữ cảnh** (context) của hệ thống đó. Bức tranh hay biểu đồ đó được gọi tên là **Context Diagram** hay **System Context Diagram (SCD).**
     Trong Context Diagram, hệ thống được biểu diễn như một hộp đen (ta chưa có hoặc chưa quan tâm đến các thành phần chi tiết bên trong) và hệ thống này sẽ có những tương tác với các hệ thống khác hoặc con người thông qua các **interface**.

**      Context Diagram:** mô tả bối cảnh của hệ thống, bao gồm các thực thể bên ngoài tương tác với hệ thống. Các thực thể bên ngoài này có thể là các hệ thống khác, các service, hoặc các đơn vị kinh doanh (yếu tố con người), hoặc các database, … Mô hình này cũng giúp xác định các dòng dữ liệu giữa các thực thể bên ngoài và hệ thống chính, và mô tả hướng đi của mỗi dòng dữ liệu. Giới hạn của mô hình này là chỉ mô tả thực thể bên ngoài tương tác trực tiếp với hệ thống dưới dạng khám phá.

## **2.Tại sao BA cần xây dựng Context Diagram?**

Việc xây dựng Context Diagram cho hệ thống có những ưu điểm sau:

- Giúp cho toàn đội dự án có cái nhìn **tổng quan về môi trường mà hệ thống sẽ vận hành**, từ đó xác định được phạm vi hệ thống. Vì vậy context diagram được phân loại là một mô hình phạm vi (**scope model**)
- Nhìn thấy **những tương tác** giữa hệ thống với các hệ thống khác và các vai trò sử dụng hệ thống, từ đó tránh các rủi ro, hoặc thiếu sót khi thiết kế hệ thống.
- Không cần kiến thức về kỹ thuật để hiểu nên có thể sử dụng để làm việc với các stakeholders không biết về kỹ thuật.
- Dễ tạo và dễ sử dụng
- Context Diagram sẽ được sử dụng để phân tích sâu hơn trong quá trình thiết kế các tính năng của hệ thống
## **3.Xây dựng Context Diagram**

Context Diagram thường được tạo sớm, thường là sau khi BA đã thực hiện các bước khai thác thông tin và làm rõ yêu cầu với các stakeholders. Tuy nhiên, trong nhiều trường hợp, Context Diagram cũng được sử dụng trong các [requirements workshop](https://vietba.org/facilitated-workshop-la-gi/) bằng cách cùng các stakeholders xác định các thành phần nằm trong context của hệ thống.
Một Context Diagram được xây dựng bởi 2 loại ký hiệu:

- Mũi tên có hướng: biểu diễn đường đi của dữ liệu (chúng ta hay gọi là input, output data, input data là data từ thực thể bên ngoài tác động vào hệ thống, còn output data là data hệ thống show ra cho thực thể bên ngoài
- Hình chữ nhật: biểu diễn các thực thể (entity) ngoài hệ thống (các hệ thống khác, các tác nhân,…)
Đây là một ví dụ về Context Diagram:

Hình tròn ở giữa là hệ thống đang phát triển. Trong ví dụ này, hệ thống sẽ tương tác với 4 thực thể khác đó là Advertisers, Staff Writers, Accountants và Community Users. Các mũi tên có hướng chỉ chiều đi của data, biểu diễn sự tương tác giữa hệ thống với các thực thể này.

## 4.Một số ví dụ context diagram 

 

## 

## **5.Context Diagram và Data Flow Diagram (DFD)**

Trong Context Diagram ta thấy có sự trao đổi của dữ liệu giữa các thành phần thực thể bên ngoài hệ thống với hệ thống đang phát triển, điều này gợi cho chúng ta về một mô hình khác, đó là Data Flow Diagram (DFD). Điều đó hoàn toàn hợp lý vì về bản chất, DFD có nhiều mức chi tiết và Context Diagram là **mức tổng quan nhất**, còn gọi là **DFD Level-0 **hay Context-level DFD.
Từ level-0 này, trong quá trình phát triển, khi có thêm thông tin hoặc phân tích thiết kế hệ thống mà đội dự án sẽ xây dựng các level chi tiết hơn.