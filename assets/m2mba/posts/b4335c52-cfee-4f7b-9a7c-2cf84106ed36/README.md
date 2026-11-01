---
id: 115
title: "Quản lý bài quizz tương tác trong khóa học"
author: "Đậu Thị Ngọc Ánh"
created_at: "2024-03-25T07:00:10.000Z"
source_url: "https://m2mba.com/blog/articles/b4335c52-cfee-4f7b-9a7c-2cf84106ed36"
---

# Quản lý bài quizz tương tác trong khóa học

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2024-03-25T07:00:10.000Z*

## **1.Quy trình**

## **2.ERD**

## 
**3.Danh sách các chức năng**

**Ứng dụng**

 

**UC**

 

**Mức độ ưu tiên**

 
Admin portalDanh sách bài quizz (event)Chưa cần làmAdmin portalThêm mới bài quizz (event)Chưa cần làmAdmin portalChi tiết bài quizz (event)Bắt buộc làmAdmin portalThêm mới câu hỏi cho bài quizzBắt buộc làmAdmin portalSửa câu hỏi cho bài quizzBắt buộc làmAdmin portalPlay câu hỏi trong bài quizzBắt buộc làmAdmin portalThống kê kết quả tương tác bài quizzBắt buộc làmAdmin portalShow đáp án câu hỏi đang playBắt buộc làmWeb học viênTrả lời câu hỏi trong bài quizzBắt buộc làm
## 4.Chi tiết yêu cầu

### **4.1.Danh sách bài event (chưa cần làm, do cần làm nhanh, ưu tiên cái khác, có thể tự vào DB tạo event)**

 

## **4.2.Tạo mới bài quiz (event) (chưa cần làm, do cần làm nhanh, ưu tiên cái khác, có thể tự vào DB tạo event)**

Màn hình có 1 control nhập tên bài quizz

## **4.3.Thêm câu hỏi cho bài quizz, luồng tương tác quit**

## 4.4.Chi tiết các ảnh

Màn hình event

 

Màn hình thêm mới câu hỏi trong event

 

**Màn hình show event đang play bên admin**

 

 

**Màn hình show event bên học viên**

 

 

## **4.5.Giải thích 1 số yêu cầu liên quan**

- Admin sẽ tạo các event, các event này sẽ khác với slido là không cấu hình thời gian bắt đầu với kết thúc
- Một event sẽ chứa nhiều câu hỏi, có thể thêm mới câu hỏi bất kỳ lúc nào
- Mỗi khi play event thì tạo ra 1 URL riêng, và kết quả thống kê tính theo lần đó, ko cộng dồn của các lần trước
- **Quy trình play event: **Chọn play event =>Hiển thị 1 trạng chứa QR : QR đó học viên quét sẽ ra trang chứa câu hỏi mà admin sẽ play. Nếu chưa có câu hỏi nào được play thì hiển thị dạng: Chờ trong giây lát (câu gì e nghĩ hay hơn nghĩ hộ chị )
- Admin chọn play 1 câu hỏi, bên trang học viên và admin sẽ nhìn thấy câu hỏi đó (nhưng 2 view khác nhau, 1 bên thì thống kê, 1 bên thì trả lời, nhớ là làm form hiển thị trên mobile dc nhé, vì học viên chủ yếu sẽ trả lời trên điện thoại) =>Chỗ này c đang thắc mắc làm sao để bên trang học viên thay đổi dc, ở đây phải dùng kỹ thuật khác hay chơi dạng 1s refresh 1 lần
- bên trang admin, sẽ có các nút Đáp án để show đáp án, Thống kê để thống kê lượng user chọn từng câu đáp án, chỗ thống kê thì sẽ tính trên các lần play của câu hỏi thì đúng hơn là theo event, tức chị play câu hỏi A ở 10:11ph và học viên trả lời, sau đó chị play lại, học viên trả lời lại thì sẽ chỉ tính thống kê ở lượt sau, ko cộng dồn
- Bình thường không show thống kê, để tránh học viên nhìn vào đó và trả lời theo
- **Câu hỏi trong event:**Cho phép đính kèm ảnh, và khi học viên view, có thể click vào ảnh để view to hơn
- Mỗi câu hỏi đều phải có text, để khi show ở màn hình thống kê, sẽ biết dc học vien chọn câu trả lời nào với tỷ lệ phần trăm ra sao
- Màn hình của admin sẽ chỉ show nội dung text của đáp án, ko cần show hình ảnh
- **Câu trả lời của học viên: **Chỗ này nếu cho phép update thì tốt hơn nhỉ, e cho update câu trả lời đi nhé, nhưng ko ưu tiên lắm, làm kịp thì làm, ko thì ko cho update cũng dc
- **Nhạc đính kèm: **Nếu có thể thì khi play event sẽ chạy 1 bản nhạc trong list có sẵn
- Khi show đáp án hay thống kê cũng cho thêm tý âm thanh vào (ưu tiên sau)