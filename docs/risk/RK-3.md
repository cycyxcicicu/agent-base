# RK-3: Sửa đổi các tệp dùng chung để phân phối, tích hợp CI và nâng cấp tri thức quy trình (T-28)

Status: APPROVED
Ngày lập: 2026-10-28        Người lập: lead (Antigravity)
Mốc kiểm tra: nhánh main, HEAD f12b1a23169da79ec8490b64d51a90c685b8f76f
Yêu cầu: Triển khai Task T-28 thuộc Epic E2: đưa các module, schema, script, protocol mới vào bản phân phối manifest, tích hợp các bước kiểm chuẩn vào CI, và bảo toàn tùy chỉnh khi nâng cấp.

## Danh sách tệp dùng chung sẽ sửa đổi
1. `agents/manifest.txt`: Bổ sung các module (`agent_core/knowledge/`, `agent_core/verification/`), các script mới (`scripts/knowledge.py`, `scripts/verify.py`, `scripts/rtm.py`, `scripts/task-claim-check.py`, `scripts/proof-check.py`), các schema JSON (`schemas/knowledge.schema.json`, `schemas/proof.schema.json`), và các protocols mới. Seed `knowledge-manifest.json` được xếp vào nhóm `template/fresh`.
2. `.github/workflows/check.yml`: Nối thêm các bước CI kiểm tra tính hợp lệ (`python scripts/knowledge.py validate`, `python scripts/rtm.py --check`), giữ nguyên vẹn toàn bộ các bước kiểm tra hiện có (`sync-adapters --check`, `notes-index --check`, `unittest discover`).
3. `scripts/bootstrap-project.py`: Đồng bộ để sao chép đúng các tệp mới và tạo dự án mới với seed tri thức sạch sẽ (không mang dữ liệu riêng của repo agent-base).
4. `scripts/agent-base-diff.py`: Đảm bảo quy trình phát hiện khác biệt hai chiều phân biệt chính xác tệp copy vs tệp template/fresh, giữ nguyên tùy chỉnh dự án khi nâng cấp.

## Đánh giá rủi ro & Tác động
- **Rủi ro phân phối**: Nếu khai báo nhầm tệp `copy` thay vì `template/fresh`, quá trình nâng cấp dự án con có thể ghi đè lên các tệp cấu hình riêng của dự án đó.
- **Rủi ro CI vỡ**: Cấu hình cú pháp YAML sai hoặc gọi lệnh thiếu module trên môi trường Ubuntu runner của GitHub Actions sẽ làm vỡ pipeline CI.
- **Rủi ro rò rỉ dữ liệu**: Template seed tri thức nếu copy nguyên trạng có thể làm lọt thông tin của repo gốc sang dự án mới.

## Biện pháp kiểm soát & Giảm thiểu
- Seed `agents/knowledge/knowledge-manifest.json` và `examples/knowledge/catalog.json` chỉ chứa dữ liệu giả định/trung lập, trạng thái `draft`, không chứa tên dự án/người dùng.
- Kiểm tra cú pháp YAML của `.github/workflows/check.yml` bằng Python (`python -c "import yaml; yaml.safe_load(open('.github/workflows/check.yml'))"`).
- Kiểm tra toàn bộ quy trình bootstrap và upgrade thông qua bài test tích hợp `tests/test_t11_distribution.py` và `tests/test_t11_upgrade_compatibility.py` trên fixture cô lập.

## Kịch bản hoàn tác
- Nếu gặp sự cố trước commit: Hoàn tác các thay đổi trên working tree bằng `git checkout -- .github/workflows/check.yml` và dọn các tệp tạm.
- Nếu gặp sự cố sau khi merge: Lập phiếu hoàn tác và thực hiện `git revert -m 1 <merge commit>`.

## Chấp thuận
- **Người dùng (Huỳnh Đức), ngày 2026-10-28**, nguyên văn trong chat: "duyệt RK-3". Claude ghi lại theo yêu cầu; HEAD lúc ghi vẫn là `f12b1a23169da79ec8490b64d51a90c685b8f76f`, khớp mốc kiểm tra.
- **Bổ sung sau duyệt (2026-10-28, Claude, theo yêu cầu "áp dụng chuẩn chặt" của người dùng): phiếu đổi nội dung nên trở lại PENDING, cần người dùng nhắn lại "duyệt lại RK-3".** Thay đổi: trong `.github/workflows/check.yml`, bước "Diagnostic Task Claim Check (Advisory)" chỉ chạy khi card `tasks/E2-tri-thuc-quy-trinh/T-12.md` tồn tại và luôn kết thúc `exit 0` (đúng nghĩa "chẩn đoán cố vấn", không làm CI đỏ). Lý do: `check.yml` thuộc nhóm `gitonly` nên dự án mới nhận bản này; không có card T-12 thì bước cũ làm CI của dự án đó đỏ. Chỉ giảm rủi ro, không thêm quyền. HEAD vẫn `f12b1a23169da79ec8490b64d51a90c685b8f76f`.
- **Duyệt lại (2026-10-28):** người dùng (Huỳnh Đức) nhắn nguyên văn trong chat: "duyệt lại RK-3". Claude ghi lại. HEAD lúc ghi vẫn là `f12b1a23169da79ec8490b64d51a90c685b8f76f`. Phạm vi duyệt lại gồm cả bổ sung ở trên (bước claim check có điều kiện, `exit 0` trong `check.yml`).
- Phạm vi chấp thuận (lần trước): đúng bốn file liệt kê ở mục "Danh sách tệp dùng chung sẽ sửa đổi". **Không bao gồm** `scripts/knowledge.py`, `agent_core/knowledge/catalog.py`, `examples/knowledge/sample.md` (T-28 sửa ngoài phạm vi, ngoài phiếu này).
