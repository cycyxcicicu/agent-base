---
id: 113
title: "Web admin - Chi tiết yêu cầu"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-25T06:52:26.000Z"
source_url: "https://m2mba.com/blog/articles/0502d912-8a12-4134-add2-502e50640d36"
---

# Web admin - Chi tiết yêu cầu

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-25T06:52:26.000Z*

## 1.Admin Portal - Quản lý Danh sách đăng ký

- Ở Page này sẽ gồm các UC: Tìm kiếm yêu cầu đăng ký khóa học
- Hủy đăng ký
- Xác nhận thanh toán
- Xuất danh sách Email (phục vụ việc share video)
### 1.1. Màn hình

### 1.2.Mô tả màn hình

**STT**

 

**Tên control**

 

**Mô tả**

 
1Khóa học đăng ký
Hiển thị danh sách khóa học trên hệ thống

Hiển thị theo thứ tự sau

Khóa học đang hoạt động

Khóa học đã bị inactive

Mặc định là chọn tất cả
2Lớp học
Hiển thị danh sách các lớp học tương ứng với khóa học đang chọn hiện tại. Nếu chọn tất cả khóa học thì lấy tất cả lớp của các khóa học trên hệ thống

Mặc định là tất cả

Các lớp sắp xếp theo thứ tự

Lớp ở trạng thái đang học

Lớp ở trạng thái Chờ khai giảng

Lớp học ở trạng thái kết thúc và Dừng hoạt động
3EmailTìm kiếm tương đối4Số điện thoạiTìm kiếm chính xác5Từ ngày
Từ ngày <=ngày hiện tại

Mặc định là ngày hiện tại - 60 ngày
6Đến ngày
Ngày hiện tại>=Đến ngày>=Từ ngày

Mặc định là ngày hiện tại
7Trạng thái đăng ký
Hiển thị danh sách các lựa chọn trạng thái

Tất cả

Chờ thanh toán

Đăng ký thành công

Đang học

Đang bảo lưu

Hoàn thành

Hủy đăng ký
8Trạng thái share video
Tất cả

Đã share

Chưa share
9Tìm kiếmClick vào sẽ tìm kiếm thỏa mãn tất cả các điều kiện nhập vào10Hủy đăng ký
Click vào đây sẽ cho phép admin hủy đăng ký khóa học của học viên

Chỉ cho phép hủy khi đang ở trạng thái Chờ thanh toán
11Xác nhận thanh toánClick vào đây sẽ cho phép admin xác nhận thanh toán12Lớp học chọn bảo lưu
Với TH học viên Đang bảo lưu và chọn lớp lúc bảo lưu rồi

Đây là tên lớp của lớp học viên chọn sẽ học khi bảo lưu
13Lớp học chọn bảo lưuVới TH học viên Đang bảo lưu và chưa chọn lớp lúc bảo lưu15Xuất danh sách email
Hiển thị popup: Danh sách email.

Thực hiện tạo danh sách các email theo kết quả tìm kiếm và các email được phân cách dấu ,

Khi click vào nút Copy thì sẽ cho phép paste thông tin vào 1 nơi khác
16Xác nhận share videoHiển thị màn hình xác nhận share video17Lịch sử share videoHiển thị màn hình lịch sử share video
### 1.3[.Biz](http://3.biz/) Rule

#### **1.3.1.Tìm kiếm khóa học**

Đầu vào tìm kiếm

 

**Thông tin**

 

**Yêu cầu lọc dữ liệu**

 
Tiêu chí tìm kiếmThỏa mãn tất cả các điều kiện tìm kiếm nhập vào (AND)EmailTìm kiếm tương đối, ko phân biệt hoa thườngSố điện thoạiTìm kiếm chính xácKhóa học đăng ký
Dữ liệu: Lấy ra toàn bộ khóa học đang tồn tại trên hệ thống, sắp xếp theo thứ tự

Khóa đang active: Sắp xếp tên tăng dần theo alpha B

Khóa inactive: Sắp xếp tên tăng dần theo alpha B

 
Lớp học
Lấy ra toàn bộ lớp học trên hệ thống (kể cả đã inactive)

Nếu chọn khóa học thì sẽ lọc lớp học theo khóa học tương ứng

Lớp học sắp xếp theo thời gian khai giảng giảm dần
Trạng thái
Bao gồm các trạng thái

Chờ thanh toán

Đăng ký thành công

Đang học

Đang bảo lưu

Hủy đăng ký
Sắp xếp danh sáchOrder theo thời gian đăng ký giảm dần
#### **1.3.2.Hủy đăng ký**

- Chỉ cho phép hủy khi đang ở trạng thái Chờ thanh toán
- Giảm 1 học viên đối với thông tin số lượng đăng ký trong bảng Lớp hoc/Đợt tuyển sinh 
- Và update trạng thái về Hủy đăng ký khi hủy thành công
 

#### **1.3.3. Xác nhận thanh toán**

- Chuyển trạng thái đăng ký về Đăng ký thành công
- Insert vào bảng Lớp học với học viên tương ứng
- Gửi email cho học viên với nội dung (sẽ cung cấp sau)
 

#### **1.3.4. Xuất danh sách email để share video**

Thực hiện tạo danh sách các email theo kết quả tìm kiếm và các email được phân cách dấu ,

 

Khi click vào nút Copy thì sẽ cho phép paste thông tin vào 1 nơi khác

## 2. Admin Portal - Danh sách lớp học/Start/Stop lớp học

Trang này mô tả cho 3 UC 

- Danh sách lớp học
- Start lớp học
- Stop lớp học
 

### **2.1. Màn hình**

### 2.2.Mô tả màn hình

**STT**

 

**Thông tin**

 

**Mô tả**

 
1Khóa học
Hiển thị danh sách các khóa học (kể cả đã dừng hoạt động)

Sắp xếp theo thứ tự

Khóa học đang active : Sắp xếp theo alpha B tăng dần

Khóa học inactive: Không cần sắp xếp
2Lớp học
Hiển thị danh sách lớp học theo khóa học đã chọn (lấy tất cả các trạng thái)

Sắp xếp theo thứ tự thời gian khai giảng giảm dần
3Trạng thái
Hiển thị danh sách trạng thái sau

Chờ khai giảng

Đang học

Kết thúc

Dừng hoạt động
4Khai giảng từ ngàyko bắt buộc nhập5Khai giảng đến ngàyko bắt buộc nhập, từ ngày <=đến ngày6Trạng thái lớp họcTrạng thái của lớp tương ứng7xem chi tiết lớp họcClick vào icon sẽ hiển thị chi tiết lớp học8Start lớp họcHiển thị khi lớp ở trạng thái chờ khai giảng9Stop Lớp họcHiển thị khi lớp ở trạng thái Đang học
### 2.[3.Biz](http://3.biz/) Rule

**Chức năng**

 

**Rule**

 
Danh sách lớp họcTìm kiếm thỏa mãn tất cả các điều kiện (nếu nhập)Danh sách lớp học
Sắp xếp danh sách theo thứ tự sau

Đang học

Chờ khai giảng

Kết thúc

Trong nhóm **Đang học và sắp khai giảng** thì sắp xếp theo thời gian khai giảng tăng dần

Nhóm **kết thúc** thì sắp xếp theo thời gian **kết thúc giảm dần**
Start lớp họcChỉ được start khi lớp đang ở trạng thái Chờ khai giảng và ngày khai giảng <=ngày hiện tạiStop lớp họcChỉ được stop lớp học khi lớp ở trạng thái Đang học và ngày khai giảng <ngày hiện tại
## 3. Admin portal - Xem chi tiết lớp học

### 3.1.Màn hình

### 3.2.Mô tả màn hình

19: Đánh giá học viên

20: Add tài liệu cho khóa học

 

### 3.3.[Biz](http://3.biz/) Rule

**Thông tin học viên**

- Tìm kiếm thỏa mãn tất cả các thông tin nhập vào
- Tìm kiếm chính xác theo số điện thoại , tương đối với email nhập vào
- Sắp xếp theo alphaB tăng dần theo Tên học viên
**Thông tin tài liệu**

- Lấy danh sách tài liệu thuộc khóa học của lớp học tương ứng
- Và danh sách tài liệu thuộc lớp học tương ứng
 

## 4.Admin Portal - Xác nhận share video

### 4.1. Màn hình

### 4.2. Mô tả màn hình

**STT**

 

**Tên control**

 

**Mô tả**

 
1Khóa học
Lấy danh sách các khóa học dang hoạt động trên hệ thống

Bắt buộc chọn
2Lớp học
Bắt buộc chọn

Chỉ được hiển thị khi đã chọn khóa học

hiển thị danh sách các lớp học ở trạng thái Chờ khai giảng và Đang học của khóa học hiện tại

Sắp xếp theo thứ tự

Lớp học chờ khai giảng

Lớp học Đang học
3List video/tài liệuLấy ds các list video/tài liệu của Khóa học tương ứng hoặc theo lớp học đã chọn4ds email
Các email cách nhau dấu , và phải đúng format email

Email đó phải tương ứng với email học viên đăng ký lớp học tương ứng

**Nếu ko đúng thì sẽ hiển thị ds email không hợp lệ, và không thực hiện xác nhận share video của toàn bộ email trong ds**

### 4.[3.Biz](http://3.biz/) Rule

- 1 email chỉ được share cho 1 list video 1 lần
- email này phải nằm trong ds đăng ký của khóa học tương ứng với lớp học của list video tương ứngMối quan hệ: 1 lớp học có 1 list video cần share trước khóa học, 1 lớp học thuộc 1 khóa học
- Ví dụ : Học viên đăng ký lớp ON062023 thuộc khóa BA thực chiến - ONLINE thì học viên đó sẽ được share các list video của lớp thuộc khóa học BA thực chiến - ONLINE (lớp nào cũng được nhưng 1 list video chỉ được share đúng 1 lần)
- Lưu thông tin:Cập nhật trong bảng Lịch sử đăng ký với trạng thái share video nếu list được chọn là list dạng video (nếu trạng thái đang là chưa share)=Đã share với các email tương ứng
- LƯu lịch sử share videoNgày share: Ngày hiện tại
- Danh sách email đã share
- List video đã share
- Khóa học tương ứng của list video
- Lớp học tương ứng của list video
## 5. [Admin portal - Lịch sử share video

### 5.1.Màn hình

### 5.2. Mô tả màn hình

5: Copy danh sách email

4: Expend: thông tin ds email đc share ở lượt đó

 

## 6. Admin portal - Thêm mới tài liệu

### 6.1.Màn hình

### 6.2. Biz Rule

- URL là duy nhất trong các URL : của khóa học tương ứng với lớp học
- và URL của lớp học tương ứng
## 7. [Admin Portal] Đánh giá học viên (bao gồm cả thêm mới và update)

### 7.1.Màn hình

###  

### 7.2.Mô tả màn hình
SttTên controlMô tả10Lớp đăng ký
Gồm tên khóa học - Tên lớp học

Trong đó lớp học là lớp mà học viên tham gia học
11Xếp loại (bắt buộc nhập)
Nếu học viên nào đã có đánh giá thì hiển thị xếp loại hiện tại

Nếu chưa đánh giá lần nào thì hiển thị : Xếp loại
12Ảnh chứng chỉ (bắt buộc nhập)
Hiển thị ảnh hiện tại (nếu đã đánh giá trước đó), và cho phép upload lại

file có đuôi png, img

size kích thước tối đa XXX MB
13Link test (bắt buộc nhập)
Cho phép user copy link bài làm của học viên

Nếu đã có đã giá trước đó thì hiển thị link hiện tại và cho phép user thay đổi
14Đánh giá Chi tiết (bắt buộc nhập)
Cho phép user nhập đánh giá chi tiết cho học viên

Nếu đã có đánh giá trước đó thì hiển thị đánh giá hiện tại và cho phép sửa

### 7.[3.Biz](http://3.biz/) Rule

Không giới hạn số lần update

Update trạng thái học viên theo lớp học về trạng thái : Đã đánh giá

 

## 8.[Admin portal] Import sao kê

### 8.1.Màn hình

### 8.2.Mô tả màn hình

**STT**

 

**Tên control**

 

**Mô tả**

 
1Chọn file
Click vào button này, hệ thống mở màn hình chọn file trên máy tính

chỉ chọn file xlsx
2Đường dẫn fileSau khi chọn file xong, hệ thống sẽ hiển thị đường dẫn file tương ứng3Download file mẫu
Cho phép user download file mẫu

File mẫu xem t

Open transaction_history.xlsx

 

**transaction_history.xlsx**

10 Jun 2023, 06:39 AM

 
4UploadClick vào đây sẽ ra màn hình số 55MH thông báo kết quả upload 6Số lượng bản ghi thành công 7Số lượng bản ghi import thất bạiKhông tính các trang header và footer8File outputClick vào file có thể tải file đó về để xem
### 8.[3.](http://3.biz/)Yêu cầu file đầu vào

File bắt buộc phải có các cột , dữ liệu trong các cột không ràng buộc gì

- Ngày GD: theo format dd/mm/yyyy hh23:mi
- Phát sinh có
- Số bút toán
- Nội dung
- Tài khoản
- Ngân hàng đối tác
### 8.[4.Biz](http://4.biz/) rule

- 1 số bút toán được import duy nhất 1 lần
- Chỉ import các giao dịch có phát sinh có>0
 
### 8.5.File output

- Tên file: Thêm _result vào cuối tên file
- Thêm 2 cột so với file import: Kết quả, mô tả lỗi
- Nếu kết quả là thất bại thì ghi mô tả lỗi tương ứng, có các lỗi sauSố bút toán đã được import trước đó
- Ngày tháng không đúng định dạng
- Thông tin không đầy đủ theo yêu cầu (Tức dữ liệu dòng phát sinh có >0 ko có đủ các trường thông tin như mục 3 (dữ liệu ở 1 trong các cột số bị rỗng
### 8.6. Thông tin bảng quản lý dữ liệu

###  

- Lưu ý các thông tin nàyĐường dẫn file sao kê = Thông tin trong control số 2
- Trạng thái khi vừa import: Chưa xác nhận
 
 

###