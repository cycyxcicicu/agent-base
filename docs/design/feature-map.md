> Task: T-26 · Epic: E2 · Vai: writer

# Bản đồ tính năng (Feature Map): CLI Kiểm chứng & Khung Tái hiện lỗi

Tài liệu bản đồ tính năng hỗ trợ các agent và kỹ sư định hướng, vận hành và kiểm chứng tự động các bề mặt CLI của nền tảng mà không cần phỏng đoán.

---

## 1. Danh mục tính năng (Sub-features)

1. **Cài đặt kiểm chứng trên fixture cô lập (`verify bootstrap`)**:
   - Tự động tạo môi trường `TemporaryDirectory` có đánh dấu ownership sentinel.
   - Chạy lệnh cài đặt `bootstrap-project.py` theo manifest phân phối.
   - Thu thập lệnh, thời gian thực thi, băm SHA256 của stdout/stderr và kiểm tra các hậu điều kiện (exit 0, metadata `.agent-base.json`, template fresh).
   - Tự động dọn dẹp fixture và xuất Proof bundle độc lập.

2. **Kiểm chứng quy trình nâng cấp và giải quyết xung đột (`verify upgrade`)**:
   - Khởi tạo fixture baseline, chèn tùy chỉnh cục bộ của người dùng và tạo tình huống xung đột tệp tracked.
   - Thẩm định chế độ `dry-run`: đảm bảo 100% không làm biến đổi byte nào trên đĩa trước khi nâng cấp.
   - Chạy `agent-base-diff.py` từ bên trong fixture để phát hiện và liệt kê tệp bị sửa đổi.
   - Kiểm tra tính bảo toàn tùy chỉnh (preserve customization) và tính lũy đễ (idempotent rerun).

3. **Harness tái hiện lỗi hai lần có reset (`verify repro`)**:
   - Thực thi kịch bản lần 1 -> reset trạng thái môi trường -> thực thi lần 2.
   - Phân định kết luận khách quan: `reproduced` (2/2 lần đều thấy lỗi), `not_reproduced` (0/2), `inconclusive` (thất thường 1/2 hoặc lỗi môi trường).
   - Chế độ Verify: Đối soát hai chiều giữa bản gốc (thấy lỗi 2/2) và bản vá (hết lỗi 0/2).

4. **Kiểm chuẩn tính toàn vẹn bằng chứng ngoại vi (`proof-check.py`)**:
   - Thẩm tra cấu trúc JSON schema Draft 2020-12 của Proof bundle.
   - Quét và đối chiếu băm SHA256 byte thực tế của từng tệp artifact trên đĩa.

---

## 2. Cách tiếp cận từ góc nhìn người dùng (User Entrypoints)

- **Kiểm chứng cài đặt framework**:
  ```bash
  python scripts/verify.py bootstrap --evidence-root build/evidence
  ```
- **Kiểm chứng quy trình nâng cấp dự án**:
  ```bash
  python scripts/verify.py upgrade --evidence-root build/evidence
  ```
- **Tái hiện lỗi theo kịch bản recipe**:
  ```bash
  python scripts/verify.py repro --recipe tests/fixtures/sample-bug.json --evidence-root build/evidence
  ```
- **Kiểm tra tệp bằng chứng sau khi hoàn tất**:
  ```bash
  python scripts/proof-check.py --bundle build/evidence/<run_id>/proof.json
  ```

---

## 3. Cách điều khiển bằng Harness tự động (Automation Harness)

- **Gọi trực tiếp qua API Python**:
  ```python
  from agent_core.verification.bootstrap import run_bootstrap_verification
  from agent_core.verification.upgrade import run_upgrade_verification
  from agent_core.verification.repro import run_repro_harness, run_verify_mode

  proof_file = run_bootstrap_verification(evidence_root="build/evidence")
  ```
- **Chế độ giữ lại fixture để điều tra (`--keep-fixture`)**:
  - Khi cần debug chi tiết hoặc xem xét hiện trường thất bại, truyền cờ `--keep-fixture` để harness bỏ qua bước `shutil.rmtree(fixture_dir)`.

---

## 4. Điểm dễ nhầm lẫn (Gotchas & Misconceptions)

1. **Nhầm lẫn giữa kiểm chứng cố vấn và cưỡng chế cấp Host**:
   - Harness hoạt động ở tầng chẩn đoán và filesystem cục bộ. Bằng chứng có cờ `needs_independent_review: true` và không thay thế thẩm quyền kiểm toán của con người.
2. **Tuyệt đối không chạy chuỗi lệnh tự do từ bên ngoài**:
   - Recipe tái hiện lỗi chỉ chấp nhận mảng `argv` được phân tách tường minh, không sử dụng `shell=True` hay thực thi chuỗi lệnh shell không rõ nguồn gốc.
3. **Template vs Copy trong Manifest**:
   - Các tệp `template` (như `models.txt`, `quick-log.md`) thuộc quyền tùy biến của dự án đích và không bị coi là xung đột framework khi người dùng sửa đổi. Chỉ các tệp `copy` (như `AGENTS.md`) mới được theo dõi đồng bộ hai chiều.
