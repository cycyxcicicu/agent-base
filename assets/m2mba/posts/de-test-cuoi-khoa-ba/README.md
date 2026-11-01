---
id: 41
title: "Bài test cuối khóa BA"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T15:28:34.000Z"
source_url: "https://m2mba.com/blog/articles/de-test-cuoi-khoa-ba"
---

# Bài test cuối khóa BA

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T15:28:34.000Z*

![Ảnh bìa](images/3224d6ea-c0e1-4244-b221-bea1d9869ccc.png)

**ĐỀ TEST CUỐI KHÓA BA **

**Case study**: Xây dựng sản phẩm quản lý bãi gửi xe thông minh cho tập đoàn XXX(cứ ghi thế cho oai chứ bọn e tìm hiểu quy trình của bên nào cũng đc nhé, ý là xây dựng SP  nhé).

**Bài 1 (2đ):** Khơi gợi yêu cầu

**Yêu cầu 1 (1 điểm):** Đưa ra quy trình tổng quan (có thể có nhiều hơn 1 quy trình tổng quan): Bạn hãy tìm ra 1 đối tượng chính cần quản lý trong hệ thống quản lý bãi gửi xe thông minh và từ đó tìm ra các bước quản lý cả vòng đời của đối tượng đó. Từ đó đưa ra được quy trình tổng quan tương ứng.

Đối tượng: Vé xe

Quy trình tổng quan:

**Yêu cầu 2 (1 điểm):** Tập trung tìm hiểu về quy trình, công việc của stakeholder hiện tại liên quan tới Quy trình đăng ký vé tháng (coi là quản lý thủ công cả nhé), và đưa ra được các yêu cầu sau (ở đây chị chỉ định quy trình cần tìm hiểu là đăng ký vé tháng luôn, nó ko bắt buộc phải có trong quy trình tổng quan ở trên nhé cả nhà, chị cần bọn e tư duy quy trình tổng quan như c dạy trên lớp):

Quy trình hiện tại: 

 

- Quy trình dạng text theo format: BướcNgười thực hiệnMô tả1Cư dân
Cư dân sẽ tới quầy lễ tân xin phiếu đăng ký thẻ xe và điền phiếu đăng ký thẻ xe sau đó nộp phiếu cho lễ tân. Khi nộp phiếu cần có kèm theo những giấy tờ sau:

- Photo CMND/CCCD của chủ xe
- Photo Giấy phép đăng ký xe có hiệu lực
Mẫu phiếu: 

2Cư dân 
Cư dân sau khi nộp đủ giấy tờ sẽ tiến hành nộp phí làm thẻ và phí gửi xe tháng đầu tiên. Chung cư sẽ thu trước phí gửi xe theo tháng. Tính theo thời điểm đăng ký vé gửi xe thuộc tháng nào thì sẽ tính phí kể từ tháng đó (Không tính theo 30 ngày mà sẽ tính phí theo tháng). Đối với các tháng sau, chung cư sẽ thu đầu tháng kèm phí dịch vụ và tiền điện nước.

VD: Đăng ký gửi xe tháng tháng từ ngày 15/07 cư dân sẽ phải đóng phí gửi xe tháng đầu tiên là tháng 7.

Sau khi nộp phí, cư dân sẽ nhận được 1 biên lai thu tiền từ lễ tân.

3Lễ tân
Bộ phận lễ tân sẽ tiếp nhận thông tin đăng ký từ cư dân, kiểm tra tính hợp lệ và lưu lại phiếu đăng ký của cư dân. Lễ tân sẽ thu tiền phí đăng ký từ cư dân và ghi biên lai thu tiền cho cư dân.

Lễ tân sẽ thực hiện tổng hợp phiếu đăng ký của cư dân 1 tuần 1 lần vào file excel và gửi file cho bộ phận Ban quản lý chung cư.

Mẫu file excel tổng hợp:

 
4BQL chung cư
Ban quản lý chung cư sẽ nhận file excel và xem xét các yếu tố như sức chứa của bãi gửi xe, quy định về đăng ký (Mỗi căn hộ chỉ được phép gửi 4 xe 2 bánh và 2 xe ô tô) và các yêu cầu khác để quyết định việc duyệt đăng ký vé gửi xe tháng. 

BQL sẽ điền tình trạng duyệt (Duyệt/từ chối) và mã thẻ xe vào file excel đã nhận trước đó. Nếu từ chối sẽ gửi kèm cả lý do.
5BQL Chung cư
BQL sẽ dựa theo mã thẻ và tiến hành in vé gửi xe tháng cho cư dân. Mẫu vé

6Lễ tân
BQL chung cư sẽ gửi lại danh sách đăng ký đã duyệt và kèm theo vé xe cho lễ tân. Lễ tân sẽ thông báo tới cư dân và thực hiện bàn giao lại vé gửi xe.

7Cư dânCư dân đến cung cấp số căn hộ, tên chủ xe để nhận thẻ xe.
 

- **Phân tích vấn đề****Thông tin****Hiện tại****Vấn đề****Mức độ ưu tiên****Tương lai****Nội dung thay đổi**Cư dân đăng ký vé thángCư dân sẽ tới quầy lễ tân xin phiếu đăng ký thẻ xe và điền phiếu đăng ký thẻ xe sau đó nộp phiếu cho lễ tân Cư dân phải đi lại nhiều lần, mất thời gian. CaoCư dân có thể đăng ký vé tháng trên app điện thoại 
Xây dựng hệ thống cho phép:

- Cư dân tạo đăng ký vé tháng trên điện thoại 

- Cư dân có thể thanh toán phí trực tuyến
Tiếp nhận đơn đăng ký và tổng hợp vào file excelLễ tân tiếp nhận đơn đăng ký và lưu trữ phiếu đăng ký. Sau đó tổng hợp vào file excel để gửi qua mail cho BQL chung cư
Việc tổng hợp phiếu thực hiện 1 tuần 1 lần và rất nhiều công sức khi phải nhập lại thông tin từ phiếu đăng ký. Gây ra thời gian chờ cấp vé sẽ lâu

Việc lưu trữ phiếu đăng ký và giấy tờ photo có thể gây thất lạc và phải có kho lưu trữ.
CaoLễ tân có thể đăng ký vé xe cho cư dân trên hệ thống và đính kèm hình ảnh photo giấy tờ.
Xây dựng hệ thống cho phép:

- Lễ tân tạo đăng ký vé xe cho cư dân
 
Duyệt danh sách đăng ký vé thángBQL chung cư sẽ nhận danh sách đăng ký vé tháng nhận được qua mail. BQL sẽ xem xét các yếu tố như sức chứa của bãi gửi xe, quy định về đăng ký để quyết định việc duyệt đăng ký vé gửi xe tháng
BQL có thể bị sót mail gửi phiếu đăng ký làm chậm quá trình duyệt

Việc kiểm tra sức chứa của bãi gửi xe và quy định đăng ký được làm thủ công gây mất nhiều công sức
CaoBQL có thể tiếp nhận đăng ký trên phần mềm và duyệt đăng ký.
Xây dựng hệ thống cho phép:

-Hệ thống check thông tin bãi gửi xe và số lượng đăng ký gửi xe trong quá trình cư dân gửi đăng ký

-BQL chung cư xem danh sách đăng ký và duyệt đăng ký vé tháng trên phần mềm

- Mindmap tổng hợp công việc của stakeholder: 

**Bài 2 (1đ):** Vẽ quy trình đề xuất triển khai trên hệ thống của quy trình bạn đã chọn

 
BướcNgười thực hiệnMô tảThủ công/Hệ thống1Cư dân
Cư dân đăng nhập vào app cư dân và thực hiện đăng ký vé gửi xe tháng

Các thông tin cần nhập khi đăng ký vé tháng

- Loại xe (Xe ô tô, xe máy/xe máy điện, xe đạp/xe đạp điện)
- Biển số
- Nhãn hiệu
- Màu sơn
- Họ tên chủ xe
- Số CMND/CCCD chủ xe
- Ảnh đính kèm: CMND/CCCD chủ xe và giấy phép đăng ký xe còn hiệu lựcHệ thống2Cư dân
Sau khi nhập thông tin cư dân tiến hành thanh toán phí làm thẻ và lựa chọn các hình thức thanh toán trực tuyến: Thanh toán qua tài khoản ngân hàng hoặc các loại thẻ (ATM/internet banking), Tín dụng/thẻ ghi nợ quốc tế (Visa/master/JCB), Ví điện tử (zalopay)

Số tiền thanh toán bao gồm phí làm thẻ và phí gửi xe tháng đầu tiên. Chung cư sẽ thu trước phí gửi xe theo tháng. Tính theo thời điểm đăng ký vé gửi xe thuộc tháng nào thì sẽ tính phí kể từ tháng đó (Không tính theo 30 ngày mà sẽ tính phí theo tháng). Đối với các tháng sau, chung cư sẽ thu đầu tháng kèm phí dịch vụ và tiền điện nước.

 
Hệ thống3Hệ thốngKhi cư dân thực hiện thanh toán online, hệ thống sẽ thực hiện đồng bộ dữ liệu với hệ thống đối tác thanh toán để cập nhật thông tin thanh toán của cư dânHệ thống4BQL chung cư
BQL chung cư sẽ xem danh sách đăng ký thẻ tháng ở trạng thái chờ duyệt và tiến hành duyệt đăng ký. Các thông tin đăng ký BQL tiếp nhận gồm:

- Mã đăng ký
- Thời gian đăng ký
- Số căn hộ
- Tòa
- Loại xe (Xe ô tô, xe máy/xe máy điện, xe đạp/xe đạp điện)
- Biển số
- Nhãn hiệu
- Màu sơn
- Họ tên chủ xe
- Số CMND/CCCD chủ xe
- Ảnh đính kèm: CMND/CCCD chủ xe và giấy phép đăng ký xe còn hiệu lực
- Trạng thái đăng ký: Đã duyệt/ chờ duyệt/ từ chốiHệ thống5BQL chung cư
Sau khi duyệt đăng ký, BQL chung cư sẽ tích phát hành thẻ xe. Thông tin thẻ xe được tạo bao gồm:

- Mã thẻ xe
- Loại thẻ
- Tên chủ xe
- Biển số xe
- Thời hạn thẻ
- Tình trạng thẻ 
Sau đó thông qua máy đọc thẻ, sẽ thực hiện gán thông tin thẻ vào thẻ từ.
Hệ thống6Lễ tânLễ tân sẽ nhận được danh sách bàn giao thẻ kèm thẻ từ và tiến hành bàn giao thẻ cho cư dân. Lễ tân yêu cầu cư dân ký xác nhận vào danh sáchThủ công7Cư dânKhi đăng ký được duyệt, hệ thống sẽ thông báo về app cho cư dân, cư dân sẽ tới quầy lễ tân cung cấp số căn hộ và tên chủ xe để nhận thẻ xeThủ công
 

 
BướcNgười thực hiệnMô tảThủ công/Hệ thống1Cư dân
Cư dân tới quầy lễ tân và đăng ký xin làm vé gửi xe tháng. Các thông tin cư dân cần cung cấp gồm: 

- Số căn hộ
- Tên chủ căn hộ
- Loại xe (Xe ô tô, xe máy/xe máy điện, xe đạp/xe đạp điện)
- Biển số
- Nhãn hiệu
- Màu sơn
- Họ tên chủ xe
- Photo CMND/CCCD chủ xe
- Photo giấy phép đăng ký xe còn hiệu lựcThủ công2Lễ tân
Lễ tân sẽ thực hiện tra cứu thông tin căn hộ và tên chủ căn hộ có tồn tại trên hệ thống hay không và tiến hành đăng ký thẻ xe tháng trên hệ thống theo thông tin cư dân cung cấp

Các thông tin cần nhập khi đăng ký vé tháng

- Số căn hộ
- Tòa
- Loại xe (Xe ô tô, xe máy/xe máy điện, xe đạp/xe đạp điện)
- Biển số
- Nhãn hiệu
- Màu sơn
- Họ tên chủ xe
- Số CMND/CCCD chủ xe
- Ảnh đính kèm: photo CMND/CCCD chủ xe và giấy phép đăng ký xe còn hiệu lựcHệ thống3Cư dân
Cư dân sau khi nộp đủ giấy tờ sẽ tiến hành nộp phí làm thẻ và phí gửi xe tháng đầu tiên. Chung cư sẽ thu trước phí gửi xe theo tháng. Tính theo thời điểm đăng ký vé gửi xe thuộc tháng nào thì sẽ tính phí kể từ tháng đó (Không tính theo 30 ngày mà sẽ tính phí theo tháng). Đối với các tháng sau, chung cư sẽ thu đầu tháng kèm phí dịch vụ và tiền điện nước.

VD: Đăng ký gửi xe tháng tháng từ ngày 15/07 cư dân sẽ phải đóng phí gửi xe tháng đầu tiên là tháng 7.

Sau khi nộp phí, cư dân sẽ nhận được 1 biên lai thu tiền từ lễ tân.
Thủ công4BQL chung cư
BQL chung cư sẽ xem danh sách đăng ký thẻ tháng ở trạng thái chờ duyệt và tiến hành duyệt đăng ký. Các thông tin đăng ký BQL tiếp nhận gồm:

- Mã đăng ký
- Thời gian đăng ký
- Số căn hộ
- Tòa
- Loại xe (Xe ô tô, xe máy/xe máy điện, xe đạp/xe đạp điện)
- Biển số
- Nhãn hiệu
- Màu sơn
- Họ tên chủ xe
- Số CMND/CCCD chủ xe
- Ảnh đính kèm: CMND/CCCD chủ xe và giấy phép đăng ký xe còn hiệu lực
Trạng thái đăng ký: Đã duyệt/ chờ duyệt/ từ chối
Hệ thống5BQL chung cư
Sau khi duyệt đăng ký, BQL chung cư sẽ tích phát hành thẻ xe. Thông tin thẻ xe được tạo bao gồm:

- Mã thẻ xe
- Loại thẻ
- Tên chủ xe
- Biển số xe
- Thời hạn thẻ
- Tình trạng thẻ 
Sau đó thông qua máy đọc thẻ, sẽ thực hiện gán thông tin thẻ vào thẻ từ.
Hệ thống6Lễ tânLễ tân sẽ nhận được danh sách bàn giao thẻ kèm thẻ từ và tiến hành bàn giao thẻ cho cư dân. Lễ tân yêu cầu cư dân ký xác nhận vào danh sáchThủ công7Cư dânKhi đăng ký được duyệt, hệ thống sẽ thông báo về app cho cư dân, cư dân sẽ tới quầy lễ tân cung cấp số căn hộ và tên chủ xe để nhận thẻ xeThủ công
**Bài 3 (3đ):** Bạn hãy xác định UC từ quy trình bạn đề xuất ở bài 1

- Với các UC dạng chỉnh sửa, xóa (Các UC khác không cần): Chị cần các em nêu rõ hơn các thông tin sau trong mô tả Điều kiện chỉnh sửa/xóa (thường liên quan tới trạng thái)
- Thông tin gì được chỉnh sửa (nếu tất cả thì ghi tất cả)**STT****Actor****Ứng dụng****Usecase****Mô tả/mục đích**1Cư dânApp tiện ích cư dânĐăng nhậpCho phép cư dân được cấp tài khoản đăng nhập vào app tiện ích cư dân2Cư dânApp tiện ích cư dânXem thông tin cá nhânCho phép cư dân xem thông tin cá nhân3Cư dânApp tiện ích cư dânChỉnh sửa thông tin cá nhânChỉnh sửa số điện thoại liên hệ và email4Cư dânApp tiện ích cư dânĐăng ký thẻ xeCho phép cư dân đăng ký thẻ xe tháng5Cư dânApp tiện ích cư dânThanh toán phí trực tuyếnCho phép cư dân thực hiện thanh toán các loại phí trực tuyến6Cư dânApp tiện ích cư dânXem thông báoCho phép cư dân xem thông báo từ BQL chung cư và thông báo liên quan đến các chức năng của app7Cư dânApp tiện ích cư dânXem danh sách đăng ký thẻ xe cá nhânCho phép cư dân xem danh sách đăng ký thẻ xe cá nhân8Cư dânApp tiện ích cư dânXem chi tiết đăng ký thẻ xeCho phép cư dân xem chi tiết đăng ký thẻ xe9Cư dânApp tiện ích cư dânChỉnh sửa đăng ký thẻ xe
Cư dân chỉ được phép chỉnh sửa thông tin đăng ký thẻ xe tại trạng thái chờ duyệt và phản hồi

Tại trạng thái phản hồi, cư dân chỉnh sửa lại thông tin và lưu đăng ký sẽ chuyển trạng thái thành chờ duyệt
10Cư dânApp tiện ích cư dânXem danh sách thẻ xe của căn hộCho phép cư dân xem danh sách thẻ xe của căn hộ của mình11Cư dânApp tiện ích cư dânThông báo mất thẻCho phép cư dân thông báo mất thẻ xe12Cư dânApp tiện ích cư dânYêu cầu hủy thẻ xe Cho phép cư dân gửi yêu cầu hủy thẻ xe13Lễ tân, BQL chung cưWeb adminTìm kiếm khách hàngTìm kiếm khách hàng theo tiêu chí: Tên, số căn hộ14Lễ tân, BQL chung cưWeb adminXem chi tiết khách hàngXem chi tiết thông tin khách hàng để thích hiện các chức năng đăng ký/hủy thẻ tháng và cập nhật thông tin khách hàng15Lễ tân, BQL chung cưWeb adminĐăng ký thẻ thángCho phép lễ tân, BQL chung cư tạo đăng ký thẻ xe16Lễ tân, BQL chung cưWeb adminCập nhật thông tin khách hàngĐược chỉnh sửa tất cả thông tin17Lễ tân, BQL chung cưWeb adminXuất khẩu danh sách khách hàngCho phép xuất khẩu danh sách khách hàng 18Lễ tân, BQL chung cưWeb adminYêu cầu hủy thẻ thángCho phép lễ tân, BQL chung cư có thể tạo yêu cầu hủy thẻ tháng19Lễ tân, BQL chung cưWeb adminXem danh sách đăng ký thẻ thángCho phép xem danh sách đăng ký thẻ tháng20Lễ tân, BQL chung cưWeb adminLọc/tìm kiếm đăng ký thẻ thángCho phép lọc tìm kiếm yêu cầu đăng ký thẻ tháng theo nhiều tiêu chí khác nhau: trạng thái, thời gian, người tạo21Lễ tân, BQL chung cưWeb adminXem chi tiết đăng ký thẻ tháng Cho phép xem chi tiết yêu cầu đăng ký thẻ tháng22Lễ tân, BQL chung cưWeb adminChỉnh sửa đăng ký thẻ tháng
Cho phép chỉnh sửa thông tin đăng ký thẻ tháng ở trạng thái Chờ duyệt và Phản hồi.

Tại trạng thái phản hồi, sau khi chỉnh sửa lại thông tin và lưu đăng ký sẽ chuyển trạng thái thành chờ duyệt
23BQL chung cưWeb adminPhê duyệt/từ chối/phản hồi đăng ký thẻ tháng
Cho phép BQL chung cư duyệt/từ chối/phản hồi yêu cầu đăng ký thẻ tháng 

 
24Lễ tân, BQL chung cưWeb adminXem danh sách yêu cầu hủy thẻ thángCho phép xem danh sách yêu cầu hủy thẻ tháng25Lễ tân, BQL chung cưWeb adminLọc/tìm kiếm yêu cầu hủy thẻ thángCho phép lọc tìm kiếm yêu cầu hủy thẻ tháng theo nhiều tiêu chí khác nhau: trạng thái, thời gian, người tạo26Lễ tân, BQL chung cưWeb adminXem chi tiết yêu cầu hủy thẻ tháng Cho phép xem chi tiết yêu cầu  thẻ tháng27BQL chung cưWeb adminPhê duyệt/từ chối yêu cầu hủy thẻ tháng
Cho phép Cho phép BQL chung cư duyệt/từ chối yêu cầu hủy thẻ tháng

Đối với yêu cầu hủy thẻ tháng, chỉ được phê duyệt khi đã thu hồi được thẻ tháng
28Lễ tân, BQL chung cưWeb adminXem danh sách thẻ thángCho phép xem danh sách thẻ tháng29BQL chung cưWeb adminTạo mới thẻ thángCho phép tạo thẻ mới30Lễ tân, BQL chung cưWeb adminTìm kiếm/ lọc danh sách thẻ  thángCho phép tìm kiếm/lọc danh sách thẻ tháng theo nhiều tiêu chí khác nhau: mã thẻ, trạng thái của thẻ, tên chủ thẻ, biển số đăng ký31Lễ tân, BQL chung cưWeb adminXem chi tiết thẻ thángCho phép xem chi tiết thẻ32Lễ tân, BQL chung cưWeb adminXuất khẩu danh sách thẻ thángCho phép xuất khẩu danh sách thẻ phục vụ cho việc in danh sách bàn giao thẻ tháng33BQL chung cưWeb adminKhóa/Mở /Hủy thẻ
Cho phép BQL chung cư thực hiện Khóa/mở / hủy thẻ

- Khóa thẻ ở trạng thái: Chờ sử dụng/đang sử dụng
- Mở thẻ khi ở trạng thái: đã khóa
- Hủy thẻ: ở trạng thái chờ sử dụng/đang sử dụng34Lễ tân, BQL chung cưWeb adminXem danh sách thẻ lượtCho phép xem danh sách thẻ lượt35BQL chung cưWeb adminTạo mới thẻ thángCho phép tạo thẻ mới36Lễ tân, BQL chung cưWeb adminTìm kiếm/ lọc danh sách thẻ  thángCho phép tìm kiếm/lọc danh sách thẻ tháng theo nhiều tiêu chí khác nhau: mã thẻ, trạng thái của thẻ37Lễ tân, BQL chung cưWeb adminXem chi tiết thẻ lượtCho phép xem chi tiết thẻ38Lễ tân, BQL chung cưWeb adminXuất khẩu danh sách thẻ lượtCho phép xuất khẩu danh sách thẻ 39BQL chung cưWeb adminKhóa/Mở /Hủy thẻ
Cho phép BQL chung cư thực hiện Khóa/mở / hủy thẻ

- Khóa thẻ ở trạng thái: Chờ sử dụng/đang sử dụng
- Mở thẻ khi ở trạng thái: đã khóa
- Hủy thẻ: ở trạng thái chờ sử dụng/đang sử dụng40BQL chung cưWeb adminĐăng nhậpCho phép người dùng đăng nhập vào web admin41BQL chung cưWeb adminQuên mật khẩuCho phép người dùng sử dụng tính năng quên mật khẩu42Admin hệ thốngWeb adminTìm kiếm tài khoảnCho phép tìm kiếm tài khoản theo tên người dùng43Admin hệ thốngWeb adminXem chi tiết tài khoảnCho phép xem chi tiết tài khoản44Admin hệ thốngWeb adminChỉnh sửa thông tin tài khoảnChỉnh sửa thông tin tài khoản 45Admin hệ thốngWeb adminThêm/khóa tài khoảnCho phép thêm tài khoản mới và khóa những tài khoản người dùng không còn sử dụng46Admin hệ thốngWeb adminQuản lý phân quyềnCho phép phân quyền sử dụng các phân hệ trong hệ thống47Admin hệ thốngWeb adminQuản lý lịch sử hoạt độngCho phép xem lịch sử hoạt động của từng người dùng trên hệ thống48Admin hệ thốngWeb adminReset mật khẩuCho phép reset lại mật khẩu của người dùng trên hệ thống49BQL chung cưWeb adminXem báo cáo thống kêCho phép xem và xuất báo cáo thống kê về doanh thu, lượt gửi xe, thẻ xe theo khoảng thời gian
 

**Bài 4(1đ): **Tạo kiến trúc thông tin (IA) và thiết kế tổng quan cho 1 ứng dụng mà bạn lựa chọn với các UC bạn đã tìm ra ở bài 3 (tùy bọn e chọn)

 

 

 

**Kiến trúc thông tin (IA)**

****

 

 

 

 

 

 

 

 

**Thiết kế tổng quan**

****

 

**Bài 5(3đ):** Bạn hãy  đặc tả 2 UC sau

**5.1. Danh sách yêu cầu đăng ký vé tháng**

**5.1.1. Mô tả chung**
**Tên Usecase**Xem danh sách yêu cầu đăng ký vé thángActorLễ tân, BQL chung cư Mục đíchCho phép lễ tân, BQL chung cư xem danh sách yêu cầu đăng ký vé thángPreconditionNgười dùng đăng nhập vào hệ thống và được phân quyền quyền quản lý đơn thẻ thángMain flow
1.Chọn quản lý đơn thẻ tháng 

2. Hệ thống hiển thị 2 mục con Đăng ký thẻ tháng và Hủy thẻ tháng

3.Chọn Đăng ký thẻ tháng

4. Hệ thống hiển thị danh sách yêu cầu đăng ký thẻ tháng mặc định

5.Nhập thông tin tìm kiếm

6. Hệ thống hiển thị danh sách tìm kiếm theo yêu cầu 
Post ConditionHiển thị danh sách yêu cầu đăng ký thẻ tháng mặc định và hiển thị danh sách yêu cầu đăng ký thẻ tháng theo kết quả tìm kiếm của người dùng
**5.1.2. Màn hình**

****

**5.1.3. Mô tả màn hình**
**STT****Tên control****Loại control****Mô tả & ghi chú**1TòaComboboxLựa chọn tòa nhà để tìm kiếm. Hiển thị danh sách tòa nhà có trên hệ thống2Trạng tháiCombobox
Hiển thị danh sách trạng thái để tìm kiếm, bao gồm các trạng thái

- Tất cả (Mặc định)
- Chờ duyệt
- Đã duyệt
- Phản hồi
- Từ chối3Căn hộCombobox
Hiển thị danh sách căn hộ thuộc tòa đang chọn và đang hoạt động trên hệ thống

 
4Loại xeCombobox
Hiển thị danh sách loại xe để tìm kiếm, bao gồm:

- Tất cả (Mặc định)
- Ô tô
- Xe máy
- Xe máy điện
- Xe đạp
- Xe đạp điện5Tên chủ xeTextboxNhập tên chủ xe để tìm kiếm6Ngày đăng ký – Từ Datepicker
Chọn thông tin tìm kiếm theo ngày tạo đăng ký – Từ ngày, chỉ chọn đến ngày- không chọn đến giờ-phút-giây, hiển thị theo định dạng theo quy định chung của ứng dụng

- Từ ngày<=Ngày hiện tại
- Mặc định=Ngày hiện tại -30 ngày7Ngày đăng ký – ĐếnDatepicker
Chọn thông tin tìm kiếm theo ngày tạo đăng ký – Đến ngày, chỉ chọn đến ngày-- không chọn đến giờ-phút-giây, hiển thị theo định dạng theo quy định chung của ứng dụng

- Từ ngày=<Đến ngày<=Ngày hiện tại
- Đến ngày mặc định =Ngày hiện tại 
- Bắt buộc phải nhập thông tin này8Biển sốTextboxNhập biển số xe để tìm kiếm9Tìm kiếmButtonClick vào button sẽ hiển thị danh sách đăng ký thẻ tháng thỏa mãn điều kiện tìm kiếm10Xóa bộ lọcButtonClick vào button này sẽ xóa toàn bộ dữ liệu tìm kiếm, thiết lập về dữ liệu mặc định11Thêm mớiButtonClick vào nút này sẽ mở màn hình thêm mới 12Hiển thị số dòngCombobox
Hiển thị cho phép chọn tổng số dòng hiển thị/trang, bao gồm các giá trị

- 10 (mặc định)
- 20
- 5013CheckboxCheckbox
Cho phép tích chọn các đăng ký tương ứng để thực hiện thao tác. Có thể chọn nhiều đăng ký cùng lúc.

Nếu tích chọn checkbox ở tiêu đề sẽ chọn tất cả các đăng ký trong trang hiện tại
14STTLabelHiển thị số thứ tự của đăng ký, đăng ký sẽ sắp xếp theo ngày đăng ký theo thứ tự giảm dần15Căn hộLabelHiển thị số căn hộ đăng ký thẻ tháng17TòaLabelHiển thị tòa nhà có căn hộ đăng ký18Loại xeLabelHiển thị loại xe đăng ký vé tháng19Biển sốLabelHiển thị biển số của xe đăng ký vé tháng20Ngày đăng kýLabel
Là ngày mà đăng ký được tạo

Định dạng: dd/mm/yyyy
21Người tạoLabelHiển thị người tạo đăng ký22Trạng tháiLabelHiển thị trạng thái của đăng ký23Chi tiết ButtonClick vào button xem sẽ mở màn hình xem chi tiết của đăng ký tương ứng24Từ số thứ tự đến thứ tự trong tổng số đăng kýLabelHiển thị số thứ tự bắt đầu và kết thúc trên trang đang xem của tổng số bản ghi thỏa mãn yêu cầu tìm kiếm25Đang chọn LabelHiển thị số đăng ký đang được chọn26Phân trangPaginationPhân trang danh sách tìm kiếm27DuyệtButton
Click vào button này sẽ thực hiện duyệt đăng ký đã chọn

Button chỉ hiển thị đối với những tài khoản của BQL chung cư được phân quyền phê duyệt đăng ký
27Từ chốiButton
Click vào button này sẽ hiển thị màn hình nhập lý do từ chối

Button chỉ hiển thị đối với những tài khoản của BQL chung cư được phân quyền phê duyệt đăng ký
27Phản hồiButton
Click vào button này sẽ hiển thị màn hình nhập nội dung phản hồi

Button chỉ hiển thị đối với những tài khoản của BQL chung cư được phân quyền phê duyệt đăng ký

**5.1.4. Business rule**
RuleChi tiết ruleTìm kiếm
Tìm kiếm theo điều kiện AND (thỏa mãn tất cả các đầu vào tìm kiếm với các đầu vào có nhập thông tin) các thông tin nhập vào 

- Trường thông tin nào chọn Tất cả hoặc không nhập dữ liệu thì không cần tìm kiếm theo tiêu chí đó
- Các thông tin tìm kiếm chính xác:
- Tòa
- Căn hộ
- Trạng thái
- Loại xe
- Biển số xe
- Các thông tin tìm kiếm tương đối, không phân biệt hoa thườngTên chủ xe
- Ngày đăng ký: Tìm kiếm trong khoảng
- Đến ngày 23:59:59>=Ngày tạo đăng ký >=từ ngày 00:00:00Sắp xếpCho phép sắp xếp theo ngày đăng ký giảm dầnMàn hình mặc địnhHiển thị danh sách tìm kiếm khi load trang theo thông tin mặc định đã mô tả ở phần Mô tả màn hình
 

- **Đăng ký vé tháng (do Lễ tân thực hiện)****Mô tả chung****Tên Usecase**Đăng ký vé thángActorLễ tânMục đíchCho phép lễ tân tạo đăng ký vé thángPreconditionNgười dùng đăng nhập vào hệ thống và được phân quyền quản lý đơn thẻ thángMain flow
1.Chọn Thêm mới đăng ký

2. Hệ thống hiển thị màn hình thêm mới đăng ký vé tháng 

3.Nhập thông tin đăng ký và chọn đăng ký

4. Hệ thống lưu thông tin đăng ký ở trạng thái chờ duyệt và thông báo đăng ký thành công
Post ConditionĐăng ký vé gửi xe tháng thành công
- **Màn hình**
****

****

- **Mô tả màn hình****STT****Tên control****Loại control****Required****Mô tả & ghi chú**1TòaComboboxYes
Lựa chọn tòa nhà để tìm kiếm. Hiển thị danh sách tòa nhà có trên hệ thống

Hiển thị thứ tự theo alpha B
2CănComboboxYes
Hiển thị danh sách căn hộ thuộc tòa đang chọn và đang hoạt động trên hệ thống

Hiển thị thứ tự theo alpha B
3Họ tên chủ xeTextboxYes
- Họ tên chủ xe 
- Chiều dài từ 2 – 100 ký tự
Chỉ được phép nhập các ký tự aA-zZ và dấu blank 
4CMND/CCCDTextboxYes
- Số CMND/CCCD của chủ xe
- Chiều dài từ 9-12 ký tự
- Chỉ được phép nhập ký tự số 0-9, không bao gồm dấu blank5Loại xeRadioBoxYes
Danh sách các loại xe, lựa chọn loại xe muốn đăng ký vé tháng. Các loại xe gồm:

- Ô tô
- Xe máy
- Xe máy điện
- Xe đạp
- Xe đạp điện6Biển số TextboxYes (Không yêu cầu đối với xe đạp và xe đạp điện)
Biển số xe đăng ký. 

- Chỉ chứa ký tự 0-9, aA-zZ, dấu "." và “-”
- Maxlength: 10 ký tự, minlength: 8 ký tự (ko tính dấu)
- Bắt buộc phải có dấu “-”
- Bắt buộc phải có dấu “.” khi có từ 9 ký tự trở lên

Không yêu cầu nhập đối với xe đạp và xe đạp điện
7Nhãn hiệuTextboxYes
Nhãn hiệu xe, kiểu xe

- Chứa ký tự 0-9, aA-zZ, dấu "," và “-”

- Chiều dài từ 2 – 100 ký tự, tính cả dầu blank
8Màu sơnTextboxYes
- Màu sơn của xe 
- Chiều dài từ 2 – 100 ký tự
Chỉ được phép nhập các ký tự aA-zZ và dấu blank
9Ảnh CMND/CCCDButtonYes
- Click vào button sẽ hiển thị màn hình chọn file từ thiết bị.
- Định dạng: PNG, JPG, PDF
- Kích thước tối đa: 2MB
- Số lượng file tối đa: 2 file10Ảnh giấy phép đăng ký xeButtonYes (Không yêu cầu đối với xe đạp và xe đạp điện)
- Click vào button sẽ hiển thị màn hình chọn file từ thiết bị.
- Định dạng: PNG, JPG, PDF
- Kích thước tối đa: 2MB
Số lượng file tối đa: 1 file
11Ảnh phương tiệnButtonNo
- Click vào button sẽ hiển thị màn hình chọn file từ thiết bị.
- Định dạng: PNG, JPG, PDF
- Kích thước tối đa: 2MB
Số lượng file tối đa: 1 file
12Đăng kýButton Click và button sẽ thực hiện lưu thông tin đăng ký ở trạng thái chờ duyệt13HủyButton Click và button hủy việc đăng ký và đóng màn hình thêm mới
- **Business rule****Rule****Thông báo nếu không thỏa mãn rule**
Căn hộ đăng ký đang hoạt động trên hệ thống 

 
Có lỗi xảy ra, vui lòng thực hiện lại
Căn hộ đăng ký phải còn lượt đăng ký vé tháng theo quy định. 

- Ô tô: 2 vé
- Xe máy/xe máy điện/xe đạp điện/ xe đạp: 4 véĐã hết lượt đăng ký vé thángNhà xe chưa đạt số lượng tối đa cho phép gửi xe vé thángNhà xe đã đầy, không thể gửi thêm xeBiển số xe đăng ký chưa có đăng ký vé tháng ở trạng thái chờ duyệt/phản hồiBiển số xe đã đăng ký vé thángBiển số xe đăng ký chưa gán với vé tháng nào ở trạng thái đã đăng ký/hết hạnBiển số xe đã có vé tháng
Lưu thông tin đăng ký:

- Trạng thái đăng ký = Chờ duyệt
- Thời gian đăng ký = Thời gian hiện tại  Thông báo lúc đăng ký thành công: “Đăng ký thành công”