---
name: xerj
description: Definition-first & hybrid AST code search over locally indexed repositories via XERJ CLI and MCP. Use instead of grep/cat to find symbols, class/method definitions, and relevant passages with exact line numbers while saving context tokens.
triggers:
  - xerj
  - code search
  - find definition
  - ast search
  - search codebase
  - symbol lookup
---

# /xerj — Bộ máy tìm kiếm mã nguồn cục bộ theo AST & Hybrid (XERJ)

> [!NOTE]
> **XERJ Engine**: Local Search Engine tương thích Elasticsearch (wire-compatible) trên cổng `9200`.
> Dùng tree-sitter trích xuất AST + BM25 + kNN vector search để trả về chính xác tọa độ hàm/lớp/khối lệnh thay vì đọc toàn bộ file.

## 1. Kiến trúc vận hành trên máy

- **XERJ Daemon**: Đang chạy tự động qua macOS LaunchAgent:
  - File cấu hình: `~/Library/LaunchAgents/com.xerj.server.plist`
  - Endpoint REST / ES-compat: `http://localhost:9200`
  - Thư mục dữ liệu: `~/.xerj-data/`
- **MCP Server**: Được đăng ký trong `mcp/mcp-servers.local.json` và phân phối đến mọi agent:
  - Tên: `xerj`
  - Lệnh: `xerj mcp` (hoặc `~/.local/bin/xerj mcp`)
  - Công cụ MCP khả dụng: `xerj_def`, `xerj_search`, `xerj_semantic_search`, `xerj_hybrid_search`, `xerj_code_search`, `xerj_map`, `xerj_hub_find`, `xerj_hub_ask`.

## 2. Cách lập chỉ mục (Indexing)

Khi vào một repo hoặc thư mục mới cần tìm kiếm:

```bash
# Đánh chỉ mục repo với prefix đại diện (ví dụ gdt hoặc auth)
xerj autoindex /path/to/repo --prefix <tên-prefix>
```

- Lần đầu chạy sẽ quét AST các file mã nguồn (Java, Python, TS, Rust, Go, C/C++...).
- Các lần sau là cập nhật gia tăng (incremental) cực nhanh.

## 3. Cách tra cứu qua CLI

```bash
# 1. Tìm chính xác nơi định nghĩa symbol (class, struct, function, interface)
xerj def "<symbol>" --prefix <tên-prefix>
# Trả về: file:line + chữ ký hàm (signature) ngay lập tức

# 2. Tìm kiếm đoạn code liên quan (Passage Search)
xerj search "<từ khóa hoặc hành động>" --prefix <tên-prefix>
# Trả về: đoạn code bao quanh hàm/block liên quan nhất kèm tọa độ dòng
```

## 4. Cách tra cứu qua MCP (Khuyến nghị cho Agent)

Khi chat hoặc lập trình, Agent ưu tiên gọi các công cụ MCP:
- `xerj_def`: Truy vấn symbol theo tên hoặc cụm từ định nghĩa (`symbol: "AuthService"`, `prefix: "gdt"`).
- `xerj_search`: Truy vấn theo ngôn ngữ tự nhiên hoặc truy vấn DSL, trả về passage chứa đoạn code khớp nhất.
- `xerj_map`: Xem sơ đồ trường và các chỉ mục đã đánh của node hiện tại.

## 5. Lưu ý bắt buộc (Tránh lỗi `0` kết quả & Lạm dụng `safe-search`)

1. **LUÔN truyền `prefix` của dự án** (`prefix="gdt"` ở `gdt-workspace`, `prefix="agentbase"` ở `agent-base`, `prefix="tiktok"` ở `tiktok`). Nếu bỏ trống `prefix`, XERJ mặc định chỉ quét `ax-*` và sẽ trả về **`0` kết quả** dù repo đã index đầy đủ.
2. **Nếu `graphify` (`graph_stats`) báo thiếu `graph.json`**: chuyển ngay sang dùng `xerj_def` / `xerj_search` kèm `prefix`, không rơi về tìm chữ thô.
3. **Phân định ranh giới với `scripts/safe-search.py`**:
   - `xerj_def` / `xerj_search` (kèm `prefix`): bắt buộc cho tra cứu AST/symbol (`class`, `enum`, `interface`, `method`, `function`).
   - `read_file`: bắt buộc khi đã biết đường dẫn file.
   - `safe-search.py` (giới hạn mặc định 10 dòng, tối đa 20 qua `-l` để chống tràn context): **CHỈ dùng cho chuỗi text thuần / nhãn UI / i18n / mã lỗi**, CẤM dùng thay `xerj` để dò tên `class` hay `enum`.
4. **Khi sửa code/rule xong**: chạy lại `xerj autoindex <thư-mục> --prefix <prefix> --yes` (hoặc `xerj` cập nhật gia tăng) để tránh chỉ mục bị trễ dòng (`stale`).

