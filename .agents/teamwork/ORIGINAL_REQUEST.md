# Original User Request

## 2026-10-28T00:23:22Z

Hoàn thiện và chuẩn hóa cấu trúc repository agent-base (D:\congty\agent-base), tích hợp triệt để các bài học, quy trình và mẫu phân bổ thư mục từ gdt-workspace-goc và Lauren Tan AI SDLC, đảm bảo phân phối sạch và kiểm thử tự động 100%.

Working directory: D:\congty\agent-base
Integrity mode: development

## Requirements

### R1. Chuẩn hóa Phân phối và CI Tự Động (T-28 / I15)
- Cập nhật `agents/manifest.txt` phân loại chuẩn xác 4 nhóm tệp: `copy` (khung lõi, schema, protocols, scripts kiểm chuẩn), `template` (tệp mẫu cho dự án con tự do tùy biến), `fresh` (tệp khởi tạo mới sạch sẽ), `generated` (adapters sinh tự động).
- Tích hợp các bước kiểm chuẩn mới vào `.github/workflows/check.yml`: `python scripts/knowledge.py validate`, `python scripts/rtm.py --check`, kiểm tra discovery và proof trên Ubuntu runner.
- Giữ nguyên vẹn 100% các bước kiểm tra CI hiện hữu (`sync-adapters --check`, `notes-index --check`, `unittest discover`).

### R2. Bảo toàn Tùy chỉnh Dự án và Seed Tri thức Thực tế từ GDT Workspace
- Xây dựng seed tri thức chuẩn mực `agents/knowledge/knowledge-manifest.json` và catalog mẫu `examples/knowledge/catalog.json` phản ánh đúng cấu trúc phân loại dự án (frontend, backend, shared, deployment).
- Nâng cấp `scripts/bootstrap-project.py` và `scripts/agent-base-diff.py` để phân biệt chính xác tệp framework vs tệp dự án tùy biến, đảm bảo nâng cấp bảo toàn tùy chỉnh người dùng, không ghi đè dữ liệu.
- Áp dụng phân bổ thư mục chuẩn xác: `docs/design/`, `docs/runbooks/`, `docs/spec/`, `docs/requirements/`, `agent_core/`, `agents/protocols/`.

### R3. Nghiệm thu Kỹ thuật Toàn diện Epic E2 (T-29 / I16)
- QA độc lập chạy toàn bộ test suite (mốc >294 unit tests stdlib), đảm bảo 100% test pass không lỗi hồi quy.
- Kiểm tra tính nhất quán giữa task cards (`tasks/BOARD.md`), sổ tay dự án (`docs/notes/INDEX.md`), và ma trận truy vết (`build/rtm/RTM.md`).
- Lập báo cáo nghiệm thu kỹ thuật chính thức cho Epic E2.

## Acceptance Criteria

### Phân phối & Kiểm chuẩn CI
- [ ] `agents/manifest.txt` khai báo đầy đủ các module `agent_core/knowledge/`, `agent_core/verification/`, CLI scripts, schemas JSON và protocols mới.
- [ ] Workflow `.github/workflows/check.yml` qua kiểm tra cú pháp YAML và chạy kiểm thử không phát sinh lỗi.
- [ ] Kiểm thử phân phối `tests/test_t11_distribution.py` và kiểm thử nâng cấp `tests/test_t11_upgrade_compatibility.py` đạt 100% PASS.

### Seed Tri thức & An toàn Dữ liệu
- [ ] Seed tri thức không chứa thông tin nhạy cảm, tên cá nhân hay dữ liệu bí mật nội bộ.
- [ ] Seed tri thức qua kiểm chuẩn `scripts/knowledge.py validate` exit code 0.
- [ ] Bootstrap dự án mới vào thư mục cô lập tạo ra một dự án hoạt động độc lập, chạy được `doctor` và bộ kiểm chuẩn.

### Độ Bao phủ & Toàn vẹn Hệ thống
- [ ] Full test suite (`python -m unittest discover -s tests`) chạy đạt 100% OK.
- [ ] Không thêm bất kỳ thư viện bên ngoài (dependency) nào ngoài thư viện chuẩn Python (stdlib).
- [ ] `scripts/task-board.py` báo 29 card 0 lỗi và `scripts/notes-index.py` đồng bộ đầy đủ các ghi chú bàn giao.
