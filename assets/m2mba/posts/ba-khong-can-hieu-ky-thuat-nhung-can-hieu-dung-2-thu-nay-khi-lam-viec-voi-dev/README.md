---
id: 339
title: "BA không cần hiểu kỹ thuật — nhưng cần hiểu đúng 2 thứ này khi làm việc với Dev"
author: "Đậu Thị Ngọc Ánh"
created_at: "2026-08-07T04:02:55.000Z"
source_url: "https://m2mba.com/blog/articles/ba-khong-can-hieu-ky-thuat-nhung-can-hieu-dung-2-thu-nay-khi-lam-viec-voi-dev"
---

# BA không cần hiểu kỹ thuật — nhưng cần hiểu đúng 2 thứ này khi làm việc với Dev

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2026-08-07T04:02:55.000Z*

![Ảnh bìa](images/0d2a7755-7f16-42c5-994a-c061b67e8343.png)

Có một tình huống mà hầu hết BA đều đã gặp ít nhất một lần: PO đề xuất một tính năng. BA hỏi Dev để đánh giá khả thi. Dev trả lời vài câu. BA không hiểu lắm nhưng gật đầu. Rồi mang về báo PO: *“Dev bảo phức tạp lắm”* hoặc *“Dev bảo không làm được”*.

Nếu bạn đã từng ở trong tình huống đó — và cảm thấy mình không có gì thêm để nói — thì bài này dành cho bạn.

Vấn đề không nằm ở việc bạn thiếu kiến thức kỹ thuật. Vấn đề nằm ở chỗ **cuộc hội thoại đang đi sai kênh**.

## Dev nói đúng — nhưng BA chưa có gì để dùng[¶](#dev-noi-ung-nhung-ba-chua-co-gi-e-dung)

Khi được hỏi về khả thi của một chức năng, Dev thường trả lời bằng ngôn ngữ của người làm hệ thống:
“Không support.”“Phải sửa nhiều layer.”“Throughput không đủ.”“Schema chưa có.”“Làm realtime sẽ bottleneck.”
Những câu này không nhất thiết là sai. Dev đang mô tả thực trạng hệ thống theo cách họ nhìn thấy.

Nhưng với BA — và với PO — những câu đó **chưa dùng được**. Vì chúng không trả lời được câu hỏi thực sự mà BA cần biết:

- Làm được không?
- Nếu làm được thì phải làm những gì?
- Nếu không làm được thì vì lý do gì, và có phương án thay thế nào không?
Để trả lời được những câu đó, BA không cần học kỹ thuật như Dev. BA cần học cách **đổi kênh giải thích** — tức là kéo Dev từ ngôn ngữ hệ thống về ngôn ngữ nghiệp vụ mà BA có thể hiểu và đánh giá được.

Cụ thể là kéo về 2 thứ:

- **Flow xử lý** — chức năng này đi qua những bước nào, từng bước chạy ở đâu, thành phần nào tham gia
- **Data logic** — để làm được chức năng này thì cần data gì, lấy từ đâu, xử lý thế nào, data đó đã có trong hệ thống chưa, nếu chưa thì làm sao để có
Khi nắm được 2 thứ này theo từng chức năng cụ thể, BA sẽ tự thấy được độ phức tạp thật và khả thi thật — thay vì bị kẹt ở jargon kỹ thuật.

## Bảng lái nhanh: Dev nói gì → BA kéo về đâu[¶](#bang-lai-nhanh-dev-noi-gi-ba-keo-ve-au)

Trước khi đi vào từng phần, đây là bảng tham khảo nhanh để bạn biết mình cần làm gì khi nghe từng loại câu từ Dev:

## Phần 1: Lái Dev về flow xử lý[¶](#phan-1-lai-dev-ve-flow-xu-ly)

### Tại sao flow lại quan trọng?[¶](#tai-sao-flow-lai-quan-trong)

Khi Dev nói “không làm được” hoặc “phức tạp lắm”, câu đó rất chung. Nó không cho BA biết: vướng ở đâu, vướng vì lý do gì, và liệu có cách nào tháo gỡ không.

Nhưng nếu BA hỏi về flow — tức là yêu cầu Dev đi từng bước một — thì bức tranh sẽ rõ hơn rất nhiều. Vì “không làm được” ở bước hiển thị giao diện sẽ rất khác với “không làm được” ở bước đồng bộ dữ liệu với hệ thống đối tác bên ngoài. Cách giải quyết, thời gian, và rủi ro của 2 tình huống đó hoàn toàn khác nhau.

### Cách hỏi để kéo về flow[¶](#cach-hoi-e-keo-ve-flow)

Câu hỏi chuẩn để mở đầu:
“Anh/chị đi giúp em flow hiện tại của chức năng này: user làm gì → hệ thống xử lý những bước nào → kết thúc ở đâu?”
Bạn cần nghe được một chuỗi bước cụ thể. Ví dụ, với chức năng hủy đơn:
Người dùng bấm hủy đơn → màn hình hiện ô nhập lý do → gửi request lên API → API cập nhật trạng thái đơn → gửi thông báo cho khách → đồng bộ trạng thái sang hệ thống kho.

Khi đã có flow như vậy, bạn mới có thể hỏi tiếp: “Vướng ở bước nào?”

Nếu Dev trả lời “vướng ở bước gửi thông báo vì cần tích hợp thêm với hệ thống SMS bên thứ ba” — thì đó là thông tin dùng được. Nó cho BA biết rằng phần còn lại của flow không có vấn đề, chỉ một bước cụ thể đang phụ thuộc vào bên ngoài.

Nếu Dev chưa chỉ được vướng ở bước nào, thì mọi kết luận “không làm được” đều còn quá sớm để mang đi báo cáo.

**Câu lái gọn nhất:**
“Vướng ở bước nào trong flow?”
## Phần 2: Lái Dev về thành phần hệ thống tham gia[¶](#phan-2-lai-dev-ve-thanh-phan-he-thong-tham-gia)

### Tại sao cần biết thành phần?[¶](#tai-sao-can-biet-thanh-phan)

Có flow rồi, nhưng chỉ biết “bước A rồi đến bước B” vẫn chưa đủ. BA cần biết thêm: mỗi bước đó đang chạy ở đâu, thuộc phần nào của hệ thống?

Lý do là vì cùng một loại vướng mắc nhưng nằm ở thành phần khác nhau sẽ có độ phức tạp và thời gian xử lý rất khác nhau:

- Vướng ở **màn hình FE**: thường sửa được tương đối nhanh, ít rủi ro ảnh hưởng đến phần khác
- Vướng ở **rule BE / API**: cần sửa logic phía server, có thể ảnh hưởng nhiều nơi nếu API đó được nhiều màn hình gọi tới
- Vướng ở **Kafka / queue**: liên quan đến luồng xử lý bất đồng bộ, có thể ảnh hưởng đến thứ tự xử lý, độ trễ, khả năng retry
- Vướng ở **API đối tác bên ngoài**: phụ thuộc bên thứ ba — họ có hỗ trợ không, có SLA không, lead time tích hợp bao lâu?
- Vướng ở **hệ thống nội bộ khác** (kho, ERP, kế toán): cần phối hợp với team khác, có thể có quy trình phê duyệt riêng
Khi BA biết vướng ở thành phần nào, mới có cơ sở để ước lượng mức độ phức tạp và trao đổi thêm với PO về phương án.

### Cách hỏi để lấy thông tin thành phần[¶](#cach-hoi-e-lay-thong-tin-thanh-phan)

Câu hỏi gọn nhất:
“Bước này đang nằm ở FE, BE, hay phải gọi sang bên khác?”
Hoặc mở rộng hơn khi muốn hiểu toàn bộ:
“Trong flow này, những thành phần nào tham gia — FE, BE, DB, Kafka, job, FTP, đối tác bên ngoài, hay hệ thống nội bộ khác?”
### Khi nghe tên thành phần lạ — đừng đứng hình[¶](#khi-nghe-ten-thanh-phan-la-ung-ung-hinh)

Đây là điểm nhiều BA bị vướng: Dev nói đến tên công nghệ mà BA chưa nghe bao giờ — Kafka, queue, FTP, Redis, Cronjob — và BA không biết phải xử lý thế nào với thông tin đó.

Đứng hình rồi gật đầu là phản xạ tự nhiên. Nhưng gật đầu cho qua sẽ khiến BA không hiểu flow thật sự đang đi qua đâu.

Điều BA cần nhớ là: **bạn không cần hiểu cơ chế bên trong của một công nghệ. Bạn chỉ cần hiểu nó đang làm gì trong flow này.**

Câu hỏi vạn năng khi nghe tên lạ:
“Cái đó trong flow này đóng vai trò gì — nó nhận gì vào, xử lý thế nào, rồi đưa ra đâu?”
Ví dụ cụ thể:

Khi Dev trả lời được những câu đó, BA đã hiểu được vai trò nghiệp vụ của thành phần đó trong flow — dù tên công nghệ vẫn còn xa lạ.

## Phần 3: Lái Dev về data — đây mới là phần quyết định[¶](#phan-3-lai-dev-ve-data-ay-moi-la-phan-quyet-inh)

### Tại sao data mới là cốt lõi?[¶](#tai-sao-data-moi-la-cot-loi)

Flow và thành phần cho BA biết “chức năng đi qua đâu”. Nhưng câu hỏi thực sự quyết định khả thi là: **data để làm chức năng đó có sẵn sàng chưa, và nếu chưa thì làm thế nào để có?**

Phần lớn những lần Dev nói “phức tạp” hay “không làm được”, lý do thực sự không phải là logic nghiệp vụ khó hay giao diện phức tạp — mà là **vấn đề về data**: thiếu data, data không chuẩn, data đang ở nơi khó lấy, hoặc cần join nhiều nguồn mới có được thứ cần tính.

Khi BA hiểu rõ thực trạng data, mọi câu jargon của Dev sẽ tự nhiên dịch được sang ngôn ngữ nghiệp vụ: “Làm được nhưng chậm vì phải lấy nhiều nơi”, “Làm được nhưng phải sửa phần nhập liệu phía trước”, hoặc “Thực sự chưa có đủ data để làm ở thời điểm này”.

### Chuỗi câu hỏi về data[¶](#chuoi-cau-hoi-ve-data)

BA không cần hỏi hết một lúc. Dẫn dắt từng bước, theo chuỗi logic sau:

**Bước 1: Data lấy từ đâu?**
“Để ra được kết quả này, data lấy từ những đâu?”
Mục tiêu là hiểu data đến từ bao nhiêu nguồn:

- **Chỉ từ DB nội bộ**: đơn giản nhất — data đã ở trong hệ thống, chỉ cần lấy ra và xử lý
- **Nhiều bảng / nhiều module trong cùng hệ thống**: phức tạp hơn vì cần hiểu quan hệ dữ liệu, nhưng vẫn nằm trong tầm kiểm soát
- **Nhiều nguồn bên ngoài**: DB nội bộ + API đối tác + file FTP + hệ thống kho/ERP — loại này khó nhất vì phải lấy từ nhiều nơi, chờ, map lại rồi mới xử lý tiếp
Quy tắc đơn giản: **càng nhiều nguồn, độ phức tạp càng tăng, và khả năng làm realtime càng giảm.**

**Bước 2: Logic xử lý thế nào?**
“Lấy data về rồi xử lý ra sao mới ra được kết quả cần?”
Có ba dạng phổ biến mà BA thường gặp:

**Dạng 1 — Lấy nhiều nguồn rồi tổng hợp:** Ví dụ phải lấy đơn từ hệ thống bán hàng, trạng thái từ kho, thông tin thanh toán từ cổng, rồi mới join lại và tính toán. Loại này volume thường lớn, join chậm, nên rất khó làm realtime — nhưng làm được nếu chấp nhận chạy theo job định kỳ.

**Dạng 2 — Chỉ nội bộ nhưng logic phức tạp:** Ví dụ một báo cáo chỉ lấy từ DB nội bộ nhưng cần hiểu quan hệ nhiều bảng, có nhiều rule suy luận, nhiều ngoại lệ. Nghe có vẻ đơn giản vì không phụ thuộc bên ngoài, nhưng query/logic lại nặng — effort lớn, cần đầu tư thời gian.

**Dạng 3 — Tính toán / phân nhóm:** Dù lấy từ đâu, vẫn cần hỏi thêm: group theo tiêu chí gì, lấy bản ghi nào khi có nhiều kết quả, có công thức tính đặc biệt không, có ngoại lệ nào cần xử lý riêng không. Những câu hỏi này giúp BA hiểu rule nghiệp vụ đằng sau, thay vì chỉ biết “cần tính toán”.

**Bước 3: Data đó đã có trong hệ thống chưa?**
“Những data cần cho chức năng này hiện đã có trong hệ thống chưa?”
Đây là câu hỏi quan trọng nhất. Ba tình huống phổ biến:

- **Đã có đủ**: hệ thống đã lưu, chỉ cần lấy ra và xử lý. Đây là tình huống lý tưởng — effort chủ yếu nằm ở phần build tính năng, không phải thu thập data
- **Có một phần**: một số field đã có, một số thì thiếu — có thể thiếu field, thiếu quan hệ giữa các bảng, hoặc thiếu lịch sử (hệ thống chỉ lưu từ một thời điểm nào đó)
- **Chưa có**: hệ thống chưa từng lưu thứ đó. Loại này cần làm thêm nhiều việc trước khi feature có thể ra đời
**Bước 4: Chưa có thì làm thế nào để có?**
“Muốn có data đó thì lấy từ đâu, hoặc sinh ra bằng cách nào?”
Khi data chưa có, thường có 4 hướng xử lý:

- **Sửa chức năng phía trước để bắt đầu thu thập**: ví dụ thêm field vào màn hình nhập liệu, sửa API để lưu thêm thông tin — data sẽ có từ ngày triển khai trở đi, không hồi tố được
- **Nhận từ bên khác cung cấp thêm**: ví dụ đối tác bắt đầu gửi thêm field trong API — cần xác nhận họ có hỗ trợ không, timeline là bao lâu
- **Suy ra từ data đang có**: ví dụ tính toán ngược từ các thông tin khác đã lưu — cần kiểm tra xem suy luận đó có đủ chính xác không
- **Migrate / bổ sung dữ liệu cũ**: lấy data từ nơi khác hoặc xử lý data cũ để điền vào — tốn công, có thể không đầy đủ
Mỗi hướng đều cần hỏi tiếp về tính khả thi: Sửa chức năng trước đụng nhiều không? Migrate được bao nhiêu phần? Đối tác có đồng ý hỗ trợ không và trong bao lâu?

**Tổng kết chuỗi câu hỏi về data:**
**Lấy từ đâu → xử lý/tính thế nào → đã có chưa → chưa có thì làm sao để có → cái giá và giới hạn là gì?**
Khi BA lái Dev trả lời được chuỗi này, kết luận khả thi sẽ tự nhiên hiện ra.

### Bảng quy đổi: thực chất data → kết luận mang đi[¶](#bang-quy-oi-thuc-chat-data-ket-luan-mang-i)

Thực chất về data

Kết luận BA nên mang đi

Phải lấy từ rất nhiều nguồn rồi mới tổng hợp

Làm được — nhưng dễ chậm; nên chạy job định kỳ, không realtime

Logic lấy data nội bộ phức tạp, nhiều bảng, nhiều rule

Làm được — nhưng effort lớn, cần thời gian và hiểu rõ model dữ liệu

Data chưa lưu; phải sửa chức năng trước + có thể migrate

Làm được từ nay — lịch sử bị giới hạn hoặc tốn thêm effort migrate

Thiếu data và không có nguồn nào để sinh ra được

Thực sự chưa khả thi ở thời điểm này

## Thực tế trông như thế nào: một cuộc hội thoại đầy đủ[¶](#thuc-te-trong-nhu-the-nao-mot-cuoc-hoi-thoai-ay-u)

Lý thuyết vậy đủ rồi. Giờ hãy xem một cuộc hội thoại thực tế để thấy cả 3 phần trên hoạt động cùng nhau như thế nào.

**Bối cảnh:** PO muốn làm báo cáo tỷ lệ hủy đơn theo lý do hủy để phân tích xu hướng và cải thiện trải nghiệm khách hàng. BA được giao đánh giá khả thi với team Dev.

**Dev:** “Cái báo cáo này phức tạp lắm, khó làm lắm.”

**BA:** “Ok, em muốn hiểu rõ hơn. Anh đi giúp em flow hiện tại: khi khách hủy đơn thì hệ thống xử lý những bước nào?”

**Dev:** “Khách bấm hủy → màn hình hiện ô nhập lý do → gọi API hủy → API cập nhật trạng thái → gửi thông báo cho khách.”

**BA:** “Vậy flow nghe khá rõ. Vậy vướng ở chỗ nào — data để báo cáo lấy từ đâu, lý do hủy hiện đang được lưu thế nào?”

**Dev:** “Lý do hủy có lưu — nhưng đang là ô text tự do. Khách muốn ghi gì thì ghi, không chuẩn hóa.”

**BA:** “À, vậy data thực ra đã có, nhưng vấn đề là không group được vì mỗi đơn ghi khác nhau?”

**Dev:** “Đúng. Không thể aggregate theo lý do được. Người thì ghi ‘đổi ý’, người thì ghi ‘thay đổi kế hoạch’, người thì ghi ‘muốn đặt lại đơn khác’ — không chuẩn thì không thể thống kê.”

**BA:** “Hiểu rồi. Vậy muốn báo cáo được thì phải sửa chỗ nào? Cần làm những gì?”

**Dev:** “Phải đổi màn hình hủy từ nhập text tự do sang chọn từ danh sách lý do định sẵn. Rồi sửa API lưu theo giá trị chuẩn đó. Bao nhiêu đó thôi.”

**BA:** “Còn dữ liệu cũ — những đơn đã hủy trước đây thì sao, có dùng được cho báo cáo không?”

**Dev:** “Cũ thì toàn text lộn xộn. Muốn dùng được phải migrate — map từng giá trị text cũ về lý do mới trong danh sách chuẩn. Tốn công mà chưa chắc map hết được, vì nhiều kiểu ghi lắm.”

**BA:** “Nếu không migrate thì báo cáo chỉ chính xác từ ngày triển khai trở đi, đúng không? Lịch sử cũ thì sẽ thiếu hoặc không tin cậy?”

**Dev:** “Đúng vậy.”

Sau đoạn hội thoại này, BA đã có đủ thông tin để tổng hợp. Không phải 1 việc, mà là 3 việc cần làm rõ với PO:

- **Sửa giao diện hủy đơn** — từ ô nhập text tự do sang dropdown chọn lý do từ danh sách chuẩn hóa
- **Sửa API** — lưu lý do hủy theo giá trị chuẩn trong danh sách, không phải text tùy ý
- **Quyết định về data cũ** — có migrate không, migrate được bao nhiêu phần trăm, và PO cần biết là báo cáo lịch sử sẽ bị giới hạn nếu không migrate
Kết luận mang đi cho PO:
“Báo cáo làm được — nhưng cần làm 3 việc trước: (1) đổi màn hình hủy đơn sang chọn lý do từ danh sách, (2) sửa API lưu theo giá trị chuẩn, (3) quyết định có migrate data cũ không — nếu không migrate thì báo cáo lịch sử sẽ chỉ chính xác từ ngày triển khai trở đi.”
Đó là một kết luận dùng được — có scope rõ, có giới hạn rõ, và giúp PO ra quyết định. Không phải *“Dev bảo phức tạp lắm”*.

## Kết: kỹ năng này không phải là học kỹ thuật[¶](#ket-ky-nang-nay-khong-phai-la-hoc-ky-thuat)

Nhiều BA nghĩ rằng để làm việc tốt hơn với Dev, họ cần học thêm kỹ thuật — hiểu Kafka là gì, biết SQL, đọc được code.

Điều đó không sai. Nhưng nó không phải điều kiện bắt buộc để làm tốt vai trò BA.

Điều kiện bắt buộc là: **biết hỏi đúng câu để lấy đúng thông tin.**

Khi BA giữ thói quen kéo Dev về 2 kênh — **flow xử lý** và **data logic** — thì hầu hết những tình huống “không làm được” sẽ tự nhiên mở ra thêm ít nhất một phương án, hoặc ít nhất một kết luận rõ ràng hơn để mang đi.

Vì phần lớn khi Dev nói “phức tạp”, vấn đề không phải là BA thiếu thuật ngữ kỹ thuật. Vấn đề là cuộc hội thoại đang nằm sai kênh — và Dev không có lý do để chuyển kênh nếu BA không chủ động lái.

Đó là việc của BA.

*Bạn đã từng gặp tình huống tương tự chưa? Câu nào từ Dev từng làm bạn bí nhất?*

Dev nói

BA không cần biết

BA cần hỏi

“Đẩy event qua Kafka”

Kafka là message broker gì, hoạt động ra sao

“Đẩy qua đó để làm gì? Bên kia nhận rồi xử lý thế nào? Có bị trễ không? Nếu fail thì sao?”

“Đưa vào queue xử lý”

Queue là hàng đợi kiểu gì, FIFO hay gì

“Đưa vào đó rồi bao lâu mới xử lý? Có đảm bảo xử lý được hết không? Có retry không?”

“Lấy file qua FTP”

FTP là giao thức truyền file như thế nào

“File đó ai đẩy lên, bao giờ có? Nếu chưa có thì mình chờ hay bỏ qua? Định dạng gì?”

“Gọi API đối tác”

API đó dùng REST, SOAP hay gì

“Đối tác có hỗ trợ trường hợp mình cần không? Họ có SLA không? Nếu họ timeout thì luồng của mình xử lý thế nào?”

Dev thường nói

Đừng dừng ở đó

Hãy lái sang

“Không support”

“Vậy là không làm được?”

Flow hiện tại đi những bước nào? Vướng ở bước nào cụ thể?

“Phải đụng nhiều service”

Gật đầu rồi báo PO

Trong flow đó, thành phần nào tham gia — FE, BE, Kafka, FTP, đối tác…?

“Logic / query phức tạp”

Nhận cảm tính rồi bỏ qua

Data lấy từ đâu? Kết hợp/tính/suy luận thế nào mới ra kết quả cần?

“Thiếu data / schema chưa có”

“Vậy thôi, không làm được”

Data cần là gì? Đã có chưa? Chưa có thì làm sao để có?

“Phải migrate nhiều”

Sợ rồi dừng

Vì trước chưa lưu? Muốn có phải sửa chức năng nào phía trước?

“Không làm realtime được”

Kết luận là chức năng chết

Vì lấy nhiều nguồn / tính nặng nên chậm → vậy làm job được không?