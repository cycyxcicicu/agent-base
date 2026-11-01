---
id: 72
title: "Các kỹ thuật giúp overview hệ thống"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T12:00:21.000Z"
source_url: "https://m2mba.com/blog/articles/cac-ky-thuat-giup-overview-he-thong"
---

# Các kỹ thuật giúp overview hệ thống

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T12:00:21.000Z*

Hiện tại phương pháp agile gần như khá phổ biến trong các công ty phát triển sản phẩm phần mềm. Khi triển khai theo phương pháp này, BA đỡ hơn rất nhiều ở công đoạn viết tài liệu. Nếu như theo phương pháp truyền thống, BA phải viết hết toàn bộ tài liệu gồm các tính năng của SP sẽ làm, vẽ màn hình, mô tả chi tiết…1 tài liệu có thể dài cỡ vài trăm trang là chuyện bình thường. Việc viết tài liệu với số lượng lớn như vậy sẽ mất thời gian,và chất lượng sẽ không đảm bảo tốt được. Tuy nhiên khi triển khai agile, vấn đề theo mình thấy khó khăn nhất đối với BA là làm sao đưa ra được overview về sản phẩm, giúp cho team nắm được khung hình sản phẩm mình sẽ làm như thế nào, để sau đó break ra các chức năng vào từng sprint mà kiểm soát được càng ràng buộc ngay từ đầu, mà các tính năng đó có tính phụ thuộc các tính năng phát triển sau, để tránh sau này thay đổi

Ví dụ như bạn được yêu cầu xây dựng 1 SP dạng SaaS về quản lý nhà hàng, bạn là BA của sản phẩm này. Cách bạn làm như thế nào để giúp đội code overview được sản phẩm

Sau đây mình xin trình bày cách của mình nhé

- **Xác định các đối tượng sẽ sử dụng sản phẩm:** Với sản phẩm quản lý nhà hàng, đối tượng sử dụng sẽ là : Nhân viên nhà hàng, NV bên kinh doanh SP QL nhà hàng. Bên nhân viên nhà hàng thì chia ra các đối tượng như NV phục vụ, Bếp và các đối tượng còn lại. Với Scope của SP mình đang làm, mình không bao gồm các phần việc liên quan tới luồng chế biến tại bếp. 
- **Xác định các ứng dụng mà các đối tượng đó sẽ dùng: **Tham khảo mô hình tổng quan sản phẩm 
- **Đưa ra business Process **cho giai đoạn trước mắt và giai đoạn có thể sau này (ưu tiên giai đoạn trước mắt nhé, nếu có thể vẽ cho luồng sau này thì tốt, không thì thôi) 
- **Đưa ra ERD của sản phẩm:** Đây là technique mà mình thấy hữu hiệu nhất khi transfer cho đội code về overview sản phẩm. Gần như khi nào đội code cũng yêu cầu mình xem ERD để hiểu, thay vì xem những thứ khác
 

 

**Tên thực thể****Ý nghĩa**Nhà hàngQuản lý danh sách nhà hàng sử dụng dịch vụ phần mềm FoodNowChủ nhà hàngQuản lý danh sách các chủ nhà hàng của các nhà hàng sử dụng phần mềm,  chủ nhà hàng có thể quản lý nhiều nhà hàng khác nhau, Chủ nhà hàng có thể điều chuyển để theo dõi hoạt động kinh doanh của từng nhà hàng khác nhauLoại phòngDanh mục loại phòng của nhà hàng, ví dụ như phòng Vip, Phòng bình dân…PhòngChi tiết các phòng thực tế tại nhà hàng, các phòng tại nhà hàng được đưa vào quản lý chi tiết trên hệ thống foodNowDanh mục bàn
Chi tiết các bàn tại nhà hàng, các bàn nằm trong các phòng khác nhau

Nếu nhà hàng chỉ có 1 phòng thì chỉ cần tạo 1 phòng chung
Món ănQuản lý danh sách món ăn tại nhà hàng, các món ăn sẽ có nhiều size khác nhau, mỗi size sẽ có 1 giá khác nhauSizeTypeQuản lý danh sách các size của món ăn, các món ăn sẽ có nhiều size khác nhau, mỗi size sẽ có 1 giá khác nhauGiá món ănChi tiết giá của từng món ăn tại nhà hàng, món ăn được thiết lập theo size nếu món ăn có nhiều sizeCombo món ănCho phép nhà hàng tạo combo món ăn để khuyến mại cho KH, trong combo món ăn sẽ quản lý được tổng giá món ăn riêng lẻ và giá của combo, tỷ lê giảm giá khi ăn theo comboMón ăn trong comboLà chi tiết các món ăn trong comboKhách hàngLà thông tin chi tiết của KH thực hiện đặt bàn ăn uống tại nhà hàng, quản lý điểm KH được tích hiện tại của KH, phân hạng KHĐặt bànChi tiết thông tin đặt bàn của KH qua các kênh như qua điện thoại, qua pasgo hoặc đến trực tiếp tại nhà hàngChi tiết bànMỗi lần đặt bàn sẽ có nhiều bàn khác nhau, thực thể này sẽ quản lý lần đặt bàn đó của KH sẽ đặt ngồi bao nhiêu bàn và cụ thể là bàn nàoĐặt mónChi tiết món ăn mà KH đặt món, quản lý chi tiết trạng thái của món ăn đó VoucherQuản lý danh sách voucher áp dụng tại nhà hàng, voucher có thể áp dụng cho toàn bộ KH hoặc áp dụng cho 1 số KH cụ thể, voucher sẽ áp dụng theo đơn hàng với giá trị đơn hàng tối thiểu thỏa mãn điều kiệnVoucher-KHThông tin chi tiết quản lý voucher theo từng KH và biết được KH được nhận voucher lúc nào, đã sử dụng chưa, sử dụng cho lần ăn nào, tổng giá trị KM áp dụng là bao nhiêuLịch sử tích điểmChi tiết lịch sử tich điểm của KHCông thức tích điểmQuản lý công thức để tích điểm cho KHDanh mục phân hạng KHQuản lý danh mục phân hạng KH, cho phép nhà hàng chủ động đưa ra các hạng của nhà hàng, các quy định liên quan tới việc phân hạng nhà hàng như mức tiêu dùng/điểm bao nhiêu trong 1 tháng, quý, năm thì tương ứng hạng nào

**Tên thực thể****Ý nghĩa**Nhà hàng
Quản lý danh sách nhà hàng sử dụng dịch vụ phần mềm FoodNow

Chi tiết thuộc tính xem ở phần trên
Gói sản phẩm
FoodNow đưa ra các gói sản phẩm để cho KH lựa chọn sử dụng

Gói SP sẽ có chứa nhiều tính năng, mỗi nhóm tính năng sẽ có nhiều quyền hạn trong đó nhưg tính năng quản lý đặt bàn: Đặt bàn, xem chi tiết thông tin bàn, Hủy bàn, đổi bàn…
Gói SP – Nhà hàngQuản lý lịch sử dụng gói sản phẩm của nhà hàngỨng dụng triển khai – nhà hàngQuản lý các ứng dụng mà nhà hàng lựa chọn triển khaiTính năngTạo ra các nhóm tính năng trên foodNow để sau đó tạo thành các gói sản phẩm cho nhà hàng lựa chọnPermissionChi tiết danh sách các quyền hạn trên foodNow, có 2 nhóm permission: Nhóm cho nội bộ foodNow và nhóm cho nhà hàngGói sản phẩm – Tính năngQuản lý các tính năng cho phép của gói sản phẩm đóTính năng – PermissionQuản lý các quyền thao tác trên tính năng đóLoại ứng dụngQuản lý các loại ứng dụng triển khai cho nhà hàng, hệ thống sẽ quy định giá sử dụng trên từng loại ứng dụng đó, ví dụ như ứng dụng Web quản lý nhà hàng, Mobile app Phục vụ, KDS…Giá gói sản phẩmQuản lý mức giá của gói sản phẩm, giá gói sẽ phụ thuộc vào gói, số lượng tài khoản sử dụng và kênh triển khaiConfigFoodNowQuản lý các tham số cấu hình linh động của foodNow như: thời hạn cảnh báo nhà hàng quá hạn, thời hạn tổng hợp tạo yêu cầu thanh toán…ListParameterConfig Nhà hàngQuản lý các tham số cần các nhà hàng config cho chính nhà hàng của mình, ví dụ như thời gian hoạt động, thời gian phục vụ trung bình, ca làm việcConfig nhà hàngChi tiết config của nhà hàng theo các tham số yêu cầu trong ListParameterConfig Nhà hàngKỳ hạnQuản lý các nhóm kỳ hạn trên hệ thống để phục vụ cho quy định giá gói sản phẩm, và để KH lựa chọn kỳ hạn phù hợpĐối tác tích hợpQuản lý các đối tác mà foodNow đang hỗ trợ tích hợp, ví dụ như đối tác thanh toán, đối tác đặt bànNhà hàng- Đối tácQuản lý xem các nhà hàng liên kết với những đối tác nào để hỗ trợ đăt bàn, thanh toánMapping Tham số giao tiếpQuản lý tham số thông tin của nhà hàng khi giao tiếp với các đối tácBiểu phí đối tácQuản lý mức phí mà đối tác thu nhà hàng khi kết nốiUser nhà hàngQuản lý danh sách user của các nhà hàngRole nhà hàngCho phép nhà hàng quản lý role của nhà hàng, ngoài các role do FoodNow tạo sẵnUser-Role nhà hàngQuản lý role của các user của nhà hàngRole nhà hàng-PermissionQuản lý chi tiết permission trong từng role của nhà hàngTài khoản liên kết nhà hàngQuản lý tài khoản liên kết thanh toán của nhà hàng, hỗ trợ việc gia hạn tự động khi đến kỳ hạn mớiYêu cầu thanh toánQuản lý yêu cầu thanh toán khi đến kỳ thanh toán của nhà hàngGiao dịch charge phíQuản lý lịch sử charge phí của nhà hàng
 

**5.State diagram **nếu thực thể nào đó có nhiều trạng thái , ví dụ ở đây là thực thể đặt chỗ, đặt món

- **Thực  thể đặt bàn**
 

- **Thực  thể đặt món**
 

Vậy chúng ta thử tìm hiểu vì sao nó lại giúp đội code hiểu được overview tốt hơn nhé

Với các bạn BA khác, thông thường khi các bạn transfer overview SP, các bạn có thể liệt kê danh sách chức năng, kèm 1 số màn hình chính. Tuy nhiên việc đó khá khó cho đội code nắm bắt được vì lượng thông tin khá nhiều, và không nhìn được các mối quan hệ giữa các đối tượng trong hệ thống, ví dụ như mình có liệt kê danh sách chức năng của SP Quản lý nhà hàng,các bạn xem  đính kèm (danh sách chức năng theo từng ứng dụng, API/Tiến trình). 

 

Khi nhìn vào ds chức năng đó, Đội code có thể nhìn thấy chức năng thêm mới gói SP, Quản lý giá gói SP. Nhưng nhìn vào tên chức năng thì khó hình dung bên trong nó như thế nào, khi thêm mới gói SP thì cần những thông tin gì, khi thiết lập giá thì cần thiết lập theo những tiêu chí gì, mà để dev biết thì phải vẽ hết rất mất thời gian

Giả sử bạn đưa ra ERD như ảnh đính kèm ở trên cho đội code xem thì ngay lập tức họ sẽ hình dung được (tất nhiên kèm mô tả + transfer của mọi người nữa, nhưng thông tin transfer nói bằng lời sẽ rất ít, nên đội code hoàn toàn xem lại ERD có thể hiểu và nhớ được)

Danh sách nhóm chức năng cần có trên hệ thống

- Quản lý đặt bàn, đặt món
- Quản lý tích điểm cho KH
- Quản lý món ăn, combo: Món ăn thì cần quản lý giá chi tiết theo size
- Quản lý tiêu chí phân hạng KH
- Quản lý công thức tích điểm
- Quản lý voucher
- Quản lý các quyền trên hệ thống
- Quản lý tính năng, 1 tính năng có nhiều quyền
- Quản lý gói sản phẩm: 1 gói sản phẩm có nhiều tính năng
- Thiết lập gói sản phẩm cho nhà hàng
- Quản lý giá gói SP
- Quản lý nhà hàng
- Quản lý role, quản lý user của nhà hàng
- Quản lý liên kết nhà hàng với các đối tác như đối tác vận chuyển, đối tác thanh toán
- Quản lý liên kết tài khoản của nhà hàng
- Quản lý charge phí nhà hàng khi sang kỳ hạn mới
- Quản lý các tham số cấu hình phục vụ quản lý linh động theo từng nhà hàng hoặc theo mong muốn của bên kinh doanh SP QL nhà hàng
Các thông tin liên quan (màn hình) với từng nhóm chức năng đó: Thay vì các bạn phải vẽ 1 loạt các màn hình để giúp đội code hình dung ra sản phẩm thì bạn chỉ cần liệt kê các trường liên quan tới từng đối tượng đó mà thôi

Với chức năng thiết lập giá, thì nhìn vào ERD, đội code sẽ hình dung ra được các thông tin liên quan đến màn hình

Chọn gói Sp cần thiết lập giá

**Nhập các thông tin: **

- Kỳ hạn
- Loại ứng dụng 
- ố lượng tài khoản sử dụng trên loại ứng dụng đó
- Và thông tin giá của gói SP dựa vào 3 thông tin trên
- Với chức năng Đặt bàn sẽ có các thông tin:
- Họ tên người đặt
- Số điện thoại người đặt
- Số người lớn
- Số trẻ em
- Giờ dự kiến tới
- Họ tên người nhận bàn
- Số điện thoại người nhận bàn
- **Các thông tin không nhập nhưng cần lưu trữ để phục vụ các ràng buộc nghiệp vụ khác**Giờ dự kiến kết thúc: Để phục vụ cho việc đặt bàn, hệ thống hiển thị bàn trống (đảm bảo không conflict thời gian mà KH khác đã đặt)
- Kênh đặt bàn: để thống kê báo cáo các kênh KH đặt bàn tại nhà hàng
**Ràng buộc nghiệp vụ có thể có**

- Khi user NV phục vụ thực hiện đặt bàn, đặt món thì cần validate nhà hàng đó có sử dụng gói SP trên ứng dụng tương ứng không, user có quyền không. Các validate này dựa vào các thực thể như Gói SP – Nhà hàng.Mặc dù các bạn sẽ làm phần đặt bàn, đặt món trước các chức năng thiết lập gói SP cho nhà hàng
Trong phạm vi 1 bài cũng không thể giải thích hết cho các bạn được, nhưng hy vọng các bạn BA đừng ngần ngại tìm hiểu các technique hữu ích như technique ERD này. Mình biết số lượng BA hiện tại chịu dùng technique này khá ít, có thể các bạn thấy như hiện tại làm cũng tốt rồi nhưng bạn hãy thử thay đổi, sẽ thấy còn có thể làm tốt hơn nhiều nữa. Như mình, các phần chi tiết có thể cắt gọt, không làm tài liệu chỉnh chu nếu dự án gấp nhưng riêng ERD luôn làm (kèm theo 1 số technique nữa như state diagram, biểu đồ luồng dữ liệu, sequence diagram nếu thực sự cần) để giúp đội code nắm tốt hơn các yêu cầu của mình. Chỉ khi 2 bên hiểu rõ ý nhau (ý của hiện tại, ý của tương lai – những thứ ưu tiên làm sau) thì khi đó requirement của bạn mới giảm tải được việc thay đổi yêu cầu, bạn cũng không thấy nản khi làm BA mà suốt ngày bị kêu là yêu cầu làm kém