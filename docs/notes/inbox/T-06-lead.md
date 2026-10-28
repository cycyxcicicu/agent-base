> summary: T-06 lead: phân rã subtask skill compliance và điều phối cầu nối .claude/.qoder
# Task: T-06 - Skill tuân 100% spec Agent Skills trên mọi IDE/AI

Task: T-06        Agent: lead        Ngày: 2026-10-25

- **Mục đích**: Điều phối 7 subtask bằng subagent ngữ cảnh sạch, giữ Plan/QA gate, chốt kế hoạch commit cho người dùng.
- **Đã làm**: tạo card + 7 subtask; xin reviewer duyệt v2 (v1 bị Reject 4 điểm); giao T-06.1..T-06.6; QA độc lập T-06.7 Accepted; cập nhật card, board, kế hoạch commit.
- **Files đã sửa**: `tasks/E1-nen-tang/T-06.md`, `tasks/BOARD.md`, `docs/notes/inbox/T-06-lead.md` (điều phối); sản phẩm của subtask xem mục "File đã đổi" trong card.
- **Skill đã chọn & áp dụng: `codebase-design`** (tách nội dung skill theo ranh giới module, giữ SKILL.md là cửa vào mỏng) và **`open-code-review`** (rà diff trước khi chốt kế hoạch commit).
- **Checklist đã tuân thủ**: (1) Không sửa gì trước khi có `Plan Approved`; (2) Mỗi subtask một subagent mới, không giao cả card cho một phiên; (3) Không chạy lệnh git ghi, không stage hộ người dùng.

## Lưu ý cho agent sau

- **Quyết định**: `.agents/skills/` là nguồn duy nhất; 5/7 công cụ đọc native, chỉ Claude Code và Qoder cần cầu nối cứng. Không nhân bản nội dung, không thêm `CLAUDE.md` thứ hai.
- **Khu vực dễ vỡ**: thêm/bớt skill phải chạy lại `python scripts/link-skills.py`, nếu không `--check` báo thiếu. Không bao giờ dùng `shutil.rmtree` lên `.claude/skills`/`.qoder/skills` vì đó là junction trỏ vào nguồn.
- **Bẫy**: `os.path.islink()` trả `False` với junction Windows — kiểm bằng `os.readlink`/reparse point như `link-skills.py` đang làm.
- **Chưa xác minh**: symlink POSIX và Qoder thật (QA chỉ chạy Windows junction). Khi có máy Linux/macOS, chạy `link-skills.py --check` để xác nhận.
- **Còn Minor**: 3 nhãn trong fence ```dot của `subagent-driven-development/SKILL.md` vẫn nhắc `../requesting-code-review/...`; vô hại với validator, sửa khi có dịp.
- **Chặn merge**: nhánh hiện tại là `main`; người dùng phải tạo `feature/06-skill-spec-compliance` và chỉ stage file trong kế hoạch commit của card. Hai file `archify`/`browse` đang sửa sẵn không thuộc T-06.
