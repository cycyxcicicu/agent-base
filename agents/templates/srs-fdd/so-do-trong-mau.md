# Các sơ đồ trong mẫu SRS_FDD và file Copilot — loại gì, vẽ thế nào, dùng khi nào

Đã **xem trực tiếp từng ảnh** (tách từ `doc/quy-trinh/template/03-srs-fdd-template-v3/goc/SRS_FDD_Template-v3.0.xlsx` — 41 ảnh — và `_SRS_FDD_AI-Agent-Copilot.xlsx` — 13 ảnh) ngày 2026-10-17. Ảnh nằm trong gói xlsx (`xl/media`), vị trí = (sheet, dòng neo). Một số ảnh quá nhỏ/ quá lớn nên **chữ trong sơ đồ không đọc hết**; phần "Nội dung" bên dưới chỉ ghi những gì nhìn rõ.
> Ảnh trong **mẫu** là ví dụ lấy từ các dự án khác nhau (quản lý trung tâm anh văn, nền tảng tạo content Toktak, hệ thống tài sản công, tin tức…) — học **cách vẽ**, không lấy nội dung. Quy tắc đã tóm ở mục 3.

## 1. Danh mục sơ đồ trong **mẫu** v3.0

### `DauMucTaiLieuCanLam` — "mục tiêu thiết kế" (đọc để hiểu thiết kế đi từ trên xuống dưới)
| Dòng | Ảnh | Nội dung |
|---|---|---|
| 39 | image13 | Ghép nhiều sơ đồ: *quy trình nghiệp vụ → mô hình triển khai → component diagram → use-case → màn hình đăng nhập → sequence diagram → bảng đặc tả use-case* (mũi tên đỏ chỉ chiều thiết kế từ tổng quan xuống chi tiết) |
| 62, 67 | image10, image14 | Kiến trúc vật lý 3 lớp (người dùng nội bộ/ ngoài, LB/ proxy, cụm máy chủ ứng dụng, staging, máy chủ đồng bộ ETL, cụm CSDL, SAN) và chuỗi *Layer 01 → 02 → 03 → Application Components → class diagram* |
| 62, 86 | image17, image5 | Mind-map kỹ năng **Software Architect** (kiến trúc, kỹ năng, vận hành, design pattern, tools, API/ tích hợp, dữ liệu, bảo mật) + khung **Need → Solution → User story**; sơ đồ **trục tích hợp** (danh mục dùng chung, phần mềm nghiệp vụ 01…N, kho CSDL) |

### `Component_Detail_Design` — bức tranh lớn
| Dòng | Ảnh | Loại | Nội dung/ cách vẽ |
|---|---|---|---|
| 12 | image8 | Sơ đồ khái niệm | 6 lớp lồng nhau: *Chương trình → Dự án → Tác vụ → Tiểu tác vụ → Gói công việc → Mức độ nỗ lực*, mỗi lớp kèm "tài liệu/ mô hình tương ứng" (cầu nối WBS ↔ tài liệu) |
| 12 (cột 7) | image7 | **Business flow (BPMN pool/ lane)** | Pool "hệ thống", 4 lane (Marketing, Chuyên môn/ Đào tạo, Thư viện, Kế toán); Start/End, các hộp "quy trình con" nối bằng mũi tên — ví dụ chuẩn của business flow cấp cao |
| 24 | image21 | Mũi tên 4 bước | *Business Analysis → Logic Analysis → System Analysis → UI/UX* (thứ tự phân tích) |
| 26 | image2 | **WBS dạng cây** | Project → Phase/Deliverable → Work package → Activities |
| 29 (cột 7) | image15 | Business flow chi tiết | Lưu đồ lớn cả nghiệp vụ trung tâm (khảo sát → xây chương trình → mua sắm → xếp lớp → mượn trả tài liệu → kiểm kê → báo cáo), có hình thoi quyết định, tài liệu/ phiếu |
| 73 | image4 | **Luồng màn hình** | Sơ đồ chuyển giữa các màn (chữ rất nhỏ, mỗi bước đánh số tròn, nhánh lỗi màu đỏ) |
| 95 | image1 | **Wireframe board** | Bảng Figma: hàng chục màn hình thu nhỏ, mũi tên nhãn "Success/ Fail/ Cancel…" nối màn với màn |
| 138 | image16 | **Component/ package diagram** | Hệ thống chia module A…L (đăng nhập, giáo viên, học viên, lớp học, chương trình, kho tài liệu, chi phí…), mỗi module chứa các chức năng (B.1, B.2…), mũi tên "dùng" giữa module — nền của danh sách chức năng |
| 164 | image20 | **Cây chức năng** | Hệ thống → Quản trị hệ thống → Quản lý tài khoản/ thông tin người dùng/ nhóm người dùng → các chức năng lá (ô xanh = đã chọn làm) |
| 164 (cột 9) | image18 | **Khung User-Story Map** | *User Need → Epic → User story → Tasks + Acceptance criteria* (kèm "It's done when…") |
| 195, 201 | image6, image24 | **Use-case diagram** + **package "use"** | Actor (Admin, CXO, User — "extends"), hình ôvan use-case nối bằng mũi tên đỏ/ xanh, quan hệ *Use*; và 5 package quản lý tài khoản/ nhóm/ phân quyền/ danh sách chức năng |
| 222 | image23 | **Component diagram theo luồng dữ liệu** | Các bước đánh số 1–9 (thu thập → OCR → tối ưu thông tin → blog/ video/ hình → đăng SNS), nét đứt gom nhóm, dịch vụ ngoài (Google Vision) |
| 245 | image22 | **Deployment diagram** | User → Internet → Firewall → Proxy/ Load balancer → 3 Web Server → Cache/ FTP/ DB; AD server; biểu tượng cơ sở dữ liệu đồng bộ |
| 247 | image19 | **Sơ đồ service tích hợp** | ECMS Web Server ↔ AD Server qua 6 REST service (đăng ký/ cập nhật/ đổi mật khẩu/ xóa/ tìm nhanh/ tìm chi tiết), ghi `HTTPS, Port 443, POST, REST & JSON`, kèm JSON mẫu |
| 271 | image10 | **System architecture vật lý** | (cùng ảnh ở trên) |
| 275 | image5 | **Giải pháp trao đổi giữa hệ thống** | "Trục tích hợp" với đánh số luồng 01/02/03 |
| 298 | image17, image11 | Kiến thức kiến trúc + **MVVM** | Mô hình Model–ViewModel–View (binding/ commands) kèm giải thích từng vai trò |
| 323 | image40 | **Chi tiết một layer** | Layer 01 (thông tin cá nhân, thực hiện mua) → Layer 02 → Layer 03 (quét QR, OTP, thanh toán) + Application Components: cách **khoan sâu từng tầng** |

### `Functions_Services_Detail_Desig` — chi tiết một chức năng
| Dòng | Ảnh | Loại | Nội dung/ cách vẽ |
|---|---|---|---|
| 28 | image37 | **Wireframe màn danh sách** | "Danh sách Học Viên": ô tìm kiếm nhanh + nút Tìm kiếm/ Tìm kiếm nâng cao, icon tải/ in/ chọn cột, bảng (checkbox, ID link, các cột, nút sửa/xóa), phân trang (số dòng/ trang, trang x/y), nút Add new/ Delete — **mỗi nút/ vùng có dòng Business Rules đối ứng ở cột H** |
| 50 | image27 | Wireframe form + popup | Form **tìm kiếm nâng cao** (mã, họ tên, ngày sinh → lịch chọn ngày, tỉnh/ quận/ xã → dropdown) |
| 67 | image25 | Service tích hợp | (như image19) |
| 129 | image28 | **Activity diagram swimlane** | 2 làn "Người dùng | System"; Start, hành động, hình thoi "kiểm tra thông tin", nhánh hợp lệ/ không hợp lệ, End; nhãn mũi tên "Gửi lệnh/ Trả dữ liệu/ Hiển thị kết quả" |
| 129 (cột 7) | image26 | Phác thảo tay | Chuỗi log theo BatchID (ví dụ cách ghi log cho từng bước) |
| 136 | image34 | **Sequence diagram** | Các lifeline: Customer, boundary, Controller, Redis, WebSocket/ Notification, MySQL, Excel, LogFiles/ Log Shipper, Slack; khung `LOOP`, khung điều kiện `Content Creation fails`, số bước, mũi tên liền (gọi) và đứt (trả về) |
| 168, 171, 174 | image30, image31, image33, image29 | **ERD** | (a) chuỗi *Bài toán → mô hình ER → mô hình quan hệ → Database*; (b) ERD hệ thống trung tâm: bảng có `PK/FK`, kiểu dữ liệu, quan hệ 1–n; (c) ERD News: Category, Article, Comment, User, Like…, kí hiệu chân quạ; (d) **kí hiệu thuộc tính** (đơn trị, đa trị, dẫn xuất, khóa) |

### Sheet khác
- `WBS_Planning` (dòng 17–19): **3 sơ đồ luồng** `image3/9/12` — cùng một thiết kế crawl dữ liệu qua **3 phiên bản** (1: gọi virtual web + consumer; 2: thêm producer/ message queue/ payload; 3: thêm browser pool, manage scenarios/ consumers). Dùng để **minh họa từng task/ phương án** trong WBS.
- `Actors_Peronas` (dòng 10): `image36` **thẻ Persona** (Name/ Age/ Work/ Location, Bio, Motivations, Goals, Frustrations, Interests, Quotes).
- `TDD-TestScenario`: `image38` (bảng user-flow Figma: kiểm tra IP → login → thanh toán Korea/ Global → deliver/ archive), `image35` (**sơ đồ đi kiểm thử** i18n: các bước đánh số, nhánh Dịch đủ/ Dịch đúng/ Giao diện không lỗi, ký hiệu hoàn thành), `image32` (**site map** theo nhóm: Home, Create Content, My Content, Payment, Customer Service, Notification, My Page…) — "đi hết các trang trong site map" là cơ sở của kịch bản test.
- Sheet `20210620`: `image41` **ảnh màn hình** (hộp thoại + thông báo thành công/ lỗi kèm mã lỗi 1023) + bảng *Screen Items* (Item Name, Item Type, IOE, Required, Data Type, Digits, Default, Note) — mẫu mô tả **từng ô** trên màn hình.

## 2. Sơ đồ trong file **Copilot** đã điền (dự án thật)
| Sheet, dòng | Ảnh | Loại | Nội dung |
|---|---|---|---|
| `Component_Detail_Design` 12 | image8 | WBS 6 lớp | (như mẫu) |
| — 55 | image2 | **Package diagram hệ thống** | AI Content Generators (StoryBoard, Space, OneTake) / AI Agent (PlayWright, AI-Agent, Planner) / AI Content Gent / System (logging, security, monitoring) / ML / AI-Search / Data / Virtualize, mũi tên hai chiều |
| — 85 | image1 | **Component 3 tầng** | Interaction Layer (Real-time, Input Handling, Stateful Chat, Output Handler) · Agentic Orchestrator (Planner, Tools Use theo ReAct) · Existing components (Scraper, Image/ Video Generator) · AWS Services (S3, Search, AI Services, Redis session, Vector DB) |
| — 112 | image4.jpg | **Kiến trúc phần mềm + luồng đánh số** | Luồng (1) Login → (2) lưu session → … → (12) lấy thông tin chat; khối `Agents` (orchestrators, nodes, states, tools, prompts), `apps` (apis/ services/ repos/ models), `Core` (llm_providers, memory adapters, db MySQL/ Mongo, config); cột trái ghi **chức năng cần chuyên sâu** và **API cần xây dựng** |
| — 156 | image12.jpg | Sơ đồ phối hợp **đội/ hệ thống** | Data Team / ML Team / AI Team / Content Pilot Team: dữ liệu → phân loại → embedding → RAG → Agent API/ worker nodes/ tools |
| `Use-Case01-…` 11 | image11 | **Sequence diagram 4 transaction** | Lifeline User, ChatBot UI, ChatApi, 4 Node, AgentStates, ChatBotAI; mỗi *Transaction* được **khoanh bằng ngoặc + ghi chú** (Xác định loại content → Khởi tạo form → Xác nhận dữ liệu → Xác nhận kịch bản), bước đánh số `1.1, 1.2…` khớp luồng chính trong bảng use-case |
| — 70 | image3 | **Activity swimlane 7 làn** | User / ChatUI / Chat_Bot_Agent / Content_Creator_Agent / User_manual_Agent / BE-Services / LLM; node (PrepareStateNode, RetrieveMemoryNode, CallLLMNode, RouterNode, RequirementAnalyzer, DynamicFormGenerator, ScriptDrafting, ConfirmFormGenerator, FinalPublisher), vòng lặp đánh giá kịch bản |
| — 121 | image7 | **Class/ state diagram chi tiết** | Các lớp `AgentState`, `AnalyzerResult`, `VideoScriptModel`, `CustomForm`, `HTMLCustomInputFields`… kèm **chú thích bước xử lý** của từng node bằng chữ |
| — 213 | image9 | **ERD/ class** | Collection `chat_topics`, `chat_message`, `chat_session`, `chat_search_index`, `User`; `AgentState`, `UserProfile`, `AggregatedContext` — có kiểu, ghi chú tiếng Việt, quan hệ 1–n/ 1–1 |
| — 341 | image10 | **Mockup có chú thích API** | Cửa sổ chat + custom form; các vòng số ①–⑦ nối tới **API tương ứng** (`/chat/send`, `/chat/history`, `/chat/search`, `/chat/interaction/context`, `/feedback`, `/chat/upload`, real-time) kèm đoạn mô tả hành vi bên cạnh |
| — 447 | image5 | **Danh sách API từ một màn hình** | "Chat-Form" nối tới 7 API, mỗi API một ô + mô tả ngắn |
| `20210620` | image13 | Màn hình mẫu | (như mẫu) |

## 3. Chuẩn vẽ rút ra (áp dụng khi viết SRS chức năng)
1. **Mỗi sơ đồ phải có tiêu đề + chú thích bước/ số** và **nối với văn bản**: số bước trong sơ đồ = số bước trong bảng use-case (`1.1, 1.2…`); số vòng ①–⑦ trong mockup = số service trong mục API.
2. **Theo loại sơ đồ:**
   - *Business flow:* BPMN **pool/ lane** theo bộ phận/ actor, Start/End, hình thoi quyết định.
   - *Luồng màn hình + wireframe:* mỗi màn một ID; mũi tên ghi **điều kiện** (Success/ Fail/ Cancel); nhánh lỗi màu đỏ.
   - *Use-case diagram:* actor ở ngoài, "Use/ Extends" ghi rõ; *User-Story Map*: Activity → Task → Release 1 (MVP)/ Release 2.
   - *Sequence:* lifeline **boundary / controller / service / DB / hệ thống ngoài**; gom bước thành **transaction** có ghi chú; khung `alt/ opt/ loop` cho nhánh; mũi tên đứt = trả về.
   - *Activity:* swimlane theo vai (Người dùng | System | …), nhãn mũi tên là hành động.
   - *ERD/ class:* tên bảng/ entity thật, `PK/FK`, kiểu dữ liệu, bội số (1, 0..n), chú thích ý nghĩa cột.
   - *Component/ package:* nhóm theo module/ layer, mũi tên "use" một chiều, ghi giao thức khi qua ranh giới (HTTPS/ REST/ JSON/ port).
   - *Deployment:* user → firewall → LB/ proxy → web server → cache/ DB/ file; ghi tên server thật.
3. **Một sơ đồ = một ý.** Sơ đồ quá to (như image4, image1) khó đọc → tách theo chức năng/ layer; ghi chú chữ thay vì chữ siêu nhỏ trong ảnh.
4. **Ảnh + nguồn:** lưu file nguồn (`.drawio`, Figma link) cạnh ảnh; ghi đường dẫn vào RTM.
5. **Dùng dữ liệu thật** (tên bảng, endpoint, node) — không dùng ví dụ của dự án khác.

## 4. Áp dụng cho SRS dạng **md** của GDT Accounting
- **Ưu tiên sơ đồ dạng mã** (đọc được bằng AI, sửa/ so sánh bằng git): `mermaid` — `flowchart` (business flow/ activity/ luồng màn hình), `sequenceDiagram`, `erDiagram`/ `classDiagram`, `stateDiagram-v2` (vòng đời trạng thái đơn — rất hợp với `OrderStage`/ mã trạng thái), `C4`-like bằng `flowchart` cho component. Ảnh/ drawio chỉ khi sơ đồ quá phức tạp (kèm file nguồn). *Mermaid có hiển thị được trong trình xem md của bạn hay không là điều chưa kiểm — hỏi trước khi dùng nhiều.*
- **Có sẵn trong tài liệu GDT** để tái dùng: sơ đồ `Business Flow`, `Stage Machine Diagram`, `Component Diagram`, `DuplicateOrder-AlgorithmFlow` (nhãn chữ ở `thiet-ke/03-business-process-mockup/md`; hình trong file `.drawio` ở `goc/`), mockup 10 màn (`doc/yeu-cau/project-doc/project-doc-images`).
- Tối thiểu cho **một chức năng**: (1) luồng use-case hoặc **activity/ flowchart**, (2) **sequence** nếu có ≥ 2 thành phần gọi nhau (FE ↔ gateway ↔ service ↔ DB/ hệ thống ngoài như Pancake/ J&T), (3) **ERD** các bảng chạm tới, (4) **wireframe** (dẫn mockup có sẵn), (5) **state diagram** nếu chức năng đổi trạng thái đơn.
