# Định nghĩa hoàn thành (theo cỡ việc)

Ghi chú: AI chỉ commit hoặc push khi người dùng yêu cầu rõ và duyệt từng lệnh. Các mục về commit, nhánh, Merge Request là việc của **người dùng** (AI chuẩn bị kế hoạch và có thể chạy giúp theo yêu cầu).

## Dẫn chứng bắt buộc khi kết luận (mọi cỡ việc)

Agent hay khẳng định rất tự tin một nguyên nhân hay một kết quả chưa từng kiểm. Mọi kết luận ghi vào card hoặc ghi chú bàn giao phải kèm dẫn chứng; **thiếu dẫn chứng thì Reviewer trả lại**, không duyệt.

- **Nguyên nhân lỗi**: ghi `file:dòng` đã **đọc thật** (không suy từ tên file hay mô tả lỗi), lệnh đã chạy và đầu ra liên quan, và cách tái hiện. Chưa tái hiện được thì ghi "chưa tái hiện" và gọi đó là giả thuyết, không gọi là nguyên nhân.
- **"Đã sửa" / "đã chạy" / "test qua"**: ghi lệnh đã chạy và kết quả thật (số test qua/lỗi, mã thoát), không ghi "chắc là qua".
- **"Không còn xảy ra" / "đã có sẵn"**: ghi nơi đã kiểm (nhánh, commit, màn hình) và cách kiểm. Với báo lỗi, theo `agents/protocols/bug-repro.md` (hai lần chạy: phiên bản người báo dùng và `main`).
- **Chỗ chưa xác minh**: nêu thẳng ở mục "Giả định chưa kiểm chứng" của ghi chú bàn giao. Không viết như đã chắc chắn.
- Skill `investigate` và `systematic-debugging` đã yêu cầu điều này khi điều tra lỗi; mục này áp cho **mọi** loại kết luận.

## Subtask Hạt Mịn (Micro-DoD)
Áp dụng cho từng Subagent khi thực hiện một Subtask `T-<ticket>.<n>`:
- [ ] **Ranh giới**: Chỉ sửa các file thuộc phạm vi được giao của Subtask. Nếu đụng file của Subtask khác: tuân thủ Quy tắc Sửa File Chéo bên dưới.
- [ ] **Kiểm thử thực tế**: Lệnh test rút gọn (`pytest -q`, `alembic upgrade head`) chạy thực tế có Exit Code 0 (PASS 100%). Cấm "fake done" khi chưa chạy test.
- [ ] **Trần số bước**: Hoàn thành trong tối đa 8–10 tool calls.
- [ ] **Ghi chú bàn giao**: Có file note `docs/notes/inbox/<Task>/<Task>.<Subtask>-<agent>.md` có đủ: Mục đích, Files đã sửa, Kết quả test, Bàn giao cho Subtask kế tiếp.

## Quy Tắc Sửa File Chéo Giữa Các Subtask (Cross-Subtask Edits - Bộ 7 Kịch Bản)
Khi Subtask hiện tại BẮT BUỘC phải sửa một file thuộc quyền sở hữu của Subtask khác hoặc tài nguyên hệ thống dùng chung:
1. **File thuộc Subtask ĐÃ XONG (Upstream)**:
   - Được phép sửa phẫu thuật tối thiểu (Surgical Patch: thêm field, type hint, fix bug nhỏ).
   - BẮT BUỘC chạy lại regression test của Subtask trước để đảm bảo không làm vỡ code cũ.
   - Bắt buộc ghi rõ vào Handoff Note: `- Sửa bổ sung cho <Subtask_cũ>: <lý do và nội dung sửa>`.
2. **File thuộc Subtask CHƯA LÀM (Downstream)**:
   - TUYỆT ĐỐI CẤM code hộ toàn bộ logic của Subtask sau.
   - Dùng Stub / Mock interface tối thiểu để Subtask hiện tại chạy test qua.
   - Ghi yêu cầu vào Handoff Note để Subtask sau triển khai đúng hợp đồng.
3. **File cấu hình dùng chung (`config.py`, `__init__.py`)**:
   - Chỉ được phép THÊM (Append / Register), CẤM sửa hoặc xóa code hiện có của Subtask khác.
4. **Nếu là Breaking Change (Làm sai lệch thiết kế của Subtask cũ)**:
   - DỪNG LẠI NGAY, đổi trạng thái sang `BLOCKED`, báo Lead và Reviewer thẩm định lại kế hoạch, không tự ý sửa lan man.
5. **File Database Migration (`alembic/versions/*.py`, SQL scripts)**:
   - TUYỆT ĐỐI CẤM sửa hoặc xóa file migration đã sinh của Subtask trước (tránh sai lệch checksum và crash dữ liệu).
   - Bắt buộc tạo file migration mới nối tiếp (`alembic revision`) với `down_revision` trỏ đúng vào head hiện tại, cấm tạo nhánh rẽ phân kỳ (multiple heads).
6. **File Test Dùng Chung (`conftest.py`, `factories.py`, shared mocks)**:
   - Chỉ được phép mở rộng: Khai báo fixture mới hoặc subclass factory mới.
   - TUYỆT ĐỐI CẤM sửa đổi giá trị trả về hoặc hành vi của fixture/factory hiện có đang phục vụ các test case trước (tránh gây flakey test hoặc gãy hàng loạt unit tests).
7. **File Đặc tả & Hợp đồng Kiến trúc (`docs/spec/`, API Schemas, OpenAPI)**:
   - Đóng băng Spec đối với Dev: Dev tuyệt đối không tự ý sửa file trong `docs/spec/` để "hợp thức hóa" code chạy khác spec.
   - Nếu phát hiện spec có điểm bất hợp lý hoặc thiếu sót: DỪNG LẠI, đánh dấu `BLOCKED`, yêu cầu Architect hoặc Lead thẩm định và cập nhật spec chính thức.

## Nhỏ
- [ ] Sửa trong nhánh riêng do người dùng tạo (`<type>/<ticket>-<mô-tả>`).
- [ ] Test và lint chạy qua (có thể nhờ `runner` chạy).
- [ ] `scripts/merge-gate.ps1` PASS (hoặc diff nằm trong phạm vi đã nêu).
- [ ] Kế hoạch commit trong `tasks/quick-log.md` hoặc card: mỗi commit một thay đổi logic, đúng `<type>(scope): <tóm tắt>`.
- [ ] Ghi chú cho agent sau trong `docs/notes/inbox/` (ngắn được, nhưng không bỏ qua).
- [ ] Người dùng đã xem diff và tự chạy các lệnh commit.

## Vừa
- [ ] Mọi mục của "Nhỏ".
- [ ] Task card đầy đủ: tiêu chí xong đạt hết, nhật ký phiên, file đã đổi, kết quả test, kế hoạch commit.
- [ ] Reviewer verdict (tư vấn) đạt yêu cầu (theo checklist trong `agents/roles/reviewer.md`).
- [ ] Người dùng duyệt phạm vi bằng file và nghiệm thu (theo `agents/protocols/approval.md`).
- [ ] QA xác nhận từng tiêu chí bằng test hoặc bước kiểm tra cụ thể.

## Lớn
- [ ] Mọi mục của "Vừa", cho từng task con.
- [ ] Yêu cầu R-xxx đều được thực hiện và đã được người dùng duyệt từ đầu.
- [ ] Nếu có tài liệu: Analyst đã đối chiếu tài liệu với code, báo cáo lệch trong `docs/analysis/` không còn mục "chặn việc".
- [ ] Nếu đổi xác thực, gói phụ thuộc hoặc dữ liệu nhạy cảm: Security duyệt.
- [ ] Nhánh đã **rebase** lên `develop`, tạo Merge Request đúng chính sách (tiêu đề, link ticket, tóm tắt, bằng chứng test, CI qua, đủ người duyệt).
- [ ] Sau khi merge: mã merge commit ghi vào card để hoàn tác được.
- [ ] Tech Writer cập nhật CHANGELOG và tài liệu, **gộp ghi chú từ `docs/notes/inbox/` vào `docs/PROJECT-NOTES.md`**.
- [ ] Release: tag `v<MAJOR>.<MINOR>.<PATCH>` trên `main` do người dùng đánh.

## Luôn luôn
- [ ] Đã xác định rõ Đầu vào (Input), Đầu ra (Output) và kịch bản Happy Path trước khi lập trình.
- [ ] Có Unit Test cho Happy Path được viết bằng công nghệ của dự án và chạy PASS (100% xanh).
- [ ] Không có khóa bí mật trong code, log, card, ghi chú.
- [ ] Việc đụng DB, dữ liệu thật hoặc deploy có "Kịch bản hoàn tác".
- [ ] Người làm sau đọc `docs/PROJECT-NOTES.md` trước khi bắt đầu.
