# AGENTS.md — quy tắc chung cho mọi agent

Nguồn quy tắc duy nhất (`CLAUDE.md`, `GEMINI.md`, `CODEX.md`, `.agents/rules/agents-core.md` được sinh tự động qua `python scripts/refresh.py`, đừng sửa tay). Chỉ con người hoặc agent được yêu cầu rõ mới được sửa. Diff tăng ~2.000 dòng khi sửa file này là do nhân bản sang các adapter đa AI.

## 0. Nguyên tắc chung & Tư duy Phản biện

Việc hoàn tác được trong phạm vi được giao thì cứ làm. **Hỏi trước khi làm việc có tác động**: mất code, dữ liệu hay lịch sử; đụng nhánh chung; tốn tiền/tài nguyên ngoài; lộ khóa bí mật/dữ liệu cá nhân; chạy mã ngoài chưa duyệt. Người dùng đồng ý rõ trong chat thì làm ngay và trích dẫn vào `agents/protocols/approval.md`; "ok" chung chung thì hỏi lại.

- **Anti-Loop & Fail-Fast**: Không lặp câu chữ, thiếu dữ kiện thì DỪNG HỎI NGAY. Shell, mạng, git, test lỗi/treo quá 10–15s thử lại tối đa 3 lần; lần 3 vẫn lỗi thì DỪNG, kill tiến trình và báo cáo.
- **Mô Hình Cây & Vùng Ảnh Hưởng (Tree Model & Blast Radius — BẮT BUỘC)**:
  - **Trunk Code (Thân & Rễ — Core, Infra, Shared State, Auth, DB Schema, Network, Common Libs)**: Vùng ảnh hưởng cao, rủi ro sập hệ thống (one-way door). BẮT BUỘC **Deep Inspection** (soi kỹ từng dòng, phân tích side-effects, cấm dùng Fast-Path bỏ qua review dù diff nhỏ).
  - **Leaf Code (Nhánh Lá — Isolated UI, Standalone Endpoint, Decoupled Worker)**: Vùng ảnh hưởng hẹp. BẮT BUỘC **Feature Gating** (bọc sau cờ tính năng / Kill-switch, default = OFF). Review theo cơ chế **Fast-Skim** (đọc lướt dựa trên bằng chứng Agentic Validation Proof).
- **Feature Gating by Default (Thủ hiểm ngay từ Planning)**: Mọi tính năng Leaf mới phải trả lời câu hỏi: *"Nếu chạy sai trên Prod, tắt flag có Rollback ngay lập tức mà không ảnh hưởng luồng cũ không?"*.
- **Zero-Step Dynamic Triage (Tự Động Định Tuyến Tăng Tốc — BẮT BUỘC)**:
  - **Làn Nhanh (Fast-Path — Fix Bug / Ảnh Lỗi / Sửa $\le 2$ file Leaf)**: Khi người dùng cung cấp ảnh lỗi, log lỗi, hoặc yêu cầu sửa cục bộ ở Leaf code: **TỰ ĐỘNG BẬT FAST-PATH**. Miễn trừ 100% Pre-Code Doc Gate (`doc-preflight`, `BOARD.md`), miễn trừ bắt buộc 3 phương án phản biện lý thuyết, miễn trừ duyệt Gate 2 trước khi sửa code. Cơ chế thực hiện: (1) Bóc "mỏ neo độc nhất" (Unique Anchor) từ ảnh/log → (2) Tìm đúng file bằng `safe-search` trong thư mục hẹp (< 1s), cấm gọi Xerj toàn cục → (3) Ngân sách đọc cực hạn $\le 2$ file, $\le 50$ dòng quanh điểm gãy, cấm đọc dây chuyền (cascade read) → (4) Viết 1 test tái hiện đơn vị (Red) → (5) Sửa code bằng `edit_file` → chạy test xanh (Green) → xuất `git diff`. Toàn bộ chu trình $\le 5$ phút.
  - **Làn Đầy Đủ (Full-Workflow — Tính Năng Mới / Đổi Trunk Code / Đổi DB Schema / Đổi API Chung)**: Áp dụng đủ 5 bước TDD/ATDD, sơ đồ JSON-first, 3 phương án phản biện, và Swarm Gate 2.
- **Adversarial Review Agent (Phản biện Zero-Context & Bỏ Nits)**: Cấm dùng cùng session context của Dev để tự review code của mình (tránh thiên vị / confirmation bias). Reviewer bắt buộc chạy ở subagent mới tinh độc lập ngữ cảnh, chỉ đọc diff + spec + hard-rules để tìm lỗi; bỏ nits (để Linter/hard-rules lo).
- **Default Boost Mode (Phản biện Sâu & 10x Scale — BẮT BUỘC)**: Không gật đầu chiều theo đề bài mơ hồ (`agents/protocols/challenger.md`). Trước khi thiết kế hay sửa code tính năng mới/vừa/lớn, kiểm `plan-eng-review` (10x Data OOM, Concurrency Deadlock, Latency Cascade) và `plan-ceo-review`.
- **Generic-First (Kế thừa nền, Đổi mới đúng trọng tâm)**: Tái sử dụng Entity/Repo/Config chạy ổn; phần người dùng yêu cầu tối ưu CẤM copy-paste cục bộ mà phải tự phản biện trừu tượng hóa Generic `<T>` (như đưa vào `ws-library`).
- **Mỗi lần đưa lựa chọn (BẮT BUỘC 3 phương án)**: (A) Cục bộ/cũ + điểm nghẽn, (B) Over-engineering + rủi ro bảo trì, (C) **Khuyến nghị** + lý do + cách khắc phục rủi ro. *(Chỉ áp dụng khi thiết kế tính năng mới hoặc task vừa/lớn; cấm áp dụng làm chậm tác vụ Fast-Path sửa bug nhỏ)*.
- **Cơ chế Đối kháng Builder vs Breaker (1 Thằng Làm - 1 Thằng Phá — BẮT BUỘC)**: Mọi chức năng mới hoặc thay đổi kiến trúc không được tự biên tự diễn rồi tự khen mình. BẮT BUỘC phân lập hai cực đối kháng:
  - **Thằng Làm (Builder / Dev / Architect)**: Thiết kế và giải trình câu hỏi cốt tử: *"Tại sao code như này? Code này tối giản ra sao? Khi mở rộng thêm 10 kênh/nghiệp vụ nữa thì có phải sửa hàm cũ không (Open-Closed Principle)?"*.
  - **Thằng Phá (Breaker / QA / Adversarial Reviewer)**: Bẻ gãy giải pháp bằng các kịch bản ác hiểm: Edge Cases, Null, Race Condition, Deadlock, Tiền lẻ làm tròn, 10x Scale OOM, và các bẫy gian lận test.
- **5 Trụ Cột Tư Duy Kỹ Nghệ Tối Thượng (The 5 Engineering Mindsets — BẮT BUỘC)**:
  1. *Tư duy Module Sâu (Deep Modules — John Ousterhout)*: Interface cực mỏng, nông và đơn giản; Implementation sâu, giấu kín toàn bộ sự phức tạp bên trong. Chống tuyệt đối Shallow Modules (hàm/class chỉ là wrapper rỗng chuyển tiếp).
  2. *Tư duy Hình Dáng Dữ Liệu (Data-Shape First — Linus Torvalds)*: Thiết kế Data Contract, Schema và cấu trúc dữ liệu chuẩn trước khi viết bất kỳ dòng logic nào; cấm chắp vá flag/biến tạm bợ để chữa cháy.
  3. *Tư duy Bớt Đi Trước Khi Thêm Vào (Occam's Razor / Subtraction First)*: Code súc tích nhất giải quyết trọn vẹn vấn đề; một quyết định logic chỉ được sống ở một nơi duy nhất (Single Source of Truth).
  4. *Tư duy Đảo Ngược (Inversion / Pre-Mortem)*: Luôn tự hỏi *"Tính năng này sẽ chết/sập ở đâu khi chạy thật?"* (Null, Concurrency, Network Timeout, OOM, Leak) trước khi bắt đầu gõ code.
  5. *Tư duy 3 Bước Tiến Hóa (Make it Work $\rightarrow$ Make it Right $\rightarrow$ Make it Fast)*: CẤM dừng lại ở bước "chạy được". Sau khi test xanh, BẮT BUỘC refactor làm sạch: áp dụng Strategy Pattern/Polymorphism, đưa hàm về $\le 45$ dòng, lồng nhau $\le 3$ tầng.

## 1. Đọc gì trước khi làm (Pre-Code Doc Gate)

> **Phân luồng áp dụng:** Pre-Code Doc Gate CHỈ áp dụng cho **Task Vừa & Lớn / Tính năng mới**. Đối với **Việc nhỏ / Fix Bug (Fast-Path)** có ảnh chụp hoặc log: **MIỄN TRỪ HOÀN TOÀN** việc đọc `BOARD.md`, Task card và `doc-preflight.py`; vào thẳng định vị anchor và sửa code.

1. `PROJECT.md`, `agents/stacks/<stack>.md` (hoặc `.ai-rules/`, `doc/architecture/engineering/*`), `doc/notes/PROJECT-NOTES.md` và `doc/notes/inbox/`.
2. **Chốt tài liệu hiện hành**: đọc `BOARD.md`, Task Card (`doc/features/<UC>/tasks/` hoặc `tasks/`) và `agents/roles/<vai>.md`. Khi UC có tài liệu cũ/mới, chạy `python3 ~/Documents/agent-base/scripts/doc-preflight.py --root . --uc <UC>` để chốt đúng `Active Source` mới nhất (bỏ `archive/`, `SUPERSEDED`, `cancelled`; nếu `.docx/.xlsx` mới hơn `.md` hoặc XERJ báo `index_stale` thì đối chiếu/đọc trực tiếp trên đĩa, xem `agents/protocols/source-precedence.md`). Cấm đoán thiết kế trước khi tra đủ hồ sơ.
3. **Tri thức & Kỹ năng (JIT 3 kênh)**: chạy `python scripts/knowledge.py query|query-skill|query-api -q "<từ khóa>" --role <vai>` và kiểm đủ `image` + `assets/` trước khi kết luận thiếu. Đọc `SKILL.md` khớp việc và ghi bằng chứng vào Handoff Note.
4. **Tra cứu mã nguồn AST & Khóa Chiến Lược Tìm Kiếm (Hard Search Policy — CẤM `grep`/`egrep`/`rg`/`find`/`cat`)**:
   - **Trần tìm kiếm Fast-Path (Search Ceiling = 1 call)**: Khi sửa bug nhỏ, CHỈ ĐƯỢC PHÉP GỌI ĐÚNG 1 LẦN TÌM KIẾM DUY NHẤT. Thấy file mục tiêu là DỪNG TÌM KIẾM NGAY. Nếu lần 1 không ra kết quả: DỪNG LẠI và HỎI NGƯỜI DÙNG tọa độ file, cấm xoay vòng thử liên tiếp nhiều tool khác nhau.
   - **Quy tắc Single-Anchor (Mỏ neo độc nhất)**: Từ khóa tìm kiếm bắt buộc có độ đặc hiệu cao (chuỗi $\ge 8$ ký tự, nhãn UI tiếng Việt, mã lỗi `ERR-xxx`, tên method/enum cụ thể). CẤM TUYỆT ĐỐI tìm bằng từ khóa chung chung (`order`, `status`, `user`, `id`).
   - **Cấm Tuyệt Đối Exploratory Browsing**: CẤM chạy `ls -R`, `tree`, `find .`, `git grep`, `git log -S/-G` diện rộng; CẤM gọi `graphify` quét mạng lưới phụ thuộc khi sửa bug; CẤM spawn subagent `@research` đi khảo sát codebase khi đang làm task nhỏ.
   - **Chặt đứt vòng lặp đọc dây chuyền (Anti-Cascade Read)**: Đọc $\le 50$ dòng quanh điểm gãy bằng `read_file`. CẤM TUYỆT ĐỐI mở đọc các file trong danh sách `import/require` trừ khi dòng lỗi gọi trực tiếp method đó và throw exception.
   - Đọc symbol/class/API/tài liệu ở root: dùng MCP `xerj_def` / `xerj_search` (luôn truyền `prefix`, vd `prefix="gdt"`, `prefix="agentbase"`, `prefix="tiktok"`) hoặc `graphify`.
   - Đọc nội dung file đã biết: dùng `read_file` với line range cụ thể.
   - Tìm chuỗi UI/i18n hoặc file mới tạo trong Git worktree ngoài workspace (chưa có trong XERJ root index): dùng `python3 scripts/safe-search.py -q "<chuỗi>" -d <dir>` + `read_file`. Shim hệ thống chặn cứng exit `2` nếu vi phạm. Ghi `Tra cứu mã nguồn (XERJ/AST): PASS` vào Handoff Note.
   - Cầu nối song ngữ & Phân làn tự động: Khi người dùng hỏi bằng tiếng Việt, chạy `python3 scripts/bilingual-query.py -q "<câu hỏi>"` để lấy từ khóa code tiếng Anh tương đương; hoặc dùng `python3 scripts/hybrid-search.py -q "<từ khóa>"` để tự động phân làn đúng tool (AST cho Symbol, safe-search cho text UI).
5. **Frontend/UI**: bắt buộc kiểm thử trình duyệt (Playwright/CDP), ghi `Xác minh giao diện (CDP/Browser): PASS` + `Console errors: 0` vào Handoff Note.

Chưa rõ thì hỏi, không có nguồn không khẳng định.

## 2. Cỡ việc & 3. Vai trò

| Cỡ | Ví dụ | Ai làm | Bắt buộc |
| --- | --- | --- | --- |
| nhỏ | fix bug, sửa chữ, $\le 2$ file, có ảnh/log | 1 Dev | Kích hoạt Fast-Path: bóc anchor → test tái hiện → sửa code → test xanh, người dùng xem diff (< 5 phút) |
| vừa | thêm chức năng nhỏ | Dev + Reviewer + QA | task card đầy đủ, `AC-xx` checklist |
| lớn | tính năng mới, nhiều service | Đủ đội theo `full-workflow.md` | toàn bộ quy trình & Gate 2 |

Tự nâng lên từ "vừa" khi đụng file chung, đổi API/DB, liên quan bảo mật hoặc sửa nhiều file. Chi tiết 20 vai (`lead`, `product`, `ba`, `analyst`, `architect`, `researcher`, `designer`, `dba`, `data-eng`, `ai-eng`, `dev`, `mobile`, `devops`, `sre`, `security`, `reviewer`, `qa`, `runner`, `debt-hunter`, `writer`): xem `agents/protocols/full-workflow.md` §3.

## 4. Quy định sửa file, Worktree và Git

- **Phạm vi & Công cụ sửa**: Chỉ sửa file khớp `scope_edit`, tránh `scope_deny`. Làm trong worktree tập trung ngoài workspace (`scripts/worktree-manager.py` / `scripts/task-branch.py`). Trước khi sửa code, BẮT BUỘC tạo checkpoint bằng `python3 scripts/task-checkpoint.py create --task <T-xx>` (nếu test fail $\ge 2$ lần thì rollback bằng `python3 scripts/task-checkpoint.py rollback --task <T-xx>` chống lỗi dây chuyền). Khi chạy lệnh test/build xả log dài, BẮT BUỘC dùng `python3 scripts/safe-exec.py -c "<lệnh>"`. Sửa code bằng `Edit`/`Write` (cấm inline Python heredoc `python3 - <<'EOF'`, `sed`, `perl`) và giữ sạch theo `agents/stacks/<stack>.md` (không unused import, không FQN nội tuyến, dùng `enum` thay magic String).
- **Lệnh Git**: Tự chạy được lệnh xem (`status`, `diff`, `log`, `show`, `blame`, `ls-files`, `rev-parse`, `merge-base`) và lệnh trong nhánh cá nhân (`checkout`/`switch`, `branch`, `fetch`, `pull`, `merge`, `rebase`, `restore`, `stash`, `cherry-pick`, `revert`, `rm`, `mv`, `worktree`, `tag` mới). `add <path>`, `commit`, `push` (nhánh cá nhân, không ép) **chỉ khi người dùng yêu cầu rõ**. **Luôn cấm**: `reset`, `clean`, `add -A`/`.`/`-f`, `commit --amend`, push ép/vào nhánh chung (`main`/`develop`/`release/*`), xóa nhánh/tag, `stash drop`/`clear`, viết lại lịch sử, `config`, `remote`, `init`, `clone`, `--no-verify`.
- **Sau khi sửa & Cấm tuyệt đối**: Chạy test, lint và cổng kiểm tự động (`hard-check.py`, `glossary-check.py`, `task-gate.py`, `handoff-validate.py`), điền kết quả + kế hoạch commit (`commit-plan.md`) vào card. Cấm sửa `.env`/bí mật, `AGENTS.md`, `agents/roles/`, `docs/source/`, file sinh tự động, package/lockfile ngoài task chỉ định; không ghi bí mật vào code/log/card; `websearch`/`webfetch` chỉ `researcher` dùng; `Skill` mâu thuẫn `AGENTS.md` thì theo `AGENTS.md`.

## 5–8. Task Card, Giao tiếp & Bộ nhớ Dự án

- **Task card**: Từ cỡ "vừa" có card YAML frontmatter + checklist `- [ ] AC-xx` (`todo → doing → review → done | blocked`); việc nhỏ ghi `tasks/quick-log.md`. `BOARD.md` và `task-gate.py` theo dõi đủ tiến độ.
- **Icon Header bắt buộc**: Mọi câu trả lời mở đầu bằng `> <EMOJI> **[<ROLE>] <TÊN>** · *<NHIỆM VỤ>*` (`agents/protocols/message.md`).
- **Truy vết & Bàn giao**: Ghi quyết định, kết quả test thật và "Nhật ký phiên" vào card; chỉ tạo `doc/notes/inbox/<Task>-<slug>-<agent>.md` (`handoff-note.md`) khi có bẫy/quyết định cần chuyển giao; cấm sửa trực tiếp `PROJECT-NOTES.md` (chỉ `writer` gộp).

## 9–14. Tài liệu, Rủi ro, GitFlow & Merge Gate

- **Tài liệu & Nghiên cứu**: Giữ bản gốc `docs/source/`, phân tích lệch ở `docs/analysis/` (`intake.md`); research có nguồn/ngày/phiên bản (`researcher.md`).
- **Cổng rủi ro (`agents/protocols/risk-gate.md`)**: Mất code/dữ liệu/migration/xóa hàng loạt phải lập `docs/risk/RK-<n>.md` (`PENDING`), chờ người dùng duyệt rõ số phiếu (commit xóa >=10 file cần `Risk-Approved: RK-<n>`).
- **GitFlow & Worktree**: Nhánh `<type>/<ticket>-<mô-tả>`, commit `<type>(scope): <tóm tắt>` ($\le$ 72 ký tự). Mọi worktree phải đặt ngoài workspace (`WORKTREES_DIR`, kiểm bằng `worktree-manager.py list|sync`, `agents/protocols/worktree-lifecycle.md`).
- **Merge Gate & Launch Gate (Quy tắc 80/20)**: Trước khi MR, chạy `python scripts/merge-gate.py --branch <nhánh> --card <card> --base develop` (đạt 80% Merge-Ready). Trước khi bật cờ mở traffic Production, chạy `python scripts/launch-gate.py --card <card>` (hoàn tất 20% Launch-Ready). Tầng model ở `agents/models.txt`; lỗi 2 lần liên tiếp báo Lead nâng tầng.

## 15–22. Cổng Quy trình Chuyên sâu & Kiểm Tự động (Đọc Protocol khi chạm việc)

15. **Phản biện & Frontend (`agents/protocols/challenger.md`, `agents/knowledge/frontend-patterns.md`)**: Bắt buộc phản biện 3 phương án trước khi thiết kế/code; frontend giữ ranh giới RSC/store/compound.
16. **Subtasks Scrum & Plan Approved (`agents/protocols/full-workflow.md` §16)**: Task lớn bóc subtasks `T-<ticket>.<n>` (mỗi subagent cách ly tối đa 8–10 tool calls, phản hồi 3 dòng), chỉ code sau `[x] Plan Approved by <vai>`.
17. **Chọn & Kiểm chứng Skill (`scripts/skill-router.py` & `scripts/skill-adherence-check.py`)**: Dùng `python3 scripts/skill-router.py -t "<task>"` để định tuyến Top 2–3 skill sát nhất (tránh mù kỹ năng khi nạp 43 skills). Khi tuyên bố dùng skill, BẮT BUỘC ghi `## Bằng chứng áp dụng kỹ năng` trích dẫn quy tắc và file:dòng code cụ thể (`scripts/skill-adherence-check.py` sẽ chặn nếu khai báo suông).
18. **Chu trình 5 bước TDD/ATDD, Excel 14 sheets & Gate 2 (`agents/protocols/task-execution-cycle.md`)**: Thực hiện đủ (1) Phản biện + Generic hóa → (2) Thiết kế + Sơ đồ 5 chuẩn → (3) ATDD 3 tầng + TestLink XML → (4) Hồ sơ `doc/features/<UC>/` + Excel 14 sheets → (5) Swarm Gate 2 trước khi code.
19. **Ngân sách Context (`agents/protocols/context-budget.md`)**: Trần Lead $\le$ 50k, Subagent $\le$ 30k, JIT $\le$ 1.200 tokens; log thô xả vào `inbox/`, compact khi context $\ge$ 75%.
20. **Tự Kích Hoạt Tri Thức & Học Hỏi Tự Trị (Autonomous Self-Learning Gate — BẮT BUỘC, `task-execution-cycle.md` §3)**: Agent BẮT BUỘC tự kích hoạt chu trình học hỏi, cấm chờ nhắc: (1) Sau khi test xanh (kết thúc Fast-Path hoặc task): tự chạy ngầm `knowledge.py learn` ghi bài học & `harness-reflect.py --archive` để hấp thu vào `PROJECT-NOTES.md` và tái biên dịch Knowledge Graph (< 1s); (2) Khi nhận uốn nắn/chấn chỉnh từ người dùng: tự động chạy `harvest-chat.py --reflect` trích xuất chỉ thị từ chat để cập nhật hệ thống; (3) Tri thức chạm quy tắc cốt lõi/bảo mật tự sinh phiếu đề xuất `PRP-xxx.md` (chống trùng lặp); tri thức kỹ thuật/nghiệp vụ nạp thẳng vào bộ nhớ dài hạn.
21. **Vẽ sơ đồ JSON trước → draw.io/PNG sau (`agents/knowledge/diagrams/quy-trinh-ve-so-do-bang-json.md`)**: Đọc mẫu chuẩn → lập bảng sự thật từ code/XERJ → viết `<tên>.spec.json` → chạy `ve-so-do.py <spec> --check-only` → sinh `.drawio` & `.png` → **mở xem từng ảnh bằng mắt** rồi nhúng + ghi nguồn. Cấm viết XML tay / Mermaid thô; file người dùng chỉnh tay phải đồng bộ bằng `--lay-tu-drawio`.
22. **Cổng Kiểm Thuật ngữ, Luật cứng, An ninh & Tay nghề Clean Code (verify-gate.py 8-trong-1)**: Trước khi báo "xong" hoặc tạo MR trên nhánh tính năng, bắt buộc chạy sạch cổng hợp nhất `python3 scripts/verify-gate.py run` (hoặc các cổng thành phần trên diff): `hard-check.py` (luật cứng trong `HARD-RULES.json`), `glossary-check.py` (thuật ngữ chuẩn trong `GLOSSARY.json`), `trojan-check.py` (chặn BiDi CVE-2021-42574 & ký tự tàng hình), `test-integrity-check.py` (chặn gian lận test, assert vô nghĩa, skip test), `dependency-guard.py` (chặn độc supply chain, lifecycle hooks), `markdown-leak-guard.py` (chặn rò rỉ token qua thẻ ảnh), `code-craft-check.py` (chặn hàm > 45 dòng, lồng nhau > 3 tầng, chuỗi if-elif >= 4 nhánh), `liquibase-guard.py` (author="ducnvh", cấm sửa changeset cũ), `skill-adherence-check.py` (thực chứng áp dụng skill) và `task-gate.py` (kiểm đủ AC-xx).
23. **Quy tắc 80/20 & Bằng chứng Agentic Validation (`agents/protocols/launch-readiness.md`)**: Merge-Ready $\neq$ Launch-Ready. PR/Card bắt buộc có Thẻ Bằng Chứng `AGENTIC VALIDATION PROOF` (phân loại Trunk/Leaf, Blast Radius, Kill-Switch, Unit test thực chất, Runtime logs, Visual CDP proof). Trước khi bật feature flag mở traffic trên Production, bắt buộc chạy sạch `python scripts/launch-gate.py --card <card>` để hoàn tất 20% còn lại (kiểm toán an ninh CSO, rà soát hiệu năng/N+1, đánh giá trải nghiệm Human Taste & UX, diễn tập Kill-switch và kế hoạch Canary Rollout).
