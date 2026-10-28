> Task: T-19 · Epic: E2 · Vai: architect

# ADR-19: Thu hẹp phạm vi spec T-11 và phân bổ lát cắt Pilot sang Epic E2

- **Trạng thái**: Proposed
- **Ngày**: 2026-10-28
- **Tác giả**: Architect

---

## 1. Ngữ cảnh & Vấn đề

Tài liệu thiết kế kiến trúc `T-11` (`docs/spec/T-11-knowledge-verification-eval.md`) ban đầu được xây dựng với quy mô rất lớn: 16 vertical slices (I1–I16), dự kiến tạo mới 30–40 tệp tin, tích hợp từ Knowledge Graph, Gatekeeper runtime, Proof system, Eval framework đến Archify visualizer.

Tuy nhiên, đối chiếu thực tế đặt ra các thách thức:
1. **Thiếu danh sách yêu cầu được duyệt từ đầu**: Spec được viết khi chưa có bộ yêu cầu R-xxx được con người phê duyệt (đã được khắc phục bởi T-18).
2. **Quá tải đối với một lượt thực thi (Single Batch)**: Kinh nghiệm vận hành từ dự án GDT và các lượt trước cho thấy việc giao một khối lượng lớn tệp tin cho AI trong một đợt duy nhất dẫn đến bỏ sót, ảo giác hoặc gãy kiểm thử.
3. **Cần chứng minh tính khả thi trên một lát cắt thật trước**: Cần ưu tiên các thành phần cốt lõi (CLI verification, catalog validator, task discovery đồng nhất) trước khi xây dựng engine phức tạp.

---

## 2. Các phương án xem xét (Ma trận 3 Phương án)

| Tiêu chí | Phương án 1: Giữ nguyên phạm vi T-11 ban đầu | Phương án 2: Thu hẹp thành lát cắt Pilot trong Epic E2 (Khuyến nghị) | Phương án 3: Tách toàn bộ module tri thức thành Repo riêng |
|---|---|---|---|
| **Mô tả** | Giữ nguyên 16 slice I1–I16 trong một task T-11 duy nhất và cố gắng thực hiện đồng loạt. | Chia nhỏ spec T-11 thành các card độc lập T-20..T-29 trong Epic E2; hoãn các phần chưa cấp thiết (I6, I12, I14). | Tách `agent_core/knowledge` và `verification` ra một repository độc lập rồi import làm dependency. |
| **Ưu điểm** | Đầy đủ tính năng như thiết kế lý tưởng ban đầu. | Phạm vi từng card rất rõ ràng, kiểm soát được rủi ro, chạy TDD tuần tự, dễ debug. | Tách biệt hoàn toàn mã nguồn khung và ứng dụng. |
| **Nhược điểm** | Rủi ro thất bại cực cao (blast radius lớn, vỡ ngữ cảnh mô hình, xung đột file). | Cần điều phối nhiều card con và cập nhật tài liệu liên tục. | Chi phí quản lý gói, phiên bản và CI tăng vọt khi nhu cầu chưa thực sự kiểm chứng. |
| **Độ phù hợp** | Không khả thi | **Phù hợp nhất cho giai đoạn hiện tại** | Quá sớm (Over-engineering) |

---

## 3. Quyết định đề xuất (Khuyến nghị)

- Chọn **Phương án 2: Thu hẹp thành lát cắt Pilot trong Epic E2**.
- **Căn chỉnh cấu trúc Cổng kiểm soát**:
  - Chuyển đổi 7 gate (G1–G7) sang chuẩn **8 Cổng kiểm soát (Cổng 0–7)** và vòng đời 13 bước của `agents/protocols/task-loop.md`.
  - Bổ sung Cổng 4 (Actor/phòng ban/hệ thống ngoài) và chế độ A4 (kiểm tuân thủ độc lập của reviewer/qa).
- **Phân bổ lát cắt sang Epic E2**:
  - I1 (Catalog & Validator) → `T-20`
  - I2 (Context CLI & Token Budget) → `T-21`
  - I3–I5 (Task Discovery lồng Epic) → `T-22`
  - *(Mới)* Cổng tiền điều kiện `claim_task` → `T-23`
  - *(Mới)* Ma trận truy vết RTM → `T-24`
  - I7–I9 (Proof Bundle & CLI Verify Bootstrap/Upgrade) → `T-25`
  - *(Mới)* Harness tái hiện lỗi 2 lần & Feature Map → `T-26`
  - I10–I11 (Eval v2 có bằng chứng, fix lỗi `{}`) → `T-27`
  - I15 (Phân phối sạch & CI integration) → `T-28`
  - I16 (Review & QA độc lập toàn bộ E2) → `T-29`
- **Hoãn sau pilot**: Hoãn I6 (gatekeeper runtime engine), I12 (seed tri thức lớn) và I14 (sơ đồ Archify).

---

## 4. Rủi ro & Biện pháp giảm thiểu

- **Rủi ro**: Việc hoãn I6 khiến hệ thống chưa có runtime gatekeeper tự động chặn ghi ở tầng OS.
  - **Giảm thiểu**: Bù đắp bằng công cụ chẩn đoán cố vấn `claim_task` (T-23) và cổng kiểm tra trước khi tích hợp `merge-gate.ps1`.
- **Rủi ro**: Thay đổi cấu trúc spec làm mất dấu vết các quyết định trước.
  - **Giảm thiểu**: Giữ nguyên vẹn văn bản spec T-11 và chỉ thêm các ghi chú căn chỉnh (T-19.1, T-19.2) giải thích rõ ràng lý do "đổi vì".
