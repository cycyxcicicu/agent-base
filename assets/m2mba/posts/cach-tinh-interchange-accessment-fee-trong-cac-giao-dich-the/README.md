---
id: 63
title: "Luồng xử lý thanh toán qua thẻ tín dụng"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T03:13:11.000Z"
source_url: "https://m2mba.com/blog/articles/cach-tinh-interchange-accessment-fee-trong-cac-giao-dich-the"
---

# Luồng xử lý thanh toán qua thẻ tín dụng

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T03:13:11.000Z*

Bạn đã cầm thẻ tín dụng đi thanh toán tại các siêu thị, cửa hàng khá nhiều rồi. Vậy bạn có muốn thử tìm hiểu xem luồng xử lý với các thẻ đó như thế nào không? Hãy cũng admin thử tham khảo luồng xử lý của nó nhé

Trong này có 1 số thuật ngữ các bạn lưu ý

- Merchant: Là đơn vị cung cấp hình thức thanh toán POS (máy quẹt thẻ mà các bạn vẫn quẹt)
- Accquirer Bank hay còn gọi Merchant Bank: Là đơn vị phát triển Merchant và xây dựng ứng dụng thanh toán qua POS
- Issuer Bank: Là ngân hàng phát hành của chủ thẻ
- Payment Network Processor: Là hệ thống xử lý thanh toán thẻ của các tổ chức thẻ, Ví dụ thẻ nội địa VN là Napas, Thẻ mastercard là Banknet, thẻ visa là visanet
- Interchange fee: Là  Lệ phí trao đổi ngân hàng hay còn được gọi là interchange rate/fee, là một khoản phí được tính cho các giao dịch thanh toán điện tử giữa các ngân hàng khác nhau. Khi một khách hàng sử dụng thẻ thanh toán của ngân hàng A để mua hàng hoặc thực hiện giao dịch tại một điểm chấp nhận thẻ thuộc ngân hàng B, ngân hàng A sẽ nhận được một khoản tiền từ ngân hàng B như một lệ phí trao đổi ngân hàng, phí này được tổ chức thẻ quy định, không đàm phán được
- Assessment fee: Là phí mà Accquirer bank phải trả cho Payment network processor để xử lý thanh toán
- Merchant discount fee: Là phí mà Accquirer Bank sẽ thu của Merchant
 

**Bước 1**: **Authorization-  Xác thực dữ liệu thanh toán - **. Đây là bước đâu tiên trong quá trình xử lý giao dịch thanh toán qua thẻ tín dụng. Merchant sẽ gửi thông tin thanh toán (bao gồm thông tin thẻ, và số tiền thanh toán…) sang cho bên accquirer, acquirer sẽ dựa vào thông tin số thẻ để đẩy sang hệ thống tổ chức thẻ phù hợp, hệ thống tổ chức thẻ sẽ đẩy tiếp GD sang bên Issuer. Issuer có trách nhiệm validate thông tin thẻ như trạng thái thẻ hợp lệ hay không, thẻ có đủ hạn mức thực hiện GD hay ko, thẻ có nằm trong blacklist hay không. Nếu okie thì ghi log lại GD và giảm hạn mức của thẻ, GD lúc này vẫn chưa lên sao kê của tài khoản, trong thời gian này, GD thẻ có thể hủy 1 cách dễ dàng. Còn sau thời gian này thì phải tiến hành tra soát giao dịch/Yêu cầu refund theo quy định

**Bước 2**: **Clearing - Thanh toán bù trừ  **- Đây mới là bước thực sự để ghi nợ vào thẻ tín dụng của KH, thông tin GD sẽ được đẩy từ Merchant sang accquirer=>Tổ chức thẻ=>Issuer, thông tin gửi sang sẽ theo dạng batchfile (Tức gửi toàn bộ GD thực hiện theo chu kỳ định trước, ví dụ GD trong ngày) . Bên Issuer lúc này mới thực sự hạch toán GD, lên GD trên sao kê của KH

**Bước 3: Settlement - Tổng kết thanh toán: **Đây là bước để hoàn thành quá trình thanh toán, tiền sẽ được chuyển từ tổ chức phát hành thẻ và ngân hàng thanh toán cho tất cả các giao dịch đã thực hiện ở bước clearing. Tổ chức thẻ sẽ có trách nhiệm tính toán tổng tiền net của từng các NH (vì 1 bank, với GD này là issuer nhưng với GD khác lại là accquirer, và tổ chức thẻ sẽ tính bù trừ các GD đó, để xem mỗi NH sẽ có dư nợ bao nhiêu để thực hiện quá trình bù trừ thanh toán) 

 Chủ thẻ có trách nhiệm hoàn trả cho ngân hàng phát hành của mình các khoản mua hàng đã được ghi trên bảng sao kê và mọi khoản lãi/phí liên quan tích lũy.

 

Sau đây chúng ta sẽ đi vào chi tiết vào 3 bước trên

 

## Authorization - Xác thực giao dịch

 

 

**Bước 1**: KH sẽ thực hiện quẹt thẻ tại máy POS ở các cửa hàng - NV merchant trước đó đã nhập thông tin GD thanh toán như số tiền cần thanh toán - Thường menu trên máy POS sẽ có tên là Sale, ảnh dưới là HDSD thực hiện GD thanh toán qua trên trên may POS

**Bước 2: **GD được gửi từ máy POS lên hệ thống xử lý thanh toán thẻ của NH phát hành máy POS (gọi là accquier Bank). 

**Bước 3**: Tại đây, Accquirer Bank sẽ dựa vào đầu thẻ để biết được đây là loại thẻ gì. 
**Đầu thẻ****Loại thẻ****Hệ thống tiếp nhận**9704Thẻ ATM nội địa của Việt NamHệ thống Napas4xxx…Thẻ visaHệ thống của tổ chức thẻ visa (visaNet5xxxx..Thẻ MastercardHệ thống của tổ chức thẻ Master Card (Banknet for Mastercard)
**Bước 4 (4.1,4.2): **Gửi thông tin GD đến hệ thống tương ứng

**Bước 5 (5.1,5.2): **Xác định ngân hàng issuer - Tại hệ thống xử lý của mình, tổ chức thẻ sẽ căn cứ vào 6 số đầu của thẻ - thường được gọi là BIN (Bank Identification Number – Mỗi NH khi ký kết với tổ chức thẻ để phát hành thẻ, thì họ sẽ làm việc với tổ chức thẻ tương ứng và bên tổ chức thẻ sẽ cấp đầu BIN cho NH đó – sau đó khi NH phát hành thẻ cho KH thì bắt buộc phải sử dụng đúng đầu BIN đã chốt với tổ chức thẻ). Dựa vào 6 số này, hệ thống sẽ biết được cần đẩy thông tin GD sang ngân hàng issuer nào 

**Bước 6 (6.1,6.2)**: Hệ thống xử lý thanh toán của tổ chức thẻ đẩy thông tin GD sang hệ thống của issuer Bank

**Bước 7:** NH Issuer tiếp nhận yêu cầu, sẽ thực hiện validate các thông tin đảm bảo cho phép thực hiện giao dịch, bao gồm:

- Card tồn tại và đang ở trạng thái hoạt động trên hệ thống
- Hạn mức thẻ >=số tiền cần thanh toán
- Thẻ không nằm trong blacklist
Nếu okie thì, NH Issuer bạn sẽ lưu log lại GD và tạm trừ hạn mức tín dụng còn lại (để phục vụ cho validate các GD tiếp theo). Ở đây, giao dịch vẫn chưa thực sự hạch toán vào thẻ của KH, chỉ tạm trừ hạn mức. Nếu GD vẫn đang ở trong trạng thái như vậy thì KH hoàn toàn có thể yêu cầu merchant hủy 1 cách dễ dàng (Thao tác trên máy POS luôn)

Và sau đó là quá trình trả lại kết quả cho các bên liên quan

 

## **Clearing - Thanh toán bù trừ**

**Bước 1:** Hệ thống merchant thực hiện submit dữ liệu thanh toán theo file cho Accquirer Bank, có thể thực hiện 1 trong 2 cách

- Bên phát hành POS có thể xây dựng các tính năng như Tổng kết/kết toán giao dịch (SETTLE), trên menu sẽ là Settle hoặc capture

- Hoặc có thể thiết lập tự động chu kỳ settel ( ví dụ 12 tiếng hoặc cố định vào mấy giờ trong ngày…và thiết lập của merchant trên hệ thống quản lý POS do accquirer bank xây dựng)
**Bước 2:** Acquirer Bank thực hiện ghi nhận thông tin các GD cần thực hiện capture/settle (ở đây đơn giản bên acquirer bank sẽ thực hiện chuyển trạng thái các GD thanh toán ở phần 1 (authorization)

Sau đó acquirer sẽ tổng hợp các GD thanh toán cần clearing, phân loại theo đầu thẻ, để biết GD nào cần được đẩy sang tổ chức thẻ nào, mỗi tổ chức thẻ sẽ được xuất 1 file danh sách GD, theo đặc tả của tổ chức thẻ đó

**Bước 3: **Khi tổ chức thẻ tiếp nhận được các file clearing, tổ chức thẻ thực hiện đối soát GD, để so khơp GD đã ghi nhận ở phần authorization.  Nếu GD hợp lệ, Tổ chức thẻ  sẽ thực hiện  ghi nợ vào tài khoản của ngân hàng Issuer  và ghi có vào tài khoản của ngân hàng acquirer. Sau đó hệ thống tổ chức thẻ sẽ phân loại GD theo** **từng bank dựa vào BIN của các thẻ KH trong GD. Mỗi NH issuer sẽ được tạo 1 file riêng và gửi sang hệ thống issuer bank

**Bước 4: **NH Issuer sẽ thực hiện đối soát để so khớp GD đã ghi nhận ở phần authorization và đánh dấu các GD hợp lệ/Không hợp lệ

**Bước 5:**  Nếu GD hợp lệ thì NH Issuer sẽ thực hiện hạch toán và lên sao kê vào cuối kỳ cho KH, để KH thực hiện thanh toán khoản tiền cho đó bank

 

## **Settlement - Tổng kết thanh toán**

**Bước 1**: Tổ chức thẻ thực hiện tính toán bù trừ để ra số tiền net position của từng ngân hàng. Net postion = Tổng số tiền GD với vai trò là accquirer - Tổng số tiền của GD với vai trò là  Issuer 

Ví dụ trong GD 1 với số tiền 100.000đ, NH A là Issuer, NH B là Acquirer. GD2 với số tiền 200.000đ, NH A là Acquirer, NH là issuer thì net position của NH A là 100, còn NH B là -100 (tạm coi như các loại phí =0 hết)

**Bước 2**: Tổ chức thẻ gửi thông tin net position cho từng bank 

**Bước 3**: Có thể xảy ra 2 trường hợp

- Nếu net position >0: Tổ chức thẻ sẽ chuyển tiền cho Ngân hàng 
- Nếu net postion <0: Ngân hàng sẽ cần chuyển tiền vào tài khoản của tổ chức thẻ tại ngân hàng settlement (ở việt nam nếu mình không nhầm là ngân hàng Sacombank/VCB )
Bản chất là tiền từ issuer trả lại cho Accquirer (accquirer trả lại cho merchant), nhưng sẽ thông qua tổ chức thẻ, và tổng hợp các GD trong chu kỳ chứ ko xử lý từng GD 1

Ngoài việc chuyển số tiền GD từ issuer sang acquirer thì còn có 1 khoản tiền khác cần thanh toán cho các bên

- Interchange fee: NH accquirer sẽ cần trả cho issuer
- Accessment fee: NH accquirer sẽ trả cho tổ chức thẻ
Khi đó phần net position có thể tính bằng : Tổng số tiền GD với vai trò là accquirer - Tổng số tiền của GD với vai trò là  Issuer + interchange fee với vai trò là issuer - interchange fee với vai trò là accquirer - Accessment fee với vai trò là accquirer

 

Mình sẽ có bài viết nói về 2 loại phí này sau nhé