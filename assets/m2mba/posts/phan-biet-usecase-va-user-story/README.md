---
id: 69
title: "Phân biệt Usecase và User story"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T11:21:06.000Z"
source_url: "https://m2mba.com/blog/articles/phan-biet-usecase-va-user-story"
---

# Phân biệt Usecase và User story

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T11:21:06.000Z*

Trong khóa học, mình chỉ dạy về usecase và không đào tạo chuyên sâu về User story nhưng mình cũng nhấn mạnh lại với các bạn, đây chỉ là 1 cách viết khác mà thôi, còn lại mục đích cuối cùng vẫn đưa ra requirement của stakeholder, cho dev/tester nắm. Tùy 1 số bên triển khai, họ sẽ nêu user story ở dạng rút gọn, 1 số bên thì triển khai user story theo dạng viết rất chi tiết như 1 usecase thông thường. Nó thường sẽ tùy vào tính gấp rút của dự án, còn lại trong quan điểm của mình, tài liệu là 1 thứ rất quan trọng vì nó không phải phục vụ cho hiện tại mà phục vụ cho tương lai khi maintain sản phẩm, có thể ngay lúc dự án gấp rút thì chúng ta có thể tập trung communicate nhưng những dự án lớn nhiều bên tham gia thì sẽ khó mà chỉ áp dụng theo kiểu tập trung communicate, thay vào đó tài liệu sẽ cần phải khá chi tiết để confirm rõ ràng và giảm thiểu thời gian trao đổi giữa các bên.

Trong bài viết này, chúng ta hãy thử phân tích sự giống và khác nhau giữa usecase và user story

Nếu như trong waterfall thì các bạn hay có khái niệm requirement, usecase, còn ở trong Agile-scrum thì nó không dùng khái niệm trên mà thay vào đó là khái niệm user story. Về định nghĩa usecase và user story, các bạn có thể google để biết thêm vì có quà nhiều bài trên mạng. Còn dưới dây mình nêu ra các điểm giống và khác nhau, mong các bạn mổ xẻ thêm nhé

**1.Điểm giống nhau: **

- Cả 2 technique này đều nhằm mục đích nêu rõ mong muốn của người dùng đối với ứng dụng phần mềm mà chúng ta sẽ làm. User story thì cần nêu rõ phục vụ cho ai (Who), còn trong usecase thì cần nêu rõ usecase do Actor thực hiện là ai, phục vụ ai
- User story đưa ra các tiêu chí nghiệm thu để team phát triển nắm được các yêu cầu mà giải pháp cần đáp ứng. Còn trong usecase đưa ra các exception flow và post condition, bản chất Exception flow và post-condition sẽ gần tương tự với tiêu chí nghiệm thu của user story Exception flow: Đưa ra các tình huống ngoại lệ và hệ thống cần phải ứng xử với các tình huống đó
- Post condition: Đưa ra kết quả đạt được khi thực hiện usecase thành công
**2.Điểm khác nhau: **

- **User story** Tập trung vào kết quả và lợi ích mà stakeholder muốn đạt được, trong khi Use Case có thể chi tiết hơn về mô tả cách hệ thống sẽ hoạt động. Usecase thiên về mặt hệ thống, user story thiên về mặt người dùng
- User story viết theo ngôn ngữ của người dùng, ai cũng có thể đọc hiểu mục đích, nó tập trung trả lời vào câu hỏi Why, tức tại sao cần phải làm yêu cầu này và nó sẽ mang lại giá trị gì cho stakeholder, cho tổ chức. Do đó nó sẽ giúp cho các bên có thể priority được các user story với nhau. Ngoài ra, Team dev/test dựa vào tiêu chí nghiệm thu để nắm được giải pháp cần phải đáp ứng những tiêu chí gì để mang lại giá trị cho người dùng.Tuy nhiên, nếu chỉ dựa vào các thông tin trên thì team dev sẽ khó phát triển được, và cần phải communicate nhiều trong team để nắm rõ luồng chi tiết, màn hình tương ứng cho user story đó. Do đó, mình thấy hiện tại 1 số công ty thì khi viết user story sẽ bao gồm đầy đủ các mô tả như 1 usecase thông thường: Flow + Mô tả flow, mockup + mô tả mockup
- **Usecase** thiên về luồng chi tiết tác động giữa actor và hệ thống hơn. Giúp cho team dev thấy rõ các luồng chi tiết cần phải thực hiện để đáp ứng usecase. Usecase sử dụng để trả lời cho câu hỏi How, tức làm thế nào để hoàn thành được yêu cầu của Stakeholder. Nó sẽ bao gồm đầy đủ các flow: Alternative flow, exception flow=>Các flow này sẽ biểu diễn thành dạng process model cho chức năng để dev/tester nắm rõ luồng xử lý bên trong hệ thống như thế nào
Thông thường 1 user story sẽ được map 1-1 sang usecase, tuy nhiên cũng có nhiều TH 1 user story sẽ break ra thành nhiều usecase khác nhau. 

Ví dụ như 1 trang TMĐT muốn tích hợp thanh toán online cho KH thì khi phát biểu thành user story và usecase sẽ như sau:

**Ví dụ 1**

**User story**: Là Khách hàng, tôi muốn thanh toán online bằng tài khoản ngân hàng của tôi khi đặt đơn hàng để xác nhận chắc chắn đặt đơn và không phải chuẩn bị tiền mặt lúc giao hàng 

Với user story này sẽ phải xây dựng các usecase:

- Khởi tạo thanh toán sang Cổng thanh toán
- Xử lý hiển thị kết quả khi cổng thanh toán redirect về URL của trang TMĐT
- Cập nhật kết quả thanh toán từ Cổng thanh toán
User role trong User story cũng thường là Actor trong usecase, tuy nhiên 1 số trường hợp cũng không phải là 1, Ví dụ user story và usecase sau

**Ví dụ 2**

User story: Là khách hàng, tôi muốn được tự động nâng hạng VIP khi tôi tiêu dùng đạt ngưỡng của KH Vip để tôi có thể hưởng các chính sách ưu đãi 

Với user story này thì Khách hàng là user role nhưng sẽ không phải là actor, bởi vì để đạt được mục đích của actor này thì hệ thống sẽ cần xây dựng 1 usecase chạy ngầm của hệ thống dạng job “Tự động nâng hạng thẻ cho KH”. Job này sẽ thực hiện tính toán tổng tiền mà KH đã chi tiêu trong 1 khoảng thời gian quy định, nếu đạt hạng KH Vip thì hệ thống sẽ tự động nâng hạng cho KH và gửi SMS/Email thông báo cho KH

Thực ra quan điểm của mình thì BA sẽ phải flexible trong tranfer yêu cầu, và tùy thuộc vào tình hình dự án để làm tài liệu detail ở mức nào. Không quan trọng quá vào lý thuyết định nghĩa các technique đó là gì, quan trọng nhất vẫn là hiệu quả làm việc trong team nên usecase hay user story hay 1 cái gì khác nữa thì cái cần là tranfer yêu cầu 1 cách tốt nhất tại thời điểm đó của dự án