# Ví Dụ Mẫu: Tracer-Bullet Tickets & Expand-Contract Wide Refactor

Thư mục này minh họa kỹ thuật phân rã công việc chuẩn công nghiệp học hỏi từ `pocock-skills`:

## Các Khái Niệm Cốt Lõi
1. **Tracer-Bullet Vertical Slices**:
   - Khác với chia cắt theo tầng ngang (chỉ làm DB, chỉ làm API, chỉ làm UI khiến không cái nào demo được độc lập), mỗi ticket cắt dọc qua toàn bộ các lớp (schema, endpoint, giao diện, test).
   - Kích thước vừa vặn trong **1 Context Window duy nhất** của AI Agent.
2. **Blocking Edges (`blocked_by`)**:
   - Định nghĩa rõ ràng đồ thị có hướng không chu trình (DAG).
   - Agent luôn tìm và xử lý các ticket trên **Frontier** (các ticket mà toàn bộ blockers đã hoàn tất).
3. **Expand-Contract Pattern**:
   - Áp dụng khi thay đổi có **Blast Radius** cực lớn (đổi tên cột, retype ký hiệu chung) ảnh hưởng hàng chục/hàng trăm file.
   - Pha 1 (Expand): Tạo trường mới song song, giữ tương thích cũ.
   - Pha 2 (Migrate): Di chuyển từng cụm (batch) độc lập, mỗi batch 1 ticket.
   - Pha 3 (Contract): Xóa bỏ trường cũ khi số lượng call sites về 0.

## Kiểm Tra Đồ Thị & Frontier Tự Động
Chạy công cụ phân tích đồ thị:
```bash
node examples/tracer-bullet-tickets/validate-tickets.js examples/tracer-bullet-tickets
```
