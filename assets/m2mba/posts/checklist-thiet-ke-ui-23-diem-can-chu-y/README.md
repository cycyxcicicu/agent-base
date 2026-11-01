---
id: 93
title: "Checklist thiết kế UI"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-03T04:03:26.000Z"
source_url: "https://m2mba.com/blog/articles/checklist-thiet-ke-ui-23-diem-can-chu-y"
---

# Checklist thiết kế UI

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-03T04:03:26.000Z*

Chiều nay ngồi đọc sách “The 23-Point UX design Checklist”. Mình có tổng hợp 1 số lưu ý khi các bạn vẽ Mockup hay mô tả mockup đó để các bạn dev thực hiện nhé

- **Rule 1:** Repetitive actions or frequent activities feel effortless. Giúp cho các hành động lặp đi lặp lại được thực hiện 1 cách dễ dàng hơn: 1 số hành động của user được lặp đi lặp lại, và để cho KH bớt phải thao tác nhập liệu, các bạn có thể thiết lập giá trị sẵn cho KH (thường trong khóa học mình hay nêu là Giá trị mặc định của các control khi load màn hình).
- **Rule 2**: Users can easily recover from errors. Cho phép KH có thể quay trở lại màn hình trước đó để hủy bỏ 1 số thao tác mà KH thực hiện nhầm
- **Rule 7**: Visual hierarchy directs the user to the required action. Cây phân cấp của ứng dụng, hay có thể gọi là menu ứng dụng, Các bạn nên gom nhóm các chức năng gần giống nhau vào cùng 1 menu để người dùng có thể hiểu được cần vào menu nào khi cần thao tác 1 tính năng nào đó
- **Rule 8**: Items on top of the visual hierarchy are the most important. Những Item ở top hay ở màn hình Trang chủ sẽ là những chức năng quan trọng nhất của ứng dụng đó
- **Rule 9:** Primary action is visually distinct from secondary actions. Với các hành động khác nhau thì cần có sự phân biệt, với những hành động chính của màn hình đó sẽ có màu nổi bật hơn những hành động còn lại
- **Rule 11**: Form submission is confirmed in a visually distinct manner. Với mỗi màn hình có nhập liệu đầu vào, bạn phải đảm bảo có màn hình xác nhận khi kết quả GD thực hiện thành công và thất bại để thể hiện rõ cho KH biết GD đã được kết thúc
- **Rule 12**: Alert messages are consistent. Với các thông báo, cầ n phải đồng nhất về style thông báo kèm với vị trí thông báo
Các bạn có thể tìm hiểu thêm các rule khác trong sách hoặc search Usability Heuristic để tìm hiểu thêm nhé

Nói chung 1 ứng dụng cần phải

- Đồng nhất về cách thiết kế màu sắc, font chữ, flow người dùng trên từng màn hình. Không nên quá nhiều màu, rối mắt
- Các icon sử dụng nên theo chuẩn chung, để mọi người dễ hiểu, dễ nhận diện
- Đồng nhất về styple, vị trí hiển thị message thông báo kết quả GD thành công, thất bại
- Mỗi khi submit cần thể hiện rõ trạng thái hiện tại của GD đang thực hiện (thành công, thất bại, Processing)
- Gom nhóm các menu giống nhau, với chức năng hay được thao tác thì có thể có thêm phần menu thao tác nhanh giúp người dùng có thể làm nhanh, thay vì phải đi như luồng bình thường
- Cố gắng giảm số bước thao tác của KH bằng cách mặc định các giá trị input thay vì để Người dùng phải nhập liệu
Dưới đây là 1 số ảnh phân tích trên 1 số ứng dụng mapping vào các rule ở trên

- **Rule 1: **
Giúp giảm thiểu việc nhập liệu của KH dựa vào các hành động lặp đi lặp lại của KH
1.Màn hình đăng nhập của Vietcombank và ViettelPay đều mặc định tài khoản Đăng nhập của KH
2.Màn hình Nạp tiền điện thoại của VTP: mặc định là số điện thoại của KH đang sử dụng Ví
3.Báo cáo giao dịch: Mặc định để KH tra cứu GD trong vòng 1 tuần

- **Rule 2**: Tại mỗi màn hình đều có nút Back để Người dùng có thể quay về màn hình trước đó. Và trước khi để Người dùng chăc chắn thực hiện GD, ứng dụng sẽ hiển thị màn hình xác nhận. Trên màn hình cần có 2 nút với ý nghĩa là Đồng ý hoặc hủy bỏ thao tác đó
 

- **Rule 7: **Menu Thanh toán Hóa đơn có menu con tương ứng trong hình. Nó sẽ gom nhóm các tính năng gần giống nhau vào cùng 1 menu để Người dùng biết mình nên thao tác ở menu nào khi cần thực hiện 1 tính năng nào đó
- **Rule 7: **Menu Chuyển tiền có menu con tương ứng trong hình. Nó sẽ gom nhóm các tính năng gần giống nhau vào cùng 1 menu để Người dùng biết mình nên thao tác ở menu nào khi cần thực hiện 1 tính năng nào đó
- **Rule 8: **Các chức năng quan trọng nhất được đặt ở màn hình đầu tiên, ví dụ như trong hình các chức năng trong 2 khung đỏ là chức năng hay được sử dụng nhất, hoặc quan trọng nhất của ViettelPay
 

- **Rule 11: **Khi summit 1 form nào đó, chúng ta cần có màn hình thông báo kết quả rõ ràng cho Người dùng, để biết được GD thành công hay thất bại và để người dùng biết GD đã kết thúc
 
 

- **Rule 12**: Các nội dung cảnh báo đều cần cùng 1 style và hiển thị ở cùng 1 vị trí đồng nhất trong cả ứng dụng