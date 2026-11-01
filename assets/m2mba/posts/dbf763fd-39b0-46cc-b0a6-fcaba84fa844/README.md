---
id: 170
title: "Xây dựng API để bên khác tích hợp - Kèm template mẫu"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-06-25T08:54:51.000Z"
source_url: "https://m2mba.com/blog/articles/dbf763fd-39b0-46cc-b0a6-fcaba84fa844"
---

# Xây dựng API để bên khác tích hợp - Kèm template mẫu

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-06-25T08:54:51.000Z*

Trong Video này, mình có đưa ra case study tích hợp giữa 2 hệ thống Pasgo và hệ thống Sapo. Mình nêu rõ ngữ cảnh để các bạn hiểu rõ hơn nhé

- **Hệ thống Pasgo:** Là hệ thống chuyên hỗ trợ các nhà hàng đặt bàn. KH muốn đặt bàn ở nhà hàng nào thì sẽ gọi điện thoại đến Pasgo hoặc vào web của Pasgo để đặt bàn. Sau đó NV Pasgo sẽ alo sang nhà hàng tương ứng để đặt bàn cho KH. Để có thể cho phép KH đặt bàn trên Pasgo, Nhà hàng sẽ cần phải ký HĐ với Pasgo, và sau đó Pasgo sẽ cung cấp 1 tài khoản cho NH để vào trang web nhà hàng của Pasgo để có thể cung cấp các thông tin nhà hàng : Địa chỉ, giờ mở cửa, Menu, bảng giá, KM…
- **Hệ thống Sapo:** Các nhà hàng đang sử dụng hệ thống Sapo để quản lý nhà hàng của họ. Hiện tại khi KH alo đặt bàn trực tiếp với nhà hàng, hoặc NV Pasgo alo sang để đặt bàn giúp KH thì NV NH sẽ vào hệ thống Sapo để đặt bàn cho KH 
=>Nhà hàng sẽ đồng thời sử dụng cả 2 hệ thống là Sapo và Pasgo. Nếu nhà hàng muốn cho phép KH đặt bàn trên Pasgo và tự động đẩy yêu cầu đặt bàn sang Sapo qua API thì NV nhà hàng sẽ phải vào hệ thống Pasgo để mapping được thông tin nhà hàng (video ở phút 24:27, ở UC Liên kết nhà hàng trên hệ thống Sapo - Web dành cho Nhà hàng)