---
id: 178
title: "Tài liệu phân tích chi tiết - Ứng dụng dành cho NV phục vụ"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-06-29T13:22:56.000Z"
source_url: "https://m2mba.com/blog/articles/tai-lieu-phan-tich-chi-tiet-ung-dung-phuc-vu"
---

# Tài liệu phân tích chi tiết - Ứng dụng dành cho NV phục vụ

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-06-29T13:22:56.000Z*

## Lịch sử thay đổi
**Nội dung thay đổi****Loại thay đổi (A,M,D)****Mục thay đổi****Nguồn thay đổi****Ngày thay đổi****Version**Toàn bộ tài liệu**A**Toàn bộAnhdtn4/10/20211.0Tạo QR Momo thanh toán online**A**3.11<Tên người/bộ phận yêu cầu thay đổi>20/10/20211.1
## **Flow người dùng (Option)**

## **Luồng đặt bàn, đặt món trực tiếp tại nhà hàng**

 

 

## **Luồng đặt món từ các bàn đang phục vụ tại nhà hàng**

## **Luồng thanh toán**

## **Bố cục màn hình**

STTTên controlLoại controlMô tả1UserIconClick vào icon sẽ hiển thị menu (2,3) : Chi tiết tài khoản, Đăng xuất2Chi tiết tài khoảnMenuClick vào menu sẽ ra màn hình chức năng Xem thông tin chi tiết tài khoản3Đăng xuấtMenuClick vào menu sẽ đăng xuất ra khỏi ứng dụng4HomeMenuClick vào menu sẽ ra màn hình Trang chủ, là danh sách bàn theo trạng thái hiện tại 5Bàn trốngMenuClick vào menu sẽ hiển thị Danh sách bàn trống hiện tại tại nhà hàng6Đang phục vụ MenuClick vào menu sẽ hiển thị Danh sách các bàn đang được phục vụ tại nhà hàng7Bàn chưa tớiMenuClick vào menu sẽ hiển thị Danh sách bàn mà KH đặt mà chưa tới nhà hàng8Danh sách đặt bànMenu Click vào menu sẽ hiển thị Danh sách đặt bàn của nhà hàng (quá khứ, hiện tại và tương lai)
 

## **Chi tiết chức năng**

## Danh sách bàn theo trạng thái

### 3.1.1.Mô tả chung
**Tên Usecase**Xem Danh sách bàn theo trạng tháiActorNV PV Mục đíchCho phép NV PV theo dõi trang thái hiện tại của các bàn trong nhà hàngPrecondition
NV PV đã đăng nhập hệ thống và có quyền thực hiện

và đã có bàn đặt trước đó
  Main flow
1.Actor Chọn menu Home

2.Hệ thống hiển thị màn hình danh sách bàn mặc định

3.Actor Nhập thông tin tìm kiếm

4.Hệ thống hiển thị kết quả tìm kiếm theo yêu cầu của Actor
Post ConditionHiển thị danh sách bàn theo trạng thái mặc định sau khi đăng nhập vào và hiển thị danh sách bàn theo kết quả tìm kiếm của người dùng
### 3.1.2.Màn hình

### 3.1.3.Mô tả màn hình
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
### 3.1.4.Business Rule
RuleChi tiết ruleTìm kiếm
Tìm kiếm theo điều kiện AND các thông tin nhập vào

- Trường thông tin nào chọn Tất cả thì không cần tìm kiếm theo tiêu chí đó
- Tìm kiếm kết hợp cả thông tin nhập trên ô searchbox: Tìm kiếm tương đối (LIKE), không phân biệt hoa thường. Nếu không nhập thì bỏ qua tiêu chí này
- Tìm kiếm theo trạng tháiBàn chưa tới: Lấy danh sách bàn có thời gian dự kiến tới >=Từ ngày và <= đến ngày và có trạng thái Đặt chỗ thành công
- Bàn đang phục vụ/ Bàn chờ thanh toán/Chờ phục vụ: Lấy danh sách bàn có trạng thái dang phục vụ, không quan tâm thời gian
- Bàn trống: Lấy danh sách bàn mà chưa được ai đặt bàn trong khoảng từ ngày- đến ngày: tức thời gian dự kiến tới không nằm trong khoảng từ ngày – Đến ngàySắp xếpCho phép sắp xếp theo tên khu vực tăng dần theo alpha BMàn hình mặc định
Mặc định lấy theo tiêu chí tìm kiếm sau

- Khu vực: Tất cả
- Trạng thái: Tất cả
- Thời gianTừ ngày=Thời gian hiện tại
- Đền ngày=thời gian hiện tại + thời gian phục vụ trung bình/bàn
- Yêu cầu: Tất cảMàu sắc hiển thịTheo quy định chung về màu sắc từng bàn trong quy định xử lý giao diện chung (tạm thời C Ánh chưa xong phần này)
## Danh sách bàn trống

### 3.2.1.Mô tả chung
**Tên Usecase**Danh sách bàn trốngActorNV PV Mục đíchCho phép NV PV theo dõi bàn trống tại nhà hàngPreconditionNV PV đã đăng nhập hệ thống và có quyền thực hiệnMain flow
1.Chọn menu Bàn trống

2.Hệ thống hiển thị danh sách bàn trống trong khoảng thời gian hiện tại (chi tiết rule xem ở Business rule)
Post ConditionHiển thị danh sách bàn trống
 

### 3.2.2.Màn hình

### 3.1.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Search BoxTextboxNhập mã/tên phòng để tìm kiếm2FilterIcon
Click vào sẽ mở ra màn hình nhập thông tin tìm kiếm nâng cao. Tham khảo mô tả trong [Danh sách bàn theo trạng thái](https://docs.google.com/document/d/1-Ise2GZwMEncBtPF_u7JVU1C4ZsvX0tr/edit#heading=h.gjdgxs)

Lưu ý: Bắt buộc tìm kiếm theo trạng thái: Đang trống, Không cho chọn thay đổi trạng thái
3Khu vựcListHiển thị danh sách khu vực của nhà hàng4Thông tin phòngLabelHiển thị thông tin phòng theo định dạng: <tên phòng> - <Loại phòng>-<Đặc điểm của phòng**>(Số bàn trống trong phòng)**5Tên bànLabel
Hiển thị tên bàn tương ứng với định dạng

- Bàn trống: <Tên bàn>
 
6Đang trốngLabelThể hiện bàn đang trống7Thời gian quá hẹnLabelThể hiện thời gian bàn đã đặt nhưng hiện tại vẫn chưa tới, tổng thời gian trễ = Thời gian hiện tại – thời gian dự kiến tới, tính trên đơn vị phút8Thời gian sẽ tớiLabelThể hiện bàn đang trống nhưng đang có thời gian dự kiến tới >=Thời gian hiện tại + thời gian phục vụ trung bình/bàn
### 3.2.4.Business Rule
RuleChi tiết ruleTìm kiếm
Tìm kiếm theo điều kiện AND các thông tin nhập vào

- Trường thông tin nào chọn Tất cả thì không cần tìm kiếm theo tiêu chí đó
- Tìm kiếm kết hợp cả thông tin nhập trên ô searchbox: Tìm kiếm tương đối (LIKE), không phân biệt hoa thường. Nếu không nhập thì bỏ qua tiêu chí này
- Tìm kiếm theo trạng tháiLấy danh sách bàn mà chưa được ai đặt bàn trong khoảng từ ngày- đến ngày: tức thời gian dự kiến tới không nằm trong khoảng từ ngày – Đến ngày
- Hoặc bàn có thời gian dự kiến tới <= thời gian hiện tại nhưng vẫn đang chưa tới
- Hoặc Thời gian hiện tại=<bàn có thời gian dự kiến tới <=Thời gian hiện tại + thời gian phục vụ trung bình/bànSắp xếpCho phép sắp xếp theo tên khu vực tăng dần theo alpha BMàn hình mặc định
Mặc định lấy theo tiêu chí tìm kiếm sau

- Khu vực: Tất cả
- Trạng thái: Đang trống (không được phép sửa)
- Thời gian : mặc định như bên dưới (không được phép sửa)Từ ngày=Thời gian hiện tại
- Đền ngày=thời gian hiện tại + thời gian phục vụ trung bình/bàn
- Yêu cầu: Tất cảMàu sắc hiển thịTheo quy định chung về màu sắc từng bàn trong quy định xử lý giao diện chung (tạm thời C Ánh chưa xong phần này)
 

 

## Danh sách bàn chưa tới

### 2.3.1.Mô tả chung
**Tên Usecase**Danh sách bàn chưa tớiActorNV PV Mục đíchCho phép NV PV theo dõi danh sách các bàn đã đặt nhưng chưa tớiPreconditionNV PV đã đăng nhập hệ thống và có quyền thực hiệnMain flow
1.Chọn menu Bàn chưa tới

2.Hệ thống hiển thị màn hình danh sách bàn chưa tới mặc định

3.Nhập thông tin tìm kiếm

3.Hệ thống hiển thị kết quả tìm kiếm theo yêu cầu của Actor
Post ConditionHiển thị danh sách bàn chưa tới theo trạng thái mặc định sau khi đăng nhập vào và hiển thị danh sách bàn chưa tới theo kết quả tìm kiếm của người dùng
 

 

 

### 2.3.2.Màn hình

### 2.3.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Search BoxTextboxNhập mã/tên phòng để tìm kiếm2FilterIcon
Click vào sẽ mở ra màn hình nhập thông tin tìm kiếm nâng cao. Tham khảo mô tả trong [Danh sách bàn theo trạng thái](https://docs.google.com/document/d/1-Ise2GZwMEncBtPF_u7JVU1C4ZsvX0tr/edit#heading=h.gjdgxs)

Lưu ý: Bắt buộc tìm kiếm theo trạng thái: Đang trống, Không cho chọn thay đổi trạng thái
3Khu vựcListHiển thị danh sách khu vực của nhà hàng4Thông tin phòngLabelHiển thị thông tin phòng theo định dạng: <tên phòng> - <Loại phòng>-<Đặc điểm của phòng>(**Số bàn chưa tới : Tính theo số bàn thực tế, 1 booking đặt 2 bàn thì vẫn tính 2 bàn**)5Tên bànLabel
Hiển thị tên bàn tương ứng với định dạng

- <Tên bàn> (<Tổng số bàn của lượt đặt bàn này)>
 
6Thời gian quá hẹnLabel
Chỉ hiển thị với bàn ở trạng thái Đặt bàn thành công và thời gian dự kiến tới <Thời gian hiện tại

Tổng thời gian trễ = Thời gian hiện tại – thời gian dự kiến tới, tính trên đơn vị phút
7Mã đặt bànLabelMã đặt bàn tương ứng8Tên KH đặt bànLabelTên KH đặt bàn9Số điện thoạiLabelSố điện thoại của KH đặt bàn
### 3.2.4.Business Rule
RuleChi tiết ruleTìm kiếm
Tìm kiếm theo điều kiện AND các thông tin nhập vào

- Trường thông tin nào chọn Tất cả thì không cần tìm kiếm theo tiêu chí đó
- Tìm kiếm kết hợp cả thông tin nhập trên ô searchbox: Tìm kiếm tương đối (LIKE), không phân biệt hoa thường. Nếu không nhập thì bỏ qua tiêu chí nàyThông tin tìm kiếm trên ô search box: Tìm kiếm theo thỏa mãn 1 trong các điều kiện: Mã bàn/tên bàn/Họ tên đặt bàn/Số điện thoại LIKE <Thông tin nhập vào>
- Tìm kiếm theo trạng tháiLấy danh sách bàn có trạng thái :Đặt bàn thành công và có thời gian hẹn tới <=Đến ngày đã nhập vào tìm kiếm
 
Sắp xếpCho phép sắp xếp theo tên khu vực tăng dần theo alpha BMàn hình mặc định
Mặc định lấy theo tiêu chí tìm kiếm sau

- Khu vực: Tất cả
- Trạng thái: Đặt bàn thành công
- Thời gian : mặc định như bên dưới (không được phép sửa)Từ ngày=Thời gian hiện tại
- Đền ngày=thời gian hiện tại + thời gian phục vụ trung bình/bàn
- Yêu cầu: Tất cả
## Danh sách bàn đang phục vụ

### 2.4.1.Mô tả chung
**Tên Usecase**Danh sách bàn chưa tớiActorNV PV Mục đíchCho phép NV PV theo dõi danh sách các bàn đã đặt nhưng chưa tớiĐường dẫn menuĐăng nhập=>Chọn Danh sách Bàn chưa tớiPreconditionNV PV đã đăng nhập hệ thống và có quyền thực hiệnMain flow
1.Chọn menu Bàn chưa tới

2.Hệ thống hiển thị màn hình danh sách bàn chưa tới mặc định

3.Nhập thông tin tìm kiếm

3.Hệ thống hiển thị kết quả tìm kiếm theo yêu cầu của Actor
Post ConditionHiển thị danh sách bàn chưa tới theo trạng thái mặc định sau khi đăng nhập vào và hiển thị danh sách bàn chưa tới theo kết quả tìm kiếm của người dùng
 

### 2.4.2.Màn hình

### 2.4.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Search BoxTextboxNhập mã/tên phòng để tìm kiếm2FilterIcon
Click vào sẽ mở ra màn hình nhập thông tin tìm kiếm nâng cao. Tham khảo mô tả trong [Danh sách bàn theo trạng thái](https://docs.google.com/document/d/1-Ise2GZwMEncBtPF_u7JVU1C4ZsvX0tr/edit#heading=h.gjdgxs)

Lưu ý: Bắt buộc tìm kiếm theo trạng thái: Đang phục vụ, Không cho chọn thay đổi trạng thái, ẩn khung thời gian tìm kiếm
3Khu vựcListHiển thị danh sách khu vực của nhà hàng4Thông tin phòngLabelHiển thị thông tin phòng theo định dạng: <tên phòng> - <Loại phòng>-<Đặc điểm của phòng>(**Số bàn đang phục vụ: Tính theo số bàn thực tế, 1 booking đặt 2 bàn thì vẫn tính 2 bàn**)5Tên bànLabel
Hiển thị tên bàn tương ứng với định dạng

- <Tên bàn> (<Tổng số bàn của lượt đặt bàn này)>
 
6Thời gian dự kiến kết thúcLabel=Thời gian tới + thời gian phục vu trung bình/bàn7Mã đặt bànLabelHiển thị 3 ký tự cuối của mã đặt bàn (mã đặt bàn sẽ đặt theo dạng Mã nhà hàng_yymmdd_số tự tăng (từ 001)8Tổng tiềnLabelTổng tiền tạm tính trên các món KH đã đặt (ko tính đã hủy, hết hàng)9,10Left, rightIconChỉ hiển thị khi số lượng hiển thị trên màn hình không đủ, user có thể trượt trái, phải để xem thông tin các bàn khác
### 2.4.4.Business Rule
RuleChi tiết ruleTìm kiếm
Tìm kiếm theo điều kiện AND các thông tin nhập vào

- Trường thông tin nào chọn Tất cả thì không cần tìm kiếm theo tiêu chí đó
- Tìm kiếm kết hợp cả thông tin nhập trên ô searchbox: Tìm kiếm tương đối (LIKE), không phân biệt hoa thường. Nếu không nhập thì bỏ qua tiêu chí nàyThông tin tìm kiếm trên ô search box: Tìm kiếm theo thỏa mãn 1 trong các điều kiện: Mã bàn/tên bàn/Họ tên đặt bàn/Số điện thoại LIKE <Thông tin nhập vào>
- Tìm kiếm theo trạng tháiLấy danh sách bàn có trạng thái hiện tại: Đang phục vụ/Chờ phục vụ
 
Sắp xếpCho phép sắp xếp theo tên khu vực tăng dần theo alpha BMàn hình mặc định
Mặc định lấy theo tiêu chí tìm kiếm sau

- Khu vực: Tất cả
- Trạng thái: Đang phục vụ (không được sửa)
- Thời gian : Ẩn đi và không quan tâm tới thông tin này
- Yêu cầu: Tất cả
 

## Xem chi tiết thông tin đặt bàn

### 2.4.1.Mô tả chung
**Tên Usecase**Xem chi tiết thông tin đặt bànActorNV PV Mục đíchCho phép NV PV xem chi tiết thông tin đặt bàn (đặt trước hoặc đến ăn tại nhà hàng rồi đặt bàn)PreconditionNV PV đã đăng nhập hệ thống và có quyền thực hiệnMain flow
1.Chọn 1 bàn trong Danh sách bàn theo trạng thái hoặc Bàn chưa tới/Đang phục vụ (nếu bàn theo trạng thái thì phải chọn vào bàn ở trạng thái Đặt chỗ thành công, Chờ phục vụ, Đang phục vụ)

2.Hệ thống hiển thị màn hình chi tiết thông tin đặt bàn

 
Post ConditionHiển thị chi tiết thông tin đặt bàn kèm với các thao tác đi kèm
 

### 2.4.2.Màn hình

 

### 2.4.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Trạng thái đặt bànLabelTrạng thái đặt bàn tương ứng, tham khảo quy định về màu sắc trạng thái của bàn trong quy định chung về xử lý giao diện2Thông tin đặt bànTab barClick vào sẽ xem chi tiết về thông tin đặt bàn3Chi tiết mónTab barClick vào sẽ xem chi tiết về thông tin món ăn của bàn tương ứng4Họ tên người đặt bànLink
Hiển thị tên người đặt bàn, có link đính kèm

Nếu click vào link sẽ ra thông tin chi tiết người đặt bàn
5Số điện thoại đặt bànLabel
Hiển thị số điện thoại người đặt bàn

 
6Họ tên người nhận bànLabelHiển thị họ tên người nhận bàn7Số điện thoại người nhận bànLabelHiển thị họ tên người nhận bàn8Tổng số ngườiLabelTổng số người 9Chi tiết ngườiLabelChi tiết số người lớn, trẻ em10Thời gian đặtLabelHiển thị thời gian đặt bàn: hiển thị theo định dạng dd/mm/yyyy hh24:mi11Kênh đặt bànLabel
Hiển thị kênh đặt bàn của bàn tương ứng

- Đặt qua điện thoại/lễ tân: Đặt trước - <username đặt bàn>
- Đặt qua đơn vị đặt chỗ khác: <Tên đơn vị đặt >
- Đến nhà hàng: Trực tiếp - <Username đặt bàn>12Dự kiến tớiLabelHiển thị thời gian dự kiến tới : hiển thị theo định dạng dd/mm/yyyy hh24:mi13Kết thúc dự kiếnLabelHiển thị thời gian dự kiến kết thúc: hiển thị theo định dạng dd/mm/yyyy hh24:mi14Thực tớiLabel
Hiển thị thời gian thực tới : hiển thị theo định dạng dd/mm/yyyy hh24:mi

Nếu chưa tới thì không hiển thị
15Thực kết thúcLabel
Hiển thị thời gian thực kết thúc: hiển thị theo định dạng dd/mm/yyyy hh24:mi

Nếu chưa tới/ Chưa kết thúc thì không hiển thị
16Tổng số bànLabelTổng số bàn của lượt đặt bàn đó17Thông tin bànLabel
Hiển thị thông tin bàn theo định dạng: <tên bàn>-<Tên phòng>-<đặc điểm của phòng>

Hiển thị màu sắc bàn theo đúng quy định chung:

- Bàn đang phục vụ
- Bàn chưa tới18Số lượng người có thể ngồi/bànLabelSố lượng người có thể ngồi/bàn19,20Thao tácCombo ButtonChỉ hiển thị khi bàn đang ở trạng thái khác Chờ thanh toán, Đã thanh toán21Xem tất cảLinkClick vào link sẽ hiển thị màn hình chi tiết bàn của lượt booking đó 22Tổng tiền tạm tínhLabelHiển thị tổng số tiền tạm tính (không tính món đã hủy hoặc hết hàng)23Thêm bànButton
Chỉ hiển thị button này khi bàn đang ở trạng thái khác Chờ thanh toán, Đã thanh toán

Click vào button này sẽ Mở màn hình chọn Danh sách bàn để thêm bàn
24Đặt mónButton
Chỉ hiển thị button này khi bàn đang ở trạng thái khác Chờ thanh toán, Đã thanh toán

Click vào button này sẽ Mở màn hình Đặt món
25Đã tớiButtonChỉ hiển thị button này khi bàn chưa tới, ở trạng thái Đặt chỗ thành công26Kết thúcButtonChỉ hiển thị button này khi bàn chưa tới, ở trạng thái Đặt chỗ thành công, Chờ phục vụ27Mã đặt bànLabelHiển thị mã đặt bàn của nhà hàng28Thanh toánLabelChỉ hiển thị button này khi bàn ở trạng thái Đang phục vụ29In kiểm đồLabelChỉ hiển thị button này khi ở trạng thái Đang phục vụ
## Xem chi tiết thông tin đặt món

### 2.4.1.Mô tả chung
**Tên Usecase**Xem chi tiết thông tin mónActorNV PV Mục đíchCho phép NV PV xem chi tiết thông tin đặt món của bàn tương ứngPrecondition
NV PV đã đăng nhập hệ thống và có quyền thực hiện

NVPV đang ở màn hình Xem chi tiết thông tin đặt bàn
Main flow
1.Chọn xem chi tiết món

2.Hệ thống hiển thị màn hình chi tiết món ăn mà bàn đã đặt

 
Post Conditionhiển thị màn hình chi tiết món ăn mà bàn đã đặt
 

### 2.4.2.Màn hình

 

 

### 2.4.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Tên mónLabel
Hiển thị tên món ăn

 
2Ghi chúLabel
Nếu món ăn có size thì hiển thị tên size món ăn tương ứng mà KH đã đặt và hiển thị phần ghi chú của KH theo định dạng

<Size> - <Ghi chú của KH>: hiển thị tối đa 30 ký tự

Nếu dài quá thì click vào mũi tên để hiển thị tiếp. 
3Đơn giá mónLabelHiển thị đơn giá món (giá sau giảm nếu có)4Số lượngLabelSố lượng đã đặt5Đã giaoLabel
Số lượng đã giao

 
6Thành tiềnLabelHiển thị tổng tiền =Số lượng* đơn giá7Trạng tháiLabel
Hiển thị trạng thái của món ăn tương ứng

Tham khảo quy định hiển thị trạng thái trong Quy định chung về xử lý giao diện
8Tổng tiền tạm tínhLabel
- Nếu bàn chưa tới/Đang phục vụ/chờ thanh toán: Hiển thị tổng tiền tạm tính = Tổng (số lượng * Đơn giá) của các món ăn khác hủy, đã hết hàng
- Nếu bàn đã thanh toán, sẽ hiển thị Tổng tiền đã thanh toán 9Tổng tiền đã giaoLabel
- Hiển thị tổng tiền tạm tính = Tổng (số lượng * Đơn giá) của các món ăn đã giao tối thiểu 1 suất cho KH
- Chỉ hiển thị với bàn ở trạng thái Đang phục vụ10Số món chưa giaoLabelChỉ hiển thị khi còn số món chưa giao11Tổng suất chưa giaoLabelChỉ hiển thị khi còn số món chưa giao12Filter Trạng tháiIconCho phép filter theo trạng thái, cụ thể các trạng thái ở mục 1313Danh sách trạng thái filterListDanh sách trạng thái filter14Giảm SLIcon
Click vào sẽ chọn giảm số lượng món

Chỉ được chọn thông tin này khi món vừa đặt được X (ph)
15Hủy mónIconChỉ hiển thị icon này khi Bàn ở trạng thái Đặt chỗ thành công hoặc nếu Đang phục vụ thì chưa được giao suất nào và thời gian đặt <X ph so với thời gian hiện tại
## Xác nhận bàn tới

### 3.1.1.Mô tả chung
**Tên Usecase**Xác nhận bàn tớiActorNV PV Mục đíchCho phép NV PV xác nhận KH đã tớiPrecondition
NV VH đã đăng nhập hệ thống và có quyền thực hiện

NVPV đang xem chi tiết bàn tương ứng của KH đặt
Main Flow
1.Chọn xác nhận KH tới

2.Hệ thống cập nhật trạng thái bàn sang Chờ phục vụ

3.Hệ thống hiển thị nút RollBack để NVPV có thể hủy thao tác nếu click nhầm

4.Chọn rollback

5.hệ thống cập nhật lại trạng thái Đặt bàn thành công
Post ConditionHệ thống cập nhật trạng thái bàn sang chờ phục vụ nếu không rollback
 

### 3.1.2.Màn hình

### 2.4.3.Mô tả màn hình
STTTên controlLoại controlMô tả & ghi chú1Đã tớiButton
Click vào button sẽ chuyển trạng thái bàn sang Chờ phục vụ, và hiển thị các thông tin tương ứng của bàn ở trạng thái chờ phục vụ

 
2Thông tin bànLabelHiển thị <Tên KH nhận bàn> - Danh sách bàn3Hủy thao tácIcon buttonClick vào sẽ hủy thao tác vừa xác nhận, bàn trở về trạng thái Đặt bàn thành công
### 3.1.3.Business Rule
RuleThông báo nếu không thỏa mãn ruleMã đặt Bàn đang ở trạng thái Đặt chỗ thành công và thời gian dự kiến tới <=thời gian hiện tại + thời gian phục vu trung bình/bàn
 
Trường hợpNội dung thông báoTrạng thái không hợp lệXác nhận không thành công do Trạng thái đặt bàn đang <Tên trạng thái> Thời gian dự kiến tới không hợp lệBàn này dự kiến tới không nằm trong khung thời gian hiện tại. Vui lòng kiểm tra lại
 
User phải có quyền thực hiện và đang ở trạng thái hoạt độngBạn không có quyền thực hiện hành động nàyBàn trong danh sách đặt bàn phải đang ở trạng thái trống<Liệt kê danh sách tên bàn, cách nhau dấu , nếu nhiều bàn> đang được sử dụng nên không thể xác nhận. Vui lòng kiểm tra lạiMã đặt bàn phải thuộc nhà hàng của user đang đăng nhậpMã đặt bàn không hợp lệ. Vui lòng kiểm tra lạiNhà hàng phải đang ở trạng thái hoạt độngNhà hàng đang không hoạt động
## Đặt bàn cho KH

### 3.2.1.Mô tả chung
**Tên Usecase**Đặt bàn ActorNV PV Mục đíchCho phép NV PV Đặt bàn cho KH khi KH tới nhà hàng ăn mà chưa book trước đóĐường dẫn menu
Đăng nhập=>Chọn Danh sách bàn trống/Chọn Bàn trống trên Danh sách bàn theo trạng thái

Ví dụ Xem chi tiết SP của tiki

Trang chủ=>Chọn Xem danh mục sản phẩm=>Chọn 1 SP để xem chi tiết

Trang chủ =>Tìm kiếm sản phẩm=>Chọn 1 SP để xem chi tiết

Đăng nhập=>Danh sách đơn hàng=>Chọn xem chi tiết đơn hàng=>Chọn Xem chi tiết Sản phẩm

 
PreconditionNV VH đã đăng nhập hệ thống và có quyền thực hiệnMain Flow
1.NVPV chọn bàn đạng ở trạng thái trống

2.Hệ thống hiển thị màn hình đặt bàn kèm thông tin bàn vừa chọn

3.NVPV nhập thông tin đặt bàn

4.NVPV chọn Xác nhận

5.hệ thống lưu thông tin đặt bàn ở trạng thái chờ phục vụ
Post ConditionHệ thống lưu thông tin đặt bàn ở trạng thái chờ phục vụ
### 3.2.2.Màn hình

### 3.2.3.Mô tả màn hình
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
### 3.2.4.Business Rule
RuleThông báo nếu không thỏa mãn rule
Bàn phải đang ở trạng thái trống, thỏa mãn điều kiện cụ thể như sau: 

- Bàn thời gian dự kiến tới >= thời gian hiện tại + thời gian phục vụ trung bình/bàn – X(ph) (X được cấu hình theo từng nhà hàng trong chức năng cấu hình tham số nhà hàng)
 

- Bàn có thời gian dự kiến tới <thời gia hiện tại: Bàn đã có người đặt, chưa quá hạn vẫn chưa tới. Vui lòng liên hệ KH để hủy bàn 
- Các TH còn lại: Bàn đã có người đặt, xin vui lòng kiểm tra lạiUser phải có quyền thực hiện và đang ở trạng thái hoạt độngBạn không có quyền thực hiện hành động nàyMã bàn phải đang hoạt động trên hệ thống và thuộc nhà hàng của user đang thực hiện<Liệt kê danh sách tên bàn, cách nhau dấu , nếu nhiều bàn> đang được sử dụng nên không thể xác nhận. Vui lòng kiểm tra lạiNhà hàng phải đang ở trạng thái hoạt độngNhà hàng đang không hoạt động
 

 

## Yêu cầu thanh toán

### 3.2.1.Mô tả chung
**Tên Usecase**Xác nhận bàn tớiActorNV PV Mục đíchCho phép NV PV xác nhận KH đã tớiPrecondition
NV VH đã đăng nhập hệ thống và có quyền thực hiện

NVPV đang xem chi tiết bàn tương ứng của KH đặt
Main Flow
1.Chọn xác nhận KH tới

2.Hệ thống cập nhật trạng thái bàn sang Chờ phục vụ

3.Hệ thống hiển thị nút RollBack để NVPV có thể hủy thao tác nếu click nhầm

4.Chọn rollback

5.hệ thống cập nhật lại trạng thái Đặt bàn thành công
Post ConditionHệ thống cập nhật trạng thái bàn sang chờ phục vụ nếu không rollback
### 3.2.2.Màn hình

### 3.2.3.Mô tả màn hình
STTTên controlLoại controlRequireMô tả1Thanh toánButton Click vào button này sẽ ra màn hình yêu cầu thanh toán2Thông tin bànLabel 
Hiển thị thông tin bàn theo định dạng:

<Mã bàn(3 ký tự cuối)> - Tên KH đặt bàn
3Trạng tháiLabel Hiển thi trạng thái hiện tại của Bàn đặt (chỉ ở yêu cầu trạng thái Đang phục vụ mới hiển thị nút Thanh toán)4Tên mónLabelYesTên món ăn5Đơn giáLabelYesGiá món ăn sau giảm6Số lượngLabel Số lượng KH đã gọi7Đã giaoLabel Số lượng đã giao cho KH8Thành tiềnLabel =Đã giao* Đơn giá9Tổng tiền (Chưa VAT)Label Tổng tiền chưa VAT10Tổng tiền (VAT)Label Tổng tiền có VAT11Lấy VATSlide Có lấy VAT hay không, mặc định sẽ tùy theo từng nhà hàng cấu hình thông số này12Đồng ý thanh toánButton Click vào button này sẽ thực hiện ghi nhận KH đã đồng ý mới đồ đã gọi và hóa đơn đã tính
### 3.2.4.Business Rule
RuleThông báo nếu không thỏa mãn ruleMã đặt bàn phải đang ở trạng thái Đang phục vụYêu cầu thanh toán không thành công do bàn đang ở trạng thái <Tên trạng thái hiện tại>User phải có quyền thực hiện và user ở trạng thái hoạt độngBạn không có quyền thực hiện hành động nàyMã đặt bàn phải thuộc nhà hàng của user đang đăng nhậpMã đặt bàn không hợp lệ. Vui lòng kiểm tra lạiNhà hàng phải đang ở trạng thái hoạt độngNhà hàng đang không hoạt động
 

## Luồng Tích hợp thanh toán Momo

Chi tiết tài liệu Momo tham khảo tại đây: [https://developers.momo.vn/v2/#/docs/qr_payment ](https://developers.momo.vn/v2/#/docs/qr_payment) 

- Bước 1.1.2: Tham khảo quy định sinh URL QR của Momo tại đây: [https://developers.momo.vn/v2/#/docs/qr_payment?id=t%e1%ba%a1o-qr-code](https://developers.momo.vn/v2/#/docs/qr_payment?id=t%e1%ba%a1o-qr-code) 
- Bước 2.2: Gọi API NotifyURL để báo kết quả Momo treo tiền của KH: [https://developers.momo.vn/v2/#/docs/qr_payment?id=x%e1%bb%ad-l%c3%bd-thanh-to%c3%a1n](https://developers.momo.vn/v2/#/docs/qr_payment?id=x%e1%bb%ad-l%c3%bd-thanh-to%c3%a1n) 
- Bước 2.3: FoodNow gọi API confirm của Momo để xác nhận kết quả thanh toán : [https://developers.momo.vn/v2/#/docs/qr_payment?id=x%c3%a1c-nh%e1%ba%adn-giao-d%e1%bb%8bch](https://developers.momo.vn/v2/#/docs/qr_payment?id=x%c3%a1c-nh%e1%ba%adn-giao-d%e1%bb%8bch) 
## Tạo Momo QR

### Mô tả chung
Tên UsecaseTạo QR MomoActorNV PVMục đíchCho phép NVPV chọn hình thức thanh toán là QR Momo PreconditionActor đã đăng nhập vào hệ thống và đã xác nhận đồng ý thanh toán của mã đặt bàn tương ứngMain Flow
1.Chọn Momo QR trong màn hình Thanh toán (sau khi NVPV đã xác nhận yêu cầu thanh toán, tham khảo tại [Mục 3.9.Yêu cầu thanh toán](https://docs.google.com/document/d/1-Ise2GZwMEncBtPF_u7JVU1C4ZsvX0tr/edit#heading=h.1fob9te))

2.Hệ thống hiển thị QR Momo
Post ConditionHệ thống hiển thị màn hình QR Momo với các tham số liên quan tới đơn hàng
### Màn hình

### 3.2.3.Mô tả màn hình
STTTên controlLoại controlMô tả1Thông tin bànLabelHiển thị mã đặt bàn và tên người nhận bàn2Trạng thái đặt bànLabelTrạng thái Chờ thanh toán3Tổng tiền (chưa VAT)LabelTổng tiền chưa tính VAT4Tổng tiền VATLabelTổng tiền đã tính VAT5Tính VATSlide
Tính hay không tính VAT, với nhà hàng có tham số config cho phép KH lấy VAT hay không thì slide này sẽ được trượt sang trái/phải

Ngược lại sẽ hiển thị mặc định là Lấy VAT và không cho sửa
6Thông tin cổng thanh toán Ảnh đại diện và tên cổng thanh toán tương ứng7Danh sách ngân hàngicon
Với bên cổng thanh toán mà có kết nối nhiều bank, click vào icon này sẽ biết được các ngân hàng hỗ trợ trên cổng thanh toán này, để NV PV dễ dàng tư vấn KH

8Tiếp tụcButtonClick vào button này sẽ chuyển sang màn hình tiếp theo9Số tiền thanh toánLabelSố tiền thanh toán của đơn hàng, phụ thuộc vào thông tin ở màn hình trước NVPV đã chọn (số tiền chưa VAT hoặc đã có VAT)10Mã đơn hàngLabelLà mã đơn hàng do hệ thống foodNow sinh ra để gửi sang bên Momo11QRcodeImageẢnh QR theo quy định của Momo
### Activity diagram và mô tả luồng

- **Mô tả luồng**
 
**Bước****Mô tả**3
Kiểm tra thông tin hợp lệ, thỏa mãn các điều kiện sau

- Mã đặt bàn phải đang ở trạng thái Chờ thanh toán
- Mã đặt bàn thuộc nhà hàng mà user đang đăng nhập
- Nhà hàng đang hoạt động
- User đang hoạt động 5
Lấy các thông tin để tạo URL QR

- PartnerCode: Mã đối tác do Momo cung cấp cho nhà hàng
- storeId: Mã chi nhánh nhà hàng do Momo cung cấp
- Số tiền thanh toán=Số tiền của mã đặt bàn tương ứng (tùy thuộc vào chọn VAT hay không VAT để lấy số tiền thanh toán
- BilID=Mã GD vừa sinh6Tạo URL QR theo quy định của Momo: [https://developers.momo.vn/v2/#/docs/qr_payment?id=t%e1%ba%a1o-qr-code](https://developers.momo.vn/v2/#/docs/qr_payment?id=t%e1%ba%a1o-qr-code) 11
 
Trường hợpThông báo
Mã đặt bàn phải không ở trạng thái Chờ thanh toán

 
Trạng thái đặt bàn không hợp lệ, Vui lòng kiểm tra lạiMã đặt bàn không thuộc nhà hàng mà user đang đăng nhậpThông tin thanh toán không hợp lệUser không hoạt độngTài khoản của bạn đang không hoạt độngNhà hàng không hoạt độngNhà hàng đang không hoạt động trên hệ thống. Vui lòng liên hệ với nhân viên FoodNow để được hỗ trợ