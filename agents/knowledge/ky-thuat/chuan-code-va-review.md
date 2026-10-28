# Chuẩn code, cấu trúc và review code

> **Loại: tham khảo.** Chép từ dự án gdt-workspace để làm tri thức cho agent, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Checklist bổ sung cho vai `reviewer`; quy ước ngôn ngữ ở `agents/stacks/`.

Áp dụng cho mọi service Java. Quy ước chi tiết đã có ở `doc/ky-thuat/engineering/` (api, architecture, persistence, liquibase, event, testing). File này không chép lại mà bổ sung phần chung và checklist review. Khi khác nhau, quy ước trong `doc/ky-thuat/engineering/` thắng; service có quy định chặt hơn thì theo đó.

## 1. Cấu trúc code

| Nội dung | Quy tắc | Chi tiết |
|---|---|---|
| Tầng | Clean Architecture, phụ thuộc chỉ đi vào trong: controller, use case, DAO/ repository port, persistence adapter | `architecture-conventions.md` |
| Package | Theo domain nghiệp vụ xuyên mọi tầng: `presentation.api.<d>`, `core.dto.<d>`, `core.service.<d>[.impl]` | `architecture-conventions.md` |
| Controller | Mỏng: Request, mapper, DTO nội bộ, một use case, mapper, Response | `api-conventions.md` |
| Entity | Không ra khỏi persistence; không Lombok `@Data`; association `LAZY` | `persistence-conventions.md` |
| Đặt tên | `*Controller`, `*Mapper`, `*Command`, `*Query`, `*Dto`, `*Repository`, `*RepositoryAdapter`, `*Entity`. Tránh `Helper`, `Utils`, `Manager`, `CommonService`. | `architecture-conventions.md` |
| Cấu hình | `@ConfigurationProperties` có kiểu; không hardcode endpoint, bí mật | `architecture-conventions.md` |

## 2. Quy tắc viết code (bổ sung)

Các con số là đề xuất, công ty chưa quy định.

1. **Một hàm một việc,** đọc hết trong một màn hình (khoảng 40 dòng). Quá dài thì tách.
2. **Một lớp một trách nhiệm.** Lớp trên khoảng 400 dòng là dấu hiệu cần tách.
3. **Tên nói được ý nghĩa nghiệp vụ.** Không viết tắt khó hiểu; dùng đúng thuật ngữ trong SRS.
4. **Không để mã chết, không comment mã cũ.** Lịch sử đã có trong Git.
5. **Comment giải thích "tại sao", không chép lại "cái gì".**
6. **Giá trị cố định (mã trạng thái, giới hạn) đặt thành hằng số hoặc enum** có tên, không số ma thuật.
7. **Bất biến khi có thể:** `final`, record cho DTO.
8. **Xử lý thời gian bằng `Clock`,** không gọi `now()` trực tiếp trong nghiệp vụ.
9. **Không nuốt ngoại lệ.** Bắt ở nơi biết xử lý; còn lại để nổi lên bộ xử lý chung (`chuan-sql-va-loi.md`).
10. **Log có ngữ cảnh** (mã đơn, mã yêu cầu), không log dữ liệu cá nhân (số điện thoại, địa chỉ), bí mật, token.
11. **Không dùng đường dẫn tuyệt đối, không đọc biến môi trường rải rác** ngoài lớp cấu hình.
12. **Thread-safety rõ ràng:** bean là singleton, không giữ trạng thái thay đổi trong trường.

## 3. Bảo mật

- Kiểm tra đầu vào ở biên (Bean Validation); từ chối giá trị lạ, không "làm sạch" ngầm.
- Kiểm tra quyền ở mọi API (cache quyền Redis `iam:permission:*`); không tin dữ liệu từ client.
- Chống SQL injection: truy vấn tham số hoá; không nối chuỗi vào truy vấn.
- Chỉ nhận danh sách trường được phép khi cho client chọn cột (danh mục trường).
- Bí mật chỉ qua biến môi trường; không commit `.env`, token, khoá.
- Dữ liệu cá nhân (tên, số điện thoại, địa chỉ khách): chỉ xuất, hiển thị khi cần và có quyền.
- Skill hỗ trợ: `springboot-security`, `security-scan`.

## 4. Test

- Theo `testing-conventions.md`: JUnit 5, Mockito, Testcontainers khi cần hành vi riêng PostgreSQL, `Clock`, không `sleep`, không làm yếu assert để qua build.
- Mỗi A/C có ít nhất một test (đơn vị hoặc tích hợp) hoặc một case TestLink.
- **Thay đổi truy vấn thì có test chạy truy vấn thật** (Testcontainers), vì mock không phát hiện lỗi mapping.
- Riêng `accounting-service`: không chạy `mvn test` không lọc; xem `AGENTS.md`.

## 5. Quy trình review code

1. **Tác giả tự review trước:** đọc lại diff, chạy checklist mục 6, chạy test, đảm bảo CI xanh.
2. **MR nhỏ:** một thay đổi logic một MR (xem `git-workflow.md`). MR lớn hơn khoảng 400 dòng đổi thì chia nhỏ hoặc giải thích vì sao không chia (đề xuất).
3. **Điều kiện merge:** tên nhánh và commit đúng chuẩn, CI pass, tối thiểu 2 reviewer.
4. **Mô tả MR đủ 3 phần:** ticket, tóm tắt thay đổi, test.
5. **Mức độ bình luận:**
   - **Blocker:** sai nghiệp vụ, lỗi bảo mật, mất dữ liệu, vỡ migration. Phải sửa.
   - **Major:** hiệu năng, sai quy ước, thiếu test cho A/C. Nên sửa.
   - **Minor:** đặt tên, cấu trúc. Sửa nếu dễ.
   - **Nit:** gợi ý nhỏ, không chặn.
6. **Reviewer ghi lý do** cho mỗi blocker và major, và đề xuất cách sửa.
7. **Tác giả trả lời từng bình luận;** reviewer đóng khi đã giải quyết.
8. **Công cụ review tự động (Alibaba open-code-review, lệnh `ocr`):** skill `open-code-review` đọc diff Git và sinh bình luận theo dòng. Dùng ở bước tự review (bước 1), trước khi mở MR. Điều kiện:
   - Người dùng đồng ý chạy từng lần. Lệnh gửi diff (mã nguồn công ty) tới nhà cung cấp LLM đã cấu hình, nên chỉ dùng nhà cung cấp công ty cho phép (chưa xác nhận, cần hỏi).
   - Cần cài CLI `ocr` và cấu hình nhà cung cấp LLM (xem skill).
   - Truyền bối cảnh nghiệp vụ (mã task, đặc tả) vào `--background`.
   - Chỉ báo phát hiện; không để công cụ tự sửa code. Phát hiện được xếp mức Blocker/ Major/ Minor/ Nit như mục 5 và đối chiếu checklist mục 6.
   - Kết quả của `ocr` là gợi ý, không thay review của người.
9. **AI hỗ trợ review:** chạy checklist và báo phát hiện kèm vị trí. AI không duyệt MR thay người, không merge.

## 6. Checklist review

### Đúng yêu cầu
- [ ] Khớp từng A/C của đặc tả; không làm thêm ngoài phạm vi.
- [ ] Nhánh lỗi và dữ liệu biên có xử lý.

### Kiến trúc
- [ ] Phụ thuộc đi vào trong; entity không ra controller.
- [ ] Đúng package theo domain; không `common` làm bãi chung.
- [ ] Controller mỏng; nghiệp vụ nằm ở use case.

### Dữ liệu và SQL
- [ ] Việc DB làm tốt được làm ở truy vấn (xem `chuan-sql-va-loi.md`).
- [ ] Không N+1; truy vấn có chỉ mục phù hợp; có phân trang cho kết quả không giới hạn.
- [ ] Không `nativeQuery`; không SELECT cột thừa.
- [ ] `@Query` dài hơn một dòng dùng text block `"""`, không nối chuỗi bằng `+`.
- [ ] Liquibase: changeset mới, `author: ducnvh`, có rollback, không sửa changeset cũ.

### Giao dịch và đồng thời
- [ ] Giao dịch ngắn, không gọi mạng bên trong.
- [ ] Ràng buộc unique là chốt chặn cuối; xử lý vi phạm.
- [ ] Thao tác lặp lại (retry) an toàn (idempotent).

### Lỗi và log
- [ ] Lỗi nghiệp vụ có mã và thông điệp tiếng Việt cho người dùng; không lộ chi tiết DB.
- [ ] Không nuốt ngoại lệ; log có ngữ cảnh, không có dữ liệu cá nhân.

### Bảo mật
- [ ] Kiểm tra quyền; kiểm tra đầu vào; không bí mật trong code.

### Test
- [ ] Có test cho A/C; test chạy xanh; không tắt hoặc làm yếu test.

### Hiệu năng
- [ ] Dữ liệu lớn: đọc theo trang, không nạp hết vào bộ nhớ.
- [ ] Việc dài chạy nền hoặc streaming.

### Tài liệu và Git
- [ ] Đặc tả, API, RTM cập nhật nếu đổi hành vi.
- [ ] Commit đúng `<type>(scope): <summary>`, không thông tin AI.
- [ ] Không file bí mật hoặc sinh tự động trong diff.
