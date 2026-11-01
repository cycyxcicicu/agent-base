---
id: 68
title: "Phân biệt Flowchart, BPMN, Activity diagram, workflow, state diagram"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T11:13:08.000Z"
source_url: "https://m2mba.com/blog/articles/phan-biet-flowchart-bpmn-activity-diagram"
---

# Phân biệt Flowchart, BPMN, Activity diagram, workflow, state diagram

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T11:13:08.000Z*

Hôm trước có 1 bạn comment trên bài viết về state diagram về việc không hiểu được các diagram khác nhau như thế nào. Hôm nay mình xin tổng hợp để chia sẻ thêm cho cả nhà nhé. Mình nghĩ đây là 1 câu hỏi mà nhiều người thắc mắc. Bài viết này mình sẽ giúp mọi người phân biệt Flowchart, BPMN, Activity diagram, workflow, state diagram

Trước hết mình sẽ định nghĩa về process Model trước đã nhé. Bản chất tất cả các diagram mình nêu ở trên, loại trừ state diagram thì các diagram khác đều được gọi là Process Model. Chỉ có nó khác nhau ở notation được sử dụng trong từng loại diagram mà thôi. Mình xin định nghĩa về process model theo đúng chuẩn sách BABOK nhé

Process model là biểu đồ dùng để thể hiện thứ tự tuần tự thực hiện các công việc trong chuỗi công việc để đạt được 1 mục đích nào đó. 

- Nếu như process model thể hiện cho luồng vận hành thì nó sẽ định nghĩa các công việc cần thực hiện giữa các phòng ban bộ phận trong công ty, tổ chức đó. 
- Nếu process model thể hiện cho luồng chức năng hệ thống thì nó thể hiện tuần tự các task cần thực hiện trong 1 chức năng nào đó của phần mềm. 
- Nếu process model thể hiện cho 1 function của code thì đó chính là thứ tự các lệnh trong function đó.
Do đó đơn giản mục đích process model dùng để thể hiện thứ tự tuần tự thực hiện các công việc, hành động, câu lệnh cho từng mục đích mà người dùng muốn thể hiện

Còn cụ thể Flowchart, BPMN, Activity diagram thì bản chất nó khác nhau ở các notation thể hiện, BPMN nó mạnh hơn vì nó có rất nhiều notation mà các loại diagram khác không có để thể hiện. Tuy nhiên nếu sử dụng nó thì bắt buộc công ty phải đào tạo cho nhân viên nắm rõ từng notation ý nghĩa là gì, còn flowchart hay Activity diagram thì notation đơn giản, không cần giải thích nhiều mọi người cũng sẽ hiểu

Các bạn có thể quan sát ảnh mình đính kèm để hiểu được là 3 loại mình nêu ở trên nó chỉ khác nhau ở notation thôi nhé

 

 

 

Với BA thì chúng ta thường sử dụng process model cho 2 mục đích

- Mô tả quy trình vận hành: Tập trung luồng vận hành giữa các phòng ban bộ phận nên mỗi lane sẽ là 1 role hoặc có thể có thêm Hệ thống liên quan (nhưng không chia nhỏ các component trong phần Hệ thống)
- Mô tả quy trình của 1 chức năng/Usecase: Chỉ được phép có tối đa 1 lane là end user, các land khác là các thành phần của hệ thống
Với state diagram thì nó thể hiện luồng chuyển đổi trạng thái của 1 thực thể, hay nói cách khác vòng đời của 1 thực thể, Ví dụ như biểu đồ trạng thái thẻ ATM mà mình đính kèm, nó thể hiện từ lúc thẻ phát hành cho KH, tới lúc thẻ khóa vĩnh viễn, không sử dụng được nữa. Biểu đồ trạng thái này là tham khảo thôi nhé, mình không nói biểu đồ này chính xác do mình không làm trong core thẻ của Bank, chỉ là ví dụ minh họa nhé