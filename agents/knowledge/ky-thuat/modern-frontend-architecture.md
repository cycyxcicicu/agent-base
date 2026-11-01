# Cẩm Nang Kiến Trúc Frontend Hiện Đại: Next.js App Router, TanStack Query & Zustand

**Loại: tham khảo.**
> **Phân vùng**: Frontend Engineering, UI State Management & Performance  
> **Phân quyền truy cập (RBAC)**: `["dev", "designer", "architect", "reviewer"]`  
> **Nguồn đối chuẩn**: Next.js Official Docs (App Router), React 19 RSC, TkDodo Blog (TanStack Query), Zustand Architecture  

---

## 1. Next.js App Router: React Server Components (RSC) & Client Components
- **Phân tách ranh giới Seam kiến trúc**:
  - **Server Components (Mặc định)**:
    - Chạy hoàn toàn trên máy chủ Node.js/Edge runtime.
    - Truy cập trực tiếp DB/ORM (Prisma, Drizzle) hoặc gọi API nội bộ mà không lộ credentials ra trình duyệt.
    - Không làm tăng kích thước Javascript Bundle tải về Client ($0\text{KB}$ JS bundle).
  - **Client Components (`'use client'`)**:
    - Chỉ dùng khi cần tương tác DOM, hooks React (`useState`, `useEffect`, `useReducer`), event listeners (`onClick`, `onChange`) hoặc Browser APIs (`localStorage`, `navigator`).
    - *Quy tắc thiết kế*: Đẩy ranh giới `'use client'` xuống thấp nhất có thể trong cây component (lá cây) để tối đa hóa phần tử server render.

```
+-------------------------------------------------------+
|  Page (Server Component - Lấy dữ liệu DB trực tiếp)    |
|   +-----------------------------------------------+   |
|   | Header (Server Component - HTML tĩnh)        |   |
|   +-----------------------------------------------+   |
|   | ProductList (Server Component - Async loop)   |   |
|   |   +-----------------------------------------+ |   |
|   |   | AddToCartButton ('use client' - Cần onClick) | |
|   |   +-----------------------------------------+ |   |
|   +-----------------------------------------------+   |
+-------------------------------------------------------+
```

---

## 2. Cơ Chế Streaming SSR & Suspense Boundaries
- **Vấn đề**: Truyền thống SSR bắt buộc phải chờ toàn bộ dữ liệu (cả phần nhanh lẫn phần chậm) nạp xong mới trả về HTML cho trình duyệt (Time to First Byte - TTFB chậm).
- **Giải pháp Streaming với `<Suspense>`**:
  - Server trả ngay khung trang chính (Navigation, Header, Layout) trong vài mili-giây đầu tiên.
  - Các khối dữ liệu nặng (vd: Đánh giá người dùng, Sản phẩm liên quan) được bọc trong `<Suspense fallback={<Skeleton />}>`.
  - Server truyền luồng HTML từng phần (HTTP Chunked Transfer Encoding) khi dữ liệu sẵn sàng và tự động thế chỗ Skeleton trên trình duyệt mà không cần tải lại trang.

```tsx
export default async function ProductPage({ params }: { params: { id: string } }) {
  return (
    <div className="container">
      {/* Khung chính trả về ngay lập tức */}
      <ProductDetails id={params.id} />
      
      {/* Phần tải chậm được stream về sau */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <ProductReviews productId={params.id} />
      </Suspense>
    </div>
  );
}
```

---

## 3. Quản Lý Vòng Đời 4 Tầng Caching Trong Next.js
1. **Request Memoization (React)**: Deduplicate các lệnh `fetch` cùng URL/params trong cùng 1 chu kỳ render component.
2. **Data Cache (Next.js Server)**: Lưu trữ kết quả fetch qua các request của nhiều người dùng khác nhau (`fetch(url, { next: { revalidate: 3600 } })`).
3. **Full Route Cache (Server Build/ISR)**: HTML và RSC payload được tạo sẵn tại thời điểm build và lưu cache tĩnh.
4. **Router Cache (Client-side)**: Cache phiên định tuyến trong bộ nhớ trình duyệt khi người dùng điều hướng qua lại giữa các trang.

---

## 4. TanStack Query v5: Xử Lý Mutation & Cập Nhật Lạc Quan (Optimistic Updates)
- **Triết lý**: Tách bạch tuyệt đối **Client State** (modal mở/đóng) và **Server State** (cache dữ liệu async).
- **Quy trình Optimistic Update chuẩn (Cập nhật trước - Rollback nếu lỗi)**:
  1. Hủy bỏ các truy vấn refetch đang chạy để tránh ghi đè state lạc quan (`cancelQueries`).
  2. Sao lưu ảnh chụp nhanh state hiện tại (`previousTodos`).
  3. Cập nhật state trong cache ngay lập tức để người dùng thấy giao diện phản hồi $0\text{ms}$.
  4. Nếu API gọi thất bại: Khôi phục lại đúng state đã sao lưu trong `onError`.
  5. Luôn làm mới dữ liệu từ server trong `onSettled` (`invalidateQueries`).

```typescript
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: updateTodoApi,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previousTodos = queryClient.getQueryData(['todos']);
    
    // Cập nhật lạc quan
    queryClient.setQueryData(['todos'], (old: Todo[] = []) => 
      old.map(t => t.id === newTodo.id ? { ...t, ...newTodo } : t)
    );
    return { previousTodos };
  },
  onError: (err, newTodo, context) => {
    // Rollback nếu API lỗi
    if (context?.previousTodos) {
      queryClient.setQueryData(['todos'], context.previousTodos);
    }
  },
  onSettled: () => {
    // Luôn đối soát lại với nguồn dữ liệu gốc
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

---

## 5. Zustand: Thiết Kế Slice Pattern & Transient Updates
- **Slice Pattern**: Chia nhỏ global store thành các lát cắt độc lập (UserSlice, CartSlice, UISlice) nhưng gộp chung vào 1 store duy nhất để dễ bảo trì.
- **Transient Updates (Tối ưu render)**:
  - Tránh `useStore(state => state)` làm re-render toàn component khi bất kỳ trường nào thay đổi.
  - Sử dụng selector chọn lọc `useStore(state => state.activeTab)` hoặc lắng nghe trực tiếp thông qua `useStore.subscribe()` đối với các tác vụ đồ họa/hoạt ảnh tần số cao (60fps).

