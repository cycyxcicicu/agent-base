# Danh mục 52 bộ quy tắc Review mã nguồn theo ngôn ngữ (Alibaba OCR)

**Loại: tham khảo.** Là trang ĐẦU VÀO để tra cứu toàn bộ quy tắc review chuyên sâu theo từng ngôn ngữ lập trình trong kho tri thức. Kế thừa chuẩn triết lý *"Favor precision over recall"* từ Alibaba Open-Code-Review.

Công cụ dòng lệnh đi kèm: `scripts/ocr.py` (chạy offline 100%, không cần npm hay Go).
- Xem quy tắc áp dụng cho file: `python scripts/ocr.py rule <đường-dẫn-file>`
- Quét kiểm định tĩnh theo luật: `python scripts/ocr.py check <đường-dẫn-file>`
- Xem trước danh sách file review: `python scripts/ocr.py preview`

## 1. Bảng tra cứu quy tắc theo ngôn ngữ lập trình

| Ngôn ngữ / Định dạng | Tệp quy tắc | Trọng tâm kiểm định chính |
|---|---|---|
| **Java** | `java.md` | NPE, Race condition check-then-act, N+1 query, truy vấn trong vòng lặp, thiếu break switch |
| **Python** | `python.md` | Mutable default arg, bare except, float equality, SQL string format, eval/exec, shell=True |
| **TypeScript / JavaScript / React** | `ts_js_tsx_jsx.md` | Hook dependency array, async race condition, prototype pollution, XSS innerHTML, memory leak event listener |
| **Go** | `go.md` | Goroutine leak, mutex lock copy, unhandled error, slice append race condition, nil pointer dereference |
| **Rust** | `rust.md` | Unsafe block, unwrap/expect trong production, deadlock, borrow checker bypass, integer overflow |
| **C / C++** | `c.md`, `cpp.md` | Buffer overflow, use-after-free, double free, memory leak, uninitialized variable, undefined behavior |
| **Kotlin** | `kotlin.md` | Coroutine scope, nullable type cast, blocking call trên dispatcher main, lateinit uninitialized |
| **Terraform / IaC** | `terraform.md`, `bicep.md` | Hardcoded credential, open security group (0.0.0.0/0), thiếu encryption at rest, public bucket |
| **Solidity / Smart Contract** | `solidity.md`, `vyper.md` | Reentrancy attack, integer under/overflow, unchecked call return, front-running, tx.origin auth |
| **SQL / Mapper DAO XML** | `mapper_dao_xml.md`, `prisma.md` | SQL Injection, thiếu index cho ORDER BY/WHERE, missing pagination, N+1 query |
| **Build & Config** | `package_json.md`, `pom_xml.md`, `build_gradle.md`, `cargo_toml.md`, `composer_json.md` | Dependency conflict, wildcards version, insecure registry, build reproducibility |
| **CI/CD & Workflows** | `github_workflows.md`, `github_config.md` | Pinned actions hash, secret exposure trong log, pull_request_target injection |
| **Format dữ liệu** | `json.md`, `yaml.md`, `properties.md`, `protobuf.md`, `graphql.md` | Schema validation, unsafe deserialization, circular reference, depth limit |
| **Ngôn ngữ khác** | `swift.md`, `php.md`, `r.md`, `ruby` (default), `zig.md`, `nim.md`, `haskell.md`, `ocaml.md`, `julia.md`, `elm.md`, `verilog.md`, `vhdl.md` | Theo quy chuẩn riêng từng ngôn ngữ |

## 2. Thứ tự ưu tiên & Cách áp dụng

1. **Khi Dev viết code:** Đọc tệp quy tắc của ngôn ngữ mình đang làm để tránh lỗi ngay từ đầu (Shift-Left).
2. **Khi Reviewer duyệt code:** Chạy `python scripts/ocr.py rule <file>` để tải đúng checklist kiểm thử; chỉ đánh dấu **Blocking (Critical/High)** khi có bằng chứng chắc chắn 100% là lỗi thật.

