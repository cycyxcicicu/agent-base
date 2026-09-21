# Hướng Dẫn Vẽ Sơ Đồ Thiết Kế Chuẩn Biên Tập (Diagram Design Guide)

Tài liệu này hướng dẫn các vai **BA, Architect, Designer, Writer** áp dụng kỹ thuật vẽ sơ đồ chuẩn xuất bản từ skill `diagram-design`. Sơ đồ được lưu dưới dạng file HTML độc lập chứa SVG vector, mở được trực tiếp trên trình duyệt, nhúng vào tài liệu hoặc xuất ra PNG mà không cần bất kỳ server hay runtime phụ thuộc nào.

---

## 1. Triết Lý Biên Tập & Chống "AI Slop"

Một sơ đồ xuất sắc không phải là sơ đồ nhồi nhét thật nhiều hình khối, mà là **loại bỏ tối đa những thứ thừa thãi**:
- **Mật độ mục tiêu: 4/10**: Đủ để hiểu trọn vẹn mặt kỹ thuật/nghiệp vụ. Nếu vượt quá 9 node, hãy tách thành 2 sơ đồ (Sơ đồ tổng quan + Sơ đồ chi tiết).
- **Quy tắc tiêu điểm (Focal Accent)**: Màu cam ấm (Accent `#eb6c36`) chỉ dùng cho **tối đa 1–2 node quan trọng nhất** (bước đột phá, điểm nghẽn, hoặc cổng bảo mật). Mọi node còn lại đều dùng màu trung tính (`ink`, `muted`).
- **Nghiêm cấm các lỗi AI Slop thường gặp**:
  - ❌ Nền đen kết hợp viền tím/xanh neon phát sáng rẻ tiền.
  - ❌ Tất cả các hình hộp đều giống hệt nhau (làm mất hệ phân cấp thông tin).
  - ❌ Chữ nằm đè lên mũi tên mà không có hộp che (`masking rect`) làm lem chữ.
  - ❌ Đổ bóng lòe loẹt (`shadow`). Hãy dùng đường viền mảnh thanh lịch (`border/hairline`).

---

## 2. Bảng Chọn 7 Mẫu Ngữ Nghĩa (Semantic Patterns)

Khi luồng nghiệp vụ hoặc kiến trúc mang ý nghĩa vận hành, hãy chọn **Semantic Pattern** trước, sau đó dùng Visual Type tương ứng để dàn trang:

| Nhu cầu diễn đạt của bạn | Mẫu ngữ nghĩa (Semantic Pattern) | Loại sơ đồ dàn trang |
|---|---|---|
| Nhiều nguồn dữ liệu đổ về một điểm nghẽn / hàng đợi | **Fan-in queue / bottleneck** | Data flow |
| Quy trình nhiều giai đoạn lặp lại cùng các ô ngữ nghĩa (Input, Policy, Output) | **Stage framework with semantic slots** | Process |
| Từ hội thoại / yêu cầu thô chuyển hóa thành tài liệu cấu trúc (Luồng Intake của BA) | **Unstructured input → structured artifact** | Data flow |
| So sánh 2 luồng đánh giá chính sách (Pass / Fail / Skipped / Not Reached) | **Paired policy-evaluation traces** | Flowchart |
| Ranh giới tin cậy: đường đi an toàn, cổng kiểm soát, luồng bị chặn | **Secure paved road** | Architecture |
| Phân loại biện pháp kiểm soát theo bề mặt thực thi | **Governance / control catalog** | Layer stack |
| Đối tượng chuyển đổi qua các trạng thái, hàng đợi chờ, thử lại, hoàn tất | **Lifecycle phase map** | State Machine |

---

## 3. Bản Đồ 41 Loại Sơ Đồ Trực Quan (Visual Types)

Tham khảo chi tiết cú pháp từng loại trong thư mục `.agents/skills/diagram-design/references/`:

1. **Kiến trúc & Hạ tầng**:
   - `type-architecture.md`: Thành phần hệ thống và các kết nối.
   - `type-it-state.md`: Hiện trạng hạ tầng CNTT trước chuyển đổi (Current-state).
   - `type-deployment.md`: Triển khai trên server, cụm container, cổng mạng, replica.
   - `type-high-level.md`: Bức tranh toàn cảnh end-to-end data stack.
2. **Nghiệp vụ & Quy trình (Dành riêng cho BA)**:
   - `type-process.md`: Quy trình phối hợp nhiều bước với dữ liệu bàn giao.
   - `type-swimlane.md`: Quy trình phân làn trách nhiệm giữa các phòng ban.
   - `type-journey.md`: Hành trình trải nghiệm của khách hàng/người dùng.
   - `type-story-map.md`: Lộ trình tính năng chia theo các bản phát hành.
   - `type-kanban.md`: Tiến độ công việc, giới hạn WIP và điểm nghẽn.
3. **Dữ liệu & Logic Hệ Thống**:
   - `type-flowchart.md`: Cây logic rẽ nhánh quyết định.
   - `type-sequence.md`: Thông điệp tuần tự theo thời gian giữa các Service/Actor.
   - `type-state.md`: Máy trạng thái (State Machine) với điều kiện Guard.
   - `type-er.md` & `type-db-schema.md`: Thực thể quan hệ và sơ đồ bảng CSDL vật lý.
   - `type-data-flow.md`: Luồng dữ liệu phân quyền theo vai trò.
   - `type-medallion.md`: Kiến trúc kho dữ liệu 3 tầng (Bronze, Silver, Gold).
4. **Phân tích & Thống kê**:
   - `type-fishbone.md`: Sơ đồ xương cá phân tích nguyên nhân gốc rễ (Root-Cause).
   - `type-wardley.md`: Bản đồ chuỗi giá trị và độ trưởng thành công nghệ.
   - `type-radar.md`: Đánh giá đa tiêu chí (Radar / Spider chart).
   - `type-quadrant.md`: Ma trận định vị 4 góc phần tư (Prioritization Matrix).
   - `type-waterfall.md`, `type-sankey.md`, `type-treemap.md`, `type-gantt.md`...

---

## 4. Hệ Thống Màu & Token Chuẩn Biên Tập (Editorial Tokens)

```css
:root {
  --color-paper:       #f5f5f5;              /* Nền trang */
  --color-paper-2:     #ececec;              /* Nền container */
  --color-ink:         #2d3142;              /* Chữ chính & nét vẽ chính */
  --color-muted:       #4f5d75;              /* Chữ phụ & nét thứ cấp */
  --color-soft:        #7a8399;              /* Nhãn chú thích nhỏ */
  --color-rule:        rgba(45,49,66,0.12);  /* Đường kẻ phân cách */
  --color-accent:      #eb6c36;              /* Màu tiêu điểm (Terracotta) */
  --color-accent-tint: rgba(235,108,54,0.08);/* Nền phủ nhẹ của node tiêu điểm */
  --color-link:        #2e5aa8;              /* Màu gọi API / kết nối ngoài */
}
```

---

## 5. Mẫu Boilerplate HTML/SVG Hoàn Chỉnh

Dưới đây là mẫu khung chuẩn, BA và Architect có thể tạo tệp `.html` trong `docs/spec/` hoặc `docs/analysis/`:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sơ Đồ Quy Trình / Kiến Trúc</title>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Geist:wght@400;500;600&family=Geist+Mono&display=swap" rel="stylesheet">
  <style>
    :root {
      --color-paper: #f5f5f5;
      --color-ink: #2d3142;
      --color-muted: #4f5d75;
      --color-accent: #eb6c36;
      --color-accent-tint: rgba(235,108,54,0.08);
      --color-rule: rgba(45,49,66,0.15);
    }
    body { font-family: 'Geist', sans-serif; background: var(--color-paper); color: var(--color-ink); padding: 2rem; margin: 0; }
    .header { max-width: 1000px; margin: 0 auto 1.5rem auto; }
    h1 { font-family: 'Instrument Serif', serif; font-size: 2.2rem; margin-bottom: 0.25rem; font-weight: normal; }
    p.subtitle { color: var(--color-muted); font-size: 0.95rem; }
    .diagram-card { max-width: 1000px; margin: 0 auto; background: #fff; border: 1px solid var(--color-rule); border-radius: 6px; padding: 1.5rem; }
    svg { width: 100%; height: auto; display: block; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Tiêu Đề Sơ Đồ Hệ Thống</h1>
    <p class="subtitle">Mô tả ngắn gọn về mục tiêu và phạm vi thể hiện của sơ đồ.</p>
  </div>
  <div class="diagram-card">
    <svg viewBox="0 0 900 350" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- Mũi tên chuẩn -->
        <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="var(--color-ink)"/>
        </marker>
      </defs>

      <!-- Node 1: Nguồn đầu vào -->
      <rect x="50" y="120" width="180" height="70" rx="6" fill="#fff" stroke="var(--color-ink)" stroke-width="1.5"/>
      <text x="140" y="150" text-anchor="middle" font-size="13" font-weight="600" fill="var(--color-ink)">docs/source/</text>
      <text x="140" y="170" text-anchor="middle" font-size="11" fill="var(--color-muted)">Tài liệu gốc (Word, PDF, Ảnh)</text>

      <!-- Mũi tên kết nối có Mask che chữ -->
      <line x1="230" y1="155" x2="350" y2="155" stroke="var(--color-ink)" stroke-width="1.5" marker-end="url(#arrow)"/>
      <rect x="255" y="145" width="70" height="20" fill="#fff"/>
      <text x="290" y="159" text-anchor="middle" font-size="10" fill="var(--color-muted)">convert-docs</text>

      <!-- Node 2: Tiêu điểm (Focal Node) -->
      <rect x="360" y="110" width="220" height="90" rx="6" fill="var(--color-accent-tint)" stroke="var(--color-accent)" stroke-width="2"/>
      <text x="470" y="145" text-anchor="middle" font-size="14" font-weight="600" fill="var(--color-accent)">MarkItDown + LLM OCR</text>
      <text x="470" y="165" text-anchor="middle" font-size="11" fill="var(--color-ink)">Bóc tách bảng, chữ, OCR hình ảnh</text>
      <text x="470" y="182" text-anchor="middle" font-size="10" font-family="'Geist Mono', monospace" fill="var(--color-muted)">9Router Gateway</text>

      <!-- Mũi tên kết nối 2 -->
      <line x1="580" y1="155" x2="690" y2="155" stroke="var(--color-ink)" stroke-width="1.5" marker-end="url(#arrow)"/>

      <!-- Node 3: Đầu ra -->
      <rect x="700" y="120" width="160" height="70" rx="6" fill="#fff" stroke="var(--color-ink)" stroke-width="1.5"/>
      <text x="780" y="150" text-anchor="middle" font-size="13" font-weight="600" fill="var(--color-ink)">docs/converted/</text>
      <text x="780" y="170" text-anchor="middle" font-size="11" fill="var(--color-muted)">Markdown + Báo cáo Audit</text>
    </svg>
  </div>
</body>
</html>
```
