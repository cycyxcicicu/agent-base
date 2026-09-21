# Sổ đăng ký skill

Mỗi skill trong `.agents/skills/` phải có **một dòng ở đây** trước khi được commit (`scripts/check-skills` kiểm). Quy trình cài và checklist duyệt: `agents/protocols/skills-policy.md`.

Chỉ **người dùng** duyệt và ghi vào sổ này. Chưa có dòng nào nghĩa là chưa có skill nào được duyệt.

| Skill | Nguồn (URL) | Phiên bản hoặc mã commit | Ngày duyệt | Người duyệt | Vai được dùng | Có script không | Ghi chú |
|---|---|---|---|---|---|---|---|
| diagram-design | https://github.com/cathrynlavery/diagram-design | v2.6 | 2026-09-20 | User | ba, analyst, architect, writer | Không | 41 loại sơ đồ HTML/SVG trực quan không script |
| grilling | Tự viết (lấy ý từ https://github.com/mattpocock/skills) | local | 2026-09-20 | User | architect, analyst, ba | Không | Phỏng vấn Cây Quyết Định đào sâu ranh giới |
| writing-for-agents | https://github.com/mattpocock/skills | main | 2026-09-20 | User | architect, analyst, writer | Không | Chuẩn viết chỉ dẫn và prompt cho Agent |
| domain-modeling | https://github.com/mattpocock/skills | main | 2026-09-20 | User | ba, analyst, architect, product | Không | Rèn luyện mô hình miền và từ điển CONTEXT.md |
| codebase-design | https://github.com/mattpocock/skills | main | 2026-09-20 | User | dev, architect, mobile | Không | Thiết kế mô-đun sâu (Deep Modules) và Seams |
| ponytail-debt | https://github.com/DietrichGebert/ponytail | main | 2026-09-20 | User | debt-hunter, reviewer, dev | Không | Gắn cờ comment nợ kỹ thuật và xuất sổ nợ DEBT.md |
| architecture-decision-records | https://github.com/affaan-m/ECC | main | 2026-09-20 | User | architect, dba, devops | Không | Quản lý vòng đời ADR chuẩn Nygard cho docs/adr/ |
| subagent-driven-development | https://github.com/obra/superpowers | main | 2026-09-20 | User | dev, architect | Không | Điều phối subagent ngữ cảnh sạch và review từng task |
| systematic-debugging | https://github.com/obra/superpowers | main | 2026-09-20 | User | dev, sre, qa | Không | 4 pha gỡ lỗi gốc rễ và condition-based waiting |
| to-spec | Tự viết (lấy ý từ https://github.com/mattpocock/skills) | local | 2026-09-20 | User | product, ba, architect | Không | Chuyển ý tưởng hội thoại thành tài liệu đặc tả docs/spec/ |
| to-tickets | Tự viết (lấy ý từ https://github.com/mattpocock/skills) | local | 2026-09-20 | User | product, ba | Không | Bẻ bài toán thành các phiếu việc nguyên tử tasks/T-xxx.md |
| ui-ux-pro-max | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | v2.0 | 2026-09-20 | User | designer, dev, mobile | Có (Python 3 search.py) | 192 reasoning rules, 79 UI styles, 74 font pairings, 119 UX guidelines, 22 stacks |
| gemini-deep-research | https://github.com/HanaokaYuzu/Gemini-API | local | 2026-09-20 | User | researcher | Có (Python gemini-research.py) | Tích hợp Gemini-API & Deep Research có cổng Ask-Before-Search |
| open-code-review | Tự viết (lấy ý từ https://github.com/alibaba/open-code-review) | local | 2026-09-21 | User | reviewer, dev, qa | Có (Python code_reviewer.py) | Chuẩn AI review code Alibaba: precision over recall, line-level schema, blocking gates |
| i-have-adhd | https://github.com/ayghri/i-have-adhd | main | 2026-09-21 | User | writer, dev, product | Không | Định hình giao tiếp: hành động lên đầu, số hóa nhiệm vụ, triệt tiêu văn hoa rườm rà |
| plan-ceo-review | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | product, architect | Không | Tự viết (ý từ gstack). Thẩm định kế hoạch bằng tư duy Founder/CEO: 10-star product, đảo ngược giả định, scope gating |
| plan-eng-review | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | architect, dev, reviewer | Không | Tự viết (ý từ gstack). Thẩm định kỹ thuật: thử tải 10x, race condition, DB table lock, ranh giới module |
| cso | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | security, reviewer, dev | Có (Python scripts/cso.py) | Tự viết (ý từ gstack). Quét bảo mật tĩnh OWASP, credentials rò rỉ, injection và traversal |
| ship | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | devops, dev | Không | Tự viết (ý từ gstack). Chuẩn bị release: test/lint theo PROJECT.md, bump version, changelog, PR gate (cấm AI tự push/deploy) |
| archify | Tự viết (lấy ý từ https://github.com/tt-a1i/archify) | local | 2026-09-21 | User | architect, designer, writer | Không | Tự viết (ý từ archify). Trình biên dịch Interactive System Map HTML/SVG từ typed JSON IR |
| archify-review | Tự viết (lấy ý từ https://github.com/tt-a1i/archify) | local | 2026-09-21 | User | architect, reviewer, product | Không | Tự viết (ý từ archify). Đánh giá thay đổi kiến trúc qua 3 chiều: Value, Cost, Impact |
| swarm-orchestration | Tự viết (lấy ý từ https://github.com/ruvnet/ruflo) | local | 2026-09-21 | User | architect, dev | Không | Tự viết (ý từ ruflo). Điều phối đàn đa Agent phân tầng, cách ly ngữ cảnh sạch và handoff protocol |
| sparc-methodology | Tự viết (lấy ý từ https://github.com/ruvnet/ruflo) | local | 2026-09-21 | User | dev, architect, qa | Không | Tự viết (ý từ ruflo). Chu trình phát triển SPARC 5 pha: Spec, Pseudocode, Arch, Refinement, Completion |
| careful | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | devops, sre, dev | Không | Tự viết (ý từ gstack). Cổng bảo vệ lệnh hủy diệt: rm -rf, DROP TABLE, force push, hard reset |
| browse | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | qa, researcher, dev, designer | Không | Tự viết (ý từ gstack). Điều khiển trình duyệt đa nền tảng kiểm thử DOM, bắt lỗi console, chụp ảnh bằng chứng |
| qa-web | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | qa, dev | Không | Tự viết (ý từ gstack). Kiểm thử web 3 cấp độ (Quick, Standard, Exhaustive), cô lập lỗi và báo cáo cho Dev (QA không sửa src) |
| office-hours | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | product, ba | Không | Tự viết (ý từ gstack). Buổi phản biện và tư vấn Founder mode Y-Combinator (6 câu hỏi bóc trần nhu cầu) |
| investigate | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | dev, sre, qa | Không | Tự viết (ý từ gstack). Điều tra nguyên nhân gốc rễ lỗi sâu (Root Cause Analysis - 5 Whys) |
| devex-review | Tự viết (lấy ý từ https://github.com/garrytan/gstack) | local | 2026-09-21 | User | dev, reviewer, architect | Không | Tự viết (ý từ gstack). Thẩm định trải nghiệm lập trình viên (Developer Experience: TTHW, CLI clarity, error docs) |






