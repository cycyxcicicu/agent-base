---
id: 328
title: "BA và Quy trình Xây Dựng Yêu Cầu Khi Tích Hợp Với Hệ Thống Đối Tác Đã Có Tài Liệu"
author: "Đậu Thị Ngọc Ánh"
created_at: "2025-08-08T03:47:13.000Z"
source_url: "https://m2mba.com/blog/articles/huong-dan-xay-dung-yeu-cau-tich-hop-he-thong"
---

# BA và Quy trình Xây Dựng Yêu Cầu Khi Tích Hợp Với Hệ Thống Đối Tác Đã Có Tài Liệu

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2025-08-08T03:47:13.000Z*

**1. Mở đầu**

Khi tham gia vào dự án cần tích hợp với đối tác đã có **tài liệu tích hợp (API Spec)**, nhiệm vụ của Business Analyst (BA) không chỉ là “đọc hiểu” tài liệu, mà còn phải **chuyển hóa thông tin kỹ thuật thành yêu cầu cụ thể cho hệ thống**, đảm bảo tích hợp đúng mục tiêu nghiệp vụ.
Việc này đòi hỏi BA phải có quy trình rõ ràng, tránh tình trạng “có tài liệu nhưng không biết bắt đầu từ đâu”.

 

**2. Các bước BA cần thực hiện**

**Bước 1: Xác định mục tiêu và phạm vi tích hợp**

- **Mục tiêu**: Tích hợp để làm gì? (Ví dụ: lấy báo giá giao hàng từ GrabExpress)
- **Nghiệp vụ liên quan**: Quy trình nào sẽ thay đổi sau khi tích hợp?
- **Phạm vi**: Tính năng nào liên quan, tính năng nào không.
 

**Bước 2: Nghiên cứu tài liệu tích hợp**

- Đọc **API Spec** hoặc hướng dẫn kết nối.
- Bước đầu **chỉ cần hiểu mục đích của từng API**, không cần đi sâu chi tiết request/response.
- Lập bảng liệt kê **API và mục đích** của chúng.
- Liên kết API với **UC (Use Case)** của hệ thống mình:API nào dùng cho UC nào
- Thứ tự gọi API ra sao
- Luồng tổng quan giữa hai hệ thống.
- Ví dụ luồng tích hợp cập nhật thông tin đơn hàng từ shopee về hệ thống quản lý đơn hàng (Nhờ AI support) 
**Bước 3: Phân tích chi tiết API**

Mục tiêu ở bước này là **mapping dữ liệu**:

- **Mapping request data**: Xác định dữ liệu mình cần gửi sang → nguồn dữ liệu trong hệ thống đã có chưa → nếu chưa, phải bổ sung chức năng hoặc trường dữ liệu.
- **Mapping response data**: Xác định dữ liệu trả về → cách hiển thị hoặc lưu trữ → mapping lỗi trả về thành thông báo thân thiện.
- Một số thông tin mapping từ hệ thống shopee sang hệ thống bán hàng ((Nhờ AI support)
 

**Bước 4: Định nghĩa yêu cầu hệ thống**

- Xác định **chính xác UC cần tích hợp**.
- Thiết kế màn hình (nếu cần thêm trường phù hợp với API).
- Đưa thêm UC cấu hình dữ liệu đầu vào (nếu cần).
- Xử lý các trường hợp lỗi và timeout.
- Viết **tài liệu yêu cầu tích hợp** cho Dev:Sequence diagram luồng tích hợp tổng quan
- Danh sách API cần sử dụng
- Mô tả UC, luồng tích hợp, thiết kế màn hình, activity diagram cho các tình huống happy case và error case.
 

**Bước 5: Xác nhận yêu cầu**

- Review với Dev team về tính khả thi kỹ thuật.
- Trao đổi với đối tác để xác nhận hiểu đúng tài liệu.
- Lấy sign-off từ stakeholder.
 

**3. Ví dụ: Mapping dữ liệu khi đọc tài liệu tích hợp GrabExpress – API Get Delivery Quotes**

**Mục tiêu:** Lấy báo giá giao hàng từ GrabExpress để hiển thị cho khách hàng trước khi họ xác nhận đơn.

**Bảng Mapping Request Data**
**API GrabExpress (Request)****Field****Mô tả****Dữ liệu bên mình****Ghi chú**origin.address1Địa chỉ lấy hàngOrder.pickup_addressCần chuẩn hóa format địa chỉ destination.address1Địa chỉ giao hàngOrder.delivery_address  weight.valueTrọng lượng kiện hàngOrder.total_weightNếu thiếu → yêu cầu bổ sung serviceTypeLoại dịch vụ giao hàngDelivery.service_typeCấu hình trong hệ thống 
 

**Bảng Mapping Response Data**
**API GrabExpress (Response)****Field****Mô tả****Xử lý trong hệ thống****Ghi chú**quotes[0].priceGiá dự kiếnHiển thị cho userFormat sang VNĐ quotes[0].currencyLoại tiền tệLưu DB + hiển thị  error.codeMã lỗi (nếu có)Mapping sang thông báo UXE102 → "Không tìm thấy tuyến vận chuyển" 
 

**4. Kết luận**

Việc đọc tài liệu tích hợp không chỉ là nhiệm vụ của Dev, mà BA cần **hiểu, lọc, và chuyển hóa** tài liệu đó thành yêu cầu cụ thể, phù hợp với hệ thống của mình.
Kỹ năng mapping data chính là “cầu nối” giữa tài liệu API khô khan và giải pháp nghiệp vụ hiệu quả.

Nếu bạn muốn thực hành quy trình này một cách bài bản, hãy thử áp dụng ngay với API GrabExpress hoặc bất kỳ API nào của đối tác mà dự án bạn đang tham gia.