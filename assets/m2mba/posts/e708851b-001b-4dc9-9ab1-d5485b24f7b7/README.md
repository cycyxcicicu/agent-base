---
id: 234
title: "Quản lý nghiệp vụ test - Yêu cầu thay đổi ngày 2907"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-07-29T12:08:13.000Z"
source_url: "https://m2mba.com/blog/articles/e708851b-001b-4dc9-9ab1-d5485b24f7b7"
---

# Quản lý nghiệp vụ test - Yêu cầu thay đổi ngày 2907

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-07-29T12:08:13.000Z*

## **1.Lý do thay đổi**

Một số chức năng của nghiệp vụ test khó sử dụng, gây bất tiện cho người dùng, cụ thể như sau
Ứng dụngChức năngLý do thay đổiChức năng ảnh hưởngWeb học viênDanh sách bài test
Khó lọc được các bài test cần làm, do 1 học viên có thể có rất nhiều bài test

Sau này khi có nhiều bài test ở dạng public, học viên sẽ càng khó tìm kiếm hơn nữa

Ngoài ra việc cần chia thêm tab Chưa thực hiện, để học viên có thể thực hiện các bài test tương ứng

=>Bổ sung phần lọc bài test và thêm mới tab Chưa thực hiện
 Web học viênLàm bài test
- Học viên có thê  việc bận nên không làm bài test kịp thời tại lúc đó nên có thể dừng lại và sau đó quay lại làm tiếp
- Ngoài ra vì việc học viên do học viên có thể click làm bài thoải mái, nến mặc dù đang mở 1 tab làm bài test, lại tiếp tục click vào làm bài =>hệ thống mở ra tab khác để làm =>Khi nộp bài, sẽ bị báo lỗi : Bạn đã nộp bài trước đó =>Tại 1 thời điểm chỉ được mở 1 tab, nếu trạng thái Đang thi thì không cho click vào Làm bài
- Với các bài cần duyệt điểm: Mentor chưa duyệt điểm, Học viên đã làm tiếp=>làm việc chấm bài ko có ý nghĩa, vì học viên đã hiểu sai thì sẽ vẫn tiếp tục hiểu sai, và học viên thường làm vội vàng cho xong, để được mở các phần khác. Từ đó , dần tới học viên ko hiểu bài, gây ảnh hưởng tới các nội dung tiếp theo. =>Bài test nào cần duyệt điểm thì học viên chỉ được làm lần tiếp theo nếu bài làm trước đó đã được duyệt. 
- Học viên làm bài thử cho biết, hoặc làm fail. Sau đó làm lại ngay=>Việc giới hạn số lần ảnh hưởng, học viên yêu cầu mở thêm để làm bài=>Cần chặn: Nếu làm bài test bị fail thì sau 30ph mới được làm lại
 
Tạo bài test=>Bổ sung cấu hình pauseWeb học viênXem chi tiết bài test
Chưa cho phép học viên xem đáp án=>Cần cho phép xem đán án, tùy cấu hình từng bài test khác nhau và rule hiển thị sẽ khác nhau

Ngoài ra các icon thể hiện học vien không rõ =>Bổ sung thêm chú thích icon
Tạo bài test=>Bổ sung Cấu hình rule hiển thịWeb adminQuản lý kết quả test
1 học viên có thể làm bài test nhiều lần, nên khi view danh sách sẽ thấy khá nhiều, với các bài cần duyệt điểm, mentor sẽ chỉ duyệt điểm cho lần làm sau

=>Hiển thị kết quả theo học viên: nếu học viên làm 2 lần thì cũng chỉ hiển thị 1 lần thôi, và chỉ hiển thị kết quả gần nhất, và bổ sung thêm icon xem lịch sử làm bài của học viên đó, để xem chi tiết từng bài làm của học viên
 Web adminTạo bài test
Hiện tại học viên làm bài test xong chưa xem được đáp án =>Bổ sung cho phép cấu hình khi nào thì show đáp án cho học viên

Ngoài ra do 1 số nhu cầu riêng, nên cần cho phép thêm câu hỏi vào bài test 1 cách tự động thay vì chọn từng câu đơn lẻ
 Web adminChấm điểm
Bổ sung phần chầm điểm khi xem bài làm của các học viên theo từng câu hỏi (Trong phần xem thống kê kết quả theo bài test)

Hiện tại mở ra tab mới, link tới bài làm tương ứng, khá bất tiện nếu cần chấm nhiều bài

Ngoài ra, hiện chỉ chấm được điêm dạng số tự nhiên=>Cho phép chấm số thập phân
 Web adminTạo câu hỏiHiện đang chưa hỗ trợ nhập đáp án tự luận và hệ thống tự chấm điểm bằng cách so sánh thông tin học viên nhập vào và thông tin của đáp án=>Bổ sung đáp án cho phần câu hỏi tự luận Tự động chấm điểm=>Hỗ trợ tự động chấm điểm cho bài tự luận của 1 số bài đơn giản
Chi tiết các nội dung ảnh hưởng như sau:

## **2.NỘI DUNG THAY ĐỔI**
Ứng dụng**Chức năng  **Loại thay đổi**Hiện trạng****Thay đổi**Web học viênTạo câu hỏiUpdate 
Bổ sung thêm nhập Đáp án khi câu hỏi dạng tự luận
     Web adminTạo bài testUpdate
Chưa có cấu hình xem đáp án

Chưa hỗ trợ cấu hình có cho phép pause bài test hay ko

Bổ sung thêm combobox lựa chọn rule show đáp án và checkbox cấu hình cho phép pause bài test hay ko
Web adminThêm câu hỏi vào bài testThêm mớiBổ sung cách thêm bằng cấu hình tự động
1.Khi chọn Thêm câu hỏi: hiển thị chọn thêm tự động hay thêm thủ công

2.Cấu hình thêm tự động

3.Khi click vào nút Thêm: Thực hiện lọc các câu hỏi trong kho đề test theo cấu hình tương ứng, trong đó **Ưu tiên những câu chưa có trong đề nào cả**
Web adminQuản lý kết quả testUpdateMỗi lần học viên làm bài test sẽ hiển thị thành 1 bản ghi=>Mentor khó review kết quả, Mentor quan trọng nhất là kết quả lần gần nhất của học viên đó
Mỗi học viên - Một bài test chỉ hiển thị 1 dòng, và hiển thị kết quả của lần gần nhất:

- click vào icon infor sẽ xem chi tiết của lần làm gần nhất
- Click vào lịch sử làm bài sẽ xem được tất cả các lần làm bài: hiển thị thêm thông tin :Điểm
- Xếp loại
- Icon xem chi tiết: nếu click vào sẽ ra MH xem chi tiết bài làm tương ứng
 
Web adminChấm điểmUpdate
Chấm điểm trong phần Thống kê kết quả theo bài test

Hiện tại click vào chấm điểm đang mở ra 1 tab mới, link tới bài làm tương ứng của học viên

Click vào sẽ mở popup gồm các thông tin sau

1.Điểm: Nhập

2.Hiển thị đáp án, và điểm tối đa

3.Nhận xét: nhập
Web adminChấm điểmUpdateHiện đang sử dụng text area để nhập nhận xét nên khá bất tiện, nếu muốn upload ảnh để comment hoặc sử dụng bullet để nhận xétNhập nhận xét bằng EditorWeb adminDuyệt điểmUpdateChưa gửi email cho học viên nên học viên không biết
Bổ sung gửi email sau khi duyệt điểm, chi tiết nội dung email cấu hình trong DB, các tham số cần có

- Điểm đạt được
- Tỉ lệ phần trắm
- Kết quả Pass/fail (nếu có)
- Điểm cần pass cho bài test (nếu có)
- Xếp loại (nếu có)
- Thời gian duyệt điểm
- Người duyệt
Với các thông tin note (nếu có): Có nghĩa nếu có thông tin thì hiển thị trong email, ko có thì ko hiển thị
Web adminXem chi tiết bài làmUpdate
Hiện tại chưa rõ cách xử lý hiển thị trong phần này với các TH: Đáp án học viên chọn là sai/Đúng

 

Với câu đúng 1 phần, cần sửa lại hiển thị như sau:

Câu nào học viên chọn mà 

- Sai: Hiển thị icon chéo
- Đúng : tích xanhWeb học viênDanh sách bài testUpdateHiển tại đang hiển thị danh sách theo order ngày gán giảm dần, và ko có lọc bài, cũng như chưa có tab Chưa thực hiện, để có thể tìm các bài học viên chưa làm=>Để có thể làm luôn
Bổ sung thêm các trường lọc bài test, cũng như thêm tab Chưa thực hiện. Trong tab Chưa thực hiện/Hoàn thành cũng hỗ trợ lọc bài test như tab Tất cả

 

 
Web học viênLàm bài testUpdateChưa hỗ trợ tính năng pause/restart bài test
Bổ sung thêm nút Pause /restart bài test

- Nếu đang ở trạng thái Pause thì hiển thị nút restart và nếu đang ở trạng thái Đang thi thì hiển thị nút Pause
- Và khi pause bài test: Học viên không được thao tác click vào ds câu hỏi cũng như các nút next, previous=>Ko dc xem nội dung câu hỏi khácWeb học viênLàm bài testUpdateHiện tại có thể click thoải mái để làm bài nên cùng 1 lúc học viên ko may click làm bài nhiều lần=>Khi nộp bài bị lỗi
Khi click vào Làm bài, nếu trạng thái bài làm ở trạng thái Đang thi thì sẽ báo lỗi: Bạn đang thực hiện làm bài test trước đó. Bạn có muốn hủy bài làm cũ không

Nếu học viên xác nhận có thì sẽ thực hiện xóa các thông tin liên quan đến bài làm gần nhất của học viên
Web học viênLàm bài testUpdateHiện tại học viên có thể click làm bài liên tục nhiều lần, cho dù bài đó chưa duyệt điểm hoặc chưa pass
Bổ sung thêm rule cho phép Làm bài: 

Chỉ được làm bài khi bài làm trước đó đã ở trạng thái duyệt điểm 

Hoặc nếu bị fail thì phải sau 30ph so với thời điểm kết thúc bài làm cũ

Ngược lại sẽ báo lỗi

“Bạn cần chờ mentor duyệt điểm trước khi làm lần tiếp theo”

“Bạn hãy xem lại kiến thức bài giảng và làm lại sau xx phút nữa”
Web học viênLàm bài testUpdateBổ sung thêm rule phần chấm điểm câu tự luận
Chấm điểm theo tiêu chí (cần trim dữ liệu xâu nhập vào để so sánh)

- Contain: Câu trả lời của học viên chứa thông tin trong đáp án 
- In: câu trả lời nằm trong danh sách các phần tử được nhập trong đáp án (Cách nhau bởi dấu ;) 
- Equal: Giá trị của học viên trả lời =Giá trị của đáp án trong đáp ánWeb học viênXem chi tiết bài testUpdateHiện chưa xem được đáp án sau khi submit bài test
Bổ sung xử lý rule xem đáp án

Tùy thuộc vào cấu hình bài test:

- Show đáp án sau khi submit: Học viên có thểm xem được đáp án khi xem chi tiết bài làm của mình
- Show đáp án khi đủ số lượng: Nếu học viên được phép làm 3 lần, thì sẽ show khi đã làm đủ 3 lần
- Show đáp án khi pass: Nếu kết quả đánh giá bài làm của bất kể 1 lần nào đó có trạng thái là pass thì sẽ hiển thị
Ngoài ra cần hiển thị như sau, Câu nào học viên chọn mà 

- Sai: Hiển thị icon chéo
- Đúng : tích xanhWeb học viênXem chi tiết bài testUpdateChưa có chú thích icon khi xem chi tiết bài làm
Bổ sung giải thích các icon

- Đúng toán phần
- Đúng 1 phần
- Chờ chấm điểm
- Sai