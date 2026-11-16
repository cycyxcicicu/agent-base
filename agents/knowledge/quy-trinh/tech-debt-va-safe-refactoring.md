# Quản Trị Nợ Kỹ Thuật & Tái Cấu Trúc An Toàn (Tech Debt & Safe Refactoring)

> **Loại: tham khảo.** Quy chuẩn theo dõi nợ kỹ thuật qua sổ DEBT.md và kỹ thuật refactor mã nguồn có bảo hiểm.
> Liên quan: `clean-code-and-refactoring-guide.md`, `gof-design-patterns-and-solid.md`.

## 1. Sổ Quản Trị Nợ Kỹ Thuật (`docs/governance/DEBT.md`)

Khi buộc phải đi đường tắt (shortcut) để kịp hotfix, kỹ sư bắt buộc phải ghi nhận vào Sổ Nợ:
- **Cú pháp comment trong code:**
  `// ponytail: <Lý do đi đường tắt> | debt-cost: <ước lượng giờ trả> | due: <Sprint>`
- **Bốn loại nợ kỹ thuật:**
  1. *Nợ Kiến trúc:* Vi phạm Ports & Adapters, lọt I/O vào Domain layer.
  2. *Nợ Mã nguồn:* Hàm dài > 45 dòng, lồng nhau > 3 tầng, biến magic string.
  3. *Nợ Kiểm thử:* Thiếu test ca lỗi, test assert giả tạo, Mutation score $< 80\%$.
  4. *Nợ Tài liệu:* SRS hoặc Swagger bị lệch so với code thực tế.
- **Quy tắc trả nợ:** Dành 15–20% dung lượng (capacity) của mỗi Sprint để trả nợ.

## 2. Chu Trình Tái Cấu Trúc An Toàn (Safe Refactoring Loop)

```
[Test Xanh (Green)] ──> [Tạo Checkpoint Git] ──> [Refactor từng bước nhỏ] ──> [Chạy Test Xanh] ──> [Commit]
```

- **Quy tắc bất di bất dịch:** CẤM refactor khi chưa có Unit test bao phủ đạt 100% các nhánh hiện tại.
- Refactor là thay đổi cấu trúc bên trong mã nguồn mà **không làm thay đổi hành vi bên ngoài**.

## 3. Kỹ Thuật Đưa Mã Nguồn Về Chuẩn Sạch (Clean Code Rules)

Cổng kiểm tra tự động `code-craft-check.py` chặn cứng các lỗi sau:
1. **Hàm dài quá 45 dòng:** Bắt buộc áp dụng *Extract Method* để tách nhỏ các bước logic tuần tự.
2. **Lồng nhau quá 3 tầng (`if-for-while`):**
   - *Áp dụng Early Return (Guard Clauses):* Kiểm tra điều kiện biên và thoát hàm ngay ở đầu, làm phẳng toàn bộ khối code chính.
3. **Chuỗi `if-else` hoặc `switch-case` $\ge 4$ nhánh:**
   - *Áp dụng Strategy Pattern / Factory:* Thay thế cấu trúc điều kiện bằng cách nạp danh sách Spring Bean implementing Interface chung.
4. **Trùng lặp logic (Duplicate Code):** Trừu tượng hóa thành hàm Generic `<T>` hoặc đưa vào thư viện dùng chung `ws-library`.
