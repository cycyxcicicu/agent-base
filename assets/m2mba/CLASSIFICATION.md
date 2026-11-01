# Bảng Phân Loại & Đánh Giá Tri Thức M2MBA Cho Đội Ngũ Agent

Tài liệu này đánh giá các bài viết chuyên môn từ m2mba.com/blog và phân bổ tri thức vào các vai trò tương ứng trong `agent-base`.

## 1. Phân Bổ Theo Vai Trò

### A. Vai Business Analyst (`ba`)
- **Kỹ năng cốt lõi**: Khảo sát nghiệp vụ, quản lý yêu cầu (BABOK), đặc tả SRS, mô hình hóa State Machine, kỹ năng làm việc với Dev.
- **Bài viết tương ứng**:
  - **[BA không cần hiểu kỹ thuật — nhưng cần hiểu đúng 2 thứ này khi làm việc với Dev](posts/ba-lam-viec-voi-dev-2-dieu-cot-loi.md)**
    - *Tóm tắt*: Kỹ năng giao tiếp và bóc tách yêu cầu khả thi giữa Business Analyst và Development Team.
  - **[Tài liệu mẫu SRS (Software Requirements Specification)](posts/tai-lieu-mau-srs-chuan.md)**
    - *Tóm tắt*: Mẫu đặc tả yêu cầu phần mềm chuẩn cho dự án thực tế từ đầu đến cuối.
  - **[Kỹ thuật State Diagram cho Business Analyst: Hướng dẫn chi tiết & Các sai lầm cần tránh](posts/state-diagram-cho-ba-huong-dan-chi-tiet.md)**
    - *Tóm tắt*: Phương pháp mô hình hóa các trạng thái nghiệp vụ và chuyển trạng thái không bị sót case.
  - **[Lộ trình IIBA – Chuẩn Khung Năng Lực Quốc Tế Cho Phân Tích Nghiệp Vụ](posts/lo-trinh-chuan-iiba-cho-business-analyst.md)**
    - *Tóm tắt*: Khung chuẩn BABOK, 6 vùng tri thức (Knowledge Areas) và quy trình quản trị yêu cầu.

### B. Vai Product Lead / Manager (`product`)
- **Kỹ năng cốt lõi**: Định hình tính năng, Scope-Cut, xây dựng workflow cho AI Agent, MVP roadmap.
- **Bài viết tương ứng**:
  - **[AI Agent Builder: Thiết kế Workflow và Gọi API Tự Động](posts/ai-agent-builder-workflow-api.md)**
    - *Tóm tắt*: Định hình sản phẩm ứng dụng AI Agent, thiết kế luồng người dùng và API integration.

### C. Vai System Architect (`architect`)
- **Kỹ năng cốt lõi**: Thiết kế RAG, Vector Search, giao thức MCP Tool Calling, tích hợp hệ thống LLM.
- **Bài viết tương ứng**:
  - **[Vì sao BA nên hiểu Model Context Protocol (MCP) & Tool Calling trong AI](posts/vi-sao-ba-nen-hieu-mcp-tool-calling.md)**
    - *Tóm tắt*: Cơ chế Tool Calling, chuẩn giao tiếp MCP và ứng dụng vào tự động hóa phân tích nghiệp vụ.
  - **[Giải Mã Sức Mạnh của LangChain, RAG và Chatbot: Hướng Dẫn Dành Cho BA](posts/giai-ma-langchain-rag-chatbot-cho-ba.md)**
    - *Tóm tắt*: Hiểu cấu trúc Retrieval-Augmented Generation, vector embedding và prompt engineering.
  - **[Từ Vector đến Chatbot: Hành trình để AI hiểu và trả lời như con người](posts/tu-vector-rag-den-chatbot-thong-minh.md)**
    - *Tóm tắt*: Cách thức xử lý dữ liệu phi cấu trúc, vector search và indexing cho hệ thống AI.
