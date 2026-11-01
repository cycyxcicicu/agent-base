# Cẩm Nang Kiến Trúc Sạch, Tối Ưu CSDL & 4 Giải Thuật Tinh Hoa

**Loại: tham khảo.**
> **Phân vùng**: Architecture, Backend Engineering & Database  
> **Phân quyền truy cập (RBAC)**: `["architect", "dev", "dba", "reviewer"]`  
> **Nguồn đối chuẩn**: 30 Repositories lớn tại `docs/research/30-repos-deep-dive.md` (Aider, PR-Agent, Vlad Mihalcea HPJP, BuckPal, Alibaba P3C)  

---

## 1. Giải Thuật 1: Tree-Sitter RepoMap (Học từ `aider/repo.py`)
- **Bài toán**: Làm thế nào để Agent hiểu được cấu trúc toàn bộ kho mã 100.000 tokens mà không làm cháy ngân sách context?
- **Nguyên lý của Aider**:
  1. Phân tích cây cú pháp trừu tượng (AST) của mọi file nguồn trong repo.
  2. Bóc tách danh sách định nghĩa (Class, Method signatures, Interfaces).
  3. Xây dựng đồ thị tham chiếu và áp dụng thuật toán **PageRank** để xếp hạng mức độ quan trọng.
  4. Nén toàn bộ cấu trúc thành chuỗi bản đồ ngữ nghĩa chỉ tiêu tốn **1.024 tokens**.
- **Ứng dụng**: Luôn dùng bản đồ tóm tắt AST thay vì đọc toàn bộ mã nguồn khi khảo sát repo.

---

## 2. Giải Thuật 2: Nén Git Diff Thông Minh (Học từ `pr-agent/algo/pr_processing.py`)
- **Bài toán**: Khi một PR lớn có hàng nghìn dòng diff, làm sao để Reviewer agent đọc và rà soát mà không bị tràn token?
- **Nguyên lý của PR-Agent**:
  1. **Lọc tệp tự sinh**: Tự động loại bỏ `package-lock.json`, `yarn.lock`, `dist/`, `.map`, file nhị phân.
  2. **Nén context hunk**: Giảm số dòng context không đổi bao quanh từ 3 dòng xuống 1 dòng.
  3. **Ưu tiên logic cốt lõi**: Sắp xếp diff theo trọng số: file chứa logic nghiệp vụ (`service`, `controller`) duyệt trước; file cấu hình hay test duyệt sau.

---

## 3. Giải Thuật 3: Khóa Bi Quan & Batching JDBC (Học từ Vlad Mihalcea)
- **Bài toán**: Race Condition khi nhiều giao dịch cập nhật số dư/đơn hàng cùng lúc, và hiệu năng kém do N+1 query.
- **Nguyên lý của Vlad Mihalcea**:
  1. **Khóa bi quan (Pessimistic Locking)**:
     ```java
     @Lock(LockModeType.PESSIMISTIC_WRITE)
     @QueryHints({@QueryHint(name = "jakarta.persistence.lock.timeout", value = "5000")})
     @Query("SELECT o FROM Order o WHERE o.id = :orderId")
     Optional<Order> findByIdWithPessimisticLock(@Param("orderId") UUID orderId);
     ```
  2. **Tránh N+1 Query**: Luôn dùng `JOIN FETCH` hoặc DTO Projection khi truy vấn quan hệ `@ManyToOne`.
  3. **JDBC Batching**: Thiết lập `hibernate.jdbc.batch_size = 50`, `order_inserts = true`, `order_updates = true` để gom các thao tác ghi dữ liệu thành một mẻ.

---

## 4. Giải Thuật 4: Ranh Giới Seam & ArchUnit Architecture Rules (Học từ `buckpal`)
- **Bài toán**: Code lâu ngày bị rò rỉ kiến trúc, Domain Entity bị phụ thuộc vào Spring Framework hay Controller.
- **Nguyên lý của BuckPal (Kiến trúc Lục giác - Ports & Adapters)**:
  - **Lõi Domain**: `Account`, `Order` hoàn toàn thuần túy Java, không có annotation `@Entity` hay `@Autowired`.
  - **Cổng vào/ra (Inbound/Outbound Ports)**: Giao tiếp hoàn toàn qua interface.
  - **Bộ kiểm thử ArchUnit tự động**:
    ```java
    @ArchTest
    static final ArchRule domain_must_not_depend_on_outside =
        noClasses().that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInAnyPackage("..adapter..", "..framework..");
    ```

---

## 5. Quy Chuẩn Đa Luồng & Bộ Nhớ Alibaba P3C
1. **Cấm tuyệt đối dùng `Executors.newFixedThreadPool()`**: Do hàng đợi `LinkedBlockingQueue` không giới hạn dung lượng dẫn đến nguy cơ OutOfMemory (OOM). Bắt buộc tự khởi tạo `ThreadPoolExecutor` có dung lượng hàng đợi (bounded queue) và chính sách từ chối (rejection policy) rõ ràng.
2. **Quy tắc so sánh hằng số**: Luôn viết `"CONSTANT".equals(variable)` thay vì `variable.equals("CONSTANT")` để triệt tiêu lỗi `NullPointerException`.

