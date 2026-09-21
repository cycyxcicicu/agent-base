# Ví Dụ Mẫu: Đánh Giá An Toàn & Red-Teaming Cho Coding Agent

Thừa hưởng từ các kỹ thuật kiểm thử LLM hàng đầu của `promptfoo` (đặc biệt là plugin `redteam-coding-agent`, `asciiSmuggling`, `bola`, `bfla`), thư mục này cung cấp hệ thống đánh giá tự động các rào chắn bảo vệ Agent.

## Các Thành Phần
1. `promptfooconfig.yaml`: File cấu hình khai báo tiêu chuẩn Promptfoo chính thức, chứa danh sách plugins, ma trận rubric và synthetic canary secret.
2. `eval-runner.js`: Bộ runner Node.js tự lập mô phỏng các đợt tấn công Red-Teaming nhắm vào Coding Agent:
   - Thử thách trích xuất dữ liệu nhạy cảm (Synthetic Canary Leak Test).
   - Thử thách bẻ khóa Human Commit Gate (`git push`, `git commit`).
   - Thử thách leo thang thư mục (Path Traversal Escapes).
   - Thử thách chèn lệnh shell phá hoại (`rm -rf /`).

## Cách Chạy Kiểm Định An Toàn
```bash
node examples/llm-eval-redteam/eval-runner.js
```
