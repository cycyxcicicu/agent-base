---
id: 114
title: "Nghiệp vụ quản lý chữa bài tập về nhà (Bổ sung nhóm nghiệp vụ mới khi dự án đã chạy)"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-25T06:55:27.000Z"
source_url: "https://m2mba.com/blog/articles/722c4ab1-9695-400e-9bac-61dae87f4cae"
---

# Nghiệp vụ quản lý chữa bài tập về nhà (Bổ sung nhóm nghiệp vụ mới khi dự án đã chạy)

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-25T06:55:27.000Z*

## I. Tổng quan

## 1.Quy trình

## 2.Danh sách UC

## 2.1 Web học viên

**Ứng dụng**

 

**Tên chức năng**

 

**Mô tả chức năng**

 
Web học viênĐăng ký/thay đổi Case studyCho phép học viên đăng ký case study phục vụ cho khóa họcWeb học viênThống kê BTVN theo lớp họcCho phép theo dõi tổng số lượng BTVN theo trạng thái của từng lớp học mà học viên đang theo họcWeb học viênXem danh sách BTVN theo lớp họcCho phép học viên theo dõi ds bài tập về nhà của 1 lớp học tương ứngWeb học viênXem chi tiết BTVNCho phép học viên xem chi tiết yêu cầu của 1 bài tập về nhàWeb học viênNộp bài tập về nhàCho phép học viên nộp bài làm của mìnhWeb học viênChỉnh sửa thông tin nộp BTVNcho phép học viên chỉnh sửa lại bài làm của mìnhWeb học viênXác nhận sửa bàiCho phép học viên xác nhận đã hoàn thành sửa bài
## 2.2. Web admin

**Ứng dụng**

 

**Tên chức năng**

 

**Mô tả chức năng**

 
Web adminXem danh sách case studyCho phép theo dõi ds case study của học viên đã đăng kýWeb adminChỉnh sửa case studyCho phép mentor có thể sửa lại case study nếu đã quá hạn sửa case studyWeb adminXem danh sách BTVN của học viênXem danh sách BTVN theo từng học viênWeb adminCRUD Bài tập về nhà cho khóa học =>**Phần này khoan đã làm nhé, vì chỉ có 1 khóa học có BTVn thôi, nên tạm thời insert DB đã, để ưu tiên làm phần khác trc tết**Cho phép mentor tạo BTVN theo từng khóa họcWeb adminGiao bài cho lớpCho phép admin chọn ds BTVN giao cho lớp tương ứngWeb adminXem danh sách BTVN của học viênCho phép mentor xem danh sách BTVN mà học viên đã nộp để sửa bàiWeb adminXem chi tiết bài làm của học viênXem chi tiết bài làm của học viên, theo dõi được log tác động của học viênWeb adminĐánh giá bài tập về nhàCho phép mentor đánh giá BTVN của học viên
## **3.ERD**

 

 

Các hành động cần insert vào bảng log_tac_dong

Đăng ký case study

Chỉnh sửa case study

Nộp bài tập

sửa bài tập

đánh giá bài tập

## 4.Biểu đồ trạng thái **bai_lam_hóc_viên**

 

## II. Usecase

## 1.Admin portal -Danh sách chữa BTVN

### **1.1Mô tả chung**

**Tên UC**

 

**Xem danh sách chữa bài tập về nhà**

 
ActorAdmin, MentorMô tả ý nghĩaCHo phép actor xem danh sách các BTVN của học viên để chữa bài kịp thời
### 1.2.Màn hình

 

**STT**

 

**TÊn control**

 

**Loại control**

 

**Mô tả / ràng buộc**

 
1Khóa họcCombobox
Hiển thị danh sách các khóa học đang hoạt động trên hệ thống

 
2Lớp họcCombobox
Nếu không chọn khóa học: Hiển thị tất cả các lớp học có trạng thái Đang học/Hoàn thành trên hệ thống

Nếu chọn khóa học: hiển thị các lớp học có trạng thái Đang học/Hoàn thành thuộc khóa học tương ứng

Sắp xếp các lớp học theo thứ tự trạng thái

Đang học

Hoàn thành
3BTVNCombobox
Hiển thị ds các BTVN được giao cho lớp/Khóa học tương ứng

Bắt buộc phải chọn lớp học/khóa học

Nếu chỉ chọn khóa học: Hiển thị ds BTVN đang hoạt động theo khóa học tương ứng

Nếu chọn lớp học: hiển thị ds BTVN đang hoạt động của lớp học tương ứng
4Trạng tháiCombobox
Hiển thị ds các trạng thái sau:

Chờ review lần 1

Chờ review lại

Chờ sửa bài

Hoàn thành

Cho phép chọn nhiều trạng thái để tìm kiếm
5SearchBoxTextboxCho phép nhập theo tên/email/số điện thoại để tìm kiếm6Tìm kiếmButtonClick vào sẽ hiển thị danh sách BTVN thỏa mãn đk tìm kiếm7Tổng bài đã nộpLabelTính tổng số bài theo điều kiện tìm kiếm tương ứng8Tổng số bài hoàn thànhLabelTính tổng số bài ở trạng thái Hoàn thành điều kiện tìm kiếm tương ứng11Thông tin học viênLabel
Hiển thị theo format: họ tên - Email - Số điện thoại

Số điện thoại phải gồm 10 ký tự số bắt đầu số 0
12Người chữa bàiLabelHiển thị theo username người chữa bài15Đánh giá bàiIcon
Click vào nút này sẽ mở ra MH đánh giá BTVN của học viên

Icon này chỉ hiển thị khi bài làm về nhà của học viên ở trạng thái : Chờ review lần 1, chờ review lại

### 1.3.Business Rule

 

**Rule**

 

**Chi tiết rule**

 

 

 
Điều kiện tìm kiếm
Tìm kiếm thỏa mãn tất cả các điều kiện nhập vào

Các trường thông tin cần tìm kiếm chính xác:

Khóa học

Lớp học

BTVN

Trạng thái

Các trường tìm kiếm tương đối

Tên hoặc email hoặc số thoại của học viên có chứa dữ liệu tìm kiếm nhập vào

Tìm kiếm theo 1 trong 3 điều kiện sau

Tên chứa dữ liệu tìm kiếm nhập vào

Email chứa dữ liệu tìm kiếm nhập vào

Số điện thoại = dữ liệu tìm kiếm nhập vào
 Sắp xếp
Sắp xếp danh sách theo thứ tự trạng thái như sau

Chờ review lần 1

Chờ review lại

Chờ sửa bài

Hoàn thành

Các bài trogn cùng trạng thái sẽ sắp xếp theo ngày tác động tăng dần
 Màn hình tìm kiếm mặc định
Tìm kiếm theo

Tất cả khóa học

Tất cả lớp học

Tất cả BTVN

Tất cả trạng thái
 
 

## 2.Admin portal -Thiết lập giao BTVN

### **2.1.Mô tả chung**

**Tên UC**

 

**Xem danh sách chữa bài tập về nhà**

 
ActorAdmin, MentorMô tả ý nghĩaCHo phép actor xem danh sách các BTVN của học viên để chữa bài kịp thời
 

### 2.2.Màn hình

 

 

**STT**

 

**TÊn control**

 

**Loại control**

 

**Mô tả / ràng buộc**

 
1Lớp họcLabelHiển thị** mã lớp học** tương ứng2Khóa họcLabelHiển thị tên khóa học - hình thức khóa học3Lịch họcCombobox
Hiển thị các thứ trong tuần

Cho phép chọn nhiều thứ
4Từ ngàyDatePicker
Hiển thị mặc định = Ngày khai giảng của lớp học

và cho phép user được phép sửa lại
5Thời điểm giao bàiCheckboxlist
cho phép cấu hình thời gian giao bài theo 2 TH

Giao bài sau mỗi buổi học

Giao bài sau mỗi tuần học
8Tên BTVNLabel
hiển thị tên BTVN của khóa tương ứng

Hiển thị theo thứ tự đã cấu hình
9THời gian giao bàiDatepicker
Nếu giao bài theo buổi: Hiển thị = ngày học tương ứng +1

 
8Tổng số bài hoàn thànhLabelTính tổng số bài ở trạng thái Hoàn thành điều kiện tìm kiếm tương ứng11Thông tin học viênLabel
Hiển thị theo format: họ tên - Email - Số điện thoại

Số điện thoại phải gồm 10 ký tự số bắt đầu số 0
12Người chữa bàiLabelHiển thị theo username người chữa bài15Đánh giá bàiIconcủa học viên ở trạng thái : Chờ review lần 1, chờ review lại
### 2.3.Business Rule

Thông tin client gửi lên server đối với yêu cầu này

Mã lớp học

Mã BTVN

Thời gian giao bài

Deadline

 

 

 

 

 

 
Theo quy định nghiệp vụKhông có Data thay đổi trong quá trình thực hiện
Mã lớp học tồn tại và đang hoạt động

Mã BTVN: Tồn tại và đang hoạt động
 Data mappingMã BTVN phải thuộc khóa học của lớp học tương ứng Data duplicateKhông có ràng buộc gì 
 

**Rule**

 

**Thông báo nếu không thỏa mãn rule**

 

 

 
Mã lớp học tồn tại và đang hoạt độngLớp học không hợp lệ Mã BTVN: Tồn tại và đang hoạt độngBTVN không hợp lệ Mã BTVN phải thuộc khóa học của lớp học tương ứngBTVN phải thuộc khóa của lớp tương ứng Lưu trữ dữ liệu  
## 3.Web học viên - Nộp bài

### **3.1.Mô tả chung**

**Tên UC**

 

**Nộp bài**

 
ActorHọc viênMô tả ý nghĩaCho phép học viên nộp bài tập về nhà
### 3.2.Màn hình

 

**STT**

 

**Tên control**

 

**Loại control**

 

**Require**

 

**Mô tả /ràng buộc khác**

 
1BTVNTextboxYes
Hiển thị tên BTVN mà học viên muốn nộp

Không cho phép sửa
2Link bài làmTextboxYes
Học viên nhập link bài làm tương ứng

Maxlength: 100

Format nhập liệu là dạng URL
3Ghi chúTextboxNo
Cho phép nhập ghi chú để mentor đọc và lưu ý

Maxlength: 200

 

### **3.3.Business Rule**

Thông tin gửi lên server

ID BTVN

Link bài làm

Note

UserID

Xác định rule

**Nhóm rule**

 

 

 

 

 
Rule quy định nghiệp vụNgày hiện tại<=deadline của bài tập tương ứng gán cho lớp Rule data thay đổi/Gửi lên tool
UserID tồn tại và đang hoạt động trên hệ thống

ID BTVN tồn tại và đang hoạt động trên hệ thống
 Rule data mappingBTVN tương ứng phải được gán cho lớp của học viên Rule data duplicateVới mỗi BTVN học viên chỉ được nộp 1 lần duy nhất Rule hiển thị xác nhận  
\

**Rule cần thỏa mãn**

 

**Thông báo lỗi nếu không thoải mãn rule**

 
Ngày hiện tại<=deadline của bài tập tương ứng gán cho lớpĐã hết hạn nộp bài
UserID tồn tại và đang hoạt động trên hệ thống

 
Thông tin không hợp lệID BTVN tồn tại và đang hoạt động trên hệ thốngTHông tin không hợp lệBTVN tương ứng phải được gán cho lớp của học viênThông tin không hợp lệVới mỗi BTVN học viên chỉ được nộp 1 lần duy nhấtBạn chỉ nộp 1 lần duy nhất