---
id: 235
title: "Quản lý khóa học - Bổ sung yêu cầu"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-07-29T13:47:51.000Z"
source_url: "https://m2mba.com/blog/articles/3d790a6e-af05-4cc1-9b0d-ab584ea3cdac"
---

# Quản lý khóa học - Bổ sung yêu cầu

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-07-29T13:47:51.000Z*

## 1.Nguồn gốc yêu cầu

Do hiện tại trung tâm triển khai các khóa học qua video nên cách quản lý hiện tại không phù hợp, đang tận dụng bên phần nghiệp vụ Chia sẻ kiến thức=>Gây rối cho phần chia sẻ kiến thức, học viên khó theo dõi

Để học viên dễ theo dõi các thông tin liên quan tới khóa học, từ lúc chưa đăng ký, tới lúc đăng ký thì cần phải thay đổi lại cách quản lý thông tin liên quan đến khóa học, cũng như cách hiển thị thông tin cho user theo dõi trước lúc đăng ký, và sau khi đăng ký

## 2.Danh sách các chức năng cần thực hiện
Ứng dụngTên UC  Web adminCRUD khóa học  Web adminCRUD nội dung khóa học  Web adminCRUD BTVN của khóa học  Web học viênXem Danh sách khóa học  Web học viênXem chi tiết khóa học  
## 2.Chi tiết yêu cầu

## 2.1 CRUD khóa học

- **Danh sách khóa học**
- **Thêm mới thông tin chung về khóa học**
- **Xem chi tiết khóa học**
## 2.2.CRUD nội dung chi tiết khóa học

### 2.3.CRUD BTVN

## 2.4.Web học viên - Danh sách khóa học đăng ký

- Với khóa dạng video sẽ chỉ hiển thị icon : Vào học (Khi khác trang thái Chờ thanh toán và Hủy đăng ký)
- Zalo của lớp
- QR thanh toán (nếu chưa thanh toán
- Khi click vào học sẽ mở trang chi tiết (khác với khóa dạng tương tác)
- Khóa còn lại: hiển thị như cũ
## 2.4.Web học viên - Xem chi tiết khóa học đã đăng ký

- Với khóa dạng video hiển thị MH như bên dưới : Lưu ý: **Rule hiển thị: **Chỉ click xem được các nội dung chi tiết của các nội dung cha tiếp theo theo nội dung cha ngay trước đó có toàn bộ bài test ở trạng thái là Pass (1 bài test được làm nhiều lần thì chỉ cần 1 lần pass là okie)
- API chỉ trả về thông tin chi tiết của các nội dung đủ điều kiện xem
- Click vào từng nội dung cha, nội dung con của nội dung cha : Vẫn hiển thị ra theo dạng menu nhưng click vào để xem chi tiết thì sẽ báo lỗi: “Bạn chưa hoàn thành các bài test ở nội dung trước. Vui lòng thực hiện để được mở các nội dung tiếp theo”
- **Rule click vào nút Làm bài quizz **(nếu nội dung chi tiết là dạng quizz): Áp dụng theo rule như trong phần Làm bài của “Bài test của tôi”
- Khóa còn lại: Bổ sung thêm 1 mục Nội dung chi tiết khóa học (hiển thị như bên Khóa học dạng video)