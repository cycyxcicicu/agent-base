---
id: 80
title: "Định nghĩa về BA"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-26T12:32:30.000Z"
source_url: "https://m2mba.com/blog/articles/tong-quan-ve-nghe-ba"
---

# Định nghĩa về BA

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-26T12:32:30.000Z*

BA là gì

Theo định nghĩa của sách BABOK: Business analysis is the practice of enabling change in an enterprise by defining needs and recommending solutions that deliver value to stakeholders

Và: A business analyst is any person who performs business analysis tasks

Vậy thì công việc BA đó chính là việc phải xác định được nhu cầu của tổ chức/stakeholder và từ đó đưa ra được giải pháp mang lại giá trị cho stakeholder, cho tổ chức. Việc giải pháp đưa ra có thể là 1 phần mềm hoặc có thể chỉ là cải tiến quy trình, công việc hiện tại của tổ chức, nhưng hiện tại khi nghề với JD là BA/PO thì chủ yếu làm trong lĩnh vực phần mềm, tức đưa ra giải pháp ở đây là phần mềm nên các bạn muốn làm BA thì nên có chút hiểu biết về phần mềm, những thứ phần mềm có thể làm được, để làm được việc đó thì nên sử dụng phần mềm nhiều vào nhé

Việc xác định nhu cầu (Define need) thường BA sẽ cần quan tâm tới các vấn đề mà tổ chức đang gặp phải, cần phải có giải pháp để cải thiện các vấn đề đó hoặc vấn đề bên ngoài thị trường đang gặp phải và tổ chức muốn nắm bắt cơ hội xử lý được vấn đề đó để mang lại lợi ích cho thị trường và cho tổ chức. Từ đó mới đưa ra giải pháp cụ thể giải quyết vấn đề đó 

**Vấn đề của tổ chức**: Ví dụ như với trung tâm đào tạo của mình, thời gian đầu triển khai số lượng học viên khá ít nên việc quản lý bằng excel không có vấn đề gì, và các học viên thường đăng ký là học luôn, nhưng sau này số lượng học viên nhiều lên, các học viên thường xuyên đăng ký bảo lưu, việc kiểm soát rất khó, rồi mình triển khai việc chữa bài 1-1, dẫn tới việc hay bị miss bài học viên (nếu học viên làm quá chậm, hoặc không kiểm soát được học viên nào làm bài lặp hay không – ví dụ cố tình nộp 2 lần – chắc ko có đâu, nhưng BA mà phải nghĩ tình huống đó :D). Từ đó mình mong muốn cần xây dựng hệ thống để quản lý được học viên, quản lý được việc chữa bài tập về nhà cho học viên

**Cơ hội cho doanh nghiệp từ vấn đề của thị trường:** Hay giả sử như 1 Doanh nghiệp nhà sách nhìn thấy hiện tại văn hóa đọc sách đang ngày càng tăng, việc thường xuyên mua sách, đặc biệt sách mới sẽ tốn khá nhiều chi phí cho các GĐ, và các GĐ mong muốn là có thể mua các sách cũ hoặc chỉ thuê sách thôi. Nhận thấy cơ hội đó thì nhà sách phát triển ra hệ thống kết nối giữa những người mua bán sách, đầu tiền thì sẽ bán sách nội bộ của doanh nghiệp, dần dần phát triển ra nhiều nhà sách doanh nghiệp hoặc cá nhận  khác

 

Các bạn BA khi được giao nhiệm vụ làm hệ thống nào đó thì cần hiểu rõ vì sao mình được giao làm sản phẩm đó, vấn đề/cơ hội gì đang cần mình giải quyết, từ đó mới đi đúng hướng được, tránh làm theo, copy của 1 bên nào đó. Copy thì cũng phải cần biết cái gì copy được, cái gì phù hợp triển khai trong mô hình tổ chức của mình, nên thực sự mình chỉ nên tham khảo của các bên tương tự chứ ko gọi là bê nguyên được

Ở trên là mình ví dụ về việc Need ở high level, còn khi BA phân tích để ra được giải pháp, tính năng cụ thể thì cần phân tích được ở detail level

Mình ví dụ trường hợp sau: Mình triển khai chữa bài 1-1 cho từng học viên, và gần như không giới hạn deadline cho học viên, học viên làm chậm bao lâu mình vẫn chữa. Mỗi tuần sẽ có 1 BTVN theo nội dugn tuần, và các bạn sẽ nộp lên file google sheet theo từng tuần như ảnh bên dưới, và mentor hay gặp vấn đề đó miss bài học viên. Vậy khi BA nghe vấn đề đó thì cần tìm hiểu kỹ công việc của mentor làm như thế nào mà lại bị miss bài, để từ đó có giải pháp phù hợp

 

Bước 1: Mentor giao bài cho học viên sau khi kết thúc tuần học tương ứng

Bước 2: Học viên làm bài nộp bài tập về nhà trên google sheet theo sheet của tuần tương ứng 

Bước 3: Mentor check BTVN theo tuần gần nhất, check các bài nộp mới trước rồi sẽ check các bài sửa. Các bài sửa sẽ dựa vào phần reply của học viên ở cột F =>Vấn đề phát sinh ở đây là mentor có thể check sót do các bài cũ học viên sửa lại, khi check trên danh sách nhiều bài thì mentor sẽ check phần phản hồi ở cột F bị thiếu sót=>Miss bài của học viên

Bước 4: Mentor comment vào từng bài làm qua file google docs. Sau đó sẽ nhận xét chung ở cột E  và đánh dấu số lần đã comment

Bước 5: Học viên check comment và sửa bài và lại tiếp tục lặp lại bước 3

Với vấn đề ở bước 3, và bây giờ giải pháp triển khai trên hệ thống thì sẽ cần phải làm như thế nào, đó là việc BA cần tư duy, giải quyết 1 vấn đề nhưng khi sử dụng phần mềm sẽ cần phải xây dựng 1 bộ các chức năng kết hợp với nhau thì mới xử lý được tới gốc vấn đề đó

và ví dụ như giải pháp đưa ra sẽ gồm các chức năng CHÍNH như dưới đây (cho cả ứng dụng dành cho mentor và ứng dụng dành cho học viên)

**1.Mentor giao bài**

Hàng tuần, sau khi học xong, mentor sẽ vào hệ thống để giao bài cho học viên

****

**2. Học viên Nộp bài/sửa bài **

Học viên sau khi được giao bài sẽ xem nội dung BTVN và sau đó thực hiện làm bài và nộp bài trên hệ thống

**3.Mentor xem Danh sách các BTVN cần chữa**

Thay vì trước đây mentor phải vào google sheet thì giờ sẽ xem danh sách các bài làm của học viên trên hệ thống và sẽ Ưu tiên hiển thị các bài vừa mới nộp, và vừa sửa lại lên đầu

 

**4.Mentor đánh giá bài**

 

Qua ví dụ trên các bạn thấy rằng để giải quyết được vấn đề mà stakeholder đưa ra (miss bài học viên) thì BA sẽ cần phải tìm hiểu detail công việc mà stakeholder làm liên quan tới việc chữa bài, để từ đó đưa ra giải pháp phù hợp. Để làm được việc này, thông thường các bạn BA cần phải tìm hiểu quy trình/công việc hiện tại của stakeholder, các vấn đề stakeholder gặp phải qua các công việc họ làm hằng ngày, lý do vì sao họ gặp vấn đề đó, để từ đó đưa ra được giải pháp phù hợp (Ví dụ như miss bài cần chữa nên danh sách các bài mới nộp và mới sửa sẽ được đẩy lên đầu danh sách với trạng thái cụ thể để mentor soát được)

 

Công việc của BA là làm sao đưa ra giải pháp phù hợp để giảm bớt công việc, sai sót của stakeholder, giúp mọi hoạt động tối ưu hơn, minh bạch hơn, thông tin trao đổi trong suốt giữa những người liên quan thông qua  phần mềm (tất nhiên nhiều TH được giải quyết không cần dùng phần mềm)

 

Từ những yêu cầu ở mức high level, BA sẽ có nhiệm vụ khơi gợi yêu cầu với các stakeholder, hoặc tìm hiểu, phân tích các tài liệu của stakeholder cung cấp hoặc trên mạng, để từ đó tổng hợp và phân tích yêu cầu, đưa ra giải pháp phù hợp nhất cho tổ chức ở thời điểm đó (là giải pháp phù hợp nhất chứ ko phải tốt nhất, vì để xây dựng và triển khai 1 phần mềm hoàn hảo không thể làm 1 sớm 1 chiều, mà cần cả quá trình, BA là người phải biết cân đối giữa cái hiện trạng tổ chức, timeline mong muốn của stakeholder, để từ đó phân chia giai đoạn triển khai cho sản phẩm 1 cách phù hợp, đó là cái khó của BA, 1 đầu vào không thực sự rõ ràng nhưng cần cho 1 đầu ra rõ ràng để dev/tester có thể thực hiện được

Trong team phần mềm, BA như là người đưa ra đầu bài, dev sẽ là người giải bài toán đó, tester sẽ chấm điểm bài làm, và sau đó BA lại nghiệm thu lại xem bài toán giải đúng hay chưa, sau đó sẽ giao tiếp cho stakeholder sử dụng để xem thực sự cách giải của team đã đáp ứng mong muốn của họ hay chưa? BA sẽ là người phải giao tiếp với rất nhiều bộ phận khác nhau (bộ phận của team phần mềm: Project manager, developer, tester, Quality assurance hay bộ phần của team kinh doanh/nghiệp vụ như các phòng ban bộ phận có liên quan đến yêu cầu giải pháp phần mềm, các bộ phận pháp chế, BGĐ…và họ sẽ cần phải thu thập các thông tin từ các nguồn đó để sau đó tổng hợp và cân đối, dung hòa được các yêu cầu, trong từng giai đoạn khác nhau, biết cái gì ưu tiên ở giai đoạn này, cái gì có quan trọng nhưng chưa cần làm ngay

Các đầu ra mà BA sẽ cần có trong quá trình thực hiện

- **Kế hoạch thực hiện công việc của BA** (BA leader sẽ làm việc này): Với mỗi dự án thì cần có kế hoạch thực hiện ngay từ đầu (kế hoạch có thể thay đổi trong quá trình thực hiện nhưng team luôn cần define ra trước các mốc quan trọng, mốc quan trọng của BA như timeline trao đổi nghiệp vụ với các phòng ban bộ phận, timeline hoàn thành tài liệu phân tích yêu cầu kinh doanh/nghiệp vụ ở high level…)
- **Tài liệu phân tích yêu cầu kinh doanh** (high level - business requirement): BRD (Business requirement document), Product Vision, Business Case
- **Tài liệu mô tả yêu cầu:** SRS, FRS, hay User Story , trong các tài liệu này các bạn cần phải vẽ màn hình để mô tả cho dev hiểu rõ yêu cầu của mình (thuật ngữ tìm hiểu:  ,Wireframe/ Prototype)
- **Tài liệu quản lý yêu cầu dự án**: Để nắm các yêu cầu của BA, cái nào đã làm, cái nào đang làm/chưa thực hiện. Phần mềm cũng như các công việc của dự án khác, luôn cần phải quản lý tiến độ, công việc của dự án và BA sẽ làm nhiệm vụ theo dõi xem yêu cầu của mình đưa ra đã xử lý tới đâu qua tài liệu quản lý yêu cầu dự án
- **Tài liệu HDSD:** Sau khi hoàn thành phần mềm, BA có thể sẽ cần phải viết HDSD để gửi tới cho stakeholder sử dụng 
- **Kịch bản nghiệm thu: **BA sẽ cần nghiệm thu lại yêu cầu mình đưa ra, dev đã làm đúng chưa, để làm được việc đó thì BA sẽ cần nghiệm thu, và trước khi nghiệm thu thì BA sẽ cần viết kịch bản nghiệm thu để chuẩn bị kiểm tra theo từng kịch bản đó trên hệ thống mà dev bàn giao
 

Trước khi làm BA, các bạn có thể có nhiều kỹ năng chưa tốt như giao tiếp, tổng hợp thông tin, quản lý công việc, nhưng nếu bạn quyết tâm và yêu nghề và theo được nghề BA thì những kỹ năng đó của các bạn sẽ cải thiện dần, và giúp ích cho các bạn nhiều trong công việc cũng như cuộc sống. 

Hy vọng bài viết này giúp các bạn hiểu được sơ lược về nghề BA