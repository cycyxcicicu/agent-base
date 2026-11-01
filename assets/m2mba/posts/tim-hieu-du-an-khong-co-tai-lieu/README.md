---
id: 64
title: "Tìm hiểu dự án không có tài liệu"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T09:55:49.000Z"
source_url: "https://m2mba.com/blog/articles/tim-hieu-du-an-khong-co-tai-lieu"
---

# Tìm hiểu dự án không có tài liệu

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T09:55:49.000Z*

HƯỚNG DẪN TIẾP CẬN DỰ ÁN KHÔNG CÓ TÀI LIỆU

Mục đích của bài chia sẻ này giúp bạn giải quyết được các vấn đề chính sau 

- Hiểu cơ bản mảng nghiệp vụ mà dự án mình sẽ làm
- Nắm bắt được quy trình nghiệp vụ và luồng xử lý hệ thống
- Tài liệu hóa hệ thống hiện tại (Ưu tiên tài liệu hóa 1 số thông tin cơ bản, không viết lại hết được)
Nếu bạn là 1 người đã có kinh nghiệm thì có thể phân tích các vấn đề đang gặp phải với dự án cũng như từ đó đề xuất ra cách xử lý (phần này thì ngay từ khi vào chúng ta khoan hãy làm việc này nhé, nếu có thì tạm thời âm thầm làm đã, dự án nào thường cũng có vấn đề, khi nói ra các vấn đề của đội cũ thì nên khéo léo, tránh TH thành viên cũ ác cảm với mình, để sau đó sẽ khó phối hợp)

Để có thể hoàn thành được các việc trên, bạn hãy thực hiện các step sau nhé

## 1.Nắm mục tiêu của dự án:

 Điều quan trọng đầu tiên với bạn đó là phải hiểu dự án của bạn đưa ra sản phẩm nhằm mục đích gì, phục vụ cho những loại đối tượng như thế nào. Mọi thứ của BA cần được xuất phát từ NEEDs phải không nhỉ? NEEDs các bạn có thể dựa vào kinh nghiệm để dự đoán được khi đọc tên dự án và sau đó thêm thông tin từ PM hay các bạn dev/test trong team của bạn

## 2.Masterplan của sản phẩm

Bạn cần nằm rõ lộ trình của sản phẩm như thế nào kèm với kế hoạch của dự án, tối thiểu là trong 1 đến 3 tháng tới. Tốt nhất bạn nên hỏi trước PM lộ trình sản phẩm và xem hiện trạng nó đang nằm ở đâu trong lộ trình đó. Nếu dự án chưa có ai quản lý phần này thì tốt nhất bạn nên chuẩn bị tinh thần lập file để quản lý kế hoạch triển khai cho sản phẩm của bạn theo từng giai đoạn nhé

## 3.Nắm bắt các vấn đề đang gặp phải của team

Hỏi leader của team hay 1 thành viên cứng của dự án để nắm các vấn đề dự án đang gặp phải, ở bước này chủ yếu lắng nghe và ghi chú lại các vấn đề rồi sau đó khi đi dần vào tìm hiểu hệ thống sẽ lắp ghép vào vấn đề mà bạn đã
được nói từ trước 

## 4.Tìm hiểu overview về hệ thống

- **Bước 1:** Request người transfer Trước khi bạn chủ động tự tìm hiểu hệ thống thì đầu tiên bạn vẫn cần phải có 1 người để transfer nghiệp vụ của hệ thống. Ở bước này bạn hãy tìm câu trả lời cho các vấn đề sau:Hệ thống của bạn có những ứng dụng con nào (Mobile app cho KTV,
Mobile app cho KH, Web app cho NV vận hành...). 
- Mục đích của từng ứng dụng con đó, và phục vụ cho những đối tương nào. (Sau đó bạn vẽ mind
map để biết các đối tượng có những nhiệm vụ gì trên từng ứng dụng đó)
- Hệ thống của bạn cần tương tác với nhưng bên nào ngoài hệ thống của bạn không, và tương tác để làm gì, lúc nào, tần suất ra sao
- Quy trình vận hành của con người tương ứng với các tính năng trên các ứng
dụng
- Output của phần này bạn sẽ có:Mô hình tổng quan của hệ thống
- Mindmap thể hiện từng nhiệm vụ của từng đối tương trên từng ứng dụng con
- Quy trình vận hành của hệ thống
 
- **Bước 2**: Lập danh sách các chức năng trên các ứng dụng
Bạn hãy đăng nhập vào ứng dụng cần tìm hiểu, xem trên từng menu của ứng để tìm ra các nhóm chức năng chính. Mỗi menu (kể cả cấp nhỏ nhất), Bạn có thể mở màn hình để view qua, chưa cần để ý quá chi tiết nhé. · Sau đó tổng hợp trong file excel theo cấu trúc sau:
☑️Phân hệ
☑️Nhóm chức năng (thường chính là menu cha của chức năng đó)
☑️Chức năng
☑️Đường dẫn menu chức năng
☑️Mô tả ý nghĩa chức năng: Cái này có thể hỏi các bạn trong team, hoặc tự mình mò mẫm tìm hiểu từ chính tên của nó
## 5. Tìm hiểu thiết kế DB của hệ thống

Ở đây các bạn chỉ cần xin vào hệ thống dev, không cần hệ thống LIVE. Bạn hãy liệt kê các bảng dữ liệu của hệ thống (có thể dùng câu lệnh trên từng hệ quản trị CSDL để select ra toàn bộ bảng dữ liệu). Sau đó tìm mối liên hệ giữa các bảng với nhau để biết mô hình quan hệ như thế nào. Cái này nếu không tự mò ra được thì có thể hỏi thêm dev nhé. Output của bước này chính là bạn sẽ có 1 biểu đồ ERD hoặc mô hình quan hệ CSDL của hệ thống

## 6. Tìm hiểu chi tiết chức năng

Sau khi bạn đã overview được các thông tin của dự án như các bước guideline ở trên thì bạn mới nên đi vào chi tiết nhé. Mục đích của bước này vừa là để bạn hiểu rõ hơn về hệ thống, vừa là để đưa ra các đánh giá nhận xét, xem hệ thống hiện tại
có vấn đề gì cần cải tiến không? Với các hệ thống nhỏ, ít chức năng thì bạn có thể tìm hiểu chi tiết lần lượt toàn bộ hệ thống trong thời gian ngắn, tuy nhiên với các hệ thống lớn thì bạn nên tập trung vào các module, chức năng, màn hình chính trước. Nếu bạn đang cần join gấp vào để làm thì nên tìm hiểu chi tiết các tính năng liên quan (có thể hỏi thêm dev nếu chưa tự phát hiện ra nhóm chức năng nào liên quan). Ở bước này, các bạn có thể thưc hiện như sau:

- Thực thi các tính năng đó trên hệ thống
- Vào check db xem thông tin lưu trữ như thế nào: Lưu trữ bảng nào, dữ liệu các trường như thế nào
- Xin testcase để nắm rõ các rule của hệ thống và nếu có thời gian thì thử thực hiện các case đó luôn · Kết hợp với các vấn đề mà bạn có thông tin ở bước 4 để hiểu thêm các vấn đề bất cập mà bạn được thành viên của team báo
- Chủ động tìm hiểu thêm các vấn đề tồn đọng khác của hệ thống trong quá trình thực thi các chức năng
## 8.Tiếp tục hỏi cho rõ thông tin

Sau khi qua các bước trên, chắc chắn các bạn cũng sẽ có 1 list các câu hỏi giống như khi các bạn đi khơi gợi yêu cầu từ KH vậy, nhưng chẳng qua ở đây các bạn đã có yêu cầu rồi và cần làm rõ các thông tin thôi. Khi đó các bạn sẽ hỏi các thành viên trong team để xác nhận lại các câu hỏi của mình, nếu cái nào không rõ thì nhờ dev xem trong code để rõ luồng hiện tại đang như thế nào

## 9.Tài liệu hóa hệ thống

Khi bạn vào giữa dự án mà bắt bạn làm lại toàn bộ tài liệu chi tiết của dự án thì thực sự là mất thời gian, chưa kể bạn còn phải nhanh chóng nắm bắt để còn bắt tay vào làm các tính năng mới khác, hoặc update các tính năng cũ. Do đó ở bước này các bạn chỉ nên tổng hợp được các thông tin sau vào 1 tài liệu tổng hợp thôi nhé.

- Mục tiêu hệ thống: Hiểu được vấn đề mà hệ thống cần phải giải quyết là gì, tại sao cần phải thực hiện nó
- Mô hình tổng quan hệ thống: Cho biết hệ thống gồm những thành phần nào, kết nối với những bên nào
- Danh sách các stakeholder liên quan, nhiệm vụ và vai trò của từng người
- Danh sách các actor của hệ thống
- Bảng danh sách các chức năng trên từng phân hệ, mỗi chức năng kèm thêm ai là actor và mô tả qua ý nghĩa của từng chức năng và các ràng buộc nếu có 
- Biểu đồ ERD hoặc thiết kế DB
## 10.Đưa ra 1 số đề xuất cải tiến (dành cho các bạn senior)

Sau khi đã hiểu hệ thống, đã biết được các vấn đề bất cập của hệ thống hiện tại. Bạn hãy đưa ra các đề xuất cải tiến cho hệ thống đó. Với các vấn đề có tầm ảnh hưởng lớn, rủi ro thì các bạn nên cố gắng phân tích để các bên hiểu rõ và cố gắng chỉnh sửa sớm. Còn các cải tiến khác thì bạn có thể đưa vào lộ trình sẽ chỉnh sửa, chưa cần chỉnh sửa ngay do vì nó còn phụ thuộc nhiều yếu tố khác. Và một lưu ý nhắc nhở các bạn đó là khi mới join vào dự án, chúng ta nên đứng với vai trò tìm hiểu và học hỏi trước. Các vấn đề có thể chúng ta sẽ nhận diện ra ngay được, nhưng bạn nhớ không phải là team không biết các vấn đề đó, chỉ có điều điều kiện chưa cho phép họ khắc phục các vấn đề đó thôi nhé.