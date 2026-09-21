# Báo Cáo Chiến Lược: Hấp Thụ Toàn Bộ Logic Tinh Hoa 17 Repo & Mở Rộng Hệ Thống Lên 20 Vai Trò

> **Tài liệu chiến lược kiến trúc tổng thể**  
> **Dự án:** `agent-base`  
> **Nguồn phân tích:** 17 Repository tại `D:\skills-quarantine\`  
> **Mục tiêu:** Bóc tách 100% logic nghiệp vụ, quy trình, tiêu chuẩn kỹ thuật đỉnh cao từ các repo; bản địa hóa cơ chế phân quyền; và mở rộng mạng lưới lên **20 vai trò chuyên biệt** hoàn chỉnh, không lược bỏ bất kỳ thành phần nào.

---

## 1. Triết Lý Cốt Lõi: "Tách Rời Logic Nghiệp Vụ Khỏi Lớp Cấp Quyền"

Hầu hết các bộ skill bên thứ ba gặp vấn đề ở **lớp thực thi (Execution/Permission Layer)**:
- Tự tiện chạy `git commit`, `git push` phá vỡ quy trình kiểm soát rủi ro.
- Tự ý cài gói toàn cục `npm i -g`, `pip install` làm rác máy.
- Gọi API ra ngoài, gửi dữ liệu telemetry.

Tuy nhiên, **lớp logic (Domain & Reasoning Logic)** của họ là thành quả kết tinh từ hàng nghìn giờ thực chiến của các kỹ sư hàng đầu thế giới (Y Combinator, Matt Pocock, Jesse Vincent, Google, Alibaba):
- Cách đặt câu hỏi bẻ khóa yêu cầu mơ hồ.
- Quy trình gỡ lỗi 4 pha không đoán mò.
- Kỹ thuật di chuyển cơ sở dữ liệu lớn không chết server (Zero-Downtime).
- Khung kiểm toán bảo mật 4 chiều.

👉 **Giải pháp của chúng ta:** **Giữ nguyên 100% logic thông minh đó, nhưng "thay ruột" tầng thực thi bằng cơ chế phân quyền chuẩn của `agent-base`**:
1. Thay `git commit` ngầm ➔ **Khối Commit Plan** chờ người dùng phê duyệt.
2. Thay `bash: full` tùy tiện ➔ **Bảng lọc lệnh nguy hiểm `/careful`** (`bash_ask` / `bash_deny`).
3. Thay việc cài đặt toàn cục ➔ **Kịch bản Python nội bộ chạy offline**.

---

## 2. Hệ Thống 20 Vai Trò Chuyên Biệt Toàn Diện (Không Lược Bỏ)

```
                                       ORCHESTRATOR
                         (Cổng thép HARD-GATE & Điều phối thực thi)
                                             │
     ┌───────────────────────────────────────┼───────────────────────────────────────┐
     ▼                                       ▼                                       ▼
[KHỐI SẢN PHẨM & NGHIỆP VỤ]             [KHỐI KỸ THUẬT & LẬP TRÌNH]             [KHỐI VẬN HÀNH & AN TOÀN]
 1. product (Product Lead) [MỚI]         7. dev (Fullstack & TDD)                13. devops (CI/CD/Infra)
 2. ba (Business Analyst & OCR)          8. mobile (Mobile Flutter/Swift) [MỚI]  14. sre (SRE & Điều tra sự cố) [MỚI]
 3. architect (Deep Modules & ADR)       9. ai-eng (AI/LLM Engineer) [MỚI]       15. dba (Zero-Downtime DB)
 4. analyst (Domain Modeling)           10. data-eng (Big Data & ETL) [MỚI]      16. security (CSO 4-Scope)
 5. designer (UI/UX & SVG 41 biểu đồ)   11. reviewer (Audit Diff & Rubrics)      17. qa (Flakey-Free Tests)
 6. writer (Living Docs & Release)      12. runner (Iron Law Verification)       18. debt-hunter (Sổ nợ DEBT.md) [MỚI]
                                                                                 19. researcher (R&D & Đánh giá)
                                                                                 20. (Phân quyền bảo mật chung)
```

### Chi Tiết 20 Chức Vụ & Trách Nhiệm Chuyên Môn

| STT | Vai trò | Miền Logic Tinh Hoa Tiếp Nhận | Thư mục quyền thao tác |
|:---:|---|---|---|
| 1 | **`orchestrator`** | HARD-GATE Brainstorming (3 nấc), Wait-What phanh khẩn cấp, Subagent Dispatching | `tasks/**`, `docs/risk/**` |
| 2 | **`product`** *(Mới)* | Plan CEO Review, Phân tích giá trị tính năng, Bẻ bài toán thành Spec, Định hình MVP | `docs/product/**`, `docs/roadmap/**` |
| 3 | **`ba`** | Domain Modeling (ép chuẩn từ ngữ), Intake đa định dạng kèm OCR đọc ảnh/PDF | `docs/requirements/**`, `docs/converted/**` |
| 4 | **`architect`** | Deep Modules (John Ousterhout), Nygard ADR Lifecycle, C4 Model, Plan Eng Review | `docs/adr/**`, `docs/spec/**`, `docs/design/**` |
| 5 | **`analyst`** | Grilling Clarification, Đối chiếu mâu thuẫn hệ thống, Ma trận khả thi | `docs/analysis/**`, `tasks/**` |
| 6 | **`designer`** | 41 mẫu biểu đồ SVG sắc nét, Design Token Audit, Thiết kế giao diện sống động | `docs/design/**`, `.agents/skills/diagram-design/` |
| 7 | **`writer`** | Living Docs Governance (tài liệu sống), Release Notes Generator từ commit logs | `docs/**`, `README.md`, `CHANGELOG.md` |
| 8 | **`dev`** | Bite-Sized TDD 2-5 phút, 4-Phase Systematic Debugging, Contract-First API | Toàn bộ mã nguồn sản phẩm (trừ file quản trị) |
| 9 | **`mobile`** *(Mới)* | Flutter/Dart Patterns, SwiftUI, React Native, Tối ưu hóa render di động | `mobile/**`, `apps/mobile/**`, `docs/mobile/**` |
| 10 | **`ai-eng`** *(Mới)* | LLM Pipeline, Prompt Optimization, Cost-Aware Budget, Chống Prompt Injection | `ai/**`, `prompts/**`, `docs/ai/**` |
| 11 | **`data-eng`** *(Mới)*| ETL Pipeline, Batch/Stream Data (Kafka/RabbitMQ), Kho dữ liệu OLAP | `data/**`, `etl/**`, `docs/data/**` |
| 12 | **`dba`** | Zero-Downtime Migration (431 dòng), PostgreSQL & Redis Mastery, Chống khóa bảng | `db/**`, `**/migrations/**`, `docs/db/**` |
| 13 | **`devops`** | Docker đa tầng tối ưu, Kubernetes Golden Path, GCP Playbooks | `.github/**`, `infra/**`, `deploy/**`, `Dockerfile*` |
| 14 | **`sre`** *(Mới)* | Read-Only Forensics, Điều tra sự cố, Benchmark tải, Lập Post-Mortem | `docs/postmortems/**`, `docs/runbooks/**` |
| 15 | **`security`** | CSO Audit 4 chiều (`--infra`, `--code`, `--supply-chain`, `--skills`), Promptfoo AI Safety | `docs/security/**`, `tasks/**` |
| 16 | **`reviewer`** | Delegation Mode Review, 4 Lăng kính chuyên gia, Kiểm tra nợ code | `tasks/**` (Chỉ đọc mã nguồn, xuất báo cáo duyệt) |
| 17 | **`debt-hunter`** *(Mới)*| Quét nợ kỹ thuật `# debt:`, Anti-Bloat Audit, Duy trì sổ nợ `DEBT.md` | `docs/DEBT.md` (Chỉ đọc toàn bộ repo) |
| 18 | **`qa`** | Condition-Based Waiting (chống flakey test), Kịch bản kiểm thử E2E | `tests/**`, `tasks/**` |
| 19 | **`runner`** | The Iron Law of Verification (chứng minh kết quả bằng log terminal thật) | Quyền thực thi lệnh test, không sửa code |
| 20 | **`researcher`**| Deep Research, Đánh giá công nghệ khách quan từ tài liệu độc lập | `docs/research/**`, `agents/knowledge/**` |

---

## 3. Bóc Tách 100% Logic Tinh Hoa Từ 17 Repo

1. **`domain-modeling` (Pocock)**: Rèn luyện ngôn ngữ miền, ép chuẩn thuật ngữ trong `CONTEXT.md`, phát hiện mâu thuẫn giữa code và lời nói.
2. **`codebase-design` (Pocock)**: Triết lý Ousterhout: Mô-đun sâu (Deep Modules), Seams (Đường nối), Locality (Tính cục bộ).
3. **`to-spec` & `to-tickets` (Pocock)**: Bẻ bài toán lớn thành Đặc tả kỹ thuật và các phiếu việc nguyên tử.
4. **`wait-what` & `handoff` (Pocock)**: Phanh khẩn cấp nhận thức khi yêu cầu phi lý, đóng gói trạng thái bàn giao phiên.
5. **`brainstorming` (Superpowers)**: Cổng thép HARD-GATE 3 nấc (*Spike* ➔ *Bounded* ➔ *Architectural*).
6. **`writing-plans` & `executing-plans` (Superpowers)**: Chu trình TDD hạt mịn 2 - 5 phút mỗi bước, bắt buộc kiểm chứng thực tế.
7. **`subagent-driven-development` (Superpowers)**: Điều phối subagent độc lập trong ngữ cảnh sạch, review kép sau mỗi task, nguyên tắc "Rulings, not stalls".
8. **`systematic-debugging` (Superpowers)**: 4 pha gỡ lỗi gốc rễ, `condition-based-waiting` chống flakey test, 5-Whys analysis.
9. **`finishing-a-development-branch` (Superpowers)**: Checklist vệ sinh nhánh trước khi merge.
10. **`/cso` (gstack)**: Kiểm toán bảo mật 4 chiều độc lập (`--infra`, `--code`, `--supply-chain`, `--skills`).
11. **`/plan-eng-review` (gstack)**: Khung Decision Brief `D<N>`, ELI10, Completeness Score, phát hiện SPOF và chịu tải 10x.
12. **`/plan-ceo-review` (gstack)**: Thẩm định giá trị sản phẩm, tính khả thi kinh doanh và ROI.
13. **`/careful` (gstack)**: Danh mục lệnh nguy hiểm cần hỏi xác nhận đối chiếu danh sách ngoại lệ an toàn.
14. **`/investigate` (gstack)**: Quy trình điều tra sự cố môi trường production chỉ bằng lệnh đọc (Forensics).
15. **`database-migrations` (ECC)**: Cẩm nang 431 dòng Zero-Downtime Migration (Expand-Contract, CONCURRENTLY index, batch update).
16. **`architecture-decision-records` (ECC)**: Quản lý vòng đời ADR chuẩn Nygard cho `docs/adr/`.
17. **`api-design` (ECC)**: Chuẩn thiết kế RESTful/gRPC contract-first, RFC 7807 error schema.
18. **`postgres-patterns` & `redis-patterns` (ECC)**: Tối ưu truy vấn, tránh N+1, chống Cache Stampede.
19. **`docker-patterns` & `kubernetes-patterns` (ECC)**: Docker đa tầng distroless, non-root, tài nguyên Pod chuẩn.
20. **`mobile-patterns` (ECC)**: Kiến trúc ứng dụng di động Flutter/SwiftUI/React Native.
21. **`ponytail-debt` & `ponytail-audit` (Ponytail)**: Cú pháp comment `# debt: <ceiling>, <upgrade>` và lệnh tự động thu hoạch sổ nợ `DEBT.md`.
22. **`action-first communication` (i-have-adhd)**: Đưa lệnh/file lên đầu dòng, số hóa nhiệm vụ, ước lượng thời gian, triệt tiêu văn rườm rà.
23. **`open-code-review-delegate` (Alibaba)**: Phân loại file diff thông minh và áp rule review chuẩn mà không tốn API ngoài.
24. **`llm-redteam-taxonomy` (Promptfoo)**: Phân loại lỗ hổng AI: Prompt Injection, Jailbreak, Tool-Call SSRF, Data Leakage.
25. **`google-cloud-playbooks` (Google Skills)**: Playbook hạ tầng GKE, Cloud Run, Cloud Logging, IAM.
26. **`diagram-design` (Cathryn Lavery)**: 41 mẫu biểu đồ kiến trúc SVG trực quan.
27. **`markitdown` (Microsoft)**: Intake tài liệu Word, Excel, PDF, PowerPoint sang Markdown kèm OCR đọc ảnh.
