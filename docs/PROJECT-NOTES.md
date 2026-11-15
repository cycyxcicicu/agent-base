# Sổ tay dự án (PROJECT-NOTES)

Bộ nhớ chung của dự án cho mọi agent. **Đọc file này (và `docs/notes/inbox/`) trước khi bắt đầu việc.**

- Chỉ **Tech Writer** sửa file này, bằng cách gộp các ghi chú từ `docs/notes/inbox/` sau mỗi lần merge (xem `agents/protocols/handoff-note.md`).
- Mỗi mục có ID (N-001, N-002...), ngày, nguồn (T-xxx và agent), và **phạm vi ảnh hưởng** (file hoặc module).
- Mục hết đúng thì gạch bỏ và ghi lý do, đừng xóa im lặng.

## Trạng thái hiện tại

(một đoạn ngắn: dự án đang ở đâu, task nào đang chạy, điều gì đang chặn. Cập nhật sau mỗi merge)

## Lưu ý và bẫy đã gặp

| ID | Ngày | Nguồn | Phạm vi | Lưu ý |
|---|---|---|---|---|
| N-367 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-368 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-369 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-370 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-371 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-372 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-373 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-374 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-375 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-350 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-351 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-352 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-353 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-354 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-355 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-356 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-357 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-358 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-333 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-334 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-335 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-336 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-337 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-338 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-339 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-340 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-341 | 2026-11-15 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-316 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-317 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-318 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-319 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-320 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-321 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-322 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-323 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-324 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-299 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-300 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-301 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-302 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-303 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-304 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-305 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-306 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-307 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-282 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-283 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-284 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-285 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-286 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-287 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-288 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-289 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-290 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-265 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-266 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-267 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-268 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-269 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-270 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-271 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-272 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-273 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-248 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-249 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-250 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-251 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-252 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-253 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-254 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-255 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-256 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-231 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-232 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-233 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-234 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-235 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-236 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-237 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-238 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-239 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-214 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-215 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-216 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-217 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-218 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-219 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-220 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-221 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-222 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-197 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-198 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-199 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-200 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-201 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-202 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-203 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-204 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-205 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-180 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-181 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-182 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-183 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-184 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-185 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-186 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-187 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-188 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-163 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-164 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-165 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-166 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-167 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-168 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-169 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-170 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-171 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-129 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-130 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-131 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-132 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-133 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-134 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-135 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-136 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-137 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-146 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-147 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-148 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-149 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-150 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-151 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-152 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-153 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-154 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-095 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-096 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-097 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-098 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-099 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-100 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-101 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-102 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-103 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-112 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-113 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-114 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-115 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-116 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-117 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-118 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-119 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-120 | 2026-11-14 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-092 | 2026-11-13 | `LEARN` | Toàn cục | Agent tu review code cua chinh minh se bi confirmation bias; Leaf Code khong co Feature Flag gay nguy co rollback khong kip khi su co. |
| N-093 | 2026-11-13 | `LEARN` | Toàn cục | [Bài học] Phan loai ro Trunk Code (soi ky tung dong) vs Leaf Code (Feature Gated doc luot). Ap dung Adversarial Reviewer zero-context va tach bach Merge-Ready 80% vs Launch-Ready 20%. |
| N-089 | 2026-11-13 | `LEARN` | Toàn cục | Agent làm việc thụ động, chỉ sửa code xong dừng lại khiến bài học bị trôi mất theo context; hoặc lạm dụng tìm kiếm diện rộng làm kéo dài thời gian sửa lỗi nhỏ lên gần 1 giờ. |
| N-090 | 2026-11-13 | `LEARN` | Toàn cục | [Bài học] Quy chuẩn hoá tự động hoá học hỏi: Agent bắt buộc tự kích hoạt ghi nhận bài học qua knowledge.py learn và harness-reflect sau mỗi lần sửa bug hoặc khi nhận uốn nắn từ người dùng, không chờ người dùng nhắc. |
| N-049 | 2026-11-09 | `LEARN` | Toàn cục | 1. Antigravity IDE đọc ~/.gemini/GEMINI.md làm user_global có độ ưu tiên cao nhất đè lên mọi file; nếu thiếu luật ở đây thì model vẫn chạy grep. 2. Worktree mới tạo nếu thiếu GEMINI.md sẽ mất ngữ cảnh Antigravity. 3. MCP AST (xerj) chỉ tìm được symbol/hàm/lớp, không tìm được chuỗi text tự do trong JSX/i18n, khiến Agent tự chế python script làm grep-proxy. |
| N-050 | 2026-11-09 | `LEARN` | Toàn cục | [Bài học] Giải quyết triệt để lỗi Agent dùng grep trên toàn bộ nền tảng Antigravity IDE, Claude Code và các Git Worktrees. |
| N-052 | 2026-11-10 | `LEARN` | Toàn cục | Cần lưu ý khi triển khai Mở khóa Git Claude Code 2 tầng & Bẫy XERJ prefix ax-* để tránh tái diễn lỗi trong các phiên làm việc tiếp theo. |
| N-053 | 2026-11-10 | `LEARN` | Toàn cục | [Bài học] Claude Code chuẩn hóa khoảng trắng/ngoặc ở subcommandResults nên các rule deny git không gắn verb (git\t*, git  *, "git" *, & git*) suy biến thành git * và chặn sạch mọi lệnh git; giữ mẫu có verb ở .claude/settings.json + ~/.claude/settings.json và đẩy bắt mẹo lách sang scripts/security-hook.py. Khi tra MCP xerj_def/xerj_search luôn truyền prefix dự án (gdt, agentbase, tiktok) vì mặc định ax-* trả 0 hits; safe-search.py (limit 10/max 20) chỉ dùng cho text thuần/i18n/UI. |
| N-055 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-056 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-057 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-058 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-059 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-060 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-061 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-062 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-063 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-009 | 2026-11-05 | `LEARN` | Toàn cục | Xử lý đồng bộ ngay trong Webhook controller làm cạn connection pool; không so sánh timestamp eventTime dẫn đến event cũ đè event mới; không cấu hình Manual ACK làm mất đơn khi worker chết giữa chừng. |
| N-010 | 2026-11-05 | `LEARN` | Toàn cục | [Bài học] Mô hình tích hợp đối tác qua Webhook + RabbitMQ + Worker (ShopSyncConsumer): Fast-Path Direct Update qua Pessimistic Lock, Slow-Path Refetch API, Self-Healing Token Refresh (401), Overlap Window 15 phút chống rớt đơn và Dead-Letter Queue (DLQ). |
| N-012 | 2026-11-06 | `LEARN` | Toàn cục | Dùng fixed worker gây cạn DB pool; không tách luồng backfill làm nghẽn real-time; gom đa sàn vào 1 bảng làm phình schema; không mã hóa token at-rest. |
| N-013 | 2026-11-06 | `LEARN` | Toàn cục | [Bài học] Tổng hợp 10 kỹ thuật tinh hoa từ tiktok_shoppe_jt: (1) Worker Auto-Scaler dựa trên HikariCP; (2) Deadlock Watchdog daemon; (3) Phân loại lỗi và Self-healing; (4) Tách luồng Backfill khỏi Real-time; (5) Dynamic OAuth Credential Resolver; (6) Cổng vận đơn J&T/Pancake; (7) Physical Table + Logical View; (8) Mã hóa AES DB at-rest; (9) RabbitMQ Priority & Deduplication; (10) Fuzzy Header Excel Mapping. |
| N-003 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Bẫy tọa độ 2D của LLM: Tuyệt đối không để AI tính toán tọa độ x, y, width, height để sinh XML Draw.io thô vì tỷ lệ lệch dây nối và đè chữ lên tới 85%. Bắt buộc dùng Auto-Layout (CSV Import, D2, Mermaid, Diagrams Python). |
| N-004 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Tránh ô nhiễm bộ khung: Không commit dữ liệu runtime của dự án ngoài (inbox notes, task board, proposals) lên repo framework agent-base; bắt buộc duy trì vành đai cách ly trong .gitignore. |

## Quyết định quan trọng

(tóm tắt một dòng kèm liên kết tới ADR trong `docs/adr/`)

| ID | Ngày | Quyết định | ADR |
|---|---|---|---|
| N-376 | 2026-11-15 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-377 | 2026-11-15 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-378 | 2026-11-15 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-379 | 2026-11-15 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-359 | 2026-11-15 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-360 | 2026-11-15 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-361 | 2026-11-15 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-362 | 2026-11-15 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-342 | 2026-11-15 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-343 | 2026-11-15 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-344 | 2026-11-15 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-345 | 2026-11-15 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-325 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-326 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-327 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-328 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-308 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-309 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-310 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-311 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-291 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-292 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-293 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-294 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-274 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-275 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-276 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-277 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-257 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-258 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-259 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-260 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-240 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-241 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-242 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-243 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-223 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-224 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-225 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-226 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-206 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-207 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-208 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-209 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-189 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-190 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-191 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-192 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-172 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-173 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-174 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-175 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-138 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-139 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-140 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-141 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-155 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-156 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-157 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-158 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-104 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-105 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-106 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-107 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-121 | 2026-11-14 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-122 | 2026-11-14 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-123 | 2026-11-14 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-124 | 2026-11-14 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-094 | 2026-11-13 | Cap nhat AGENTS.md, reviewer.md, merge-gate.py va tao launch-gate.py kiem toan traffic truoc Production. | Theo `LEARN` |
| N-091 | 2026-11-13 | Thiết lập cơ chế Tự Trị Học Hỏi (Autonomous Self-Learning Gate): Tự kích hoạt chu trình learn + harness-reflect sau mỗi lần pass test hoặc nhận phản hồi; đồng thời áp trần Fast-Path <= 5 phút, Search Ceiling = 1 call, Single-Anchor >= 8 ký tự, Anti-cascade read <= 50 dòng. | Theo `LEARN` |
| N-051 | 2026-11-09 | 1. Cài đặt Hard Shim exit code 2 tại ~/.gemini/antigravity/bin/grep và find. 2. scripts/worktree-manager.py tự động symlink GEMINI.md và CLAUDE.md sang 100% worktree. 3. Phân định rõ ràng: Tra cứu symbol dùng MCP xerj/graphify; đọc file đã biết dùng read_file; tìm chuỗi text thuần phải dùng công cụ giới hạn dòng an toàn, cấm quét thô. | Theo `LEARN` |
| N-054 | 2026-11-10 | Chuẩn hóa giải pháp kỹ thuật theo đề xuất và bài học từ vai trò architect. | Theo `LEARN` |
| N-064 | 2026-11-13 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-065 | 2026-11-13 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-066 | 2026-11-13 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-067 | 2026-11-13 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-081 | 2026-11-13 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-082 | 2026-11-13 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-083 | 2026-11-13 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-084 | 2026-11-13 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-041 | 2026-11-07 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-042 | 2026-11-07 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-043 | 2026-11-07 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-044 | 2026-11-07 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-024 | 2026-11-07 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-025 | 2026-11-07 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-026 | 2026-11-07 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-027 | 2026-11-07 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-011 | 2026-11-05 | Áp dụng Sync-then-Serve: Webhook xác thực HMAC đẩy queue trả 200 OK ngay; Worker prefetch=1 manual ACK; findForUpdate chống race condition; Overlap 15 phút cronjob quét bù. | Theo `LEARN` |
| N-014 | 2026-11-06 | Áp dụng trọn bộ 10 patterns trong docs/architecture/10-CHUYEN-DE-KIEN-TRUC-CHUYEN-SAU.md làm blueprint cho các dự án kết nối bên thứ 3. | Theo `LEARN` |
| N-005 | 2026-10-28 | Quyết định chuẩn hóa sơ đồ kiến trúc Draw.io thông qua định dạng CSV Auto-Layout (Header # style, # connect, # layout: auto) và Python diagrams thay vì viết XML mxGraphModel trực tiếp. | Theo `KNOWLEDGE-DIAGRAMS-EPIC` |
| N-006 | 2026-10-28 | Quyết định phân tách tri thức: Giữ nguyên doc/ và .ai-rules/ ở gốc workspace làm la bàn chung; agent-base chỉ sao phần dùng chung được (quy trình, chuẩn, mẫu) vào agents/knowledge và agents/templates, dữ liệu dự án ở lại bên ngoài. | Theo `KNOWLEDGE-DIAGRAMS-EPIC` |

## Quy ước phát hiện thêm

- **[N-380 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-381 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-382 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-383 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-363 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-364 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-365 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-366 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-346 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-347 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-348 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-349 - 2026-11-15]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-329 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-330 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-331 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-332 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-312 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-313 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-314 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-315 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-295 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-296 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-297 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-298 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-278 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-279 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-280 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-281 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-261 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-262 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-263 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-264 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-244 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-245 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-246 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-247 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-227 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-228 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-229 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-230 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-210 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-211 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-212 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-213 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-193 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-194 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-195 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-196 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-176 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-177 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-178 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-179 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-142 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-143 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-144 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-145 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.
- **[N-159 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-160 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-161 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-162 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-108 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-109 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-110 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-111 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.
- **[N-125 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-126 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-127 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-128 - 2026-11-14]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-068 - 2026-11-13]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-069 - 2026-11-13]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-070 - 2026-11-13]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-071 - 2026-11-13]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.
- **[N-085 - 2026-11-13]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-086 - 2026-11-13]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-087 - 2026-11-13]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-088 - 2026-11-13]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-045 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-046 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-047 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-048 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-028 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-029 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-030 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-031 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-007 - 2026-10-28]** (`KNOWLEDGE-DIAGRAMS-EPIC`): Khi người dùng cần sơ đồ kiến trúc có thể chỉnh sửa tay trên Draw.io, Agent ưu tiên xuất khối mã CSV kèm hướng dẫn 4 bước Insert CSV vào diagrams.net.
- **[N-008 - 2026-10-28]** (`KNOWLEDGE-DIAGRAMS-EPIC`): Mọi node tri thức mới sinh ra từ chu trình phản tư luôn mang trạng thái state: draft và phải qua 11 Validators CMMI L3 trước khi con người nghiệm thu.

(điều chưa có trong `agents/stacks/` hay `PROJECT.md`. Khi đã ổn định thì đề xuất đưa vào các file đó và ghi ở đây là đã chuyển)

## Việc dở dang và nợ kỹ thuật

| ID | Ngày | Nguồn | Mô tả | Ưu tiên |
|---|---|---|---|---|
| N-092 | 2026-11-13 | `LEARN` | Toàn cục | Agent tu review code cua chinh minh se bi confirmation bias; Leaf Code khong co Feature Flag gay nguy co rollback khong kip khi su co. |
| N-093 | 2026-11-13 | `LEARN` | Toàn cục | [Bài học] Phan loai ro Trunk Code (soi ky tung dong) vs Leaf Code (Feature Gated doc luot). Ap dung Adversarial Reviewer zero-context va tach bach Merge-Ready 80% vs Launch-Ready 20%. |
| N-089 | 2026-11-13 | `LEARN` | Toàn cục | Agent làm việc thụ động, chỉ sửa code xong dừng lại khiến bài học bị trôi mất theo context; hoặc lạm dụng tìm kiếm diện rộng làm kéo dài thời gian sửa lỗi nhỏ lên gần 1 giờ. |
| N-090 | 2026-11-13 | `LEARN` | Toàn cục | [Bài học] Quy chuẩn hoá tự động hoá học hỏi: Agent bắt buộc tự kích hoạt ghi nhận bài học qua knowledge.py learn và harness-reflect sau mỗi lần sửa bug hoặc khi nhận uốn nắn từ người dùng, không chờ người dùng nhắc. |
| N-049 | 2026-11-09 | `LEARN` | Toàn cục | 1. Antigravity IDE đọc ~/.gemini/GEMINI.md làm user_global có độ ưu tiên cao nhất đè lên mọi file; nếu thiếu luật ở đây thì model vẫn chạy grep. 2. Worktree mới tạo nếu thiếu GEMINI.md sẽ mất ngữ cảnh Antigravity. 3. MCP AST (xerj) chỉ tìm được symbol/hàm/lớp, không tìm được chuỗi text tự do trong JSX/i18n, khiến Agent tự chế python script làm grep-proxy. |
| N-050 | 2026-11-09 | `LEARN` | Toàn cục | [Bài học] Giải quyết triệt để lỗi Agent dùng grep trên toàn bộ nền tảng Antigravity IDE, Claude Code và các Git Worktrees. |
| N-052 | 2026-11-10 | `LEARN` | Toàn cục | Cần lưu ý khi triển khai Mở khóa Git Claude Code 2 tầng & Bẫy XERJ prefix ax-* để tránh tái diễn lỗi trong các phiên làm việc tiếp theo. |
| N-053 | 2026-11-10 | `LEARN` | Toàn cục | [Bài học] Claude Code chuẩn hóa khoảng trắng/ngoặc ở subcommandResults nên các rule deny git không gắn verb (git\t*, git  *, "git" *, & git*) suy biến thành git * và chặn sạch mọi lệnh git; giữ mẫu có verb ở .claude/settings.json + ~/.claude/settings.json và đẩy bắt mẹo lách sang scripts/security-hook.py. Khi tra MCP xerj_def/xerj_search luôn truyền prefix dự án (gdt, agentbase, tiktok) vì mặc định ax-* trả 0 hits; safe-search.py (limit 10/max 20) chỉ dùng cho text thuần/i18n/UI. |
| N-055 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-056 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-057 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-058 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-059 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-060 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-061 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-062 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-063 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-009 | 2026-11-05 | `LEARN` | Toàn cục | Xử lý đồng bộ ngay trong Webhook controller làm cạn connection pool; không so sánh timestamp eventTime dẫn đến event cũ đè event mới; không cấu hình Manual ACK làm mất đơn khi worker chết giữa chừng. |
| N-010 | 2026-11-05 | `LEARN` | Toàn cục | [Bài học] Mô hình tích hợp đối tác qua Webhook + RabbitMQ + Worker (ShopSyncConsumer): Fast-Path Direct Update qua Pessimistic Lock, Slow-Path Refetch API, Self-Healing Token Refresh (401), Overlap Window 15 phút chống rớt đơn và Dead-Letter Queue (DLQ). |
| N-012 | 2026-11-06 | `LEARN` | Toàn cục | Dùng fixed worker gây cạn DB pool; không tách luồng backfill làm nghẽn real-time; gom đa sàn vào 1 bảng làm phình schema; không mã hóa token at-rest. |
| N-013 | 2026-11-06 | `LEARN` | Toàn cục | [Bài học] Tổng hợp 10 kỹ thuật tinh hoa từ tiktok_shoppe_jt: (1) Worker Auto-Scaler dựa trên HikariCP; (2) Deadlock Watchdog daemon; (3) Phân loại lỗi và Self-healing; (4) Tách luồng Backfill khỏi Real-time; (5) Dynamic OAuth Credential Resolver; (6) Cổng vận đơn J&T/Pancake; (7) Physical Table + Logical View; (8) Mã hóa AES DB at-rest; (9) RabbitMQ Priority & Deduplication; (10) Fuzzy Header Excel Mapping. |
| N-003 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Bẫy tọa độ 2D của LLM: Tuyệt đối không để AI tính toán tọa độ x, y, width, height để sinh XML Draw.io thô vì tỷ lệ lệch dây nối và đè chữ lên tới 85%. Bắt buộc dùng Auto-Layout (CSV Import, D2, Mermaid, Diagrams Python). |
| N-004 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Tránh ô nhiễm bộ khung: Không commit dữ liệu runtime của dự án ngoài (inbox notes, task board, proposals) lên repo framework agent-base; bắt buộc duy trì vành đai cách ly trong .gitignore. |

## Giả định chưa kiểm chứng

| ID | Ngày | Nguồn | Giả định | Cách kiểm chứng |
|---|---|---|---|---|
| N-092 | 2026-11-13 | `LEARN` | Toàn cục | Agent tu review code cua chinh minh se bi confirmation bias; Leaf Code khong co Feature Flag gay nguy co rollback khong kip khi su co. |
| N-093 | 2026-11-13 | `LEARN` | Toàn cục | [Bài học] Phan loai ro Trunk Code (soi ky tung dong) vs Leaf Code (Feature Gated doc luot). Ap dung Adversarial Reviewer zero-context va tach bach Merge-Ready 80% vs Launch-Ready 20%. |
| N-089 | 2026-11-13 | `LEARN` | Toàn cục | Agent làm việc thụ động, chỉ sửa code xong dừng lại khiến bài học bị trôi mất theo context; hoặc lạm dụng tìm kiếm diện rộng làm kéo dài thời gian sửa lỗi nhỏ lên gần 1 giờ. |
| N-090 | 2026-11-13 | `LEARN` | Toàn cục | [Bài học] Quy chuẩn hoá tự động hoá học hỏi: Agent bắt buộc tự kích hoạt ghi nhận bài học qua knowledge.py learn và harness-reflect sau mỗi lần sửa bug hoặc khi nhận uốn nắn từ người dùng, không chờ người dùng nhắc. |
| N-049 | 2026-11-09 | `LEARN` | Toàn cục | 1. Antigravity IDE đọc ~/.gemini/GEMINI.md làm user_global có độ ưu tiên cao nhất đè lên mọi file; nếu thiếu luật ở đây thì model vẫn chạy grep. 2. Worktree mới tạo nếu thiếu GEMINI.md sẽ mất ngữ cảnh Antigravity. 3. MCP AST (xerj) chỉ tìm được symbol/hàm/lớp, không tìm được chuỗi text tự do trong JSX/i18n, khiến Agent tự chế python script làm grep-proxy. |
| N-050 | 2026-11-09 | `LEARN` | Toàn cục | [Bài học] Giải quyết triệt để lỗi Agent dùng grep trên toàn bộ nền tảng Antigravity IDE, Claude Code và các Git Worktrees. |
| N-052 | 2026-11-10 | `LEARN` | Toàn cục | Cần lưu ý khi triển khai Mở khóa Git Claude Code 2 tầng & Bẫy XERJ prefix ax-* để tránh tái diễn lỗi trong các phiên làm việc tiếp theo. |
| N-053 | 2026-11-10 | `LEARN` | Toàn cục | [Bài học] Claude Code chuẩn hóa khoảng trắng/ngoặc ở subcommandResults nên các rule deny git không gắn verb (git\t*, git  *, "git" *, & git*) suy biến thành git * và chặn sạch mọi lệnh git; giữ mẫu có verb ở .claude/settings.json + ~/.claude/settings.json và đẩy bắt mẹo lách sang scripts/security-hook.py. Khi tra MCP xerj_def/xerj_search luôn truyền prefix dự án (gdt, agentbase, tiktok) vì mặc định ax-* trả 0 hits; safe-search.py (limit 10/max 20) chỉ dùng cho text thuần/i18n/UI. |
| N-055 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-056 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-057 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-058 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-059 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-060 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-061 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-062 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-063 | 2026-11-13 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-009 | 2026-11-05 | `LEARN` | Toàn cục | Xử lý đồng bộ ngay trong Webhook controller làm cạn connection pool; không so sánh timestamp eventTime dẫn đến event cũ đè event mới; không cấu hình Manual ACK làm mất đơn khi worker chết giữa chừng. |
| N-010 | 2026-11-05 | `LEARN` | Toàn cục | [Bài học] Mô hình tích hợp đối tác qua Webhook + RabbitMQ + Worker (ShopSyncConsumer): Fast-Path Direct Update qua Pessimistic Lock, Slow-Path Refetch API, Self-Healing Token Refresh (401), Overlap Window 15 phút chống rớt đơn và Dead-Letter Queue (DLQ). |
| N-012 | 2026-11-06 | `LEARN` | Toàn cục | Dùng fixed worker gây cạn DB pool; không tách luồng backfill làm nghẽn real-time; gom đa sàn vào 1 bảng làm phình schema; không mã hóa token at-rest. |
| N-013 | 2026-11-06 | `LEARN` | Toàn cục | [Bài học] Tổng hợp 10 kỹ thuật tinh hoa từ tiktok_shoppe_jt: (1) Worker Auto-Scaler dựa trên HikariCP; (2) Deadlock Watchdog daemon; (3) Phân loại lỗi và Self-healing; (4) Tách luồng Backfill khỏi Real-time; (5) Dynamic OAuth Credential Resolver; (6) Cổng vận đơn J&T/Pancake; (7) Physical Table + Logical View; (8) Mã hóa AES DB at-rest; (9) RabbitMQ Priority & Deduplication; (10) Fuzzy Header Excel Mapping. |
| N-003 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Bẫy tọa độ 2D của LLM: Tuyệt đối không để AI tính toán tọa độ x, y, width, height để sinh XML Draw.io thô vì tỷ lệ lệch dây nối và đè chữ lên tới 85%. Bắt buộc dùng Auto-Layout (CSV Import, D2, Mermaid, Diagrams Python). |
| N-004 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Tránh ô nhiễm bộ khung: Không commit dữ liệu runtime của dự án ngoài (inbox notes, task board, proposals) lên repo framework agent-base; bắt buộc duy trì vành đai cách ly trong .gitignore. |

## Câu hỏi còn mở cho người dùng

| ID | Ngày | Câu hỏi | Trạng thái |
|---|---|---|---|
