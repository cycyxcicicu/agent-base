---
id: T-04
size: large
status: done
owner: ba
epic: E01
phase: GĐ1
outputs:
  - D:/test-repo/m2mba/
branch: feature/04-crawl-m2mba-blog
requirements: [REQ-KG-03]
scope_edit:
  - D:/test-repo/m2mba/**
scope_deny:
  - AGENTS.md
---

# T-04: Khai Thác & Phân Loại Toàn Diện Blog `m2mba.com/blog` (Kèm Ảnh Minh Họa)

## Mục tiêu
Cào toàn bộ danh mục bài viết từ `https://m2mba.com/blog` qua `r.jina.ai`, tải đầy đủ 100% ảnh infographic và sơ đồ tư duy trong từng bài viết. Sau đó, tiến hành phân tích và sàng lọc những bài viết có giá trị tri thức cao, gắn nhãn phân loại theo vai trò (`ba`, `product`, `architect`) để nạp vào bộ não của Agent.

## Tài liệu tham chiếu & Sơ đồ
- **Nguồn bài viết**: `https://m2mba.com/blog`
- **Các nhóm chủ đề trọng điểm**:
  - Business Analysis, Khảo sát nghiệp vụ, bóc tách User Story / Use Case.
  - Product Management, MVP scoping, tư duy thiết kế sản phẩm.
  - Phân tích luồng nghiệp vụ & sơ đồ hóa quy trình doanh nghiệp.

## Contract & Happy Path
- **Đầu ra tại `D:\test-repo\m2mba\`**:
  - `posts/`: Thư mục chứa từng bài blog dưới dạng `<slug>.md` kèm ảnh trong `posts/images/`.
  - `INDEX.md`: Bảng mục lục tổng hợp toàn bộ bài viết, ngày đăng, tác giả và chủ đề chính.
  - `CLASSIFICATION.md`: Bảng đánh giá và phân loại bài học:
    + Bài nào nạp cho vai `ba`: Kỹ thuật phỏng vấn, Domain Glossary, bóc tách BR-xxx.
    + Bài nào nạp cho vai `product`: Định hình tính năng, Plan CEO Review, Roadmapping.
    + Bài nào nạp cho vai `architect`: Phân tích phi chức năng (NFR), ranh giới hệ thống.

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch
- [x] **T-04.1** [Thu thập danh mục bài viết]: Bóc tách toàn bộ link bài viết trên tất cả các trang phân trang của `m2mba.com/blog` lưu vào `D:\test-repo\m2mba\blog_urls.txt` · Assigned: `analyst`.
- [x] **T-04.2** [Cào bài viết & Tải ảnh đính kèm]: Chạy crawler tải toàn bộ bài viết Markdown và tải 100% ảnh infographic, sơ đồ minh họa trong từng bài về `D:\test-repo\m2mba\posts/` · Assigned: `dev`.
- [x] **T-04.3** [Thẩm định & Phân loại Tri thức]: Đọc toàn bộ các bài viết, loại bỏ các bài quảng cáo/sự kiện, chắt lọc bài học nghiệp vụ tinh hoa vào `CLASSIFICATION.md` · Assigned: `ba`.

## Tiêu chí xong
- [x] 100% bài viết blog và ảnh minh họa được lưu trữ offline tại `D:\test-repo\m2mba`.
- [x] Có báo cáo phân loại rõ ràng: Bài nào nạp cho Agent nào để phục vụ công việc thực chiến.
