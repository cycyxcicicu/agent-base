---
id: 82
title: "Bài tập về nhà về lập trình cơ bản ở khóa IT cho BA"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-01-26T03:02:50.000Z"
source_url: "https://m2mba.com/blog/articles/tinh-thuong-lap-trinh-co-ban-it-ba"
---

# Bài tập về nhà về lập trình cơ bản ở khóa IT cho BA

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-01-26T03:02:50.000Z*

**BTVN LẬP TRÌNH CƠ BẢN**

## **1.Ngữ cảnh đề bài**

Giải thích thuật ngữ

- AR: Acceptance Rate: Tỷ lệ tài xế chấp nhận chuyến xe
- CR: Cancel Rate: Tỷ lệ tài xế Hủy chuyến xe
Bạn hãy đọc một số quy định của Grab tại link đính kèm, hãy đưa ra ERD để có thể quản lý được theo yêu cầu đó

Một số quy định/lưu ý thêm

- Mỗi khu vực sẽ gồm 1 số các tỉnh thành
- Tỷ lệ AR, CR có thể thay đổi theo từng thời kỳ
## 1.1.Chi tiết yêu cầu 

Yêu cầu về Thưởng Nhân giá giờ cao điểm như sau:

Thưởng Nhân Giá Giờ Cao Điểm – Chương trình này với mục đích hỗ trợ Đối tác có thể GIA TĂNG MỨC THU NHẬP VỚI VIỆC GRAB ĐẢM BẢO NHÂN GIÁ CHO TỪNG CUỐC XE. Nếu cuốc xe có hệ số nhân giá (trên giá cước) thấp hơn mức đảm bảo, GRAB sẽ thưởng cho đối tác khoản chênh lệch.

Ví dụ

Một chương trình Thưởng Nhân Giá Giờ Cao Điểm với mô tả chi tiết như sau:

Với 2 cuốc xe thỏa c.trinh thưởng như sau:

- Cuốc 1 – Cuốc xe tại khu vực A hoàn thành trong khung giờ từ 6h30 – 7h30 sáng sẽ có hệ số nhân là 1.2
- Cuốc 2 – Cuốc xe tại khu vực B hoàn thành trong khung giờ từ 6h30 – 7h30 sáng sẽ có hệ số nhân là 1.4
Cách tính thưởng: Giá thông thường x Hệ số nhân – Giá cuối cùng = Thưởng.

Trong đó giá thông thường (Đây là giá thu KH) là giá tính ở mức đơn giá bình thường (không nhân hệ số giờ cao điểm)

Giá cuối cùng là giá mà KH phải trả thực cho Grab (có thể bị tăng giá hoặc ko tăng giá so với giá thông thường)

Một số yêu cầu nghiệp vụ

 
Yêu cầu nghiệp vụ
Chương trình được áp dụng cho các khu vực khác nhau. Theo đó tỷ lệ nhân giá được tính trên địa điểm đón, với ràng buộc cuốc xe phải được kết thúc trong địa phận Thành phố đang áp dụng chương trình (có thể không cùng khu vực với điểm đón, nhưng phải ở khu vực đang có áp dụng hệ số nhân)

Ví dụ 

- Cuốc A đi từ HCM đến Bình Dương: HCM và Bình Dương đều trong khu vực áp dụng hệ số nhân nên cuốc này sẽ được hệ số nhân theo điểm đón Khu vực HCM
- Cuốc B đi từ HCM đến Đồng Nai: HCM nằm trong khu vực áp dụng chường trình nhưng Đồng Nai không thuộc=>Không được áp dụng chương trình nàyMỗi cuốc xe chỉ dừng ở 1 điểm (tạm thời chị đưa yêu cầu như thế này để đơn giản đã nhé)Nếu giá cuối cùng > Giá thông thường x Hệ số nhân thì điểm thưởng sẽ =0 (thực ra cái này bình thường là tự tư duy, ko ai nói ra cả nhé, chị note để bọn e lưu ý khi làm bài
 

## 1.2.Thiết kế DB

Dưới đây là thiết kế DB liên quan tới yêu cầu trên

Giải thích bảng
BảngGiải thíchbooking
Lưu thông tin các cuốc xe

Sau khi hệ thống tính được tiền thưởng của cuốc xe thì sẽ lưu vào thuộc tính tien_thuong

Giá trị mặc định da_tinh_thuong=0,Nếu đã tính thưởng thì sẽ update Da_tinh_thuong=1
config_bonusCấu hình mức hệ số nhân theo yêu cầu nghiệp vụ ở trên (đã có trong BTVN về ERD)dịch vụLưu các thông tin dịch vụ của grab như grabbike, car, delivery,...cấu hình tham số chungCấu hình các tham số như AR, CRcustomerLưu thông tin KHdriverLưu thông tin tài xếDiem_thuong
Lưu thông tin điểm thưởng theo từng cuốc xe (nếu có)

Để tính tổng tiền thưởng cho 

 

## 1.3.Luồng nghiệp vụ

## 1.4.Mô tả chi tiết về Tiến trình tính thưởng 

- Tần suất: 1 ngày/lần vào 1:00 sáng
- Điều kiện lọc dữ liệu: Lọc các booking của ngày N-1 và có trạng thái hoàn thành (Completed) và chưa được tính điểm thưởng
- Xử lý: Thực hiện tính tiền thưởng cho tài xế và lưu thông tin tiền thưởng vào Bảng Diem_thuong với trạng thái Chưa thanh toán, và thông tin tiền thưởng vào bảng booking.tien_thuong, booking.da_tinh_thuong=1
 

## **2.Yêu cầu bài tập**

**Bài 1:** trong tiến trình tính thưởng, sẽ cần gọi hàm **calc_bonus** với tham số đầu vào là bookingID, bạn hãy tư duy flow (không cần viết code) để tính ra được tiền thưởng đó

các bạn cần xem thiết kế DB để biết lấy dữ liệu ở bảng nào, điều kiện gì nhé, chỗ flow bên dưới có câu SQL, các e có thể ko cần viết mà chỉ cần nêu lấy dữ liệu bảng nào, lọc theo điều kiện gì là đủ nhé

Flow dạng như sau (Ví dụ flow đăng ký khóa học của trung tâm đào tạo)

**Bài 2**: Để lọc được các booking thỏa mãn như yêu cầu trên Lọc các booking của ngày N-1 và có trạng thái hoàn thành (Completed) và chưa được tính điểm thưởng. Bạn hãy nêu cụ thể cách lọc trong bảng booking như thế nào (lọc trường nào, điều kiện ra sao, nói bằng lời, ko cần câu SQL cụ thể)

**Bài 3:** Để xử lý tính toán tiền thưởng cho tất cả các booking, theo bạn lập trình viên phải dùng lệnh gì trong số các lệnh đã học (if else, switch case, for loop, while loop), và bạn có thể diễn giải ý hiểu của mình với lệnh đó áp dụng trong bài này (ko sợ sai, cứ làm thôi nhé)