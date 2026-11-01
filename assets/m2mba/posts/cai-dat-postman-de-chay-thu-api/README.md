---
id: 32
title: "Cài đặt postman để chạy thử API"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-19T13:56:45.000Z"
source_url: "https://m2mba.com/blog/articles/cai-dat-postman-de-chay-thu-api"
---

# Cài đặt postman để chạy thử API

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-19T13:56:45.000Z*

![Ảnh bìa](images/09c51704-f12b-4d1a-a838-d056ec02eb54.png)

## 1.Hướng dẫn cài đặt tool Postman

**Bước 1:** Cài đặt postman

- Tải ứng dụng về máy : [https://www.postman.com/downloads/](https://www.postman.com/downloads/) 
- Và chạy file cài đăt tương ứng
**Bước 2:** Mở ứng dụng postman trên máy đã cài đặt

**Bước 3**: Tạo API để chạy thử, bằng cách click vào nút New

**Bước 4:** Chọn Tạo request hoặc collection

- Request là sẽ tạo API để chạy thử 
- Collection: Tạo forder chứa các request để chạy thử, giúp cho các bạn dễ quản lý, tạo collection xong, bạn tạo tiếp request ở và đặt trong collection đó

**Bước 5:** Chọn Collection, nhập Tên và mô tả, Chọn nút Create 

Collection sau khi tạo xong

**Bước 6:** Click chuột phải ở tên Collection, sau đó chọn Add request

**Bước 7**:  Nhập Tên, mô tả của request, sau đó chọn Save

**Bước 8:** Tạo thông tin chi tiết của request , chọn vào icon < ở cạnh Collection bạn tạo ra

## 2.Hướng dẫn nhập thông tin chi tiết của API trên postman

Bước 1: Chọn Request cần tạo thông tin chi tiết

**Bước 2**: Nhập thông tin method, URL, Body, header. Các thông tin này nếu bạn áp dụng trong dự án của các bạn thì sẽ cần hỏi dev, còn nếu bạn muốn chạy thử trên 1 ứng dụng public nào đó như tiki, shophee thì các bạn có thể thực hiện các bước sau:

  Bạn vào trang tiki.vn, và sau đây mình hướng dẫn các bạn chạy thử 1 API, sau đó các bạn có thể chạy bất cứ API nào của tiki nếu bạn muốn nhé. Mình hướng dẫn các bạn chạy API lấy danh sách đơn hàng của tôi nhé

- Bước 2.1: Chọn phím Fn+F12, chọn tiếp Network, Chọn Fetch XHR, như hình dưới

- Bước 2.2: Vào đơn hàng của tôi, sau đó bạn vào khung thông tin ở bước 2.1 (khung này có thể nằm bên trái, phải, dưới web tiki nhé), chọn đến phần được khoanh tròn

- Bước 2.3: Chọn header như hình dưới

- Bước 2.4: Lấy các thông tin trên API của tiki để điền vào trên postman

- Số thứ tự 1: Điền method = thông tin số 1 ở hình ở bước 2.3
- Số thứ tự 2: Điền URL = URL ở thông tin số 2 ở hình ở bước 2.3

Bước 2.5: Nhập x-access-token: Ở phần header đã chọn ở bước 2.3, kéo xuống phía dưới phần response header** **

 

Bước 2.6: Chọn thông tin header trong phần request của API trong postman và nhập thông tin như sau

Bước 2.4: Chạy API bằng cách click vào nút Send

Bước 2.11: Hình trên là hình kết quả server trả về, còn hình ở bên dưới ở bước này là hình chụp trên giao diện của tiki hiển thj cho người dùng