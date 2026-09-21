# Frontend Architecture & Design Patterns (Cẩm Nang Thiết Kế & Lập Trình Frontend)

Tài liệu này chuẩn hóa các nguyên tắc kiến trúc, quy chuẩn mã nguồn, mô hình thiết kế (Design Patterns) và quy tắc sửa đổi mã (Token-efficient diffs) cho ứng dụng Frontend hiện đại (React, Next.js App Router, Vue, Svelte), chắt lọc từ các kỹ thuật thực chiến (Onlook, Headless UI, Atomic Design).

---

## 1. Ranh Giới Server & Client (Client / Server Boundary)

Trong các framework hiện đại (đặc biệt là Next.js App Router / React Server Components - RSC):

### 1.1. Mặc định là Server Component
- **Nguyên tắc**: Luôn giữ component ở Server theo mặc định (`RSC`).
- **Lợi ích**: Giảm kích thước JS bundle tải xuống client, truy cập DB/dịch vụ nội bộ trực tiếp, bảo mật bí mật (API keys, secrets), tăng tốc First Contentful Paint (FCP).

### 1.2. Khi nào dùng `'use client'`?
Chỉ thêm chỉ thị `'use client'` ở **tầng lá (leaf components)** khi component thực sự cần:
1. Lắng nghe sự kiện người dùng (`onClick`, `onChange`, `onSubmit`, `onKeyDown`).
2. Sử dụng React Hooks quản lý trạng thái hoặc vòng đời (`useState`, `useEffect`, `useReducer`, `useRef`).
3. Truy cập Web API của trình duyệt (`window`, `localStorage`, `navigator`, `document`).
4. Sử dụng các thư viện client-only (như animation framer-motion, observer stores).

### 1.3. Quy tắc "Bình Chứa Tầng Lá" (Don't Poison the Tree)
- Không bao giờ đặt `'use client'` ở các layout cấp cao hoặc trang gốc nếu chỉ có một nút bấm cần tương tác.
- Tách nhỏ nút bấm hoặc widget tương tác thành một client component riêng, rồi truyền vào server component dưới dạng `children` hoặc props.

```tsx
// ❌ SAI: Biến toàn bộ trang Dashboard thành Client Component
'use client';
export default function DashboardPage() {
  const [filter, setFilter] = useState('');
  return <div><HeavyDataChart /><FilterInput value={filter} onChange={setFilter} /></div>;
}

// ✅ ĐÚNG: Giữ trang làm Server Component, chỉ Client hóa component tương tác
// FilterWidget.tsx
'use client';
export function FilterWidget() { ... }

// page.tsx (Server Component)
export default async function DashboardPage() {
  const data = await getDashboardData(); // chạy an toàn trên server
  return (
    <div>
      <FilterWidget />
      <HeavyDataChart data={data} />
    </div>
  );
}
```

### 1.4. Bảo vệ Biến Môi Trường (Env Validation)
- Tuyệt đối không đọc trực tiếp biến môi trường nhạy cảm trên client.
- Chỉ các biến có tiền tố công khai (như `NEXT_PUBLIC_*` hoặc `VITE_*`) mới được phép ra client.
- Kiểm tra hợp lệ schema biến môi trường bằng Zod hoặc `@t3-oss/env-nextjs` ngay từ build-time.

---

## 2. Vòng Đời State & Quản Lý Store (State Store Lifecycles)

### 2.1. Khởi tạo Store an toàn (Tránh Re-initialization & Memory Leaks)
- Khi dùng các state store dạng class/instance (MobX, Tinybase, custom event emitter), không dùng `useMemo(() => new Store(), [])` vì React không đảm bảo giữ nguyên giá trị `useMemo` qua các lần dọn dẹp bộ nhớ (semantic memoization can drop cached values).
- Hãy dùng `useState(() => new Store())` để đảm bảo khởi tạo duy nhất một lần:

```tsx
// ✅ ĐÚNG: Ổn định xuyên suốt các lần render
const [store] = useState(() => new EditorStore(config));

// ❌ SAI: useMemo có thể bị React GC dọn và khởi tạo lại, gây mất dữ liệu
const store = useMemo(() => new EditorStore(config), []);
```

### 2.2. Dọn dẹp Async chống Race-Condition khi chuyển trang (Navigation Race)
- Khi component unmount do chuyển route, việc dọn dẹp store tức thì (`store.dispose()`) có thể gây crash nếu một micro-task đang chờ xử lý dở dang.
- Sử dụng `useRef` lưu store và dọn dẹp qua `setTimeout(..., 0)`:

```tsx
const storeRef = useRef(store);
storeRef.current = store;

useEffect(() => {
  return () => {
    // Dọn dẹp an toàn ngoài luồng callstack tức thời
    setTimeout(() => {
      storeRef.current?.dispose();
    }, 0);
  };
}, []);
```

---

## 3. Các Mô Hình Thiết Kế Frontend Cốt Lõi (Frontend Design Patterns)

### 3.1. Container / Presentational Pattern
- **Presentational Component (Dumb/Pure)**: Chỉ quan tâm giao diện hiển thị thế nào. Nhận data & callbacks qua props. Không chứa business logic hay gọi API. Dễ dàng viết Storybook và Unit test.
- **Container Component (Smart)**: Chỉ quan tâm logic vận hành thế nào. Gọi API, quản lý state, bắt lỗi, truyền dữ liệu xuống Presentational component.

### 3.2. Compound Components Pattern (Thành phần Hợp thành)
- Áp dụng cho các UI phức tạp có nhiều bộ phận phụ thuộc nhau (Select, Tabs, Accordion, Modal).
- Cho phép người dùng linh hoạt bố cục mà vẫn chia sẻ state ngầm qua Context:

```tsx
// Sử dụng thanh thoát, không cần truyền hàng chục boolean props:
<Tabs defaultValue="account">
  <Tabs.List>
    <Tabs.Trigger value="account">Tài khoản</Tabs.Trigger>
    <Tabs.Trigger value="password">Mật khẩu</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="account"><AccountSettings /></Tabs.Content>
  <Tabs.Content value="password"><PasswordForm /></Tabs.Content>
</Tabs>
```

### 3.3. Headless UI & Custom Hooks Pattern (Tách Logic khỏi Giao diện)
- Mọi logic phức tạp (xử lý keyboard navigation, focus trap, validation form, debounce input) nên được tách thành Custom Hook không phụ thuộc UI (`useDropdown`, `useModal`, `useDebounce`).
- Nhờ đó, logic có thể tái sử dụng trên cả Web, Mobile (React Native) hoặc thay đổi theme mà không cần viết lại mã xử lý.

### 3.4. State Reducer & Finite State Machines (FSM)
- Với các luồng form nhiều bước (Wizard, Checkout, Onboarding), tránh dùng hàng loạt cờ boolean rải rác (`isStep1Done`, `isStep2Loading`, `isError`).
- Dùng `useReducer` hoặc Finite State Machine với các trạng thái tường minh:
  `IDLE -> STEP_1_FILLING -> STEP_1_VALIDATING -> STEP_2_FILLING -> SUBMITTING -> SUCCESS | ERROR`.
- Không bao giờ để hệ thống rơi vào trạng thái bất khả thi (ví dụ vừa `isLoading = true` vừa `isSuccess = true`).

### 3.5. Optimistic UI Updates & Skeleton Loading
- **Optimistic UI**: Cập nhật UI ngay lập tức khi người dùng click (như Like, Bookmark, Đổi tên) và gửi API nền; rollback nếu API thất bại kèm thông báo nhẹ nhàng (Toast).
- **Skeleton Loading**: Tuyệt đối không để màn hình trắng hoặc chỉ hiện một vòng xoay loading spinner đơn điệu. Sử dụng Skeleton Loader có kích thước tương đồng khối nội dung thực tế để loại bỏ Layout Shift (CLS).

---

## 4. Quy Chuẩn Sửa Đổi Mã Tối Ưu Token (Token-Efficient Surgical Diffs)

*(Đúc kết từ Onlook & Superpowers)*

1. **Sửa đổi phẫu thuật (Surgical Edits)**:
   - Khi chỉnh sửa một component, chỉ thay thế đúng hàm, thẻ JSX hoặc style cần sửa.
   - Tuyệt đối không rewrite toàn bộ file 500 dòng chỉ để đổi màu một nút bấm hoặc thêm một prop.
2. **Tôn trọng Path Alias**:
   - Luôn sử dụng alias cấu hình trong project (ví dụ `@/components/...`, `~/utils/...`). Tránh dùng đường dẫn tương đối dài ngoằng rắc rối (`../../../../components/...`).
3. **Giữ nguyên định dạng & Comments hiện hữu**:
   - Không tự ý re-format hay xóa các comment ghi chú logic của các lập trình viên khác trừ khi đó là mục tiêu chính của task.
4. **Xác thực dữ liệu biên (Edge Validation)**:
   - Mọi dữ liệu nhận từ Form hoặc API bên ngoài phải được parse/validate qua Zod schema trước khi đưa vào React state hoặc render.

---

## 5. Quy Chuẩn Thẩm Mỹ & Trải Nghiệm Người Dùng (Aesthetics & UX Standards)

1. **Bảng màu HSL có chủ đích (Curated Palettes)**:
   - Không dùng màu nguyên bản thô ráp (`#ff0000`, `#00ff00`).
   - Sử dụng các cặp màu hiện đại với sắc thái tương phản dễ chịu (slate/zinc, indigo/violet, emerald/teal).
   - Thiết kế sẵn hỗ trợ Dark Mode đồng bộ (dùng CSS variables cho màu nền, chữ, border).
2. **Phân cấp Typography rõ rệt**:
   - Sử dụng font chữ hiện đại (Inter, Geist, Roboto, Outfit).
   - Tỷ lệ kích thước phân cấp khoa học (`text-xs`, `text-sm`, `text-base`, `text-lg`, `text-2xl`, `text-4xl`).
   - Khoảng cách dòng (`leading-relaxed`) và khoảng cách tracking chuẩn mực.
3. **Micro-interactions & Glassmorphism**:
   - Nút bấm, card, modal phải có hiệu ứng hover, focus, active mượt mà (`transition-all duration-200 ease-in-out`).
   - Backdrop-blur nhẹ nhàng cho navbar/modal (`backdrop-blur-md bg-background/80`).
4. **Trạng thái Trống & Bắt Lỗi (Empty States & Error Boundaries)**:
   - Luôn thiết kế UI cho 4 trạng thái: **Loading**, **Empty (Chưa có dữ liệu)**, **Error (Lỗi kết nối/dữ liệu)**, và **Ready (Dữ liệu hiển thị)**.
   - Bọc các module giao diện lớn bằng `ErrorBoundary` để tránh crash toàn bộ ứng dụng khi một widget con bị lỗi.

---

## 6. Trí Tuệ Thiết Kế Tự Động & Danh Sách Kiểm Định Tiền Bàn Giao (UI/UX Pro Max)

*(Kế thừa từ kỹ năng `ui-ux-pro-max` - 192 reasoning rules, 79 UI styles, 74 font pairings, 119 UX guidelines)*

### 6.1. Sinh Hệ Thống Thiết Kế Tự Động (Design System Engine)
Khi bắt đầu một trang mới, màn hình mới hoặc toàn bộ dự án, chạy lệnh nội bộ để sinh bộ quy chuẩn thiết kế hoàn chỉnh:
```bash
python .agents/skills/ui-ux-pro-max/scripts/search.py "<loại_sản_phẩm> <ngành> <phong_cách>" --design-system -p "<Tên Dự Án>"
```
Ví dụ:
`python .agents/skills/ui-ux-pro-max/scripts/search.py "saas analytics dashboard modern" --design-system -p "Fteck Suite"`
Lệnh sẽ tự động trả về:
- **Bố cục (Layout Pattern)** & Cấu trúc các Section.
- **Phong cách UI chuẩn (UI Style)**: Glassmorphism, Bento Grid, Minimal, Soft UI, v.v. kèm đánh giá hiệu năng & khả năng tiếp cận.
- **Bảng màu ngữ nghĩa (Semantic Tokens)**: Primary, Secondary, Accent, Background, Foreground, Destructive kèm biến CSS `--color-*`.
- **Cặp Font chữ tối ưu (Typography Pairings)** từ Google Fonts kèm link `@import`.
- **Hiệu ứng & Anti-patterns cần tránh tuyệt đối**.

### 6.2. 10 Tiêu Chuẩn Ưu Tiên (Priority Hierarchy 1 → 10)
1. **Accessibility (CRITICAL)**: Độ tương phản văn bản tối thiểu 4.5:1 (WCAG AA). Mọi nút bấm icon phải có `aria-label`. Không xóa focus ring khi duyệt bằng bàn phím.
2. **Touch & Interaction (CRITICAL)**: Kích thước vùng bấm tối thiểu 44×44px (iOS) / 48×48px (Android). Phản hồi nhấn (active/hover/elevation) trong 80–150ms.
3. **Hiệu Năng Giao Diện (HIGH)**: Định dạng ảnh WebP/AVIF, lazy loading. Khóa chiều cao khung hình để triệt tiêu xô lệch bố cục (CLS < 0.1).
4. **Phong Cách & Biểu Tượng (HIGH)**: Cấm tuyệt đối dùng Emoji (🎨 🚀 ⚙️) làm biểu tượng tính năng/điều hướng. Bắt buộc dùng SVG vector đồng bộ (Lucide, Heroicons, Phosphor).
5. **Layout & Responsive (HIGH)**: Mobile-first. Cấm tuyệt đối để thanh cuộn ngang ngoài ý muốn (`overflow-x: hidden` nếu cần), không fix cứng `width: ...px` ở container chính.
6. **Kiểu Chữ & Màu Sắc (MEDIUM)**: Cỡ chữ thân tối thiểu 14–16px, line-height 1.5. Cấm văn bản xám mờ trên nền xám. Cấm viết mã màu hex cứng rải rác trong JSX.
7. **Chuyển Động (Animation - MEDIUM)**: Thời lượng vi chuyển động 150–300ms. Tôn trọng `prefers-reduced-motion`. Cấm animate thuộc tính `width`/`height` gây tái tính toán layout; chỉ animate `transform` và `opacity`.
8. **Biểu Mẫu & Phản Hồi (Forms - MEDIUM)**: Luôn có nhãn hiển thị (Visible Labels, không chỉ dựa vào placeholder). Lỗi hiển thị ngay dưới trường nhập. Hỗ trợ password manager và paste.
9. **Điều Hướng (Navigation - HIGH)**: Nút Back có thể đoán trước. Thanh điều hướng đáy (Bottom Nav) tối đa 5 tab. Hỗ trợ deep linking.
10. **Biểu Đồ & Dữ Liệu (Charts - LOW)**: Có chú giải (Legend), tooltip rõ ràng. Không truyền đạt thông tin chỉ bằng một sắc màu duy nhất.

### 6.3. Danh Sách Kiểm Định Tiền Bàn Giao (Pre-Delivery Checklist)
Mọi lập trình viên và nhà thiết kế trước khi nộp task Frontend phải tự tích đủ các tiêu chí:
- [ ] Không có emoji làm icon hệ thống (đã dùng SVG Lucide / Phosphor).
- [ ] Thuộc tính `cursor-pointer` có trên mọi phần tử bấm được.
- [ ] Vùng chạm đạt tối thiểu 44×44px trên mobile.
- [ ] Tương phản chữ đạt chuẩn ≥ 4.5:1 ở cả Light Mode và Dark Mode.
- [ ] Trạng thái focus hiển thị rõ nét khi bấm phím Tab.
- [ ] Tôn trọng tùy chọn giảm chuyển động `prefers-reduced-motion`.
- [ ] Đã kiểm tra responsive mượt mà trên 4 kích thước: 375px, 768px, 1024px, 1440px.

