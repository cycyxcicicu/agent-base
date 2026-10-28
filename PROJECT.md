# PROJECT.md — phần riêng của dự án agent-base

Tài liệu cấu hình và hướng dẫn vận hành của khung làm việc tác tử `agent-base`.

| Mục | Giá trị |
|---|---|
| Tên dự án | agent-base |
| Mô tả một câu | Khung làm việc đa tác tử (multi-agent framework) độc lập nền tảng, lấy tri thức và bằng chứng làm cốt lõi cho vòng đời phát triển phần mềm |
| Stack | `agents/stacks/python.md` (Python 3.11+) |
| Nhánh chính | `main` |
| Nhánh tích hợp | `develop` |

## Lệnh vận hành và kiểm chuẩn

Toàn bộ các lệnh dưới đây được lấy từ quy trình kiểm tra CI (`.github/workflows/check.yml`) và đã được kiểm chứng chạy thật.

| Việc | Lệnh |
|---|---|
| Cài phụ thuộc | `pip install -e ".[dev]"` (hoặc dùng thư viện tiêu chuẩn Python) |
| Chạy kiểm tra sức khỏe | `python scripts/doctor.py` |
| Test suite | `python -m unittest discover -s tests -q` |
| Lint / Check adapters | `python scripts/sync-adapters.py --check` |
| Check task board | `python scripts/task-board.py --check` |
| Check skills integrity | `python scripts/check-skills.py` |
| Check skill bridges | `python scripts/link-skills.py --check` |
| Check security scan | `python scripts/cso.py --strict` |
| Build / Pack | `python -m build` |

## Phạm vi và ràng buộc

- **Ngoài phạm vi**: Phát triển trực tiếp các tính năng nghiệp vụ end-user không liên quan đến cơ chế tác tử; không chứa cookie/token thực tế hoặc dữ liệu cá nhân của các dự án khác.
- **Ràng buộc kỹ thuật**: Python >= 3.9 (chuẩn hóa trên Python 3.11); tối đa hóa việc sử dụng thư viện chuẩn (standard library) để hạn chế dependency ngoài; tương thích đa nền tảng (Windows PowerShell, Linux Bash, macOS).
- **File dùng chung, chỉ task được chỉ định mới sửa**: `agents/manifest.txt`, `.github/workflows/check.yml`, `scripts/bootstrap-project.py`, `scripts/agent-base-diff.py`, `scripts/verify.py`.
- **File/thư mục cấm agent tự ý sửa**: `AGENTS.md`, `agents/roles/**`, `docs/source/**`, `.env*`, và các file sinh tự động (`GEMINI.md`, `.claude/`, `.kilo/`, `.agents/rules/`).

## Attribution commit (Ghi nhận đóng góp tác tử)

Cấu hình cách ghi nhận đóng góp của AI trong commit message:

| Mục | Cấu hình |
|---|---|
| Chế độ attribution | `co-authored-by` |
| Các giá trị hợp lệ | `co-authored-by` (mặc định: thêm dòng Co-Authored-By theo AGENTS.md), `none` (không thêm bất kỳ trailer AI nào vào commit) |

## Domain & Tri thức cốt lõi

- **Thuật ngữ & Quy trình**: Vòng đời 13 bước, 8 cổng kiểm soát (Gate G0–G7), duyệt bằng file (`agents/protocols/approval.md`), cơ chế `claim_task` và ranh giới trust boundary.
- **Tài liệu tham chiếu**: [docs/CODEMAP.md](docs/CODEMAP.md), [docs/PROJECT-NOTES.md](docs/PROJECT-NOTES.md).

## Có thao tác không hoàn tác được không?

Dự án là khung làm việc không trực tiếp kết nối database sản xuất hoặc dịch vụ trả phí bên ngoài. Các thao tác có nguy cơ mất code/lịch sử (revert, xóa hàng loạt > 10 file, thay đổi file dùng chung của khung) bắt buộc phải tuân thủ cổng rủi ro `agents/protocols/risk-gate.md` và lập phiếu `docs/risk/RK-*.md` trước khi tiến hành.
