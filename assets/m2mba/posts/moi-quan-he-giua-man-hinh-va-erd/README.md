---
id: 67
title: "MỐI QUAN HỆ GIỮA MÀN HÌNH VÀ ERD"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T10:59:00.000Z"
source_url: "https://m2mba.com/blog/articles/moi-quan-he-giua-man-hinh-va-erd"
---

# MỐI QUAN HỆ GIỮA MÀN HÌNH VÀ ERD

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T10:59:00.000Z*

Tại sao các bạn dễ vẽ màn hình nhưng lại không thể tư duy được ERD. Chắc chắn không có 1 BA nào mà không biết vẽ màn hình đúng không ạ? Mà mình nghĩ nhiều bạn BA giờ làm việc có khi chủ yếu cũng chỉ vẽ màn hình mà thôi, nhưng tại sao khi yêu cầu các bạn tư duy thêm về ERD thì bắt đầu nhiều bạn lại ngại, đặc biệt là các bạn non IT vì các bạn nghĩ mình ko thể làm được. Vẽ màn hình chỉ là 1 technique quá cơ bản của BA, nhưng ERD lại ở tầm khác và cực hữu ích. Vậy tại sao các bạn không thử cố gắng tiếp cận nó. Bài này mình sẽ nói mối quan hệ giữa ERD và màn hình nhé, để các bạn thấy được ERD cũng không phải cái gì nó phức tạp, nhưng nó cần tư duy xa hơn

 

Màn hình và ERD thực ra nó có mối quan hệ với nhau, bạn nào vẽ được màn hình, chịu khó tư duy sâu 1 tý thì ra được ERD (tất nhiên số lượng màn hình thường rất nhiều hơn so với số lượng thực thể). Bạn nào đã vẽ được ERD rồi thì vẽ màn hình cũng không có gì khó khăn , vì từ ERD là đã biết được với màn hình tương ứng sẽ có những thông tin gì rồi

Dưới đây mình nêu 1 ví dụ đơn giản về Đăng ký tài khoản trên 1 ứng dụng Tiki nhé

- Khi bạn đăng ký tài khoản user của tiki, các bạn sẽ cần nhập các thông tin cơ bản (như ảnh đính kèm): Số điện thoại, Họ tên. Những thông tin này bắt buộc phải lưu lại trên hệ thống để phục vụ cho việc đăng nhập của user đó. Khi đó chúng ta sẽ có 1 thực thể là customer, thực thể này dùng để lưu lại các thông tin đăng ký của KH, thực thể sẽ có các thuộc tính như Customer ID, số điện thoại,họ tên, mật khẩu
- Khi bạn đăng nhập, bạn nhập các thông tin số điện thoại và mật khẩu. Hệ thống sẽ cần check thông tin trong thực thể này để check xem thông tin đăng nhập có trùng khớp không? Nếu trùng khớp sẽ cho đăng nhập, ngược lại báo lỗi
- Khi các bạn vào chức năng xem chi tiết tài khoản, hệ thống sẽ lấy thông tin trong thực thể customer tương ứng với user bạn đang đăng nhập để hiển thị ra cho các bạn nhìn thấy
- Khi các bạn vào chức năng cập nhật thông tin tài khoản, các bạn sẽ update thông tin cũ (lúc đăng ký) và có thể bổ sung thêm 1 số thông tin khác như ngày sinh, giới tính, quốc tịch, email. Tất cả thông tin này sẽ được lưu trữ vào thực thể customer và khi đó thực thể này sẽ cần có thêm 1 số thuộc tính như ngày sinh, giới tính, quốc tịch, email để lưu trữ các thông tin này khi KH cập nhật thông tin
Vây khi đó thực thể user/customer/account sẽ có các thuộc tính để mô tả nó gồm: User ID, số điện thoại,họ tên, mật khẩu, ngày sinh, giới tính, quốc tịch, email và có thể có 1 số thông tin mà không bao giờ KH phải nhập vào như kênh đăng ký, thời gian đăng ký

Từ đó các bạn có thể thấy, 1 thực thể có thể có nhiều usecase tác động vào, như thực thể trên có usecase: Đăng ký, đăng nhập, xem chi tiết, cập nhật tài khoản, cập nhật số điện thoại, cập nhật email=>Số lượng thực thể sẽ luôn ít hơn số lượng màn hình rất nhiều. Các thuộc tính của 1 thực thể chính là tổng hợp các trường từ các usecase tác động vào thực thể đó. Vậy tại sao các bạn lại vẽ được màn hình nhưng thực thể lại không thể liệt kê ra được? Đó là vì bạn chưa chịu tư duy sâu về mặt data lưu trữ mà thôi

Một bạn senior BA, khi dự án ở sprint 0, các bạn đã cần phải phân tích để nắm được ds các usecase sẽ có trên hệ thống rồi, giả sử bạn tìm ra tầm 50 usecase thì khi đó có tầm khoảng 10 thực thể, khi đó bạn cần liệt kê các thực thể , thuộc tính của các thực thể đó, và thể hiện mối quan hệ giữa các thực thể đó. Còn nếu bạn vẽ thì bạn cần vẽ 50 màn hình đấy, việc vẽ màn hình lâu hơn rất nhiều so với liệt kê các thông tin trên màn hình đúng không? Nó chỉ khó do các bạn chưa chịu tư duy, và tư duy tổng hợp của các usecase mà bạn dự định có. Tất nhiên ở đoạn này các bạn sẽ có thể liệt kê đang thiếu, nhưng việc bạn đưa ra đc ERD sẽ giúp team hiểu được khung sườn bài toán nhanh hơn nhìn vào ds usecase, ds màn hình bạn vẽ ra (mà chắc chắn bạn ko thể vẽ đủ được, chưa kể mối liên hệ giữa các màn hình cũng khó thể hiện)

Mình có 1 bạn học viên làm case study trong khóa học về hệ thống giao đồ ăn, trong hệ thống đó bạn ấy có tìm được thực thể là Công thức tính phí. Thực thể này thì hoàn toàn đúng, nhưng bạn đưa ra các thuộc tính của thực thể này là:

- Điều kiện tính phí
- Điều kiện khoảng cách
- Điều kiện thời tiết
- Giá. 
Khi đưa ra thuộc tính ntn thì mình hiểu là bạn ấy chưa hình dung được về công thức tính phí này nó sẽ tính toán ntn, nó có khả thi hay không, vì thuộc tính nhìn đã thấy rất chung chung, thuộc tính bọn e phải break ra từng thông cụ thể (Ví dụ khoảng cách thì phải từ khoảng cách mấy đến khoảng cách mấy=>thuộc tính from, to). Và các bạn hãy thử nghĩ luôn, khi bạn ấy đưa ra thực thể như vậy thì nếu bạn cần xây dựng 1 Usecase là Tạo mới công thức tính phí, bạn ấy sẽ vẽ màn hình ntn=>Chắc chắn bạn ấy cũng sẽ không biết vẽ ntn, bởi vì khi thuộc tính các bạn còn nêu chung chung, bạn chưa lắp ghép được với thông tin đầu vào (giả sử như KH đặt đồ ăn trong khung giờ A, thời tiết nóng, khoảng cách 7km thì giá tiền bao nhiêu, ví dụ vậy) thì với thực thể công thức tính phí đưa ra như trên , hệ thống tính ntn 

Sau đó, mình có yêu cầu bạn nêu công thức tính phí mà bạn muốn hệ thống sẽ xây dựng để mình hỗ trợ bạn hiểu được vấn đề của bạn ở đâu. 

- **Công thức tính phí như sau**:. Trong điều kiện thời gian sẽ có khoảng thời gian ví dụ từ 22 giờ -24, cứ trong khoảng thời gian đó thì mỗi đơn hàng +3k. Điều kiện về khoảng cách sẽ có khoảng cách từ vị trí khách đến nhà hàng, 3km đầu phí là 15k, cứ trên 3km thì mỗi km sau sẽ được tính thêm 5k. Điều kiện thời tiết sẽ có giá trị 0,1,2,3 (0 là bình thường, 1 sẽ dạng như nắng nóng to trên 38 độ chẳng hạn, 2 là mưa to, 3 là rét dưới 8 độ, mỗi trường hợp thì + 1 giá khác nhau) 
Và với công thức tính phí như trên thì mình có lấy ví dụ cho bạn cách nó sẽ lưu trên hệ thống như ảnh đính kèm

và khi bạn tư duy được ERD thì quay ra bạn sẽ vẽ được màn hình tạo mới công thức phí cũng rất dễ dàng như ảnh đính kèm

 

1 số bạn BA thì có thể nghĩ là mình chỉ cần đưa công thức ntn là okie, còn lại là việc của dev. Thực ra là cũng không sai hẳn, nhưng đó là BA chỉ là người lấy yêu cầu từ stakeholder chứ không phải là người phân tích và đưa ra giải pháp. Khi gặp yêu cầu đó thì BA cần tổng quát hóa và tư duy lưu lại công thức ntn trên hệ thống ,còn sau đội code có họ thiết kế lại theo ý họ, thì mình chỉ cần review lại thiết kế đó của họ đã cover được hết các TH tính phí của mình chưa, nếu chưa thì mình giải thích để họ sửa khi nào okie thì thôi, giả sử bất khả thi thì có thể yêu cầu đổi công thức tính phí, nhưng ít nhất mình nắm được vì sao bất khả thi, chứ không phải chỉ nghe từ 1 chiều là dev nói không khả thi nên đành chấp nhận

Vấn đề phần lớn của các bạn BA chưa tư duy được ERD là do các bạn chưa tư duy xa được, mà các bạn chỉ nghĩ tới những cái trước mắt mình làm mà thôi, chính vì điều này cũng làm cho dự án các bạn liên tục thay đổi yêu cầu. Khi các bạn chịu tư duy ERD, nó sẽ giúp cho đội code nắm được khung sườn sản phẩm rất tốt, đội code sẽ hình dung ra được có những chức năng chính gì, trong từng thực thể đó có những thuộc tính gì đặc biệt, cần lưu ý. Khi bạn tư duy được ERD thì xác suất bạn làm chức năng tiếp theo sẽ phải quay lại sửa chức năng cũ khá ít, vì bạn đã chịu tư duy sớm rồi

Do đó, nếu bạn đang là BA, fresher hay senior thì nên chịu khó tìm hiểu thêm technique này, thời gian đầu chỉ là thử tư duy, sau đó mapping dần với DB các bạn code thiết kế. Những lần đầu sẽ sai, nhưng dần dẫn sẽ vỡ ra nhiều thứ. Mình tin cứ dần dần như thế trong 1 năm thì các bạn sẽ tiến bộ lên rất nhiều. Và khi join dự án, mà gặp trường hợp mình làm chức năng A mà phải quay lại sửa chức năng trước đó, thì bạn nghĩ kỹ lý do là gì, nếu mình tư duy về ERD thì có giúp mình giải quyết được vấn đề này không? 

Hy vọng các bạn sẽ có thêm động lực để tìm hiểu technique khó nhưng có võ này nhé