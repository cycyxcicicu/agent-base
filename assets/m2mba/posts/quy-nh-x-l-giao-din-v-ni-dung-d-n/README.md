---
id: 181
title: "Quy định chung về xử lý giao diện"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-06-29T13:31:43.000Z"
source_url: "https://m2mba.com/blog/articles/quy-nh-x-l-giao-din-v-ni-dung-d-n"
---

# Quy định chung về xử lý giao diện

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-06-29T13:31:43.000Z*

Với phần mô tả giao diện, thay vì chúng ta cứ phải lặp đi lặp lại những mô tả, quy định giống nhau thì BA có thể tạo thành 1 file chuẩn quy định chung trong dự án để các bạn dev tuân thủ - tạo nên sự đồng nhất trong xử lý giao diện giữa các dev và các BA với nhau(nếu team có nhiều BA)

Dưới dây là ví dụ về quy định chung về phần xử lý giao diện, các bạn BA có thể tham khảo để áp dụng cho dự án của mình
**Loại control****Item****Ràng buộc**

 Tất cả controlValidate dữ liệuDữ liệu sẽ được validate và báo lỗi ngay dưới control ngay sau khi thoát khỏi controlButtonValidate dữ liệuDữ liệu trước khi gửi lên server sẽ cần validate dữ liệuPopup thông báo lỗi/Gd thất bạiPopup thông báo lỗi
Theo mô tả của SRS, nếu không có thì hiển thị theo dạng sau, chi tiết nội dung thông báo sẽ mô tả trong SRS hoặc trong quy định từng control cụ thể bên dưới

 

 

 
Popup confirmPopup confirm
Theo mô tả của SRS, chi tiết nội dung câu confirm sẽ nêu cụ thể trong từng chức năng, nếu không có thì hiển thị theo dạng sau,

Popup thông báo GD thành côngPopup thông báo GD thành côngTheo mô tả của SRS, nếu không có thì hiển thị theo dạng sau, chi tiết nội dung thông báo sẽ mô tả trong SRS hoặc trong quy định từng control cụ thể bên dưới
TextboxTrim dữ liệuTrim space đầu cuối khi lưu và kiểm tra dữ liệuMax lengthKhông cho phép nhập quá max length từ key board, nếu copy paste thì tự động cut luônBắt buộc nhập
- Label các trường bắt buộc có dấu * đỏ
- Nếu không nhập thì hiển thị thông báo lỗi: <**Tên control trong phần mô tả màn hình**> không được để trống
- Ví dụ: **Họ tên không được để trống**Ràng buộc ký tự nhậpNếu dữ liệu tương ứng với trường textbox có yêu cầu: Chỉ nhập số, hoặc chữ thì web cần chặn không cho người dùng nhập các kí tự khác ngoài aA-zZ, 0-9Ràng buộc format dữ liệuQuy định theo SRS (nếu có) hoặc mặc định tham khảo chi tiết từng loại dữ liệu bên dướiComboboxNhập dữ liệuChỉ cho phép chọn dữ liệu từ danh sách và chỉ chọn được 1 dòng dữ liệugridCăn lề-Tiêu đề cột: Căn giữa
- Cột dữ liệu là text: căn trái
- Cột dữ liệu số, ngày tháng: căn giữa
- Cột dữ liệu tiền, phần trăm: Căn phải
- Cột dữ liệu là file: Căn trái, cho phép click vào để tải vềNgày thángKiểu nhập liệu
Thực hiện 1 trong 2 cách:

- Cho phép nhập: Nếu nhập sai định dạng thì tự động fill về ngày 1/1/1970
- Cho phép chọn từ datepicker. Show calendar khi click vào iconFormat ngày tháng
- Nếu không hiển thị giờ: DD/MM/YYYY
- Nếu hiển thị giờ: DD/MM/YYYY HH:MM24:SSTừ ngày, Đến ngày
Thứ tự kiểm tra như sau

- 1: Từ ngày<=Ngày hiện tại. Nếu không thỏa mãn thì báo lỗi:  **<Tên control ở màn hình> không được vượt quá ngày hiện tại**
- 2: Đến ngày<=Ngày hiện tại. Nếu không thỏa mãn thì báo lỗi> Nếu không thỏa mãn thì báo lỗi:  **<Tên control ở màn hình> không được vượt quá ngày hiện tại**
- 3: Từ ngày<=Đến ngày. Nếu không thỏa mãn thì báo lỗi:  **<Tên control ở màn hình tương ứng với Từ ngày> không được vượt quá <Tên control ở màn hình tương ứng với Đến ngày>****Format số tiền**Đơn vị tiền tệVNĐFormat nhập
- Chỉ cho phép nhập số và dấu "." (dấu "." dùng để phân cách phần thập phân)
- Tự động phân cách dấu hàng nghìn khi nhậpFormat hiển thị
- Phân cách dấu hàng nghìn bằng dấu ","
- Dấu thập phân bằng dấu "."Format sốFormat nhập
- Chỉ cho phép nhập số và dấu "." (dấu "." dùng để phân cách phần thập phân)
- Tự động phân cách dấu hàng nghìn khi nhậpFormat hiển thị
- Phân cách dấu hàng nghìn bằng dấu ","
- Dấu thập phân bằng dấu "."Ảnh/logo mặc địnhẢnh/logo mặc địnhCác trường hợp cần show ảnh nhưng chưa có ảnh thì sẽ hiển thị ảnh mặc định
Design: UpdatingFile uploadĐịnh dạng
Định dạng file cụ thể sẽ nêu ở từng chức năng .

- Nếu chọn sai định dạng file thì báo lỗi: **Định dạng File <Tên control ở mô tả màn hình> bắt buộc là <ds các định dạng cho phép>****Dung lượng**
Sẽ quy định ở đặc tả yêu cầu chức năng, nếu không có thì mặc định là 5MB

- Nếu chọn file quá dung lượng cho phép thì báo lỗi: **Dung lượng file <Tên control ở mô tả màn hình> không vượt quá <dung lượng cho phép>****Quy định về format Email**Format email hợp lệ: [example@mail.com](mailto:example@mail.com), trong đó:
•  Example (phần trước @) là tiền tố
•  [Mail.com](http://mail.com) (phần sau @) là email domain.
•  Tiền tố email được phép bao gồm:
o  Các ký tự: Chữ cái (a-z), số, dấu gạch dưới, dấu chấm và dấu gạch ngang.
o   Sau mỗi dấu gạch dưới, dấu chấm hoặc dấu gạch ngang phải phải có ít nhất 1 ký tự chữ hoặc số
•  Định dạng tên miền email được chấp nhận:
o   Ký tự được phép: chữ cái, số, dấu gạch ngang, có ít nhất 1 dấu chấm (.)
o  Phần cuối cùng của tên miền phải có ít nhất hai ký tự

Nếu Email không đúng yêu cầu thì thông báo lỗi:** Email không đúng định dạng**Số điện thoạiFormat nhập
- Chỉ nhập số
- Bắt đầu bằng 0 hoặc 84 và tối đa 13 ký tự số
nếu nhập sai format thì thông báo lỗi: **Số điện thoại không đúng định dạng**
Địa chỉFormat địa chỉFormat nhập: Chọn Tỉnh/ thành phố, Quận/ huyện, phường/ xã từ list, nhập tòa nhà tên đường => Tất cả đều bắt buộc nhập
- Tỉnh/ thành phố: ví dụ Hà Nội, Quảng Ninh...
- Quận/ huyện: Chỉ enable khi đã chọn tỉnh, thành phố, giới hạn theo Tỉnh/ thành phố đã chọn, ghi rõ là Huyện hay Quận, ví dụ Quận Cầu Giấy
- Phường/ Xã: Chỉ enable khi đã chọn tỉnh, thành phố, giới hạn theo Quận/ Huyện đã chọn, ghi rõ là Phường hay Xã, ví dụ Phường Mai Dịch
- Tòa nhà, tên đường: Nhập text
Format hiển thị: Ghép các thông tin nhập và hiển thị dạng
Tòa nhà tên đường, phường/xã, quận/ huyện, tỉnh/ thành phố
Vi dụ: Tòa nhà Sudico, Phường Mễ Trì, Quận Nam từ liêm, Hà NộiTìm kiếm dữ liệuQuy định về việc tìm kiếm dữ liệu
Cụ thể sẽ nêu trong đặc tả chức năng, nếu không nêu thì theo điều kiện mặc định ở đây

-  AND/OR: Tìm kiếm theo điều kiện AND các tiêu chí
- Textbox:Không phân biệt hoa thường, Tìm kiếm theo điều kiện LIKE
- Combobox: Tìm kiếm chính xác
- Từ ngày, Đến ngày: Từ ngày<= AND <Đến ngày +1
- Khoảng thời gian tìm kiếm: Tối đa 31 ngày