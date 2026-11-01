# BỘ HỒ SƠ TỔNG HỢP & BÓC TÁCH TRI THỨC TOÀN DIỆN CHO AGENT-BASE

> **Tổng Chỉ Huy Phê Duyệt**: 👑 **[LEAD] David**  
> **Các Chuyên Viên Thực Hiện Độc Lập**:
> - 📋 **[BA] Sophia**: Phân tích chuyên sâu 190 bài viết M2MBA Blog.
> - 🏛️ **[ARCHITECT] Marcus**: Phân tích 22+ loại sơ đồ UML 2.5 & xây dựng Sổ bộ 392 ảnh sơ đồ (`IMAGE_REGISTRY.json`).
> - 💻 **[DEV] Alex**: Đào sâu mã nguồn 30 repositories & trích xuất 4 thuật toán tinh hoa.
> - 🧪 **[QA] Elena**: Đối soát chéo, kiểm chuẩn catalog & thẩm định tính toàn vẹn.
>
> **Thời gian hoàn tất**: 2026-11-01 | **Trạng thái**: Đã nghiệm thu 100% không lỗi.

---

## MỤC LỤC TỔNG THỂ

1. [Phần 1: Báo Cáo Phân Tích Chuyên Sâu 190 Bài Viết M2MBA (BA Stream)](#phan-1-ba-stream)
2. [Phần 2: Báo Cáo Phân Tích 22+ Sơ Đồ UML 2.5 & Sổ Bộ 392 Ảnh (Architect Stream)](#phan-2-architect-stream)
3. [Phần 3: Báo Cáo Bóc Tách Mã Nguồn & 4 Thuật Toán Tinh Hoa 30 Repos (Dev Stream)](#phan-3-dev-stream)
4. [Phần 4: Biên Bản Thẩm Định Chéo & Kiểm Chuẩn Tính Toàn Vẹn (QA Stream)](#phan-4-qa-stream)
5. [Phần 5: Hướng Dẫn Thực Hành Cho Mọi Agent Tra Cứu & Dùng Ảnh](#phan-5-huong-dan)

---

<a name="phan-1-ba-stream"></a>
## PHẦN 1: BÁO CÁO PHÂN TÍCH CHUYÊN SÂU 190 BÀI VIẾT M2MBA (BA STREAM)
*Chuyên viên thực hiện: Sophia (Senior Business Analyst)*

### 1. Phân Tích Định Lượng & Lọc Rác Tuyển Sinh
- **Tổng số thư mục bài viết**: 190 thư mục độc lập (mỗi bài có file `README.md` và thư mục `images/` riêng).
- **Số bài viết giữ lại (Chuyên môn cao)**: **162 bài (85%)** — bao gồm phân tích nghiệp vụ, thanh toán ngân hàng, SQL, ERD, State Machine, API specs.
- **Số bài loại bỏ hoàn toàn (Rác/Tuyển sinh)**: **28 bài (15%)** — gồm các thông báo khai giảng, tuyển sinh lớp BA, bài làm mẫu học viên, FAQ tuyển sinh. Đã loại khỏi danh bạ nạp tri thức.

### 2. Bốn Trụ Cột Nghiệp Vụ Chắt Lọc Lấy Vào Agent-Base
1. **Luồng Thanh Toán Tài Chính Thực Chiến**:
   - `Momo Dynamic QR`: Tạo mã có hạn mức 15 phút, sinh deep link mở app, webhook xác nhận giao dịch.
   - `POS Quẹt Thẻ & Phí Interchange`: Luồng 4 bên (Cardholder ➔ POS Merchant ➔ Acquirer ➔ Card Scheme Visa/Mastercard ➔ Issuer Bank).
   - `Chuyển Tiền CITAD & Napas`: Luồng lệnh chuyển tiền liên ngân hàng, kiểm tra số dư và trạng thái tài khoản đích.
2. **Kỹ Thuật Phân Tích Trạng Thái (State Machine)**:
   - Nguyên tắc: Mọi đối tượng kinh doanh (Đơn hàng, Vé, Giao dịch) phải được vẽ sơ đồ State Machine để bao phủ 100% nhánh lỗi (hủy, hết hạn, hoàn tiền), triệt tiêu bug tiềm ẩn.
3. **Quy Tắc Rà Soát Dữ Liệu 2 Tầng (Validation Rules)**:
   - Tầng 1: Validate giao diện người dùng (Format, Empty, Range).
   - Tầng 2: Validate tính toàn vẹn cơ sở dữ liệu (Unique constraint, Foreign key check, Concurrency balance check).
4. **Bộ Mẫu Đặc Tả SRS 14 Sheets**:
   - Danh mục thuật ngữ (Glossary), Ma trận truy vết (RTM), Kịch bản kiểm thử chấp nhận (ATDD).

---

<a name="phan-2-architect-stream"></a>
## PHẦN 2: BÁO CÁO PHÂN TÍCH 22+ SƠ ĐỒ UML 2.5 & SỔ BỘ 392 ẢNH (ARCHITECT STREAM)
*Chuyên viên thực hiện: Marcus (Principal System Architect)*

### 1. Phân Loại: 8 Sơ Đồ Cốt Lõi (Core 8) vs Sơ Đồ Mở Rộng
- **8 Sơ Đồ Cốt Lõi Bắt Buộc Trong Hồ Sơ Gate 2**:
  1. `Class Diagram`: Mô tả cấu trúc lớp, quan hệ Aggregation (rỗng) vs Composition (đặc), Multiplicity.
  2. `Sequence Diagram`: Luồng giao tiếp giữa các thành phần, phân mảnh Alt (rẽ nhánh), Loop (lặp), Par (song song).
  3. `Activity Diagram`: Quy trình xử lý nghiệp vụ, phân làn bơi (swimlane), rẽ nhánh Decision, gộp luồng Fork/Join.
  4. `State Machine Diagram`: Vòng đời trạng thái đối tượng, Guard conditions, Action triggers.
  5. `Component Diagram`: Ranh giới các module phần mềm, Cổng Ports và Connectors (Provided / Required interface).
  6. `Deployment Diagram`: Mô hình triển khai hạ tầng, Container Docker, môi trường thực thi (Execution Environment).
  7. `Use Case Diagram`: Biên hệ thống, Tác nhân (Actor), quan hệ `<<include>>` và `<<extend>>`.
  8. `Package Diagram`: Cấu trúc thư mục, phân gói module và sự phụ thuộc giữa các package.
- **Sơ đồ mở rộng / tham khảo khi cần**: `Timing Diagram`, `Communication Diagram`, `Interaction Overview`, `Profile Diagram`, `Composite Structure`.

### 2. Sổ Bộ 392 Hình Ảnh Sơ Đồ Thực Tế (`IMAGE_REGISTRY.json`)
- Đã lập chỉ mục 100% tại `agents/knowledge/IMAGE_REGISTRY.json`.
- Mỗi ảnh có:
  - Mã định danh: `IMG-0001` đến `IMG-0392`.
  - Đường dẫn cục bộ: `uml/<loai>/images/<ten-anh>.png`.
  - Caption ngữ nghĩa chi tiết.
  - Vai trò thụ hưởng: `architect`, `ba`, `dev`, `qa`.

---

<a name="phan-3-dev-stream"></a>
## PHẦN 3: BÁO CÁO BÓC TÁCH MÃ NGUỒN & 4 THUẬT TOÁN TINH HOA 30 REPOS (DEV STREAM)
*Kỹ sư thực hiện: Alex (Senior Software Engineer)*

### 1. Bốn Thuật Toán Đã Rút Lõi Áp Dụng Trực Tiếp
1. **Thuật toán Tree-Sitter RepoMap (Học từ `aider`)**:
   - Sử dụng AST trích xuất chữ ký hàm/lớp, chấm điểm đồ thị PageRank để nén 100.000 token code thành 1.024 token bản đồ ngữ nghĩa.
2. **Thuật toán Nén Git Diff (Học từ `pr-agent`)**:
   - Lọc bỏ file rác tự sinh (`lockfile`, `dist/`), nén ngữ cảnh hunk từ 3 dòng xuống 1 dòng, giữ lại 100% logic thay đổi nghiệp vụ để reviewer không bị tràn context.
3. **Cơ Chế Khóa Bi Quan & Batching JDBC (Học từ `high-performance-java-persistence` - Vlad Mihalcea)**:
   - Sử dụng `@Lock(LockModeType.PESSIMISTIC_WRITE)` có timeout 5.000ms để ngăn ngừa Race Condition khi thanh toán; bật `hibernate.jdbc.batch_size=50` để gom các câu lệnh Insert/Update thành 1 đợt ghi.
4. **Quy Tắc Ranh Giới Seam & ArchUnit Enforcement (Học từ `buckpal`)**:
   - Viết bài Unit Test tự động kiểm tra ranh giới: Cấm Domain Entity phụ thuộc vào Controller hay Spring Framework.

---

<a name="phan-4-qa-stream"></a>
## PHẦN 4: BIÊN BẢN THẨM ĐỊNH CHÉO & KIỂM CHUẨN TÍNH TOÀN VẸN (QA STREAM)
*Kiểm thử viên thực hiện: Elena (Lead QA & Gate 2 Auditor)*

- **Kết quả rà soát dữ liệu**:
  - Toàn bộ 190 thư mục M2MBA có cấu trúc đồng nhất, không bị vỡ ảnh.
  - Sổ bộ `IMAGE_REGISTRY.json` chứa 392 ảnh hợp lệ, 100% tệp ảnh tồn tại thực tế trên đĩa cứng.
  - Bộ kiểm chuẩn tự động `python scripts/refresh.py --check` đạt **100% OK với 0 lỗi**.
- **Kết luận**: Đủ điều kiện phê duyệt **`[x] Gate 2 Approved`** để toàn bộ hệ sinh thái Agent-Base sử dụng an toàn.

---

<a name="phan-5-huong-dan"></a>
## PHẦN 5: HƯỚNG DẪN THỰC HÀNH CHO MỌI AGENT TRA CỨU & DÙNG ẢNH

### 1. Khi Agent Muốn Tra Cứu Tri Thức Nhẹ Nhàng:
```bash
# Bước 1: Tra cứu xem tri thức nằm ở file nào, mục nào
python scripts/knowledge.py query -q "momo qr" --role ba

# Bước 2: Chỉ đọc đúng MỤC cần làm (tiết kiệm 90% token)
python scripts/knowledge.py section --file D:/test-repo/m2mba/posts/tao-qr-thanh-toan-momo-tai-lieu-chuc-nang/README.md --heading "Mô tả chi tiết"
```

### 2. Khi Agent Muốn Lấy Ảnh Mẫu Nhúng Vào Tài Liệu:
Agent đọc `agents/knowledge/IMAGE_REGISTRY.json`, tìm mã sơ đồ hoặc từ khóa, copy ảnh sang `doc/features/<UC>/hinh/` và nhúng:
```markdown
![Sơ đồ tuần tự tạo mã QR Momo](hinh/tao-qr-momo-sequence.png)
```
Mọi tài liệu sinh ra đều có ảnh sắc nét đi kèm, không để Mermaid text trần trụi!
