# Xử lý bug: nhận danh sách, gom nhóm, tái hiện, sửa

> **Loại: tham khảo.** Chép từ dự án gdt-workspace để làm tri thức cho agent, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Bổ sung cho `protocols/bug-repro.md` (xử lý từng bug). Còn nhắc TestLink, Mantis và `doc/` là quy ước của gdt.

Áp dụng khi người dùng đưa danh sách bug (CSV hoặc ảnh chụp Mantis) hoặc nhiều mã bug cùng lúc. Một bug lẻ đi từ mục 6.
Cách làm sửa bug (tái hiện lỗi, viết case bao phủ lỗi trước, rồi mới sửa) là cách người dùng đã học từ Lauren Tan. Nội dung dưới đây theo mô tả của người dùng; workspace chưa có tài liệu gốc để đối chiếu.
Tên branch, commit, MR theo `git-workflow.md` mục 2, 3, 5. Không chép lại ở đây.

## 1. Nhận danh sách: chỉ lọc, gom, báo cáo
- Chưa tạo worktree, chưa sửa code, chưa commit.
- Lưu bản CSV người dùng đưa vào `doc/bug/mantis/mantis-<dự án>-<ngày xuất>.csv` (thêm file mới, không ghi đè bản cũ). So với bản cũ và với `doc/bug/theo-doi-bug-mantis.md`: báo bug đã làm mà Mantis chưa đóng, bug mới, bug đổi người gán, bug bị mở lại. Làm xong nhóm nào thì ghi vào file theo dõi (nhánh, merge commit); AI không đổi trạng thái Mantis.
- Lọc theo cột Assigned To: của người dùng; chưa gán; của người khác (chỉ báo trùng, không đụng); đã xong (resolved và fixed).
- Task đang `feedback` hoặc cần chốt nghiệp vụ thì để riêng, không nhận.
- CSV chỉ có tiêu đề. Chưa đọc mô tả trên Mantis thì ghi rõ là "chỉ đọc tiêu đề".
- Kiểm tra trên code (`origin/develop` mới nhất) xem bug nào **đã được sửa sẵn**: tìm commit, test và hành vi hiện tại. Kết quả báo theo mục 3, không tự coi là xong.

## 2. Gom nhóm và xếp ưu tiên
**Gom:** các bug cùng chủ đề (cùng màn, hoặc cùng thành phần code dùng chung) vào một branch. Tên branch dùng `feature/<ticket>-<mô-tả>` cho cả sửa lỗi lẫn tính năng nhỏ: hook GitLab của công ty chỉ nhận `main`, `develop`, `release/*`, `feature/*`, `fix/*`, `hotfix/*` và **từ chối push `bugfix/*`** (kiểm chứng 27/10/2026). `fix/*` dành cho sửa lỗi trên release. Nhóm quá lớn (trên 7 task hoặc trên 1 tuần) thì tách. Thiếu số ticket thì hỏi, đừng bịa.

**Ưu tiên, theo thứ tự:**
1. Severity `block` hoặc `crash`, hoặc Priority `urgent` và `immediate`.
2. Đã `reopened` mà còn high: lần sửa trước chưa hết nên rủi ro cao.
3. Bug chặn người khác hoặc chặn QA test tiếp.
4. Nhóm làm nhanh mà xử lý được nhiều bug một lượt.
5. Cuối cùng: nhóm cần thiết kế, chờ phản hồi, cần chốt nghiệp vụ. Nếu nhóm đó có mức cao thì bắt đầu phân tích sớm, chưa code.

Hai tiêu chí xung đột thì nêu rõ và để người dùng quyết.

## 3. Báo cáo cho người dùng
Mỗi nhóm có: branch đề xuất; các task; repo đụng tới; căn cứ (đã đọc code nào, hay chỉ đọc tiêu đề); ước lượng (đề xuất, người làm chốt); trùng việc người khác; khả năng không phải bug (theo thiết kế, theo SRS); câu hỏi mở; thứ tự ưu tiên kèm lý do.
Cách gom có nhiều lựa chọn thì đưa 3 phương án, một khuyến nghị (mẫu ở `quy-trinh-tong-the.md` mục 6).

### Bug đã xử lý sẵn
Bug đã có commit sửa trên `develop` (thường vì báo trước ngày sửa) thì **không sửa code lại**. Báo thành một mục riêng, mỗi bug ghi:
- Bằng chứng: hash commit và ngày, file và hàm, test đang có.
- Mức chắc chắn, ghi đúng một trong hai: "chỉ đọc code" hoặc "đã chạy thử trên dev".
- Việc cần người làm: QA test lại, rồi **người dùng tự đổi trạng thái trên Mantis** (AI không có quyền và không tự kết luận đã xong).
- Phần còn hở nếu có (ví dụ yêu cầu rộng hơn những gì commit làm).

## 4. Người dùng chọn
Người dùng quyết task nào là bug thật của mình. Chỉ làm những task đó.

## 5. Worktree (chỉ khi người dùng bảo)
Dùng khi cần làm bug song song trong lúc việc đang dở ở thư mục chính.
- Chạy `git status` ở repo chính (chỉ xem), rồi `git fetch origin`.
- Tạo từ `origin/develop` mới nhất, branch mới theo chuẩn tên: `git worktree add -b <branch> <đường dẫn> origin/develop`.
- Đường dẫn nằm ngoài thư mục đang làm, không lồng. Cần nhiều repo đồng bộ thì dựng thư mục song song `gdt-workspace-<mã>/` cùng cấu trúc; repo nào chưa cần commit thì để detached tại `origin/develop`.
- Không đụng thay đổi chưa commit ở thư mục chính. Không commit, không push.
- File ignore (`.env*`, `target/`, `node_modules/`) không có trong worktree. Người dùng tự tạo `.env`, AI không đọc và không copy file bí mật.
- Chạy thử một bản tại một thời điểm: trùng port, DB dev, Redis, RabbitMQ. Buộc chạy hai bản thì bản thứ hai dùng `--server.port` khác và tắt đăng ký Eureka (chưa kiểm chứng, xem log để xác nhận).
- `ws-bom`, `ws-library`, `ws-sdk` cài vào `~/.m2` dùng chung. Đổi task thì `mvn install` lại các thư viện đó nếu bản đang chạy phụ thuộc.
- Xong thì xoá: `git worktree remove <đường dẫn>` (không `rm -rf`), rồi `git branch -d` sau khi MR đã merge.

## 6. Mỗi nhóm: tái hiện, soát tác động, viết case TestLink, rồi mới sửa
Thứ tự bắt buộc. Chưa xong bước nào thì chưa sang bước sau.

1. **Đọc đủ mô tả trên Mantis** và các bước tái hiện. Bug `reopened`: đọc ghi chú và `git log` của lần sửa trước để biết vì sao chưa hết.
2. **Tái hiện lỗi trên code hiện tại** (`develop`, worktree sạch). Ghi branch và commit hash, bước làm, dữ liệu, kết quả thực tế so với mong đợi, bằng chứng (log, ảnh, test đỏ).
   - Không tái hiện được: tra `git log` xem đã có commit sửa chưa. Có thì xếp vào "Bug đã xử lý sẵn" (mục 3). Không có thì dừng, báo người dùng, không sửa mò; hỏi lại người báo hoặc chuyển `feedback`.
   - Lỗi do dữ liệu hoặc cấu hình: báo, không sửa code.
3. **Soát tác động trước khi sửa.** Tìm mọi nơi dùng chung phần định sửa (component, hàm, enum, API, bảng, quyền, dữ liệu cũ). Liệt kê màn và chức năng bị ảnh hưởng; danh sách này đưa vào case hồi quy ở bước 4. Phạm vi lan ra ngoài nhóm hoặc đụng việc người khác thì dừng và hỏi. Phải đổi nghiệp vụ hoặc cần thiết kế thì chuyển sang lối "Vừa" trong `quy-trinh-tong-the.md`.
4. **Viết happy case trên TestLink trước khi code.** Sau khi tái hiện lỗi và soát tác động, viết bộ happy case thành file XML import TestLink, theo `qa-process.md` mục 2 và 6b (một bước một hành động, kết quả quan sát được, ngôn ngữ giao diện, chữ lấy từ code và bản dịch thật). **Chưa viết xong case thì chưa được sửa code.** Không viết case sau khi code.
   - **Keyword** của case là mã Mantis của bug mà case kiểm tra. Thiếu mã thì hỏi.
   - **Bao phủ chuẩn chỉ:** mỗi bug có ít nhất một case có bước mà code hiện tại cho kết quả sai (bằng chứng tái hiện). Mỗi màn, mỗi đối tượng mà bug nêu có bước riêng, không viết gộp "các màn". Có đủ vai trò, dữ liệu, ngôn ngữ (vi, và en nếu đổi bản dịch), cỡ cửa sổ nếu là lỗi giao diện. Bước soát tác động ở mục 3 có case hồi quy. Phần tester không làm được bằng tay thì nói rõ và kiểm bằng cách khác.
   - **Đỏ trước:** chạy case trên code hiện tại (`develop`) và ghi bước nào cho kết quả sai. Không chạy được (ví dụ chưa đăng nhập được) thì ghi "chưa chạy trên code cũ" và nhờ người dùng chạy; không tự ghi Passed hay Failed.
   - **Cổng:** báo người dùng danh sách case và độ phủ từng bug; được người dùng duyệt mới sang bước 5.
5. **Test tự động bổ sung (nếu repo có hạ tầng):** viết trước khi sửa, chạy và thấy **fail đúng lý do**. Không fail nghĩa là chưa bao phủ lỗi. Test tự động bổ sung cho case TestLink, không thay thế.
6. **Sửa tối thiểu, đúng nguyên nhân gốc.** Không refactor lan. Theo `ky-thuat/chuan-code-va-review.md` và `ky-thuat/chuan-sql-va-loi.md`.
7. **Chạy lại:** từng bước của case ở bước 4 phải cho kết quả đúng; test cũ liên quan; case hồi quy cho từng màn đã liệt kê ở bước 3. Với accounting-service theo cảnh báo trong `AGENTS.md`: không `mvn test` không lọc, không `spotless:apply` toàn repo, test Testcontainers cần Docker.
8. **Tự review diff:** chỉ chứa thay đổi của bug; không file bí mật; Liquibase `author: ducnvh` và không sửa changeset cũ.
9. **Cập nhật tài liệu** nếu hành vi đổi, và file tiến độ trong `doc/tien-do/`.

## 7. Báo cáo kết quả, commit, MR
- Báo từng nhóm: đã tái hiện (bằng chứng), case TestLink đã viết **trước khi code** (đường dẫn file XML, kết quả chạy trên code cũ), sửa gì, tác động đã soát, đã chạy gì và kết quả, **chưa kiểm chứng gì**. Nếu thứ tự bị đảo (code trước, case sau) thì nói thẳng.
- Mỗi bug một commit, đúng `<type>(scope): <summary>`. Commit, push, tạo MR chỉ khi người dùng nói rõ.
- Mô tả MR đủ 3 phần (ticket, tóm tắt, test); liệt kê link Mantis của từng bug trong nhóm.
- AI không có quyền đổi trạng thái Mantis. Người dùng tự cập nhật.
