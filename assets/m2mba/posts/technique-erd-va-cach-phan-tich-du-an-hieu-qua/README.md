---
id: 73
title: "Technique ERD"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T12:06:13.000Z"
source_url: "https://m2mba.com/blog/articles/technique-erd-va-cach-phan-tich-du-an-hieu-qua"
---

# Technique ERD

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T12:06:13.000Z*

Một trong những technique khá quan trọng cho các bạn BA sử dụng để phân tích và trợ giúp các bạn dev thiết kế Database đó là ERD: Entity Relationship Diagram (Biểu đồ quan hệ thực thể)

Trong diagram này có 3 thành phần chính

- Entity
- Relationship
- Atribute
- **Entity** là 1 đối tượng hay khái niệm ngoài đời thực như Nhân viên, sinh viên hay dạng khái niệm như Môn học, dự án, tài khoản …mà cần được** lưu trữ vào hệ thống. **Thực thể sẽ là 1 danh từ
- **Atribute: **Để mô tả được thông tin của 1 entity thì chúng ta cần các thuộc tính của nó, ví dụ như Nhân viên thì phải có thông tin: Mã nhân viên, Họ tên, ngày sinh, Email…
Các bạn lưu ý là entity hay attribute đều là danh từ, vậy chúng khác nhau ở điểm gì: Entity có thể đứng độc lập, còn attribute thì không thể, ví dụ con người là entity nhưng cánh tay là attribute vì con người có thể đứng độc lập thành 1 đối tượng riêng biệt, còn cánh tay thì không thể đứng độc lập mà nó phải thuộc vào 1 con người

**3.Relationship:** Diễn tả những entity nào có quan hệ với nhau và chúng được quan hệ như thế nào. 1 quan hệ thể hiện số lần xuất hiện tối đa, tối thiểu của mỗi entity trong quan hệ đó. Ví dụ như mối quan hệ giữa thực thể nhân viên và phòng ban:

- 1 nhân viên thuộc 1 phòng ban
- 1 phòng ban thì có nhiều nhân viên 
Trên đây là 1 số định nghĩa, vậy các bạn sẽ thắc mắc làm thế nào để có thể xác định được các thành phần của ERD như trên. 

Vẫn như bài trước, Biểu đồ ERD chỉ được hình thành khi các bạn đã hoàn thành bước khơi gợi yêu cầu, do đó các bạn đã có thông tin về các quy trình nghiệp vụ liên quan tới dự án mà bạn làm

Vậy điều kiện cần vẫn là quy trình đã có nhé

Sau đó các bạn thực hiện các bước sau

- Bước 1: Tìm các danh từ trong quy trình của bạn đọc được, khoanh tròn nó lại
- Bước 2: Trả lời câu hỏi: Nó có đứng độc lập được không=>nếu được thì nó là entity, nếu không phải thì trả lời tiếp: Nó mô tả cho 1 đối tượng nào khác?. Nếu có thì đó là attribute
Quan trọng nhất là các bạn xác định được các thực thể chính, sau đó attribute thì các bạn có thể khai thác thêm từ khách hàng, vì có thể trong tài liệu mà bạn tìm được có không đầy đủ

Sau khi tìm ra được các entity thì các bạn tìm ra mối quan hệ giữa các entity đó

Mình lấy tạm quy trình của tài xế grab trên trang của grab nhé, do quy trình này khá tổng quan nên thông tin lộ ra không nhiều, nhưng mình cứ tạm minh họa cho các bạn. Hình vẽ đính kèm là hình mình khai thác từ sơ đồ + 1 số quy trình khác của họ nữa (quy trình đăng ký tài xế, xem thông tin chuyến xe mà mình đã đặt…)

Mình đánh dấu các danh từ có được trong quy trình 

- Chuyến (chuyến xe): Là 1 thực thể do nó có thể coi là 1 khái niệm và nó không thuộc 1 đối tượng/khái niệm nào khác
- Khách hàng: Là 1 thực thể do nó là 1 đối tượng ngoài đời thực
- Địa điểm: Địa điểm của KH nó chính là điểm đi của chuyến xe, và nó không có ý nghĩa khi đứng riêng lẻ, nên địa điểm này coi là 1 thuộc tính của chuyến xe
- Tiền: Là giá trị của chuyến xe, giá trị chuyến xe thì phải gắn vào chuyến xe, không thể đứng độc lập được nên coi nó là 1 thuộc tính của chuyến xe
- Tài xế (không lộ diện trong quy trình nhưng đang nói về quy trình sử dụng của tài xế khi nhận cuốc xe): Là 1 thực thể do nó là 1 đối tượng ngoài đời thực
Kết hợp với 1 số quy trình nữa mình tạm xác định 1 số thực thể như : Tài xế, Xe, Chuyến xe, Khách hàng. Và với mỗi thực thể có các thuộc tính và mối quan hệ giữa các entity như trong hình