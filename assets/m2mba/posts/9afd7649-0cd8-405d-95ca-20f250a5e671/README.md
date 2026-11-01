---
id: 110
title: "Tài liệu phân tích tổng quan  (Với dự án chạy mới hoàn toàn)"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-25T03:31:23.000Z"
source_url: "https://m2mba.com/blog/articles/9afd7649-0cd8-405d-95ca-20f250a5e671"
---

# Tài liệu phân tích tổng quan  (Với dự án chạy mới hoàn toàn)

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-25T03:31:23.000Z*

## **1.Giới thiệu chung**

Hiện tại, Trung tâm đào tạo BA đã triển khai được 3 năm, với số lượng học viên khá đông. Nhiều công việc trong quá trình vận hành phải thực hiện thủ công, và dạo gần đây đã phát sinh ra nhiều vấn đề, ảnh hưởng đến cả Trung tâm và Học viên

Do đó, Trung tâm nhận thấy cần xây dựng phần mềm để quản lý vận hành cho trung tâm, và lâu dài cũng có thể đưa sản phẩm đi kinh doanh, bán cho các bên quản lý đào tạo dạng cá nhân, có mô hình tương tự như bên trung tâm hiện tại đang làm

## **2.Mô hình tổ chức của trung tâm**

Hiện tại trung tâm chỉ có các thành phần sau

Quản lý trung tâm: 1 Người - Chị Ánh

Mentor: Mentor tham gia vào việc giảng dạy cũng như chữa bài trong trung tâm: Chị Ánh - Chị Ngọc

Trợ giảng: Đang dự kiến có khoảng 5 trợ giảng - hỗ trợ học viên thực hành trong các buổi dạy offline

Trợ lý (chưa có): Dự kiến 1 người, sẽ hỗ trợ việc trực page, giải đáp cho học viên, chuẩn bị hậu cần công việc của lớp học

## 3.Phân tích quy trình

### 3.1.Quy trình tổng quan

**Tình huống phát sinh**

 

**Quy trình phát sinh**

 
Học viên bảo lưu khi không có thời gian để theo tiếp khóa học hiện tạiQuy trình bảo lưu
### 3.2.Quy trình tuyển sinh

#### 3.2.1.Quy trình hiện tại
**Bước 1****Người thực hiện****Mô tả****Thủ công/Hệ thống**1AdminAdmin thực hiện tạo nhóm quan tâm khóa học trên zalo/ facebook và nhóm tham gia khoá học chính thức trên zaloThủ công2Admin
Đăng bài tuyển sinh gồm các nội dung:

Tên khoá học, thời gian, địa điểm

Hình thức học và chi phí

Đối tượng phù hợp

Nội dung khóa học và quy định

Link nhóm zalo quan tâm khóa học

Thủ công

 
3Học viênĐọc kỹ các thông tin tuyển sinh và tham gia vào nhóm zalo được chia sẻThủ công4Admin
Gửi thông tin đăng ký khoá học vào nhóm:

Số tài khoản, nội dung chuyển khoản (Họ tên - Số điện thoại - ON/OFF, ứng với khóa ON/OFF), số tiền

Form khai thông tin: [Thông tin học viên khóa học BA](https://docs.google.com/forms/d/1mHx2UdUJ-o0aAd5wEOMY-dpAhHMy-H70FVnHMW1dvTs/edit)

Link nhóm zalo khoá học
Thủ công5Học viênChuyển khoản học phí sau đó điền thông tin vào link form rồi tham gia nhóm lớp , và request vào lớp học chính thứcThủ công6Admin
Xác nhận đóng học phí

Admin thực hiện check SMS để lọc số điện thoại ra tên lớp, số tiền

Admin tiếp tục so khớp với danh sách mà học viên đăng ký trên gg form

Nếu khớp thì thực hiện cập nhật trạng thái đóng học phí
Thủ công7Admin
Chia sẻ tài liệu và duyệt vào nhóm zalo

**Chia sẻ tài liệu**

Lọc danh sách email của các bạn đã đóng học phí và chưa được share tài liệu

Thực hiện tạo list email cần share

Vào youtube share theo list video của khóa hiện tại

**Duyệt vào nhóm zalo**

Duyệt thành viên dựa vào số điện thoại của học viên khai báo lúc request vào nhóm
 8AdminGửi hướng dẫn tự học và tài liệu cho học viên Thủ công
#### 3.2.2.Các vấn đề bất cập

**Thông tin**

 

**Hiện trạng**

 

**Vấn đề**

 

**Mong muốn xử lý**

 

**Nội dung thay đổi**

 
Học viên muốn tham gia khóa học
Học viên like và theo dõi fanpage để cập nhật các bài post, inbox hỏi admin về khóa học

Tham gia nhóm quan tâm khóa học để nhận thông tin đăng ký

 
Học viên thường bị miss thông tin đăng ký khoá học
-Học viên có thể xem được thông tin và đăng ký khóa học trực tiếp trên web

-Đăng ký thông tin email để nhận thông báo đăng ký khóa học

 

Xây dựng website cho phép KH chủ động đăng ký khóa học nếu như đang có đợt tuyển sinh

Ngược lại, nếu đang chưa có đợt tuyển sinh, cho phép học viên để lại email để nhận thông tin nhanh nhất khi có đợt tuyển khóa học tương ứng

Tuyển sinh - xác nhận đóng học phí

Share tài liệu, share video cho học viên

Khi học viên đóng học phí, học viên sẽ cần phải khai form do trung tâm yêu cầu [Thông tin học viên khóa học BA](https://docs.google.com/forms/d/1mHx2UdUJ-o0aAd5wEOMY-dpAhHMy-H70FVnHMW1dvTs/edit)

Sau đó admin của Trung tâm sẽ check SMS biến động số dư (ND biến động Họ tên - Số điện thoại - ON/OFF, ứng với khóa ON/OFF), và thông tin khai trên form của học viên, để xác nhận học viên đóng học phí

Sau khi xác nhận xong, Admin sẽ lấy danh sách email để share tài liệu trên google driver và share private 20 video trên kênh youtube (các video này được nhặt từ 1 khóa học nào đó)

Và duyệt vào nhóm zalo

Việc check tin nhắn và mapping khá mất thời gian, và nếu học viên quên khai form thì sẽ không có thông tin để confirm, và cũng ko biết bạn nào quên khai form

Và việc share video trên youtube, dễ share sót do nhặt các video từ 1 khóa học nào đó, hiện tại rất hay nhận đc tin từ học viên về việc sót các video. Khi đó admin phải nhờ học viên chụp ảnh lại danh sách video mà học viên thấy, để từ đó tìm ra video thiếu

Việc duyệt vào nhóm thường yêu cầu học viên nhập thêm họ tên/SĐT. Tuy nhiên khi thực hiện request trên máy tính thì ko có chỗ để học viên nhập (zalo đang như vậy)

Cho phép học viên đăng ký trên website, thay vì nhập thông tin trên form

Học viên có thể thanh toán CK hoặc thanh toán online

Tất cả tài liệu được quản lý trên hệ thống, ko phân tán ở các nơi

Nhưng sẽ chia thành các giai đoạn như sau

GD1:

Thanh toán: Tạm thời ưu tiên thanh toán Ck trước, do thanh toán online có nhiều thủ tục phức tạp + phí thu trên từng GD=>Phí này có thể trả cho 1 trợ lý chuyên phụ trách các công việc khác của trung tâm =>Nên chưa cần thiết làm Thanh toán online

Share tài liệu: Và sau khi đăng ký và ck thành công, hệ thống sẽ tự động share tài liệu trên google driver và share video trên youtube

**GD2**

Tích hợp thanh toán online

Tài liệu được upload toàn bộ trên nền tảng của trung tâm

Xây dựng website cho KH đăng ký

Xây dựng chức năng cho đội admin có thể xác nhận thanh toán

sau khi xác nhận thanh toán xong thì hệ thống tự động share tài liệu trên gg driver, youtube

và add vào nhóm zalo
          
#### 3.2.3.Quy trình đề xuất

## 3.3.Quy trình bảo lưu khóa học

#### 3.3.1.Quy trình hiện tại

#### 3.3.2.Vấn đề găp phải

**Thông tin**

 

**Hiện trạng**

 

**Vấn đề**

 

**Mong muốn xử lý**

 
Việc lọc học viên có phải đã từng đăng ký học không
Dựa vào thông tin học viên khai trong gg form bảo lưu (Họ tên, sđt, khóa học đăng ký)

sau đó admin sẽ mở danh sách khóa học mà học viên đăng ký, để check xem học viên có trong danh sách không
Học viên có thể không nhớ chính xác mình đăng ký khóa nào=>Nhập sai thông tin=>Admin không check đượcHọc viên đăng ký bảo lưu trên hệ thống, hệ thống sẽ track được thông tin liên quan tới học viên: Đăng ký khóa nào, đã bảo lưu sang những khóa nào, đã tham gia học đến buổi nào trong khóa (dựa vào BTVN)Học viên bảo lưu quá nhiều lần, quá hạn quy địnhHiện tại không kiểm tra thông tin này, nên học viên muốn bảo lưu bao lâu cũng được,Học viên có thể bảo lưu sau đó cấp mail cho người khác thì có thể học trong nhiều khóa khác nhauKiểm tra học viên đã làm BTVN tuần nàoGần như không kiểm tra, do học viên có thể bảo lưu bất cứ lúc nào trong khóa học, và bảo lưu bao nhiêu khóa cũng được, nên việc dò lại rất khó
Học viên có thể làm bài nhiều lần

có thể cấp mail cho bạn khác học và được chữa bài cho các bạn khác đó

#### 3.3.3.Quy trình đề xuất

### 3.4.Mô hình tổng quan sản phẩm

### 3.5.Danh sách các chức năng

**Ứng dụng**

 

**Chức năng**

 

**Mô tả ý nghĩa**

 

**Độ ưu tiên**

 
Website M2MXem danh sách khóa họcCho phép KH có thể xem khóa học để xem khóa nào phù hợp với yêu cầu của họCaoWebsite M2MXem chi tiết khóa họcCho phép KH có thể xem thông tin chi tiết của khóa học để lựa chọn khóa học phụ hợp với yêu cầu của họCaoWebsite M2MĐăng ký khóa họcCho phép KH có thể đăng ký vào khóa học đang activeCaoWebsite M2MĐăng ký nhận thông báo khóa họcCho phép KH có thể đăng ký nhận email thông báo khi khóa học mở tuyển sinh để nắm được lịch tuyển sinhTrung bìnhWebsite M2MTra cứu đánh giá học viênCho phép KH có thể tra cứu kết quả đánh giá của học viên public kết quảTrung bìnhWebsite M2MXem bài test của học viênCho phép KH xem bài test cuối khóa của học viên khi học viên public kết quả đánh giáTrung bìnhWebsite M2MXem chứng chỉ của học viênCho phép KH xem chứng chỉ bản mềm của họ để họ có thể in hay tải bản mềm của chứng chỉTrung bìnhWebsite M2MĐăng ký tài khoảnCho phép KH đăng ký tài khoản để thực hiện các chức năng
Cao

 
Website M2MĐăng nhậpCho phép KH đăng nhập để thực hiện các chức năngCaoWebsite M2MQuên mật khẩuCho phép KH thực hiện lấy lại mật khẩuCaoWebsite M2MXem chi tiết tài khoảnCho phép KH thực hiện xem chi tiết thông tin tài khoản của họCaoWebsite M2MCập nhật tài khoảnCho phép KH thực hiện cập nhật thông tin tài khoản khi có nhu cầuCaoWebsite M2MĐăng ký bảo lưuCho phép KH thực hiện đăng ký bảo lưu khi có nhu cầu muốn bảo lưu khóa học đã đăng kýCaoWebsite M2MXem kết quả đánh giáCho phép KH xem kết quả đánh giá của họ sau khóa họcTrung bìnhWebsite M2MPublic/Un-public kết quả trên webCho phép KH lựa chọn public hay un-public kết quả trên webTrung bìnhWebsite M2MXem danh sách khóa học đăng kýCho phép KH xem danh sách các khóa học đã đăng kýCaoWebsite M2MXem chi tiết khóa học đã đăng kỹCho phép KH xem lại chi tiết thông tin khóa học đã đăng ký để kiểm tra lại thông tin khóa họcCaoWebsite M2MXem thông tin thanh toánCho phép KH xem thông tin QR thanh toán để thực hiện thanh toán và hoàn thành đăng kýCaoWebsite M2MXem QR nhóm zaloCho phép KH xem QR tham gia nhóm zalo để trao đổi , nhận thông báo về lớp họcCaoAdmin PortalĐăng nhập web adminCho phép admin đăng nhập vào hệ thống để thực hiện các chức năng quản lýCaoAdmin PortalTìm kiếm yêu cầu đăng ký khóa họcCho phép admin tìm kiếm yêu cầu đăng ký khóa học để phục vụ cho công tác quản lýCaoAdmin PortalHủy đăng kýCho phép admin thực hiện hủy đăng ký của KHCaoAdmin PortalImport file sao kêCho phép admin thực hiện import sao kê để hệ thống cập nhật trạng thái thanh toán thành côngCaoAdmin PortalXuất danh sách emailCho phép admin xuất danh sách email để thực hiện share video cho học viênCaoAdmin PortalXác nhận share videoCho phép admin xác nhận share video để phục vụ cho khóa họcCaoAdmin PortalLịch sử share videoCho phép admin xem lại lịch sử đã share video để đảm bảo share đầy đủ tài liệu cho học viênCaoAdmin PortalXem danh sách lớp họcCho phép admin xem danh sách lớp học để phục vụ cho công tác quản lýCaoAdmin PortalXem chi tiết lớp họcCho phép admin xem thông tin chi tiết lớp họcCaoAdmin PortalStart lớp họcCho phép admin cập nhật trạng thái start lớp họcCaoAdmin PortalStop lớp họcCho phép admin cập nhật trạng thái stop lớp họcCaoAdmin PortalXem bài tập về nhàCho phép admin xem BTVN đã làm của học viên để chấm chữa BTapThấpAdmin PortalĐánh giá học viênCho phép admin thực hiện đánh giá học viên sau khóa họcTrung bìnhAdmin PortalXem chứng nhận của học viênCho phép admin xem chứng nhận của học viênTrung bìnhAdmin PortalThêm mới tài liệuCho phép admin thêm mới tài liệu để phục vụ cho khóa họcThấp    
## 4.ERD

## Chi tiết mô tả các bảng
**Tên bảng****Ý nghĩa****Ghi chú khác**Khóa học
Bảng lưu trữ các khóa học của trung tâm

Hiện tại khóa học chỉ có 2 khóa học BA - Online và Offline

Dev thực hiện thiết lập các khóa học theo yêu cầu

Chưa cần làm chức năng trên giao diện để có quản lý thông tin khóa học này

 
Lớp học
Quản lý các lớp học tương ứng với các đợt tuyển sinh của khóa học

Mỗi khóa học sẽ có nhiều lớp học ở các đợt khác nhau

Có thể cân nhắc xây dựng chức năng tạo Lớp học

hoặc có thể tạo thẳng trong DB (quản lý đợt tuyển sinh sẽ chưa ưu tiên làm giao diện, nếu kịp thì làm)
UserQuản lý thông tin user trên hệ thống
Có chức năng đăng ký user trên website dành cho User

sau đó user có thể đăng nhập bằng email/Sđt
Lịch sử đăng kýQuản lý thông tin đăng ký khóa học của các học viên Học viên theo lớpQuản lý học viên theo từng lớp học
Sau khi đăng ký và thanh toán thành công, hệ thống sẽ tự động add học viên vào lớp học tương ứng

Với các học viên bảo lưu, sẽ lưu lại được lớp học gốc mà học viên đăng ký

Với học viên bảo lưu mà chưa chọn lớp học nào thì thông tin mã lớp học sẽ rỗng
Đăng ký bảo lưuQuản lý lịch sử đăng ký bảo lưu của các học viên Đánh giá học viên
Quản lý đánh giá của các học viên

 

Các mentor sẽ nhập thông tin đánh giá học viên qua bài test cuối khóa

Học viên có thực hiện thiết lập có cho public thông tin này cho các bên vào tra cứu trên page hay không (is_public=1)
Email nhận thông báoLưu trữ thông tin của các bạn có nhu cầu thông báo khi có đợt tuyển sinh của khóa tương ứng Chi tiết sao kêLưu thông tin chi tiết các GD được import từ file sao kê, phục vụ cho việc xác nhận thanh toán Lịch sử share videoLưu lại các lần share video cho học viên 
## 5.Biểu đồ trạng thái

**Biểu đồ trạng thái Đăng ký khóa học (Lịch sử đăng ký khóa học)**

 

**Biểu đồ trạng thái lớp học**

 

**Biểu đồ trạng thái học viên trong lớp học**

 

**Biểu đồ trạng thái chi tiết sao kê**