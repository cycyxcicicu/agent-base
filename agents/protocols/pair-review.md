# Review theo cặp (Solution-Pair và Code-Review-Pair)

Nguồn: quy trình công ty (`quy-trinh-cong-ty.md` mục 1). Mỗi sản phẩm quan trọng có **hai cặp mắt độc lập** trước khi đi tiếp. Người tạo và người soát phải là hai vai (hai agent) khác nhau.

## Hai cặp

| Cặp | Soát cái gì | Người tạo | Người soát | Ra khỏi cặp khi |
|---|---|---|---|---|
| **Solution-Pair** | spec, thiết kế, ADR, chia task | architect (hoặc product, ba) | reviewer hoặc một architect khác | Checklist thiết kế đạt, verdict ghi vào tài liệu |
| **Code-Review-Pair** | diff, test, ghi chú bàn giao | dev | reviewer | Đạt 5 rubric của reviewer, test xanh |

Việc nhỏ (cỡ "nhỏ" theo `AGENTS.md` mục 2) chỉ cần Code-Review-Pair; việc lớn cần cả hai.

## Quy tắc

1. Người soát đọc **diff và tài liệu**, không nghe người tạo thuyết trình. Câu hỏi đầu tiên: "lỗi nào còn sót ở đây?".
2. Verdict (Đạt, Đạt có điều kiện, Trả lại) và lý do ghi vào task card hoặc tài liệu, kèm ngày. Verdict chỉ là tư vấn; `Approved` vẫn do con người (xem `approval.md`).
3. Trả lại thì người tạo sửa, không tự đóng; người soát soát lại phần đã sửa.
4. Soát **sớm**: lỗi tìm ở khâu thiết kế rẻ hơn nhiều lần so với khâu test.
5. Một vai không tự soát sản phẩm của chính mình, kể cả khi chạy trong cùng phiên.
