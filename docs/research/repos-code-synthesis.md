# BÁO CÁO TỔNG HỢP MÃ NGUỒN & 4 GIẢI THUẬT TINH HOA TỪ 30 REPOSITORIES (DEV STREAM)
> Kỹ sư thực hiện: **Alex (Senior Software Engineer)** | Thời gian: 2026-11-01 12:35:11

## 1. BẢNG PHÂN BỔ 30 KHO MÃ THEO 3 TRỤ CỘT KỸ THUẬT

| Nhóm Trụ Cột | Các Repositories Tiêu Biểu | Mục Tiêu Rút Lõi Kiến Trúc |
|---|---|---|
| **Trụ Cột 1: Swarm & Agent Orchestration** | `AutoGPT`, `ChatDev`, `MetaGPT`, `crewAI`, `devika`, `langgraph`, `reflexion`, `aider` | Cơ chế điều phối, StateGraph, RepoMap nén token, vòng lặp phản tỉnh |
| **Trụ Cột 2: Clean Architecture & Database** | `buckpal`, `domain-driven-hexagon`, `high-performance-java-persistence`, `p3c`, `spring-petclinic`, `restful-api-guidelines` | Ranh giới Seam, ArchUnit test, JPA batching, Khóa bi quan, Problem Details RFC 7807 |
| **Trụ Cột 3: Testing, Evaluation & QA** | `SWE-bench`, `playwright`, `cucumber-common`, `pr-agent`, `claude-cookbooks` | Nén git diff, kịch bản BDD 1-1 TestLink XML, đánh giá regression patch |

## 2. BỐN GIẢI THUẬT TINH HOA RÚT TRÍCH TRỰC TIẾP TỪ MÃ NGUỒN THỰC TẾ

### GIẢI THUẬT 1: TREE-SITTER REPOMAP (RÚT TỪ `aider/repo.py`)
- **Vấn đề**: Một repo có 100.000 tokens mã nguồn, nếu nhồi vào prompt sẽ gây cháy ngân sách và loãng ngữ cảnh.
- **Giải pháp của Aider**: Dùng bộ phân tích AST trích xuất Class signatures, Method names, sau đó dùng thuật toán PageRank đồ thị để chọn ra đúng 1.024 token biểu tượng quan trọng nhất.
```python
# Mã nguồn trích xuất logic rút gọn từ Aider TreeContext
def extract_repo_map_signatures(source_files: list[Path], max_tokens=1024) -> str:
    ast_tags = []
    for f in source_files:
        # Trích xuất class / def / interface
        tags = parse_ast_definitions(f)
        ast_tags.extend(tags)
    ranked = pagerank_graph_sort(ast_tags)
    return render_compact_map(ranked, budget=max_tokens)
```

### GIẢI THUẬT 2: GIT DIFF COMPRESSION (RÚT TỪ `pr-agent/algo/pr_processing.py`)
- **Vấn đề**: Git diff của một Pull Request lớn có thể dài hàng chục nghìn dòng (chứa lockfile, build assets, whitespace).
- **Giải pháp của PR-Agent**: Bộ lọc 3 bước: (1) Loại bỏ file tự sinh (`package-lock.json`, `dist/`), (2) Nén hunk context từ 3 dòng xuống 1 dòng, (3) Ưu tiên diff các file logic nghiệp vụ.
```python
# Logic nén diff thông minh
def compress_git_diff(raw_diff: str, max_tokens=4000) -> str:
    cleaned = remove_generated_and_lockfiles(raw_diff)
    hunks = parse_diff_hunks(cleaned)
    return prioritize_and_trim_hunks(hunks, token_limit=max_tokens)
```

### GIẢI THUẬT 3: JPA PESSIMISTIC LOCKING & BATCHING (RÚT TỪ VLAD MIHALCEA)
- **Vấn đề**: Khi thanh toán hoặc trừ số dư ví, 2 request đồng thời dẫn đến Race Condition (mất tiền hoặc nhân đôi tiền).
- **Giải pháp của Vlad Mihalcea**: Khóa hàng mức database bằng `LockModeType.PESSIMISTIC_WRITE` có timeout tường minh, kết hợp JDBC batching.
```java
// Khóa bi quan hàng đơn hàng kèm Timeout 5s chống Deadlock
@Lock(LockModeType.PESSIMISTIC_WRITE)
@QueryHints({@QueryHint(name = "jakarta.persistence.lock.timeout", value = "5000")})
@Query("SELECT o FROM Order o WHERE o.id = :orderId")
Optional<Order> findByIdWithPessimisticLock(@Param("orderId") UUID orderId);
```

### GIẢI THUẬT 4: ARCHUNIT ARCHITECTURE ENFORCEMENT (RÚT TỪ BUCKPAL)
- **Vấn đề**: Sau vài tuần phát triển, Dev thường vô tình import Controller hoặc JPA Repository vào Domain Entity, phá vỡ tính độc lập.
- **Giải pháp của Tom Hombergs**: Viết bài Unit Test tự động quét bytecode ép ranh giới kiến trúc.
```java
// Kiểm thử ranh giới Lục giác tự động trong CI/CD
@ArchTest
static final ArchRule domain_must_not_depend_on_adapters = 
    noClasses().that().resideInAPackage("..domain..")
    .should().dependOnClassesThat().resideInAnyPackage("..adapter..", "..controller..");
```

