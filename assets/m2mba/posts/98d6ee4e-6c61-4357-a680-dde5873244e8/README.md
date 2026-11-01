---
id: 112
title: "Web học viên - Chi tiết yêu cầu"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-25T04:12:01.000Z"
source_url: "https://m2mba.com/blog/articles/98d6ee4e-6c61-4357-a680-dde5873244e8"
---

# Web học viên - Chi tiết yêu cầu

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-25T04:12:01.000Z*

## 1.[Website học viên]Xem danh sách khóa học

### 1.1.Màn hình

## 1.2.Mô tả màn hình
**STT****Tên control****Mô tả**1Tên khóa học 2Hình thức khóa học 3Thời lượng khóa họcHiển thị theo thông tin khóa học theo dạng: <Số giờ> - <số> buổi4Học phíHọc phí hiện tại của khóa học đó5Số lượng học viênSố lượng học viên đã đăng ký học6,7Thông tin tuyển sinh
Nếu đang có lớp tuyển sinh cho khóa tương ứng thì hiển thị số lớp đang tuyển, tổng số slot đang còn của các lớp đó

Ngược lại hiển thị Chưa mở tuyển sinh

Rule tính lớp tuyển sinh theo khóa học:

Lấy danh sách các lớp thuộc khóa học tương ứng thỏa mãn

Trạng thái active

Có thời gian tuyển sinh>=thời gian hiện tại và thời gian hiện tại<=ngày khai giảng khóa học

Số lượng đã tuyển sinh<Số lượng tối đa

## 2.[Website học viên] - Xem chi tiết khóa học

### 2.1.Màn hình

### 2.2.Mô tả màn hình
**STT****Tên control****Mô tả****Mapping bảng DB  (ko cần mô tả nhưng nên biết)**1Tên khóa họcHiển thị theo dạng: <Tên khóa học> - <Hình thức khóa học>Course2Lớp tuyển sinhChứa ds các lớp đang tuyển sinh của khóa học đang xem 3Học phíhọc phí của khóa họcCourse4Đối tượng phù hợpĐối tượng phù hợp của khóa họcCourse5Nội dung khóa họcNội dung khóa họcCourse6Giảng viênHiển thị thông tin giảng viên của khóaCourse7Số slot còn lại
Hiển thị theo dạng:

Số slot còn lại/Tổng số slot tối đa của lớp đó

Slot còn lại =Tổng slot tối đa của lớp - tổng số đã đăng ký (và đã ck)
Class.Registermax - Class.Register8Đăng kýChỉ hiển thị nút này khi đang còn slot và Ngày khai giảng >=Ngày hiện tại và Ngày tuyển sinh<=Ngày hiện tại 9Đăng ký nhận thông báoClick vào đây sẽ hiển thị nút Đăng ký nhận thông báo 
## 2.3.Biz Rule

- Lấy ra danh sách các lớp thỏa mãn rule sauCác lớp của khóa học hiện tại và ở trạng thái Active
- Thời gian tuyển sinh<=ngày hiện tại
- Sắp xếp theo order sau**Lớp đang tuyển sinh** (là lớp còn slot và thời gian khai giảng >=thời gian hiện tại): Sắp xếp theo thời gian ngày khai giảng tăng dần
- **Lớp không tuyển sinh **(là lớp không còn slot và thời gian khai giảng <thời gian hiện tại): Sắp xếp theo thời gian khai giảng giảm dần
## 3.[Website học viên] - Đăng ký khóa học

### 3.1.User flow

### 3.2.Màn hình

Từ màn hình Danh sách lớp tuyển sinh, click vào Nút Đăng ký, hiển thị popup

## 3.3.Mô tả màn hình
**STT****Tên control****Mô tả**1Đăng ký
Click vào button đăng ký thì hiển thị Popup xác nhận đăng ký khóa học.

Chọn “Đăng ký” → Chuyển sang màn hình “Đăng ký giữ chỗ thành công”

Chọn “Hủy” → Quay lại màn hình danh sách lớp tuyển sinh
2Xác nhận đăng ký khóa học
“Bạn có chắc chắn đăng ký lớp học ON062023 không?”

Trong đó “ON062023” là tên lớp học
3Thông báo thời hạn đóng học phí
“Vui lòng thanh toán học phí trước dd/mm/yyyy hh24:mi theo thông tin sau:”

Trong đó: “dd/mm/yyyy hh24:mi” là thời hạn đóng học phí để được giữ chỗ. .
4Mã QR thanh toán học phíMã QR để học sinh quét mã đóng học phí.5Học phíSố tiền học phí lớp học đó. VD: “5.000.000đ”6Chủ tài khoảnChủ tài khoản học sinh cần thanh toán học phí là: Đậu Thị Ngọc Ánh7Số tài khoảnSố tài khoản học sinh cần thanh toán học phí8Ngân hàngNgân hàng của tài khoản học sinh cần thanh toán học phí9Nội dung chuyển khoảnNội dung chuyển khoản tương ứng với từng học viên
 

## 3.4.Activity diagram và mô tả luồng

**Mô tả luồng**
**Bước****Mô tả****Bảng dữ liệu liên quan**4
Kiểm tra điều kiện đăng ký của học viên

Học viên chưa đăng ký lớp hiện tại của khóa học đó - Độ ưu tiên 1

Hoặc đã đăng ký nhưng ở trạng thái Đã hủy - Độ ưu tiên 1

Lớp học đang còn slot: Số đã đăng ký ở trạng thái Đăng ký thành công<số lượng tối đa - Độ ưu tiên 2

Lớp học phải tồn tại và ở trạng thái chờ khai giảng

Bảng Lịch sử đăng ký

Ko có thông tin đăng ký học viên đó với khóa học tương ứng từ ngày hiện tại - 1 năm đến hiện tại

hoặc có nhưng ở trạng thái Đã hủy

Lưu ý: Lọc theo khóa học, không tính theo lớp học=>nếu học viên đã học 1 năm rồi, muốn đăng ký lại thì cho đăng ký, còn trong vòng 1 năm thì cho vào dự thính lại (ở UC đăng ký dự thính - sẽ làm sau)
5
Hiển thị thông báo lỗiATH như sau:

Học viên đã đăng ký và chưa hủy:** Bạn đã đăng ký khóa học trước đó. Vui lòng thanh toán để hoàn thành việc đăng ký**

Lớp đã hết slot: **Số lượng đăng ký đã đạt tối đa. Cám ơn bạn đã quan tâm tới khóa học, bạn có thể theo dõi và đăng ký khóa học tiếp theo**

Lớp học ở trạng thái không hợp lệ: **Lớp học đang không tuyển sinh. Vui lòng chọn lớp khác**

 
6
Lưu thông tin đăng ký của học viên với trạng thái Chờ thanh toán

Mã đăng ký sinh theo rule: <mã lớp học>yymmddxx ,yymmdd là ngày hiện tại, XX là số thứ tự đăng ký của học viên này trong khóa học

Thời hạn giữ chỗ = Thời gian hiện tại + thời gian cấu hình cho phép giữ chỗ (có thể thay đổi theo từng thời kỳ)

Bảng Lớp học

tăng số lương đăng ký của lớp học hiện tại lên 1 =

 
7Gửi email cho Học viên hướng dẫn đóng học phíLấy email của học viên trong bảng user để gửi email cho học viên, nội dung email sẽ gửi lại sau
## 4. [Website học viên] - Đăng ký/Đăng nhập/Reset mật khẩu

## 4.1. Màn hình

### 4.2.Ràng buộc

- **Chức năng Đăng ký**Họ tên:Minlength=3,Maxlength: 100
- Chỉ nhập ký tự chữ và blank
- Bắt buộc nhập
- EmailĐúng định dạng email (e tự tìm rule trên mạng nhé)
- Bắt buộc nhập
- Số điện thoạiBắt buộc nhập
- Bắt đầu bằng 0, gồm 10 ký tự số
- Email / số điện thoại bắt buộc phải duy nhất, nếu chỉ 1 trong 2 đã tồn tại thì báo lỗi: Email/Số điện thoại đã được đăng ký trước đó. Vui lòng kiểm tra lại
- Mật khẩu tối thiểu 6 ký tự (lưu ý trim xâu): Mật khẩu cần được mã hóa lưu trong DB
- **Chức năng Đăng nhập:** check email/số điện thoại tồn tại trên hệ thống và mật khẩu khớp với thông tin email/sđt
- **Chức năng Reset mật khẩu:** Hiển thị màn hình nhập email, sau đó hệ thống validate email tồn tại và sinh mật khẩu gửi lại cho KH, mật khẩu sinh ký tự ngẫu nhiên
## 5.  [Website học viên] - Quản lý user - Xem chi tiết/cập nhật tài khoản

### 5.1.Màn hình

### 5.2.Mô tả màn hình
**Trường thông tin****Mô tả yêu cầu**Họ tên
Bắt buộc nhập

Chỉ được nhập ký tự aA-zZ và blank
Số điện thoại
Bắt buộc nhập

Nhập 10 ký tự số, bắt đầu bằng 0
email
Bắt buộc nhập

Nhập đúng theo tiêu chuẩn email (dev tự lấy trên mạng)
Mật khẩu
Hiển thị mặc định là các ký tự sao như hình

User có thể nhập để đổi mật khẩu (không có ràng buộc về mật khẩu)

Mật khẩu lưu trên DB cần mã hóa

Mật khẩu nếu thay đổi : phải nhập tối thiếu 6 ký tự
Nghề nghiệpĐược phép chọn từ danh mục nghề nghiệp đang hoạt động trên hệ thống 
### 5.3. Ràng buộc nghiệp vụ

Email/số điện thoại là duy nhất trên hệ thống

Nếu user nhập email chưa tồn tại nhưng số điện thoại đã tồn tại thì cũng sẽ bị báo lỗi: Thông tin email/số điện thoại đã tồn tại trên hệ thống. Vui lòng kiểm tra lại

## 6. [Website học viên] - Đăng ký bảo lưu

### 6.1.Màn hình

### 6.2.Mô tả màn hình

**Tên control**

 

**Ràng buộc**

 

**Mô tả**

 
Danh sách lớpKhông bắt buộc chọn
Hiển thị lớp học thỏa mãn tiêu chí sau

Lớp thuộc khóa học mà học viên đã đăng ký (ví dụ ON hay khóa OFF)

Ở trạng thái Active

Ngày bắt đầu>ngày hiện tại

Và không hiển thị lớp mà học viên đã đăng ký

Sắp xếp theo thứ tự thời gian khai giảng tăng dần

hiển thị dữ liệu trong combobox theo dạng: xem ảnh ở trên

### [6.3.Biz](http://3.biz/) Rule

- Chỉ được đăng ký bảo lưu tối đa 3 lần : Chỉ tính các lần chọn lớp
- Và thời gian hiện tại <=Thời gian đăng ký khóa học gốc + 1 năm
- Thời gian hiện tại <=thời gian bắt đầu lớp học +35 ngày
- Biểu đồ luồng dữ liệu
 

## 7.[Website học viên] - Xem đánh giá kết quả

Mapping trường với Bảng Đánh giá học viên (trong [ERD](https://m2mba.atlassian.net/wiki/spaces/QLTTOT/pages/393229))

 

- Nếu Trạng thái public = 0 thì hiển thị nút Public Đánh giá trên website
- Ngược lại thì hiển thị nút Unpublic Đánh giá trên website
## 8. [Website học viên] - Danh sách khóa học đăng ký

### 8.1 Màn hình

### 8.2.Mô tả màn hình

**STT**

 

**Tên control**

 

**Mô tả**

 
1Icon xem chi tiếtClick vào sẽ mở màn hình chi tiết thông tin đăng ký khóa học2Xem thông tin thanh toán
Click vào sẽ hiển thị màn hình QR chứa thông tin thanh toán

Chỉ hiển thị khi ở trạng thái Chờ thanh toán
3Bảo lưu khóa họcChỉ hiển thị khi ở trạng thái Đang bảo lưu, Đang học, Đăng ký thành công4Xem bản đánh giáChỉ hiển thị khi đã hoàn thành khóa học và đã có cert5Join nhóm Zalo
Chỉ hiển thị khi khác trạng thái Hủy và chờ thanh toán

Sẽ thực hiện zen QR code là URL của link zalo của lớp học hiện tại của học viên

Lấy trong bảng class, với lớp hiện tại của học viên. Nếu lớp hiện tại bằng rỗng thì hiển thị báo lỗi: Bạn chưa chọn lớp học nên chưa có thông tin link lớp học!

 

### 8.3. Ràng buộc

Sắp xếp theo thời gian đăng ký giảm dần theo thời gian

 

## 9. [Website học viên] - Xem thông tin QR thanh toán

### 9.1.Màn hình

### 9.2. Mô tả màn hình

**STT**

 

**Tên control**

 

**Mô tả**

 
1Ảnh QRẢnh QR thanh toán: Chứa thông tin TK của stk2Học phíSố tiền học phí cần đóng3Tên chủ TKTên chủ TK4Số TKSố TK5Ngân hàngNgân hàng của số tài khoản6Mã đăng kýMã đăng ký khóa học
### 9.3. Quy tắc sinh ảnh QR

Tài liệu đặc tả (Mục 6.1.3): [https://vietqr.net/portal-service/download/documents/QR_Format_T&C_v1.0_VN_092021.pdf](https://vietqr.net/portal-service/download/documents/QR_Format_T&C_v1.0_VN_092021.pdf)

Dev không cần đọc tài liệu đặc tả ở trên, chỉ cần làm các bước sau:

**Bước 1**: Nhìn ở các đoạn text bôi đỏ

**00020101021238570010A00000072701270006970422011300501095020030208QRIBFTTA5303704540750000005802VN62100806353454**63042E73

 

**Ví dụ dữ liệu**

 

**Mô tả cách tạo**

 
**54075000000**
1.Lấy số tiền học phí cần nộp, tính ra chiều dài của số tiền học phí, ví dụ 5tr thì chiều dài là 7 ký tự, 500.000 thì chiều dài là 6 ký tự

2.sau đó tạo ra đoạn text

54[length][học phí]

ví dụ ở bên là 54075000000
**62100806353454**
1.Lấy mã đăng ký của học viên (registerID)

2.Tính length của mã đăng ký

sau đó tạo ra đoạn text

08[length][mã đăng ký]

**0806353454**

3.Tính length được tạo ra ở bước 2, ví dụ ở trên là 10

4.Tạo đoạn text

62[length ở bước 3][đoạn text ở bước 2]

ví dụ này là : **62100806353454**

**Bước 2**: Sau đó thực hiện chèn các đoạn text này vào chuỗi ở trên (phần nào bôi đen sẽ không cần chỉnh sửa gì)

**Bước 3**: Tạo ra ảnh QR tương ứng với đoạn text được sinh ra

 

## 10. [Website học viên] - Xem chi tiết khóa học đã đăng ký

### 10.1. Màn hình

### 10.2.Mô tả màn hình

**STT**

 

**Tên control**

 

**Mô tả**

 
1Trạng thái đăng ký khóa họcHiển thị trạng thái của bản ghi đăng ký khóa học của Học viên2Ngày hủyChỉ hiển thị khi ở trạng thái Hủy, hiển thị theo định dạng dd/mm/yyyy hh24:mi:ss3Người hủy
Nếu hệ thống hủy thì hiển thị: Hệ thống

Ngược lại hiển thị username của user hủy
4Lý do hủyHiển thị lý do hủy (trường note trong bảng đăng ký)5Thông tin của lớp hiện tại
Hiển thị lớp gần nhất mà user liên quan

Nếu user đã bảo lưu (tính lần bảo lưu gần nhất) thì lớp bảo lưu gần nhất (nếu có)

Nếu user bảo lưu (tính lần gần nhất) nhưng chưa chọn lớp thì hiển thị : Chưa có thông tin lớp hiện tại

Nếu user chưa bảo lưu thì hiển thị lớp mà học viên đăng ký
6Trạng thái của lớp hiện tại
Có các trạng thái sau:

Chưa bắt đầu: Ngày khai giảng > ngày hiện tại

Đang học: nếu lớp đang ở trạng thái Đang học

Hoàn thành: Nếu lớp đang ở trạng thái Hoàn thành
7Thông tin bảo lưuHiển thị ngày đăng ký bảo lưu và lớp sẽ học8Đăng ký bảo lưuClick vào đây sẽ mở màn hình Đăng ký bảo lưu
## 11. [Website học viên] - Tra cứu đánh giá học viên

### 11.1.Màn hình

**MH tra cứu thì học viên đã có đánh giá và cho phép public đánh giá**

**MH tra cứu thì học viên đã có đánh giá và không cho phép public đánh giá, hoặc chưa có đánh giá**

### 11.2.Mô tả màn hình

**STT**

 

**Tên control**

 

**Mô tả**

 
1Email/sđt
User nhập emai/sdt để tìm kiếm

cần tìm kiếm chính xác thông tin
2Khóa học
Sau khi nhập email/sđt, hệ thống thực hiện tìm kiếm khóa học theo thông tin nhập vào

Tìm kiếm chính xác theo email/sđt

Tìm kiếm trong bảng học viên theo lớp
3Tra cứuClick vào nút này sẽ thực hiện tìm kiếm đánh giá của học viên theo khóa học tương ứng4Thông tin khi chưa có đánh giáKhi chưa có đánh giá hoặc ko cho phép view đánh giá sẽ chỉ hiển thị các thông tin như hình
### 11.3. **Mô tả ràng buộc**

- Bảng dữ liệu: Đánh giá học viên, Học viên theo lớp
- Tìm kiếm theo Email hoặc số điện thoại: cả 2 đều tìm kiếm chính xác
- Nếu is_public=1: Hiển thị full thông tin đánh giá 
- Nếu is_public =0 hoặc chưa có đánh giá thì sẽ hiển thị các thông tinChỉ hiển thị các thông tin như hình
- hiển thị trạng thái hiện tại của học viên theo lớp học
- Nếu không tìm thấy bản ghi nào thì hiển thị: Không tìm thấy kết quả mong muốn