---
name: xerj-hub
description: Answer questions about public libraries, frameworks, open-source code, and standards using pre-indexed Hub corpus without cloning or manual downloading (e.g. xerj "how does react render work").
triggers:
  - xerj hub
  - public library code
  - framework source
  - ask hub
---

# /xerj-hub — Tra cứu mã nguồn thư viện mã nguồn mở qua XERJ Corpus Hub

> [!NOTE]
> Cho phép Agent truy vấn các dự án mã nguồn mở, chuẩn RFC, hay tài liệu thư viện bên ngoài mà không cần git clone hay đọc tốn dung lượng ổ cứng.

## 1. Khi nào dùng

- Khi cần tra cứu cách một thư viện mã nguồn mở (Spring Boot, React, Tokio, Elasticsearch...) hoạt động bên dưới.
- Khi cần xem chữ ký hàm, hằng số, default config của các gói phụ thuộc bên thứ 3.
- Khi không có mã nguồn repo đó trên máy cục bộ.

## 2. Cách tra cứu qua CLI

```bash
# Hỏi trực tiếp bằng ngôn ngữ tự nhiên
xerj "<câu hỏi kỹ thuật hoặc thư viện>"

# Tìm chính xác định nghĩa hằng số hoặc hàm trong hub
xerj ask --def <SYMBOL>
```

## 3. Cách tra cứu qua MCP

- `xerj_hub_find`: Tìm xem Hub có gói dữ liệu nào khớp với câu hỏi (`question: "..."`).
- `xerj_hub_def`: Tìm định nghĩa symbol trong một corpus cụ thể (`slug: "...", symbol: "..."`).
- `xerj_hub_ask`: Trả lời câu hỏi kỹ thuật từ hub corpus trong 1 lượt gọi.

