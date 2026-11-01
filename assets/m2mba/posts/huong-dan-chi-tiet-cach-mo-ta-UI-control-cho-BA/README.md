---
id: 173
title: "Hướng dẫn mô tả màn hình với từng loại control"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-06-25T12:38:41.000Z"
source_url: "https://m2mba.com/blog/articles/huong-dan-chi-tiet-cach-mo-ta-UI-control-cho-BA"
---

# Hướng dẫn mô tả màn hình với từng loại control

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-06-25T12:38:41.000Z*

Bài viết này hướng dẫn các bạn BA cách mô tả MH với các loại control khác nhau

## **1.Label**

Label là một loại control dùng để hiển thị văn bản tĩnh trên màn hình. Label thường không nhận tương tác trực tiếp từ người dùng (không thể nhấp vào, nhập liệu, ...).

Các control ở ảnh dưới (từ 1-4 ) là Label

**Label nào cần đánh số mô tả: **

- Chỉ đánh số mô tả với các Label sẽ có dữ liệu thay đổi tùy thuộc vào thông tin user xem, ví dụ ở ảnh trên Label: Thời lượng là label có giá trị không thay đổi, còn 1 giờ/buổi là label có giá trị thay đổi tùy thuộc vào khóa học tương ứng=>Chỉ cần đánh số mô tả thông tin 1 giờ/Buổi
- Ví dụ MH Xem chi tiết đơn hàng của Tiki bên dưới thì control đánh số 1 sẽ không cần mô tả (tức không cần đánh số mô tả cho DEV trong mô tả MH) còn control số 2 thì bắt buộc phải đánh số mô tả

**Thông tin cần mô tả đối với Label**
**Thông tin mô tả****Bắt buộc mô tả**Tên dữ liệu hiển thị là gì ví dụ Trạng thái đơn hàng hay Họ tên KH**Yes**Format hiển thị nếu có: ví dụ Hiển thị chữ Hoa, Hiển thị chữ màu đỏ ,Với trường ngày tháng thì mô tả format hiển thị dd/mm/yyyy giờ: phút : Giây**Option, nếu có yêu cầu thì mô tả**
Khi nào hiển thị Label đó, khi nào thì không hiển thị

Ví dụ trong MH danh sách các Task cần thực hiện, task nào ở mức độ ưu tiên cao sẽ hiển thị Label Urgent.  Khi đó cần đánh số và Mô tả: Chỉ hiển thị khi task có trạng thái chưa hoàn thành và mức độ ưu tiên là Cao

**Option, nếu có yêu cầu thì mô tả**
**Thông tin KHÔNG mô tả đối với Label: **

Do label chỉ sử dụng để hiển thị dữ liệu có sẵn trên hệ thống, nên không đưa ra các mô tả về quy định dạng dữ liệu nhập vào**, **Ví dụ Label hiển thị thông tin số điện thoại của KH nhưng lại mô tả: Số điện thoại bắt buộc gồm 10 ký tự số

## **2.Textbox/Text Input/Text Area**

- Textbox là một loại control trong giao diện người dùng (UI) thường được sử dụng để cho phép người dùng nhập dữ liệu văn bản. Textbox cho phép người dùng nhập và chỉnh sửa văn bản hoặc có thể hiển thị văn bản mà người dùng đã nhập hoặc mà chương trình đã thiết lập

**Textbox nào cần đánh số mô tả: **Luôn đánh số mô tả

**Thông tin cần mô tả đối với Textbox**
**Thông tin mô tả****Bắt buộc mô tả**Ý nghĩa của dữ liệu nhập vào ô textbox tương ứngYesCó bắt buộc nhập hay khôngOption, Mặc định không mô tả sẽ không bắt buộc nhập, nếu muốn bắt buộc thì cần mô tả
MaxLength

Nếu control có Length cố định thì mô tả chính xác length tương ứng, ví dụ số điện thoại phải có 10 ký tự số (tức chiều dài luôn bằng 10)
**Bắt buộc**MinLength**Option**Giá trị mặc định: Là giá trị được hiển thị trên textbox ngay khi mở MH chức năng tương ứng ra**Option**Format nhập liệu: Được phép/Không được phép nhập ký tự gì (Chỉ cần mô tả 1 trong 2)**Option**Readonly: Tức có cho phép sửa hay chỉ được phép đọc thông tin. Mặc định mọi textbox đều được sửa, nếu muốn textbox đó chỉ read Only thì mô tả là Textbox chỉ được phép readOnly**Option**
**Thông tin KHÔNG mô tả đối với Textbox: **

- Trong MH tìm kiếm, nhập dữ liệu input tìm kiếm vào textbox: Không cần mô tả rang buộc format nhập liệu hay lengh của textbox
- Trong trường hợp form MH hiển thị textbox nhưng chỉ hiển thị những dữ liệu trên hệ thống đã có,thì khi đó không đưa ra các mô tả về quy định dạng dữ liệu nhập vào**, **Ví dụ Textbox hiển thị thông tin số điện thoại của KH nhưng lại mô tả: Số điện thoại bắt buộc gồm 10 ký tự số
## **3.Combobox**

ComboBox cho phép người dùng chọn một mục từ danh sách sổ xuống hoặc nhập trực tiếp một giá trị vào hộp văn bản (mặc định chỉ chọn từ danh sách, không được nhập)

Ví dụ control combobox

**Combobox nào cần đánh số mô tả: **Luôn đánh số mô tả

**Thông tin cần mô tả đối với Combobox**
**Thông tin mô tả****Bắt buộc mô tả**Ý nghĩa của dữ liệu nhập vào ô textbox tương ứng**Bắt buộc**
Dữ liệu hiển thị trong combobox

Chia làm 2 trường hợp

- Fix cứng danh sách: BA sẽ mô tả liệt kê danh sách dữ liệu hiển thị trong combobox
- Dữ liệu load từ DB: BA sẽ mô tả “HIển thị danh sách xxx trên hệ thống”**Bắt buộc**
Dữ liệu hiển thị được sắp xếp như thế nào

Nếu có rang buộc về thứ tự dữ liệu hiển thị thì mô tả
**Option**Dữ liệu hiển thị có phụ thuộc vào dữ liệu nào khác được chọn ở trước không**Option**Có bắt buộc nhập hay khôngOption, Mặc định không mô tả sẽ không bắt buộc nhập, nếu muốn bắt buộc thì cần mô tảGiá trị mặc định: Là giá trị được hiển thị trên Combobox ngay khi mở MH chức năng tương ứng ra**Option**Có cho phép chọn nhiều hay không, mặc định là chỉ được chọn 1**Option**Có cho phép gõ vào để filter dữ liệu không, mặc định là không được filter Readonly: Tức có cho phép sửa hay chỉ được phép đọc thông tin. Mặc định mọi combobox sẽ được thay đổi giá trị được chọn, nếu muốn chỉ hiển thị, không được phép thay đổi thì cần mô tả combobox đó chỉ được readonly **Option**
 

STTTên controlLoại controlMô tả1Khóa họcCombobox
(TH fix cứng dữ liệu hiển thị thì mô tả) 

 Hiển thị danh sách các khóa học sau:

- Khóa BA thực chiến OFFline
- Khóa học BA thực chiến Online
o   Khóa học IT cơ bản
1Khóa họcCombobox
(TH muốn quản lý linh động) 

Hiển thị danh sách các khóa học đang hoạt động trên hệ thống
2Lớp họcCombobox
Hiển thị danh sách các lớp học trên hệ thống

Nếu chọn khóa học thì hiển thị lớp học đang hoạt động thuộc khóa học đó

Ngược lại hiển thị toàn bộ lớp học đang hoạt động trên hệ thống

Dữ liệu được sắp xếp

·                 Chờ khai giảng

·                 Đang học

·                 Kết thúc 

 

## **4. Radiobox List, Checkbox List**

**Sự khác nhau giữa Radiobox và checkbox**

- Checkbox được phép tích chọn nhiều, radiobox chỉ được phép chọn 1
- Khi có danh sách radiobox, nếu đã tích chọn 1 radiobox rồi thì không thể bỏ chọn cho toàn bộ  (bắt buộc phải tích chọn 1 radiobox trong list đó) =>nếu muốn cho phép bỏ chọn toàn bộ thì nên dùng Checkbox
**Cách mô tả: Tương tự với combobox**

 

## **5.Upload ảnh/file**

**Thông tin cần mô tả**

- Định dạng file (đuôi file là gì)
- Kích thước file
## **6.DatePicker**

- DatePicker là loại control sử dụng để nhập thông tin ngày tháng

**DatePicker nào cần đánh số mô tả:  Tất cả**

**Thông tin cần mô tả đối với DatePicker**
**Thông tin mô tả****Bắt buộc mô tả**Ý nghĩa thông tin nhập vào**Bắt buộc**Format hiển thị: ví dụ dd/mm/yyyy hay dd-mm-yyyy**Bắt buộc**Ràng buộc về thời gian nhập liệu, ví dụ thời gian nhập vào <=ngày hiện tại hoặc >=ngày hiện tại -30 ngày…hoặc Từ ngày >=Đến ngày (nếu form cho nhập 2 loại ngày này)**Option**Bắt buộc nhập hay không**Option**Readonly hay được phép chỉnh sửa, mặc định không mô tả là được phép chỉnh sửa 
## 8.Icon trên bảng hiển thị dữ liệu

Cần mô tả icon đó được hiển thị khi nào hoặc không được hiển thị khi nào (Chọn 1 trong 2 cách mô tả)

Mô tả control số 8,9 như sau

##