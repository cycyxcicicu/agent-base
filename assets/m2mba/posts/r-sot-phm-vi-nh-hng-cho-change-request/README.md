---
id: 324
title: "Rà soát phạm vi ảnh hưởng khi có change request"
author: "Đậu Thị Ngọc Ánh"
created_at: "2025-06-16T02:31:41.000Z"
source_url: "https://m2mba.com/blog/articles/r-sot-phm-vi-nh-hng-cho-change-request"
---

# Rà soát phạm vi ảnh hưởng khi có change request

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2025-06-16T02:31:41.000Z*

### **Làm thế nào để xác định phạm vi ảnh hưởng khi có Change Request?**

## **❓ Vì sao đây là vấn đề khiến BA mới lo lắng?**

Một trong những nỗi sợ lớn nhất của Business Analyst – đặc biệt là những bạn mới vào nghề – là khi nhận được một **Change Request (CR)** mà không biết **toàn bộ các chức năng nào sẽ bị ảnh hưởng**. Việc phân tích thiếu phạm vi có thể dẫn đến lỗi hệ thống, ảnh hưởng tiến độ, hoặc thậm chí gây ra sự cố nghiêm trọng khi triển khai.

Các BA lâu năm cũng không hoàn toàn tránh được việc sót phạm vi, nhưng nhờ vào kinh nghiệm, kỹ năng phân tích hệ thống và sự nhạy bén, họ thường nhận diện được ảnh hưởng một cách đầy đủ hơn.

## **📚 Trace Requirements– Khó để maintain**

Trong BABOK, có task **“5.1.Trace Requirements”** nhằm truy vết mối liên hệ giữa các yêu cầu với nhau, giúp xác định CR ảnh hưởng đến đâu. Nhưng thực tế, việc này hiếm khi được thực hiện bài bản tại các công ty Việt Nam. Một số BA có sử dụng **Excel Traceability Matrix**, nhưng để duy trì và cập nhật thường xuyên là việc cực kỳ mất thời gian – điều mà không phải team nào cũng ưu tiên.

Vậy có cách nào thực tiễn, đơn giản hơn không? Dưới đây là **5 phương pháp đơn giản nhưng hiệu quả** mà bạn có thể áp dụng.

## **✅ 5 Cách rà soát phạm vi ảnh hưởng khi có Change Request**

### **1. Xác định đối tượng quản lý bị tác động**

**Nguyên tắc:** Nếu CR thay đổi thuộc tính, logic hoặc hành vi của một đối tượng nào đó, thì tất cả các chức năng thao tác với đối tượng đó có thể bị ảnh hưởng.

Các ban BA khi xác định UC có thể thấy rõ hay có cụm UC CRUD 1 đối tượng nào đó - Ví dụ CRUD đơn hàng - Đặt đơn , Xem ds đơn, xem chi tiết đơn, Chỉnh sửa đơn, xác nhận đơn …Các UC này đang liên quan tới đối tượng quản lý là Đơn hàng. Vậy nếu change request có liên quan tới việc thay đổi các yếu tố quản lý tới đơn hàng thì các UC liên quan tới đối tượng đó sẽ bị ảnh hưởng

**Ví dụ 1:**
Change request yêu cầu **thêm trạng thái “Tạm giữ” cho đơn hàng**. Khi đó, bạn cần rà soát tất cả các chức năng làm việc với đơn hàng:

- Xem danh sách đơn hàng (có cần lọc theo trạng thái mới không?)
- Chi tiết đơn hàng (hiển thị trạng thái mới?)
- Chỉnh sửa đơn hàng (cho phép chuyển sang trạng thái này?)
- Gửi thông báo trạng thái mới?
 
**Ví dụ 2: **Trong hệ thống LMS, có đối tượng quản lý là bài test. Các chức năng liên quan tới quản lý bài test: Tạo bài test - xem ds bài test, xem chi tiết bài test, gán bài test, làm bài test, Nộp bài test…

Change Request yêu cầu **thêm thời gian làm bài (theo phút)** cho mỗi đề thi khi tạo đề kiểm tra.

#### Mối quan hệ chức năng:

- Chức năng A - Tạo bài test : Tạo bài test có thêm thuộc tính “thời gian làm bài”)
- Chức năng B - Làm bài test: Giao diện làm bài của thí sinh cần bổ sung thêm thời gian count down khi làm bài
- Chức năng C - Nộp bài test: Bổ sung thêm chức năng tự động gửi kết quả về cho hệ thống sau khi hết giờ
### **2. Xác định quy trình nghiệp vụ liên quan**

**Nguyên tắc:** Nếu một chức năng nằm trong quy trình nghiệp vụ A bị thay đổi, hoặc quy trình đó thêm bước mới thì toàn bộ chức năng liên quan quy trình A có thể bị ảnh hưởng.

**Ví dụ:** Change Request yêu cầu bổ sung bước “Đánh giá CV bằng AI” sau khi ứng viên nộp hồ sơ.

 

#### **Quy trình tuyển dụng ban đầu**

#### **Sau khi thay đổi:**

- Ứng viên nộp CV
- HR duyệt sơ tuyển
- Mời phỏng vấn
- Đánh giá & ra quyết định

 
- Ứng viên nộp CV
- Hệ thống tự động đánh giá CV bằng AI (xếp loại A, B, C)
- HR xem kết quả & duyệt sơ tuyển
- Mời phỏng vấn
- Đánh giá & ra quyết định
 

**Cần rà soát phạm vi ảnh hưởng gì?**

**✅ Chức năng xem danh sách ứng viên:  **Cần hiển thị kết quả đánh giá AI hay theo phê duyệt cuối cùng của HR (bổ sung trạng thái =>lại quay lại tip 1 do thay đổi thuộc tính quản lý của đối tượng ứng viên), Cần thêm bộ lọc theo xếp loại (A, B, C)
**✅ Giao diện phê duyệt hồ sơ: **Cần bổ sung thêm các thông tin do AI phân tích, phân loại hồ sơ. Ngoài ra, cho phép HR có thể chỉnh sửa kết quả AI?
**✅ Báo cáo tuyển dụng: **Các chức năng liên quan tới báo cáo tuyển dụng có cần thay đổi gì ko, có cần báo cáo số lượng hồ sơ theo xếp loại AI không? Có cần điều chỉnh biểu đồ để bổ sung dữ liệu này?

### **3. Xác định chuỗi Input – Output giữa các chức năng**

**Nguyên tắc:** Nếu output của chức năng A là input cho chức năng B, thì thay đổi ở A có thể làm sai logic ở B.

- **Ví dụ 1: **Chức năng A: Tạo khách hàng
- Chức năng B: Tạo đơn hàng, trong đơn hàng có thông tin KH -  sử dụng thông tin từ A. Và output của chức năng B là gửi email xác nhận thông tin đơn hàng qua email cho KH
- Nếu CR yêu cầu thêm “Loại khách hàng” vào chức năng A, thì bạn phải kiểm tra chức năng B có bị ảnh hưởng không (có hiển thị đúng loại khách trong email không?)
**Ví dụ 2: Luồng xử lý phiếu chi trong hệ thống kế toán nội bộ**

#### **Chức năng A: Tạo phiếu đề nghị thanh toán**

- Người dùng nhập:
Số tiền
Loại chi phí (Công tác phí, Mua hàng, Tiếp khách…)
Bộ phận đề nghị
Ghi chú
- **Output**: Phiếu đề nghị thanh toán (bao gồm dữ liệu đã nhập) được lưu vào hệ thống
**Chức năng B: Kiểm tra và phê duyệt phiếu thanh toán**

- **Input**: Nhận dữ liệu từ chức năng ANgười duyệt xem các thông tin (số tiền, loại chi phí, bộ phận…) để phê duyệt
** Chức năng C: Tổng hợp báo cáo chi phí theo tháng**

- **Input**: Dữ liệu từ A (đã được duyệt trong B)
Tính toán số tiền chi theo từng loại chi phí, từng bộ phận
**📝 Change Request xảy ra: CR yêu cầu thêm trường “Hình thức thanh toán” (Tiền mặt, Chuyển khoản, Nội bộ bù trừ)** vào chức năng A.
**✅ Rà soát phạm vi ảnh hưởng theo chuỗi Input → Output:**

#### **1. Chức năng A (tạo phiếu): **Thêm trường “Hình thức thanh toán”
**2. Chức năng B (phê duyệt):**

- Form phê duyệt có hiển thị trường mới không?
- Có rule nào thay đổi theo hình thức thanh toán? (VD: Nếu là "Tiền mặt", cần thêm người duyệt?)
#### **3. Chức năng C (báo cáo):**

- Có cần thêm cột phân tích theo “Hình thức thanh toán”?
- Có ảnh hưởng đến báo cáo hiện tại không?
- Có cần migration dữ liệu cũ (nếu không có trường này trước đó)?
**Thông điệp dành cho BA: **“Khi một chức năng tạo ra dữ liệu, hãy luôn nhìn theo luồng dữ liệu chảy trong hệ thống để biết ai đang tiêu thụ dữ liệu đó. Nếu bạn chỉ fix chỗ tạo mà quên nơi dùng, thì lỗi là điều chắc chắn.”

### **4. Phân tích quan hệ cha – con trong dữ liệu**

**Nguyên tắc:** Khi dữ liệu có quan hệ phân cấp, thay đổi ở cha có thể ảnh hưởng đến con (và ngược lại).

**Ví dụ:  Dự án và Nhiệm vụ (Project – Task)**

#### **📌 Change Request: Khách hàng yêu cầu bổ sung trạng thái “Đóng băng” cho Dự án, nghĩa là khi dự án chưa bị hủy, nhưng tạm ngưng hoạt động (freeze trạng thái – không chỉnh sửa, không thêm task mới).**

### **❓ Vậy BA cần rà soát gì?**

#### ** Dữ liệu con – Nhiệm vụ (Task):**

- Các nhiệm vụ thuộc dự án đó có cho phép chỉnh sửa không?
- Có chặn tạo mới task khi dự án “Đóng băng” không?
- Nếu task đang xử lý → có cho cập nhật trạng thái nữa không?
### **5. Kiểm tra các API được dùng chung**

**Nguyên tắc:** Nếu nhiều chức năng dùng chung một API, thay đổi API đó có thể gây lỗi diện rộng.

**Ví dụ:**
Một API getAttendanceInfo() trả về thông tin công của NV, API này được sử dụng trong 2 UC:

- Xem thông tin công của NV (actor là NV HR + Lead)
- Xem thông tin công của tôi (Actor là Nhân viên)
### Ví dụ: Bổ sung trường phản ánh mức độ hoàn thành ngày công

### ✅ Ngữ cảnh:

#### API gốc: getAttendanceInfo()

Trước đây chỉ trả về workingDays là tổng số ngày đi làm có check-in và check-out đầy đủ.

### 🔁 Change Request:

HR muốn phản ánh chính xác hơn về chất lượng ngày làm việc.
Yêu cầu bổ sung trường mới: qualifiedWorkingDays – là số ngày công **đủ chuẩn** (check-in đúng giờ, không vi phạm nội quy thời gian).

📌 **Yêu cầu nghiệp vụ:**

- Những ngày có check-in muộn trên 30 phút: tính 0.5 ngày
- Những ngày không đủ dữ liệu (chỉ check-in, không check-out): không tính 
- **Giữ lại workingDays để thể hiện số ngày có mặt, nhưng dùng qualifiedWorkingDays để tính thưởng**
### 🔄 Output mới của API:

### 🧨 Phân tích ảnh hưởng:

- API  getAttendanceInfo được sử dụng ở 2 chức năng Xem thông tin công của NV (actor là NV HR + Lead), Xem thông tin công của tôi (Actor là Nhân viên). Do đó nếu BA đưa ra UC xem thông tin công của NV (actor là NV HR + Lead) và dev sẽ cần sửa API getAttendanceInfo() =>BA và dev sẽ nhận diện ra UC xem thông tin công của tôi với actor là NV cũng có thể bị ảnh hưởng. Trong tình huống này là chắc chắn bị ảnh hưởng, cần hiển thị số ngày công đủ chuẩn của NV
 
Và để có thể xác định được phạm vi ảnh hưởng như trên thì bạn là người cần nắm rõ nghiệp vụ của hệ thống, các chức năng của hệ thống, logic xử lý của hệ thống. Với các bạn mới, sau khi đọc xong, để các bạn áp dụng được nhuần nhuyễn cũng khá là khó, nhưng dựa vào các cách xác định như trên, khi các e làm BA, các e để ý tới mối quan hệ của các chức năng dựa trên 5 tip kia. Dần dần các bạn sẽ hiểu mối quan hệ giữa các chức năng trên hệ thống hơn, từ đó giúp cho các bạn dễ dàng xác định được phạm vi ảnh hưởng. Các anh chị đi trước chủ yếu vẫn xác định dựa vào hiểu biết của mình trong dự án chứ rất ít khi có bảng quản lý yêu cầu, bảng thể hiện mối quan hệ giữa các yêu cầu. Nhiệm vụ của các bạn mới là làm sao hiểu rõ hệ thống của mình nhất có thể để giúp ích cho việc xác định phạm vi ảnh hưởng. 

Hôm sau mình sẽ có bài liên quan tới việc làm thế nào để 1 BA mới join vào 1 dự án có thể tìm hiểu dự án 1 cách nhanh nhất - trước có share 1 bài rồi nhưng giờ mình sẽ lại sẽ chi tiết và có hệ thống hơn