---
id: 132
title: "Lỗi liên quan tới Usecase"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-04-19T01:56:00.000Z"
source_url: "https://m2mba.com/blog/articles/cc-li-thng-gp-khi-thit-k-usecase-chnh-sa-xa-d-liu"
---

# Lỗi liên quan tới Usecase

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-04-19T01:56:00.000Z*

## 1.UC chỉnh sửa, xóa

- Với các UC chỉnh sửa, xóa, các bạn cần lưu ý về điều kiện để thực hiện, và điều kiện hệ thống phải check được, không phải điều kiện ở ngoài đời. Vì điều kiện đưa ra là để hệ thống check (Dev sẽ lập trình để check theo các điều kiện mà BA đưa ra). Điều kiện thườngChỉnh sửa: Ai được phép chỉnh sửa, được chỉnh sửa thông tin gì, Trạng thái đối tượng chỉnh sửa phải thỏa mãn điều kiện gì, hoặc tùy nghiệp vụ cụ thể của bạn
- Xóa: Ai được phép xóa, có thông tin nào được tạo ra liên quan tới thông tin ứng với UC xóa đó không. Ví dụ Xóa khóa học, nhưng trên hệ thống đã có lớp học của khóa học đó. Hoặc xóa lớp học nhưng trên hệ thống đã có các yêu cầu đăng ký lớp học tương ứngGiải pháp: Chỉ cho xóa khi chưa tồn tại các thông tin liên kết như trên (nên xử lý theo cách này)
- Hoặc khi xóa thì xóa các thông tin liên quan
Một số lỗi của các bạn học viên trong phần UC chỉnh sửa, xóa

### 1.1.Hủy đơn hàng
Lỗifix
Hệ thống không thể biết như thế nào là đơn hàng chưa được gửi

Phải đưa ra đk để hệ thống có thể check được
Đơn hàng đang ở trạng thái Chờ xác nhận (hoặc trạng thái gì thì tùy nghiệp vụ của bọn e để đưa ra cụ thể