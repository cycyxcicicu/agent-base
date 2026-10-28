# Cẩm Nang Clean Code, Kỹ Thuật Refactoring & Google Engineering Practices

> **Loại: tham khảo.**  
> **Mã định danh:** `clean-code-and-refactoring-guide`  
> **Chuyên mục:** Kỹ Nghệ Viết Mã Sạch, Tái Cấu Trúc Mã Nguồn & Tiêu Chuẩn Review Code  
> **Nguồn gốc:** Martin Fowler (Refactoring: Improving the Design of Existing Code), Google Software Engineering Practices  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. Bản Đồ Mùi Mã Nguồn (Code Smells) & Kỹ Thuật Refactoring (Martin Fowler)

Refactoring là quá trình thay đổi cấu trúc bên trong của mã nguồn để làm nó dễ hiểu và dễ bảo trì hơn mà **hoàn toàn không làm thay đổi hành vi bên ngoài** của phần mềm.

### 1.1. Bảng Tra Cứu Code Smells & Kỹ Thuật Hóa Giải

| Mùi Mã Nguồn (Code Smell) | Dấu hiệu nhận dạng | Kỹ thuật Refactoring tương ứng |
|---|---|---|
| **Long Method (Hàm quá dài)** | Hàm dài hơn 25 dòng, làm nhiều việc, nhiều cấp thụt lề | **Extract Method:** Tách các khối lệnh logic thành hàm con có tên mang tính mô tả cao |
| **Large Class (Lớp quá ôm đồm)** | Class chứa hàng chục trường và phương thức (God Object) | **Extract Class:** Nhóm các trường và hàm có quan hệ mật thiết sang một Class mới |
| **Primitive Obsession (Lạm dụng kiểu nguyên thủy)** | Dùng chuỗi, số nguyên thô cho tiền tệ, số điện thoại, dải ngày | **Replace Primitive with Object:** Đóng gói thành Value Object (`Money`, `PhoneNumber`) |
| **Long Parameter List (Danh sách tham số dài)** | Hàm nhận từ 4 tham số trở lên | **Introduce Parameter Object:** Đóng gói các tham số thành một Command/DTO |
| **Switch Statements / Complex If-Else** | Câu lệnh `switch-case` hoặc `if-else` lặp đi lặp lại nhiều nơi | **Replace Conditional with Polymorphism:** Sử dụng Strategy Pattern hoặc Kế thừa đa hình |
| **Feature Envy (Ghen tị tính năng)** | Hàm của Class A gọi phương thức của Class B nhiều hơn dữ liệu của chính mình | **Move Method:** Chuyển phương thức đó sang Class B để đạt tính gắn kết cao (High Cohesion) |
| **Data Clumps (Dữ liệu đi thành chùm)** | Bộ ba `city`, `street`, `zipcode` luôn xuất hiện cùng nhau | **Preserve Whole Object:** Gom lại thành một Value Object `Address` |

### 1.2. Ví Dụ Refactoring: Thay Thế Câu Lệnh Điều Kiện Bằng Đa Hình

**❌ Trước khi Refactoring (Dễ gãy, vi phạm Open/Closed Principle):**
```java
public class ShippingFeeCalculator {
    public BigDecimal calculate(Order order, String carrier) {
        if ("JNT".equalsIgnoreCase(carrier)) {
            return order.getWeight().multiply(new BigDecimal("15000"));
        } else if ("GHN".equalsIgnoreCase(carrier)) {
            return order.getWeight().multiply(new BigDecimal("18000")).add(new BigDecimal("5000"));
        } else if ("VIETTEL_POST".equalsIgnoreCase(carrier)) {
            return order.getWeight().multiply(new BigDecimal("16000"));
        }
        throw new IllegalArgumentException("Hãng vận chuyển không hỗ trợ: " + carrier);
    }
}
```

**✅ Sau khi Refactoring (Replace Conditional with Polymorphism / Strategy Pattern):**
```java
public interface ShippingCarrierStrategy {
    boolean supports(String carrier);
    BigDecimal calculateFee(Order order);
}

@Component
public class JntShippingStrategy implements ShippingCarrierStrategy {
    public boolean supports(String carrier) { return "JNT".equalsIgnoreCase(carrier); }
    public BigDecimal calculateFee(Order order) {
        return order.getWeight().multiply(new BigDecimal("15000"));
    }
}

// Lớp điều phối sạch sẽ, tuân thủ nguyên lý Đóng/Mở (Open/Closed)
@Service
public class ShippingFeeService {
    private final List<ShippingCarrierStrategy> strategies;

    public ShippingFeeService(List<ShippingCarrierStrategy> strategies) {
        this.strategies = strategies;
    }

    public BigDecimal calculate(Order order, String carrier) {
        return strategies.stream()
            .filter(s -> s.supports(carrier))
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Không hỗ trợ: " + carrier))
            .calculateFee(order);
    }
}
```

---

## 2. Quy Chuẩn Kỹ Nghệ Phần Mềm Của Google (Google Engineering Practices)

Google quản trị mã nguồn quy mô hàng tỷ dòng lệnh dựa trên các tiêu chuẩn xem xét mã (Code Review Standards) cực kỳ nghiêm ngặt:

### 2.1. Tiêu Chuẩn Phê Duyệt Mã Nguồn (The Standard of Code Review)
> **Mục tiêu của Code Review:** Đảm bảo chất lượng toàn bộ mã nguồn của dự án được cải thiện liên tục theo thời gian.  
> Người review không đòi hỏi sự hoàn hảo tuyệt đối (Perfect Code), mà tìm kiếm **sự cải thiện chắc chắn (Net Improvement)**.

### 2.2. Quy Tắc Kích Thước PR Nhỏ (Small Changes / Small CLs)
- **Quy tắc vàng:** Một PR lý tưởng chỉ nên chứa từ **100 đến 300 dòng code** và chỉ tập trung giải quyết **DUY NHẤT một nhiệm vụ**.
- **Lợi ích:**
  - Reviewer duyệt kỹ hơn, phát hiện bug logic nhanh hơn.
  - Dễ dàng rollback nếu phát sinh sự cố production mà không làm ảnh hưởng các tính năng khác.
  - Hạn chế tối đa xung đột Git (Merge Conflicts).

### 2.3. Văn Hóa Phản Biện Lành Mạnh & Tôn Trọng (Google Code Review Etiquette)
1. **Phê bình mã nguồn, không phê bình con người:**
   - ❌ *"Bạn viết đoạn này khó hiểu quá."*
   - ✅ *"Đoạn logic này có thể khó hiểu cho người đọc sau. Chúng ta có thể tách hàm `calculateDiscount()` để rõ nghĩa hơn không?"*
2. **Phân biệt rõ giữa Yêu cầu bắt buộc và Đề xuất tùy chọn:**
   - Sử dụng tiền tố `Nit:` (Nitpick - tiểu tiết tùy chọn) cho những nhận xét nhỏ về phong cách, không chặn việc merge PR.
3. **Giải thích lý do tại sao:** Luôn đi kèm lời giải thích về rủi ro hiệu năng, bảo mật hoặc khả năng bảo trì thay vì chỉ nói "phải sửa thế này".
