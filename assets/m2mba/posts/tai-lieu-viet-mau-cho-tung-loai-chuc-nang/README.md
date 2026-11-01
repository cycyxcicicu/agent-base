---
id: 179
title: "Tài liệu viết mẫu cho từng loại chức năng"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-06-29T13:27:31.000Z"
source_url: "https://m2mba.com/blog/articles/tai-lieu-viet-mau-cho-tung-loai-chuc-nang"
---

# Tài liệu viết mẫu cho từng loại chức năng

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-06-29T13:27:31.000Z*

## **Dnh sách các loại chức năng**
**Nhóm chức năng****Loại chức năng****Các lưu ý cho loai chức năng này**Chức năng actor là end UserChức năng dạng tìm kiếm/Danh sách
**1**.**Lựa chọn các tiêu chí tìm kiếm**: Cần xem người dùng **thường có các thông tin gì** để tìm kiếm, và ngữ cảnh tìm kiếm để lựa chọn thông tin tìm kiếm phù hợp, tránh đưa ra nhiều đầu vào tìm kiếm quá

2.**Business Rule**: Cần đưa ra được tìm kiếm thỏa mãn tất cả các điều kiện hay chỉ 1 trong các điều kiện nhập vào, Tìm kiếm chính xác (=), hay tìm kiếm tương đối (like ‘%xysdfsdf% (hay tìm kiếm bắt đầu bằng chuỗi ký tự nhập vào: sdfsfd%) , thứ tự sắp xếp đầu ra tìm kiếm, Dữ liệu tìm kiếm ở màn hình mặc định

 
Chức năng actor là end User**Chức năng enduser dạng đơn giản**
Với chức năng này thì actor chỉ cần nhập các thông tin trên form xong và submit lên, server sẽ validate, nếu okie sẽ lưu thông tin, ngược lại sẽ không lưu

Với luồng này thì activity diagram luôn gồm các bước cơ bản ở client và server nên sẽ không cần vẽ luồng, thay vào đó chỉ cần mô tả business Rule

Trong business rule sẽ đưa ra các thông tin cần validate ở server, và các công thức tính toán liên quan nếu có (nếu có công thức, bạn cần lưu ý cách để lấy ra được các đầu vào tính toán cho công thức đó)
 **Chức năng dạng end user đầy đủ**
Với chức năng có luồng giao tiếp giữa client và server gồm nhiều step hoặc trên server xử lý nhiều bước thì khi đó các bạn nên vẽ activity diagram và sau đó mô tả các bước (bước nào chưa rõ nghĩa), Lưu ý các bước check trên server theo nguyên tắc server nhận thông tin nào mà nó có thì check lại thông tin đó đảm bảo dữ liệu hiện tại trên server phải thỏa mãn với yêu cầu xử lý hiện tại

Nếu luồng xử lý có liên quan tới công thức tính toán thì cần mô tả rõ cách lấy dữ liệu đầu vào cho công thức tính đó
 **Chức năng dạng nhóm danh mục đầu vào**
Với các chức năng CRUD, tìm kiếm/danh sách của Danh mục đầu vào thì các bạn không cần phải viết tách biệt từng chức năng, vì các rule ở các chức năng này thường không có gì đặc biệt và lặp nhau như chức năng Tạo mới và chỉnh sửa

Do đó ở chức năng này các bạn có thể làm gộp cụm 5 chức năng này vào 1 Mục trong tài liệu 

- **Màn hình: Mô tả màn hình Danh sách/tìm kiếm, mô tả màn hình Thêm mới. Màn hình chỉnh sửa và Xem chi tiết không cần mô tả, vì thông tin nó giống như màn hình thêm mới, chỉ có cách hiển thị khác nhau (ví dụ Xem chi tiết chỉ hiển thị dạng read only, chỉnh sửa thì hiển thị giá trị hiện tại của thông tin đang cần chỉnh sửa)**
- **Mô tả Business Rule: Mô tả rule của chức năng Tìm kiếm/Danh sách (Tham khảo loại Chức năng dạng tìm kiếm/Danh sách ở trên), Thêm mới/Chỉnh sửa** **Chức năng dạng import**
**Màn hình: **

- Cần lưu ý có phần tải file mẫu về (để actor nắm được file cần tải lên template như thế nào)
- Cần quy định rõ định dạng file
- Cần quy định kích thước file/số dòng trên file 
**Business rule và quy định về file import**

- Mô tả các trường: Require, maxlength, định dạng, Tập giá trị cho phép…Nếu bạn đã có chức năng thêm mới đơn lẻ thì có thể link sang mô tả các trường tương ứng bên chức năng đơn lẻ
- **Quy định file trả kết quả: Quy định tên file trả ra, File trả ra thường thêm cột kết quả, và mô tả so với file import lên. Chi tiết mô tả thì ghi rõ các TH và mô tả lỗi muốn thông báo** **Chức năng báo cáo, xuất excel**
**Màn hình: **

- **Xác định đầu vào báo cáo: Cần hỏi rõ stakeholder để nắm họ thường báo cáo theo đầu vào nào, và đầu ra họ muốn ntn. **
**Business Rule**

- Cần nói rõ cách tính giá trị trên báo cáo,lấy dữ liệu điều kiện như thế nào, công thức tính giá trị trên báo cáo ra sao (cộng /trừ/chia/nhân hay 1 công thức nào đó theo nghiệp vụ quy định)
- Xuất file excel: Cần có template mẫu để xuất excel, để đội code sử dụng file đó. File xuất ra thường sẽ hiển thị các trường y nguyên như trên giao diện đang nhìn thấy
 
 **Chức năng dạng tích hợp API với bên khác**
Với chức năng dạng này, các bạn nên vẽ sequence để hiểu rõ luồng tích hợp 2 bên như thế nào, mapping API giao tiếp 2 bên theo đặc tả đã /sẽ có

Nếu trong 1 UC mà có nhiều luồng tương tác với đối tác thì các bạn có thể tách nhỏ ra các UC con để luồng đỡ phức tạp

Khi mô tả luồng activity diagram, các bạn cần lưu ý

- Trước khi gửi yêu cầu sang đối tác, các bạn cần cần nắm được thông tin gửi sang đối tác theo đặc tả sẽ được lấy ở trường nào – Thực thể nào trên hệ thống mình (Có thể mô tả hoặc không cần, nhưng phải hiểu được vì khi giao tiếp giữa 2 bên sẽ cần có thông tin mapping dữ liệu hệ thống A sang hệ thống B trước khi gửi sang)
- Cần mô tả tham số gửi sang đối tác (theo đặc tả đối tác) tương ứng với dữ liệu nào bên mình
- **Với các kết quả trả về: Các bạn cần mapping lại kết quả với bên mình (ntn là thành công, ntn là thất bại, ntn là timeout)****Chức năng dạng API****API do mình tự đưa ra đặc tả**
Cần mô tả các phần

- Luồng xử lý: Khi mình tiếp nhận yêu cầu xử lý qua API này thì hệ thống mình sẽ cần làm gì, các bạn cần vẽ rõ ra
- **Thông tin đầu vào**: Các bạn BA sẽ cần đưa ra các tham số theo yêu cầu nghiệp vụ với chức năng tương ứng đó(Ví dụ khi đặt bàn thì cần gì, lấy bàn trống thì cần gửi gì sang để hệ thống mình có đủ thông tin xử lý), ở đây các bạn lưu ý các tham số nhưMã của đối tác, bên gọi sang mình (để hệ thống biết yêu cầu đang được ai gửi qua, mã này thường do mình cấp cho các bên)
- Mã định dạnh địa điểm gọi sang mình (Ví dụ pasgo có web/app thì có thể gửi ID tương ứng với kênh thực hiện)
- Mã yêu cầu (với yêu cầu nào cần insert/update db thì sẽ cần có mã này
- **Thông tin đầu ra**: Mô tả các tham số bên mình cần trả ra cho đối tác khi xử lý xong yêu cầu nàyMã xử lý bên mình
- Mã đối tác
- Mã định danh địa điểm thực hiện
- Mã lỗi (kết quả thực hiện)
- Mô tả lỗi
- Danh sách mã lỗi: Liệt kê các lỗi có thể có khi xử lý API tương ứng và liệt kê mô tả lỗi tương ứng để đội code biết xử lý với các tình huống đó**Chức năng dạng API****API do bên khác đưa ra đặc tả**
Tương tự với chức năng API do mình đưa ra đặc tả, tuy nhiên phần thông tin đầu vào, đầu ra, danh mục mã lỗi do bên đối tác định nghĩa trước rồi

Với danh sách lỗi thì mình sẽ cần ghi rõ cho đội code biết với từng trường hợp sẽ trả về mã lỗi nào theo yêu cầu của đối tác
Chức năng dạng tiến trìnhTiến trình xử lý đơn giản
**Biểu đồ trạng thái**: Các bạn nên vẽ biểu đồ trạng thái nếu tiến trình của bạn sẽ đi qua tối thiểu 3 trạng thái, ví dụ quét các yêu cầu trạng thái A, xử lý TH 1 thì về trạng thái B, TH2 thì về trạng thái C, khi đó các bạn nên vẽ state diagram

**Luồng xử lý:** Chỉ cần mô tả step bằng word vì nó khá đơn giản

**Biểu đồ luồng dữ liệu**: Các bạn có thể mô tả dữ liệu lấy ở đâu và sau khi xử lý xong thì lưu vào đâu
Chức năng dạng tiến trìnhTiến trình xử lý phức tạp
**Biểu đồ trạng thái**: Các bạn nên vẽ biểu đồ trạng thái nếu tiến trình của bạn sẽ đi qua tối thiểu 3 trạng thái, ví dụ quét các yêu cầu trạng thái A, xử lý TH 1 thì về trạng thái B, TH2 thì về trạng thái C, khi đó các bạn nên vẽ state diagram

**Luồng xử lý:** Vẽ lưu đồ và mô tả như luồng thông thường

**Biểu đồ luồng dữ liệu**: Các bạn có thể mô tả dữ liệu lấy ở đâu và sau khi xử lý xong thì lưu vào đâu

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

## **Chức năng actor là end user**

## Chức năng dạng Tìm kiếm/Danh sách (Mobile app – Danh sách bàn theo trạng thái)

### 1.1.1.Mô tả chung
**Tên Usecase**Danh sách bàn theo trạng tháiActorNV PV, NV lễ tânMục đíchCho phép NV PV theo dõi trang thái hiện tại của các bàn trong nhà hàngPreconditionNV PV đã đăng nhập hệ thống và có quyền thực hiệnMain flow
1.Chọn menu Home

2.Hệ thống hiển thị màn hình danh sách bàn mặc định

3.Nhập thông tin tìm kiếm

4.Hệ thống hiển thị kết quả tìm kiếm theo yêu cầu của Actor
Post ConditionHiển thị danh sách bàn theo trạng thái mặc định sau khi đăng nhập vào và hiển thị danh sách bàn theo kết quả tìm kiếm của người dùng
### 1.1.2.Màn hình

### 1.1.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Search BoxTextboxNhập mã/tên phòng để tìm kiếm2FilterIconClick vào sẽ mở ra màn hình nhập thông tin tìm kiếm nâng cao (control từ 10-14)3Khu vựcListHiển thị danh sách khu vực của nhà hàng4Thông tin phòngLabelHiển thị thông tin phòng theo định dạng: <tên phòng> - <Loại phòng>-<Đặc điểm của phòng>(Số bàn trong phòng)5Tên bànLabel
Hiển thị tên bàn tương ứng với định dạng

- Bàn trống: <Tên bàn>
- Bàn đã đặt: <Tên bàn> (Số bàn đặt cùng bàn này)6Thời gian Label
Hiển thị theo định dạng hh24:mi

- Nếu bàn đang phục vụ: hiển thị giờ dự kiến kết thúc=Giờ tới + thời gian phục vụ trung bình/bàn
- Nếu bàn chưa tới: Hiển thị giờ dự kiến tới7Mã đặt bànLabelHiển thị 3 ký tự cuối của mã đặt bàn (mã đặt bàn sẽ đặt theo dạng Mã nhà hàng_yymmdd_số tự tăng (từ 001) 8Tổng tiềnLabelHiển thị tổng tiền tạm tính của bàn9Số lượng chỗ ngồiLabelHiển thị chỗ ngồi có thể ngồi đối với bàn trống10Đang trốngLabelThể hiện bàn đang trống11,12Left, rightIconChỉ hiển thị khi số lượng hiển thị trên màn hình không đủ, user có thể trượt trái, phải để xem thông tin các bàn khác13Khu vựcList
Hiển thị danh sách khu vực của nhà hàng

Mặc định là giá trị mà NV PV đã chọn ở lần trước đó
nếu chưa chọn lần nào thì mặc định là Tất cả
14Loại phòngList
Hiển thị danh sách loại phòng trong nhà hàng

Mặc định là giá trị mà NV PV đã chọn ở lần trước đó
nếu chưa chọn lần nào thì mặc định là Tất cả
15Yêu cầuList
Hiển thị danh sách yêu cầu trong nhà hàng

Mặc định là giá trị mà NV PV đã chọn ở lần trước đó
nếu chưa chọn lần nào thì mặc định là chọn Tất cả các yêu cầu
17Trạng tháiList
Hiển thị các trạng thái: Tất cả, Đang trống, Đang phục vụ, Chờ thanh toán

Mặc định là giá trị mà NV PV đã chọn ở lần trước đó
nếu chưa chọn lần nào thì mặc định là chọn Tất cả 
18Thời gianDatetime Picker
Mặc định là thời gian mà NV Phục vụ đã chọn lần trước đó 

Nếu chưa chọn thì mặc định chọn

- Từ ngày=Thời gian hiện tại
- Đền ngày=thời gian hiện tại + thời gian phục vụ trung bình/bàn
### 1.1.4.Business Rule
RuleChi tiết ruleTìm kiếm
Tìm kiếm theo điều kiện AND các thông tin nhập vào

- Trường thông tin nào chọn Tất cả thì không cần tìm kiếm theo tiêu chí đó
- Tìm kiếm kết hợp cả thông tin nhập trên ô searchbox: Tìm kiếm các bàn trên hệ thống có mã bàn/Tên bàn có chứa thông tin nhập vào ô searchbox (LIKE), không phân biệt hoa thường. Nếu không nhập thì bỏ qua tiêu chí này
- Tìm kiếm theo trạng tháiBàn chưa tới: Lấy danh sách bàn có thời gian dự kiến tới >=Từ ngày và <= đến ngày và có trạng thái Đặt chỗ thành công
- Bàn đang phục vụ/ Bàn chờ thanh toán/Chờ phục vụ: Lấy danh sách bàn có trạng thái dang phục vụ, không quan tâm thời gian
- Bàn trống: Lấy danh sách bàn mà chưa được ai đặt bàn trong khoảng từ ngày- đến ngày: tức thời gian dự kiến tới không nằm trong khoảng từ ngày – Đến ngàySắp xếpCho phép sắp xếp theo tên khu vực tăng dần theo alpha BMàn hình mặc định
Mặc định lấy theo tiêu chí tìm kiếm sau

- Khu vực: Tất cả
- Trạng thái: Tất cả
- Thời gianTừ ngày=Thời gian hiện tại
- Đền ngày=thời gian hiện tại + thời gian phục vụ trung bình/bàn
- Yêu cầu: Tất cảMàu sắc hiển thịTheo quy định chung về màu sắc từng bàn trong quy định xử lý giao diện chung (tạm thời C Ánh chưa xong phần này)
## Chức năng dạng Tìm kiếm/Danh sách (Web admin - Danh sách nhà hàng)

### 1.2.1.Mô tả chung
**Tên Usecase**Danh sách nhà hàngỨng dụngWeb adminActorNV Sale Mục đíchCho phép NV Sale xem danh sách các nhà hàng đã/đang sử dụng phần mềm FoodNowPreconditionNV sale đã đăng nhập hệ thống và có quyền thực hiệnMain flow
1.Chọn menu Quản lý nhà hàng

2.Hệ thống hiển thị màn hình danh sách nhà hàng theo màn hình tìm kiếm mặc định

3.Nhập thông tin tìm kiếm

3.Hệ thống hiển thị kết quả tìm kiếm theo yêu cầu của Actor
Post ConditionHiển thị danh sách nhà hàng theo đầu vào tìm kiếm (đầu vào mặc định hoặc do actor nhập vào)
### 1.2.2.Màn hình

 

### 1.2.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Mã nhà hàngTextboxNhập mã nhà hàng để tìm kiếm2Tên nhà hàngTextboxNhập tên nhà hàng để tìm kiếm3Số điện thoại liên hệTextboxNhập SĐT liên hệ của nhà hàng để tìm kiếm4EmailTextboxNhập Email liên hệ của nhà hàng để tìm kiếm5Ngày tạo – Từ ngàyDatepicker
Chọn thông tin tìm kiếm theo ngày tạo – Từ ngày nhà hàng, chỉ chọn đến ngày- không chọn đến giờ-phút-giây, hiển thị theo định dạng theo quy định chung của ứng dụng

- Từ ngày<=Ngày hiện tại
- Mặc định=Ngày hiện tại -30 ngày6Ngày tạo – Đến ngàyLabel
Chọn thông tin tìm kiếm theo ngày tạo – Đến ngày nhà hàng, chỉ chọn đến ngày-- không chọn đến giờ-phút-giây, hiển thị theo định dạng theo quy định chung của ứng dụng

- Từ ngày=<Đến ngày<=Ngày hiện tại
- Đến ngày mặc định =Ngày hiện tại 
- Bắt buộc phải nhập thông tin này7Ngày kết thúc – Từ ngàyDatepicker
Chọn thông tin tìm kiếm theo ngày kết thúc – Từ ngày nhà hàng, chỉ chọn đến ngày- không chọn đến giờ-phút-giây, hiển thị theo định dạng theo quy định chung của ứng dụng

- Từ ngày<=Ngày hiện tại
- Bắt buộc phải nhập thông tin này
 
8Ngày kết thúc – Đến ngàyLabel
Chọn thông tin tìm kiếm theo ngày kết thúc – Đến ngày nhà hàng, chỉ chọn đến ngày-- không chọn đến giờ-phút-giây, hiển thị theo định dạng theo quy định chung của ứng dụng

- Từ ngày=<Đến ngày<=Ngày hiện tại9Trạng tháiCombobox
Hiển thị danh sách trạng thái để tìm kiếm, bao gồm các trạng thái

- Tất cả
- Hoạt động (Mặc định)
- Khóa
- Dừng hoạt động10Tìm kiếmButtonClick vào button sẽ hiển thị danh sách nhà hàng thỏa mãn điều kiện tìm kiếm11ResetButtonClick vào button này sẽ xóa toàn bộ dữ liệu tìm kiếm, thiết lập về dữ liệu mặc định12Thêm mớiButtonClick vào nút này sẽ mở màn hình thêm mới (tham khảo chức năng thêm mới tại đây)—đính kèm link tới chức năng đó nếu có13Import danh sáchButtonClick vào nút này sẽ mở màn hình Import danh sách nhà hàng (tham khảo chức năng thêm mới tại đây)—đính kèm link tới chức năng đó nếu có14Số điện thoại-EmailLabelHiển thị số điện thoại và email liên hệ của nhà hàng theo dạng :<Sdt>-Email, nếu ko có email thì chỉ hiển thị số điện thoại15Ngày bắt đầuLabelLà ngày bắt đầu sử dụng phần mềm foodNow17Ngày kết thúcLabel
Là ngày kết thúc sử dụng phần mềm foodNow

- Nếu nhà hàng dừng hoạt động: Hiển thị ngày kết thúc hợp đồng
- Nếu nhà hàng vẫn đang hoạt động/Khóa: Hiển thị ngày kết thúc của kỳ hiện tại (Nhà hàng sẽ mua các gói dịch vụ theo kỳ 1-3-6-12 tháng) 18Trạng tháiLabelHiển thị trạng thái hiện tại của nhà hàng19Xem chi tiết IconClick vào icon này sẽ mở màn hình xem chi tiết của nhà hàng tương ứng20Chỉnh sửaIconClick vào icon này sẽ mở màn hình chỉnh sửa thông tin nhà hàng21Khóa nhà hàngIconClick vào icon này sẽ hiển thị popup xác nhận khóa nhà hàng22Tổng số bản ghiLabelHiển thị tổng số bản ghi thỏa mãn yêu cầu tìm kiếm23Tổng số bản ghi / trangCombobox
Hiển thị cho phép chọn tổng số bản ghi hiển thị/trang, bao gồm các giá trị

- 10 (mặc định)
- 20
- 5024Phân trangPaginationPhân trang danh sách tìm kiếm
### 1.2.4.Business Rule
RuleChi tiết ruleTìm kiếm
Tìm kiếm theo điều kiện AND (thỏa mãn tất cả các đầu vào tìm kiếm với các đầu vào có nhập thông tin) các thông tin nhập vào 

- Trường thông tin nào chọn Tất cả hoặc không nhập dữ liệu thì không cần tìm kiếm theo tiêu chí đó
- Các thông tin tìm kiếm chính xác:Trạng thái
- Số điện thoại liên hệ 
- Các thông tin tìm kiếm tương đốiMã nhà hàng
- Tên nhà hàng
- Email liên hệ của nhà hàng
- Ngày tạo, ngày kết thúc: Tìm kiếm trong khoảngĐến ngày 23:59:59>=Ngày tạo nhà hàng >=từ ngày 00:00:00
- Đến ngày 23:59:59>=Ngày kết thúc nhà hàng >=từ ngày 00:00:00: Trong đó nếu trạng thái nhà hàng Hoạt động/Khóa thì ngày kết thúc là ngày kết thúc của kỳ hiện tại
- Dừng hoạt động thì ngày kết thúc là ngày kết thúc của hợp đồngSắp xếpCho phép sắp xếp theo ngày tạo giảm dần, ngày kết thúc giảm dầnMàn hình mặc địnhHiển thị danh sách tìm kiếm khi load trang theo thông tin mặc định đã mô tả ở phần Mô tả màn hình
## Chức năng end user dạng đơn giản (Mobile app PV-Đặt bàn)

### 1.3.1.Mô tả chung
**Tên Usecase**Đặt bàn ActorNV PV Mục đíchCho phép NV PV Đặt bàn cho KH khi KH tới nhà hàng ăn mà chưa book trước đóPreconditionNV VH đã đăng nhập hệ thống và có quyền thực hiệnMain Flow
1.NVPV chọn bàn đạng ở trạng thái trống

2.Hệ thống hiển thị màn hình đặt bàn kèm thông tin bàn vừa chọn

3.NVPV nhập thông tin đặt bàn

4.NVPV chọn Xác nhận

5.hệ thống lưu thông tin đặt bàn ở trạng thái chờ phục vụ
Post ConditionHệ thống lưu thông tin đặt bàn ở trạng thái chờ phục vụ
### 1.3.2.Màn hình

### 1.3.3.Mô tả màn hình
STTTên controlLoại controlRequireMô tả1,2Bàn  
Tích chọn vào 1 bàn đang trống sẽ hiển thị ra màn hình đặt bàn (từ control số 3)

Nếu chọn bàn chưa tới nhưng có thời gian dự kiến tới<thời gian hiện tại thì hiển thị cảnh báo bằng popup **, và không cho chọn**

Hoặc Thời gian hiện tại<thời gian dự kiến tới <=thời gian hiện tại + thời gian phục vu trung bình/bàn – (X ph)  (X được cấu hình theo từng nhà hàng)

 

 

 
3Tổng số bànLabel 
Tổng số bàn đã chọn

Nếu loại bỏ đi 1 bàn thì tự động giảm

Nếu chọn thêm 1 bàn thì tự động tăng
3Tổng số ngườiLabel Tổng số người có thể ngồi ở các bàn đã chọn= Tổng số người có thể ngồi trên từng bàn (tự động tăng giảm theo số bàn đã chọn)4Họ tên TextboxYes
Nhập thông tin tên người đặt bàn

Chỉ được nhập ký tự aA-zZ và ký tự trắng

Chiều dài tối đa là 50 ký tự
6TổngTextboxYes
Tổng số người đến ăn, nhập ký tự số

Tối đa 4 ký tự số
7Xác nhậnButton Click vào button sẽ thực hiện lưu thông tin đặt bàn8Thu nhỏIcon Thu nhỏ màn hình đặt bàn9ĐóngIcon Đóng màn hình đặt bàn và coi như bỏ chọn các bàn đã chọn
### 1.3.4.Business Rule **(Những rule trên server thực hiện: 1.Check những gì, 2.Nếu hợp lệ thì Server lưu thông tin ntn, bỏ qua các rule validate format, maxlength, require**

### **3.Lỗi thông báo khi không thỏa mãn rule)**
RuleThông báo nếu không thỏa mãn rule
Bàn phải đang ở trạng thái trống, thỏa mãn điều kiện cụ thể như sau: 

- Bàn thời gian dự kiến tới >= thời gian hiện tại + thời gian phục vụ trung bình/bàn – X(ph) (X được cấu hình theo từng nhà hàng trong chức năng cấu hình tham số nhà hàng)
 

- Bàn có thời gian dự kiến tới <thời gia hiện tại: Bàn đã có người đặt, chưa quá hạn vẫn chưa tới. Vui lòng liên hệ KH để hủy bàn 
- Các TH còn lại: Bàn đã có người đặt, xin vui lòng kiểm tra lạiUser phải có quyền thực hiện và đang ở trạng thái hoạt độngBạn không có quyền thực hiện hành động nàyMã bàn phải đang hoạt động trên hệ thống và thuộc nhà hàng của user đang thực hiện<Liệt kê danh sách tên bàn, cách nhau dấu , nếu nhiều bàn> đang được sử dụng nên không thể xác nhận. Vui lòng kiểm tra lạiNhà hàng phải đang ở trạng thái hoạt độngNhà hàng đang không hoạt động
Lưu thông tin đặt bàn:

- Trạng thái đặt bàn =   Chờ phục vụ
- Thời gian đặt bàn=Thời gian hiện tại
- Thời gian dự kiến kết thúc = Thời gian hiện tại + thời gian phục vụ trung bình/bàn
- … Thông báo lúc Đặt bàn thành công: “Đặt bàn thành công….‘ 
## Chức năng end user dạng đầy đủ (Tạo Momo QR)

### 1.4.1.Mô tả chung
Tên UsecaseTạo QR MomoActorNV PVMục đíchCho phép NVPV chọn hình thức thanh toán là QR Momo PreconditionActor đã đăng nhập vào hệ thống và đã xác nhận đồng ý thanh toán của mã đặt bàn tương ứngMain Flow
1.Chọn Momo QR trong màn hình Thanh toán (sau khi NVPV đã xác nhận yêu cầu thanh toán, tham khảo tại [Mục 3.9.Yêu cầu thanh toán](https://docs.google.com/document/d/15aHigzA6UvCvwHoPnQU5Lpa_nI6_BbSb/edit#heading=h.17dp8vu))

2.Hệ thống hiển thị QR Momo
Post ConditionHệ thống hiển thị màn hình QR Momo với các tham số liên quan tới đơn hàng
### 1.4.2.Màn hình

### 1.4.3.Mô tả màn hình
STTTên controlLoại controlMô tả1Thông tin bànLabelHiển thị mã đặt bàn và tên người nhận bàn2Trạng thái đặt bànLabelTrạng thái Chờ thanh toán3Tổng tiền (chưa VAT)LabelTổng tiền chưa tính VAT4Tổng tiền VATLabelTổng tiền đã tính VAT5Tính VATSlide
Tính hay không tính VAT, với nhà hàng có tham số config cho phép KH lấy VAT hay không thì slide này sẽ được trượt sang trái/phải

Ngược lại sẽ hiển thị mặc định là Lấy VAT và không cho sửa
6Thông tin cổng thanh toán Ảnh đại diện và tên cổng thanh toán tương ứng7Danh sách ngân hàngicon
Với bên cổng thanh toán mà có kết nối nhiều bank, click vào icon này sẽ biết được các ngân hàng hỗ trợ trên cổng thanh toán này, để NV PV dễ dàng tư vấn KH

8Tiếp tụcButtonClick vào button này sẽ chuyển sang màn hình tiếp theo9Số tiền thanh toánLabelSố tiền thanh toán của đơn hàng, phụ thuộc vào thông tin ở màn hình trước NVPV đã chọn (số tiền chưa VAT hoặc đã có VAT)10Mã đơn hàngLabelLà mã đơn hàng do hệ thống foodNow sinh ra để gửi sang bên Momo11QRcodeImageẢnh QR theo quy định của Momo
### 1.4.4.Activity diagram và mô tả luồng

- **Mô tả luồng**
 
**Bước****Mô tả**3
Kiểm tra thông tin hợp lệ, thỏa mãn các điều kiện sau

- Mã đặt bàn phải đang ở trạng thái Chờ thanh toán
- Mã đặt bàn thuộc nhà hàng mà user đang đăng nhập
- Nhà hàng đang hoạt động
- User đang hoạt động 
-  4
Sinh mã GD 

- 1 là BA yêu cầu rule sinh mã GD: Mã GD phải theo dạng yyyymmddxxxxx 
- trong đó yyyymmdd là ngày GD hiện tại
- xxxxx: là chuỗi số được tăng dần từ 00001
-  
- BA ko yêu cầu sinh mã: Mã GD này phải là duy nhất5
Lấy các thông tin để tạo URL QR

- PartnerCode: Mã đối tác do Momo cung cấp cho nhà hàng
- storeId: Mã chi nhánh nhà hàng do Momo cung cấp
- Số tiền thanh toán=Số tiền của mã đặt bàn tương ứng (tùy thuộc vào chọn VAT hay không VAT để lấy số tiền thanh toán
- BilID=Mã GD vừa sinh6Tạo URL QR theo quy định của Momo: [https://developers.momo.vn/v2/#/docs/qr_payment?id=t%e1%ba%a1o-qr-code](https://developers.momo.vn/v2/#/docs/qr_payment?id=t%e1%ba%a1o-qr-code) 11
 
Trường hợpThông báo
Mã đặt bàn phải không ở trạng thái Chờ thanh toán

 
Trạng thái đặt bàn không hợp lệ, Vui lòng kiểm tra lạiMã đặt bàn không thuộc nhà hàng mà user đang đăng nhậpThông tin thanh toán không hợp lệUser không hoạt độngTài khoản của bạn đang không hoạt độngNhà hàng không hoạt độngNhà hàng đang không hoạt động trên hệ thống. Vui lòng liên hệ với nhân viên FoodNow để được hỗ trợ
 

## Chức năng dạng nhóm danh mục đầu vào CRUD Tìm kiếm/Danh sách (Danh mục bàn của nhà hàng)

### 1.5.1.Mô tả chung
**Tên Usecase**CRUD Tìm kiếm/Danh sách Bàn của nhà hàngActorNV PV Mục đích Precondition Post ConditionHiển thị chi tiết thông tin đặt bàn kèm với các thao tác đi kèm
### 1.5.2.Màn hình

 

### 1.5.3.Mô tả màn hình

- Control từ 1-15 (Màn hình tìm kiếm)

STTTên controlLoại controlMô tả & ghi chú1Mã bànLabelTrạng thái đặt bàn tương ứng, tham khảo quy định về màu sắc trạng thái của bàn trong quy định chung về xử lý giao diện2Tên bànTab barClick vào sẽ xem chi tiết về thông tin đặt bàn3Khu vựcTab barClick vào sẽ xem chi tiết về thông tin món ăn của bàn tương ứng4Trạng tháiLink
Hiển thị tên người đặt bàn, có link đính kèm

Nếu click vào link sẽ ra thông tin chi tiết người đặt bàn
5Tìm kiếmButton
Hiển thị số điện thoại người đặt bàn

 
6ResetButtonHiển thị họ tên người nhận bàn7Thêm mớiLabelHiển thị họ tên người nhận bàn8Danh sách bànGridTổng số người 9Trạng tháiLabelChi tiết số người lớn, trẻ em10Xem thông tinIconHiển thị thời gian đặt bàn: hiển thị theo định dạng dd/mm/yyyy hh24:mi11Chỉnh sửaIcon
Hiển thị kênh đặt bàn của bàn tương ứng

- Đặt qua điện thoại/lễ tân: Đặt trước - <username đặt bàn>
- Đặt qua đơn vị đặt chỗ khác: <Tên đơn vị đặt >
- Đến nhà hàng: Trực tiếp - <Username đặt bàn>12Tổng số bản ghiLabelHiển thị tổng số bản ghi thỏa mãn yêu cầu tìm kiếm13Tổng số bản ghi / trangCombobox
Hiển thị cho phép chọn tổng số bản ghi hiển thị/trang, bao gồm các giá trị

- 10 (mặc định)
- 20
- 5014Phân trangPaginationPhân trang danh sách tìm kiếm15PopupPopupPopup confirm active/inactive bàn
- Control còn lại
-  STTTên controlLoại controlRequireMaxlengthMô tả & ghi chú16Khu vựccomboboxYes 
- Hiển thị danh sách khu vực đang hoạt động trong nhà hàng mà user login đang chọn (1 user có thể thuộc nhiều nhà hàng, khi vào thao tác trên ứng dụng, sẽ cần chọn nhà hàng mà user sẽ thực hiện)
- Hiển thị theo order tăng dần alphaB 17PhòngcomboboxYes 
- Hiển thị danh sách phòng theo đang hoạt động theo khu vực đang chọn
- Hiển thị theo order tăng dần alphaB18Đặc điểmTextbox  
- Hiển thị thông tin đặc điểm từ thông tin phòng đã chọn
- Thông tin này chỉ đọc, không được sửa19Mã bànTextboxYes20Mã bàn của bàn tương ứng, chỉ được nhập các ký tự số, chữ và ký tự - hoặc _20Tên bànTextboxYes50Nhập tên bàn của bàn tương ứng, chỉ được nhập các ký tự số, chữ và ký tự blank21Số chỗ ngồiTextboxYes2Chỉ được nhập ký tự số22Trạng tháicomboboxYes 
Hiển thị danh sách trạng thái của bàn sau khi tạo mới, gồm các trạng thái

- Hoạt động (mặc định)
- Không hoạt động23Thêm mớiButton  Click vào button này sẽ hiển thị màn hình popup số 2724ĐóngButton  Click vào button này sẽ25Xem chi tiết bànMàn hình popup  Màn hình xem chi tiết thông tin bàn, view ở chế độ read only26Chỉnh sửa thông tin bànMàn hình popup  
Màn hình chỉnh sửa thông tin bàn, với thông tin load mặc định là thông tin hiện tại của bàn tương ứng và ở chế độ được phép sửa

Ràng buộc các trường tương tự như các control ở màn hình thêm mới
27Popup xác nhận thêm mới   Popup xác nhận thêm mới trước khi thêm mới28Popup xác nhận chỉnh sửa   Popup xác nhận chỉnh sửa trước khi chỉnh sửa
### 1.5.4.Business Rule
UCRuleThông báo nếu không thỏa mãn ruleTìm kiếm bàn
Tìm kiếm theo điều kiện AND (thỏa mãn tất cả các đầu vào tìm kiếm với các đầu vào có nhập thông tin) các thông tin nhập vào 

- Trường thông tin nào chọn Tất cả hoặc không nhập dữ liệu thì không cần tìm kiếm theo tiêu chí đó
- Các thông tin tìm kiếm chính xác:Mã bàn
- Khu vực
- Trạng thái
- Các thông tin tìm kiếm tương đốiTên bànNếu không có kết quả nào thỏa mãn thì hiển thị: “Không có kết quả nào thỏa mãn”Tìm kiếm bànKết quả đầu ra sắp xếp theo thứ tự ngày tạo giảm dần Tìm kiếm bànDữ liệu tìm kiếm mặc định: Lấy hết toán bộ các bàn trên hệ thống với trạng thái Hoạt động Thêm mới/chỉnh sửaMã bàn và tên bàn là duy nhất trong 1 nhà hàngMã bàn/Tên bàn đã tồn tại trong nhà hàng. Vui lòng kiểm tra lại Thêm mới/chỉnh sửaNhà hàng đang hoạt độngNhà hàng đang không hoạt động. Vui lòng kiểm tra lạiThêm mới/chỉnh sửaUser có quyền hoặc đang bị khóaBạn không có quyền thực hiện thao tác nàyThêm mới/chỉnh sửaPhòng phải thuộc khu vực tương ứng và khu vực thuộc nhà hàng tương ứngThông tin bàn không hợp lệ. Vui lòng kiểm tra lại
## Chức năng dạng import thông tin (Import danh sách nhà hàng)

### 1.6.1.Mô tả chung
**Tên Usecase**Import danh sách nhà hàngActorNV Sale Mục đíchCho phép NV sale import 1 loạt danh sách nhà hàng thay vì phải nhập bằng tay từng nhà hàngPrecondition
NV PV đã đăng nhập hệ thống và có quyền thực hiện

NVPV đang ở màn hình Danh sách nhà hàng
Main flow
1.Actor chọn Import danh sách nhà hàng

2.Hệ thống hiển thị màn hình import danh sách nhà hàng

3.Actor tải file mẫu về để nhập dữ liệu vào đúng file như yêu cầu và import lên hệ thống

4.Hệ thống thực hiện lưu thông tin nhà hàng

 

 
Post ConditionThực hiện lưu thông tin nhà hàng vào hệ thống
### 1.6.2.Màn hình

 

### 1.6.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Chọn fileButton
Click vào button này sẽ mở màn hình chọn file trên máy tính

 
2Đường dẫn fileTextboxHiển thị đường dẫn tới file vừa chọn, chỉ hiển thị dạng đọc, không được sửa3Download file mẫuLink button
Click vào đây sẽ tải file mẫu về , giúp cho actor có thể tạo file theo đúng yêu cầu

File mẫu chứa các thông tin này
4,5ĐóngButton/iconClick vào đây sẽ đóng màn hình lại
### 1.6.4.Các quy định về file import và file trả về &Business rule 

- **Loại file**: xlsx, kích thước tối đa 3MB, tối đa 500 dòng dữ liệu (không tính các dòng header)
- **Link file mẫu**: <Chèn link file mẫu [vào đây](https://docs.google.com/spreadsheets/d/14EV8wsxg5A48__s7c8G7Ce_34xIjUk2t/edit?rtpof=true)>
- **Quy định về các trường trong file Import ****Tên trường****Require****Maxlength****Mô tả và Ràng buộc****Business Rule**Mã nhà hàng (*)Yes10
Mã nhà hàng gồm ký tự chữ và số , và ký tự - hoặc _

Mã nhà hàng bắt buộc duy nhất, nếu 2 hàng trùng nhau thì chỉ ghi nhận 1 hàng
Mã nhà hàng là duy nhất trong nhà hàng tương ứngTên nhà hàng(*)Yes100
Tên nhà hàng gồm ký tự chữ và số , và ký tự - hoặc _, tối đa 100 ký tự

Tên nhà hàng bắt buộc duy nhất, nếu 2 hàng trùng nhau thì chỉ ghi nhận 1 hàng
Tên nhà hàng là duy nhất trong nhà hàng tương ứngSĐT liên hệ nhà hàng(*)Yes10Số điện thoại liên hệ gồm các ký tự số, gồm 10 ký tự số Email liên hệ nhà hàng 100Email thỏa mãn đúng quy định email tại quy định chung Chủ nhà hàng(*)Yes100Tên chủ nhà hàng, gồm các ký tự chữ và blank SĐT chủ nhà hàng(*)Yes10SĐT chủ nhà hàng gồm các ký tự số, gồm 10 ký tự số Email chủ nhà hàng 100Email thỏa mãn đúng quy định email tại quy định chung Địa chỉ chi tiết(*)Yes100Địa chỉ chi tiết nhà hàng Mã tỉnh(*)Yes2Mã tỉnh theo danh mục quy định trên hệ thống Mã huyện(*)Yes3Mã huyện theo danh mục quy định trên hệ thống Mã xã(*)Yes5Mã xã theo danh mục quy định trên hệ thống Mã HĐ 10Mã hợp đồng ký với nhà hàngMã HĐ phải duy nhất trên toàn hệ thốngNgày Ký HĐ  
Ngày ký hợp đồng với nhà hàng

Nhập theo định dạng : dd/mm/yyyy và phải <=ngày hiện tại
 Ngày bắt đầu   
Ngày bắt đầu nhà hàng sử dụng dịch vụ

Nhập theo định dạng : dd/mm/yyyy
 Ngày kết thúc  
Ngày kết thúc nhà hàng sử dụng dịch vụ (Của kỳ hiện tại hoặc là ngày kết thúc hợp đồng)

Nhập theo định dạng : dd/mm/yyyy
 Sale ký HĐ 20Username của NV sale ký hợp đồng Sale quản lý nhà hàng 20Username của NV sale tiếp nhận quản lý, chăm sóc nhà hàng Mã gói SP 20Mã gói của SP mà KH sử dụng, mã gói tồn tại trên hệ thống và đang hoạt độngMã gói sản phẩm phải tồn tại và đang hoạt động trên hệ thốngKỳ hạn sử dụng 2Kỳ hạn sử dụng tính theo thángGói sản phẩm có hỗ trợ kỳ hạn tương ứng
- **Business Rule**
-  
- **Quy định file trả ra****Tên file**: giống tên file đã import lên nhưng bổ sung đuôi **_result** (ví dụ tên file là Danh sách nhà hàng 012022.xlsx thì tên file trả ra là Danh sách nhà hàng 012022_result.xlsx
- Trường thông tin: Bổ sung thêm 2 trườngKết quả (thành công/Thất bại)
- Mô tả lỗi: Mô tả chi tiết lỗi của bản ghi tương ứng nếu kết quả import bị lỗiChi tiết mô tả lỗi: **Trường hợp****Mô tả lỗi**Nếu bắt buộc nhập nhưng không nhập<Liệt kê các trường, cách nhau bởi dấu ,> không được phép để trốngMã nhà hàng/Tên nhà hàng bị trùng với mã nhà hàng/tên nhà hàng đã có (Và đang hoạt động) của nhà hàng tương ứngMã nhà hàng/Tên nhà hàng đã tồn tại trên hệ thốngMã tỉnh/huyện/xã không hợp lệ (không cùng bộ hoặc không tồn tại trên hệ thống)Thông tin mã tỉnh/Huyện/Xã không hợp lệMã HĐ trùng với mã HĐ đã có trên hệ thốngMã HĐ trùng với Mã HĐ đã có trên hệ thốngMã gói sản phẩm không tồn tại hoặc không hoạt động trên hệ thốngMã gói SP không hợp lệKỳ hạn không hợp lệGói SP không hỗ trợ kỳ hạn tương ứng
## Chức năng dạng báo cáo, xuất excel (Báo cáo hệ số quay vòng bàn)

### 1.7.1.Mô tả chung
**Tên Usecase**Báo cáo hệ số quay vòng bànActorKế toán, QL nhà hàng Mục đíchCho phép actor theo dõi hệ số quay vòng nhà hàng để có thể nâng cao đươc hệ số này để tăng doanh sôPreconditionActor đã đăng nhập hệ thống và có quyền thực hiệnMain Flow
1.Actor chọn Báo cáo tổng hợp=>Báo cáo hệ số quay vòng nhà hàng

2.Hệ thống hiển thị màn hình nhập các đầu vào để lấy báo cáo

3.Actor nhập tham số đầu vào để lấy báo cáo và chọn lấy báo cáo

4.Hệ thống hiển thị báo cáo theo đầu vào Actor đã nhập (công thức lấy báo cáo xem ở mục 4.Business rule)

5.Actor chọn xuất excel

6.Hệ thống xuất excel theo dữ liệu ở bảng kết quả báo cáo 
Post ConditionHệ thống xuất dữ liệu báo cáo theo đúng điều kiện đầu vào 
 

### 1.7.2.Màn hình

### 1.7.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Nhà hàngCombobox
- Hiển thị danh sách TÊN nhà hàng mà user đang quản lý
- Nếu chỉ có 1 nhà hàng thì hiển thị mặc định nhà hàng đó
- Ngược lại sẽ hiển thị mặc định nhà hàng mà user đang lựa chọn sau khi login vào2,3Thời gian báo cáo (Từ ngày – Đến ngày)DatePicker
Đây là khoảng thời gian báo cáo

- Mặc định từ ngày=Ngày hiện tại trừ 30 ngày
- Mặc định đến ngày=Ngày hiện tại -1
- Từ ngày<=Đến ngày<=Ngày hiện tại4Khung thời gian tính hệ số quay vòng –Bắt đầuCombobox
Khung thời gian tính hệ số quay vòng, giá trị bắt đầu =thời gian bắt đầu của các buổi bán hàng, và step tăng thêm 1 cho đến giá trị kết thúc của buổi bán hàng đó

- Giá trị mặc định=Thời gian start của các buổi bán hàng của nhà hàng
- Ví dụ nhà hàng có cấu hình thời gian phục vụSáng: 06:09 thì giá trị trong khung thời gian này =06,07,08,09
- Trưa: 11:00-14:00, thì giá trị khung thời gian này =11,12,13,14
- Chiều, tối: 18:00-21h thì giá trị khung thời gian này=18,19,20,21
- Có bao nhiêu khung thời gian phục vụ của nhà hàng thì có bấy nhiều khung thời gian tính hệ số quay vòng5Khung thời gian tính hệ số quay vòng –Kết thúcCombobox
Khung thời gian tính hệ số quay vòng, giá trị bắt đầu =thời gian bắt đầu của các buổi bán hàng, và step tăng thêm 1 cho đến giá trị kết thúc của buổi bán hàng đó

- Giá trị mặc định=Thời gian kết thúc của các buổi bán hàng của nhà hàng
- Ví dụ nhà hàng có cấu hình thời gian phục vụSáng: 06:09 thì giá trị trong khung thời gian này =06,07,08,09
- Trưa: 11:00-14:00, thì giá trị khung thời gian này =11,12,13,14
- Chiều, tối: 18:00-21h thì giá trị khung thời gian này=18,19,20,21
- Có bao nhiêu khung thời gian phục vụ của nhà hàng thì có bấy nhiều khung thời gian tính hệ số quay vòng6ThêmIcon buttonClick vào icon này để tạo ra bộ nhập liệu về khung thời gian tính hệ số vòng quay7Báo cáoButton
Click vào button này sẽ hiển thị kết quả báo cáo 

Nếu không có dữ liệu báo cáo thì hiển thị: “Chưa có dữ liệu báo cáo”
8Xuất excelButtonClick vào button này sẽ xuất excel dữ liệu báo cáo đang hiển thị theo template [tại đây](https://docs.google.com/spreadsheets/d/15RhY_ZSCENO0KpCcWaoQu-e866XtnJh4?rtpof=true&authuser=anhminhbaokhanh%40gmail.com&usp=drive_fs)9Ngày báo cáoLabel
Hiển thị báo cáo theo từng ngày trong khoảng thời gian báo cáo

Định dạng hiển thị theo quy định chung của hệ thống
10Khung thời gian tính hệ sốLabelHiển thị khung thời gian tính báo cáo, theo đầu vào mà Actor đã chọn, nhập vào bao nhiêu khung thì hiển thị bấy nhiều11Tổng số KHLabelHiển thị tổng số KH theo khung thời gian tương ứng trong ngày tương ứng, công thức tính tham khảo ở Mục Business Rule12Tổng số chỗ ngồiLabelHiển thị tổng số chỗ ngồi của nhà hàng trong khung thời gian tương ứng trong ngày tương ứng, công thức tham giáo ở business Rule13Hệ số quay vòngLabelHiển thị hệ số quay vòng của nhà hàng=Giá trị ô 11/Giá trị ô 12 và làm tròn lên 2 số sau thập phân14Tổng số KH theo kỳ báo cáoLabelHiển thị tổng KH trong tất cả các ngày báo cáo trong khung thời gian tương ứng15Tổng số chỗ ngồiLabelHiển thị tổng số chỗ ngồi của nhà hàng trong tất cả các ngày trong khung thời gian tương ứng16Hệ số quay vòng trung bìnhLabelHiển thị hệ số quay vòng của nhà hàng=Giá trị ô 14/Giá trị ô 15 và làm tròn lên 2 số sau thập phân
### 1.7.3.Business Rule
STTRuleThông báo nếu không thỏa mãn rule1
Công thức tính hệ số vòng quay vòng(Table turnover rate)

Hệ số quay vòng bàn (giá trị control số 13,16)  = Tổng số khách hàng được phục vụ theo khoảng thời gian tìm kiếm/Số chỗ ngồi của nhà hàng 

Công thức tính của control số 11, 12

- **Tổng số KH (11):** Ví dụ khoảng thời gian tìm kiếm là từ 18:00-21:00, thì cần lấy tổng số người trên các **lượt đặt bàn** có trạng thái là **Đã thanh toán** trong các ngày báo cáo tương ứng và các lượt đặt bàn đó phải có **thời gian thực tới** >=18:00 và <=21:00
- **Tổng số chỗ ngồi:** Tổng số chỗ ngồi của nhà hàng trong từng ngày báo cáo (dữ liệu chỗ ngồi từng ngày sẽ thay đổi do nhà hàng có thể bố trí thêm bàn, do đó cần lưu ý có bảng lưu trữ thông tin chỗ ngồi theo từng bàn theo ngày)
Dữ liệu cần lấy theo nhà hàng của user đang chọn
 3User phải có quyền thực hiện và đang ở trạng thái hoạt độngBạn không có quyền thực hiện hành động này4User đăng nhập phải thuộc nhà hàng tương  ứng đang sử dụng để lấy báo cáoBạn không thuộc nhà hàng tương ứng5Nhà hàng phải đang ở trạng thái hoạt độngNhà hàng đang không hoạt động6Template file khi xuất excel: template [tại đây](https://docs.google.com/spreadsheets/d/15RhY_ZSCENO0KpCcWaoQu-e866XtnJh4?rtpof=true&authuser=anhminhbaokhanh%40gmail.com&usp=drive_fs) 
## Chức năng tích hợp API với bên khác (Chức năng lấy phí VC)

- <Hiện tại trong list hệ thống quản lý nhà hàng theo scope làm mẫu sẽ ko có chức năng nào cần tích hợp API với bên khác, nên chị giả định xây dựng chức năng Đặt yêu cầu vận chuyển để nhà hàng tạo yêu cầu ship cho đơn của KH nhé>
### 1.8.1.Mô tả chung
**Tên Usecase**Lấy phí VCActorNV lễ tânMục đíchCho phép NV lễ tân xem được thông tin phí vc khi đặt giao hàng Precondition
NV Lễ tân đã đăng nhập hệ thống và có quyền thực hiện

NVPV đang xem chi tiết yêu cầu đơn đặt ship
Main Flow
1.Actor chọn Đặt yêu cầu ship

2.Actor chọn 1 bên đối tác giao hàng và xác nhận đặt

3.Hệ thống gửi lấy phí VC

4.Đối tác trả kết quả

5.Hệ thống hiển thị phí VC
Post ConditionHệ thống hiển thị phí VC tương ứng
 

### 1.8.2.Màn hình

### 1.8.3.Mô tả màn hình

<Tương tự các chức năng khác nên chị không mô tả vào nhé>

### 1.8.4.Luồng tích hợp với DVVC - Sequence diagram

Danh sách API của GHTK
BướcLink đặc tả API1.1.1[https://docs.giaohangtietkiem.vn/#t-nh-ph-v-n-chuy-n](https://docs.giaohangtietkiem.vn/#t-nh-ph-v-n-chuy-n) 2.1.1[https://docs.giaohangtietkiem.vn/#ng-n-h-ng](https://docs.giaohangtietkiem.vn/#ng-n-h-ng) 3.1[https://docs.giaohangtietkiem.vn/#in-nh-n-n-h-ng](https://docs.giaohangtietkiem.vn/#in-nh-n-n-h-ng)3.1.3[https://docs.giaohangtietkiem.vn/#webhooks](https://docs.giaohangtietkiem.vn/#webhooks) 
### 1.8.5.Activity diagram & Mô tả luồng

Với UC này mình có thể tách ra thành 3 UC con để việc vẽ lưu đồ đỡ rối, do nhiều bước quá

- UC lấy phí vận chuyển: Chị sẽ chỉ mô tả UC này, các UC khác tương tự nhé
- UC gửi yêu cầu giao hàng
- UC in nhãn hàng
- **Lấy phí vận chuyển**

 

Mô tả luồng
BướcMô tả3
Mapping thông tin địa bàn

- Mã tỉnh của FoodNow=>Tên tỉnh địa bàn của ĐVVC (Danh mục này được đồng bộ về từ ĐVVC)
- Mã huyện của FoodNow=>Tên huyện địa bàn của ĐVVC
- Mã xã của FoodNow=>Tên xã địa bàn của ĐVVC5.1
Gửi yêu cầu lấy phí sang ĐVVC, chi tiết đặc tả API 

- GHTK: [https://docs.giaohangtietkiem.vn/#t-nh-ph-v-n-chuy-n](https://docs.giaohangtietkiem.vn/#t-nh-ph-v-n-chuy-n)
- Request data: Thông tinMô tả và mapping với hệ thống Foodnowpick_address_idID của địa điểm lấy hàng, nếu trên hệ thống đã có thông tin mapping giữa mã nhà hàng foodNow và mã address_id của đơn vị vận chuyển tương ứng thì lấy giá trị address_id đó rapick_addressĐịa chỉ chi tiết của nhà hàngpick_provinceTên tỉnh lấy hàng (tên tỉnh của nhà hàng) – Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcpick_districtTên huyện lấy hàng  (tên huyện của nhà hàng) – Mapping thông tin mã huyện của foodNow sang tên huyện của ĐvVcpick_wardTên tỉnh lấy hàng  (tên xã của nhà hàng) – Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcpick_street
Tên đường/phố nơi lấy hàng hóa

=>Không truyền giá trị này
addressTên tỉnh lấy hàng – Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcprovinceTên tỉnh nhận hàng– Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcDistrictTên huyện nhận hàng   – Mapping thông tin mã huyện của foodNow sang tên tỉnh của ĐvVcWardTên tỉnh nhận hàng  (tên xã của nhà hàng) – Mapping thông tin mã tỉnh của foodNow sang tên tỉnh của ĐvVcStreet
Tên đường/phố nơi nhận hàng hóa

=>Không truyền giá trị này
WeightTính tổng cân nặng của các món ăn (mỗi món ăn đều cấu hình cân nặng tương ứng)ValueTổng giá trị tiền của món ănTransportHÌnh thức vận chuyển hàng hóa road ( bộ ) , fly (bay, Không truyền sang/truyền sang với giá trị =roaddeliver_option
Sử dụng phương thức vận chuyển xfas

Truyền giá trị none
tags<Hiện tại chị chưa hiểu trường này>
 
5.3Hiển thị thông báo lỗi: “Vui lòng liên hệ số hotline 1243345 (Không mapping được danh mục địa bàn)”7
Mapping kết quả trả về

- Nếu fee.delivery=false hoặc success=false=>Lấy phí thất bại
- Nếu success=true và fee.delivery=true=>Lấy phí thành côngThông tinMô tả và mapping với hệ thống FoodnowSuccess
True nếu thành công

False nếu thất bại
MessageMô tả lỗi, nếu thất bại sẽ có thông tin nàyfee.nameTên gói cước áp dụng, có các giá trị area1, area2, area3fee.feeCước vận chuyển tính theo VNĐfee.insurance_feeGiá bảo hiểm tính theo VNĐfee.delivery
=true nếu đã hỗ trợ giao tại địa chỉ này

=false nếu chưa giao về địa chỉ này

extFees.display

 
Thông tin hiển thị phụ phíextFees. titleTên phụ phíextFees. amountSố tiền phíextFees. TypeLoại phụ phí
 
8Kiểm tra thông tin hợp lệ nếu kết quả trả về là thành công 10
Hiển thị thông báo lỗi
**Trường hợp****Lỗi hiển thị**Địa bàn chưa hỗ trợ giao hàng (fee.delivery=false) Địa bàn chưa hỗ trợ giao hàngGửi yêu càu lấy phí thất bại (success=false)Hiển thị thông báo lỗi theo message mà ĐVVC trả về
 

 

 

## **Chức năng dạng API**

## API do mình định nghĩa đặc tả(API đặt bàn)

### **2.2.1.Mô tả chung**
**Tên UC****API đặt bàn****Mục đích****Cho phép các đối tác gửi yêu cầu đặt bàn sang FoodNow****Đối tượng sử dụng**Đối tác đặt bàn như Pasgo, tableNow**Post-condition**Lưu thông tin đặt bàn và Trả về kết quả đặt bàn
### **2.2.2.**Luồng** nghiệp vụ**

**Mô tả luồng**
**Bước****Mô tả****2**Mã đối tác hợp lệ: Mã đối tác tồn tại và đang hoạt động trên hệ thống**3**
Mã nhà hàng hợp lệ:

- Mã nhà hàng đang hoạt động trên hệ thống và nhà hàng đang liên kết đặt chỗ với đối tác (Mỗi nhà hàng muốn triển khai đặt chỗ trên Pasgo/Table now thì cần phải đăng ký triển khải trên ứng dụng Web quản lý nhà hàng)**4**
Khung thời gian hợp lệ

- Thời gian tới > thời gian hiện tại
- Thời gian tới nằm trong khung thời gian mở cửa của nhà hàng
- Thời gian tới không nằm trong thời gian nhà hàng thiết lập thời gian nghỉ lễ
 
**5**
Bàn hợp lệ

- Mã bàn tồn tại và đang hoạt động trên nhà hàng tương ứng
- Bàn chưa được đặt trong khung thời gian đó: Bàn không booking nào mà có thời gian thời gian dự kiến kết thúc>=thời gian KH đặt >=Thời gian dự kiến tới
 
**6**
Lưu thông tin đặt bàn

- Các thông tin tham số đầu vào
- Và các thông tinMã đặt bàn: Tự sinh theo quy định chung
- Thời gian đặt =Thời gian hiện tại
- Thời gian dự kiến kết thúc=Thời gian dự kiến tới + thời gian phục vụ trung bình/bàn
### **2.2.3.Thông tin đầu vào**
**Thông tin****Require****Length****Mô tả/Ràng buộc khác**Mã đối tácYes Mã đối tác do foodNow đã cung cấp cho đối tácMã yêu cầu đặt bànYes  Mã nhà hàngYes Mã nhà hàng trên hệ thống pasgoHọ tên KH đặtYes**3-50**Chỉ gồm các ký tự aA-zZ và ký tự blankSố điện thoại người đặt bànYes10Gồm 10 ký số bắt đầu bằng 03,08,09Thời gian dự kiến tớiYes 
Định dạng ddmmyyyy hh24:mi:ss

Thời gian dự kiến tới>Thời gian hiện tại
Số người Yes Số nguyên dương, tối đa 3 ký tự số
### **2.2.4.Thông tin đầu ra**
**Thông tin****Mô tả/Ràng buộc khác**Mã đối tácMã đối tác do foodNow đã cung cấp cho đối tácMã nhà hàngMã nhà hàng trên hệ thống FoodNowMã yêu cầu đặt bànMã này của pasgoMã đặt bànMã đặt bàn tương ứngMã lỗiMã lỗi tương ứngMô tả lỗiMô tả lỗi tương ứng, xem chi tiết danh sách lỗi bên dưới
### **2.2.5.Danh sách mã lỗi**
**Trường hợp****Mô tả lỗi tương ứng**Mã đối tác không tồn tại hoặc không hoạt độngMã đối tác không hợp lệMã nhà hàng không tồn tại hoặc không hoạt độngMã nhà hàng không hợp lệHết bàn đặtHết bànThành côngThành công
 

## **API do bên khác define thông tin (API cập nhật kết quả thanh toán Momo)**

### **2.2.1.Mô tả **chung
**Tên UC****API cập nhật thanh toán kết quả của Momo****Mục đích****Cho phép các đối tác gửi yêu cầu đặt bàn sang FoodNow****Đối tượng sử dụng**Đối tác đặt bàn như Pasgo, tableNow**Post-condition**Trả về kết quả đặt bàn
### **2.2**.2.Luồng** nghiệp vụ**

**Mô tả luồng**
**Bước****Mô tả****2**Checksum hợp lệ: Thực hiện mã hóa theo yêu cầu của Momo với key được cung cấp, nếu checksum của FoodNow tạo ra = checksum do đối tác gửi sang thì coi là hợp lệ**3**
- Mã nhà hàng hợp lệ: Mã nhà hàng đang hoạt động trên hệ thống và nhà hàng đang liên kết thanh toán với đối tác
- Mã chi nhánh nhà hàng hợp lệ: Mã chi nhánh nhà hàng đang hoạt động trên hệ thống**4**
Mã GD tồn tại trên hệ thống và khớp với nhà hàng , chi nhánh nhà hàng tương ứng

 
**5**
Số tiền hợp lệ: Số tiền momo gửi sang = số tiền tương ứng với mã GD của foodnow

 
**6**
Trạng thái bàn hợp lệ là bàn ở trạng thái Chờ thanh toán

Ngược lại là không hơp lệ
**7,8**
Tham khảo đặc tả API của Momo tại đây:

[https://developers.momo.vn/v2/#/docs/qr_payment?id=x%c3%a1c-nh%e1%ba%adn-giao-d%e1%bb%8bch](https://developers.momo.vn/v2/#/docs/qr_payment?id=x%c3%a1c-nh%e1%ba%adn-giao-d%e1%bb%8bch) 

### **2.2.3.Thông **tin** đầu vào/ đầu ra**

Tham khảo đặc tả API của Momo tại đây: [https://developers.momo.vn/v2/#/docs/qr_payment?id=x%e1%bb%ad-l%c3%bd-thanh-to%c3%a1n](https://developers.momo.vn/v2/#/docs/qr_payment?id=x%e1%bb%ad-l%c3%bd-thanh-to%c3%a1n) 

### **2.2**.4.Danh** sách mã lỗi**
**Trường hợp****Mã lỗi tương ứng (theo yêu cầu của Momo**Checksum không đúng13Mã nhà hàng hoặc chi nhánh nhà hàng không hợp lệ13Mã GD không tồn tại42Số tiền không hợp lệ21Không có lỗi gì00Thành công 
## **Tiến trình**

## **Tiến trình xử lý đơn giản**

### 3.1.1.Mô tả chung
**Tên Usecase**Tiến trình tạo yêu cầu thanh toán cho nhà hàngMục đíchHệ thống tạo ra các yêu cầu thanh toán cho các nhà hàng khi sắp bước sang kỳ hạn mớiTần suất1 ngày/lần vào 01 giờ hàng ngày (có thể cấu hình thay đổi theo từng thời kỳ)Điều kiện quét dữ liệuLọc các nhà hàng có ngày kết thúc sử dụng-Ngày hiện tại <=10 và trạng thái nhà hàng khác trạng thái ĐóngPost-conditionTạo yêu cầu thanh toán với hạn thanh toán = Ngày kết thúc sử dụng, trạng thái thanh toán = Chờ thanh toán
### 3.1.2.Biểu đồ trạng thái

- N/A
### 3.1.3.Luồng, Mô tả luồng/Business rule

- Bước 1: Quét các nhà hàng thỏa mãn điều kiện ở trên
- Bước 2: Thực hiện lấy gói sản phẩm nhà hàng đang dùng, giá gói hiện tại , lấy CTKM đang áp dụng
- Bước 3: Tạo yêu cầu thanh toán với các thông tinMã nhà hàng=Nhà hàng đã quét được ở bước 1
- Gói sản phẩm= gói SP nhà hàng đang sử dụng
- Số tiền thanh toán=Giá gói hiện tai sản phẩm của nhà hàng đang sử dụng – Giảm giá KM
- Hạn thanh toán=Ngày kết thúc hiện tại của nhà hàng
- Kỳ hạn=kỳ hạn mà nhà hàng đang đăng ký sử dụng
- Trạng thái thanh toán=Chờ thanh toán
### 3.1.4.Biểu đồ luồng dữ liệu

 

 

 

 

 

## **Tiến trình xử lý phức tạp (Tiến trình charge phí)**

### 3.3.1.Mô tả chung
**Tên Usecase**Tiến trình charge phíMục đíchTiến trình tự động charge phí với các nhà hàng đã liên kết tài khoản/ThẻTần suất1 ngày/lần vào 8 giờ hàng ngàyĐiều kiện quét dữ liệu
Lọc theo điều kiện sau:

- các yêu cầu thanh toán có trạng thái Chờ thanh toán
- Nhà hàng có trạng thái Đang hoạt động
- Và nhà hàng tương ứng với yêu cầu thanh toán đó đã liên kết thẻ/TK và trạng thái đang hoạt độngPost-condition
- Thực hiện gửi yêu cầu sang cổng thanh toán để thực hiện trừ tiền KH 
- Cập nhật yêu cầu thanh toán về trạng thái Đã thanh toán
- Gia hạn kỳ hạn mới cho nhà hàng
- Nếu ngày kết thúc kỳ hiện tại=Ngày hiện tại -1 thì thực hiện khóa nhà hàng
### 3.3.2.Biểu đồ trạng thái

 

### 3.3.3. Luồng, Mô tả luồng/Business rule

### 3.3.4.Biểu đồ luồng dữ liệu