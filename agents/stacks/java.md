# Stack: Java / Spring Boot

Lệnh dưới đây là mặc định phổ biến cho dự án Java/Spring Boot (dùng Maven hoặc Gradle). Nếu `PROJECT.md` ghi lệnh khác thì theo `PROJECT.md`.

## Lệnh mặc định

### Dùng Maven (Maven Wrapper)

| Việc | Lệnh (Windows / PowerShell) | Lệnh (Linux / macOS) |
|---|---|---|
| Cài / Khôi phục phụ thuộc | `.\mvnw.cmd dependency:go-offline` | `./mvnw dependency:go-offline` |
| Build | `.\mvnw.cmd clean package -DskipTests` | `./mvnw clean package -DskipTests` |
| Chạy ứng dụng | `.\mvnw.cmd spring-boot:run` | `./mvnw spring-boot:run` |
| Test (Unit & Integration) | `.\mvnw.cmd test` | `./mvnw test` |
| Lint / Checkstyle | `.\mvnw.cmd checkstyle:check` (nếu có) | `./mvnw checkstyle:check` |
| Format | `.\mvnw.cmd spotless:apply` (nếu có) | `./mvnw spotless:apply` |

### Dùng Gradle (Gradle Wrapper)

| Việc | Lệnh (Windows / PowerShell) | Lệnh (Linux / macOS) |
|---|---|---|
| Khôi phục phụ thuộc | `.\gradlew.bat build --dry-run` | `./gradlew build --dry-run` |
| Build | `.\gradlew.bat build -x test` | `./gradlew build -x test` |
| Chạy ứng dụng | `.\gradlew.bat bootRun` | `./gradlew bootRun` |
| Test | `.\gradlew.bat test` | `./gradlew test` |
| Format / Lint | `.\gradlew.bat spotlessApply` | `./gradlew spotlessApply` |

## Cấu trúc thường dùng

- Mã nguồn: `src/main/java/com/<cong-ty>/<du-an>/`
- Cấu hình & tài nguyên: `src/main/resources/` (chứa `application.yml` hoặc `application.properties`)
- Kiểm thử: `src/test/java/`, `src/test/resources/`
- Quản lý phụ thuộc: `pom.xml` (Maven) hoặc `build.gradle` / `settings.gradle` (Gradle)

## Quy ước code

- **Đặt tên**: `PascalCase` cho class, interface, enum, record; `camelCase` cho method, biến cục bộ, trường; `UPPER_SNAKE_CASE` cho constant (`static final`).
- **Package**: Toàn bộ chữ thường, theo domain đảo ngược: `com.<tochuc>.<duan>.<module>`.
- **Spring Boot**: 
  - Phân tầng rõ ràng: `Controller` → `Service` → `Repository` → `Entity` / `DTO`.
  - Không tiêm phụ thuộc qua trường `@Autowired`, ưu tiên tiêm qua constructor (kết hợp `@RequiredArgsConstructor` của Lombok).
  - Bắt lỗi tập trung bằng `@ControllerAdvice` / `@ExceptionHandler`.

## Cơ sở dữ liệu & Middleware (PostgreSQL, Redis, RabbitMQ)

- **Migration**: Dùng Flyway (`src/main/resources/db/migration/V<version>__<mo_ta>.sql`) hoặc Liquibase. Migration đã áp dụng lên môi trường thật không sửa, chỉ tạo migration mới.
- **Integration Test độc lập**: Bắt buộc dùng **Testcontainers** (`org.testcontainers:postgresql`, `testcontainers:rabbitmq`) hoặc Embedded Test Engine để các bài test tích hợp có thể chạy tự động ở máy local hoặc CI mà không cần người dùng tự bật container thủ công.

## File dùng chung (chỉ task được chỉ định mới sửa)

`pom.xml`, `build.gradle`, `settings.gradle`, `gradle/wrapper/*`, `.mvn/wrapper/*`, `src/main/resources/application*.yml`.

## Không sửa tay

`target/`, `build/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, migration đã áp dụng.

## Bẫy thường gặp trên Windows

- Trên Windows/PowerShell, phải chạy qua script wrapper có đuôi `.cmd` hoặc `.bat` (`.\mvnw.cmd` hoặc `.\gradlew.bat`), không gõ `./mvnw` trần nếu shell không nhận diện được bash runner.
- Thư mục `target/` hoặc `build/` rất nặng, **tuyệt đối không đặt trong thư mục OneDrive** để tránh xung đột file lock khi Maven/Gradle đang biên dịch.
- Đảm bảo biến môi trường `JAVA_HOME` trỏ đúng phiên bản JDK yêu cầu (JDK 17 hoặc 21 LTS).
