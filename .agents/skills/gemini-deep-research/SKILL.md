---
name: gemini-deep-research
description: Tích hợp và điều phối công cụ Gemini-API (gemini-webapi) để thực hiện tra cứu web nâng cao, hỏi đáp có Google Grounding, và kích hoạt tiến trình Deep Research tự động, tuân thủ nghiêm ngặt cổng Ask-Before-Search.
---

# Gemini Deep Research & Web Lookup Skill

Cẩm nang kỹ năng này hướng dẫn các Agent (đặc biệt là `researcher`, `analyst`, `ai-eng`) cách tận dụng bộ công cụ **Gemini-API** (`fteck/Gemini-API`) để thực hiện tra cứu thông tin trên Internet, cào dữ liệu có kiểm chứng, và chạy quy trình **Gemini Deep Research** chuyên sâu nhiều tầng.

---

## 🛑 NGUYÊN TẮC CỐT TỬ: CỔNG HỎI TRƯỚC KHI TRA CỨU (Ask-Before-Search)

Trước khi thực hiện bất kỳ lệnh nào gửi request đến `Gemini-API` hoặc ra ngoài Internet, Agent **BẮT BUỘC** phải dừng lại và hỏi người dùng:

```text
❓ [XÁC NHẬN TRA CỨU QUA GEMINI-API]
- Chủ đề / Câu hỏi: "<nội dung dự kiến gửi>"
- Phương thức: [ask (Tra cứu nhanh có nguồn) | research (Deep Research chuyên sâu)]
- Mô hình: [gemini-flash | gemini-pro]
👉 Bạn có đồng ý cho phép gửi yêu cầu tra cứu này không?
```

Chỉ khi người dùng xác nhận đồng ý (hoặc cung cấp cờ `--confirm`), Agent mới được phép gọi script thực thi.

---

## 1. Cấu Trúc Thành Phần Tự Chứa (Self-Contained in agent-base)
- **Mã nguồn Gemini-API nội bộ**: `tools/gemini-api/cli.py` (nằm gọn gàng bên trong `agent-base`, không phụ thuộc ra ngoài)
- **Mẫu cấu hình Cookies**: `gemini_cookies.example.json` ➔ người dùng sao chép thành `gemini_cookies.json`
- **Script điều phối tại agent-base**: `scripts/gemini-research.py` (tự động ưu tiên `tools/gemini-api`)

---

## 2. Các Luồng Nghiệp Vụ Chính

### Luồng A: Tra cứu nhanh kèm nguồn Google Grounding (`ask`)
Dùng khi cần câu trả lời nhanh, có trích dẫn nguồn web trực tiếp từ Google:
```bash
python scripts/gemini-research.py ask "So sánh hiệu năng giữa BiRefNet và InSPyReNet cho ảnh POD 4K"
```
Kết quả trả về text tổng hợp kèm danh sách link nguồn (Web citations) và hình ảnh nếu có.

---

### Luồng B: Quy trình Nghiên cứu Đa tầng (Deep Research Workflow)
Dành cho các bài toán phức tạp đòi hỏi Agent nghiên cứu hàng chục trang web, lập dàn ý và xuất bản báo cáo hoàn chỉnh (3.000 – 10.000 từ):

1. **Khởi tạo tiến trình nghiên cứu**:
   ```bash
   python scripts/gemini-research.py research-send "Phân tích xu hướng thiết kế thời trang Halloween 2026 trên Etsy và Pinterest"
   ```
   Lệnh sẽ in ra: `Chat ID: <chat_id>`, `Title: ...`, `Steps: ...`

2. **Kiểm tra tiến độ (Status Polling)**:
   ```bash
   python scripts/gemini-research.py research-check <chat_id>
   ```
   * Nếu đang chạy: Trả về trạng thái các bước đã duyệt web.
   * Nếu hoàn tất: Báo hiệu báo cáo đã sẵn sàng.

3. **Tải và lưu báo cáo chính thức**:
   ```bash
   python scripts/gemini-research.py research-get <chat_id> -o docs/research/bao-cao-xu-huong-halloween-2026.md
   ```
   Báo cáo Markdown hoàn chỉnh được lưu trực tiếp vào thư mục `docs/research/` của dự án để `architect` và `product` khai thác.

---

## 3. Xử Lý Khi Cookies Hết Hạn (Authentication Troubleshooting)

Khi chạy lệnh kiểm tra:
```bash
python scripts/gemini-research.py inspect
```
Nếu nhận thông báo `Account status: UNAUTHENTICATED (1016)`:
1. Agent **không tự ý đọc hay sửa file cookies**.
2. Báo cáo rõ ràng cho người dùng: *"Cookies trong `gemini_cookies.json` đã hết hạn. Bạn vui lòng mở trình duyệt đăng nhập lại Gemini Web và xuất cookies mới vào file `gemini_cookies.json`."*
