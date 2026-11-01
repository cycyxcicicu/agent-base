---
id: 176
title: "Quản lý nghiệp vụ test"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-06-29T13:17:20.000Z"
source_url: "https://m2mba.com/blog/articles/e7c0e591-703c-4220-8135-da33acfed679"
---

# Quản lý nghiệp vụ test

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-06-29T13:17:20.000Z*

## 1.Quy trình nghiệp vụ

## 2.Một số khái niệm/định nghĩa cơ bản
**Khái niêm/định nghĩa****Giải thích chi tiết**Câu hỏi
Mỗi câu hỏi sẽ được soạn trên editor để thuận tiện cho việc linh hoạt đề bài

Chia làm 2 loại câu hỏi

**Câu hỏi nhóm**: Là các câu hỏi có cùng chung ngữ cảnh đề bài, sau đó admin sẽ ra các câu hỏi từ ngữ cảnh đề bài đó. Câu hỏi theo nhóm phải hiển thị theo đúng thứ tự như lúc tạo câu hỏi

**Câu hỏi đơn lẻ**: Là câu hỏi độc lập, các câu hỏi đơn lẻ khi hiển thị trong bài test có thể hiển thị ở bất cứ vị trí nào trong danh sách câu hỏi của bài test

Mỗi câu hỏi sẽ có đáp án dạng trắc nghiệm hoặc tự luận
Chủ đề câu hỏi
Mỗi câu hỏi sẽ được gán với 1 chủ đề nào đó, ví dụ chủ đề về Khơi gợi yêu cầu, hay chủ đề về xác định UC

Mỗi câu hỏi có thể có 2 chủ đề: Chủ đề cha, chủ đề con

Danh sách chủ đề cha, con do admin tạo trên danh mục - cái này sẽ cần làm nhưng làm sau
Bài test publicLà bài test mà ai cũng có thể view, miễn là có user trên hệ thốngKết quả đánh giá
Mỗi bài test sẽ được setup kiểu đánh giá theo danh mục kiểu đánh giá đã tạo sẵn, có thể có các kiểu đánh giá như sau

**Pass/fail**: Có nghĩa thiết lập bao nhiêu điểm thì pass, bao nhiêu điểm sẽ fail

**Xuất sắc/Tốt/Khá/Trung bình:** Thiết lập bao nhiêu điểm thì đạt các mức tương ứng

…

Danh mục kiểu đánh giá sẽ do admin tạo (có thể insert thẳng DB thời gian đầu)
Chấm điểm
Với bài trắc nghiệm mà có nhiều đáp án đúng thì nếu đúng là phải chọn 3 câu, mà học viên chỉ chọn 2 câu thì sẽ được 2/3 số điểm của câu hỏi đó

Và khi đó kết quả câu trả lời của học viên sẽ có các TH: Đúng, Sai, Đúng 1 phần
Gán bài test
Có thể gán theo khóa học, lớp học

Không gán đến chi tiết từng học viên

## 3.ERD

 

 

## 4.Biểu đồ trạng thái

**Biểu đồ trạng thái bài làm học viên**

 

 

 

## 5.Danh sách chức năng

## [5.1.Web](http://5.1.Web) admin
**Chức năng****Mô tả****Mức độ ưu tiên**CRUD đối tượng Trung bìnhCRUD Chủ đề Trung bìnhCRUD câu hỏi CaoCRUD bài test CaoDanh sách bài làm của học viên CaoXem chi tiết bài làm của học viên CaoChấm điểm câu hỏi tự luận Cao   
## [5.2.Web](http://5.2.Web) học viên
**Chức năng****Mô tả****Mức độ ưu tiên**Danh sách bài test của tôi CaoLàm bài test CaoXem lịch sử làm bài Cao (chị chưa có MH - sẽ tạo sau)Xem chi tiết bài làm Cao (Chưa có MH)
## 6.Một số màn hình chính

## **6.1.Admin portal - Danh sách Ngân hàng câu hỏi**

 

 

## 6.2.**.Admin portal - **Thêm mới câu hỏi

**Câu hỏi nhóm :** FLow : Tích chọn Câu hỏi nhóm=>hiển thị editor để nhập ngữ cảnh câu hỏi=>Tạo các câu hỏi trong câu hỏi nhóm, Nếu câu hỏi cuối thì nhấn nút Lưu thì coi như kết thúc list câu hỏi của câu hỏi nhóm đó. Mỗi câu hỏi sẽ được lưu ngay khi tạo, ko phải đến khi ấn nút Lưu mới lưu vào DB

- Nếu câu hỏi trắc nghiệm thì sẽ cần phải tích chọn đáp án đúng tối thiểu 1 câu
- Nếu câu hỏi tự luận: Đáp án có thể tạo ngay lúc đó hoặc để sau (đáp án ko bắt buộc nhập ngay)
 

 

 

**Câu hỏi đơn lẻ**

 

 

 

## 6.3.Admin portal - Danh sách bài test, Gán bài test, Thiết lập xếp loại

 

 

 

- Tổng số học viên: Là bài test này được gán cho bao nhiêu học viên được phép làm bài đó, Có các hành động đi kèm:
- Xem chi tiết bài test (Cái này e tự thiết kế MH nhé): hiển thị chi tiết bài test (thông tin cơ bản, danh sách câu hỏi, các lớp/khóa dc gán, thông tin thiết lập xếp loại: Trong này các thông tin đều có thể sửa được
- Danh sách câu hỏi: Có thể xóa câu hỏi ra khỏi ds
- Các lớp/khóa học đc gán: Có thể xóa khỏi danh sách, và có nút để gán bài test =>Sẽ mở ra MH của UC gán bài test
- Thiết lập xếp loại: Có thể sửa được
- Gán bài test (gán theo lớp, theo khóa: Gán bài test cho lớp học hoặc khóa học nào đóNếu chọn lớp thì hiển thị ds lớp đang ở trạng thái hoạt động và khác chờ khai giảng
- nếu chọn Khóa thì thiển thị ds các khóa đang hoạt động
- Có thể gán (nếu chưa gán thì hiển thị icon gán) hoặc bỏ gán ds các lớp/khóa hiện tại (nếu đã gán thì hiển thị icon bỏ gán)
Click vào icon gán bài test thì sẽ hiển thị ra MH

 

 

**Thiết lập xếp loại: **Thiết lập tiêu chí xếp loại, bao nhiêu điểm thì đạt mức nào

 

 

## 6.4.Admin portal - Tạo mới bài test

**Flow:** Tạo thông tin cơ bản của bài test và ấn Lưu=>Hiển thị chi tiết bài test=>Chọn add câu hỏi vào bài test=>hiển thị MH tìm kiếm câu hỏi trong NH câu hỏi=>Chọn câu hỏi để add (có thể add đơn lẻ hoặc tích chọn và add theo list)

**MH tạo bài test**

 

 

**MH chi tiết bài test**

- Với mỗi câu hỏi thì hiển thị các thông tinLoại câu hỏi nhóm hay không
- Chủ đề cha, chủ đề con : Nếu câu hỏi nhóm thì không hiển thị bên ngoài ngữ cảnh câu hỏi mà chỉ hiển thị chi tiết bên trong. Nếu không có chủ đề con thì không hiển thị
- Được phép xóa câu hỏi ra khỏi ds
- Được phép chỉnh sửa câu hỏi (chỉnh sửa ở đây sẽ chỉnh sửa luôn ở NH câu hỏi)
- nếu **câu hỏi nhóm **thì hiển thị:Câu hỏi X-Y (trong đó X là thứ tự của câu hỏi này trong ds bài test, Y=X+số câu hỏi trong câu hỏi nhóm đó -1)
- Số điểm của mỗi câu hỏi sẽ được chỉnh sửa tùy theo nhu cầu của Admin (nhưng ko ảnh hưởng điểm trong NH câu hỏi)
 

 

 

**MH search câu hỏi trong NH câu hỏi**

- Nếu câu hỏi đã add vào bài test thì hiển thị Added, Ngược lại hiển thị Button Add
- Có thể tick chọn vào các câu hỏi (Chưa add) để add 1 loạt theo ds)
- Hiển thị số câu hỏi đã có trong bài test, và tổng điểm tối đa của bài test
 

 

## 6.5.Admin portal - Danh sách kết quả bài làm học viên

Có icon xem chi tiết bài làm và icon duyệt điểm

Icon duyệt điểm chỉ có khi bài test đó cần duyệt và ở trạng thái chờ admin duyệt điểm

 

 

## 6.6.Xem chi tiết bài làm của học viên

- Hiển thị kết quả tạm tính (tính tổng điểm của các câu hỏi dc mentor hoặc hệ thống tự chấm)
- Hiển thị mỗi trạng thái câu hỏi: Đúng/Sai/Đúng 1 phần. Nếu chưa trả lời thì hiển thị icon thể hiện là học viên ko làm (e tự nghĩ hộ c nhé)
- Cho phép filter theo loại câu hỏi tự luận hay câu trắc nghiệm
- Với câu hỏi tự luận: Cho phép mentor chấm điểmNhập số điểm: Điểm không được vượt quá số điểm quy định của câu đó
- Nhập đúng, sai hay đúng 1 phần (e tráo thứ tự hộ c cái nhé, viết mới thấy logic vẽ chưa đúng):Nếu chọn sai thì 0 điểm
- Nếu chọn đúng thì tối đa điểm
- Nếu chọn đúng 1 phần thì, mentor nhập số điểm
- Nhập comment thêm nếu có (không bắt buộc)
 

## 6.7. Web học viên - Bài test của tôi

## [6.8.Web](http://6.8.Web) học viên - làm bài test

**với dạng câu hỏi nhóm: **Ngữ cảnh được giữ nguyên, chỉ thay đổi các câu hỏi trong câu hỏi nhóm đó