# Kế hoạch: AI chỉ đạo điều khiển `agy` làm việc (agy-bridge)

> Trạng thái: nháp, chờ chạy P0. Người chỉ đạo (Claude/Codex/AI khác) chỉ viết brief, đọc micro-summary, chạy cổng kiểm. `agy` làm toàn bộ việc nặng.

## Mục tiêu
1. Một lệnh chung cho mọi AI: giao việc cho `agy`, nhận về tối đa 3 dòng tóm tắt, toàn bộ log nằm trong file.
2. `agy` làm đúng cấu hình dự án (đã kiểm chứng: tự nạp `AGENTS.md`, `GEMINI.md`, `.agents/rules`).
3. Ưu tiên model flash vì quota: `gemini-3.8-flash-medium` trước, `gemini-3.8-flash-high` khi thất bại, dừng báo người nếu vẫn thất bại. Claude/Opus chỉ dùng khi người đồng ý.

## Dùng lại, không viết lại
- Hợp đồng giao việc và Micro-Summary 3 dòng: `agents/protocols/delegation-prompt.md`.
- Tầng model: `agents/protocols/model-policy.md`, `agents/models.txt`.
- Kênh báo cáo: `docs/notes/inbox/<Task>/` theo `agents/protocols/handoff-note.md`.

## Phạm vi và cấm (áp dụng cho mọi pha)
- Chỉ TẠO file mới. Cấm sửa: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CODEX.md`, `.agents/**`, `.claude/**`, `.codex/**`, `.github/**`, và mọi file đang có thay đổi chưa commit (`git status`).
- Cấm `git add`, `commit`, `push`, `reset`, `clean`. Nhánh hiện tại giữ nguyên.
- Cấm đọc hay in file bí mật (`.env*`, token, khóa).

## Các pha

| Pha | Việc | Người làm | Model | Sản phẩm | Cổng nghiệm thu (máy kiểm) |
|---|---|---|---|---|---|
| P0 | Thử thật `agy -p` và `agy acp` trong thư mục tạm: hỏi quyền, sửa file, giới hạn `--sandbox`, resume phiên, cấu trúc JSON, mã thoát | agy | flash-medium | `docs/notes/inbox/AGY-1/P0-findings.md` (bảng sự thật có lệnh và output thật; mục "CHƯA kiểm chứng") | file tồn tại, mỗi kết luận kèm lệnh chứng |
| P1 | `scripts/agy-bridge.py` (chỉ stdlib): `run --dir --task-file --role --model --effort`; ép tiền tố luật cứng vào prompt; ghi báo cáo đầy đủ ra file; in 3 dòng tóm tắt + `git diff --stat`; thang model; khóa theo thư mục; `--dry-run` | agy | flash-high | script + `tests/test_agy_bridge.py` dùng agy giả | `python3 -m unittest tests.test_agy_bridge -q` xanh; `--dry-run` chạy |
| P2 | `agents/protocols/agy-delegation.md` (dưới 60 dòng): cách gọi bridge, bảng tầng sang model của agy, thang flash, phiên và resume, cổng giám sát theo loại việc | agy | flash-medium | file protocol | `wc -l` dưới 60; không lặp lại nội dung `delegation-prompt.md` |
| P3 | `agents/templates/agy-brief/`: brief ngắn (dưới 25 dòng) cho code, tài liệu, plan, sơ đồ, review; mỗi brief kèm lệnh cổng | agy | flash-medium | 5 file template | mỗi file có mục: phạm vi, cấm, lệnh bằng chứng, "CHƯA kiểm chứng" |
| P4 | Pilot: 1 task tài liệu + 1 task sơ đồ thật qua bridge, flash-medium | agy (mình giao) | flash-medium | báo cáo pilot; lỗi thật ghi vào `agents/knowledge/agy-lessons.md` | `doc-preflight.py`, `ve-so-do.py --check-only` sạch |
| P5 | Sửa brief/protocol theo lỗi pilot; chạy lại pilot | agy | flash-high | bản brief v2 | pilot lần 2 qua cổng, số lượt sửa giảm |
| P6 | Review chéo: phiên agy MỚI, model khác phiên viết, chỉ đọc diff + spec | agy | flash-high (khác phiên viết) | ghi chú review | không có lỗi Major mở |
| P7 | Gắn con trỏ cho từng AI chỉ đạo (Claude, Codex, Gemini): cần người duyệt vì `CLAUDE.md`/`GEMINI.md` là file sinh từ `AGENTS.md` | người duyệt, rồi agy | — | dòng trỏ | `python scripts/refresh.py` không lệch |

## Vai trò giám sát của người chỉ đạo (tốn ít token)
- Viết brief từ template; không chép lại luật vì `agy` đã tự nạp.
- Chạy `agy-bridge` ở nền, được báo khi xong, không hỏi thăm liên tục.
- Chỉ đọc micro-summary. Đọc file báo cáo đầy đủ khi cổng báo lỗi hoặc khi cần phản biện thiết kế.
- Cổng máy kiểm: `doc-preflight.py`, `verify-gate.py`, `hard-check.py`, `ve-so-do.py --check-only`, test có lọc.

## Rủi ro và cách khắc phục
| Rủi ro | Khắc phục |
|---|---|
| `agy` sửa nhầm file đang dở của người khác | `scope_deny`, kiểm `git status` trước và sau mỗi pha, lệch thì dừng |
| `agy acp` khác chuẩn hoặc hỏi quyền kiểu lạ | P0 làm trước; lùi về `agy -p` nếu cần |
| Flash bỏ sót bước do luật dày | brief ngắn có checklist; cổng máy kiểm; thang flash-high |
| Hai AI cùng điều khiển một thư mục | khóa theo thư mục trong bridge |
| Quota cạn giữa chừng | mỗi pha là một phiên riêng, kết quả ghi file, phiên sau đọc file |

## Điều kiện dừng
Pha lỗi 2 lần liên tiếp thì dừng, ghi nguyên nhân vào file báo cáo và báo người.
