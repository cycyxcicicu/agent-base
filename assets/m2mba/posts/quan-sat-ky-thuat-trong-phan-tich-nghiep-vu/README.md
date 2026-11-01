---
id: 91
title: "Technique observation (Quan sát)"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-03T03:07:58.000Z"
source_url: "https://m2mba.com/blog/articles/quan-sat-ky-thuat-trong-phan-tich-nghiep-vu"
---

# Technique observation (Quan sát)

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-03T03:07:58.000Z*

Nghe đến 50 technique của Babok có vẻ kinh khủng, nhiều người cầm sách đọc có khi hoang mang nhưng thực tế các bạn đều đã sử dụng qua, chỉ có điều chúng ta không nghĩ nó lại là 1 cái gì đó mỹ miều được Babok cô đọng lại thành 1 technique trong phân tích nghiệp vụ

Hôm nay mình sẽ nói qua 1 technique mà rất nhiều người sử dụng, và các BA nên sử dụng technique này trong cuộc sống hằng ngày để có thể hiểu và tiếp cận các mảng nghiệp vụ khác nhau khi cần thiết. Đó là technique Observation (Quan sát). Technique này sẽ rất hiệu quả nếu ai làm bên triển khai ERP cho các doanh nghiệp sản xuất, quản lý kho bãi lớn

      Theo Babok thì Quan sát là phương pháp được sử dụng để thu thâp, khơi gợi thông tin bằng cách xem và hiểu các hoạt động, các ngữ cảnh thực hiện. Nó có thể sử dụng để xác định các yêu cầu và đưa ra các cải tiến cũng như hiểu được quy trình nghiệp vụ, thiết lập tiêu chuẩn hiệu quả, đánh giá tính hiệu quả của giải pháp hay hỗ trợ đào tạo và phát triển

      Dưới đây mình kế 1 câu chuyện thực hiện áp dụng technique này

      Tháng 4 năm ngoái mình được chuyển sang làm 1 mảng dự án với bên Tổng công ty Bưu điện Việt Nam về hệ thống chi trả lương hưu qua thẻ từ. Ai có bố mẹ nhận lương hưu tại Hải Dương và Hà nội đều có thể nghe các cụ nói qua. Thay vì các cụ cầm quyển số BHXH để đi nhận lương thì giờ đây các cụ cầm cái thẻ để nhận lương vào các ngày lĩnh quy định của BHXH và Vnpost. 

       Mình vào sử dụng hệ thống hiện tại, và note lại các vấn đề mình thấy bất cập, trong đó có 1 cái note: Chưa có Popup xác nhận khi thực hiện chi trả : “Xác nhận chi trả tiền cho cụ xxx”. Tại thời điểm đó mình nghĩ: Sao mọi người có thể thiếu sót 1 điều cơ bản khi làm hệ thống như thế. Nhưng sau 1 buổi đi hỗ trợ triển khai thì mình đã hiểu nguyên nhân

       Số lượng các cụ nhận lương hưu bằng tiền mặt rất lớn, lại với tâm trạng hoan hỉ được đi nhận lương, để gặp gỡ bạn bè trong hội, các cụ thường đi rất sớm=>7h sáng mình có mặt tại điểm chi trả thì đã có khoảng gần 50-100 cụ ngồi chờ rồi=>Tốc độ xử lý giao dịch cần phải rất nhanh, phải giảm bớt các thao tác của Nhân viên chi trả nên việc xác nhận là hoàn toàn không cần thiết. Vậy các bạn sẽ đặt câu hỏi, không có xác nhận, nhân viên làm nhầm thì sao. Thực ra việc nhân viên làm nhầm là có, nhưng sẽ ít hơn rất nhiều số lần làm đúng, nên thay vì phải xác nhận thì bỏ xác nhận và cho hủy GD được khi làm sai.

Ngoài ra sau khi quan sát thì về mình cũng đưa ra 1 số cải tiến khác như

1.Những nhân viên tham gia chi trả là những người trung tuổi và sử dụng máy tính không nhiều, không thuần thục, do đó 

- Việc thể hiển các icon trên giao diện làm người dùng khó thao tác=>Chuyển tất cả các icon về tên nút rõ ràng, để người dùng nhìn là biết nút nào làm gì, thay vì đưa con trỏ chuột lại icon và nhìn tooltip (chưa kể người dung còn không biết đưa con trỏ lại có thể nhìn thấy tooltip :D)
- Font chữ cần to, rõ ràng để họ có thể nhìn được dễ dàng
- Hỗ trợ các phím tắt để không phải dùng chuột mất time, và các phím tắt sẽ áp dụng giống với phần mềm trước đã sử dụng (do họ đã quen và tất nhiên cũng theo chuẩn phím tắt của Microsoft)
2.Do áp lực chi trả rất cao nên các thao tác trên hệ thống phải mặc định làm sao nhanh nhất cho người sử dụng: 

- Với những người chi trả có ủy quyền: Thông thường khi họ ủy quyền cho người khác đi nhận (thường là vợ/chồng hoặc bác tổ trưởng tố đân phố) thì người được ủy quyền sẽ đi nhận thay cho người đó=>Mặc định thông tin là người lĩnh tiền là người được ủy quyền
3.Tại thời điểm đó, Phía cty mình và đối tác đang tập trung làm ứng dụng chi trả online, nhưng qua quan sát khi đi hỗ trợ thì mình về báo PM xác nhận lại với đối tác để tập trung nguồn lực xử lý những vấn đề cần thiết trước, vì chắc chắn trong tương lai gần ứng dụng chi trả online chưa phải là cái ưu tiên số 1, thay vào đó sẽ là ứng dụng chi trả offline

Vì ap lực chi trả cao, thời gian xử lý phải nhanh, nếu dùng hệ thống online, các rủi ro về mạng, thời gian upload dữ liệu qua mấy hệ thống sẽ rất rủi ro=> Nếu xảy ra lỗi sẽ khó khắc phục, các cụ sẽ rất khó chịu

Và sau đó, đối tác cũng thừa nhận tại thời điểm này chỉ nên tập trung vào ứng dụng chi trả offline. Sau hơn 1 tháng các dev tập trung làm việc, bọn mình cũng đưa ra được sản phẩm tạm hài lòng KH. Tất nhiên sau đó vẫn còn nhiều vấn đề để xử lý, nhưng ít nhất, hệ thống mới đã cho họ trải nghiệm hoàn toàn khác.

Dưới đây là mình tổng hợp lý thuyết từ sách Babok về technique Observation, mọi người tham khảo nhé

**Cách tiếp cận thực hiện Observation**

**Các bước thực hiện kỹ thuật Observation**

 

**Ưu và nhược điểm của Observation**