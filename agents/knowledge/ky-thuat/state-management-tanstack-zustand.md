# Chuyên Đề Quản Lý Trạng Thái: TanStack Query v5 Optimistic Updates & Zustand Slices

**Loại: tham khảo.**
> **Phân vùng**: Frontend Architecture & State Engineering  
> **Phân quyền truy cập (RBAC)**: `["dev", "designer", "architect"]`  
> **Nguồn đối chuẩn**: TkDodo's Blog (TanStack Query Maintainer), Zustand Recipes (Poimandres), React 19 State Patterns  

---

## 1. Phân Tách Tuyệt Đối: Server State vs Client State
- **Sai lầm phổ biến**: Nhồi nhét dữ liệu từ API (danh sách sản phẩm, hồ sơ người dùng) vào các Global Store của Client (Redux, Zustand) rồi tự viết logic `loading`, `error`, `caching`, `polling`.
- **Nguyên tắc phân định chuẩn**:
  - **Server State (Dùng TanStack Query)**: Dữ liệu thuộc quyền sở hữu của máy chủ, cần đồng bộ qua mạng, có khả năng bị lỗi thời (Stale), cần deduplication, cache và refetch nền.
  - **Client State (Dùng Zustand / Context)**: Dữ liệu giao diện cục bộ thuần túy (Modal đang bật/tắt, giao diện Dark/Light mode, tab đang active, giỏ hàng tạm offline).

---

## 2. Kỹ Thuật Optimistic Updates (Cập Nhật Lạc Quan) & Tự Động Rollback
- **Mục tiêu**: Người dùng bấm nút "Like" hoặc "Thêm vào giỏ", giao diện phản hồi $0\text{ms}$ ngay lập tức, không có vòng xoay loading. Nếu máy chủ báo lỗi $500$, giao diện tự động hoàn tác (Rollback) về trạng thái cũ kèm thông báo lỗi.

```typescript
// useUpdateTodo.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface Todo {
  id: string;
  title: string;
  completed: boolean;
}

export function useUpdateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (updatedTodo: Todo) => {
      const res = await fetch(`/api/todos/${updatedTodo.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedTodo),
      });
      if (!res.ok) throw new Error('Cập nhật thất bại từ máy chủ!');
      return res.json();
    },

    // 1. Trước khi mutation chạy: Cập nhật lạc quan cache
    onMutate: async (newTodo) => {
      // Hủy bỏ các lệnh refetch ngầm đang chạy để tránh đè state mới
      await queryClient.cancelQueries({ queryKey: ['todos'] });

      // Lưu lại ảnh chụp nhanh (Snapshot) dữ liệu cũ
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);

      // Ép cập nhật cache ngay lập tức để UI render tức thì
      queryClient.setQueryData<Todo[]>(['todos'], (old = []) =>
        old.map((item) => (item.id === newTodo.id ? { ...item, ...newTodo } : item))
      );

      // Trả về context chứa snapshot cũ để dùng khi cần rollback
      return { previousTodos };
    },

    // 2. Nếu API bị lỗi: Rollback lại đúng trạng thái cũ
    onError: (err, newTodo, context) => {
      if (context?.previousTodos) {
        queryClient.setQueryData(['todos'], context.previousTodos);
      }
      alert('Không thể lưu dữ liệu: ' + err.message);
    },

    // 3. Luôn luôn đối soát lại với Server sau khi hoàn tất (dù thành công hay thất bại)
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
}
```

---

## 3. Zustand: Thiết Kế Slice Pattern & Tránh Re-render Thừa (Transient Updates)

```typescript
// store/useBoundStore.ts
import { create } from 'zustand';

// Định nghĩa từng Slice độc lập
interface UISlice {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
}

interface CartSlice {
  itemCount: number;
  addItem: () => void;
}

const createUISlice = (set: any): UISlice => ({
  isSidebarOpen: false,
  toggleSidebar: () => set((state: any) => ({ isSidebarOpen: !state.isSidebarOpen })),
});

const createCartSlice = (set: any): CartSlice => ({
  itemCount: 0,
  addItem: () => set((state: any) => ({ itemCount: state.itemCount + 1 })),
});

// Kết hợp thành Store duy nhất
export const useBoundStore = create<UISlice & CartSlice>()((...a) => ({
  ...createUISlice(...a),
  ...createCartSlice(...a),
}));

// TỐI ƯU RENDER: Chỉ re-render khi biến cần dùng thay đổi (Selector)
// Component này CHỈ re-render khi isSidebarOpen đổi, itemCount đổi nó KHÔNG render lại!
function SidebarToggle() {
  const isSidebarOpen = useBoundStore((state) => state.isSidebarOpen);
  const toggleSidebar = useBoundStore((state) => state.toggleSidebar);
  return <button onClick={toggleSidebar}>{isSidebarOpen ? 'Đóng' : 'Mở'}</button>;
}
```

