---
id: 62
title: "Thảo luận về luồng thanh toán QR"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T03:10:04.000Z"
source_url: "https://m2mba.com/blog/articles/giai-phap-thanh-toan-qr-da-nen-tang"
---

# Thảo luận về luồng thanh toán QR

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T03:10:04.000Z*

**Vấn đề thảo luận**: Làm sao 1 cửa hàng chỉ cần sử dụng 1 QR cho tất cả các ví/mobile banking

Tại sao mình lại nêu vấn đề này ra. Các bạn có thể thấy trong mấy năm gần đây, số lượng ví điện thử/Mobile banking app ra đời rất nhiều, và còn sẽ nhiều nữa trong thời gian tới . Và với xu thế đó thì phương thức thanh toán QR cũng được đẩy mạnh từ năm 2017 trở lại đây vì nó là phương thức phù hợp với mobile app. Hơn nữa, Số lượng người dùng ở VN sử dụng smartphone rất lớn nên VN sẽ là thị trường hấp dẫn cho hình thức thanh toán này

Tuy nhiên, các đơn vị phát triển đang mạnh ai nấy chạy, cụ thể bạn vào 1 cửa hàng sẽ có thể thấy dán 2,3 ảnh QR hoặc nhiều hơn nữa. Với việc 1 cửa hàng có nhiều QR sẽ bất cập như thế nào cho người dùng và merchant

- **Người dùng:** Phải chọn đúng mobile app phù hợp với các QR đang có ở merchant. Và cũng có thể cửa hàng đó còn chưa hỗ trợ các mobile app của KH đang sử dụng 
- **Merchant: **Phải vào đúng trang merchant view do Acquirer cung cấp=>merchant phải nhớ quá nhiều trang của các Acquirer để vào check kết quả giao dịch
Do đó mình nghĩ đây là 1 vấn đề hot trong tương lai gần cho các ví và các đơn vị phát triển merchant (như VNpay, Vimo, Momo, Viettelpay…). Vậy chúng ta thử đưa ra 1 số hướng xử lý xem như thế nào nhé (từ kém tối ưu cho đến tối ưu nhất)

Để đưa ra giải pháp, trước hết chúng ta cần phải trả lời được các câu hỏi sau

**Câu hỏi 1**: QR dùng trong thanh toán chứa những thông tin gì

QR chỉ là 1 hình ảnh được chuyển từ 1 đoạn text (các bạn có thể search tool QR generator và sau đó dùng 1 app QR reader để đọc lại QR vừa sinh nhé ). QR dùng trong thanh toán luôn phải có thông tin merchant , thường là merchant code, để biết GD thanh toán cho merchant nào. 

**Câu hỏi 2**: Luồng thanh toán QR như thế nào

Các bạn cần xem lại bài [tại đây](https://m2mba.com/posts/30)

**Câu hỏi 3**: Làm thế nào để các ví có thể hiểu được các QR do các đối tác/ví khác khác sinh ra. 

Mình đưa ra 1 số cách như sau

-  **Cách 1: **Các bên công khai rule sinh QR của nhau (và các bên kết nối sẽ sử dụng regular expression để có thể nhận diện ra rule của đối tác nào). Tất nhiên 2 đối tác không được cùng 1 rule. Ví dụ trên QR chỉ in mỗi mã merchant thì chắc chắn không ai xác định được mã QR đó của đơn vị nào sinh ra, nhưng ví dụ như mã của ViettelPay / Wechat/ Vnpay Momo hiện tại thì có thể sử dụng bộ regular expression sau để xác định được (cái này chắc chỉ các anh em dev hiểu, các bạn có thể vào trang [https://regex101.com/r/3dNzjU/99](https://l.facebook.com/l.php?u=https%3A%2F%2Fregex101.com%2Fr%2F3dNzjU%2F99%3Ffbclid%3DIwAR0wR1xdESPpePrF55Wq7uK28cF6berIWekVSWOM10uHldX8AozPD9DJtOE&h=AT028VsD-pzs_XnGjLElPljicAMQbwM-8-9t_Uao4tsWoA0-t6gMJDVn7O9YZtaLIVto_DT0xtWdNzUcjv61o-gH_Gi5Ppvqom4kpumXfUCRSo0Y_y4_k3EaznXpfY_GtZSi&__tn__=-UK-R&c%5b0%5d=AT1sLaxniKfVMpcBv3_3BzxBi7KzbtU0MLu02rI2srSL232JvisM7gMw8W9pBQG4Dx7o1lZhEfVXmVUo72rdLNONtzXltBUhZWOgBYBwRfOVaMjcmtvf3x7CAU7U0nw69BBUhdgK9Q7WGtngmd3LCB3tcGXdHUwyGsZMxTSnqVTC8H7yyxo) để test nhé, minh tạo sẵn các chuỗi text QR của các đối tác bên dưới rồi )ViettelPay: /VERSION.*PRIORITY.*BankPlus.*TYPE.*MERCHANT_CODE/
- Wechat: / weixin:\/\/wxpay\/bizpayurl\?/
- Vnpay: /00+.*(26)+.*(52)+.*53+.*63+.*/
- Momo: /(https:\/\/payment.momo.vn\/gw_payment).+/
- **Cách 2**: KH chủ động chọn quét QR của đối tác nào (Vnpay, ViettelPay, MoMo hay …). Cách này lúc đầu mình nghĩ chắc sẽ bị phản đối J, ai ngờ đâu dò vào Mpos.vn thì họ cũng đang làm theo cách này, nhưng họ làm theo hướng: NV bán hàng hỏi KH muốn thanh toán QR của đơn vị nào. Sau khi KH trả lời thì họ sẽ thực hiện sinh QR theo đơn vị đó. Khi đó KH mở ví tương ứng ra để quét QR và thanh toán 
- **Cách 3**: Các bên cùng sinh 1 chuẩn chung QR, hiện tại trên thế giới có chuẩn QR EMV (nếu có dịp mình sẽ có bài về chuẩn này). Khi các bên cùng sử dụng 1 chuẩn chung thì sẽ hiểu được các thông tin trong QR đó. Cách này là cách tối ưu nhất trong 3 cách, và hiện tại các bên đang phát triển theo hướng này, NHNN đã đưa ra quy định chuẩn chung của QR, các bên sẽ tuân thủ theo, chi tiết đặc tả các bạn có thể tham khảo [tại đây](https://vietqr.net/portal-service/download/documents/QR_Format_T&C_v1.0_VN_092021.pdf)
- **Câu hỏi 4: **Với cách thứ 3, làm thế nào để biết được merchant này do Acquirer nào phát triển (QR đặt tại Merchant do đơn vị nào phát hành )
Bạn nhớ lại quy trình thanh toán POS mình viết ở bài trước, Napas sử dụng đầu BIN trên thẻ của KH để biết đơn vị nào issue ra thẻ đó. Vận dụng cách đó, chúng ta sẽ có ý tưởng là mã merchant code cũng sẽ sinh theo 1 rule tương ứng, ví dụ: [xxxxxx][yyyyyy] trong đó 

- xxxxxx là mã số nhận diện acquirer (Aquierer Indentification Number: AIN) ví dụ như :
- 123456: Ví A
- 123457: Ví B
- 123458: Ví C
- yyyyyy là chuỗi tự sinh và duy nhất của Acquirer để phân biệt merchant
**Câu hỏi 5**: Làm thế nào để issuer có thể notify cho Acquirer biết thông tin thanh toán để Acquirer thông báo cho merchant

Có 3 giải pháp như trong ảnh mình nêu

- **Giải pháp 1:** Các ví kết nối chéo nhau, Ví A đọc đc QR của Ví B thì gửi thông tin sang ví B để ví B notify cho Merchant
Là giải pháp kém tối ưu nhất và mất thời gian triển khai khi các bên kết nối chéo nhau và không tận dụng được sự kết nối có sẵn nào

- **Giải pháp 2:** Kết nối tới ví mà ví đó đã kết nối tới nhiều acquirer khác
Tận dụng kết nối có sẵn của 1 đơn vị, ở đây là ví A, ví A đã kết nối được với 3 đối tác khác là Ví B, C, D. Khi đó ví E chỉ cần kết nối với ví A thì có thể kết nối được với ví B, C, D

- **Giải pháp 3**: Thay vì kết nối chồng chéo, có 1 đơn vị trung gian đứng giữa 
Là giải pháp tối ưu nhất, có đơn vị trung gian đứng giữa để điều hướng giao dịch về đúng acquirer (tương tự như Napas với giao dịch qua máy POS hay rút tiền ATM)

Kết hợp các câu trả lời trên, chúng ta có thể đưa ra quy trình xử lý giao dịch cho giải pháp lý tưởng nhất (Giải pháp 3) như sau

- Bước 1: Acquirer phát triển merchant và in QRcode theo chuẩn thống nhất
- Bước 2: Issuer đọc QR, thực hiện trừ tiền thành công
- Bước 3: Issuer check xem QR do acquierer nào phát triển:Nếu QR do chính issuer phát triển thì thực hiện hạch toán nội bộ và notify cho merchant 
- Nếu QR do đơn vị khác phát triển thì chuyển cho đơn vị trung gian (Giả sử là VNPAY, tựa như Napas của thẻ nội địa)
- Bước 4: VNPAY thực hiện đọc mã merchant và xác định Acquierer dựa vào AIN (6 kí tự đầu trong chuỗi merchant code)
- Bước 5: Vnpay FW thông tin sang Acquirer
- Bước 6: Acquirer notify thông tin cho merchant trên app và gửi thông tin sang merchant để thông báo kết quả giao dịch (nếu merchant kết nối hệ thống)
Các bạn có thấy rõ ràng là chúng ta có thể đưa ra giải pháp thực hiện dựa vào những gì chúng ta đã xử lý trước đó không. Phương pháp này cũng rất hữu ích trong nhiều nghề, không chỉ nghề BA=>Chúng ta cần phải tích lũy kinh nghiệm, làm nhiều mảng dự án khác nhau để có thể đưa ra giải pháp nhanh trong nhiều tình huống khác nhau