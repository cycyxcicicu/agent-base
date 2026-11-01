---
id: 131
title: "Luồng xử lý notification qua firebase"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-04-12T09:11:27.000Z"
source_url: "https://m2mba.com/blog/articles/luong-xu-ly-notification-qua-firebase"
---

# Luồng xử lý notification qua firebase

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-04-12T09:11:27.000Z*

## 1.Giới thiệu

Firebase Cloud Messaging (FCM) là một giải pháp nhắn tin đa nền tảng cho phép bạn gửi tin nhắn một cách đáng tin cậy mà không tốn phí.

Với Firebase Cloud Messaging (FCM), bạn có thể thông báo cho ứng dụng client rằng có email mới hoặc dữ liệu khác có sẵn để đồng bộ hóa. Bạn có thể gửi tin nhắn thông báo để tăng sự tương tác và giữ chân người dùng.

Ví dụ về việc sử dụng Firebase Cloud Messaging (FCM):

- **Thông báo ứng dụng di động**: Khi bạn muốn thông báo cho người dùng về một tin nhắn mới trong ứng dụng nhắn tin, bạn có thể sử dụng FCM để gửi thông báo ngay lập tức tới ứng dụng của người dùng. Tin nhắn có thể chứa nội dung như tên người gửi, nội dung tin nhắn ngắn, hoặc một liên kết dẫn đến nội dung chi tiết trong ứng dụng.
- **Cập nhật nội dung ứng dụng**: Khi có một cập nhật mới trong ứng dụng, như tin tức mới, bài viết blog, hoặc sản phẩm mới trong một cửa hàng trực tuyến, bạn có thể sử dụng FCM để thông báo cho người dùng về những cập nhật này. Điều này giúp giữ chân người dùng và khuyến khích họ quay lại ứng dụng.
- **Nhắc nhở sự kiện**: Nếu bạn có một ứng dụng quản lý lịch hoặc sự kiện, bạn có thể sử dụng FCM để nhắc nhở người dùng về các sự kiện sắp diễn ra, như cuộc họp, cuộc hẹn, hoặc các sự kiện quan trọng khác.
- **Gửi thông báo cá nhân hóa**: Bạn có thể sử dụng FCM để gửi thông báo cá nhân hóa dựa trên sở thích hoặc hành vi của người dùng. Ví dụ, nếu một người dùng thường mua một loại sản phẩm nhất định, bạn có thể gửi thông báo khi có giảm giá hoặc ưu đãi cho sản phẩm đó.
## 2.Luồng xử lý

 

- **Notification console GUI hoặc Admin SDK/HTTP**: Firebase Cloud Messaging (FCM) có một công cụ gọi là Notifications composer (trình soạn thông báo) cung cấp một giao diện người dùng (GUI) cho phép người dùng tạo và gửi thông báo. Công cụ này giúp bạn dễ dàng thiết lập thông báo, bao gồm tiêu đề, nội dung, hình ảnh và các tùy chọn khác, sau đó gửi chúng đến ứng dụng khách. Tuy nhiên, để hỗ trợ đầy đủ cho tất cả các loại thông báo và tự động hóa quá trình gửi thông báo, bạn có thể xây dựng yêu cầu thông báo trong môi trường máy chủ tin cậy bằng cách sử dụng Firebase Admin SDK hoặc giao thức máy chủ FCM. Firebase Admin SDK là một bộ công cụ phát triển phần mềm (SDK) cho phép bạn quản lý và tương tác với các dịch vụ Firebase từ môi trường máy chủ của bạn. Nó cung cấp giao diện lập trình dễ sử dụng để truy cập và thao tác các dịch vụ Firebase. Đội lập trình viên sẽ thực hiện tích hợp bộ thư viên Firebase Admin SDK vào môi trường máy chủ hoặc backend của ứng dụng của bạn
- **FCM Backend**:Đây là phần phụ trách việc chấp nhận các yêu cầu thông báo từ máy chủ ứng dụng của bạn.
- Sau đó, nó thực hiện phân phối (fanout) thông báo thông qua các chủ đề (topics) hoặc đến danh sách các thiết bị cụ thể.
- Backend cũng tạo ra MessageID để theo dõi và quản lý thông báo.
- **Platform-level message transport **:  Sau khi nhận yêu cầu từ máy chủ ứng dụng, FCM phân phối thông báo đến các thiết bị khách được chỉ định. Thông báo có thể được gửi đến ứng dụng khách dựa trên các tiêu chí như nhóm người dùng, danh sách thiết bị, hoặc dựa trên nội dung của yêu cầu thông báo.
- Lớp vận chuyển bao gồm:**Lớp vận chuyển Android (ATL)**: Được sử dụng để gửi thông báo đến các thiết bị Android có Google Play Services.
- **Apple Push Notification service (APNs)**: Được sử dụng để gửi thông báo đến các thiết bị Apple (iOS, iPadOS, watchOS, macOS).
- **Giao thức Web push**: Được sử dụng để gửi thông báo đến các ứng dụng web (web apps) thông qua giao thức web push.
- **Ứng dụng client nhận thông báo**:. Firebase Cloud Messaging (FCM) SDK được cài đặt trên ứng dụng **client** (ứng dụng của người dùng) để cho phép ứng dụng nhận và xử lý thông báo được gửi từ FCM. Khi bạn tích hợp FCM SDK vào ứng dụng client, bạn có thể:**Nhận thông báo**: Ứng dụng client có thể nhận được thông báo từ FCM và xử lý chúng.
- **Xử lý thông báo**: Ứng dụng client có thể tùy chỉnh cách xử lý thông báo khi nhận được, tùy thuộc vào trạng thái của ứng dụng (foreground – là đang ở trong ứng dụng đó hoặc background – là ở MH Home hoặc MH lock) và các logic cụ thể của ứng dụng.
- **Tương tác với người dùng**: Thông qua FCM SDK, ứng dụng client có thể hiển thị thông báo cho người dùng một cách phù hợp, giúp tương tác hiệu quả với người dùng.
 

Đọc đến đây chắc 1 số bạn sẽ lăn tăn hỏi là làm thế nào FCM transport layer có thể nhận diện được message đó được chuyển tới thiết bị nào phải ko, vì ở trên mới nói luồng, nhưng chưa có dấu hiệu nhận biết là message đó sẽ đi về thiết bị A hay thiết bị B, vì không phải 1 message tất cả các thiết bị đều nhận được

Vậy nên chúng ta sẽ sang 1 khái niệm đó là khái niệm về Token

## **3.Registration token**

Trong Firebase Cloud Messaging (FCM), **token** là một mã định danh duy nhất được gán cho mỗi thiết bị hoặc ứng dụng để cho phép FCM gửi thông báo đến thiết bị hoặc ứng dụng cụ thể đó. Đây là cách token hoạt động và cơ chế sinh, quản lý token:

- **Sinh token**:Khi ứng dụng của bạn được cài đặt trên thiết bị người dùng và tích hợp FCM SDK, SDK sẽ tạo ra một **registration token** duy nhất cho thiết bị hoặc ứng dụng cụ thể.
- Token này thường được tạo ra khi ứng dụng khởi chạy lần đầu tiên hoặc khi token cũ bị hết hạn hoặc bị thu hồi.
- **Quản lý token**:**Lưu trữ token**: Token cần được lưu trữ an toàn trên máy chủ của bạn hoặc trong cơ sở dữ liệu để bạn có thể sử dụng nó để gửi thông báo sau này.
- **Xử lý token hết hạn**: Token có thể hết hạn hoặc bị thu hồi theo thời gian. Khi điều này xảy ra, ứng dụng cần xử lý và lấy token mới.
- **Cập nhật token**: Khi token mới được sinh ra (do hết hạn hoặc do thay đổi trong ứng dụng), bạn cần cập nhật token mới trong cơ sở dữ liệu của bạn và thay thế token cũ.
- **Bảo mật**: Token là một mã định danh nhạy cảm, do đó bạn cần đảm bảo bảo mật nó để tránh rò rỉ và chỉ sử dụng nó để gửi thông báo đến thiết bị hoặc ứng dụng cụ thể mà nó đại diện.
- **Sử dụng token**:Token được sử dụng để gửi thông báo đến thiết bị hoặc ứng dụng cụ thể.
- Khi bạn muốn gửi thông báo, bạn cung cấp token cho FCM Backend cùng với nội dung thông báo.
Token đóng vai trò quan trọng trong hệ thống FCM vì nó là cách để định danh các thiết bị hoặc ứng dụng cụ thể và gửi thông báo đến chúng. Do đó, việc quản lý token một cách an toàn và hiệu quả là rất quan trọng để đảm bảo thông báo được gửi đến đúng đối tượng và giữ cho hệ thống hoạt động ổn định.

Qua 2 phần trên các bạn có thể hình dung được luồng như ảnh dưới đây
 
## **4.FCM Message (nội dung data trong message)**

Firebase Cloud Messaging (FCM) cho phép bạn gửi hai loại thông điệp khác nhau đến các ứng dụng của người dùng 

- **Thông điệp thông báo (Notification messages)**:Đôi khi được gọi là "display messages" (thông điệp hiển thị).
- Chứa một tập hợp các khóa có thể nhìn thấy bởi người dùng (user-visible keys) được định trước, như tiêu đề (title), nội dung (body), hình ảnh (image), và các yếu tố khác để hiển thị thông báo cho người dùng.
- Thông điệp thông báo có thể chứa một **data payload** (gói dữ liệu) tùy chọn.
Ví dụ

{

  "token": "bk3RNwTe3H0:CI2k_HHwgIpoDKCIZvvDMExUdFQ3P1...",

   "notification": {

     "title": "Account Balance Update",

     "body": "Your account balance has been updated by +$200.00. New balance: $1500.00",

     "sound": "default",

     "image": "https://example.com/images/balance-update.png"

  },

   "data": {

     "transaction_id": "56789",

     "amount": "+$200.00",

     "new_balance": "$1500.00",

     "timestamp": "2024-04-12T10:30:00Z",

     "description": "Salary for April",

     "transaction_type": "Credit"

  }

}
 
Hình ảnh thể hiện trên điện thoại: với 1 là title, 2 là ảnh, và 3 là body

- **Thông điệp dữ liệu (Data messages)**:Thông điệp dữ liệu được xử lý bởi ứng dụng client
- Chứa các cặp khóa-giá trị (key-value pairs) tùy chỉnh do hệ thống định nghĩa.
- Ứng dụng client sẽ nhận và xử lý thông điệp dữ liệu theo logic riêng của nó.
Ví dụ

{

     "message": {

        "token": "bk3RNwTe3H0:CI2k_HHwgIpoDKCIZvvDMExUdFQ3P1...",

         "data": {

             "promotionTitle": "Flash Sale!",

             "promotionDescription": "Get 50% off on selected items.",

             "promotionImageUrl": "https://example.com/promotion.jpg",

             "promotionEndDate": "2024-04-15T23:59:59Z"

         }

    }

}

Khi ứng dụng nhận được message trên thì ứng dụng có thể xử lý :

- Nếu user đang bật app:  hiển thị ngay popup thông báo về CTKM và user có thể click vào để xem (cái này thì tùy BA yêu cầu để có cách hiển thị phù hợp)
- Nếu user đang ở chế độ không bật app: Hiển thị message dạng notification hiển thị trên MH Notification center của thiết bị. User click vào notification thì mở ra chi tiết CTKM
Ngoài ra các bạn lưu ý: Kích thước tối đa cho cả hai loại thông điệp là **4000 bytes**, ngoại trừ khi gửi thông điệp từ Firebase console, giới hạn ở **1000 ký tự**.

Do đó, khi BA yêu cầu thì cần lưu ý, là data trong message có giới hạn nên khi trao đổi với dev, nếu có 1 yêu cầu nào đó mà BA đưa ra, message trong đó sẽ vượt 1000 ký tự thì khi đó dev sẽ cần bạn xem xét lại, để làm sao rút ngắn được data trao đổi này

## 5.BA cần lưu ý gì khi làm nghiệp vụ phần notification

Qua việc tìm hiểu firebase ở trên thì sẽ giúp bạn BA lưu ý được điều gì

- Luồng giao tiếp giữa các bên: Các bạn chỉ cần nắm luồng giao tiếp, ko cần nắm làm sao tạo ra được luồng giao tiếp như thế
- Data trao đổi giữa các thành phần trong luồng  (token, loại thiết bị, nội dung của từng loại message ở trên)
- Kích thước message để biết không phải thích gửi gì cũng được
- Trạng thái background và trạng thái foreground (Thực ra cái này cũng ko hẳn đến mức đọc bài này mới biết, nhưng đúng là ai ít để ý – như mình, thì sau khi đọc bài này mới lưu ý về cách xử lý ứng với 2 loại trạng thái này sẽ khác nhau
- Token sẽ có thời gian hiệu lực và khi nó bị hết hạn thì sao: cái này thì mình chưa nói rõ trong bài, nhưng tìm hiểu thì nếu token không hoạt động gì trong vòng 270 ngày thì nó sẽ bị expire(tức ko có tín hiệu gửi nhận gì từ tokent đó), BA cũng cần nắm để xem xử lý TH này như thế nào – Dev có thể họ đọc tài liệu và quay sang hỏi BA trong tình huống này
Hy vọng bài viết này giúp các bạn hiểu được luồng notifcation nhé, hoặc luồng update chủ động từ BE nhé

chi tiết các bạn có thể tìm hiểu tại link [https://firebase.google.com/docs/cloud-messaging](https://firebase.google.com/docs/cloud-messaging)