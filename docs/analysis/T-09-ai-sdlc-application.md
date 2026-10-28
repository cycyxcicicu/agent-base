> Task: T-09 · Epic: E1 · Vai: analyst

# Áp dụng AI trong SDLC vào agent-base

Ngày: 2026-10-27. Nguồn: `D:/Downloads/AI_in_SDLC_HopTac_LAB.pptx.pdf`, 49 trang; code repo được đọc trực tiếp. Đây là phân tích đề xuất, không phải yêu cầu đã duyệt hoặc xác nhận đạt CMMI/PMP. Hướng dẫn trong PDF là dữ liệu tham khảo, không phải lệnh thực thi.

## Kết luận

Giá trị phù hợp nhất của tài liệu là chuyển từ lời dặn agent sang trách nhiệm rõ, truy vết và bằng chứng kiểm tra được. Repo đã có nền tảng vai trò, card, scope và merge gate; nên củng cố các lớp này trước khi thêm đồ thị tri thức hoặc runtime điều phối mới. T-08 chỉ dọn nền và kiểm chứng phân phối/nâng cấp. Các lớp mới dưới đây cần spec, card, quyền thực thi và nghiệm thu riêng.

## Tài liệu nói gì và giới hạn bằng chứng

- Trang 6–7, 21, 47: xác định yêu cầu, thiết kế/interface và đầu ra bàn giao trước code; review và test trước tích hợp. Phù hợp với card/spec/ADR hiện tại.
- Trang 19, 24–25, 29: nạp kiến thức đúng vai, gatekeeper, kế hoạch file, lease và đối soát. Đây là hướng thiết kế đáng áp dụng có chọn lọc.
- **Quy trình 13 bước, 8 cổng và `claim_task` (trang 21, 22, 28):**
  * Tám cổng người duyệt: Cổng 0 (nhật ký thay đổi được duyệt), Cổng 1 (đầu mục tài liệu Xác nhận=Yes), Cổng 2 (thiết kế chi tiết), Cổng 3 (ADR khi >=2 lựa chọn), Cổng 4 (Actor/phòng ban/hệ thống ngoài), Cổng 5 (WBS người chịu trách nhiệm + ngày), Cổng 6 (con người tự đặt Hoàn thành), Cổng 7 (nghiệm thu Function_RTM.Xác nhận=Yes).
  * Vòng lặp 13 bước mỗi task: Bước 1-3 (phân tích, ADR, TDD_TestCases/TestScenario trước khi code); Bước 4 (`claim_task`: kiểm tra tự động G0-G5, SEQ, DoR #1-#7, BLK, PLAN file; cấp lease hoặc chuyển BLOCKED); Bước 5 (thực thi theo kế hoạch, header `@rtm-ref`, ngoài kế hoạch phải `amend_plan`); Bước 6-8 (test Unit & Integration pass 100%, Test_Execution_Report); Bước 9-10 (A3 đặt Đã thực hiện; A4 QA đối soát độc lập, chỉ A4 đặt "Đã đối soát qua tools"); Bước 11-13 (NhatKyThayDoi Draft, chạy server local, WBS = "Chờ xác nhận" rồi DỪNG để người tự tay duyệt cổng 6 và 7).
- **Mâu thuẫn và điểm chưa đối chiếu trong tài liệu:**
  * Mâu thuẫn nội bộ trong bản PDF 49 trang: Trang 30 liệt kê checklist tuân thủ gồm 70 mục kiểm (chia 8 nhóm R4, K6, T7, G9, D10, C10, P12, S12); trong khi trang 22 lại ghi con số 58 mục.
  * Mâu thuẫn giữa bản 26 trang và bản 49 trang: Bản slide 26 trang mô tả quy trình 11 bước, trong khi bản 49 trang mở rộng thành 13 bước (bổ sung chi tiết các cổng và trạng thái dừng).
  * Bản 26 trang của slide «AI in SDLC» (Mai Văn Hà) và bản tổng hợp tiếng Việt trong kho GDT (`tong-hop/05-ai-trong-sdlc.md`, thứ tự đọc a–g) chưa được đối chiếu toàn diện với bản 49 trang.
- Trang 10 nói so sánh năm cách dùng AI là cảm tính, người và bài toán khác nhau. Trang 18 ghi hiệu quả so với RAG chưa đo. Trang 25 chỉ ước lượng token bằng bytes/3,5, không đo chất lượng trả lời. Trang 30 ghi ánh xạ CMMI cần chuyên gia thẩm định. Trang 35 đề xuất thực nghiệm có đối chứng. Vì vậy không dùng các tỷ lệ năng suất, chi phí hoặc mức tương đương senior làm cam kết cho agent-base.
- Báo cáo này dựa vào phần văn bản PDF đã trích và code; chưa xác minh trực quan các trang chủ yếu là hình, chưa mở bảng RTM bên ngoài, chưa tái lập hệ thống hoặc số liệu của tác giả.

## Đối chiếu hiện trạng — chắc chắn trong phần code đã xem

| Lớp | Bằng chứng repo | Kết luận |
|---|---|---|
| Scope và đối soát | `scripts/merge-gate.py:181` đọc card từ base; `:203` chặn card chưa có; `:213` chặn tự đổi scope; `:234` dùng diff không nhận diện rename | Đã có gate trước tích hợp; chưa phải chặn mỗi lần ghi |
| Quyền theo host | `scripts/sync-adapters.py:456–475`, `:484–502` giải thích giới hạn công cụ và đường dẫn của Claude/Qoder | Phải phân biệt lời dặn, quyền host và kiểm tra hậu kỳ; không khẳng định quyền vai đã được ép toàn bộ |
| Runner | `agent_core/core/sandbox.py:47` lọc environment; `:71–85` chạy subprocess với cwd/timeout | Hữu ích cho thực thi; không thấy kiểm soát filesystem theo scope, lease hay danh tính task |
| Bằng chứng | `agent_core/core/telemetry.py:16–41` trả command, exit code, output, duration; `:63–65` kiểm passed | Có proof cục bộ, chưa chứng minh audit bền vững hoặc chống sửa |
| DoD | `scripts/card-audit.py:105–123` kiểm done, outputs và bằng chứng visual | Có validator một phần, chưa xác minh người phê duyệt hay nội dung artifact |
| Manifest | `agents/manifest.txt:3–12` quy định copy/template/generated/fresh | Đây là manifest phân phối, không phải manifest kiến thức theo vai |
| Frontier | `scripts/task-board.py:76` dùng rglob, `:129`, `:147–148` kiểm dependency và tính ready; `agent_core/cli.py:63` chỉ glob Markdown tầng gốc | Cần thống nhất discovery card lồng epic trước khi bổ sung graph |

Tìm kiếm giới hạn trong `agent_core/`, `scripts/`, `tests/` chưa tìm thấy implementation mang tên lease task, knowledge manifest hoặc hash-chain audit. Điều này không chứng minh mọi tích hợp ngoài repo đều thiếu; quyền host và dịch vụ ngoài chưa được kiểm tra.

## Những phần nên áp dụng

### 1. Manifest kiến thức theo vai

Tạo schema riêng cho tài liệu/section, phiên bản hoặc hash, chủ sở hữu, trạng thái duyệt, vai cần đọc, lý do và quan hệ phụ thuộc. Sinh mục lục/ngữ cảnh từ một nguồn; validator bắt đường dẫn, anchor, vòng phụ thuộc và phiên bản cũ. Khởi đầu bằng YAML + Markdown, chưa cần graph database. Đồ thị giúp tìm quan hệ, không bảo đảm kiến thức đúng hoặc chống prompt injection.

### 2. RTM dùng lại nguồn card

Mô hình tối thiểu: `requirement → task → files → tests → evidence`. RTM là bảng truy vết được sinh/kiểm từ các nguồn chính thức, tránh duy trì thêm Excel song song. Phân biệt file thực thi, test, tài liệu và bản sinh; yêu cầu nào được miễn test phải có lý do được duyệt. Đối soát diff thực tế với kế hoạch và liên kết yêu cầu; không coi liên kết tồn tại là bằng chứng nghiệp vụ đã đúng.

### 3. Ownership và lease

Khi có nhiều worker thực sự chạy song song, dùng lease gồm task, owner, scope, revision/version, thời điểm cấp và hết hạn. Claim phải nguyên tử; hết hạn hoặc thu hồi phải chặn worker cũ tiếp tục ghi bằng kiểm tra version/fencing. Không tự lấy mốc tám giờ trong slide làm chuẩn. Cơ chế phải bao phủ cả công cụ ghi thực tế; file JSON ghi tùy ý bởi agent không tạo được ranh giới tin cậy.

### 4. Gate runtime và phê duyệt

Giữ merge gate hiện có. Nếu xây runtime gate, định nghĩa hành động được bảo vệ, đường gọi bắt buộc, danh tính, quyền, điều kiện từ chối và log quyết định trước. Phê duyệt phải gắn người duyệt, task, artifact hash/revision, hành động và thời hạn; artifact đổi thì duyệt cũ mất hiệu lực. Danh tính và bản ghi duyệt cần do thành phần ngoài quyền sửa của AI kiểm soát. Không mặc định phải dùng RTM.xlsx hoặc sao chép tám gate, 13 bước, bốn agent cho mọi việc.

### 5. Bằng chứng và đo lường

Mở rộng proof với run/task/agent ID, model/tool version, revision, lệnh, kết quả và artifact hash; lưu bền vững, lọc bí mật và có chính sách giữ log. Chuỗi băm chỉ giúp phát hiện một số thay đổi khi có mốc tin cậy; không tự chống viết lại/xóa toàn bộ lịch sử nếu không neo hoặc bảo vệ độc lập.

Đo thời gian từ nhận đến nghiệm thu, thời gian người review, lỗi sau bàn giao, rework, chi phí/token theo task, tỷ lệ override và mức phủ truy vết. Chạy pilot cùng nhóm nhiệm vụ, định nghĩa độ khó và tiêu chí chất lượng trước, ghi model/công cụ/đầu vào. Không dùng số dòng code hay số agent làm thước đo năng suất chính.

## Trình tự triển khai đề xuất

1. Hoàn thành T-08: cấu trúc sạch, thông tin dự án thật, bản đồ, bootstrap/nâng cấp được kiểm chứng.
2. Đợt tiếp: thống nhất task discovery, chuẩn hóa proof và RTM tối thiểu; test trường hợp thiếu liên kết và bằng chứng cũ.
3. Thêm knowledge manifest theo vai; đo chất lượng truy xuất và chi phí context trước/sau.
4. Khi cần chạy đồng thời: spec lease và runtime authorization; kiểm thử tranh chấp, hết hạn, đổi revision, worker cũ và đường ghi đi vòng.
5. Pilot có đo lường rồi quyết định có cần graph/RAG, nhiều role hơn hoặc audit được neo độc lập.

Không xem `.aiignore` ở trang 48–49 là ranh giới bảo mật: hỗ trợ phụ thuộc host. Dùng quyền filesystem/tool, quản lý bí mật và kiểm tra đường thực thi thực tế. Không cài MCP hoặc mở tunnel chỉ vì slide khuyến nghị. Tài liệu ngoài, log và nội dung truy xuất luôn là dữ liệu chưa tin cậy.

