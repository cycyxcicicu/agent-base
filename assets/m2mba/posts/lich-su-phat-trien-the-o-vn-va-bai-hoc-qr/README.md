---
id: 61
title: "Lịch sử phát triển thẻ ở VN"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T03:01:39.000Z"
source_url: "https://m2mba.com/blog/articles/lich-su-phat-trien-the-o-vn-va-bai-hoc-qr"
---

# Lịch sử phát triển thẻ ở VN

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T03:01:39.000Z*

Nhớ lại cách đây 2 năm khi Viettel làm với với 2 đối tác Mastercard và Visa để hợp tác thanh toán QRCode cho KH ViettelPay trên toàn cầu và KH nước ngoài vào VN thanh toán tại các Merchant của ViettelPay (Sau này sẽ có bài nói về vấn đề này nhé ). Lúc đó mình mới bắt đầu join vào dự án tý xíu, tham gia vào cuộc họp và nghe 1 câu: Nếu chúng ta không sớm chuẩn hóa thì sẽ gặp lại vấn đề với POS cách đây 10 năm

Tại thời điểm đó, mình chưa khi nào làm với hệ thống POS nhưng đoán hiểu rằng: Hồi xưa máy POS do ngân hàng nào phát hành thì chỉ chấp nhận thẻ của ngân hàng đó.

Điều này tương tự như vấn đề về QR hiện tại: Các Ví điện tử (VĐT)/Mobile banking chỉ quét được QR do các VĐT/Mobile banking sinh ra

Vậy trước khi đưa ra giải pháp giải quyết bài toán mình nêu ra hôm trước, chúng ta hay thử tìm hiểu lại lịch sử phát triển hệ thống chuyển mạch thẻ nội địa/POS (Thực tế cái này mình không làm, mình chỉ google lại và hiểu theo ý của mình, nếu ai thấy không hợp lý chỗ nào thì comment giúp mình để sửa lại nhé)

Lịch sử phát triển được chia làm các giai đoạn

- Phase 1: Các ngân hàng đứng độc lập nhau, chủ động phát triển hệ thống thanh toán thẻ : Thẻ ngân hàng nào rút tiền ở ngân hàng đó, Máy POS của ngân hàng nào phát hành chỉ sử dụng được cho thẻ của ngân hàng đó=>Tương tự với hiện trạng thanh toán QR bây giờ
- Phase 2: Hình thành các tổ chức chuyển mạch như banketvn, smartlink, vnbc (các bạn google để ra thông tin các ngân hàng thuộc các tổ chức trên nhé.). Trong giai đoạn này, các ngân hàng thuộc cùng 1 tổ chức sẽ rút tiền/Thanh toán qua máy POS tại các máy ATM/POS của các ngân hàng phát hành cùng tổ chức đó.
- Phase 3 : Để thuận tiện cho người tiêu dung, 3 tổ chức đã kết nối liên thông với nhau để có thể hỗ trợ KH sử dụng thẻ thuộc 3 tổ chức đều có thể rút tiền hoặc quẹt thẻ POS do ngân hàng thuộc 1 trong 3 tổ chức phát hành
- Phase 4: 3 tổ chức hợp lại thành tổ chức Banknetvn , sau này đổi tên thành Napas. Hiện tại Napas đã kết nối được hệ thống thẻ của 43 ngân hàng. Do đó KH sử dụng thẻ ATM thuộc 1 trong 43 ngân hàng này sẽ thực hiện rút tiền/thanh toán qua máy POS do các ngân hàng cùng thuộc tổ chức Napas kết nối
Mình đang nghĩ, bài toán QR tại VN cũng sẽ trải quá các phase rồi mới tới được phase cuối cùng (là giải pháp tối ưu nhất) như bài hôm trước mình vẽ (mà đang đặt dấu ? đơn vị nào sẽ thực hiện chuyển mạch QR).

Mình có đọc 1 bài báo nói rằng 

Nhiều nước trên thế giới, từng đi trước trong lĩnh vực ATM, trải qua 3 giai đoạn phát triển: đầu tiên là mỗi ngân hàng tự xây dựng hệ thống thanh toán thẻ riêng. Sau đó hình thành các nhóm ngân hàng thỏa thuận dùng chung hệ thống. Cuối cùng, tất cả cùng hợp tác xây dựng một hệ thống duy nhất. “VN là nước đi sau, đáng ra chúng ta có thể học tập để bỏ qua giai đoạn hai, nhưng thực tế thì chúng ta lại bị xoáy vào lối mòn của các nước đi trước”, Cục trưởng Tạ Quang Tiến phân tích. “Nguyên nhân chủ yếu là vì VN thiếu một cơ chế chỉ đạo, điều hành, không có một tổ chức đầu mối, vận động và tập hợp trong khi các ngân hàng thì không đồng thuận, mạnh ai nấy lo. Thậm chí, họ coi phát triển ATM là vũ khí cạnh tranh”

Và các bạn cũng có thể thấy, vấn đề lại lặp lại với QR. Bài sau sẽ phân tích các giải pháp theo từng thời kỳ như trên nhé 

Tại sao mình lại nêu vấn đề POS ở đây, thực ra mình cùng muốn nói với các bạn 1 technique nữa mà BA thường áp dụng đó là Lesson Learned

Nghe cái tên các bạn cũng có thể đoán ra được ý nghĩa, nó là dạng rút ra bài học kinh nghiệm cho các vấn đề đã trải qua. Tất nhiên với bài toán POS và QR thì thuộc tầm khác xử lý, không phải là tầm BA của chúng ta. Tuy nhiên, trong công việc BA của các bạn, việc xử lý tình huống dựa theo các bài học kinh nghiệm thường được sử dụng rất nhiều, Kể cả giải pháp sắp tới mình đưa ra, sau này các bạn cũng có thể áp dụng rất nhiều vào các dự án các bạn tham gia (Lý thuyết BABOK về lesson Learned, tối mình sẽ post nhé, nó cũng dễ hiểu, mình cũng ko muốn post vào bài này, vì sợ dài quá)

Để việc đưa giải pháp cho bài sau được dễ hiểu, mình xin nêu thêm 1 số thông tin mà bên POS đang thực hiện

Quy trình thanh toán qua máy POS

- Bước 1: KH quẹt thẻ, NV bán hàng nhập số hóa đơn, số tiền, KH nhập PIN
- Bước 2: Máy POS gửi yêu cầu xác thực lên ngân hàng phát hành POS (Acquirer)
- Bước 3: Acquirer kiểm tra xem thẻ của KH có phải là thẻ của đơn vị mình phát hành koNếu thẻ của chính mình, thực hiện hạch toán nội bộ
- Nếu thẻ của đơn vị khác, chuyển yêu cầu sang Napas
- Bước 4: Napas dựa vào BIN của thẻ issuer để định tuyến chuyển sang ngân hàng issuer tương ứng
- Bước 5: Issuer verify thẻ và thực hiện hạch toán, trả kết quả về cho Napas, Napas trả kết quả về cho acquirer
Mọi người sẽ thắc mắc BIN là gì, BIN là viết tắt của Bank Identification Number, là mã định dạng ngân hàng in trên mặt trước thẻ, là một dãy số có 6 chữ số theo chuẩn ISO/IEC 7812-1:2006(E) của Tổ chức Tiêu chuẩn Quốc tế và Tổ chức Kỹ thuật điện Quốc tế ban hành năm 2006, có định dạng 9704xx, trong đó:

- 04 chữ số đầu tiên của mã BIN phản ánh mã quốc gia của tổ chức phát hành thẻ thực hiện nghiệp vụ phát hành thẻ tại Việt Nam.
- 02 chữ số cuối cùng bắt đầu từ số 00 cho đến số 99 do Ngân hàng Nhà nước Việt Nam quy định cho từng tổ chức phát hành thẻ.
Căn cứ vào 38/2007/QĐ-NHNN 30 tháng 10 năm 2007, Các ngân hàng mới bắt đầu quy chuẩn lại BIN để việc kết nối qua đơn vị trung gian được dễ dàng trong việc định tuyển ngân hàng. Trước đây, các ngân hàng chủ động đưa ra mã BIN và có trường hợp 2 ngân hàng cùng 1 mã BIN

 

Dưới đây là ảnh minh họa các giai đoạn

- **Phase 1:** Các ngân hàng xây dựng hệ thống thanh toán thẻ riêng. KH của các ngân hàng không sử dụng chéo trên hệ thống ATM/POS của các ngân hàng khác
- Phase 2: Hình thành 3 tổ chức chuyển mạch như banketvn, smartlink, vnbc. Trong giai đoạn này, các ngân hàng thuộc cùng 1 tổ chức sẽ rút tiền/Thanh toán qua máy POS tại các máy ATM/POS của các ngân hàng cùng tổ chức đó.
 

- Phase 3: 3 tổ chức đã kết nối liên thông với nhau để có thể hỗ trợ KH sử dụng thẻ thuộc 3 tổ chức đều có thể rút tiền hoặc quẹt thẻ POS do ngân hàng thuộc 1 trong 3 tổ chức phát hành
Các bank ngoài 3 tổ chức trên có thể kết nối liên thông vào 1 trong 3 tổ chức để có thể kết nối liên thông 3 tổ chức
 

- Phase 4: 3 tổ chức hợp lại thành tổ chức Banknetvn , sau này đổi tên thành Napas. Napas đã kết nối được hệ thống thẻ của 43 ngân hàng. KH sử dụng thẻ ATM thuộc 1 trong 43 ngân hàng này sẽ thực hiện rút tiền/thanh toán qua máy POS do các ngân hàng cùng thuộc tổ chức Napas kết nối