# Heuristics Phân Tích & Bộ Nhận Diện Lỗi FEW HICCUPPS (Test Oracles & SFDIPOT)

> **Loại: tham khảo.**
> Nguồn: tách từ test-heuristics-and-oracles.md mục 1, 2, 3.
> Tiêu chuẩn: James Bach & Michael Bolton (RST / HTSM), Elisabeth Hendrickson (Explore It!).

## 1. Mô Hình Phân Tích SFDIPOT (San Francisco Depot)

Giúp quét toàn diện sản phẩm mà không bị đóng khung trong giao diện đồ họa (UI):
- **S – Structure:** Mã nguồn, module, config, DB schema, microservices, thư viện thứ 3.
- **F – Function:** Mọi điều sản phẩm thực hiện (tính toán, IF-ELSE, luồng, ngoại lệ).
- **D – Data:** Dữ liệu vào/ra, giá trị mặc định, liên kết bảng, dữ liệu rác.
- **I – Interfaces:** REST endpoints, Web UI, CLI, Kafka/RabbitMQ, Webhook, Sockets.
- **P – Platform:** OS, JVM/Node, Trình duyệt, Tài nguyên CPU/RAM/Heap.
- **O – Operations:** Người dùng thực tế (Admin, Khách, Kẻ tấn công). Giờ cao điểm.
- **T – Time:** Múi giờ, năm nhuận, chốt sổ ban đêm, timeout, độ trễ bất đồng bộ.

## 2. Heuristic Tấn Công Biến Số (Elisabeth Hendrickson)

*"It's all about the variables"* — Mọi lỗi đều bắt nguồn từ sự biến đổi của biến số:
1. **Heuristic "Count: 0, 1, Many":**
   - *Zero (0):* Danh sách rỗng, giỏ 0 món, số lượng = 0, file 0 byte $\rightarrow$ Bắt lỗi NPE.
   - *One (1):* Đúng 1 phần tử (Biên đơn lập).
   - *Many (Nhiều):* Hàng nghìn phần tử đổ về $\rightarrow$ Bắt lỗi phân trang, tràn bộ đệm.
2. **Heuristic "Goldilocks" (Ba Chú Gấu):**
   - *Too Small:* Chuỗi rỗng, số âm, payload 1 byte.
   - *Too Big:* Chuỗi 10k ký tự, số vượt quá $2^{31}-1$, file 500MB.
   - *Just Right:* Dữ liệu danh định chuẩn mực.
3. **Heuristic "Sequence Perturbation":** Làm ngược quy trình, nhảy bước, bấm Back giữa chừng, gọi API bước 3 khi chưa chạy bước 1.
4. **Heuristic "Input Method":** Thử gõ phím vs Copy/Paste vs Kéo thả vs cURL trực tiếp.

## 3. Bộ 11 Tiêu Chí Nhận Diện Lỗi FEW HICCUPPS

Giúp Agent nhận diện chính xác khi nào một hành vi bất thường là **BUG**:
1. **F – Familiarity:** Trái ngược thói quen chuẩn mực thông thường.
2. **E – Explainable:** Không thể giải thích hợp lý (hiện tượng kỳ quặc).
3. **W – World:** Vi phạm thực tế đời sống (tiền tệ 3 số lẻ, ngày sinh tương lai).
4. **H – History:** Bản trước chạy tốt, bản này lỗi $\rightarrow$ **Bug hồi quy**.
5. **I – Image:** Làm mất uy tín thương hiệu, lộ dữ liệu khách hàng.
6. **C – Comparable:** Sản phẩm đối thủ chạy tốt, hệ thống mình báo lỗi.
7. **C – Claims:** Mâu thuẫn với PRD, Swagger API hoặc cam kết tiếp thị.
8. **U – User Desires:** Cản trở mục đích cốt lõi người dùng muốn hoàn thành.
9. **P – Product:** Bất nhất quán nội tại (màn hình A nút bên phải, B bên trái).
10. **P – Purpose:** Vi phạm mục đích cơ bản tính năng phục vụ.
11. **S – Statutes:** Vi phạm pháp luật (An ninh mạng, bảo vệ PII, PCI-DSS).
