# Mục tra cứu sơ đồ: khái niệm, cách xây dựng, ảnh mẫu, công cụ

**Loại: tham khảo.** Là trang ĐẦU VÀO để tra cứu mọi thứ về sơ đồ trong kho tri thức. Bản này thay bản cũ cùng tên (bản cũ còn ghi luật "một điểm kết thúc, nhánh lỗi đỏ", đường dẫn gõ sai `ssets/`, số ảnh 392).
> **Nguồn đối chuẩn:** uml-diagrams.org và SourceMaking (đã tải về `assets/`, tiếng Anh). AI đọc thẳng bản tiếng Anh, KHÔNG cần dịch; chỉ phần tài liệu dự án viết bằng tiếng Việt.
> **Khi khác nhau thì theo chuẩn dự án:** `quy-trinh-ve-so-do-bang-json.md` (mục 0 là bảng tra công cụ), `AGENTS.md` mục 21. Tài liệu UML chung chỉ để hiểu nghĩa ký hiệu.

**Ma trận mọi loại sơ đồ (đã có công cụ, chưa có, vì sao): `agents/knowledge/diagrams/ma-tran-loai-so-do.md`.**

**Mẫu phân tích và khung JSON cho từng loại (đọc sau khi hiểu khái niệm):** `agents/knowledge/diagrams/mau-phan-tich/`.

**Mẫu vàng một UC đủ năm sơ đồ để bắt chước:** `doc/features/UC-04-advanced-filter/hinh/*.spec.json` (danh sách ở mục 0 của `quy-trinh-ve-so-do-bang-json.md`).

## 1. Ba cách tra
1. **Đọc thẳng file** theo bảng mục 2 (khái niệm và cách xây dựng nằm ở hai cột riêng, bắt đầu từ `spec.md` của loại).
2. **Tra ảnh mẫu:** `python3 scripts/knowledge.py image -q "<từ khóa>"` (718 ảnh có chú thích, 551 ảnh cốt lõi, 28 loại; có đường dẫn nhúng sẵn). Ví dụ: `"use case include"`, `"sequence alt"`, `"binary association"`, `"activity fork"`.
3. **Tra một mục cụ thể:** `python3 scripts/knowledge.py section --file <tệp> --heading "<tiêu đề mục>"`; tra tổng quát: `python3 scripts/knowledge.py query -q "<chủ đề>"`.

Thứ tự đọc khi chuẩn bị vẽ một loại: (1) hàng của loại đó trong mục 2; (2) bài "Constructing …" của SourceMaking để biết cách đi từ yêu cầu tới phần tử; (3) `spec.md` để hiểu nghĩa từng ký hiệu; (4) ảnh mẫu; (5) mục 4.x của `quy-trinh-ve-so-do-bang-json.md` để biết chuẩn dự án và lệnh vẽ. Bản tóm tắt tiếng Việt về cách phân tích: `agents/knowledge/srs/sourcemaking-uml-case-study.md` và `agents/knowledge/quy-trinh/ba-business-analysis-mastery.md` (mục 2 đến 4: state machine, use case khác user story, luồng rẽ nhánh khác luồng ngoại lệ).

## 2. Từng loại sơ đồ

### Use case
- **Trả lời câu hỏi:** Ai (bên ngoài) dùng hệ thống để đạt giá trị gì.
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/use-case-diagram/spec.md`; `use-case.md`; `actor.md`; `how-to.md` (cách vẽ 4 bước); `subject.md` (ranh giới hệ thống); `actor-association.md`; `include.md`; `extend.md` (có bảng so sánh include, extend, generalization), cùng thư mục `assets/uml/use-case-diagram/`.
- **Cách xây dựng sơ đồ từ yêu cầu và phân tích** (SourceMaking, tiếng Anh, có ví dụ làm từng bước): `assets/sourcemaking-uml/pages/modeling-business-systems/use-case-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-business-systems/constructing-use-case-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/use-case-diagram/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/constructing-the-external-view/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/use-case-sequence-diagram/README.md`.
- **Ảnh mẫu:** 27 ảnh uml-diagrams.org + 37 ảnh SourceMaking, loại `use-case-diagram`: `python3 scripts/knowledge.py image -q "use <từ khóa>"`.
- **Công cụ và mẫu của dự án:** `usecase` (use case: mục 4.10 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/use-case-diagram/template.png` nếu có).

### Activity (hoạt động)
- **Trả lời câu hỏi:** Việc diễn ra theo thứ tự nào, ai hoặc lớp nào làm, rẽ nhánh ở đâu.
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/activity-diagram/spec.md`; `assets/uml/activity-diagram/actions.md`; `assets/uml/activity-diagram/controls.md`; `assets/uml/activity-diagram/objects.md`.
- **Cách xây dựng sơ đồ từ yêu cầu và phân tích** (SourceMaking, tiếng Anh, có ví dụ làm từng bước): `assets/sourcemaking-uml/pages/modeling-business-systems/activity-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-business-systems/constructing-activity-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-for-system-integration/activity-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-for-system-integration/constructing-diagrams-in-the-process-view/README.md`.
- **Ảnh mẫu:** 57 ảnh uml-diagrams.org + 34 ảnh SourceMaking, loại `activity-diagram`: `python3 scripts/knowledge.py image -q "activity <từ khóa>"`.
- **Công cụ và mẫu của dự án:** `activity` (làn theo lớp); cũ: `flow`, `swimlane` (mục 4.6, 4.9 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/activity-diagram/template.png` nếu có).

### Class
- **Trả lời câu hỏi:** Hệ thống gồm những kiểu (lớp) nào, liên hệ cấu trúc ra sao.
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/class-diagram/spec.md`; `assets/uml/class-diagram/classifier.md`; `assets/uml/class-diagram/association.md`; `assets/uml/class-diagram/generalization.md`; `assets/uml/class-diagram/dependency.md`; `assets/uml/class-diagram/interface.md`; `assets/uml/class-diagram/multiplicity.md`.
- **Cách xây dựng sơ đồ từ yêu cầu và phân tích** (SourceMaking, tiếng Anh, có ví dụ làm từng bước): `assets/sourcemaking-uml/pages/modeling-it-systems/class-diagram/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/constructing-class-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/objects-and-classes/README.md`; `assets/sourcemaking-uml/pages/modeling-business-systems/class-diagram/README.md`; `assets/sourcemaking-uml/pages/modeling-business-systems/constructing-class-diagrams/README.md`.
- **Ảnh mẫu:** 61 ảnh uml-diagrams.org + 45 ảnh SourceMaking, loại `class-diagram`: `python3 scripts/knowledge.py image -q "class <từ khóa>"`.
- **Công cụ và mẫu của dự án:** `class` (mục 4.1, 4.9 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/class-diagram/template.png` nếu có).

### Sequence (tuần tự)
- **Trả lời câu hỏi:** Theo thời gian, ai gọi ai, thông điệp gì, trả về gì.
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/sequence-diagram/spec.md`; `messages.md` (đồng bộ, bất đồng bộ, reply, create, delete); `fragments.md` (alt, opt, loop, par...); `interaction.md`; `examples.md`, cùng thư mục `assets/uml/sequence-diagram/`.
- **Cách xây dựng sơ đồ từ yêu cầu và phân tích** (SourceMaking, tiếng Anh, có ví dụ làm từng bước): `assets/sourcemaking-uml/pages/modeling-it-systems/sequence-diagram/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/constructing-sequence-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/use-case-sequence-diagram/README.md`; `assets/sourcemaking-uml/pages/modeling-business-systems/sequence-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-business-systems/constructing-sequence-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-business-systems/high-level-sequence-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-for-system-integration/sequence-diagram/README.md`.
- **Ảnh mẫu:** 16 ảnh uml-diagrams.org + 30 ảnh SourceMaking, loại `sequence-diagram`: `python3 scripts/knowledge.py image -q "sequence <từ khóa>"`.
- **Công cụ và mẫu của dự án:** `sequence` (mục 4.3, 4.9 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/sequence-diagram/template.png` nếu có).

### State machine (trạng thái)
- **Trả lời câu hỏi:** Một đối tượng có những trạng thái nào, sự kiện nào đổi trạng thái.
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/state-machine-diagram/spec.md`; `assets/uml/protocol-state-machine/spec.md`.
- **Cách xây dựng sơ đồ từ yêu cầu và phân tích** (SourceMaking, tiếng Anh, có ví dụ làm từng bước): `assets/sourcemaking-uml/pages/modeling-it-systems/statechart-diagram/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/constructing-statechart-diagrams/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/the-life-of-an-object/README.md`.
- **Ảnh mẫu:** 16 ảnh uml-diagrams.org + 16 ảnh SourceMaking, loại `state-machine-diagram`: `python3 scripts/knowledge.py image -q "state <từ khóa>"`.
- **Công cụ và mẫu của dự án:** `statemachine` (mục 6 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/state-machine-diagram/template.png` nếu có).

### Communication
- **Trả lời câu hỏi:** Các đối tượng cộng tác với nhau thế nào (nhấn vào liên kết, không nhấn vào thời gian).
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/communication-diagram/spec.md`.
- **Cách xây dựng sơ đồ từ yêu cầu và phân tích** (SourceMaking, tiếng Anh, có ví dụ làm từng bước): `assets/sourcemaking-uml/pages/modeling-it-systems/communication-diagram/README.md`; `assets/sourcemaking-uml/pages/modeling-it-systems/constructing-communication-diagrams/README.md`.
- **Ảnh mẫu:** 13 ảnh uml-diagrams.org + 14 ảnh SourceMaking, loại `communication-diagram`: `python3 scripts/knowledge.py image -q "communication <từ khóa>"`.
- **Công cụ và mẫu của dự án:** chưa có công cụ (mục 6 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/communication-diagram/template.png` nếu có).

### Component
- **Trả lời câu hỏi:** Các thành phần phần mềm, cổng và kết nối.
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/component-diagram/spec.md`; `assets/uml/component-diagram/component.md`; `assets/uml/component-diagram/port.md`.
- **Cách xây dựng:** chưa có bài riêng; dùng `spec.md` ở trên và `uml-examples`.
- **Ảnh mẫu:** 27 ảnh uml-diagrams.org + 0 ảnh SourceMaking, loại `component-diagram`: `python3 scripts/knowledge.py image -q "component <từ khóa>"`.
- **Công cụ và mẫu của dự án:** `component` (thành phần), `deployment` (triển khai), `package` (gói) (mục 6 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/component-diagram/template.png` nếu có).

### Deployment
- **Trả lời câu hỏi:** Phần mềm chạy trên máy, nút mạng nào.
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/deployment-diagram/spec.md`; `assets/uml/deployment-diagram/node.md`.
- **Cách xây dựng:** chưa có bài riêng; dùng `spec.md` ở trên và `uml-examples`.
- **Ảnh mẫu:** 31 ảnh uml-diagrams.org + 0 ảnh SourceMaking, loại `deployment-diagram`: `python3 scripts/knowledge.py image -q "deployment <từ khóa>"`.
- **Công cụ và mẫu của dự án:** `component` (thành phần), `deployment` (triển khai), `package` (gói) (mục 6 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/deployment-diagram/template.png` nếu có).

### Package
- **Trả lời câu hỏi:** Cách chia gói và phụ thuộc giữa các gói.
- **Khái niệm, ký hiệu, nghĩa của từng đường và hình** (tiếng Anh, AI đọc thẳng): `assets/uml/package-diagram/spec.md`; `assets/uml/package-diagram/package-merge.md`.
- **Cách xây dựng sơ đồ từ yêu cầu và phân tích** (SourceMaking, tiếng Anh, có ví dụ làm từng bước): `assets/sourcemaking-uml/pages/modeling-business-systems/package-diagram/README.md`; `assets/sourcemaking-uml/pages/modeling-business-systems/constructing-package-diagrams/README.md`.
- **Ảnh mẫu:** 7 ảnh uml-diagrams.org + 8 ảnh SourceMaking, loại `package-diagram`: `python3 scripts/knowledge.py image -q "package <từ khóa>"`.
- **Công cụ và mẫu của dự án:** `component` (thành phần), `deployment` (triển khai), `package` (gói) (mục 6 của `quy-trinh-ve-so-do-bang-json.md`; ảnh mẫu `assets/uml/package-diagram/template.png` nếu có).

## 3. Loại khác và tài liệu liên quan

- **ERD (cơ sở dữ liệu):** Không thuộc UML. Chuẩn dự án: `quy-trinh-ve-so-do-bang-json.md` mục 4.4 và 4.9 (đường nối cột khóa chính tới cột khóa ngoại). Bài tiếng Việt về quan hệ bảng: `assets/m2mba/posts/moi-quan-he-giua-cac-bang-trong-csdl/README.md`, `moi-quan-he-nhieu-nhieu-trong-thiet-ke-CSDL`, `kha-chnh-primary-key--ngha-v-vai-tr-trong-csdl`, `cm-nang-c-bn-v-database` (cùng thư mục `assets/m2mba/posts/`). Công cụ `erd`.
- **Composite structure, information flow, interaction overview, manifestation, model, network architecture, profile, timing:** Chỉ `assets/uml/<loại>/spec.md` (profile thêm `stereotype.md`). Không có bài xây dựng. Chưa có công cụ.
- **Ví dụ tổng hợp:** `assets/uml/uml-examples/spec.md` (86 ảnh ví dụ đủ loại).
- **Kiến trúc hệ thống, cache, thanh toán, Kafka, database scaling:** `assets/system-design-elite/INDEX.md` và `pages/` (ảnh loại `caching-architecture`, `fintech-architecture`, `database-architecture`, `messaging-architecture`...).
- **Luồng nghiệp vụ, thanh toán (tiếng Việt):** `assets/m2mba/FULL_INDEX.md`, `posts/` (73 ảnh loại `business-workflow`).
- **Mẫu HTML/SVG đẹp (ví dụ kiến trúc, biểu đồ số):** `assets/templates/` và skill `diagram-design`; dùng cho trang trình bày, không dùng cho sơ đồ nộp vào tài liệu UC.

## 4. Lưu ý đã biết về kho
- Ba file từng là trang lỗi 404 (đường dẫn tải sai). Đã tải lại ngày 10/11/2026: `sequence-diagram/messages.md` (từ `interaction-message.html`), `sequence-diagram/fragments.md` (từ `sequence-diagrams-combined-fragment.html`); `state-machine-diagram/behavioral-state.md` không có trang riêng nên chỉ còn ghi chú trỏ về `spec.md`. Chỉ tải chữ, ảnh của các trang mới chưa nằm trong `IMAGE_REGISTRY.json`.
- Các `template.json` và `template.drawio` cũ trong `assets/uml/` từng là bản sao sai của một mẫu hoạt động; đã chuyển vào `assets/uml/_template-cu-sai/`. Mẫu đúng: `<loại>/template.json` của bốn loại có công cụ và `agents/knowledge/diagrams/mau/`.
- Số ảnh và đường dẫn trong trang này kiểm bằng `IMAGE_REGISTRY.json` ngày 10/11/2026; thêm ảnh hoặc bài mới thì cập nhật lại trang này.

## 5. Đối chiếu kho với nguồn ngoài (10/11/2026)

Đã đối chiếu các điểm dễ sai của tri thức dự án với uml-diagrams.org (đọc trang gốc) và các bài SourceMaking có sẵn trong kho:

| Điều dự án đang dùng | Nguồn nói gì | Kết luận |
|---|---|---|
| `include`: mũi tên nét đứt đầu hở từ use case GỐC tới use case được gọi, nhãn «include»; phần được gọi bắt buộc | `use-case-diagram/include.md`: đúng như vậy, gốc chưa hoàn chỉnh một mình | Đúng |
| `extend`: mũi tên nét đứt đầu hở từ use case MỞ RỘNG tới use case gốc, nhãn «extend»; tùy chọn, có điều kiện, có điểm mở rộng | `use-case-diagram/extend.md` | Đúng; công cụ chưa vẽ điều kiện và điểm mở rộng (ghi trong mô tả) |
| Tác nhân đặt tên theo vai, là thực thể bên ngoài, nối use case bằng đường liền không mũi tên | `use-case-diagram/how-to.md`, `actor-association.md` | Đúng |
| Activity được phép nhiều điểm bắt đầu và nhiều điểm kết thúc | `activity-diagram/controls.md`: "may have more than one initial node", "more than one activity final node" | Đúng. Luật cũ "đúng một điểm kết thúc" là quy ước riêng của dự án, không phải UML |
| Activity: mũi tên NÉT ĐỨT khi sang làn khác (lời gọi, message) | UML không định nghĩa nét đứt này cho activity | Là QUY ƯỚC của mẫu anhbv, không phải UML gốc; ghi rõ khi giải thích sơ đồ |
| Sequence: gọi = mũi tên đặc, trả về = nét đứt đầu hở | `sequence-diagram/messages.md`: call đồng bộ đầu đặc, reply nét đứt đầu hở; bất đồng bộ đầu hở nét liền | Đúng; công cụ đã thêm `kind: async` |
| Class: thoi rỗng ở phía lớp chứa (aggregation), thoi đặc (composition), tam giác rỗng (kế thừa, implements nét đứt) | `class-diagram/association.md`, `generalization.md`, `dependency.md` | Đúng |
| Class: liên kết (association) vẽ bằng mũi tên ĐẶC | `class-diagram/association.md`: UML dùng đầu mũi tên HỞ cho đầu có thể điều hướng, dấu x cho đầu không điều hướng | Là QUY ƯỚC của mẫu sơ đồ lớp dự án ("mũi tên đặc: dùng"); giữ nguyên, ghi rõ khi giải thích |
| Class: phụ thuộc là nét đứt đầu hở từ client tới supplier; kế thừa là tam giác rỗng về lớp cha; thoi rỗng là aggregation, thoi đặc là composition | `dependency.md`: "dashed arrow from the client to the supplier"; `generalization.md`: "hollow triangle ... points to the general classifier"; `association.md`: shared và composite aggregation | Đúng |
| ERD: nối cột khóa chính tới cột khóa ngoại, đầu "một" và "nhiều" | Không phải UML; ký hiệu chân quạ | Quy ước dự án, giữ nguyên |
| Luật dự án "sơ đồ lớp không ghi bội số 1, 0..*" | `class-diagram/multiplicity.md`: UML có bội số | Khác UML: là quy ước dự án (theo mẫu anhbv); khi tài liệu cần mô tả bội số thì ghi bằng chữ |
