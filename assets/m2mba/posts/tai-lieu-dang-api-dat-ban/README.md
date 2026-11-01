---
id: 35
title: "Tài liệu dạng API (API đặt bàn)"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-19T14:11:00.000Z"
source_url: "https://m2mba.com/blog/articles/tai-lieu-dang-api-dat-ban"
---

# Tài liệu dạng API (API đặt bàn)

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-19T14:11:00.000Z*

![Ảnh bìa](images/e4473f88-e3ae-4bae-800f-21fdbbaf10be.png)

## API đặt bàn

## **1.Mô tả chung**
**Tên UC****API đặt bàn****Mục đích****Cho phép các đối tác gửi yêu cầu đặt bàn sang FoodNow****Đối tượng sử dụng**Đối tác đặt bàn như Pasgo, tableNow**Post-condition**Lưu thông tin đặt bàn và Trả về kết quả đặt bàn
## **2.**Luồng** nghiệp vụ**

**Mô tả luồng**
**Bước****Mô tả****2**Mã đối tác hợp lệ: Mã đối tác tồn tại và đang hoạt động trên hệ thống**3**
Mã nhà hàng hợp lệ:

- Mã nhà hàng đang hoạt động trên hệ thống và nhà hàng đang liên kết đặt chỗ với đối tác (Mỗi nhà hàng muốn triển khai đặt chỗ trên Pasgo/Table now thì cần phải đăng ký triển khải trên ứng dụng Web quản lý nhà hàng)**4**
Khung thời gian hợp lệ

- Thời gian tới > thời gian hiện tại
- Thời gian tới nằm trong khung thời gian mở cửa của nhà hàng
- Thời gian tới không nằm trong thời gian nhà hàng thiết lập thời gian nghỉ lễ
 
**5**
Bàn hợp lệ

- Mã bàn tồn tại và đang hoạt động trên nhà hàng tương ứng
- Bàn chưa được đặt trong khung thời gian đó: Bàn không booking nào mà có thời gian thời gian dự kiến kết thúc>=thời gian KH đặt >=Thời gian dự kiến tới
 
**6**
Lưu thông tin đặt bàn

- Các thông tin tham số đầu vào
- Và các thông tinMã đặt bàn: Tự sinh theo quy định chung
- Thời gian đặt =Thời gian hiện tại
- Thời gian dự kiến kết thúc=Thời gian dự kiến tới + thời gian phục vụ trung bình/bàn
## **3.Thông tin đầu vào**
**Thông tin****Require****Length****Mô tả/Ràng buộc khác**Mã đối tácYes Mã đối tác do foodNow đã cung cấp cho đối tácMã yêu cầu đặt bànYes  Mã nhà hàngYes Mã nhà hàng trên hệ thống pasgoHọ tên KH đặtYes**3-50**Chỉ gồm các ký tự aA-zZ và ký tự blankSố điện thoại người đặt bànYes10Gồm 10 ký số bắt đầu bằng 03,08,09Thời gian dự kiến tớiYes 
Định dạng ddmmyyyy hh24:mi:ss

Thời gian dự kiến tới>Thời gian hiện tại
Số người Yes Số nguyên dương, tối đa 3 ký tự số
## **4.Thông tin đầu ra**
**Thông tin****Mô tả/Ràng buộc khác**Mã đối tácMã đối tác do foodNow đã cung cấp cho đối tácMã nhà hàngMã nhà hàng trên hệ thống FoodNowMã yêu cầu đặt bànMã này của pasgoMã đặt bànMã đặt bàn tương ứngMã lỗiMã lỗi tương ứngMô tả lỗiMô tả lỗi tương ứng, xem chi tiết danh sách lỗi bên dưới
## **5.Danh sách mã lỗi**
**Trường hợp****Mô tả lỗi tương ứng**Mã đối tác không tồn tại hoặc không hoạt độngMã đối tác không hợp lệMã nhà hàng không tồn tại hoặc không hoạt độngMã nhà hàng không hợp lệHết bàn đặtHết bànThành côngThành công