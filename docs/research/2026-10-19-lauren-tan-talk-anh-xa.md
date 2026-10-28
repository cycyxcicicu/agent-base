# Brief: bài nói của Lauren Tan (Cursor / SpaceX AI) và việc áp dụng vào agent-base

Đọc ngày 2026-10-19. Hạn xem lại: 2027-01-17 (90 ngày).

## Nguồn và độ tin cậy
- **Cập nhật 2026-10-19: đã có transcript của video** do người dùng dán vào phiên (bản chép lời tự động, có lỗi chính tả như "Gary Tan" thay vì Garry Tan, "bug bar", "PAC", "Grockbot"; chưa có video gốc để nghe lại). Các bản tóm tắt NotebookLM trước đó đã **đối chiếu với transcript**: nhìn chung đúng ý; các chỗ lệch ở mục "Đối chiếu transcript" bên dưới. Vẫn là bản chép tự động nên chi tiết nhỏ (tên riêng, con số) cần nghe lại video khi quan trọng.
- Phần đầu của transcript thứ nhất (đoạn "the best use of AI is as a pair programming partner... I spend more time reviewing what the AI did") là của **một người dẫn khác**, không phải Lauren Tan; Lauren bắt đầu sau câu "So yeah, today...". Đừng gán nhận định đó cho Lauren.
- Việc áp dụng bên dưới là **diễn giải của agent-base**, không phải bản sao của hệ thống Cursor. Lauren nói rõ Dune là "tập hợp ý tưởng và nguyên tắc", **không mã nguồn mở**; Pstack thì công khai ("search Pstack cursor on Google"), chưa xem mã.

## Đối chiếu transcript với bản tóm tắt NotebookLM
- **Đúng**: Pstack (Potato Stack, trêu Gstack của Garry Tan); skill `create` và `maintain verification skill`; Feature Map gồm tính năng và tính năng phụ, cách vào từ góc nhìn người dùng, phím tắt, thuộc tính DOM/CDP; Eval playbook (điều phối viên lập rubric, sub-agent trong thư mục "đặt tên khéo" vì agent đoán được và đổi hành vi, trọng tài là model khác, nhiều model, `/loop` tới 10/10); Benny tái hiện lỗi rồi báo "đã sửa trên main"; không có trần PR (khoảng 50 đến khoảng 1.000 dòng); cấm `useEffect`; cấm comment; kiểm đồ thị phụ thuộc giữa electron main và renderer; Bugbot chạy trên CI; số liệu 1.000 PR / gần 800 PR ngày 12 / 20 PR một đêm / hơn 600 PR refactor.
- **Chi tiết transcript thêm hoặc làm rõ**:
  - Lý do cấm comment: agent hay viết chú thích kể lại lịch sử không liên quan ("Lauren bảo không bao giờ làm thế này") do hiểu sai một câu nhận xét. Đây là vấn đề cụ thể và hẹp, nên agent-base chỉ lấy **phiên bản hẹp** (cảnh báo comment kể chuyện trò chuyện, `no-conversation-comments` trong `examples/hard-rules/`), không cấm mọi comment.
  - **Lớp ràng buộc mạnh nhất là cấu trúc quy ước**: một tính năng gom trong một thư mục, một cách duy nhất để tạo tính năng mới, vì agent thích sao chép mẫu có sẵn; nguyên tắc "đường ngắn nhất là đường tốt nhất". Agent-base thêm luật `path_must_match`.
  - Ba cách tránh lặp lỗi review: biến thành luật lint/CI, hoặc **loại bỏ hẳn vấn đề bằng thiết kế** (cách thứ ba mà bản NotebookLM bỏ sót; đã ghi vào `hard-rules.md` mục 2b). Ông cũng nhắc ngôn ngữ có trình biên dịch chặt (Rust) như một lớp ràng buộc cứng.
  - Lòng tin: ông **không khuyên tin mù quáng** vào mình hay Pstack, khuyên tự xây hoặc fork skill; khuyên **bắt đầu ở local** để quan sát agent rồi mới tới cloud và tự merge.
  - "Control glass": ông nói mã của skill "không quá thú vị, agent tự làm được"; điều quan trọng là Feature Map đi kèm. Skill xác minh là một CLI điều khiển ứng dụng qua CDP hoặc tiện ích của Apple.
  - Ông thừa nhận làm việc ở phòng thí nghiệm AI có token không giới hạn, nên không nên coi cách làm là vừa túi tiền của mọi đội.
  - Khẳng định về chi phí token của Grok 4.6 ("tôi tin là bằng 4.5") do chính người nói không chắc; không dùng làm số liệu.
- **Lệch nhỏ**: NotebookLM đôi chỗ viết liền các tầng Dune thành "5 tầng đánh số"; transcript nói theo kiểu "các lớp" và nhấn mạnh ranh giới giữa **cứng** (cấu trúc mã nguồn, phân tích tĩnh/CI/compiler) và **mềm** (rules, Bugbot, skills, style guide), không cam kết đánh số chính xác.

## Điều bài nói (theo NotebookLM), rút gọn
- Kỹ năng xác minh: agent tự chạy ứng dụng, dùng CDP/Apple simulator, chụp CPU trace, flame graph, heap snapshot; kết quả đưa thẳng vào ngữ cảnh agent.
- Feature Map: tính năng và tính năng phụ, đường điều hướng, phím tắt, thuộc tính DOM/bộ chọn CDP. Dựng bằng `create verification skill`, cập nhật bằng `maintain verification skill` (trong bộ Pstack).
- Eval playbook: điều phối viên lập rubric, các sub-agent chạy trong thư mục cô lập đặt tên khéo để không biết đang bị kiểm, trọng tài là model khác, nhiều model, lặp (`/loop`) tới 10/10.
- Dune: 5 tầng ràng buộc. Hai tầng đầu là cứng (cấu trúc mã nguồn gom theo tính năng; phân tích tĩnh/CI/compiler gồm cấm `useEffect`, cấm comment, kiểm đồ thị phụ thuộc giữa tiến trình main và renderer); ba tầng sau là mềm (luật Bugbot, skill/prompt, style guide).
- **PR nhỏ: không có trần cứng**, từ khoảng 50 đến khoảng 1.000 dòng; mục đích là lịch sử git rõ và rollback dễ.
- **Không có giới hạn "review tối đa 3 lần"**. Cơ chế thật: lỗi lặp lại thì đổi nhận xét review thành linter/CI/compiler rule.
- Benny: agent trên đám mây nhận báo lỗi từ Slack, mở máy ảo, chạy ứng dụng, dùng kỹ năng xác minh và Feature Map để tái hiện, báo lỗi còn hay đã sửa trên `main`. Cảnh báo: xây lòng tin và bài kiểm thử ở local trước khi bung hàng loạt agent đám mây.
- Số liệu (theo lời kể): khoảng 1.000 PR merge tháng trước, gần 800 PR tính đến ngày 12 tháng này, khoảng 20 PR tự merge một đêm, hơn 600 PR để refactor Grockbot sang Dune.

## Ánh xạ vào agent-base

| Ý trong bài | Trạng thái | Ở đâu |
|---|---|---|
| Feature Map (4 nhóm trường) | Đã làm (mẫu 7 trường, bao trùm 4 nhóm) | `agents/protocols/feature-map.md` |
| `create`/`maintain verification skill` | Đã làm cho Feature Map | skill `feature-map` |
| Bản đồ bị lệch mã | Đã làm, là ràng buộc cứng | `scripts/feature-map-check.py`, CI |
| Eval playbook (rubric, cô lập, trọng tài khác, nhiều model, leo núi) | Đã làm, **chưa chạy với model thật** | `agents/protocols/skill-eval.md`, `scripts/skill-eval.py` |
| Nhận xét review lặp lại thành luật cứng | Đã làm | `agents/protocols/hard-rules.md`, `scripts/hard-check.py`, `docs/HARD-RULES.json` |
| PR nguyên tử | Đã làm, **chỉ cảnh báo** (bài không có trần cứng) | `agents/protocols/atomic-changes.md`, `scripts/merge-gate.py` |
| Tái hiện lỗi trước khi sửa | Đã làm bản cục bộ | `agents/protocols/bug-repro.md` |
| Làm ở máy nội bộ trước | Đã ghi vào giao thức | `feature-map.md`, `skill-eval.md` |
| Kiểm tra đồ thị phụ thuộc giữa các lớp | Làm một phần: cấm import theo mẫu chữ | `forbid_regex` trong `hard-check` (chưa có đồ thị phụ thuộc thật) |
| Gom mã theo tính năng (colocation), cấu trúc quy ước | Đã làm: luật `path_must_match` (máy ép vị trí file) và quy ước trong bản đồ mã nguồn | `hard-check`, `codebase-map`, `examples/hard-rules/` |
| Cấm comment (phiên bản hẹp: comment kể chuyện trò chuyện) | Làm bản hẹp, chỉ cảnh báo | `no-conversation-comments` trong `examples/hard-rules/` |
| Loại bỏ vấn đề bằng thiết kế (không chỉ thêm luật) | Đã ghi thành nguyên tắc | `hard-rules.md` mục 2b |
| Kỹ năng xác minh hiệu năng: CPU trace, heap snapshot, flame graph, Apple simulator | **Chưa làm** (mới có `browse`/Playwright cho thao tác và kiểm bằng mắt) | khoảng trống |
| Cloud agent tái hiện lỗi (Benny) | **Cố ý không làm** | thay bằng `bug-repro` chạy cục bộ |
| Tự động merge PR | **Cố ý không làm** (người dùng giữ quyền merge) | AGENTS.md mục 12 |
| Cấm `useEffect`, cấm mọi comment | **Cố ý không đưa vào khung** (luật riêng của một đội/stack; agent-base còn yêu cầu docstring tiếng Việt và comment `# debt:`) | chỉ là ví dụ trong `examples/hard-rules/` |
| Bugbot (review tự động trên CI) | Chưa làm trên CI | có vai `reviewer` và `agent_core/eval/code_reviewer.py` chạy tay |

## Điều chưa xác minh
- Chi tiết nhỏ trong bản chép tự động (tên riêng, con số) vì chưa nghe lại video; đã đối chiếu với NotebookLM nên ý chính khá chắc.
- Cách Pstack thực sự dựng Feature Map; skill `feature-map` của agent-base là bản tự viết theo mô tả, chưa so với bản gốc.
- Chi phí token và chất lượng thật của Eval và Feature Map khi chạy với model thật.

## Việc còn lại nếu muốn bám sát hơn
1. Skill xác minh hiệu năng (thu CPU trace/heap snapshot qua Playwright hoặc CDP cho ứng dụng web), cần thử với một dự án giao diện thật trước.
2. Chạy review tự động trên CI (`code_reviewer.py`) ở chế độ chỉ cảnh báo.
3. Kiểm đồ thị phụ thuộc thật (thay cho `forbid_regex`) khi có dự án cần ranh giới module chặt.
