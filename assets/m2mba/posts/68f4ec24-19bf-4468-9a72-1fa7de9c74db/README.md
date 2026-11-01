---
id: 338
title: "Kỹ thuật State Diagram cho Business Analyst: Hướng dẫn chi tiết & Các sai lầm cần tránh"
author: "Đậu Thị Ngọc Ánh"
created_at: "2026-07-13T12:38:53.000Z"
source_url: "https://m2mba.com/blog/articles/68f4ec24-19bf-4468-9a72-1fa7de9c74db"
---

# Kỹ thuật State Diagram cho Business Analyst: Hướng dẫn chi tiết & Các sai lầm cần tránh

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2026-07-13T12:38:53.000Z*

Trong phân tích thiết kế hệ thống, **ERD (Entity Relationship Diagram)** là một kỹ thuật cực kỳ hữu hiệu giúp đội ngũ Developer có cái nhìn tổng quan (overview) rất nhanh về hệ thống, từ các chức năng liên quan đến việc thiết lập các rule ràng buộc dữ liệu. Đi cặp bài trùng với ERD chính là **State Diagram (Biểu đồ trạng thái)** – công cụ “sắc bén” chuyên biệt gắn liền với việc quản lý vòng đời của các thực thể cốt lõi.

Nếu ERD định nghĩa cấu trúc dữ liệu, thì State Diagram giúp rà soát logic nghiệp vụ và đảm bảo hệ thống không bị bỏ sót các trường hợp rẽ nhánh (edge cases). Việc vẽ State Diagram không chỉ là nối các hình khối, mà là quá trình tư duy logic về dữ liệu. Tuy nhiên, nếu các bạn chưa xác định đúng thực thể cần vẽ diagram (từ mô hình ERD), thì biểu đồ trạng thái của bạn có thể sẽ không chính xác và sai lệch hoàn toàn bản chất.

Dưới đây là hướng dẫn chi tiết từng bước áp dụng State Diagram chuẩn xác, bắt đầu từ việc chọn đúng thực thể, cùng với các “cạm bẫy” mà BA thường mắc phải.

## Phần 1: 8 Bước Phân Tích & Vẽ State Diagram Hiệu Quả

### 1. Xác định thực thể (Identify the Entity)

Nguyên tắc tối thượng: **State Diagram luôn gắn liền với MỘT thực thể duy nhất**. Bạn cần xác định rõ mình đang vẽ vòng đời cho cái gì (ví dụ: Đơn hàng, Tài khoản người dùng). Việc nhầm lẫn thực thể sẽ làm biểu đồ trở nên rối rắm và sai bản chất.

**📌 Dấu hiệu nhận biết: Khi nào một thực thể cần vẽ State Diagram?**
Không phải thực thể hay trường dữ liệu nào trong hệ thống cũng cần vẽ biểu đồ trạng thái. Một thực thể (hoặc trường dữ liệu) chỉ nên có State Diagram khi nó thỏa mãn 2 điều kiện cốt lõi:

- **Tập giá trị hữu hạn:** Trường đó chứa một danh sách các giá trị trạng thái nhất định có thể liệt kê được.
- **Có tính tuần tự và ràng buộc chuyển đổi:** Không phải giá trị nào cũng có thể tự do cập nhật sang giá trị khác một cách tùy tiện. Việc chuyển đổi (transition) phải tuân thủ luồng nghiệp vụ, không được nhảy cóc và bắt buộc phải có một hành động (action) hay sự kiện (event) cụ thể để kích hoạt sự chuyển đổi đó.
**Ví dụ đối chiếu:**

❌ **Tình huống KHÔNG CẦN vẽ:** Trường Giới tính (Nam / Nữ / Khác) hoặc Cấp bậc của thực thể Người dùng. Mặc dù chúng có tập giá trị hữu hạn, nhưng đây là thuộc tính mang tính chất “phân loại” tĩnh. Nếu cần thay đổi, user chỉ việc bấm Edit và chọn lại (từ Nam sang Nữ), đó chỉ là hành động cập nhật dữ liệu (Data Update) đơn thuần, không phải là tiến trình vòng đời.

🗄️ Mô phỏng DB (Bảng User): Chỉ cập nhật đè (overwrite) giá trị cũ.
user_idnamegenderU001Nguyễn Văn AMALE -> **FEMALE**
✅ **Tình huống BẮT BUỘC vẽ:** Trường Tình trạng Đơn hàng. Một đơn hàng không thể “nhảy cóc” từ trạng thái Chờ lấy hàng sang thẳng Giao thành công nếu thiếu bước Đang đi giao. Để chuyển trạng thái, hệ thống cần các hành động xác nhận cụ thể từ các Actor khác nhau (Shipper, Kho) chứ không phải user thích đổi trạng thái nào cũng được.

🗄️ Mô phỏng DB (Bảng Order): Cần track lịch sử vòng đời tuần tự.
order_idcustomer_idstatusupdated_byORD-01U001PENDING_PICKUP -> DELIVERINGShipper_01
### 2. Xác định các hành động (Event) và Actor tác động

Việc chuyển đổi từ trạng thái này sang trạng thái khác không tự nhiên diễn ra, nó luôn cần một **sự kiện kích hoạt (Event/Trigger)** từ một **chủ thể (Actor)** nhất định.

- **Actor:** Ai là người thực hiện? (Người dùng cuối, Admin, Hệ thống tự động, hay Hệ thống đối tác).
- **Hành động/Sự kiện:** Họ làm gì? (Khách hàng bấm “Hủy”, Admin bấm “Duyệt”, Hệ thống tự động báo “Hết hạn”).
**📌 Ghi chú quan trọng về Mục tiêu quản lý trạng thái:**
Mục đích cốt lõi của việc thiết lập các trạng thái này không chỉ để Developer code cho chạy, mà là để **phục vụ quá trình vận hành (Operations)**. Các trạng thái bạn thiết lập phải giúp những người vận hành (nhân viên CSKH, điều phối, kế toán…) chỉ cần nhìn vào hệ thống là biết ngay lập tức **công việc ở ngoài đời thực đang diễn ra đến đâu**, ai đang nắm giữ “trái bóng” trách nhiệm. Nếu trạng thái trên phần mềm chỉ ghi chung chung là “Đang xử lý” trong khi ngoài đời shipper đã lấy hàng đi giao, thì thiết kế trạng thái đó hoàn toàn vô giá trị với người vận hành.

### 3. Quyết định mức độ chi tiết của trạng thái

Bạn muốn tra cứu trạng thái của thực thể chi tiết đến mức nào?

- **Góc độ Business (Mức cơ bản):** Đơn hàng có thể chỉ cần: Chờ xử lý, Đang giao, Đã giao, Đã hủy. Nhìn vào là biết ngay giai đoạn nghiệp vụ.
- **Góc độ Technical/Operation (Mức chi tiết):** Nếu quy trình phức tạp, bạn có thể cần tách nhỏ: Chờ lấy hàng, Đang trung chuyển, Đã đến kho giao, Đang đi giao.
Lưu ý: Việc chia nhỏ hay gộp là do bạn phân tích và quyết định dựa trên yêu cầu quản lý. Càng nhiều tác động phức tạp, bạn càng nên quản lý chi tiết.
### 4. Xác định trạng thái bắt đầu (Start) và kết thúc (End)

Mọi thực thể đều có vòng đời (Sinh ra -> Sống -> Chết):

- **Trạng thái bắt đầu (Initial State):** Trạng thái ngay khi thực thể được khởi tạo (VD: Khi user vừa submit form, record được insert vào DB với status = Pending).
- **Trạng thái kết thúc (Final State):** Nơi thực thể dừng lại và không có luồng nào chuyển sang trạng thái khác được nữa (VD: Completed, Cancelled, Rejected).
### 5. Xác định luồng chuyển trạng thái (Transitions)

Đây là cốt lõi của biểu đồ. Bạn phải trả lời được câu hỏi: **Từ trạng thái A, có thể chuyển sang những trạng thái nào? Và điều kiện/hành động nào kích hoạt sự chuyển đổi đó?**

- Ví dụ: Đơn hàng từ Chờ duyệt -> Đã duyệt (khi Admin nhấn Approve) hoặc Đã hủy (khi User nhấn Cancel).
### 6. Tách vòng đời song song để tránh “Bùng nổ trạng thái” (State Explosion)

**Hiện tượng “Bùng nổ trạng thái” là gì?**
Đó là khi một thực thể có nhiều khía cạnh nghiệp vụ diễn ra đồng thời. Ví dụ: Một đơn hàng vừa chịu sự chi phối của tiến trình Giao hàng, vừa chịu sự chi phối của tiến trình Thanh toán. Nếu BA cố gắng nhồi nhét mọi thứ vào **một trường Status duy nhất**, bạn sẽ phải nhân chéo các tổ hợp, tạo ra một ma trận trạng thái khổng lồ và rối rắm:

- Chưa giao hàng - Chưa thanh toán
- Chưa giao hàng - Đã thanh toán
- Đang giao hàng - Chưa thanh toán
- Đang giao hàng - Đã thanh toán…
Hậu quả là State Diagram trông như một “mạng nhện”, Developer phải viết hàng loạt lệnh if/else chằng chịt. Càng tệ hơn, nếu tương lai sinh thêm một quy trình mới (VD: Quy trình xuất hóa đơn), số lượng trạng thái sẽ bùng nổ theo cấp số nhân khiến hệ thống không thể bảo trì.
**Giải pháp (Trạng thái song song - Concurrent/Orthogonal States):**
Hãy “chẻ” chúng thành các **trường (field) trạng thái độc lập** chạy song song trên cùng một thực thể. Ví dụ thay vì 1 trường Order_Status gánh vác mọi thứ, hãy tách thành:

- **Delivery_Status (Vòng đời vận chuyển):** Chờ lấy hàng -> Đang đi giao -> Đã giao thành công -> Hoàn trả.
- **Payment_Status (Vòng đời thanh toán):** Chưa thanh toán -> Đang xử lý -> Đã thanh toán -> Đã hoàn tiền.
🗄️ Mô phỏng DB (Bảng Order): Hai trường hoạt động song song.
order_idtotal_amountpayment_statusdelivery_statusORD-001500,000đPAIDDELIVERINGORD-002150,000đUNPAIDPENDING_PICKUP
Mỗi trường sẽ có một State Diagram cực kỳ nhỏ gọn, tuyến tính và dễ hiểu. Giao diện (UI) hiển thị cho Admin cũng rành mạch hơn (chia làm 2 nhãn rõ ràng). Các vòng đời này chỉ “giao tiếp” với nhau thông qua **Điều kiện (Guard)**. (Ví dụ: Chỉ cho phép Shipper chuyển Delivery_Status sang Đã giao NẾU Payment_Status bằng Đã thanh toán - đối với đơn hàng không dùng COD).

### 7. Chuyển thể lên Diagram

Hãy dùng các công cụ thiết kế như [Draw.io](http://Draw.io), Figma, Visio, PlantUML hoặc Mermaid để trực quan hóa. Dùng hình tròn đen cho điểm bắt đầu (Start), hình tròn đen có viền cho điểm kết thúc (End), và các mũi tên có nhãn (Label) mô tả hành động.

### 8. Lập Bảng mô tả trạng thái (State Transition Table)

Nếu Diagram quá chằng chịt, hoặc để giúp Developer dễ code/Tester dễ test hơn, hãy lập một Ma trận trạng thái.

- **Cấu trúc bảng:** Trạng thái hiện tại | Sự kiện / Hành động | Điều kiện (Guard) | Trạng thái tiếp theo.
- Bảng này sẽ “bịt” mọi lỗ hổng logic mà hình vẽ đôi khi khó nhìn ra.
## Phần 2: 🔴 5 Lỗi “Kinh Điển” BA Thường Gặp Khi Vẽ State Diagram

Mặc dù nắm vững lý thuyết, trong thực tế các BA (đặc biệt là Junior) rất dễ mắc phải các sai lầm sau:

[!WARNING]
**1. Nhầm lẫn giữa State Diagram và Activity Diagram (Flowchart)**

- Dấu hiệu: Đặt tên trạng thái bằng **Động từ** thay vì Danh từ/Tính từ (VD: Đặt tên ô trạng thái là “Gửi email cho khách hàng” hoặc “Kiểm tra dữ liệu”).
- Cách sửa: Trạng thái phải là tình trạng của đối tượng tại một thời điểm. Hãy đổi thành Đang chờ kiểm tra, Đã gửi Email. Việc “Gửi email” là một hành động (Event) nằm trên mũi tên chuyển trạng thái, hoặc là hành động hệ thống tự làm (Entry/Exit action) bên trong trạng thái đó.
[!CAUTION]
**2. Rơi vào “Hố đen trạng thái” (Black hole) hoặc “Trạng thái rác” (Unreachable State)**

- Hố đen: Là trạng thái có mũi tên đi vào nhưng **không có mũi tên đi ra**, và nó cũng không được đánh dấu là Trạng thái kết thúc (Final State). Dữ liệu rơi vào đây sẽ bị kẹt vĩnh viễn trên hệ thống.
- Trạng thái rác: Một trạng thái được vẽ ra nhưng **không có bất kỳ mũi tên nào hướng tới nó** từ các trạng thái trước. Đoạn code này được dev viết ra nhưng sẽ không bao giờ được chạy.
[!IMPORTANT]
**3. Bỏ quên luồng ngoại lệ (Unhappy Path)**

- Dấu hiệu: Chỉ vẽ một đường thẳng tắp: Tạo mới -> Chờ duyệt -> Đã duyệt -> Thành công.
- Hậu quả: Khi người dùng đang ở Chờ duyệt nhưng muốn đổi ý Hủy thì sao? Khi gọi API đối tác bị Timeout thì rơi vào trạng thái nào? Việc thiếu các luồng Thất bại (Failed), Hết hạn (Expired), Đã hủy (Cancelled) là nguyên nhân số 1 gây lỗi sập hệ thống (Crash) hoặc kẹt logic.
[!NOTE]
**4. Không mô tả rõ điều kiện rẽ nhánh (Guard Conditions)**

- Lỗi: Từ trạng thái Chờ thanh toán, có 2 mũi tên cùng chỉ ra trạng thái Thành công và Thất bại với cùng một hành động “Hệ thống đối tác trả kết quả”, nhưng không ghi rõ điều kiện.
- Cách sửa: Trên mũi tên, ngoài tên hành động phải bổ sung thêm Điều kiện trong ngoặc vuông [ ]. VD: [Nếu balance >= amount] -> Thành công; [Nếu balance < amount] -> Thất bại.
[!TIP]
**5. Xác định sai thực thể (Gom chung nhiều vòng đời vào một biểu đồ)**

Sai lầm phổ biến: Lấy ví dụ ở nghiệp vụ **“Phát hành thẻ tín dụng”**, rất nhiều BA gộp chung trạng thái giao nhận vật lý của chiếc thẻ và trạng thái hoạt động logic của thẻ trên app vào thành **một biểu đồ duy nhất** (VD: vẽ 1 đường thẳng nối từ IN_TRANSIT -> DELIVERED -> WAITING_ACTIVATION -> ACTIVE). Điều này sai bản chất vì thực tế một chiếc thẻ tín dụng có thể bị user chọn TEMP_LOCKED (Khóa tạm thời) ngay cả khi nó vẫn đang trên đường IN_TRANSIT.

Cách sửa: Phải nhận diện được đây là 2 khía cạnh quản lý song song, chạy độc lập với nhau của cùng một chiếc thẻ. Cần tách bạch ra làm 2 State Diagram riêng biệt:

- **Vòng đời thẻ vật lý (Physical Card Delivery):** Chờ phát hành -> Đang in -> Đã phát hành -> Đang trung chuyển -> Đã giao KH -> Hoàn trả.
- **Vòng đời trạng thái thẻ (Logical Card Status):** Đóng -> Chờ kích hoạt -> Đang hoạt động <-> Khóa tạm thời -> Khóa vĩnh viễn.
[!WARNING]
 

**Tóm lại:** Kỹ thuật State Diagram là “Vũ khí tối thượng” giúp BA chốt logic với Developer cực kỳ hiệu quả. Một biểu đồ State tốt là biểu đồ mà Developer nhìn vào có thể hình dung ngay cấu trúc database và các hàm kiểm tra điều kiện (if/else). Hãy thử áp dụng ngay vào dự án hiện tại và review lại xem mình có đang mắc phải các sai lầm trên không nhé!