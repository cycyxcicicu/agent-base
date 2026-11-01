---
id: 66
title: "Usecase Diagram - Include, extend"
author: "Đậu Thị Ngọc Ánh"
created_at: "2023-12-28T10:44:08.000Z"
source_url: "https://m2mba.com/blog/articles/phan-biet-include-extend-trong-usecase-diagram"
---

# Usecase Diagram - Include, extend

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2023-12-28T10:44:08.000Z*

Trước đây trong khóa học của mình có dạy về Usecase diagram và mối quan hệ giữa các usecase nhưng sau đó mình thấy việc thể hiện các mối quan hệ Usecase không quá cần thiết lắm, vì việc vẽ đúng vẽ sai không ai biết, và nếu có sai thì có vẻ cũng không ảnh hưởng gì trong quá trình thực hiện thế nên mình quyết định không giảng cho học viên về mối quan hệ này nữa hoặc giảng nhanh. Vì mình thấy việc quan trọng của Usecase diagram đó là để thể hiện được các UC trên hệ thống, và ai là người thực hiện UC đó. Tuy nhiên nếu số lượng usecase nhiều lên thì nếu vẽ trên 1 hình sẽ rối , và phải vẽ trên nhiều hình, mà nhiều hình thì cũng không overview được, do đó mình có guideline là nếu nhiều quá thì liệt kê dạng bảng, không cần thiết rập khuôn khi nào cũng phải vẽ Usecase diagram nữa Dạo gần đây thấy 1 số bạn lại quay lại hỏi về mối quan hệ giữa các Usecase vì template của công ty/đối tác yêu cầu như thế và trong template, mình thấy ví dụ mẫu cũng sai, bạn học viên vẽ 1 cái mới cũng sai nên mình quyết định viết 1 bài về quan hệ giữa các usecase này (mình nghĩ tỷ lệ người nắm đúng cái này không nhiều, và quan trọng hơn hết đúng/sai có vẻ không quá ảnh hưởng lắm thì phải, do đại đa số đều hiểu sai giống nhau thì phải , mà không chắc mình hiểu đúng không ). Chúng ta thử đi tìm khái niệm trong sách BABOK và cùng phân tích qua các ví dụ và các lỗi nhé. Tất nhiên nếu các bạn đang hiểu khác thì hãy thử comment để trao đổi nhé

## **1.Include**

- Mình copy câu định nghĩa của BABOK: "allows for the use case to make use of functionality present in another use case. The included use case does not need to be a complete use case in its own right if it is not directly triggered by an actor. This relationship is most often used either when some shared functionality is required by several use cases or to abstract out a complex piece of logic "
Câu này dịch tạm theo nghĩa hiểu là Include là Usecase A include usecase B 

- Usecase B sẽ là 1 phần khi thực hiện Usecase A, có nghĩa trong khi thực hiện Usecase A thì bắt buộc bao gồm các bước xử lý trong usecase B. 
- Usecase B không cần là 1 Usecase hoàn chỉnh (độc lập) nếu nó không trực tiếp trigger bởi 1 actor (Ví dụ Usecase chuyển khoản include usecase Kiểm tra thông tin GD (hạn mức, số dư Tk..), thì usecase Kiểm tra thông tin GD là 1 usecase thuộc về hệ thống xử lý, không trigger bởi actor). 
- Chúng ta chỉ nên tách Usecase B ra khỏi Usecase A nếu Usecase B được sử dụng bởi nhiều usecase khác nhau (Tái sử dụng xử lý logic giữa các Usecase với nhau) hoặc khi 1 usecase phức tạp cần tách nhỏ ra để giúp chúng ta thể hiện đơn giản cho luồng xử lý của usecase đó
=>Bình thường mình thấy các bạn hay thể hiện Usecase A include B bằng cách trả lời câu hỏi A thành công khi B thành công. Nhiều bạn coi Usecase A include login=>Bản chất Login ở đây ko phải là 1 Included usecase mà là precondition của nhiều usecase khác nhau

Vậy khi nào chúng ta hãy thử lấy ví dụ để hiểu hơn khi nào nên dùng kỹ thuật tách usecase để hình thành nên quan hệ include

- Khi 1 Usecase có quá nhiều bước xử lý, để đơn giản hóa quá trình xử lý (Vẽ flow, mô tả flow) thì chúng ta nên tách ra thành các usecase khác nhau để khi vẽ luồng, mô tả luồng được đơn giản hơn. 
- Ví dụ khi thực hiện chức năng Chuyển tiền theo số tài khoản trong ngân hàng của 1 app Mobile Banking nào đó. Thay vì các bạn thể hiện 1 flow luồng từ đầu tới cuối có quá nhiều step thì các bạn có thể tách ra thành: Usecase Chuyển tiền trong NH theo số tài khoản include Usecase truy vấn thông tin tài khoản thụ hưởng, Truy vấn phí GD và Kiểm tra thông tin GD (Chính là bước để sinh OTP) (Xem ảnh minh họa)
- Khi 1 đoạn xử lý logic nghiệp vụ được tái sử dụng lại ở nhiều usecase khác nhau thì thay vì việc ở tất cả các usecase mình đều nêu cùng 1 đoạn xử lý như thế thì mình tách ra:Đỡ công đoạn viết tài liệu 
- Trong trường hợp sửa đổi logic chỗ đó thì chỉ cần sửa 1 nơi, tránh sửa chỗ A không sửa chỗ B, không nhất quán
- Ví dụ trong GD của ngân hàng luôn có phần tính phí, thì usecase tính phí sẽ là 1 usecase riêng để thể hiện nghiệp vụ tính phí cho các loại GD (Xem ảnh minh họa)
## **2.Extend**: 

Mình copy câu định nghĩa của BABOK : “allows for the insertion of additional behavior into a use case. The use case that is being extended must be completely functional in its own right and must not depend on the extending use case for its successful execution. This relationship may be used to show that an alternate flow has been added to an existing use case (representing new requirements).”

Tạm dịch câu trên: Cho phép add thêm 1 hành vi vào 1 Usecase. Base Usecase sẽ thực hiện độc lập với extending usecase (không có tính phụ thuộc như Include), extending usecase chỉ là lựa chọn thêm của KH khi thực hiện base usecase

Ví dụ đặt xe grab thì Lựa chọn mã KM sẽ là extending usecase của usecase đặt xe Grab vì KH có thể add mã KM hoặc không

## **3.Rút gọn lại ý extend và include**

- Dùng quan hệ A include B khi B bắt buộc phải là 1 phần của A
- B là extend của A thì khi thực hiện A có thể thực hiện B cũng được, không thực hiện B cũng được: Hay còn gọi B là alternative flow của Usecase A
Mình có đính kèm ảnh minh họa 1 số ví dụ sai của quan hệ include và extend mà mình từng bắt gặp

 

Tất nhiên, ko loại trừ mình cũng hiểu sai, vậy nên các bạn hãy thử cùng thảo luận dựa trên định nghĩa và google thêm nhé. 

Ngoài ra trước đây mình cũng có 1 viết 1 bài về phân biệt 1 số khái niệm trong phần UC diagram, các bạn thử đọc lại nhé