# Ghi chú cho agent sau (handoff note)

Sau khi xử lý xong việc của mình, **mỗi agent ghi lại những gì agent sau cần biết**. Task card ghi *việc này đã xong chưa*. Ghi chú này ghi *điều học được, bằng chứng kỹ thuật và điều cần cẩn thận* để người sau (và agent sau) không bị đâm vào cùng một chỗ.

---

## 1. Kiến trúc Lưu trữ 4 Tầng (Tiered Storage & Indexing Architecture)

Để tránh làm tràn cửa sổ ngữ cảnh (Context Window 200k–500k tokens) của Lead và giữ sạch khung chat chính, hệ thống áp dụng kiến trúc lưu trữ 4 tầng:

```
[Agent Con / Subagent]
       │
       ├── (1. Xả log & bằng chứng đầy đủ) ───► docs/notes/inbox/<Task>/<Task>.<Subtask>-<agent>.md
       │                                        (Tầng 1: Raw Execution Artifact)
       │
       └── (2. Gửi tóm tắt 3 dòng) ───────────► Khung chat của Lead / Tin nhắn trả về
                                                (Tầng 2: Micro Handoff Summary)
                                                       │
                                          [scripts/notes-index.py]
                                                       │
                                                       ▼
                                        docs/notes/INDEX.md
                                        (Tầng 3: Bảng chỉ mục tra cứu & lọc nhanh)
                                                       │
                                          [Sau khi Task hoàn thành]
                                                       ▼
                                        docs/notes/PROJECT-NOTES.md & docs/notes/archive/
                                        (Tầng 4: Sổ tay vĩnh viễn & Kho lưu trữ)
```

1. **Tầng 1: Báo cáo kỹ thuật chi tiết (Raw Execution Artifact)**:
   - Lưu tại: `docs/notes/inbox/<Task>/<Task>.<Subtask>-<agent>.md` (hoặc trực tiếp `docs/notes/inbox/<Task>-<slug>-<agent>.md`).
   - Chứa toàn bộ output test thực tế, lệnh kiểm chứng, diff chi tiết. Cấm in dữ liệu này ra khung chat của Lead.
2. **Tầng 2: Tóm tắt bàn giao siêu gọn (Micro Handoff Summary)**:
   - Lưu tại Frontmatter `summary:` của file note và gửi 3-5 dòng qua chat/tin nhắn cho Lead.
   - Lead chỉ nạp 3 dòng này vào ngữ cảnh làm việc.
3. **Tầng 3: Bảng chỉ mục tra cứu tự động (`docs/notes/INDEX.md`)**:
   - Sinh tự động bởi `python scripts/notes-index.py`. Quét toàn bộ hộp thư (kể cả thư mục con), hiển thị `Task | File Note | Role | Tags | Summary`.
   - Cung cấp các cờ lọc CLI: `--task`, `--role`, `--tag`, `--query`, `--json` để tra cứu tức thì mà không cần mở từng file.
4. **Tầng 4: Sổ tay tri thức vĩnh viễn & Kho lưu trữ (`docs/notes/PROJECT-NOTES.md` & `archive/`)**:
   - Sau khi task hoàn thành: Tech Writer gộp tri thức cốt lõi (bẫy lỗi, quy ước) vào `docs/PROJECT-NOTES.md`.
   - Chuyển file note chi tiết sang `docs/notes/archive/<Task>/` để làm sạch `inbox/`.

---

## 2. Chuẩn Frontmatter cho Note

Mỗi file note khuyến nghị sử dụng khối YAML frontmatter đầy đủ ở đầu file (hoặc tối thiểu dòng `> summary:`):

```yaml
---
task: T-12.1
role: dev
status: done
tags: [auth, token, guard-check]
summary: Chuẩn hóa hàm normalize_payload, 46/46 test OK
---
```

---

## 3. Mẫu 1: Ghi chú Task chính (Standard Handoff Note)
Áp dụng khi một vai trò hoàn thành hoặc tạm dừng phiên của một Task card lớn (`docs/notes/inbox/<Task>-<slug>-<agent>.md`, ví dụ `T-12-dev.md`).

```markdown
---
task: T-12
role: dev-a
status: done
tags: [core, api]
summary: Hoàn thành refactor module auth, toàn bộ unit tests pass
---

Task: T-12        Agent: dev-a        Ngày: YYYY-MM-DD

## Đã làm
(1–3 dòng)

## Lưu ý cho agent sau
(chỉ khi có điều agent sau cần biết. Nếu không có, bỏ qua cả ghi chú)
- Bẫy hoặc hành vi bất ngờ: (ví dụ: hàm X trả về null khi ..., cần kiểm tra trước khi dùng)
- Quyết định đã đưa ra và lý do:
- File hoặc khu vực dễ vỡ, cần cẩn thận: (đường dẫn cụ thể)
- Giả định chưa kiểm chứng:

## Việc dở dang hoặc nợ kỹ thuật
(việc chưa làm, làm tạm, cần làm lại)

## Ảnh hưởng đến task khác
(T-xxx nào cần biết, và cần biết gì)

## Đề xuất cập nhật quy ước hoặc tài liệu
(nếu phát hiện quy ước nên thêm vào `agents/stacks/` hoặc `PROJECT.md`)

## Thay đổi dùng chung cho agent-base
(bắt buộc nếu đã sửa file khung trong `agents/manifest.txt`: script, protocol, vai, mẫu. Ghi: file, sửa gì, vì sao, dùng chung được không. Không sửa thì ghi "không có". Xem `agents/protocols/agent-base-sync.md`)
```

---

## 4. Mẫu 2: Ghi chú Subtask siêu gọn (Micro Subtask Handoff Note - AGENTS.md §16)
Áp dụng cho từng **Subagent** sau khi hoàn thành 1 Subtask hạt mịn (một mục đích, vừa một phiên ngắn khoảng 2–5 phút).
- **Quy tắc đặt tên file**: Gom gọn vào thư mục mang tên Task `docs/notes/inbox/<Task>/<Task>.<Subtask>-<agent>.md` (ví dụ: `docs/notes/inbox/T-57/T-57.1-dev.md`, `docs/notes/inbox/T-57/T-57.2-dba.md`) giúp quản lý lâu dài không bị lẫn lộn giữa các task.
- **Mẫu (3–5 dòng, tối ưu token, không viết dài dòng)**:

```markdown
---
task: T-57.1
role: dev
status: done
tags: [db, migration]
summary: Tạo bảng auth_audit_log và index cho trường created_at
---

# Subtask: T-57.1 - Tạo migration cho audit log
- **Mục đích**: Lưu vết truy cập nhạy cảm theo chuẩn SOC2
- **Đã làm**: Viết script migration Liquibase/Flyway, thêm index
- **Files đã sửa**: `src/main/resources/db/changelog/001-audit.sql`
- **Kết quả test**: `alembic upgrade head PASS` hoặc `./mvnw compile test PASS`
- **Bàn giao cho Subtask kế tiếp**: Subtask T-57.2 có thể bắt đầu viết Entity JPA map với bảng này
```

---

## 5. Quy tắc viết

- **Giới hạn độ dài**: Mỗi note phải **≤ 80 dòng**. Ghi sự thật + quyết định + đường dẫn cụ thể, không chép lại tài liệu.
- Viết cho người **chưa biết ngữ cảnh**: nêu đường dẫn cụ thể, không viết "như đã nói".
- Ngắn, mỗi ý một dòng. Điều đáng ghi là điều **không thể suy ra từ code hay git log**.
- Không ghi khóa bí mật, mật khẩu, token, dữ liệu cá nhân.
- Không ghi điều đã có trong code hoặc trong task card.
- Điều chưa chắc thì gắn nhãn "chưa xác minh".
- Ghi lại cả những hướng đã thử mà **không** chạy, để người sau khỏi thử lại.
