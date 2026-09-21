# Đánh giá 17 repo skill và công cụ bên thứ ba (bản 2, đánh giá lại từ nội dung thật)

Ngày: 2026-09-19        Người viết: Claude (đóng vai researcher)        Xem lại vào: 2026-12-19

## Câu hỏi
Áp dụng được những repo nào trong danh sách của người dùng vào `agent-base`, cho vai nào, cài phần nào, và gộp nhóm ra sao? Kèm: WebMCP, Langfuse, E2B, open-code-review.

## Kết luận ngắn
- **Không áp dụng "hết" được.** Trong 17 repo chỉ có khoảng 7 repo chứa skill đáng cân nhắc; còn lại là công cụ dòng lệnh, dịch vụ, ứng dụng, hoặc khung điều phối trùng vai trò và trái quy tắc.
- **Đánh giá lại làm thay đổi kết quả.** Đợt 1 chỉ dựa README. Đợt 2 đọc cây thư mục, nội dung `SKILL.md`, script và nguồn độc lập, và **đảo ngược nhiều kết luận** (mục 2). Điển hình: superpowers từ 7 skill xuống còn 3; `ponytail` xung đột với TDD nên hạ xuống theo dõi; `diagram-design` **có script Python** (đợt 1 nói không có); `promptfoo` **bật telemetry mặc định** (đợt 1 nói không rõ); `to-spec` của Pocock đẩy lên **issue tracker**.
- Đợt đầu dự kiến **11 skill** (mục 5), sau khi bạn đọc và quét cục bộ. **Không chạy bộ cài của repo nào.**

## 1. Cách đánh giá, giới hạn
- **Đợt 1** (README): tóm tắt trang GitHub. **Đợt 2**: cây thư mục từng repo; nội dung `SKILL.md` của các skill ứng viên; hai script; và tìm nguồn độc lập (báo cáo kiểm toán, issue, bài phê bình).
- Công cụ đọc tóm tắt trang bằng một mô hình nhỏ, nên **có thể sai chi tiết**, và **chú thích HTML ẩn có thể bị lược** khi đọc. Vì vậy việc quét cuối cùng phải làm cục bộ bằng `scripts/check-skills.ps1` trên bản tải về, và **bạn phải tự đọc** (`agents/protocols/skills-policy.md`).
- Số sao, giấy phép là theo trang GitHub, chưa kiểm chứng độc lập. Tôi **chưa tải hay chạy** thứ gì.

## 1b. Kiểm chứng lại bằng nguyên văn (đợt 3, cùng ngày)

Người dùng hỏi các nhận định về chức năng từng skill có đúng không. Tôi đọc **nguyên văn** các file `SKILL.md` (nạp vào bộ nhớ để tìm từ khóa và đọc ngữ cảnh, không lưu file, không chạy) và đối chiếu với những gì đã ghi ở đợt 1 và 2.

**Đã xác nhận đúng (kèm dòng trong file):**

| Skill | Xác nhận |
|---|---|
| superpowers `brainstorming` | Lưu spec vào `docs/superpowers/specs/...` **và commit** (dòng 135, 244, 259). Mô tả mở đầu "You MUST use this before any creative work" |
| superpowers `writing-plans` | Mẫu kế hoạch chứa `git add ...` và `git commit -m ...` (dòng 138-139); dẫn sang `subagent-driven-development` hoặc `executing-plans` |
| superpowers `test-driven-development` | "Write code before the test? Delete it. Start over." (dòng 37, 254) |
| superpowers `systematic-debugging` | Ví dụ chứa `security list-keychains`, `security find-identity -v`, `codesign --sign` (dòng 98-103) |
| superpowers `requesting-code-review` | Dispatch subagent duyệt code; git chỉ đọc (`rev-parse`, `merge-base`) |
| superpowers `receiving-code-review` | Có `gh api .../replies` (dòng 205) |
| superpowers `using-superpowers` | "even a 1% chance ... you ABSOLUTELY MUST invoke", "This is not negotiable" |
| superpowers `verification-before-completion` | Sạch: không git, không mạng |
| Pocock `to-spec` | Đăng lên **issue tracker**, gắn nhãn `ready-for-agent`, cần chạy `/setup-matt-pocock-skills` trước |
| Pocock `implement` | "Commit your work to the current branch." |
| Pocock `resolving-merge-conflicts` | "Stage everything and commit... continue the rebase process" |
| Pocock `grill-with-docs` | File 8 dòng, chỉ gọi hai skill `grilling` và `domain-modeling`, chỉ người dùng gọi được |
| Pocock `improve-codebase-architecture` | Ghi báo cáo HTML vào **thư mục tạm của hệ điều hành** (không vào repo), dùng Tailwind và Mermaid qua CDN |
| Pocock `writing-for-agents` | Sạch |
| diagram-design | Gọi `python3 scripts/self_check.py` và `python3 scripts/*_extract.py`; có liên kết Google Fonts. 7 dòng `<!--` là chú thích trong mẫu SVG, lành tính |
| archify | Bảo chạy `node bin/archify.mjs validate` và `deliver`; **tự chạy `scripts/check-update.mjs` một lần**, nói rõ không tải, cài hay chạy bản cập nhật |
| i-have-adhd | Hiệu lực "cho phần còn lại của phiên" đến khi nói "stop adhd mode"; có mục "Cap lists to 5 items" |
| open-code-review | Thiếu `ocr` thì bảo chạy `npm i -g @alibaba-group/open-code-review` (dòng 53); nếu người dùng nói "review and fix" thì tự áp dụng sửa |
| gstack | README nói `./setup` đăng ký một hook Stop **bật mặc định** trong `~/.claude/settings.json` |

**Tôi đã nói sai hoặc cường điệu, nay sửa:**
- **ponytail**: không phải "được bỏ test cho thay đổi nhỏ". Skill yêu cầu logic không tầm thường để lại **một kiểm tra chạy được, nhỏ nhất**; chỉ "thay đổi một dòng tầm thường" không cần test, và không dùng framework hay bộ test theo hàm trừ khi được yêu cầu. Vẫn lệch với TDD và định nghĩa hoàn thành của bạn nên giữ ở Theo dõi, nhưng lý do nhẹ hơn tôi nói.
- **open-code-review**: skill **không** bảo agent tự nhập khóa API. Nó bảo "Prompt the user", đưa lệnh cấu hình làm mẫu, rồi "Stop here and ask the user to provide credentials — never invent or hardcode API keys". Chỉ còn hai điểm trái quy tắc: tự `npm i -g`, và tự sửa code khi "review and fix". Nó cũng bảo hỏi người dùng trước khi nâng cấp.
- **gstack và sandbox**: README **có** nhắc Docker và chính sách cô lập, nhưng trong quy trình đánh giá bảo mật `/cso`, không phải một sandbox chung để chạy mã do AI sinh. Kết luận "không thay được E2B" vẫn đứng, nhưng câu "trang không nhắc sandbox" là chưa chính xác.
- **Pocock `implement`**: chỉ nói commit, **không** nói tạo PR hay gọi issue tracker như bản tóm tắt trước.
- superpowers `receiving-code-review` có chữ "DELETE IT" nhưng chỉ nói về xóa chữ "Thanks", không phải xóa code.

**Vẫn chưa xác minh nguyên văn** (còn dựa tóm tắt hoặc đoạn trích tìm kiếm): mã của `archify.mjs` (mạng, tiến trình con, thư mục `.archify-*`, `brands capture`), 3 script extractor và `self_check.py` của diagram-design, hook của superpowers, ponytail và i-have-adhd, từng skill của google/skills (chỉ suy từ tên), kiểm toán gstack và ruflo (từ đoạn trích, kiểm toán gstack còn **không thấy hành vi độc hại**), telemetry của promptfoo, rủi ro SSRF của MarkItDown, E2B, webcmd, số sao và giấy phép.

## 2. Đợt 2 đã đổi điều gì so với đợt 1

| Điểm | Đợt 1 | Đợt 2 (sau khi đọc nội dung thật) |
|---|---|---|
| superpowers | 7 skill dự kiến, kể cả `brainstorming`, `writing-plans`, `requesting/receiving-code-review` | **3 skill**. `brainstorming` và `writing-plans` bảo agent `git add/commit` và ghi vào `docs/superpowers/`; `requesting-code-review` dispatch subagent (trùng vai `reviewer`); `receiving-code-review` gọi `gh api`; `using-superpowers` ép gọi skill "dù chỉ 1% khả năng" |
| superpowers, chi phí ngữ cảnh | không biết | Issue #190: nạp sẵn ~22k token (11% cửa sổ 200k); bản 6.1.0 phải nén; phê bình phổ biến là "cồng kềnh" |
| ponytail | Thử cho dev, reviewer | **Theo dõi**: chỉ yêu cầu một kiểm tra nhỏ cho logic không tầm thường, không bộ test theo hàm trừ khi được yêu cầu, và ưu tiên xóa, **lệch với TDD và định nghĩa hoàn thành** (đã đọc nguyên văn, mục 1b); kèm 12 file hook |
| diagram-design | "không có script" | **Có script Python** trong `skills/diagram-design/scripts/` (`self_check.py`, `drawio_extract.py`, `mermaid_extract.py`, `excalidraw_extract.py`). `self_check.py` chỉ dùng thư viện chuẩn, không mạng, không ghi (theo tóm tắt); 3 script kia chưa đọc |
| archify | "không chạy script" | **CLI Node** (`archify/bin/archify.mjs`): chạy tiến trình con, tạo thư mục tạm `.archify-*` trong thư mục xuất, có script **kiểm tra cập nhật qua mạng** (tắt bằng `ARCHIFY_UPDATE_CHECK_DISABLED=1`), lệnh `brands capture <url>` truy cập mạng, và kho có file **`archify.zip`** |
| Pocock | 4 skill | `to-spec` **đẩy lên issue tracker**; `implement` **commit**; `resolving-merge-conflicts` tự stage, commit, tiếp tục rebase. Các skill giữ lại **kéo theo skill phụ thuộc** (`grilling`, `domain-modeling`, `codebase-design`) nên là 6 skill |
| promptfoo | "không rõ telemetry" | **Telemetry bật mặc định**, tắt bằng `PROMPTFOO_DISABLE_TELEMETRY=1` (giao diện web cần đúng chuỗi `true` lúc build); không gồm prompt hay khóa, nhưng gồm email nếu đã đăng nhập |
| gstack | Tránh (vì bộ cài) | **Tránh, mạnh hơn** (theo đoạn trích tìm kiếm của một báo cáo kiểm toán, chưa đọc nguyên văn; báo cáo đó **không thấy hành vi độc hại**, chỉ nêu vấn đề minh bạch): công cụ `gstack-global-discover` quét `~/.claude/projects`, `~/.codex/sessions`, `~/.gemini/tmp`, và `skill-usage.jsonl` vẫn ghi khi telemetry tắt; hook SessionStart có thể `git pull` mỗi giờ ở chế độ nhóm |
| ruflo | Tránh | **Tránh, mạnh hơn**: chính kiểm toán nội bộ của dự án nói nhiều hệ số tăng tốc là chuỗi cứng không có benchmark, một số con số được **tạo lúc chạy**, và có lỗi đảo dấu phần thưởng |
| ECC | Tham khảo | Giữ nguyên. Phàn nàn số một là chi phí token; dự án tự có 4 hồ sơ cài (Core, Developer, Security, Full) |

## 3. Đánh giá cuối theo từng repo

| Repo | Là gì | Kết luận | Chỉ chép phần này | Vai |
|---|---|---|---|---|
| `obra/superpowers` | 15 skill quy trình phát triển (MIT) | **Thử, rất chọn lọc** | `verification-before-completion` (sạch); `test-driven-development` (có chỉ dẫn xóa code viết trước test, chỉ áp dụng cho code agent vừa viết); `systematic-debugging` (chép `SKILL.md` và 3 file `.md` tham chiếu; **bỏ** `find-polluter.sh`, `test-*.md`, `CREATION-LOG.md`; có ví dụ lệnh keychain macOS cần đọc) | dev, qa |
| `mattpocock/skills` | Bộ skill kỹ thuật, năng suất (MIT) | **Thử, chọn lọc** | `writing-for-agents`; `grill-with-docs` + `grilling` + `domain-modeling`; `improve-codebase-architecture` + `codebase-design` (tạo báo cáo HTML dùng Tailwind và Mermaid qua CDN) | analyst, architect, writer |
| `cathrynlavery/diagram-design` | Sơ đồ HTML/SVG, 40+ loại (MIT) | **Thử** | thư mục `skills/diagram-design/` (SKILL.md, references, assets). Script chỉ sau khi đọc. **Không** chép `commands/`, `prompts/`, manifest plugin. Phông Google tải lúc xem HTML | designer, architect, ba, analyst |
| `tt-a1i/archify` | Sơ đồ kiến trúc bằng CLI Node (MIT) | **Thử có điều kiện** | thư mục `archify/`, **không** chép `archify.zip`; đặt `ARCHIFY_UPDATE_CHECK_DISABLED=1`; không dùng `brands capture`; thêm `.archify-*/` vào `.gitignore` | architect (cần quyền chạy `node` hẹp, mục 6) |
| `DietrichGebert/ponytail` | Quy tắc tối giản code (MIT) | **Theo dõi** | — | — |
| `ayghri/i-have-adhd` | Skill kiểu trả lời; sau khi gọi `/i-have-adhd` kéo dài cả phiên, cắt lời mở đầu và tóm tắt, giới hạn danh sách 5 mục (MIT) | **Tùy chọn** | chỉ `SKILL.md`, **không** hook `always-on`. Có thể xung đột định dạng phiếu và kế hoạch commit | orchestrator (người dùng tự gọi) |
| `google/skills` | Skill Google Cloud theo `skills/{cloud,ads,analytics,identity,developers}/` (Apache-2.0) | **Theo dõi, chỉ khi dùng GCP** | từng skill sau khi đọc. Một số (ví dụ `gke-cluster-creation`) nhiều khả năng chạy `gcloud` tạo hay xóa tài nguyên: cần `gcloud*` ở mức hỏi | devops, dba, security |
| `microsoft/markitdown` | Chuyển tài liệu sang markdown (MIT) | **Thử** (dòng lệnh cục bộ, không dùng gói MCP) | không phải skill | ba, analyst |
| `alibaba/open-code-review` | CLI duyệt code, có chế độ Delegation | **Thử có điều kiện** (mục 4c) | không dùng `SKILL.md` gốc nguyên bản | reviewer |
| `promptfoo/promptfoo` | Đánh giá và red-team prompt | **Theo dõi** (giai đoạn 3), đặt `PROMPTFOO_DISABLE_TELEMETRY=1` | — | chủ repo, security |
| `e2b-dev/E2B` | Sandbox đám mây | **Theo dõi** (mục 4b) | — | — |
| `agentrhq/webcmd` | Tự động hóa trình duyệt có phiên đăng nhập | **Tránh mặc định** | — | qa trên `localhost` nếu cần |
| `garrytan/gstack` | 23 công cụ nhập vai + bộ cài | **Tránh** (dùng tham khảo) | — | — |
| `affaan-m/ECC` | Khung 68 agent, 292 skill | **Tham khảo, không cài** | — | — |
| `ruvnet/ruflo` | Nền tảng bầy agent | **Tránh** | — | — |
| `onlook-dev/onlook`, `bilawalsidhu/gods-eye-view` | Ứng dụng | **Không áp dụng như skill** | — | — |

## 4. Nhóm skill (sơ đồ: `docs/research/skill-bundles.svg`)

| Nhóm | Gồm | Vai |
|---|---|---|
| 1. Tài liệu, tiếp nhận | markitdown (công cụ), diagram-design, writing-for-agents | ba, analyst, writer |
| 2. Thiết kế, kiến trúc | archify, diagram-design, grill-with-docs, grilling, domain-modeling, improve-codebase-architecture, codebase-design | architect, designer, analyst |
| 3. Code và chất lượng | test-driven-development, systematic-debugging, verification-before-completion | dev, qa, reviewer |
| 4. Bảo mật, kiểm tra | promptfoo (sau), open-code-review (thử chế độ delegate) | security, reviewer |
| 5. Google Cloud (chỉ khi dùng) | chọn từng skill trong google/skills | devops, dba, security |
| 6. Phong cách trả lời (tùy chọn) | i-have-adhd | orchestrator |
| Không cài | gstack, ECC, ruflo, webcmd, onlook, E2B, gods-eye-view, ponytail, các skill superpowers và Pocock còn lại | — |

Mỗi skill đã cài làm tăng ngữ cảnh mỗi phiên. Giữ **không quá 10–14 skill mỗi dự án**.

## 5. Skill dự kiến cài đợt đầu (11), và đọc đến đâu

| Skill | Nguồn | Đã đọc nội dung thật | Việc phải làm trước khi cài |
|---|---|---|---|
| verification-before-completion | superpowers | có | quét cục bộ |
| test-driven-development | superpowers | có | quét; ghi chú lệnh xóa chỉ áp cho code vừa viết |
| systematic-debugging | superpowers | có `SKILL.md`, chưa đọc 3 file tham chiếu | đọc 3 file; bỏ script `.sh` |
| writing-for-agents | Pocock | có | quét |
| grill-with-docs | Pocock | có | đọc `grilling`, `domain-modeling` |
| grilling, domain-modeling | Pocock | **chưa** | đọc toàn bộ |
| improve-codebase-architecture | Pocock | có | đọc `codebase-design`; báo cáo HTML dùng CDN |
| codebase-design | Pocock | **chưa** | đọc toàn bộ |
| diagram-design | diagram-design | có `SKILL.md`, một script | đọc 3 script extractor, `references/` |
| archify | archify | có `SKILL.md` và `archify.mjs` (tóm tắt) | đọc `scripts/check-update.mjs`, các module nạp động; bỏ `archify.zip` |

**Loại rõ ràng**, kèm lý do: superpowers `brainstorming` và `writing-plans` (git commit, đường dẫn `docs/superpowers/`), `requesting-code-review` (trùng reviewer, subagent), `receiving-code-review` (`gh api`), `using-superpowers` (ép gọi skill), `using-git-worktrees`, `finishing-a-development-branch`, `subagent-driven-development`, `dispatching-parallel-agents`, `executing-plans` (theo tên, chưa đọc nội dung), `diagnosing-superpowers`, `writing-skills` (chưa đọc); Pocock `to-spec`, `implement`, `to-tickets`, `resolving-merge-conflicts`, `setup-matt-pocock-skills`, `wizard`, `ask-matt`, `triage`, `wayfinder`.

## 6. Quyền và cấu hình cần khi cài (chưa làm)

Skill có script cần vai được phép chạy lệnh. Hiện `architect`, `designer`, `analyst` chỉ có `bash: readonly`, nên **không chạy được** `node` hay `python`. Nếu bạn duyệt, thêm quyền **hẹp**, không đổi sang `full`:
- `architect`: `bash_allow: node*archify.mjs*`; `bash_deny: *brands capture*`.
- `designer`, `architect`: `bash_allow: python*self_check.py*` (diagram-design; SKILL gốc ghi `python3`, trên Windows là `python`).
- Vai `full` đã chạy được lệnh, nhưng vẫn bị luật riêng (git ghi bị chặn).
- `.gitignore`: thêm `.archify-*/` và thư mục xuất của archify.
- Biến môi trường (người dùng đặt): `ARCHIFY_UPDATE_CHECK_DISABLED=1`, `PROMPTFOO_DISABLE_TELEMETRY=1`, `SUPERPOWERS_DISABLE_TELEMETRY` (nếu dùng bất kỳ phần nào của superpowers ngoài việc chép skill).
- Google Cloud: nếu cài, thêm `gcloud*` vào `bash_ask` cho `devops`, `dba`, `security`.

## 4b. gstack không thay được E2B (kiểm ngày 2026-09-19)

Giả định "gstack gộp nhiều thứ nên không cần E2B" **sai về tầng**:
- **gstack** là bộ lệnh nhập vai cộng trình duyệt Chromium và máy chủ Bun. Theo tài liệu của nó, các thành phần chạy trên máy người dùng với quyền của người dùng. README có nhắc Docker và chính sách cô lập, nhưng trong quy trình đánh giá bảo mật `/cso`, **không** trình bày như một sandbox chung để chạy mã do AI sinh. `/ship`, `/land-and-deploy`, `/qa` chạy git và test, commit, push, mở PR bằng quyền của bạn; bộ cài đăng ký hook vào cấu hình.
- **E2B** là hạ tầng chạy mã không tin cậy trong **sandbox cô lập trên đám mây** (cần tài khoản và khóa; trang không nêu công nghệ cô lập).
- Phần trùng thật của gstack là **vai trò**: `/plan-eng-review` ~ architect, `/review` ~ reviewer, `/qa` ~ qa, `/cso` ~ security, `/document-*` ~ writer, `/design-*` ~ designer, `/ship` và `/land-and-deploy` ~ devops (nhưng chạm git và deploy).
- Kết luận về E2B vẫn là **chưa cần**: chưa chạy mã không tin cậy, Docker cục bộ (máy đã có) đủ cho việc thử skill, và quyền vai cùng cổng rủi ro đã giới hạn agent.
- Đáng mượn ý từ gstack: `/careful` và `/guard` (cảnh báo trước `rm -rf`, `DROP TABLE`, force-push).
- Giới hạn: tôi chưa đọc toàn bộ tài liệu gstack; kết luận dựa trên README và các trang tôi đã đọc.

## 4c. open-code-review (Alibaba): chi tiết và cách khớp vào luồng

Đọc trang repo, `skills/open-code-review/SKILL.md` và các bài mô tả ngày 2026-09-19.

**Là gì**: CLI `ocr` duyệt code trên thay đổi Git. Phần **xác định** (chọn file, gom file liên quan, khớp quy tắc theo mẫu) làm trước, rồi một agent LLM đọc file đầy đủ, tìm trong repo và ra nhận xét theo dòng (JSON hoặc markdown). Lệnh: `ocr review`, `ocr review --from develop --to <nhánh>`, `ocr review --commit <mã>`, `ocr scan` (duyệt cả file, hợp với `analyst` khi nhận dự án có sẵn), `ocr delegate ...`, `ocr session list`, `ocr config ...`.

**Hai chế độ**:

| | Tự chạy (khóa LLM riêng) | Delegation |
|---|---|---|
| Ai duyệt | LLM cấu hình trong `ocr` | **Chính agent của bạn** dùng cách chọn file và quy tắc của `ocr` |
| Code đi đâu | Diff, file đầy đủ, ngữ cảnh repo tới nhà cung cấp đã cấu hình; việc che dữ liệu **không được ghi** | Chỉ tới mô hình agent đó đã dùng |
| Khóa API | Cần | Không cần thêm |

**Khớp vào luồng** (nếu chọn thử): Dev làm xong (chưa commit) thì `reviewer` chạy `ocr` ở chế độ Delegation; kết quả **ghi vào task card** (nếu cần `--output` thì vào thư mục đã `.gitignore`, ví dụ `.ocr-out/`); `reviewer` vẫn làm checklist riêng (đúng phạm vi, kế hoạch commit, cổng rủi ro, có test), `ocr` chỉ bổ sung phát hiện lỗi; lỗi trả lại Dev sửa, reviewer không sửa; nhận xét của `ocr` là dữ liệu tham khảo, không phải quyết định.

**Không dùng nguyên `SKILL.md` gốc** (đã đọc nguyên văn, mục 1b): nó bảo agent (a) tự `npm i -g @alibaba-group/open-code-review` khi thiếu `ocr`, và (b) tự áp dụng sửa code nếu người dùng nói "review and fix". Cả hai trái quy tắc: cài đặt do **người dùng** làm, reviewer không sửa. Phần khóa API thì skill xử lý **đúng**: nó dừng lại và yêu cầu người dùng tự cung cấp, "never invent or hardcode API keys". Nếu dùng skill thì chép rồi **cắt hai bước đó** và ghi vào sổ là đã chỉnh sửa, hoặc viết chỉ dẫn ngắn riêng trong vai `reviewer`.

**Điều kiện thử**: bạn tự cài `ocr` (ghim phiên bản) và tự cấu hình; cần Git từ 2.41 (máy có 2.45.1), yêu cầu Node chưa được nêu. Thử ở chế độ Delegation trên một dự án nhỏ, so với reviewer thường (cảnh báo đúng, sai, bỏ sót). Khi được duyệt, thêm chỉ cho `reviewer`: `bash_allow`: `ocr review*`, `ocr delegate*`, `ocr session list*`, `ocr scan*`; `bash_deny`: `ocr config*`, `npm*`. Thêm `.ocr-out/` vào `.gitignore`. `ocr` ghi cấu hình và dữ liệu phiên trong thư mục home.

**Số liệu**: dự án nói độ chính xác 33,9% so với 7,23% của agent thông thường và tốn ít token hơn, **nhưng độ phủ thấp hơn**; đây là số của nhà phát hành, chưa kiểm chứng độc lập. Bộ quy tắc gốc thiên về Java, cần thử với ngăn xếp của bạn.

## 4d. Các câu hỏi khác

- **MarkItDown cho tài liệu đầu vào**: đúng, hợp với vai `ba`. Dùng **dòng lệnh cục bộ** (`markitdown <tệp> > docs/converted/<tên>.md`), không dùng gói MCP (rủi ro SSRF và đọc file), không bật OCR bằng LLM khi chưa duyệt (nó gửi ảnh ra ngoài). Đã ghi vào `agents/protocols/intake.md`.
- **diagram-design cho BA**: nó **vẽ sơ đồ**, không viết tài liệu yêu cầu. Tài liệu vẫn viết markdown, sơ đồ lưu `.svg` và nhúng vào.
- **ECC**: không cài nguyên khối (là hệ vai trò và quy tắc thứ hai). Dùng làm thư viện tham khảo, chép từng skill sau khi đọc.
- **WebMCP**: API của trình duyệt (Chrome/Edge, bản xem trước, cần Chromium 146 trở lên và cờ thử nghiệm) cho **trang web** công bố công cụ cho agent trình duyệt. Không cài vào Kilo hay Antigravity. Chưa cần.
- **Langfuse**: chưa cần giai đoạn 1–2. Có tích hợp OpenCode qua plugin `@langfuse/opencode-observability-plugin` (Kilo 7 xây trên OpenCode nên có thể dùng, chưa kiểm chứng). Đổi lại phải có tài khoản hoặc tự dựng máy chủ, và vết ghi chứa mã và prompt. Cân nhắc ở giai đoạn 4.

## 7. Kế hoạch cài (chưa làm, chờ bạn)

1. **Bạn** tải các repo ứng viên vào `D:\skills-quarantine` (ngoài OneDrive, ngoài dự án). Tôi không chạy `git clone`.
2. Tôi chạy `scripts/check-skills.ps1` (chỉ đọc) và đọc các file **chưa đọc** ở mục 5 (`grilling`, `domain-modeling`, `codebase-design`, 3 file tham chiếu của systematic-debugging, 3 script extractor, `check-update.mjs`), báo từng file.
3. Bạn duyệt từng skill. Tôi **chép thư mục skill** (không bộ cài, không hook) vào `.agents/skills/` và ghi `agents/knowledge/skills.md`; thêm quyền hẹp ở mục 6 nếu cần.
4. Bạn commit qua nhánh và Merge Request.
5. Thử trong worktree với vai quyền thấp, rồi mới mở rộng.
6. Sau đó thêm khóa `skills:` theo vai (cần thử cú pháp quyền `skill` của Kilo trong giao diện thật).

## Rủi ro
- Chỉ dẫn độc trong `SKILL.md` (kể cả chú thích ẩn), script tải mã, đọc khóa: `agents/protocols/skills-policy.md`.
- Bộ cài của gstack, superpowers (bản plugin), ECC, ruflo, ponytail sửa cấu hình người dùng và thêm hook: không chạy.
- Skill có thể dặn dùng git ghi, tạo subagent, tìm web, gọi `gh`: quy tắc vai và `AGENTS.md` mục 4 (quy tắc 14) vẫn thắng.
- Antigravity không giới hạn skill theo agent (tài liệu không nói): mọi agent ở đó thấy mọi skill đã cài.

## Chưa xác minh
- Nội dung thật của các skill ở mục 5 đánh dấu "chưa", 3 script extractor, `check-update.mjs`, hook của superpowers và ponytail, webcmd, từng skill của google/skills.
- Nội dung đã đọc là bản tóm tắt của công cụ đọc trang, chú thích ẩn có thể bị lược.
- Số sao, giấy phép, mức bảo trì (theo trang GitHub).
- Cú pháp quyền `skill` theo vai trong Kilo; Langfuse với Kilo 7; script chạy đúng trên Windows PowerShell 5.1.

## Nguồn (đọc ngày 2026-09-19)
- https://github.com/obra/superpowers (cây thư mục, `skills/*/SKILL.md`), issue #190 và #832 của repo
- https://github.com/mattpocock/skills (`skills/engineering/*`, `skills/productivity/*`)
- https://github.com/cathrynlavery/diagram-design (`skills/diagram-design/SKILL.md`, `scripts/self_check.py`)
- https://github.com/tt-a1i/archify (`archify/SKILL.md`, `archify/bin/archify.mjs`)
- https://github.com/DietrichGebert/ponytail, https://github.com/ayghri/i-have-adhd, https://github.com/google/skills
- https://github.com/microsoft/markitdown, https://github.com/alibaba/open-code-review (`skills/open-code-review/SKILL.md`)
- https://github.com/promptfoo/promptfoo, https://www.promptfoo.dev/docs/configuration/telemetry/
- https://github.com/e2b-dev/E2B, https://github.com/agentrhq/webcmd, https://github.com/onlook-dev/onlook, https://github.com/bilawalsidhu/gods-eye-view
- https://github.com/garrytan/gstack, issue #467 và #1579 của repo
- https://github.com/ruvnet/ruflo (tài liệu kiểm toán nội bộ `docs/reviews/`), https://github.com/affaan-m/ECC
- https://developer.chrome.com/docs/ai/webmcp, https://langfuse.com/integrations/developer-tools/opencode
