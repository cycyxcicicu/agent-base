---
id: 169
title: "Tích hợp API của bên đối tác - Viết tài liệu transfer cho dev"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-06-25T08:53:18.000Z"
source_url: "https://m2mba.com/blog/articles/49f5cf20-200f-436e-942a-afb11a5ed273"
---

# Tích hợp API của bên đối tác - Viết tài liệu transfer cho dev

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-06-25T08:53:18.000Z*

## 1.Video

## 2.Tài liệu mẫu dành cho UC có bước tích hợp

## Chức năng tích hợp API với bên khác (Chức năng lấy phí VC)

- <Hiện tại trong list hệ thống quản lý nhà hàng theo scope làm mẫu sẽ ko có chức năng nào cần tích hợp API với bên khác, nên chị giả định xây dựng chức năng Đặt yêu cầu vận chuyển để nhà hàng tạo yêu cầu ship cho đơn của KH nhé>
### 1.8.1.Mô tả chung
**Tên Usecase**Lấy phí VCActorNV lễ tânMục đíchCho phép NV lễ tân xem được thông tin phí vc khi đặt giao hàng Precondition
NV Lễ tân đã đăng nhập hệ thống và có quyền thực hiện

NVPV đang xem chi tiết yêu cầu đơn đặt ship
Main Flow
1.Actor chọn Đặt yêu cầu ship

2.Actor chọn 1 bên đối tác giao hàng và xác nhận đặt

3.Hệ thống gửi lấy phí VC

4.Đối tác trả kết quả

5.Hệ thống hiển thị phí VC
Post ConditionHệ thống hiển thị phí VC tương ứng
 

### 1.8.2.Màn hình

### 1.8.3.Mô tả màn hình

<Tương tự các chức năng khác nên chị không mô tả vào nhé>

### 1.8.4.Luồng tích hợp với DVVC - Sequence diagram

Danh sách API của GHTK
BướcLink đặc tả API1.1.1[https://docs.giaohangtietkiem.vn/#t-nh-ph-v-n-chuy-n](https://docs.giaohangtietkiem.vn/#t-nh-ph-v-n-chuy-n) 2.1.1[https://docs.giaohangtietkiem.vn/#ng-n-h-ng](https://docs.giaohangtietkiem.vn/#ng-n-h-ng) 3.1[https://docs.giaohangtietkiem.vn/#in-nh-n-n-h-ng](https://docs.giaohangtietkiem.vn/#in-nh-n-n-h-ng)3.1.3[https://docs.giaohangtietkiem.vn/#webhooks](https://docs.giaohangtietkiem.vn/#webhooks) 
### 1.8.5.Activity diagram & Mô tả luồng

Với UC này mình có thể tách ra thành 3 UC con để việc vẽ lưu đồ đỡ rối, do nhiều bước quá

- UC lấy phí vận chuyển: Chị sẽ chỉ mô tả UC này, các UC khác tương tự nhé
- UC gửi yêu cầu giao hàng
- UC in nhãn hàng
- **Lấy phí vận chuyển**

 

Mô tả luồng
BướcMô tả3
Mapping thông tin địa bàn

- Mã tỉnh của FoodNow=>Tên tỉnh địa bàn của ĐVVC (Danh mục này được đồng bộ về từ ĐVVC)
- Mã huyện của FoodNow=>Tên huyện địa bàn của ĐVVC
- Mã xã của FoodNow=>Tên xã địa bàn của ĐVVC5.1
Gửi yêu cầu lấy phí sang ĐVVC, chi tiết đặc tả API 

- GHTK: [https://docs.giaohangtietkiem.vn/#t-nh-ph-v-n-chuy-n](https://docs.giaohangtietkiem.vn/#t-nh-ph-v-n-chuy-n)
- Request data: Thông tinMô tả và mapping với hệ thống Foodnowpick_address_idID của địa điểm lấy hàng, nếu trên hệ thống đã có thông tin mapping giữa mã nhà hàng foodNow và mã address_id của đơn vị vận chuyển tương ứng thì lấy giá trị address_id đó rapick_addressĐịa chỉ chi tiết của nhà hàngpick_provinceTên tỉnh lấy hàng (tên tỉnh của nhà hàng) – Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcpick_districtTên huyện lấy hàng  (tên huyện của nhà hàng) – Mapping thông tin mã huyện của foodNow sang tên huyện của ĐvVcpick_wardTên tỉnh lấy hàng  (tên xã của nhà hàng) – Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcpick_street
Tên đường/phố nơi lấy hàng hóa

=>Không truyền giá trị này
addressTên tỉnh lấy hàng – Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcprovinceTên tỉnh nhận hàng– Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcDistrictTên huyện nhận hàng   – Mapping thông tin mã huyện của foodNow sang tên tỉnh của ĐvVcWardTên tỉnh nhận hàng  (tên xã của nhà hàng) – Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcStreet
Tên đường/phố nơi nhận hàng hóa

=>Không truyền giá trị này
WeightTính tổng cân nặng của các món ăn (mỗi món ăn đều cấu hình cân nặng tương ứng)ValueTổng giá trị tiền của món ănTransportHÌnh thức vận chuyển hàng hóa road ( bộ ) , fly (bay, Không truyền sang/truyền sang với giá trị =roaddeliver_option
Sử dụng phương thức vận chuyển xfas

Truyền giá trị none
tags<Hiện tại chị chưa hiểu trường này>
 
5.3Hiển thị thông báo lỗi: “Vui lòng liên hệ số hotline 1243345 (Không mapping được danh mục địa bàn)”7
Mapping kết quả trả về

- Nếu fee.delivery=false hoặc success=false=>Lấy phí thất bại
- Nếu success=true và fee.delivery=true=>Lấy phí thành côngThông tinMô tả và mapping với hệ thống FoodnowSuccess
True nếu thành công

False nếu thất bại
MessageMô tả lỗi, nếu thất bại sẽ có thông tin nàyfee.nameTên gói cước áp dụng, có các giá trị area1, area2, area3fee.feeCước vận chuyển tính theo VNĐfee.insurance_feeGiá bảo hiểm tính theo VNĐfee.delivery
=true nếu đã hỗ trợ giao tại địa chỉ này

=false nếu chưa giao về địa chỉ này

extFees.display

 
Thông tin hiển thị phụ phíextFees. titleTên phụ phíextFees. amountSố tiền phíextFees. TypeLoại phụ phí
 
8Kiểm tra thông tin hợp lệ nếu kết quả trả về là thành công 10
Hiển thị thông báo lỗi
**Trường hợp****Lỗi hiển thị**Địa bàn chưa hỗ trợ giao hàng (fee.delivery=false) Địa bàn chưa hỗ trợ giao hàngGửi yêu càu lấy phí thất bại (success=false)Hiển thị thông báo lỗi theo message mà ĐVVC trả về