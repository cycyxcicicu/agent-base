---
id: 36
title: "Tạo QR thanh toán Momo - Tài liệu chức năng có actor là end user"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-19T14:16:46.000Z"
source_url: "https://m2mba.com/blog/articles/tao-qr-thanh-toan-momo-tai-lieu-chuc-nang"
---

# Tạo QR thanh toán Momo - Tài liệu chức năng có actor là end user

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-19T14:16:46.000Z*

![Ảnh bìa](images/60ed88d3-a919-4c33-9b5b-6f45ff60b451.png)

## Tạo Momo QR

 

Ngữ Cảnh: Bạn cần xây dựng chức năng Tạo QR Momo để hỗ trọ KH có nhu cầu thanh toán hóa đơn online qua Momo tại nhà hàng 

## 1.Mô tả chung
Tên UsecaseTạo QR MomoActorNV PVMục đíchCho phép NVPV chọn hình thức thanh toán là QR Momo PreconditionActor đã đăng nhập vào hệ thống và đã xác nhận đồng ý thanh toán của mã đặt bàn tương ứngMain Flow
1.Chọn Momo QR trong màn hình Thanh toán (sau khi NVPV đã xác nhận yêu cầu thanh toán, tham khảo tại [Mục 3.9.Yêu cầu thanh toán](https://docs.google.com/document/d/15aHigzA6UvCvwHoPnQU5Lpa_nI6_BbSb/edit#heading=h.17dp8vu))

2.Hệ thống hiển thị QR Momo
Post ConditionHệ thống hiển thị màn hình QR Momo với các tham số liên quan tới đơn hàng
### 2.Màn hình

 

### 3.Mô tả màn hình
STTTên controlLoại controlMô tả1Thông tin bànLabelHiển thị mã đặt bàn và tên người nhận bàn2Trạng thái đặt bànLabelTrạng thái Chờ thanh toán3Tổng tiền (chưa VAT)LabelTổng tiền chưa tính VAT4Tổng tiền VATLabelTổng tiền đã tính VAT5Tính VATSlide
Tính hay không tính VAT, với nhà hàng có tham số config cho phép KH lấy VAT hay không thì slide này sẽ được trượt sang trái/phải

Ngược lại sẽ hiển thị mặc định là Lấy VAT và không cho sửa
6Thông tin cổng thanh toán Ảnh đại diện và tên cổng thanh toán tương ứng7Danh sách ngân hàngicon
Với bên cổng thanh toán mà có kết nối nhiều bank, click vào icon này sẽ biết được các ngân hàng hỗ trợ trên cổng thanh toán này, để NV PV dễ dàng tư vấn KH

8Tiếp tụcButtonClick vào button này sẽ chuyển sang màn hình tiếp theo9Số tiền thanh toánLabelSố tiền thanh toán của đơn hàng, phụ thuộc vào thông tin ở màn hình trước NVPV đã chọn (số tiền chưa VAT hoặc đã có VAT)10Mã đơn hàngLabelLà mã đơn hàng do hệ thống foodNow sinh ra để gửi sang bên Momo11QRcodeImageẢnh QR theo quy định của Momo
### 4.Activity diagram và mô tả luồng

- **Mô tả luồng**
 
**Bước****Mô tả**3
Kiểm tra thông tin hợp lệ, thỏa mãn các điều kiện sau

- Mã đặt bàn phải đang ở trạng thái Chờ thanh toán
- Mã đặt bàn thuộc nhà hàng mà user đang đăng nhập
- Nhà hàng đang hoạt động
- User đang hoạt động 
-  4
Sinh mã GD 

- 1 là BA yêu cầu rule sinh mã GD: Mã GD phải theo dạng yyyymmddxxxxx 
- trong đó yyyymmdd là ngày GD hiện tại
- xxxxx: là chuỗi số được tăng dần từ 00001
-  
- BA ko yêu cầu sinh mã: Mã GD này phải là duy nhất5
Lấy các thông tin để tạo URL QR

- PartnerCode: Mã đối tác do Momo cung cấp cho nhà hàng
- storeId: Mã chi nhánh nhà hàng do Momo cung cấp
- Số tiền thanh toán=Số tiền của mã đặt bàn tương ứng (tùy thuộc vào chọn VAT hay không VAT để lấy số tiền thanh toán
- BilID=Mã GD vừa sinh6Tạo URL QR theo quy định của Momo: [https://developers.momo.vn/v2/#/docs/qr_payment?id=t%e1%ba%a1o-qr-code](https://developers.momo.vn/v2/#/docs/qr_payment?id=t%e1%ba%a1o-qr-code) 11
 
Trường hợpThông báo
Mã đặt bàn phải không ở trạng thái Chờ thanh toán

 
Trạng thái đặt bàn không hợp lệ, Vui lòng kiểm tra lạiMã đặt bàn không thuộc nhà hàng mà user đang đăng nhậpThông tin thanh toán không hợp lệUser không hoạt độngTài khoản của bạn đang không hoạt độngNhà hàng không hoạt độngNhà hàng đang không hoạt động trên hệ thống. Vui lòng liên hệ với nhân viên FoodNow để được hỗ trợ