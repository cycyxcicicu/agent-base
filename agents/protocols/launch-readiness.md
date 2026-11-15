# Quy Chuẩn Đánh Giá An Toàn, Bằng Chứng Agentic & Cổng Phát Hành (Launch Readiness)

> **Mã quy chuẩn: AGENTS-LR-8020**  
> Áp dụng cho: Mọi Agent, Lead, Architect, Dev, Reviewer, QA, SRE và Security.  
> Kế thừa từ thực chiến Meta Senior Staff: *Tree Model, Feature Gating, Adversarial Review, và Quy tắc 80/20.*

---

## 1. Mô Hình Cây & Phân Định Vùng Ảnh Hưởng (Tree Model & Blast Radius)

Khối lượng code do AI sinh ra rất lớn. Để tránh trở thành nút thắt cổ chai, toàn bộ codebase và các thay đổi phải được phân loại rõ ràng:

### A. Trunk Code (Phần Thân & Rễ — Blast Radius Lớn)
- **Định danh**:
  * Tầng Infrastructure, Middleware, Routing cấp hệ thống.
  * Xử lý mạng (*Networking*), Connection Pool, Thread Pool.
  * Quản trị phiên (*Session*), Bảo mật, Xác thực & Phân quyền (*IAM/Auth*).
  * Vùng lưu trữ trạng thái dùng chung (*Shared State, Central Reducers, Event Bus*).
  * Database Schemas, Migrations, và các Core Services/Libraries (`ws-library`).
- **Bản chất**: Cánh cửa một chiều (*One-way door*), nhiều downstream dependencies. Sai sót có thể làm sập toàn bộ hệ thống hoặc gây rò rỉ dữ liệu diện rộng.
- **Quy tắc Review**:
  * **BẮT BUỘC Deep Inspection**: Con người và Reviewer soi kỹ từng dòng (100% Line-by-line).
  * Phân tích triệt để side-effects, rủi ro concurrency (Deadlock, Race Condition), và tác động lên các downstream services.
  * **TUYỆT ĐỐI CẤM dùng Fast-Path** để bỏ qua review sâu dù diff chỉ có 1–2 dòng.

### B. Leaf Code (Phần Nhánh Lá — Blast Radius Hẹp)
- **Định danh**:
  * Các UI Component đơn lẻ, cô lập.
  * Endpoint API mới tinh chưa nối vào luồng chính của ứng dụng.
  * Worker xử lý nền cho một tác vụ phụ trợ độc lập.
  * Hàm tiện ích (Utility) cục bộ không có side-effects toàn cục.
- **Bản chất**: Độc lập (*Isolated*), không ảnh hưởng luồng vận hành chính.
- **Quy tắc Review**:
  * **Áp dụng Fast-Skim (Đọc lướt)**: Tập trung vào hợp đồng giao tiếp (Interface Contract) và kiểm tra bằng chứng xác thực (Agentic Validation Proof).
  * **ĐIỀU KIỆN TIÊN QUYẾT**: Leaf Code **BẮT BUỘC phải được bọc sau Feature Gate (Feature Flag / Config Toggle)**.

---

## 2. Thiết Kế Feature Gating Ngay Từ Bước Planning (DoR)

Để an tâm đọc lướt Leaf Code mà hệ thống vẫn an toàn tuyệt đối, nguyên tắc sống còn là **Feature Gating by Default**:

1. **Tách biệt ranh giới**:
   * Phần code tính năng mới phải nằm hoàn toàn phía sau Feature Flag (ví dụ: `flags.isFeatureEnabled('NEW_CHECKOUT')` hoặc biến cấu hình).
   * Điểm tiếp giáp (*Integration Layer*) với hệ thống cũ phải là điểm rẽ nhánh nhỏ nhất có thể (*Surgical Seam*).
2. **Quy tắc Kill-Switch**:
   * Trả lời câu hỏi sống còn: *"Nếu đoạn code mới bị lỗi 500 trên Production, tắt flag thì hệ thống cũ có lập tức trở lại bình thường 100% mà không cần redeploy không?"*
   * Nếu câu trả lời là **CÓ**: Mới đủ điều kiện nghiệm thu thiết kế (DoR).
   * Nếu câu trả lời là **KHÔNG** (ví dụ: sửa đổi đè lên bảng DB chung mà không có fallback): Tính năng bị coi là Trunk Code và phải áp dụng quy trình kiểm duyệt khắt khe nhất.
3. **Trạng thái cờ (Flag State)**: Mọi cờ tính năng mới khi commit vào nhánh chính mặc định phải ở trạng thái **OFF / FALSE**.

---

## 3. Thẩm Định Agentic & Mẫu Thẻ Bằng Chứng (Agentic Validation Proof)

Thay vì yêu cầu con người kéo nhánh về tự chạy thử, Agent phải tự chứng minh công việc của mình bằng chứng cứ xác thực (Proof-driven).

Mọi Task Card / PR khi bàn giao review bắt buộc phải có khối thông tin chuẩn sau:

```markdown
### 🛡️ AGENTIC VALIDATION PROOF
- **Code Category**: [ ] Trunk (Core/Infra/Shared) | [x] Leaf (Isolated/Decoupled)
- **Blast Radius**: Low | Medium | High
- **Feature Flag**: `ENABLE_NEW_FEATURE_X` (Default: `OFF`)
- **Kill-Switch Verified**: PASS (Tắt flag hệ thống fallback về luồng cũ trong < 1s, 0 side-effects)
- **Proof Matrix**:
  * Unit/Integration: <số test> tests PASS (Assert đúng logic nghiệp vụ, 0 mock hình thức rỗng)
  * Runtime Evidence: Lệnh thực thi thật, logs sạch, latency < <ngưỡng> ms
  * Visual/CDP Proof: PASS | Console errors: 0 | [screenshot.png](file:///...) (bắt buộc nếu có UI)
- **Confidence Score**: <X>/10 (Kèm lý do nếu < 9)
```

### Tiêu Chí Chất Lượng Cho Bằng Chứng
- **Chống Mock Rác (Meaningful Tests)**: Cấm viết test chỉ để kéo coverage (như assert != null mà không kiểm tra kết quả tính toán). Kiểm tra theo skill `ub-mode` và `test-value`.
- **Runtime Evidence**: Agent phải tự chạy thử qua terminal, đọc output thật, tự sửa nếu có lỗi trước khi nộp diff.
- **Visual Proof**: Task chạm Frontend bắt buộc chụp ảnh màn hình hoặc dùng CDP/Playwright xác nhận `console.error = 0`.

---

## 4. Adversarial Review Agent (Phản Biện Độc Lập Ngữ Cảnh)

### A. Khai Tử Văn Hóa Bắt Lỗi Vụn Vặt (No Nits)
- Các vấn đề về code style, formatting, khoảng trắng, import thừa, type annotation: **GIAO TOÀN BỘ CHO LINTER VÀ CỔNG TỰ ĐỘNG** (`hard-check.py`, `glossary-check.py`, Prettier/ESLint).
- Con người và Reviewer không lãng phí thời gian comment nits trên PR.

### B. Cơ Chế Adversarial Reviewer (Context-Blind)
- **Cấm Bẫy Thiên Vị (Confirmation Bias)**: Tuyệt đối cấm Agent vừa viết code tự chuyển mũ sang Reviewer trong cùng một phiên chat. Agent nắm toàn bộ lịch sử sẽ luôn có xu hướng bao biện và bảo vệ cách làm của mình.
- **Triển khai chuẩn**:
  * Khởi tạo một **Subagent hoàn toàn mới (Clean / Zero-Context)**.
  * Subagent Reviewer chỉ nhận 3 đầu vào:
    1. Tiêu chí nghiệm thu (`AC-xx` từ Task Card).
    2. Diff của Git (`git diff develop...<nhánh>`).
    3. Bộ quy tắc cứng (`HARD-RULES.json`, `open-code-review`).
  * Mục tiêu của Adversarial Reviewer: Tìm kiếm lỗ hổng logic, lỗi tranh chấp tài nguyên (Concurrency), bẫy bộ nhớ (OOM/N+1), vi phạm bảo mật (CSO), và mock hình thức.
- **Fast-Track Quick Fix**: Reviewer được quyền tự sửa trực tiếp các lỗi cực nhỏ ($\le 5$ dòng) để đóng task ngay, tránh ping-pong qua lại lãng phí token và thời gian.

---

## 5. Quy Tắc 80/20: Merge-Ready $\neq$ Launch-Ready

Quy trình release được chia làm 2 chặng tách bạch:

### Chặng 1: Merge-Ready Gate (80% Công việc)
- **Mục tiêu**: Đưa code an toàn vào nhánh tích hợp chung (`develop`/`main`).
- **Điều kiện PASS**:
  * Chạy qua `python scripts/merge-gate.py --branch <nhánh> --card <card>`.
  * Đúng phạm vi `scope_edit`, không đụng file cấm `scope_deny`.
  * Hard-check và Glossary-check sạch.
  * Có đầy đủ `AGENTIC VALIDATION PROOF`.
  * Feature Flag mặc định là `OFF`.

### Chặng 2: Launch-Ready Gate (20% Cuối — Yếu Tố Quyết Định Đẳng Cấp)
- **Mục tiêu**: Bật cờ tính năng cho người dùng thật (Production Go-Live).
- **Điều kiện PASS** (Kiểm tra qua `python scripts/launch-gate.py --card <card> --flag <flag-name>`):
  1. **Security CSO Audit**: Không có lỗ hổng IDOR, Injection, rò rỉ token/secret.
  2. **Performance & Scalability Audit**: Kiểm tra truy vấn DB (không N+1, có index), latency dưới ngưỡng SLA, không giữ long-running lock.
  3. **Human Taste & UX Audit**: Trải nghiệm thực tế mượt mà, micro-interactions chuẩn, tương phản màu sắc $\ge 4.5:1$, phím bấm chuẩn accessible.
  4. **Kill-Switch Drill**: Đã diễn tập kịch bản tắt cờ khẩn cấp, đảm bảo hạ tải êm ái (*Graceful degradation*).
  5. **Canary Deployment Plan**: Lộ trình mở traffic từng bước qua Feature Gate:
     $$\text{Internal / Beta (0\%)} \longrightarrow \text{Canary (5\%)} \longrightarrow \text{Staging (25\%)} \longrightarrow \text{General Availability (100\%)}.$$

