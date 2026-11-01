---
id: 92
title: "Nguyên nhân BA đưa ra requirement không tốt"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-03T03:28:17.000Z"
source_url: "https://m2mba.com/blog/articles/nguyen-nhan-ba-dua-ra-requirement-khong-tot"
---

# Nguyên nhân BA đưa ra requirement không tốt

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-03T03:28:17.000Z*

Các nguyên nhân dẫn tới BA đưa ra requirement không tốt thường như sau

- **Hỏi không đúng người**
- **Tập trung vào giải pháp, không phải problem**: Chúng ta chỉ đưa ra được giải pháp khi chúng ta hiểu vấn đề thực sự đang gặp phải là gì. Nhiều bạn tham khảo bên khác và đưa giải pháp bên khác vào bên mình=>điều này sẽ dần tới  không tập trung vấn đề mà doanh nghiệp mình đang gặp phải, đang muốn xử lý
- **User đưa ra giải pháp, không đưa ra requirement: **Stakeholder chỉ là người cung cấp quy trình, công việc, các vấn đề họ gặp phải, các nhu cầu của họ mà phần mềm cần đáp ứng, chứ ko nêu ra giải pháp cần làm gì, làm như thế nào (Ví dụ làm chức năng gì), vì họ không phải là người chuyên làm IT để làm được việc này, do đó BA không nên để user dẫn dắt theo các giải pháp của họ
- **BA không có kiến thức về domain tương ứng:** các giải pháp sẽ tập trung vào domain nào đó, do đó BA muốn làm tốt thì cần phải có kiến thức domain đó
- **BA không biết cách đặt câu hỏi: **Các yêu cầu được tìm ra từ các câu trả lời của stakeholder, và để có câu trả lời thì bắt buộc phải biết đặt đúng câu hỏi, các bạn BA mới vào nghề thường sẽ gặp vấn đề này
- **Lấy yêu cầu chỉ từ 1 người**: Có thể BA chỉ được giao làm đầu mối với 1 người, từ đó BA luôn tập trung hỏi người đó mà ko giao tiếp với những người liên quan khác, điều này có thể làm chậm trễ quá trình cũng như việc người đó hiểu nhầm ý mình hỏi và khi trao đổi lại với người trực tiếp liên quan tới nhu cầu đấy thì lại nói sai ý. Việc này BA cực kỳ hạn chế, trừ khi là không thể có giải pháp nào khác
- **User không nói toàn bộ mọi thứ cho bạn: **vì họ chưa đặt niềm tin vào BA hoặc họ có thể gặp 1 số bất lợi khi giải pháp triển khai
- **User không biết nên nói gì với các bạn là đủ** vì thực tế user đâu biết bạn cần thông tin gì, nên BA sẽ là người phải biết đặt câu hỏi để họ nói ra đủ thông tin mình cần
- **Không quản lý được scope**: BA không nắm vững scope và bị stakeholder đưa ra các yêu cầu ngoài scope vẫn tiếp nhận, dẫn tới yêu cầu ngày càng phình ra, và không quản lý được
- **User không biết họ muốn cái gì: **Vì ở  giai đoạn đầu, họ đang có quá nhiều ý tưởng, thành ra lại không biết mình muốn gì, từ đó BA đưa ra requirement không rõ ràng. Trong TH này thì hoặc BA chủ động tìm hiểu về các ý tưởng liên quan tới vấn đề mà họ đang muốn xử lý, để có thể gợi ý cho user, hoặc cả 2 bên chấp nhận sẽ vừa làm vừa dò, để tìm ra cái thực sự mình mong muốn là gì 
Một trong những vấn đề mà dễ gây ra việc đưa ra yêu cầu kém chất lượng đó là user là người cung cấp requirement, BA chỉ là người thu thập chúng thôi. 

Ví dụ như trường hợp sau thì BA chỉ đơn giản là người viết tài liệu chứ không phải làm việc phân tích như trong tên gọi role của chúng ta:

BA tìm gặp những người liên quan và hỏi họ, họ cần những chức năng gì, bạn note lại và ghi rõ các yêu cầu của user. Sau đó bạn tổng hợp lại các yêu cầu và xem loại bỏ các yêu cầu nào trùng lặp nhau. TIếp đến, BA thực hiện tổng hợp lại và viết lại thành 1 tài liệu và gửi cho stakeholder để đảm bảo là yêu cầu đã được viết 1 cách chính xác. Sau đó thì stakeholder bổ sung thêm 1 số thông tin (thêm 1 số thông tin  mới vào yêu cầu cũ hoặc thêm 1 số yêu cầu mới), khi đó BA sẽ bắt đầu gặp khó khăn.  Cuối cùng BA đưa tài liệu đã viết ra cho người phê duyệt, tài liệu được phê duyệt, BA đưa yêu cầu đó cho đội dev và đội dev thực thi

Có 2 vấn đề trong trường hợp này:

- Vấn đề 1: BA chưa thực hiện phân tích yêu cầu của KH như tên gọi của role chúng ta
- Vấn đề 2: Có thể gọi là trầm trọng hơn đó là yêu cầu đã có , đã được ai đó thực hiện đưa ra yêu cầu. Điều này có nghĩa KH đã có yêu cầu, mặc dù họ không biết họ đang làm gì, 
Trong quá trình thu thập yêu cầu, chúng ta giả định rằng user đã biết được các vấn đề và đưa ra giải pháp phù hợp cho vấn đề đó. Hơn nữa, User có thể thể hiện được requirement mà đội phát triển có thể thực thi được

**User không đưa ra giải pháp,bởi vì:**

- Họ có cái nhìn phiến diện, họ chỉ nhìn được dưới góc độ của họ chứ không nhìn trong 1 bức tranh tổng thể được
- Người có thể đưa ra được vấn đề tốt nhất đang gặp phải thì lại không phải là người được giao nhiệm vụ cung cấp requirement
- User không biết IT làm gì ,có thể làm được gì. 
- Họ không muốn commit 1 hoặc nhiều yêu cầu cụ thể nào bởi vì họ sợ việc họ sẽ phải chịu trách nhiệm với chúng
- Họ không biết công nghệ nào có thể sử dụng được
 

Dưới đây là 1 số nhóm nội dung mà BA có thể sử dụng để khơi gợi yêu cầu tốt hơn: 

- Vấn đề là gì
- Đã có cách xử lý vấn đề này về mặt kinh doanh chưa
- Những rủi ro gặp phải khi xẩy ra vấn đề này
- Nếu như vấn đề này không xử lý hoặc xử lý chậm thì như thế nào, ảnh hưởng ra sao
- Có ràng buộc về kinh doanh nào không
- Ai là người chịu trách nhiệm về vấn đề này
- Vấn đề này xảy ra khi nào, bao lâu xảy ra 1 lần
 

Cụ thể 1 số câu hỏi với 1 số đối tượng

- **Manager:**Hiện tại công ty/phòng ban đang gặp những vấn đề gì
- Vấn đề này ảnh hưởng như thế nào tới hoạt động của công ty
- Nếu không xử lý thì sẽ dẫn tới những rủi ro gì cho tổ chức
- Khi nào thì vấn đề này xảy ra, tần suất ra sao
- Đã có phương án nào để tạm khắc phục chưa
- các stakeholder liên quan tới các quy trình trong tổ chức : và câu hỏi đặt ra để hiểu quy trình làm việc của họ Với công việc A trong quy trình: Để thực hiện việc này thì bạn cần/nhận thông tin từ bộ phận nào trước đó (input). Thông tin cụ thể như thế nào: (chi tiết input)
- Các bước bạn cần thực hiện như thế nào (process)
- Bên nào sẽ thực hiện tiếp sau khi bạn thực hiện công việc của bạn xong (output)
- Ngoài bạn có thể thực hiện công việc này thì có ai có thể thực hiện được nữa không, và nếu họ được phép thì các bước họ thực hiện có giống  như bạn không, nếu không giống thì các bước như thế nào
- Bạn thấy có vấn đề gì trogn luồng hoạt động hiện tại, nguyên nhân do đâu
- Dữ liệu báo cáo thống kê nào bạn đang sử dụng khi hoàn thành công việc này, cho xem dữ liệu cụ thể trên báo cáo (chủ yếu là xin field cần trong báo cáo)
- Bạn có HDSD hay checklist nào liên quan tới công việc này không
- Bạn có sử dụng những template nào trong các step thực hiện không