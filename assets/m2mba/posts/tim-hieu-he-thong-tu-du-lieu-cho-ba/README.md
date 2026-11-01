---
id: 65
title: "TÌM HIỂU HỆ THỐNG TỪ DỮ LIỆU"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T10:21:56.000Z"
source_url: "https://m2mba.com/blog/articles/tim-hieu-he-thong-tu-du-lieu-cho-ba"
---

# TÌM HIỂU HỆ THỐNG TỪ DỮ LIỆU

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T10:21:56.000Z*

Bài này là bài tiếp nối bài hôm trước về việc tư duy dữ liệu cần thiết như thế nào đối với BA nhé. Việc 1 BA mới phải join vào 1 dự án đã chạy thời gian là chuyện hoàn toàn bình thường. Vậy các bạn thường làm thế nào để có thể tìm hiểu được về dự án đó, các bạn có thể tham khảo bài viết mình viết cũng khá lâu rồi nhé, các bạn xem [tại đây](https://m2mba.com/posts/ae7cf425-e13c-11ee-9ada-e61017865c59): 

Trong bài viết này, mình sẽ guideline cách mọi người tìm hiểu hệ thống từ thông tin lưu trữ trong database, đây là cách mà mình thường xuyên làm (cũng là 1 step trong link mình gửi). Do trong khóa học, mình có lấy case study là xây dựng hệ thống Chăm sóc khách hàng, trong hệ thống này thì tổng đài là 1 phần không thể thiếu được. Trước đây mình đã từng join dự án kiểu như thế này, lúc đó hoàn toàn không hiểu về cách thức vận hành của luồng tổng đài như thế nào, và cách mình làm là đọc tài liệu về opensource Asterisk với sự giúp đỡ của dev. Tất nhiên mình chỉ quan tâm tới những gì mà mình thấy là cần để phân tích nghiệp vụ, còn các yếu tố về kỹ thuật mình vẫn mờ tịt, không hiểu sâu. Đó cũng là chuyện bình thường với 1 người làm BA, bạn có thể không cần giỏi về kỹ thuật, chỉ cần biết cách để nói chuyện, khai thác thêm thông tin từ đội kỹ thuật là được. Và cách mình thường trao đổi với kỹ thuật, vẫn là tập trung vào data: Data input là gì, cần lưu trữ data gì, ý nghĩa của nó như thế nào, data cần output là gì

Vậy Cách tìm hiểu dự án từ database , data model như thế nào. Các bạn tham khảo nhé

- **Bước 1** : Đầu tiên các bạn sẽ xin account để đăng nhập vào database của dự án. Mình join dự án nào thì việc đầu tiên đó là xin cấp account DB. Đợt gần đây mình có hỗ trợ các dự án cho 1 số công ty, và dự án chạy được 1 thời gian rồi, trong đầu mục yêu cầu cung cấp thông tin thì database là điều bắt buộc, tài liệu dự án có hay không với mình cũng không quan trọng lắm. Vì tài liệu các nơi làm rải rác, không có phần overview nên đọc những tài liệu đó là ngột thở ngay
- **Bước 2**: Tiếp đến hãy mở ra xem danh sách các table trong đó (nếu nhiều bảng thì có thể dùng câu lệnh để lấy ra tên tất cả các table rồi xuất ra excel)
- **Bước 3:** Nếu như dự án của bạn có nhiều Table quá thì có thể team dev khoanh vùng các bảng theo các nhóm nghiệp vụ để tìm hiểu
- **Bước 4**: Tìm hiểu ý nghĩa từng bảng, thường thì tên mỗi bảng nó cũng toát lên ý nghĩa rồi, nếu mà các bạn không dự đoán được thì hỏi trực tiếp đội code ý nghĩa của các bảng đó. Ví dụ, với phần tổng đài CSKH thì có các bảng như ảnh đính kèm
 

-  **Bảng queue** lưu thông tin danh sách các queue của hệ thống tổng đài. Khi các bạn gọi vào các tổng đài mà có chia các nhánh, mỗi nhánh đó sẽ tương ứng với 1 queue
- **Queue_memeber**: Danh sách các ĐTV ở trong từng queue, ở đây sẽ lưu thông tin extension của các ĐTV (số máy lẻ)
- **Call_Status:** Lưu thông tin tổng hợp của cuộc gọi KH gọi
- **CDR**: Bảng lưu chi tiết cuộc gọi con của cuộc gọi từ KH (cuộc gọi của KH vào queue (vào nhánh), cuộc gọi từ KH tới ĐTV 1, Cuộc gọi từ KH tới ĐTV 2 nếu có chuyển cuộc gọi)
- **Bước** **5**: Tìm hiểu ý nghĩa từng trường trong các bảng đó, tìm hiểu ý nghĩa của trường đó, khi nào thì dữ liệu được insert/update vào trường này hoặc sử dụng đầu vào cho chức năng khác, các giá trị có thể có của trường đó, khi nào thì có giá trị nào (có thể dự đoán bằng kinh nghiệm nghề nghiệp, nếu không đoán được thì note lại hỏi team dự án) =>từ đó suy ra các nghiệp vụ liên quanTrong hệ thống CSKH, có bảng ticket , trong bảng này có trường Staff_process (Nhân viên xử lý ticket), deadline (hạn xử lý). Từ đó các bạn sẽ đặt câu hỏi khi nào thì dữ liệu được update/insert vào các trường này, từ đó tìm hiểu ngược lại sẽ có chức năng : Phân công xử lý, và gán hạn xử lý hoặc nếu có bảng quy định SLA xử lý cho từng loại ticket thì trường deadine sẽ được update tự động khi phân công xử lý dựa vào SLA đã cấu hình
- Ví dụ bảng call_status có trường status, mình sẽ xem nó có các giá trị như thế nào: InQue, CONNECT, COMPLETECALLER, COMPLETEAGENT, ABANDON, EXITEMPTY, EXITWITHKEY, EXITWITHTIMEOUT. Từ các giá trị đó mình lại tìm hiểu khi nào thì nó về các trạng thái đó và mình tổng hợp lại thành 1 biểu đồ trạng thái như đình kèm. Từ biểu đồ trạng thái bạn hoàn toàn có thể biết có các nghiệp vụ gì có thể xảy 
- Dựa vào đoạn code trigger insert dữ liệu vào queue_log xem trên mạng, sau đó tổng hợp thành biểu đồ trạng thái
 

- **Bước 6**: Tìm hiểu mối quan hệ giữa các bảng (bước này hoàn toàn có thể làm song song với bước 5). Từ mối quan hệ đó các bạn có thể dự đoán được chức năng trên hệ thống như với ảnh ERD đính kèm, các bạn có thể dự đoán được 1 số chức năng dựa vào ERD như sau
    Giả sử 1 hệ thống có ERD như ảnh đính kèm

Dựa vào ERD trên, chúng ta có thể dự đoán 1 số thông tin như sau

- Một nhân viên quản lý nhiều KH: Như vậy sẽ có 1 trong khả năng chức năng như sau trên hệ thốngTạo KH và gán luôn nhân viên quản lý
- KH đăng ký tài khoản, sau đó có chức năng để phân công KH đó được nhân viên nào quản lý
- Một KH có nhiều Hóa đơn, hóa đơn có nhiều chi tiết hóa đơn, 1 chi tiết hóa đơn thì gắn với 1 track, 1 track thì có trong nhiều chi tiết hóa đơn. Vậy chức năng trên hệ thống sẽ như sauKH đặt mua 1 đơn hàng gồm các track: mỗi lần đặt mua sẽ có 1 invoice, 1 invoice_detail sẽ chứa chi tiết KH mua track nào, số lượng bao nhiêu và giá tại thời điểm đó như thế nào
- Ngoài ra, còn có các chức năng tạo Album của các nghệ sỹ (1 album chứa nhiều track, 1album gắn với 1 artist) hoặc có thể tạo playlist, 1 playlist có thể có nhiều track (chỗ này thì mình nghĩ cái ảnh mình lấy trên mạng bị sai về quan hệ giữa playlist và playlist_track, phải là quan hệ 1 nhiều thay vì quan hệ 1-1 như hình)
 

Một số link liên quan, ai muốn đọc tìm hiểu về tổng đài asterisk có thể đọc thêm. 

Các event trong queue_Log: [https://docs.asterisk.org/Operation/Logging/Queue-Logs/?h=queue+log#how-do-i-interpret-the-lines-in-the-queue-log](https://docs.asterisk.org/Operation/Logging/Queue-Logs/?h=queue+log#how-do-i-interpret-the-lines-in-the-queue-log) 

Đăc tả chi tiết thông tin cuộc gọi [https://docs.asterisk.org/Configuration/Reporting/Call-Detail-Records-CDR/CDR-Specification/#cdr-lifetime](https://docs.asterisk.org/Configuration/Reporting/Call-Detail-Records-CDR/CDR-Specification/#cdr-lifetime)