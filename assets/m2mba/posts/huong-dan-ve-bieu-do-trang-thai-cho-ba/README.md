---
id: 71
title: "State diagram"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T11:28:59.000Z"
source_url: "https://m2mba.com/blog/articles/huong-dan-ve-bieu-do-trang-thai-cho-ba"
---

# State diagram

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T11:28:59.000Z*

State diagram là 1 technique khá hiệu quả và thường được BA sử dụng để mô tả luồng chuyển trạng thái của 1 thực thể, giúp nắm rõ tổng quan luồng hoạt động của thực thể đó. 

Nhiều bạn vẽ biểu đồ trạng thái nhưng lại vẽ theo kiểu quy trình nghiệp vụ, và không gắn với 1 thực thể được quản lý trên hệ thống

Để vẽ được biểu đồ trạng thái bạn cần thực hiện các step sau (Xem ảnh minh họa)

- **Xác định thực thể:** Bạn cần phải biết bạn vẽ biểu đồ trạng thái cho thực thể nào.
- **Xác định các hành động và actor tác động lên thực thể đó:** Chỉ khi bạn biết có những tác động nào tác động lên thực thể đó thì bạn mới xác định được đẩy đủ các trạng thái cần có
- **Xác định trạng thái:** Bạn cần phải trả lời câu hỏi: Mình muốn theo dõi và tra cứu chi tiết trạng thái của thực thể đó chi tiết đến mức nào? Ví dụ như nhìn vào trạng thái thực thể là có thể biết nó đang ở trong giai đoạn nào, hay hành động nào vừa tác động vào trạng thái đó. Hay nhiều lúc bạn không muốn quá nhiều trạng thái, chỉ cần những trạng thái cơ bản thôi=>Đấy là do bạn phân tích và quyết định. Với những thực thể có nhiều tác động phức tạp thì bạn nên quản lý trạng thái càng chi tiết càng tốt
- **Xác định trạng thái bắt đầu, kết thúc:** Biểu đồ trạng thái thể hiện vòng đời trạng thái của thực thể đó, nên chúng ta cần phải có trạng thái của thực thể khi nó được khởi tạo (nếu match vào việc insert DB thì đó là trạng thái đầu tiên khi nó được insert vào bảng dữ liệu tương ứng), và trạng thái kết thúc là trạng thái mà ở đó thực thể sẽ không có luồng chuyển sang 1 trạng thái nào khác
- **Xác định luồng chuyển trạng thái:** Bạn cần biết trạng thái A được chuyển sang những trạng thái nào, và khi nào thì chuyển sang trạng thái đó (Hành động nào của actor nào)
- **Chuyển thể lên diagram**: Bạn hãy dùng tool phù hợp để vẽ thôi
- **Bảng mô tả trạng thái (nếu cần):** Nếu như trên biểu đồ chưa thể hiện rõ được lúc nào thì chuyển từ A sang B thì bạn có thể bổ sung thêm bảng mô tả nhé
Ngoài ra, mỗi thực thể có nhiều trạng thái khác nhau thay vì quản lý trên 1 trạng thái (sẽ sinh ra quá nhiều trạng thái khác nhau) và để nắm rõ chi tiêt thực thể đang ở đâu thì bạn sẽ kết hợp các trạng thái đó với nhau

Trên đây là 1 số gợi ý của mình khi sử dụng technique state diagram, các bạn hãy thử áp dụng vào trong công việc BA của mình nhé, sẽ rất hiệu quả đấy