---
id: 130
title: "Tìm hiểu về hệ thống GPS, trạng thái giao thông google map"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-04-09T07:56:23.000Z"
source_url: "https://m2mba.com/blog/articles/tim-hieu-ve-he-thong-gps-va-giao-thong-google-map"
---

# Tìm hiểu về hệ thống GPS, trạng thái giao thông google map

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-04-09T07:56:23.000Z*

## **1.GPS là gì? **

GPS là hệ thống định vị toàn cầu do Mỹ phát triển và vận hành. GPS là tên viết tắt của cụm từ “Global Positioning System”. Nó là một hệ thống bao gồm hơn 30 vệ tinh bay trên quỹ đạo phía trên trái đất ở độ cao 20.200 km.

GPS hoạt động trong mọi điều kiện thời tiết, mọi nơi trên Trái Đất, liên tục suốt 24 giờ và **hoàn toàn miễn phí **đối** **với một số dịch vụ.

## 2.Thành phần

Hệ thống Định vị Toàn cầu (GPS) bao gồm các thành phần chính sau:

- **Vệ tinh GPS (Space component)**: Đây là các vệ tinh hoạt động trên quỹ đạo quanh Trái Đất và phát sóng tín hiệu radio chứa thông tin về vị trí và thời gian. Hiện nay, có hơn 30 vệ tinh GPS được triển khai trên quỹ đạo. Mỗi vệ tinh GPS được trang bị đồng hồ nguyên tử, đảm bảo rằng dữ liệu thời gian được truyền bởi các vệ tinh là chính xác đến độ nanogiây. Mức độ chính xác này rất quan trọng cho việc xác định vị trí và điều hướng chính xác, vì ngay cả sự không đồng bộ nhỏ nhất trong thời gian cũng có thể dẫn đến sai lệch đáng kể trong việc xác định vị trí của một người.
- **Điểm kiểm soát đất liền (Ground Control Stations – Control component)**: Các điểm kiểm soát đất liền được sử dụng để quản lý hệ thống GPS và giám sát vệ tinh. Chúng theo dõi quỹ đạo, tốc độ, và trạng thái của từng vệ tinh để đảm bảo rằng chúng đang hoạt động như dự kiến và đáp ứng các tiêu chuẩn hiệu suất. Các chuyên gia tại các trạm kiểm soát phân tích dữ liệu từ các vệ tinh GPS để phát hiện ra bất kỳ sự cố hoặc biến đổi nào của các vệ tinh. Họ kiểm tra tín hiệu, thời gian, và các thông số khác để đảm bảo rằng hệ thống hoạt động một cách chính xác và ổn định. Trong trường hợp xảy ra sự cố ví dụ như vệ tinh GPS có vấn đề, các trạm kiểm soát có nhiệm vụ nhanh chóng đưa ra phản ứng và giải quyết vấn đề. Họ cũng sẵn sàng chuyển đổi sang các hệ thống dự phòng để đảm bảo rằng dịch vụ GPS không bị gián đoạn.
- **Thiết bị nhận GPS (GPS Receiver – User component)**: Đây là các thiết bị điện tử được tích hợp trong các thiết bị di động như điện thoại thông minh, máy tính bảng, hoặc đồng hồ GPS, để nhận và xử lý tín hiệu từ các vệ tinh GPS. Thiết bị nhận GPS có nhiệm vụ tính toán vị trí và hiển thị thông tin vị trí cho người dùng. Trên thiết bị nhận này 
- **Tín hiệu trong GPS** : là nền móng của toàn bộ hệ thống, vì chúng mang dữ liệu truyền trong dải tần số L-band, cho phép chúng xuyên qua các vật cản như tòa nhà, mây và lá cây, giúp định vị và điều hướng chính xác. Khi nhận được tín hiệu GPS, thiết bị nhận GPS giải mã và xử lý dữ liệu được truyền, và cung cấp được thông tin vị trí của các thiết bị nhận
## 3.​Nguyên lý hoạt động

.

 

**Bước 1:** Các vệ tinh GPS bay **vòng quanh Trái Đất hai lần trong một ngày** theo một quỹ đạo rất chính xác và **phát tín hiệu có thông tin** xuống Trái Đất. Vận tốc tín hiệu được tính theo vận tốc ánh sáng gần 300.000km/h. Thông tin trong tín hiệu phát ra từ vệ tinh GPS gồm:

- Mã định danh vệ tinh: mã định danh duy nhất được gắn với mỗi vệ tinh GPS để xác định vệ tinh nào đang phát tín hiệu
- Dữ liệu về vị trí của vệ tinh
- Dữ liệu về thời gian phát tín hiệu từ vệ tinh
- …
**Bước 2:** Các máy thu GPS nhận thông tin này và thực hiện giải mã thông tin từ tín hiệu vệ tinh 

**Bước 3**: Máy thu GPS tính toán khoảng cách từ máy thu tới vệ tinh. Việc tính toán có thể phức tạp, nhưng các bạn có thể hiểu đơn giản như sau

- Khoảng cách từ máy thu tới vệ tinh = Thời gian di chuyển * vận tốc ánh sáng
Thời gian di chuyển=Thời gian lúc máy thu nhận tín hiệu – Thời gian mà vệ tinh phát tín hiệu (được gửi trong thông tin tín hiệu do vệ tinh phát ra)

**Bước 4**: Máy thu cần nhận thông tin từ **ít nhất 4 vệ tinh,** để biết khoảng cách từ máy thu tới các vệ tinh, và từ đó bằng phép tính lượng giác ( [**trilateration**](https://en.wikipedia.org/wiki/Trilateration)) , máy thu sẽ tính ra được tọa độ của thiết bị

Nếu máy thu chỉ nhận được tín hiệu từ 1 vệ tinh thì khi đó thực tế vị trí của Máy thu sẽ nằm 1 điểm bất kỳ trên 1 hình cầu với tâm là vệ tinh. Do đó, nếu xác định vị trí 2D thì chỉ cần 3 vệ tinh, nhưng chúng ta cần xác định chính xác vị trí của máy thu trong không gian 3D nên cần thêm 1 vệ tinh nữa mới đảm bảo thông tin chính xác về vị trí

 

Mình vẽ thêm 1 luồng dạng sequence để các bạn hình dung nhé

 

## 4.Các hệ thống định vị 

Hiện nay các hệ thống định vị trên thế giới gồm có :

-  GPS (Mỹ)
-  GLONASS (Nga)
- GALILEO (Châu Âu)
-  IRNSS (Ấn Độ)
- BEIDOU của (Trung Quốc)
- QZSS (Nhật Bản).
Chỉ có duy nhất GPS là hệ thống định vị có các vệ tinh định vị toàn cầu được, còn các hệ thống còn lại chỉ định vị trong khu vực của quốc gia hoặc Châu Âu nên sẽ không sử dụng được cho toàn bộ các thiết bị trên toàn cầu

## 5.Trạng thái giao thông trên bản đồ

Sau khi hiểu về cơ chế tìm ra tọa độ của 1 máy thu (như điện thoại di động) thì chúng ta có thể hiểu được làm sao để xác định được trạng thái giao thông

Đó chính là dựa vào vận tốc di chuyển của các máy thu trên cung đường đó, nếu di chuyển với vận tốc rất rất rất chậm thì có nghĩa là màu đỏ, còn vẫn di chuyển được nhưng tốc độ chậm thì màu vàng, còn di chuyển bình thường thì màu xanh

Server của google map sẽ thu thập dữ liệu vị trí từ nhiều thiết bị khác nhau, tính vận tốc của từng thiết bị đó để tìm ra vận tốc trung bình trên cung đường đó và từ đó có thể update được trạng thái giao thông của các cung đường trên server

Việc làm sao để ứng dụng google map trên các thiết bị update được trạng thái giao thông thì có thể thực hiện 2 cách

- **Cách 1**: Ứng dụng gọi API của BE google map để lấy thông tin trạng thái giao thông trên cung đường mà thiết bị di chuyển
- **Cách 2**: BE chủ động update lại trạng thái giao thông cho Ứng dụng google map thông tin các công nghệ xử lý như firebase, hay socket. Hôm sau mình sẽ có bài nói về 2 loại này, về firebase trước mình có nói về luồng notify trên các ứng dụng di động (cũng là BE bắn message xuống cho app) Hôm nay mình không đủ time nữa nên mình xin phép chỉ dừng tại đây nhé
Dưới dây là luồng update trạng thái giao thông (Giả định qua API nhé)