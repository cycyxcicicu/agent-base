---
# Lưu thành tasks/<thư mục epic trong tasks/EPICS.md>/T-<số>-<slug>.md (bắt đầu bằng loại việc rồi việc gì, ví dụ T-13-fix-loi-xuat-excel, T-12-feat-them-cot-an-hien)
id: T-0
size: medium
status: todo
owner: dev-a
epic: E1
phase: GĐ1
outputs: []
branch: feature/0-example
requirements: []
slice_type: tracer-bullet
blast_radius: low
blocked_by: []
scope_edit:
  - src/example/**
  - tests/example/**
scope_deny:
  - package.json
---

# T-0: <tiêu đề tiếng Việt nói rõ kết quả, tối đa 70 ký tự, không bắt đầu bằng mã>

## 1. Bản Chất Bài Toán & Lát Cắt Dọc (Tracer-Bullet Vertical Slice)
- **Hành vi End-to-End từ góc nhìn người dùng**: (Mô tả hành vi hoàn chỉnh từ Giao diện ➔ API ➔ Cơ sở dữ liệu ➔ Kiểm thử. Hoàn thành task này là người dùng hoặc test có thể bấm/thử nghiệm được ngay, không chia ngang theo tầng kỹ thuật).
- **Bán kính ảnh hưởng (Blast Radius)**: Ước lượng số lượng modules, call-sites bị ảnh hưởng và mức độ rủi ro lan truyền.
- **Chiến lược nếu là Wide Refactor (Expand-Contract)**:
  - [ ] Pha 1 (Expand): Thêm cấu trúc/trường mới song song với cái cũ (CI xanh 100%).
  - [ ] Pha 2 (Migrate): Chuyển dịch dần các call-sites sang cấu trúc mới.
  - [ ] Pha 3 (Contract): Xóa bỏ cấu trúc cũ sau khi dọn sạch người gọi.

## 2. Ranh Giới Hợp Đồng (Contract & Happy Path)
- **Đầu vào (Input Payload / Request)**:
- **Đầu ra (Output Response / State Change)**:
- **Kịch bản Happy Path**:
- **Tình huống biên (Edge Cases / Exception Flows)**:

## 3. Các Bước Hạt Mịn (Bite-Sized Tasks: 2 - 5 phút/bước)
- [ ] **Bước 1**: Viết Unit Test kiểm tra Happy Path (Test Đỏ) và chạy xác minh test fail.
- [ ] **Bước 2**: Viết mã nguồn tối thiểu để test chuyển sang ĐỎ ➔ XANH.
- [ ] **Bước 3**: Rà soát nợ kỹ thuật: nếu phải đi tắt tạm thời, bắt buộc gắn cờ inline:
  `# debt: <giải pháp>, ceiling: <ngưỡng>, upgrade: <khi nào sửa>`
- [ ] **Bước 4**: Chạy lại toàn bộ test suite để đảm bảo không có lỗi hồi quy.

## 3b. Card giao diện: Mẫu tham chiếu và Kiểm tra bằng mắt (Lead điền, Dev KHÔNG sửa; xem `agents/protocols/ui-fidelity.md`)
- **Mẫu tham chiếu (đường dẫn file cụ thể sẽ copy/đối chiếu)**: (không có thì ghi "không phải card giao diện")
- **Kiểm tra bằng mắt**: (màn hình | 375/768/1440px | điều nhìn thấy thì đạt)

## 3c. Card sửa lỗi: Phiếu lỗi (Lead điền; theo `agents/protocols/bug-repro.md`, bỏ trống nếu không phải sửa lỗi)
- **Nguyên văn báo lỗi**: (dán đúng chữ người báo, đính ảnh nếu có; không diễn đạt lại)
- **Môi trường / phiên bản người báo dùng**: (nhánh, tag, commit, thiết bị)
- **Mục `F-xx` trong Feature Map**: (hoặc "chưa có trong Feature Map")
- **Tái hiện trên `main`**: TÁI HIỆN ĐƯỢC | KHÔNG TÁI HIỆN ĐƯỢC | CHƯA ĐỦ THÔNG TIN (bằng chứng ở `docs/qa/bugs/<Mã>/`)
- **Nguyên nhân gốc**: (`file:dòng` đã đọc; chưa tái hiện được thì chỉ ghi là giả thuyết)
- **Đề xuất luật cứng** (nếu lỗi này đã gặp lần thứ hai; theo `agents/protocols/hard-rules.md`): (lint / test / `hard-check` / merge-gate / hook, hoặc "không")

## 4. Tiêu Chí Nghiệm Thu (Acceptance Criteria)
- [ ] Tính năng End-to-End hoạt động chuẩn xác theo kịch bản Happy Path.
- [ ] Toàn bộ bài test liên quan chạy PASS 100%.
- [ ] Card giao diện: khớp bố cục với file mẫu đã ghi ở mục 3b; QA có ảnh chụp 375/768/1440px và bảng đối chiếu (`docs/qa/<Task>-visual.md`).
- [ ] Không có cờ nợ kỹ thuật nào bị thiếu trigger sửa chữa.
- [ ] Nếu có đụng giao diện Frontend/Mobile: Đạt chuẩn Pre-Delivery Checklist của `ui-ux-pro-max`:
  - [ ] Không dùng emoji làm icon hệ thống (đã dùng SVG Lucide/Phosphor).
  - [ ] Vùng chạm mobile đạt tối thiểu 44×44px, có thuộc tính `cursor-pointer`.
  - [ ] Độ tương phản văn bản đạt chuẩn WCAG AA ≥ 4.5:1 cả Light và Dark Mode.

## 5. Bằng Chứng Thực Thi Từ Terminal (The Iron Law)
> **Quy tắc Thép:** Không bao giờ tuyên bố hoàn thành nếu không có log terminal thực tế chứng minh lệnh chạy thành công với Exit Code 0.
```text
(Dán log stdout/stderr thực tế từ lệnh test/build tại đây)
```

## 6. Nhật Ký Phiên & Lời Phán Quyết (Session Log & Rulings)
- `Ruling: <quyết định kiến trúc> — <lý do> — <hậu quả nếu quyết định sai>`
- Danh sách file đã đổi:
- Ghi chú bàn giao cho Agent sau: (Tạo file `docs/notes/inbox/<Task>-<slug>-<agent>.md`)

## 7. Kế Hoạch Commit (Người Dùng Thực Hiện - AI Không Tự Commit)
```bash
git add <các file thuộc scope_edit>
git commit -m "feat(scope): <mô tả ngắn gọn theo conventional commit>"
```

## 8. Cổng Rủi Ro & Kịch Bản Hoàn Tác (Rollback Plan)
- **Mức độ rủi ro**: [ ] Không rủi ro | [ ] Có rủi ro mất dữ liệu (Yêu cầu phiếu `RK-xxx`)
- **Kịch bản hoàn tác**: `git revert -m 1 <merge commit hash>` (hoặc rollback script nếu có chạm DB).
