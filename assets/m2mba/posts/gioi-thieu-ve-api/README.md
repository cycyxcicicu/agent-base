---
id: 33
title: "Giới thiệu về API"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-19T13:59:03.000Z"
source_url: "https://m2mba.com/blog/articles/gioi-thieu-ve-api"
---

# Giới thiệu về API

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-19T13:59:03.000Z*

![Ảnh bìa](images/fc749cb0-6900-41a9-aef9-0775c2a2d928.png)

## 1.API là gì

- API là cầu nối giữa client và server (máy khách và máy chủ) giữa server hệ thống này với server hệ thống khác để kết nối trao đổi thông tin với nhau (như hệ thống TMĐT với hệ thống giao hàng để yêu cầu giao hàng, hệ thống TMĐT với hệ thống thanh toán để kết nối thanh toán online)
- Khi A cần gửi yêu cầu cho B thực hiện việc gì đó thì A sẽ call API của B hay máy chủ sẽ cần mở cổng (API) để bên máy khách gọi vào để yêu cầu Máy chủ xử lý, ví dụ KH vào xem  danh sách đơn hàng trên tiki, web/mobile app Tiki (client/Máy khách) sẽ gọi API order (lấy danh sách đơn hàng) của server TIKI (server/máy chủ). Với mỗi yêu cầu sẽ có dữ liệu gửi lên và trả về khác nhau, người ta gọi đó là request data, và response data 

- Các bạn BA luôn cần nắm được data trao đổi giữa client – server, giữa server này và server kia (2 hệ thống với nhau), data trao đổi luôn kiểu dạng cặp key – value (để biết thông tin A có giá trị bao nhiêu, ví dụ họ tên có giá trị là Đậu Thị Ngọc Ánh, ngày sinh có giá trị là 06/02/1985…)
 

## 2.Định dạng XML, Json trong request, response data

Định dạng data trong request và response data trong API có dạng XML hoặc Json

Json: 

{

    "full_name": "Dau Thi Ngoc Anh",

    "company": "Teko Viet Nam ",

    "telephone": "0983xxx076",

    "street": "CT1A, Chung cư mễ trì plaza, lương thế vinh",

    "is_default": **false**,

    "delivery_address_type": "company",

    "region_id": "297",

    "city_id": "724",

    "ward_id": "3719"

}

 

XML: 

<?xml version="1.0" encoding="UTF-8"?>

<products>

    <product>

        <name>Dom quixote de La Mancha</name>

        <quantity>12</quantity>

        <category>Book</category>

    </product>

    <product>

        <name>Hamlet</name>

        <quantity>3</quantity>

        <category>Book</category>

    </product>

    <product>

        <name>War and Peace</name>

        <quantity>7</quantity>

        <category>Book</category>

    </product>

    <product>

        <name>Moby Dick</name>

        <quantity>14</quantity>

        <category>Book</category>

    </product>

    <product>

        <name>Forrest Gump</name>

        <quantity>16</quantity>

        <category>DVD</category>

    </product>

    <product>

        <name>Taxi Driver</name>

        <quantity>25</quantity>

        <category>DVD</category>

    </product>

    <product>

        <name>The Godfather</name>

        <quantity>21</quantity>

        <category>DVD</category>

    </product>

    <product>

        <name>Star Wars: The Last Jedi</name>

        <quantity>48</quantity>

        <category>Blu Ray</category>

    </product>

    <product>

        <name>Dunkirk</name>

        <quantity>12</quantity>

        <category>Blu Ray</category>

    </product>

    <product>

        <name>Black Panther</name>

        <quantity>21</quantity>

        <category>Blu Ray</category>

    </product>

</products>

 

Các bạn không cần quá quan tâm đến đặc điểm của định dạng Json hay XML, mà bạn chỉ cần thấy trong 2 loại trên thì cái quan trọng trong phần data đó là cặp key-value, tức nó cho biết với thông tin A này có giá trị là bao nhiêu, ví dụ với thông tin dạng json "full_name": "Dau Thi Ngoc Anh"

=>Có nghĩa là họ tên (full_name) có giá trị là Đậu thị Ngọc Ánh

Còn với dạng XML <product>

        <name>Dunkirk</name>

        <quantity>12</quantity>

        <category>Blu Ray</category>

    </product>

=>Tên sản phẩm: Dunkirk, Số lượng: 12, Danh mục (category); Blue Ray

- Json

- XML

## 3.Các thành phần trong API

- Một request API chuẩn cần có đủ 4 thứURL
- Method
- Header
- Body
 
Thành phần APIMô tả ý nghĩaURL
là 1 địa chỉ định danh yêu cầu mà bên cung cấp API muốn thực hiện, ví dụ API lấy danh sách đơn hàng của tôi của TIKI có URL: [https://tiki.vn/api/v2/orders?page=0&limit=10](https://tiki.vn/api/v2/orders?page=0&limit=10) 

Mỗi APi sẽ tác động tới resource cụ thể, như API ở trên là tác động vào resource order, API chỉnh sửa sổ địa chỉ sẽ tác động tới resource address

Mỗi API sẽ có 1 URL
Method
Là hành động mà bên gửi yêu cầu muốn tác động lên resource tương ứng, ví dụ

– GET: Yêu cầu server cung cấp thông tin resource: Lấy danh sách order của tôi trong tiki, lấy thông tin tài khoản của tôi trong tiki

– POST: Yêu cầu server tạo mới 1 resource, như tạo mới sổ địa chỉ, tạo mới đơn hàng

– PUT: Yêu cầu server cho sửa / thêm vào resource đã có trên hệ thống. Ví dụ: chỉnh sửa thông tin sổ địa chỉ

– DELETE: Yêu cầu server cho xóa 1 resourse. 
HeaderNơi chứa các thông tin cần thiết của 1 request nhưng end-users không biết có sự tồn tại của nó. Ví dụ: độ dài của request body, thời gian gửi request, loại thiết bị, đang sử dụng, loại định dạng cái response mà client có đọc được…thông tin token của user (thông tin định danh user nào đang thực hiện)BodyNơi chứa thông tin mà bên gửi (client) sẽ điền để gửi lên server. Giả sử bạn muốn đăng ký học tại 1 trung tâm , bạn sẽ cần cung cấp như thông tin cá nhân của bạn và thông tin lớp học bạn muốn đăng ký, trong giao tiếp hệ thống cũng vậy, client muốn server làm gì thì client sẽ cần phải gửi đủ thông tin cho server
**Response**:

Sau khi nhận được request từ phía client, server sẽ xử lý cái request đó và gửi ngược lại cho client response, chứa kết quả thực hiện của server. Cấu trúc của 1 response tương đối giống phần request nhưng Status code sẽ thay thế cho URL và Method. 

**Thông tin trong response****Mô tả ý nghĩa****Status code**là những con số có 3 chữ số và có duy nhất 1 ý nghĩa. Chắc các bạn cũng không còn lạ lẫm với những Error “404 Not Found” hoặc “503 Service Unavailable”. Full list có [ở đây](https://docs.oracle.com/en/cloud/saas/enterprise-performance-management-common/prest/status_codes.html) .**Header **và **Body **tương đối giống với request.
 

Ví dụ về response data

Status code và header

Body

 
 

Có thể tham khảo đặc tả API của bên giao hàng tiết kiệm, với các sample request và response mẫu nhé

[https://docs.giaohangtietkiem.vn/#ng-n-h-ng](https://docs.giaohangtietkiem.vn/#ng-n-h-ng)