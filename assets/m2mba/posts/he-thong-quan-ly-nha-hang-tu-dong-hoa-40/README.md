---
id: 177
title: "Tài liệu phân tích tổng quan"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-06-29T13:21:18.000Z"
source_url: "https://m2mba.com/blog/articles/he-thong-quan-ly-nha-hang-tu-dong-hoa-40"
---

# Tài liệu phân tích tổng quan

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-06-29T13:21:18.000Z*

## **Mục đích của dự án**

Với xu hướng công nghệ 4.0 các quy trình cần phải được tự động hóa. Và với nhu cầu quản lý thông tin minh bạch giữa các bộ phận trong nhà hàng và khách hàng thì hệ thống quản lý nhà hàng vô cùng cần thiết. Hệ thống quản lý nhà hàng sẽ thực hiện được các công việc sau:

- Cho khách hàng có thể đặt bàn trên nhiều kênh khác nhau như qua app, gọi điện đến nhà hàng, hay qua bên thứ 3 như pasgo 
- Cho phép KH có thể order thức ăn theo nhiều cách khác nhau như order trực tiếp tại ứng dụng cài đặt trên tablet tại bàn, quét QR để đặt món…
- Cho nhân viên nhà hàng có thể kiểm tra tình trạng bàn trống, món ăn đã đặt, trạng thái phục vụ món qua app.
- Cho phép bộ phận bếp theo dõi được tình trạng đặt món ăn.
- Cho phép nhân viên quản lý thao tác và kiểm tra tình trạng nhập xuất kho.
- Cho phép bộ phận kế toán, thu ngân tự động hạch toán, in biên lai, hóa đơn cho khách hàng từ order của nhân viên phục vụ
- Cho phép ban Giám đốc và các cấp quản lý kiểm tra được doanh thu của nhà hàng theo ngày, tuần, quý,...
Tuy nhiên trong giai đoạn đầu, Dự án sẽ tập trung vào các chức năng chính trong quy trình phục vụ tại nhà hàng, bao gồm

- Quy trình đặt chỗ, đặt món, phục vụ tại nhà hàng
- Quy trình thanh toán, quản lý tài chính tại nhà hàng
- …
Không bao gồm:

- Quy trình quản lý kho tại nhà hàng
- Quy trình xử lý tại bếp
- …
 

## **Khái niệm/Thuật ngữ**
**STT****Khái niệm/Thuật ngữ****Mô tả**1KHKhách hàng, người đến nhà hàng để sử dụng dịch vu tại nhà hàng2NV PVBan quản lý chung cư, đơn vị do BQT chung cư thuê để vận hành các hoạt động hằng ngày của chung cư3QLNHQuản lý nhà hàng4OrderPhiếu đặt món   
## **Nguồn tham khảo**

Dưới đây là những tài liệu tham khảo khác của hệ thống:
**STT****Tài liệu****Mô tả****Ngày ban hành****Link tài liệu**1    2    
## **Đối tượng sử dụng**
**Tên đối tượng****Mô tả**NVPVLà người thực hiện giao tiếp trực tiếp với KH tại nhà hàng để đặt bàn, đặt món, kiểm kê hóa đơn trước khi thanh toánNVTNSử dụng để xác nhận thanh toán, in hóa đơn cho KHChủ nhà hàngLà người theo dõi các hoạt động trong nhà hàngKế toánLà người tổng hợp báo cáo tài chính liên quan tới nguồn thu chi tại nhà hàngNVVH FoodNowLà nhân viên bên công ty foodNow, thực hiện theo dõi và quản lý tài khoản của các nhà hàng sử dụng phần mềm foodNow
 

## **Mô hình tổng quan**

 

- **Mô tả các thành phần trong Mô hình**Tên thành phầnMô tảNV Phục vụTham khảo Mục 4.Đối tượng sử dụngNhân viên nhà hàngTham khảo Mục 4.Đối tượng sử dụngNV VH FoodNowTham khảo Mục 4.Đối tượng sử dụngMobile app Phục vụLà mobile app dành cho NV phục vụ để thực hiện đặt bàn, đặt món, xác nhận order trước khi thanh toán tại nhà hàngWeb Quản lý nhà hàngLà ứng dụng dành cho NV tại nhà hàng (bao gồm lễ tân, NV phục vụ, thu ngân, kế toán, Chủ nhà hàng) để thực hiện các công việc tại nhà hàng, ứng dụng được phân quyền linh động cho từng đối tượng khác nhau theo nhu cầu của nhà hàng Web admin
Là ứng dụng dành cho đội NVVH tại foodNow để quản lý hợp đồng với các nhà hàng, cung cấp tài khoản cho nhà hàng, quản lý công nợ nhà hàng…

 
Cổng thanh toánHệ thống foodnow tích hợp với các bên cổng thanh toán để hỗ trợ đa dạng hình thức thanh toán online cho KHHệ thống đặt bànLà hệ thống của các bên thứ 3 như Pasgo, table Now của foody, để hỗ trợ KH có thể đặt bàn trên các ứng dụng đó và đẩy thông tin sang hệ thống FoodNow
## **Quy trình nghiệp vụ**

## **6.1.Quy trình đặt bàn**

## **6.2.Quy trình phục vụ tại nhà hàng**

## **6.3.Quy trình quản lý user nhà hàng**

## **6.4.Quy trình thanh toán của chủ nhà hàng để sử dụng foodNow**

 

 

 

## **ERD**

<Đây chỉ là 1 phần nhỏ của hệ thống nhé>

 

 
**Tên thực thể****Ý nghĩa**Nhà hàngQuản lý danh sách nhà hàng sử dụng dịch vụ phần mềm FoodNowChủ nhà hàngQuản lý danh sách các chủ nhà hàng của các nhà hàng sử dụng phần mềm,  chủ nhà hàng có thể quản lý nhiều nhà hàng khác nhau, Chủ nhà hàng có thể điều chuyển để theo dõi hoạt động kinh doanh của từng nhà hàng khác nhauLoại phòngDanh mục loại phòng của nhà hàng, ví dụ như phòng Vip, Phòng bình dân…PhòngChi tiết các phòng thực tế tại nhà hàng, các phòng tại nhà hàng được đưa vào quản lý chi tiết trên hệ thống foodNowDanh mục bàn
Chi tiết các bàn tại nhà hàng, các bàn nằm trong các phòng khác nhau

Nếu nhà hàng chỉ có 1 phòng thì chỉ cần tạo 1 phòng chung
Món ănQuản lý danh sách món ăn tại nhà hàng, các món ăn sẽ có nhiều size khác nhau, mỗi size sẽ có 1 giá khác nhauSizeTypeQuản lý danh sách các size của món ăn, các món ăn sẽ có nhiều size khác nhau, mỗi size sẽ có 1 giá khác nhauGiá món ănChi tiết giá của từng món ăn tại nhà hàng, món ăn được thiết lập theo size nếu món ăn có nhiều sizeCombo món ănCho phép nhà hàng tạo combo món ăn để khuyến mại cho KH, trong combo món ăn sẽ quản lý được tổng giá món ăn riêng lẻ và giá của combo, tỷ lê giảm giá khi ăn theo comboMón ăn trong comboLà chi tiết các món ăn trong comboKhách hàngLà thông tin chi tiết của KH thực hiện đặt bàn ăn uống tại nhà hàng, quản lý điểm KH được tích hiện tại của KH, phân hạng KHĐặt bànChi tiết thông tin đặt bàn của KH qua các kênh như qua điện thoại, qua pasgo hoặc đến trực tiếp tại nhà hàngChi tiết bànMỗi lần đặt bàn sẽ có nhiều bàn khác nhau, thực thể này sẽ quản lý lần đặt bàn đó của KH sẽ đặt ngồi bao nhiêu bàn và cụ thể là bàn nàoĐặt mónChi tiết món ăn mà KH đặt món, quản lý chi tiết trạng thái của món ăn đó VoucherQuản lý danh sách voucher áp dụng tại nhà hàng, voucher có thể áp dụng cho toàn bộ KH hoặc áp dụng cho 1 số KH cụ thể, voucher sẽ áp dụng theo đơn hàng với giá trị đơn hàng tối thiểu thỏa mãn điều kiệnVoucher-KHThông tin chi tiết quản lý voucher theo từng KH và biết được KH được nhận voucher lúc nào, đã sử dụng chưa, sử dụng cho lần ăn nào, tổng giá trị KM áp dụng là bao nhiêuLịch sử tích điểmChi tiết lịch sử tich điểm của KHCông thức tích điểmQuản lý công thức để tích điểm cho KHDanh mục phân hạng KHQuản lý danh mục phân hạng KH, cho phép nhà hàng chủ động đưa ra các hạng của nhà hàng, các quy định liên quan tới việc phân hạng nhà hàng như mức tiêu dùng/điểm bao nhiêu trong 1 tháng, quý, năm thì tương ứng hạng nào

**Tên thực thể****Ý nghĩa**Nhà hàng
Quản lý danh sách nhà hàng sử dụng dịch vụ phần mềm FoodNow

Chi tiết thuộc tính xem ở phần trên
Gói sản phẩm
FoodNow đưa ra các gói sản phẩm để cho KH lựa chọn sử dụng

Gói SP sẽ có chứa nhiều tính năng, mỗi nhóm tính năng sẽ có nhiều quyền hạn trong đó nhưg tính năng quản lý đặt bàn: Đặt bàn, xem chi tiết thông tin bàn, Hủy bàn, đổi bàn…
Gói SP – Nhà hàngQuản lý lịch sử dụng gói sản phẩm của nhà hàngỨng dụng triển khai – nhà hàngQuản lý các ứng dụng mà nhà hàng lựa chọn triển khaiTính năngTạo ra các nhóm tính năng trên foodNow để sau đó tạo thành các gói sản phẩm cho nhà hàng lựa chọnPermissionChi tiết danh sách các quyền hạn trên foodNow, có 2 nhóm permission: Nhóm cho nội bộ foodNow và nhóm cho nhà hàngGói sản phẩm – Tính năngQuản lý các tính năng cho phép của gói sản phẩm đóTính năng – PermissionQuản lý các quyền thao tác trên tính năng đóLoại ứng dụngQuản lý các loại ứng dụng triển khai cho nhà hàng, hệ thống sẽ quy định giá sử dụng trên từng loại ứng dụng đó, ví dụ như ứng dụng Web quản lý nhà hàng, Mobile app Phục vụ, KDS…Giá gói sản phẩmQuản lý mức giá của gói sản phẩm, giá gói sẽ phụ thuộc vào gói, số lượng tài khoản sử dụng và kênh triển khaiConfigFoodNowQuản lý các tham số cấu hình linh động của foodNow như: thời hạn cảnh báo nhà hàng quá hạn, thời hạn tổng hợp tạo yêu cầu thanh toán…ListParameterConfig Nhà hàngQuản lý các tham số cần các nhà hàng config cho chính nhà hàng của mình, ví dụ như thời gian hoạt động, thời gian phục vụ trung bình, ca làm việcConfig nhà hàngChi tiết config của nhà hàng theo các tham số yêu cầu trong ListParameterConfig Nhà hàngKỳ hạnQuản lý các nhóm kỳ hạn trên hệ thống để phục vụ cho quy định giá gói sản phẩm, và để KH lựa chọn kỳ hạn phù hợpĐối tác tích hợpQuản lý các đối tác mà foodNow đang hỗ trợ tích hợp, ví dụ như đối tác thanh toán, đối tác đặt bànNhà hàng- Đối tácQuản lý xem các nhà hàng liên kết với những đối tác nào để hỗ trợ đăt bàn, thanh toánMapping Tham số giao tiếpQuản lý tham số thông tin của nhà hàng khi giao tiếp với các đối tácBiểu phí đối tácQuản lý mức phí mà đối tác thu nhà hàng khi kết nốiUser nhà hàngQuản lý danh sách user của các nhà hàngRole nhà hàngCho phép nhà hàng quản lý role của nhà hàng, ngoài các role do FoodNow tạo sẵnUser-Role nhà hàngQuản lý role của các user của nhà hàngRole nhà hàng-PermissionQuản lý chi tiết permission trong từng role của nhà hàngTài khoản liên kết nhà hàngQuản lý tài khoản liên kết thanh toán của nhà hàng, hỗ trợ việc gia hạn tự động khi đến kỳ hạn mớiYêu cầu thanh toánQuản lý yêu cầu thanh toán khi đến kỳ thanh toán của nhà hàngGiao dịch charge phíQuản lý lịch sử charge phí của nhà hàng
 

## **Biểu đồ trạng thái**

- **Biểu đồ trạng thái của thực thể đặt bàn**

 

- **Biểu đồ trạng thái thực thể Đặt món**

## **Biểu đồ phân rã chức năng**

 

Danh sách các phân hệ của hệ thống

**STT****Kênh thực hiện****Actor****Mô tả chức năg**1Mobile App phục vụNV phục vụ tại nhà hàngCho phép NV PV thực hiện các nghiệp vụ trong lúc phục vụ tại nhà hàng như Đặt chỗ (cho KH đến trực tiếp), Đặt món, Kiểm đồ,…2Web Quản lý nhà hàngNV nhà hàngCho phép NV nhà hàng có thể quản lý, theo dõi được các hoạt động của nhà hàng, hệ thống thực hiện phân quyền cho từng đối tượng trong nhà hàng để thực hiện các nghiệp vụ liên quan3Web adminNV FoodNowCho phép NV FoodNow có thể thực hiện các nghiệp vụ như quản lý hợp đồng, tài khoản của các nhà hàng, theo dõi số liệu báo cáo tài chính, công nợ… của các nhà hàng4API Hệ thống cung cấp các API để tích hợp với các bên đặt chỗ như Pasgo hoặc tiếp nhận kết quả thanh toán từ các cổng thanh toán như Momo, Vnpay,ViettelPay…5Tiến trình Cung cấp các tiến trình xử lý ngầm trên hệ thống
## **9.1.Danh sách chức năng Mobile app NV Phục vụ**

 
**STT****Chức năng****Ý nghĩa**1Đăng nhậpCho phép NV PV đăng nhập vào mobile app Phục vụ để thực hiện các nghiệp vụ của mình2Xem thông tin cá nhânCho phép NVPV xem thông tin cá nhân của mình3Đổi mật khẩuCho phép NVPV đổi mật khẩu lúc có nhu cầu để đảm bảo bảo mật4Danh sách theo trạng thái bànCho phép NVPV xem trạng thái hiện tại của các bàn theo khung giờ phục vụ hiện tại của nhà hàng, để NVPV có thể nắm được hiển trạng của các bàn5Đặt bànCho phép NVPV đặt bàn cho TH KH đến trực tiếp tại nhà hàng để ăn mà chưa đặt chỗ6Thêm bànCho phép NVPV bổ sung thêm bàn trong TH có thêm người7Đổi bànCho phép NVPV đổi bàn trong TH KH có nhu cầu hoặc sắp xếp lại giữa các bàn để phù hợp hơn cho KH8Hủy bànCho phép NVPV hủy bàn trong TH KH có nhu cầu do giảm người đến ăn9Hủy đặt chỗCho  phép NVPV hủy đặt bàn trong TH KH vừa đến ngồi ăn nhưng lại quyết định không ăn nữa10Xem chi tiết đặt bànCho phép NVPV xem thông tin chi tiết của yêu cầu đặt bàn tương ứng11Đặt mónCho phép NVPV đặt món cho bàn ăn của KH12Hủy mónCho phép NVPV Hủy món khi KH không có nhu cầu và chỉ được phép hủy món trong 1 thời gian nhất định (Ví dụ trong 5ph kể từ lúc đặt)13Yêu cầu thanh toánCho phép NVPV xác nhận KH đã okie với thông tin đồ ăn, để có thể tiếp tục thanh toán cho đơn hàng14In kiểm đồCho phép NVPV in menu kiểm đồ để KH có thể kiểm soát lại thông tin và chốt thông tin đồ ăn đã khớp đúng để chuẩn bị thanh toán15Tạo QR thanh toánCho phép NVPV tạo QR thanh toán khi KH chọn hình thức thanh toán QR qua các bên như Momo, VNpay, ViettelPay16Danh sách bàn chưa tớiLà danh sách các bàn mà KH đặt cho khung thời gian hiện tại nhưng chưa tới (Ví dụ buổi trưa thì chỉ nhìn vào các bàn đặt vào khung buổi trưa17Danh sách bàn đang phục vụLà các bàn đang ăn tại nhà hàng và đang được phục vụ18Danh sách đặt bànCho phép NV PV xem danh sách các bàn đã đặt ở trong quá khứ, hiện tại và trong thời gian ở tương lai
## **9.2.Danh sách chức năng Web Quản lý nhà hàng**

**STT****Actor****Chức năng****Ý nghĩa**1NV nhà hàngDashboard thu ngânLà dashboard dành cho nhân viên thu ngân hay các nhân viên khác trong nhà hàng, để theo dõi thông tin trong ngày hiện tai ở nhà hàng như về số lượng đặt chỗ theo trạng thái, danh sách các bàn chuẩn bị thanh toán, danh sách các giao dịch vừa thanh toán2Quản lý nhà hàngDashboard quản lý nhà hàngLà dashboard dành cho Quản lý nhà hàng có thể xem để đánh giá hoạt động chung của nhà hàng trong 30 ngày qua, ngày hiện tại như doanh thu, tổng số lượng KH, thời gian phục vụ bàn trung bình…3NV nhà hàngĐặt bànCho phép NV nhà hàng có thể đặt bàn trước cho KH khi KH có nhu cầu4NV nhà hàngChỉnh sửa thông tin đặt bàn
Cho phép NV nhà hàng chỉnh sửa thông tin đặt bàn khi KH có nhu cầu thay đổi 

Thông tin đặt bàn chỉ chỉnh sửa khi trạng thái chưa thanh toán
5NV nhà hàngHủy đặt bànCho phép NV nhà hàng hủy thông tin đặt bàn của KH khi KH không có nhu cầu tới nhà hàng nữa6NV nhà hàngXem chi tiết đặt bànCho phép NV nhà hàng xem chi tiết thông tin đặt bàn  NV nhà hàngThêm bànCho phép NV nhà hàng thêm bàn khi KH có nhu cầu thêm người7NV nhà hàngĐổi bànCho phép NV nhà hàng đổi bàn trong TH KH có nhu cầu hoặc sắp xếp lại giữa các bàn để phù hợp hơn cho KH8NV nhà hàngHủy bànCho phép NV nhà hàng hủy bàn trong TH KH có nhu cầu do giảm người đến ăn9NV nhà hàngĐặt mónCho  phép NV nhà hàng đặt món cho KH, có thể đặt món trước hoặc đặt món cho KH đến tại nhà hàng trong TH nhà hàng không sử dụng mobile app cho NV phục vụ10NV nhà hàngChỉnh sửa thông tin đặt mónCho phép NV nhà hàng chỉnh sửa lại thông tin đặt món khi KH có nhu cầu thay đổi11Kế toán/Thu ngân/QL nhà hàngDanh sách voucherDanh sách voucher nhà hàng áp dụng cho Kh12Kế toán/Thu ngân/QL nhà hàngTạo voucher đơn lẻCho phép Actor tạo voucher để áp dụng cho nhà hàng 13Kế toán/Thu ngân/QL nhà hàngImport voucherCho phép Actor tạo voucher bằng cách import danh sách để áp dụng cho nhà hàng14Kế toán/Thu ngân/QL nhà hàngXem chi tiết voucherCho phép Actor xem chi tiết thông tin voucher phục vụ tại nhà hàng15Kế toán/Thu ngân/QL nhà hàngChỉnh sửa voucherCho phép Actor chỉnh sửa thông tin voucher khi có nhu cầu thay đổi16Kế toán/Thu ngân/QL nhà hàngXóa voucherCho phép Actor xóa thông tin voucher khi tạo sai thông tin17NV nhà hàngDanh sách phân ca làm việcCho phép NV nhà hàng nhìn thấy danh sách ca làm việc đã được bố trí ở nhà hàng18NV nhà hàngChi tiết ca làm việcCho phép NV nhà hàng xem chi tiết phân ca làm việc của nhà hàng19Quản lý nhà hàngPhân ca làm việc đơn lẻCho phép QL nhà hàng phân ca làm việc hàng tuần/tháng cho NV nhà hàng20Quản lý nhà hàngImport phân ca làm việcCho phép QL nhà hàng phân ca làm việc bằng cách import excel vào hệ thống21Quản lý nhà hàngĐổi ca làm việcCho phép QL nhà hàng hỗ trợ đổi ca cho các nhân viên khi có nhu cầu22Quản lý nhà hàngHủy ca làm việcCho phép QL nhà hàng Hủy ca làm việc đã phân khi thông tin không phù hợp nữa23Quản lý nhà hàngDanh mục bànCho Phép QL Nhà hàng CRUD Bàn và Xem danh sách bàn đang có trên hệ thống của nhà hàng23Quản lý nhà hàngDanh mục phòng/khu vực phục vụCho phép QL nhà hàng CRUD Phòng/khu vực phục vụ và Xem danh sách Phòng/khu vực phục vụ đang có trên hệ thống của nhà hàng24Quản lý nhà hàngDanh mục món ănCho Phép QL Nhà hàng CRUD Món ăn và Xem danh sách Món ăn đang có trên hệ thống của nhà hàng25Quản lý nhà hàngDanh mục comboCho Phép QL Nhà hàng CRUD combo Món ăn và Xem danh sách Món ăn đang có trên hệ thống của nhà hàng26Quản lý nhà hàngDanh mục nhân viên/UserCho Phép QL Nhà hàng CRUD nhân viên và Xem danh sách nhân viên của nhà hàng đang có trên hệ thống của nhà hàng27Quản lý nhà hàng**Danh mục bộ phận**Cho Phép QL Nhà hàng CRUD Bộ phận  (Kho, bếp, Phục vụ..)của nhà hàng và Xem danh sách Bộ phận của nhà hàng đang có trên hệ thống của nhà hàng28Quản lý nhà hàng**Quản lý vai trò**Cho Phép QL Nhà hàng CRUD Vai trò và Xem danh sách Vai trò đang có trên hệ thống của nhà hàng, để hỗ trợ việc phân quyền linh động trong nhà hàng29Quản lý nhà hàng**Gán/Bỏ gán user vào role**Cho phép QL NH gán/bỏ gán user vào role nào đó để hỗ trợ phân quyền linh động cho từng user trong nhà hàng NV nhà hàng**Đăng nhập**Cho phép NV nhà hàng đăng nhập vào web Quản lý nhà hàng để thực hiện các nghiệp vụ liên quan30NV nhà hàng**Đổi mật khẩu**Cho phép NV nhà hàng đổi mật khẩu khi có nhu cầu 31Quản lý nhà hàng**Cấu hình thời gian phục vụ trung bình/bàn**Cho phép QL nhà hàng cấu hình thời gian phục vụ trung bình/bàn để ước tính được thời gian KH sử dụng dịch vụ tại nhà hàng, hỗ trợ việc đặt bàn theo thời gian trống 1 cách thuận tiện nhất32Quản lý nhà hàng**Cấu hình khung thời gian phục vụ**Cho phép QL nhà hàng cấu hình khung thời gian phục vụ tại nhà hàng, vì có nhà hàng phục vụ sáng/trưa/tối hoặc cả ngày33Quản lý nhà hàng**Cấu hình ca làm việc**Cho phép QL nhà hàng cấu hình ca làm việc thì phục vụ cho việc Phân ca làm việc34Quản lý nhà hàng**Liên kết tài khoản thanh toán**Cho phép QL nhà hàng liên kết tài khoản để hỗ trợ gia hạn tự động khi đến kỳ thanh toán34Quản lý nhà hàng**Hủy liên kết tài khoản thanh toán**Cho phép QL nhà hàng hủy liên kết tài khoản khi không sử dụng tài khoản đó nữa35Quản lý nhà hàng**Danh sách tài khoản liên kết**Cho phép QL nhà hàng xem danh sách tài khoản đã liên kết 36Quản lý nhà hàng**Xem thông tin chi tiết tài khoản liên kết**Cho phép QL nhà hàng xem chi tiết tài khoản đã liên kết37Quản lý nhà hàng**Thiết lập tài khoản mặc định**Cho phép QL nhà hàng thiết lập tài khoản mặc định để hệ thống tự động trừ tiền trên tài khoản đó38 **Quản lý kết nối đối tác thanh toán**Cho phép QL nhà hàng thiết lập chọn đối tác thanh toán sẽ hỗ trợ tại nhà hàng trong danh sách các đối tác thanh toán mà FoodNow đã kết nối39 **Quản lý kết nối đối tác đặt chỗ**Cho phép QL nhà hàng thiết lập chọn đối tác đặt chỗ sẽ hỗ trợ tại nhà hàng trong danh sách các đối tác đặt chỗ mà FoodNow đã kết nối40Quản lý nhà hàng**Thiết lập menu nhà hàng**
Cho phép QL nhà hàng thiết lập menu nhà hàng theo ngày, buổi

Thông tin món ăn hiển thị cho KH hoặc NV phục vụ sẽ dựa vào thiết lập này của nhà hàng
41Quản lý nhà hàng**Thiết lập các món ăn yêu thích**Cho phép QL nhà hàng thiết lập các món ăn được yêu thích hoặc nhà hàng muốn đẩy món ăn đó lên để KH sử dụng42Quản lý nhà hàng**Báo cáo tổng hợp doanh thu tuần/tháng/quý/năm**Cho phép QL nhà hàng theo dõi được doanh thu theo thời gian mong muốn43Quản lý nhà hàng**Báo cáo tổng hợp thực đơn**Cho phép QL nhà hàng theo dõi được các món ăn được sử dụng nhiều tại nhà hàng 44Quản lý nhà hàng**Báo cáo tổng hợp đặt bàn  theo trạng thái**Cho phép QL nhà hàng theo dõi được tình hình đặt bàn tại nhà hàng theo trạng thái trong khoảng thời gian mong muốn45Quản lý nhà hàng**Báo cáo thời gian phục vụ trung bình**Cho phép QL nhà hàng theo dõi được thời gian phục vụ trung bình của 1 bàn theo từng ngày để từ đó có thông tin điều chỉnh lại tham số thời gian phục vụ trung bình/bàn46Quản lý nhà hàng**Báo cáo chi tiết doanh thu**Cho phép QL nhà hàng theo dõi được chi tiết doanh thu của nhà hàng47Quản lý nhà hàng**Báo cáo chi tiết thực đơn**Cho phép QL nhà hàng theo dõi được chi tiết thực đơn của nhà hàng, số lượng sử dụng trên từng món ăn theo khoảng thời gian báo cáo
 

## **9.3.Danh sách chức năng Web admin**

STTActorChức năngÝ nghĩa1NV FoodNowDashboardCho phép actor xem thông tin chung về tình hình kinh doanh sản phẩm quản lý nhà hàng2NV FoodNowDanh sách nhà hàngCho phép Actor có thể xem danh sách nhà hàng đang/đã kết nối sử dụng hệ thống FoodNow, có thể tìm kiếm theo đầu vào hỗ trợ3NV SaleThêm mới nhà hàngCho phép NV sale thêm mới nhà hàng, trong đó có chi tiết về nhà hàng và HĐ ký kết với nhà hàng4NV SaleChỉnh sửa thông tin nhà hàngCho phép NV sale chỉnh sửa lại thông tin nếu thông tin nhà hàng thay đổi hoặc thông tin nhập vào trước đó bị sai5NV SaleXem chi tiết nhà hàngCho phép NV Sale xem thông tin chi tiết về nhà hàng 6NV SaleMở khóa/Khóa nhà hàngCho phép nv sale mở khóa/Khóa nhà hàng khi có nhu cầu7NV SaleĐóng nhà hàngCho phép NV sale Đóng hợp đồng với nhà hàng khi nhà hàng không có nhu cầu sử dụng Phần mềm foodNow nữa8NV SaleThiết lập gói sản phẩm cho nhà hàngCho phép NV Sale thiết lập gói mà Nhà hàng mong muốn sử dụng9NV SaleChuyển đổi gói sản phẩmCho phép NV sale chuyển đổi gói theo nhu cầu của nhà hàng10NV SaleDanh sách user nhà hàngCho phép NV sale theo dõi danh sách user nhà hàng đã/đang được sử dụng trên hệ thống FoodNow11NV SaleTạo mới user nhà hàngCho phép NV sale tạo tài khoản cho nhà hàng để sử dụng dịch vụ, sau khi tạo Tài khoản xong thì nhà hàng sẽ chủ động tạo các tài khoản sử dụng trên phần mềm web quản lý nhà hàng và mobile app phục vụ12NV SaleChỉnh sửa thông tin userCho phép Cho phép NV sale chỉnh sửa thông tin user nhà hàng khi có nhu cầu13NV Salexem chi tiết userCho phép Cho phép NV sale xem chi tiết thông tin user nhà hàng khi có nhu cầu14NV SaleKhóa/mở khóa userCho phép NV sale Khóa/mở khóa user nhà hàng khi có nhu cầu15NV SaleĐóng userCho phép NV sale Đóng tài khoản user nhà hàng khi có nhu cầu16NV Salereset mật khẩuCho phép NV sale reset mật khẩu cho tài khoản user nhà hàng khi có nhu cầu17AdminDanh sách user FoodNow Cho phép Admin theo dõi danh sách user foodNow đã/đang được sử dụng trên hệ thống18AdminTạo mới user foodNowCho phép Admin tạo tài khoản NV foodNow để sử dụng dịch vụ AdminChỉnh sửa thông tin user foodNowCho phép Admin chỉnh sửa thông tin user foodNow khi có nhu cầu Adminxem chi tiết user foodNowCho phép Admin xem chi tiết thông tin user foodNow khi có nhu cầu AdminKhóa/mở khóa user FoodnowCho phép Admin Khóa/mở khóa user foodNow khi có nhu cầu AdminĐóng user foodNowCho phép Admin Đóng tài khoản user foodNow khi có nhu cầu NV FoodNowĐăng nhậpCho phép NV Foodnow đăng nhập vào hệ thống để thực hiện các nghiệp vụ liên quan NV FoodNowĐổi mật khẩuCho phép NV Foodnow đổi mật khẩu khi có nhu cầu Adminreset mật khẩuCho phép Admin reset mật khẩu tài khoản user nhà hàng khi có nhu cầu AdminQuản lý role (CRUD Danh sách role)Cho phép Admin quản lý role để phục vụ việc phân quyền, với các nhóm user có quyền giống nhau sẽ tạo ra 1 role tương ứng với nhóm đó AdminQuản lý permission (CRUD Danh sách Permission)Cho phép Admin quản lý permission để phục vụ việc phân quyền, mỗi permission sẽ tương ứng với 1 quyền thao tác trên hệ thống như đặt bàn, đặt món, thanh toán… AdminGán permission vào roleCho phép gán permission cụ thể vào các role để phục vụ phân quyền AdminGán user vào roleSau khi gán permission vào role, Admin sẽ gán user vào role tương ứng để cấp quyền hạn sử dụng cho các user đó trên hệ thống NV saleDanh sách gói sản phẩmCho phép NV sale xem danh sách gói sản phẩm đã/đang hoạt động trên hệ thống NV saleTạo gói sản phẩmCho phép NV sale tạo ra các gói sản phẩm để chào bán nhà hàng NV saleChỉnh sửa gói sản phẩmCho phép NV sale chỉnh sửa gói sản phẩm khi có nhu cầu NV saleDừng hoạt động gói sản phẩmCho phép NV sale Dừng gói sản phẩm khi có nhu cầu NV saleXem chi tiết gói sản phẩmCho phép NV sale Xem chi tiết gói sản phẩm khi có nhu cầu NV saleQuản lý giá gói sản phẩmCho phép NV sale Quản lý giá (Thiết lập, thay đổi giá) gói sản phẩm khi có nhu cầu NV saleThiết lập tính năng của sản phẩmCho phép NV sale thiết lập các tính năng có trên gói sản phẩm tương ứng NV saleXóa tính năng trong gói sản phẩmCho phép NV sale xóa các tính năng có trên gói sản phẩm tương ứng khi không có nhu cầu NV saleDanh sách tính năng sản phẩmCho phép admin xem danh sách tính năng sản phẩm AdminTạo tính năng sản phẩmCho phép admin tạo ra các tính năng trên sản phẩm, mỗi tính năng có thể chứa nhiều quyền (permission) khác nhau AdminXem chi tiết tính năng sản phẩmCho phép admin xem chi tiết tính năng sản phẩm AdminChỉnh sửa tính năng sản phẩmCho phép admin chỉnh sửa tính năng sản phẩm khi có nhu cầu AdminXóa tính năng sản phẩmCho phép admin xóa tính năng sản phẩm khi có nhu cầu Kế toánLịch sử thanh toánCho phép kế toán  xem danh sách lịch sử thanh toán của các nhà hàng để sử dụng dịch vụ nhà hàng   Kế toánXem chi tiết thông tin thanh toánCho phép kế toán xem chi tiết thông tin thanh toán   Kế toánDanh sách chờ thanh toánCho phép kế toán  xem danh sách đang chờ thanh toán   Kế toánXem chi tiết thông tin chờ thanh toánCho phép kế toán  xem chi tiết yêu cầu chờ thanh toán   Kế toánXác nhận thanh toánCho phép kế toán xác nhận thanh toán khi nhà hàng thực hiện thanh toán qua hình thức chuyển khoản  Kế toánHủy xác nhận thanh toánCho phép kế toán hủy xác nhận thanh toán khi xác nhận nhầm, tuy nhiên chỉ được hủy trong thời gian quy định (ví dụ như trong 1 tuần kể từ ngày xác nhận) Kế toánQuản lý đối tác tích hợp thanh toánCho phép admin quản lý đối tác tích hợp thanh toán để hỗ trợ nhà hàng liên kết thanh toán với các đối tác đó AdminQuản lý đối tác tích hợp đặt bànCho phép admin quản lý đối tác tích hợp đặt bàn để hỗ trợ nhà hàng liên kết đặt bàn với các đối tác đó AdminQuản lý biểu phí thanh toán cho đối tácCho phép admin cấu hình biểu phí thanh toán đối với các đối tác thanh toán/Đặt bàn NV Sale/BGĐ/Kế toánBáo cáo tổng hợp doanh thuCho phép NV Sale/BGĐ/Kế toán có thể theo dõi được báo cáo doanh thu từ việc kinh doanh sản phẩm FoodNow NV Sale/BGĐ/Kế toánBáo cáo công nợCho phép NV Sale/BGĐ/Kế toán có thể theo dõi được báo cáo công nợ của các nhà hàng  NV Sale/BGĐ/Kế toánBáo cáo tổng hợp tài khoản nhà hàng theo trạng tháiCho phép NV Sale/BGĐ/Kế toán có thể theo dõi được thông tin tổng hợp tài khoản các nhà hàng đang sử dụng theo trạng thái NV Sale/BGĐ/Kế toánBáo cáo nhà hàng theo gói sản phẩmCho phép NV Sale/BGĐ/Kế toán có thể theo dõi thông tin tổng hợp số lượng nhà hàng sử dụng theo từng gói sản phẩm NV Sale/BGĐ/Kế toánbáo cáo chi tiết doanh thuCho phép NV Sale/BGĐ/Kế toán có thể theo dõi thông tin chi tiết liên quan tới doanh thu nhà hàng NV Sale/BGĐ/Kế toánBáo cáo chi tiết tài khoản nhà hàng theo trạng tháiCho phép NV Sale/BGĐ/Kế toán có thể theo dõi được thông tin tài khoản các nhà hàng đang sử dụng theo trạng thái
 

 

## **9.4.Danh sách API**

**STT****Chức năng****Ý nghĩa**1API lấy danh sách bàn trốngCung cấp API trả về danh sách các bàn trống theo khung thời gian mà KH chọn cho các bên đặt chỗ như pasgo, để KH có thể lựa chọn bàn sử dụng2API đặt bànCung cấp API đặt chỗ cho các bên đặt bàn như Pasgo3API cập nhật kết quả thanh toánCung cấp API để bên cổng thanh toán có thể gửi thông tin kết quả thanh toán về cho hệ thống quản lý nhà hàng, giúp hệ thống quản lý nhà hàng cập nhật thông tin hiển thị cho NV nhà hàng
 

## **9.5.Danh sách Tiến trình**

**STT****Chức năng****Ý nghĩa**1Tiến trình nhắc nhà hàng thanh toánTiến trình thực hiện nhắc nhà hàng thanh toán để gia hạn tiếp tài khoản cho các tháng tiếp theo2Tiến trình khóa nhà hàng/tài khoản nhà hàngTiến trình thực hiện khóa tài khoản nhà hàng khi nhà hàng không thực hiện thanh toán3Tiến trình charge tiền phí sử dụngTiến trình thực hiện charge tiền phí sử dụng khi sang kỳ mới của nhà hàng4Tiến trình hủy đặt bànTiến trình hủy đặt bàn khi KH không tới quá X(ph) so với giờ hẹn