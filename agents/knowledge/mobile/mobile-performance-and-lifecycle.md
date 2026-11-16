# Tối Ưu Hiệu Năng 60 FPS & Vòng Đời Ứng Dụng Di Động (Mobile Performance & Lifecycle)

> **Loại: tham khảo.** Kỹ thuật tối ưu render 60/120 FPS, chống rò rỉ bộ nhớ và quản trị vòng đời ứng dụng di động.
> Liên quan: `agents/roles/role-mobile.md`, `frontend-patterns.md`.

## 1. Mục Tiêu Hiệu Năng Render (The 16.6ms Budget)

Để đạt chuẩn hiển thị mượt mà 60 FPS, UI Thread chỉ có tối đa **16.6 mili-giây** để vẽ mỗi khung hình (hoặc 8.3ms cho màn hình 120Hz).
- Nếu một phép tính chiếm dụng UI Thread quá 16.6ms $\rightarrow$ Khung hình bị rơi rớt (*Frame Drop / Jank*), tạo cảm giác giật khựng khó chịu.

## 2. Bốn Kỹ Thuật Triệt Tiêu Giật Khựng (Jank-Free Engineering)

1. **Tái chế View cho danh sách dài (View Recycling):**
   - Tuyệt đối cấm render hàng nghìn phần tử cùng lúc vào bộ nhớ.
   - Bắt buộc dùng view ảo hóa có tái chế bộ nhớ: `RecyclerView` (Android), `LazyColumn` (Jetpack Compose), `ListView.builder` (Flutter), hoặc `FlatList` kèm `getItemLayout`, `windowSize={5}` (React Native).
2. **Đưa tác vụ nặng sang Background Thread:**
   - Parse JSON dung lượng lớn, mã hóa mật mã (Crypto), nén ảnh, và truy vấn DB **bắt buộc chạy trên background**: dùng Kotlin Coroutines `Dispatchers.IO`, Flutter `compute()` / `Isolate`, hoặc Worker thread.
   - UI Thread chỉ làm duy nhất một việc: tiếp nhận cử chỉ chạm và vẽ giao diện.
3. **Đường ống nén và cache hình ảnh (Image Pipeline):**
   - Không tải ảnh nguyên gốc 4K về hiển thị ở thumbnail 100x100px. Bắt buộc resize ảnh theo đúng kích thước hiển thị.
   - Dùng cache 2 tầng (Memory Cache LRU + Disk Cache): Glide, Coil (Android), `cached_network_image` (Flutter).
4. **Triệt tiêu re-render thừa (Re-render Optimization):**
   - Áp dụng `const constructor` (Flutter) để widget không bị rebuild khi cha đổi state.
   - Dùng `React.memo`, `useCallback`, selector pattern (Zustand/Bloc) để chỉ rebuild đúng component lắng nghe trường dữ liệu thay đổi.

## 3. Chống Rò Rỉ Bộ Nhớ (Memory Leak Prevention)

Cổng kiểm tra mã nguồn chặn đứng 3 nguyên nhân gây sập ứng dụng (OOM Crash):
- **Quên hủy đăng ký lắng nghe:** Mọi StreamSubscription, EventListener, Timer, RxJava Disposable bắt buộc phải `cancel()` trong `dispose()` / `onDestroyView()`.
- **Giữ tham chiếu Context tĩnh:** Cấm lưu Activity Context vào biến `static` hoặc Singleton.
- **Closure giữ tham chiếu Widget:** Dùng `WeakReference` khi truyền callback vào các tác vụ chạy nền dài hạn.

## 4. Quản Trị Vòng Đời & Khôi Phục Trạng Thái (State Restoration)

Khi người dùng chuyển sang app khác, hệ điều hành có thể tiêu diệt app ngầm để giải phóng RAM:
- Bắt buộc lưu trữ trạng thái form đang nhập dở và vị trí cuộn danh sách vào `savedInstanceState` (Android) hoặc `RestorationMixin` (Flutter).
- Khi người dùng quay lại, tự động khôi phục đúng trạng thái trước khi bị tắt ngầm.
