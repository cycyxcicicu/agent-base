---
id: 34
title: "Tài liệu dạng tiến trình"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-19T14:08:48.000Z"
source_url: "https://m2mba.com/blog/articles/tien-trinh-xu-ly-va-charge-phi-nha-hang"
---

# Tài liệu dạng tiến trình

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-19T14:08:48.000Z*

![Ảnh bìa](images/3ba8fae5-5937-4518-93bf-9621c8ef4fb5.png)

## **1.Tiến trình xử lý đơn giản**

### **1.1.Tiến trình tạo yêu cầu thanh toán cho nhà hàng**

#### **1.1.1.Mô tả chung**
**Tên Usecase**Tiến trình tạo yêu cầu thanh toán cho nhà hàngMục đíchHệ thống tạo ra các yêu cầu thanh toán cho các nhà hàng khi sắp bước sang kỳ hạn mớiTần suất1 ngày/lần vào 01 giờ hàng ngày (có thể cấu hình thay đổi theo từng thời kỳ)Điều kiện quét dữ liệuLọc các nhà hàng có ngày kết thúc sử dụng-Ngày hiện tại <=10 và trạng thái nhà hàng khác trạng thái ĐóngPost-conditionTạo yêu cầu thanh toán với hạn thanh toán = Ngày kết thúc sử dụng, trạng thái thanh toán = Chờ thanh toán
#### **1.1.2.Biểu đồ trạng thái**

- N/A
#### **1.1.3.Luồng, Mô tả luồng/Business rule**

- Bước 1: Quét các nhà hàng thỏa mãn điều kiện ở trên
- Bước 2: Thực hiện lấy gói sản phẩm nhà hàng đang dùng, giá gói hiện tại , lấy CTKM đang áp dụng
- Bước 3: Tạo yêu cầu thanh toán với các thông tinMã nhà hàng=Nhà hàng đã quét được ở bước 1
- Gói sản phẩm= gói SP nhà hàng đang sử dụng
- Số tiền thanh toán=Giá gói hiện tai sản phẩm của nhà hàng đang sử dụng – Giảm giá KM
- Hạn thanh toán=Ngày kết thúc hiện tại của nhà hàng
- Kỳ hạn=kỳ hạn mà nhà hàng đang đăng ký sử dụng
- Trạng thái thanh toán=Chờ thanh toán
### 1.1.4.Biểu đồ luồng dữ liệu

 

 

 

 

 

## **2.Tiến trình xử lý phức tạp (Tiến trình charge phí)**

### **2.1.Tiến trình charge phí**

#### **2.1.1.Mô tả chung**
**Tên Usecase**Tiến trình charge phíMục đíchTiến trình tự động charge phí với các nhà hàng đã liên kết tài khoản/ThẻTần suất1 ngày/lần vào 8 giờ hàng ngàyĐiều kiện quét dữ liệu
Lọc theo điều kiện sau:

- các yêu cầu thanh toán có trạng thái Chờ thanh toán
- Nhà hàng có trạng thái Đang hoạt động
- Và nhà hàng tương ứng với yêu cầu thanh toán đó đã liên kết thẻ/TK và trạng thái đang hoạt độngPost-condition
- Thực hiện gửi yêu cầu sang cổng thanh toán để thực hiện trừ tiền KH 
- Cập nhật yêu cầu thanh toán về trạng thái Đã thanh toán
- Gia hạn kỳ hạn mới cho nhà hàng
- Nếu ngày kết thúc kỳ hiện tại=Ngày hiện tại -1 thì thực hiện khóa nhà hàng
#### 2.1.2.Biểu đồ trạng thái