# Chuyên Đề Next.js App Router, React Server Components (RSC) & Streaming SSR

**Loại: tham khảo.**
> **Phân vùng**: Frontend Architecture & Web Performance  
> **Phân quyền truy cập (RBAC)**: `["dev", "designer", "architect", "reviewer"]`  
> **Nguồn đối chuẩn**: Next.js Official Architecture Guide, React 19 Server Components RFC, Vercel Engineering  

---

## 1. Ranh Giới Server Components vs Client Components
- **React Server Components (RSC - Mặc định)**:
  - Chỉ thực thi trên máy chủ Node.js/Edge runtime, **không bao giờ gửi code JS về trình duyệt** ($0\text{KB}$ Bundle Size).
  - Được quyền truy cập trực tiếp hệ thống file, cơ sở dữ liệu nội bộ (Prisma, Drizzle, TypeORM), đọc biến môi trường bảo mật (`process.env.SECRET_API_KEY`).
  - Hạn chế: Không thể dùng State (`useState`), Effects (`useEffect`) hay Event Listeners (`onClick`).
- **Client Components (`'use client'`)**:
  - Biên dịch và gửi mã JS về trình duyệt để thực hiện tương tác UI (Hydration).
  - *Quy tắc vàng kiến trúc*: **Đẩy `'use client'` xuống sâu nhất trong cây component** (chỉ bọc các nút bấm, input, modal). Không bao giờ đặt `'use client'` ở cấp độ trang (`page.tsx`) hoặc layout chính.

---

## 2. Kỹ Thuật Streaming SSR Với `<Suspense>` & Skeleton Loading
- **Vấn đề**: SSR truyền thống chặn hiển thị toàn trang cho đến khi request chậm nhất hoàn tất (Time To First Byte - TTFB rất cao).
- **Streaming SSR**:
  - Trả về khung tĩnh (Header, Sidebar, Navigation) ngay sau $20\text{ms}$.
  - Bọc phần dữ liệu chậm (vd: danh sách đánh giá, biểu đồ phân tích) bằng thẻ `<Suspense fallback={<Skeleton />}>`.
  - Khi dữ liệu chậm nạp xong, server tự động truyền chunk HTML bổ sung qua luồng HTTP stream để trình duyệt hoán đổi Skeleton mà không cần nạp lại trang.

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';
import Header from '@/components/Header';
import MetricsOverview from '@/components/MetricsOverview';
import SlowTransactionList from '@/components/SlowTransactionList';
import { TableSkeleton } from '@/components/Skeletons';

export default async function DashboardPage() {
  return (
    <main className="p-6">
      {/* Khung chính render ngay lập tức */}
      <Header title="Bảng Điều Khiển Tài Chính" />
      <MetricsOverview />

      {/* Dữ liệu nặng được stream về sau */}
      <section className="mt-8">
        <h2 className="text-xl font-bold mb-4">Lịch Sử Giao Dịch Phức Tạp</h2>
        <Suspense fallback={<TableSkeleton />}>
          <SlowTransactionList />
        </Suspense>
      </section>
    </main>
  );
}
```

---

## 3. Bản Đồ 4 Tầng Caching Trong Next.js App Router

```
Request Đến
    │
    ▼
[1. Request Memoization] ──(Trùng URL trong 1 chu kỳ render?)──> Trả kết quả cùng chu kỳ
    │ (Miss)
    ▼
[2. Data Cache] ─────────(Dữ liệu fetch đã lưu trên Server?)──> Trả dữ liệu cache (Revalidate)
    │ (Miss)
    ▼
[3. Full Route Cache] ───(Trang tĩnh HTML + RSC payload?)──────> Trả HTML tĩnh tức thì
    │ (Miss)
    ▼
[Chạy Server Logic RSC & Gửi Trình Duyệt]
    │
    ▼
[4. Router Cache] ───────(Cache phiên trên trình duyệt)────────> Chuyển trang tức thì (0ms)
```

| Tầng Cache | Nơi lưu trữ | Mục đích | Cách vô hiệu hóa (Invalidation) |
|---|---|---|---|
| **Request Memoization** | Bộ nhớ Server (Per-request) | Tránh gọi trùng 1 API trong cùng cây component. | Tự động dọn sau mỗi request HTTP. |
| **Data Cache** | Ổ đĩa Server (Persistent) | Lưu trữ kết quả fetch qua nhiều người dùng. | `revalidatePath('/blog')`, `revalidateTag('products')`. |
| **Full Route Cache** | Ổ đĩa Server (Build time) | Cache toàn bộ trang tĩnh. | Cập nhật khi Data Cache thay đổi. |
| **Router Cache** | Bộ nhớ trình duyệt Client | Chuyển trang tức thì khi click `<Link>`. | `router.refresh()`, hết thời gian TTL phiên. |

