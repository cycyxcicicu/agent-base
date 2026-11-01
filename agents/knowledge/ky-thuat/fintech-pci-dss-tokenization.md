# Chuyên Đề PCI-DSS v4.0, Tokenization & Kiến Trúc PAN Vaulting

**Loại: tham khảo.**
> **Phân vùng**: Security & FinTech Engineering  
> **Phân quyền truy cập (RBAC)**: `["security", "architect", "dev", "dba"]`  
> **Nguồn đối chuẩn**: PCI-DSS v4.0 Standard Requirements, Stripe Security Architecture, AWS KMS Best Practices  

---

## 1. Ranh Giới Cô Lập CDE (Cardholder Data Environment)
- **Định nghĩa CDE**: Là mạng logic hoặc vật lý chứa hệ thống lưu trữ, xử lý hoặc truyền tải dữ liệu thẻ thanh toán (Primary Account Number - PAN, Expiration Date, Cardholder Name).
- **Quy tắc phân vùng bất khả xâm phạm**:
  - Không bao giờ để hệ thống backend chính (Monolith hoặc các Microservices thông thường) tiếp xúc trực tiếp với PAN thô.
  - Vùng CDE phải nằm trong một VPC riêng biệt, chặn toàn bộ Ingress/Egress ngoại trừ cổng kết nối bảo mật tới cổng thanh toán ngân hàng (Acquiring Bank) hoặc Token Vault.
  - Nghiêm cấm tuyệt đối việc lưu trữ dữ liệu xác thực nhạy cảm (SAD - Sensitive Authentication Data) sau khi ủy quyền giao dịch, bao gồm: Full Track Data (từ tính), CVV2/CVC2/CID, mã PIN hoặc PIN block.

```
[Khách Hàng] 
      │ (1) Nhập thẻ trên Client iFrame
      ▼
[Token Vault Độc Lập (CDE)] ──(2) Mã hóa lưu PAN Vault (AES-256-GCM)
      │
      │ (3) Trả về token_id vô nghĩa (vd: tok_99ab71x)
      ▼
[Hệ Thống Backend App (Non-CDE)] 
      │ Chỉ lưu token_id, 4 số cuối (last4), thương hiệu (Visa/Mastercard)
      ▼
[Database Ứng Dụng] (Hoàn toàn nằm ngoài phạm vi kiểm toán PCI-DSS đắt đỏ)
```

---

## 2. Thiết Kế Token Vault & Cơ Chế Mã Hóa PAN
- **Chuẩn mã hóa**: **AES-256-GCM (Galois/Counter Mode)**.
  - Cung cấp cả tính bí mật (Confidentiality) lẫn tính toàn vẹn (Authenticity/Integrity).
  - Sử dụng IV (Initialization Vector) ngẫu nhiên 96-bit cho mỗi bản ghi; không bao giờ tái sử dụng cặp (Key, IV).
- **Quản lý khóa (Key Management Service - KMS)**:
  - Khóa chủ (Master Key / KEK - Key Encryption Key) được lưu giữ trong HSM (Hardware Security Module) đạt chuẩn FIPS 140-2 Level 3.
  - Khóa dữ liệu (DEK - Data Encryption Key) dùng để mã hóa PAN được sinh động và mã hóa ngược lại bởi KEK (Envelope Encryption).
  - Tự động luân chuyển khóa (Key Rotation) định kỳ 90 ngày hoặc ngay lập tức khi nghi ngờ lộ lọt.

---

## 3. Mã Nguồn Mẫu: Token Vault Envelope Encryption (Java / Spring Boot)

```java
@Service
public class PanVaultService {

    private final KmsClient kmsClient;
    private final SecretKey masterKek;

    public EncryptedPanRecord encryptPan(String rawPan) throws Exception {
        // 1. Sinh Data Encryption Key (DEK) 256-bit ngẫu nhiên
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(256, new SecureRandom());
        SecretKey dek = keyGen.generateKey();

        // 2. Mã hóa raw PAN bằng DEK với thuật toán AES-GCM
        byte[] iv = new byte[12]; // 96-bit IV
        new SecureRandom().nextBytes(iv);
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec spec = new GCMParameterSpec(128, iv);
        cipher.init(Cipher.ENCRYPT_MODE, dek, spec);
        byte[] cipherText = cipher.doFinal(rawPan.getBytes(StandardCharsets.UTF_8));

        // 3. Dùng AWS KMS (hoặc Master Key) để mã hóa ngược lại DEK (Envelope Encryption)
        byte[] encryptedDek = encryptDekWithKms(dek.getEncoded());

        // 4. Trả về bản ghi an toàn, chỉ giữ 4 số cuối làm masked pan
        String last4 = rawPan.substring(rawPan.length() - 4);
        String tokenId = "tok_" + UUID.randomUUID().toString().replace("-", "");

        return new EncryptedPanRecord(tokenId, cipherText, encryptedDek, iv, last4);
    }
}
```

---

## 4. Checklist Kiểm Định Bảo Mật Trước Khi Ra Mắt
- [ ] 100% Request log, debug log, APM trace không chứa bất kỳ chuỗi số nào có 13–19 chữ số thỏa mãn thuật toán Luhn.
- [ ] Không lưu trữ mã bảo mật CVV sau khi nhận kết quả thanh toán từ cổng.
- [ ] Truy cập SSH/Console vào máy chủ Token Vault bắt buộc qua Bastion Host với xác thực MFA và ghi hình phiên (Session Recording).

