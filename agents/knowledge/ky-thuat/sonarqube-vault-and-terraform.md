# Cẩm Nang SonarQube Quality Gates, HashiCorp Vault & Terraform (IaC)

> **Loại: tham khảo.**  
> **Mã định danh:** `sonarqube-vault-and-terraform`  
> **Chuyên mục:** Kiểm Soát Chất Lượng Mã Nguồn, Quản Trị Bí Mật & Hạ Tầng Dưới Dạng Mã Nguồn (IaC)  
> **Nguồn gốc:** SonarSource SonarQube Documentation, HashiCorp Vault Docs, HashiCorp Terraform Docs  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. SonarQube — Chuẩn Kiểm Soát Chất Lượng Mã Nguồn & Quality Gates

SonarQube là nền tảng phân tích mã nguồn tĩnh (SAST) hàng đầu thế giới, áp dụng triết lý **Clean as You Go** (Mã nguồn mới viết phải sạch, không để tích tụ nợ kỹ thuật).

### 1.1. Bốn Tiêu Chí Phân Loại Lỗi Của SonarQube
1. **Bug (Lỗi mã nguồn):** Đoạn code chắc chắn gây sai sót hoặc ném ngoại lệ khi chạy runtime (ví dụ: `NullPointerException`, rò rỉ tài nguyên).
2. **Vulnerability (Lỗ hổng bảo mật):** Điểm yếu có thể bị tin tặc khai thác trực tiếp (SQL Injection, XSS, Hardcoded Secret).
3. **Security Hotspot (Điểm nghi vấn bảo mật):** Đoạn mã nhạy cảm cần con người kiểm tra thủ công (ví dụ: dùng thuật toán mã hóa cũ MD5, tắt kiểm tra chứng chỉ SSL).
4. **Code Smell (Mùi mã nguồn / Nợ kỹ thuật):** Đoạn code khó hiểu, dài dòng hoặc trùng lặp làm giảm khả năng bảo trì.

### 1.2. Tiêu Chuẩn Cổng Chất Lượng Chặn Release (Production Quality Gate)
Một Pull Request chỉ được phép merge khi thỏa mãn 100% các điều kiện trên mã nguồn mới (New Code):
- ✅ **0 New Bugs**
- ✅ **0 New Vulnerabilities**
- ✅ **Độ bao phủ kiểm thử (Coverage on New Code) $\ge 80\%$**
- ✅ **Tỷ lệ trùng lặp mã (Duplications on New Code) $< 3\%$**
- ✅ **Xếp hạng bảo trì (Maintainability Rating) đạt mức A** (Tỷ lệ nợ kỹ thuật $< 5\%$)

---

## 2. HashiCorp Vault — Quản Trị Bí Mật Tập Trung (Zero Trust Secrets Management)

Trong kiến trúc Enterprise, **tuyệt đối không lưu trữ thông tin mật (Mật khẩu DB, Private Key, API Token) dưới dạng văn bản thô (Plaintext)** trong file cấu hình `.env` hay `application.yml`.

```mermaid
flowchart LR
    App["Ứng Dụng (Spring Boot)"] 
    -->|1. Xác thực bằng K8s ServiceAccount| Vault["HashiCorp Vault Server"]
    Vault -->|2. Cấp phát Dynamic Secret (TTL 1 giờ)| App
    Vault -->|3. Tự động tạo User tạm thời| PG[("PostgreSQL Database")]
    App -->|4. Kết nối bằng mật khẩu tạm| PG
```

### 2.1. Hai Tính Năng Đột Phá Của Vault
1. **Dynamic Secrets (Mật khẩu động tự hủy):**
   - Thay vì dùng chung một mật khẩu database vĩnh viễn, ứng dụng yêu cầu Vault cấp quyền truy cập.
   - Vault tự động sinh một tài khoản PostgreSQL ngẫu nhiên (ví dụ: `v-token-xyz-123`) với thời hạn sống (TTL) 1 giờ. Khi hết hạn hoặc pod bị hủy, Vault tự động xóa tài khoản này trên PostgreSQL. Nếu hacker đánh cắp mật khẩu, mật khẩu đó cũng vô giá trị sau 1 giờ.
2. **Transit Secrets Engine (Mã hóa dưới dạng dịch vụ - EaaS):**
   - Ứng dụng không cần lưu giữ khóa mã hóa (Encryption Key) trong mã nguồn.
   - Khi cần lưu thông tin nhạy cảm (Số CCCD, Số thẻ ngân hàng), ứng dụng gửi dữ liệu thô sang Vault qua API. Vault mã hóa và trả về chuỗi `vault:v1:8hF...` để ứng dụng lưu vào CSDL.

---

## 3. HashiCorp Terraform — Hạ Tầng Dưới Dạng Mã Nguồn (Infrastructure as Code - IaC)

Terraform cho phép khai báo toàn bộ tài nguyên đám mây (VPC, Subnet, RDS, EKS, Redis) bằng ngôn ngữ **HCL (HashiCorp Configuration Language)** có thể quản lý phiên bản trên Git.

### 3.1. Vòng Đời Triển Khai 4 Bước Bắt Buộc
1. **`terraform init`:** Tải các Provider plugins (AWS, Azure, Kubernetes) và khởi tạo Backend.
2. **`terraform plan`:** So sánh trạng thái thực tế với mã nguồn khai báo, dự báo chính xác những gì sẽ được thêm (`+`), sửa (`~`) hoặc xóa (`-`). Bắt buộc review trước khi chạy thật!
3. **`terraform apply`:** Thực thi thay đổi lên đám mây.
4. **`terraform destroy`:** Hủy bỏ toàn bộ tài nguyên khi kết thúc thử nghiệm.

### 3.2. Quản Trị Trạng Thái An Toàn (Remote State & Distributed Locking)
File `terraform.tfstate` lưu trữ toàn bộ bản đồ hạ tầng thực tế.
> [!CAUTION]
> Tuyệt đối không commit file `.tfstate` lên Git vì file này chứa thông tin nhạy cảm và dễ gây xung đột hạ tầng.

**Mẫu cấu hình Backend Production (S3 + DynamoDB State Locking):**
```hcl
terraform {
  required_version = ">= 1.5.0"
  
  backend "s3" {
    bucket         = "gdt-terraform-states"
    key            = "production/accounting-platform.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "terraform-lock-table" # Khóa phân tán: Ngăn 2 kỹ sư apply cùng lúc
    encrypt        = true
  }
}
```

### 3.3. Đoạn Mã Khai Báo Cụm PostgreSQL Bằng Terraform Mẫu

```hcl
resource "aws_db_instance" "accounting_postgres" {
  identifier           = "accounting-postgres-master"
  allocated_storage    = 100
  max_allocated_storage = 500 # Tự động mở rộng dung lượng ổ đĩa
  storage_type         = "gp3"
  engine               = "postgres"
  engine_version       = "16.2"
  instance_class       = "db.r6g.xlarge"
  db_name              = "accounting_db"
  username             = "gdt_admin"
  password             = var.db_master_password # Nhận từ HashiCorp Vault
  
  multi_az             = true  # Tự động chuyển đổi dự phòng High Availability
  skip_final_snapshot  = false
  deletion_protection  = true  # Chống vô tình xóa mất CSDL
  
  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Service     = "accounting"
  }
}
```
