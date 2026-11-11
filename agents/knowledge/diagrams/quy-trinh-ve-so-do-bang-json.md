# Quy trình vẽ sơ đồ bằng JSON (bắt buộc cho mọi agent, mọi loại sơ đồ)

> **Loại: tham khảo.** Chi tiết của luật nằm ở `AGENTS.md` mục 21; file này nói rõ từng bước, công cụ, chuẩn từng loại sơ đồ và cách xử lý lỗi. Khi khác `AGENTS.md` thì theo `AGENTS.md`.

Áp dụng cho **Claude, Gemini, Codex và mọi agent khác**. Lý do chung: agent phải tự tính tọa độ và viết XML draw.io thì sai ngay lần đầu mà không biết. Công cụ `scripts/ve-so-do.py` bỏ việc đó đi: agent chỉ viết **JSON mô tả**, công cụ bố trí, nối đường, xuất ảnh và kiểm lỗi bằng chữ.

## 0. Bảng tra nhanh: loại sơ đồ nào, cần gì, công cụ nào, mẫu ở đâu

**MẪU PHÂN TÍCH VÀ KHUNG JSON để điền sau khi phân tích: `agents/knowledge/diagrams/mau-phan-tich/` (`00-quy-trinh-mot-uc.md` đọc trước; rồi `use-case.md`, `sequence.md`, `activity.md`, `class.md`, `erd.md`, `state-machine.md`). Mỗi file có phiếu phân tích, khung JSON đã kiểm chạy được, lỗi hay gặp.**

**Muốn hiểu KHÁI NIỆM, nghĩa của từng đường và hình, hoặc CÁCH PHÂN TÍCH để vẽ một loại sơ đồ: đọc `agents/knowledge/srs/uml-diagrams-mastery.md` (mục tra cứu: trỏ tới bài uml-diagrams.org, bài SourceMaking "Constructing …", ảnh mẫu, tiếng Anh, AI đọc thẳng).** Bảng dưới chỉ nói công cụ và chuẩn dự án.

Đọc bảng này ĐẦU TIÊN. `ve-so-do.py --mau <type>` in JSON mẫu; ảnh mẫu sinh sẵn nằm ở `assets/uml/<thư mục>/template.png`; ảnh UML chung để tra ký hiệu nằm ở `assets/uml/<thư mục>/images/` (KHÔNG phải chuẩn dự án, khi khác thì theo chuẩn dự án).

| Loại sơ đồ | Phải chuẩn bị trước (nguồn thật) | Công cụ (`type`) | JSON mẫu và ảnh mẫu | Mục chuẩn |
|---|---|---|---|---|
| ERD | Tên bảng, cột, kiểu, khóa chính, khóa ngoại, cột có chỉ mục (từ entity, Liquibase, DB) | `erd` | `mau/erd.json` | 4.4, 4.8 |
| Class | Danh sách lớp thật, thuộc tính, hàm, loại quan hệ (kế thừa, chứa, phụ thuộc) từ mã nguồn | `class` | `mau/class.json`, `assets/uml/class-diagram/template.png` | 4.1 |
| Sequence | Thứ tự các lớp gọi nhau, hàm, dữ liệu trả về; lớp thực sự là người gọi | `sequence` | `mau/sequence.json`, `assets/uml/sequence-diagram/template.png` | 4.3 |
| Activity (hoạt động) | Các lớp hoặc thành phần chạy mã làm làn, các bước theo thứ tự chạy, mọi điểm rẽ nhánh và nhánh lỗi tới nơi trả lỗi | `activity` | `mau/activity.json`, `assets/uml/activity-diagram/template.png`, `mau-anhbv/mau-activity.png` | 4.6, 4.9 |
| Use case | Tác nhân theo VAI THẬT (Kế toán, CSKH, Telesale, Nhân viên kho, Quản trị viên...), use case lấy từ tài liệu yêu cầu, quan hệ include và extend | `usecase` | `mau/usecase.json`, `assets/uml/use-case-diagram/template.png` | 4.10 |
| Một UC trọn bộ | Bốn sơ đồ trên (ERD, Class, Sequence, Activity) | `bundle` | `mau/bundle.json` | 4.7 |
| Lưu đồ một làn (cũ) | Thuật toán một lớp | `flow` | `mau/flow.json` | 4.2 |
| Hoạt động theo vai (cũ) | Luồng nhiều vai người dùng | `swimlane` | `mau/swimlane.json` | 4.5 |
| Trạng thái | Danh sách trạng thái thật (enum), sự kiện, điều kiện, hành động | `statemachine` | `mau/statemachine.json`, `assets/uml/state-machine-diagram/template.png` | 4.11 |
| Thành phần | Module, giao diện cung cấp, giao diện cần | `component` | `mau/component.json`, `assets/uml/component-diagram/template.png` | 4.11 |
| Triển khai | Máy, môi trường chạy, artifact, đường truyền (từ compose, manifest) | `deployment` | `mau/deployment.json`, `assets/uml/deployment-diagram/template.png` | 4.11 |
| Gói | Gói mã thật, câu import giữa các gói | `package` | `mau/package.json`, `assets/uml/package-diagram/template.png` | 4.11 |
| Kiến trúc tổng thể, vòng đời nhiều đối tượng | Thành phần và kết nối mức hệ thống | archify (JSON có `diagram_type`) | `quy-uoc-draw-io-va-archify.md` | 6 |
| Mockup giao diện | Dữ liệu và nhãn chụp từ giao diện thật đang chạy | `scripts/ve_mockup_uc04.py` của workspace (spec JSON) | `doc/features/UC-04-advanced-filter/hinh/UC-04-mockup.spec.json` | 6 |
| Communication, timing, interaction overview, profile, user story map | Tùy loại | CHƯA có công cụ: vẽ tay draw.io theo `assets/uml/<loại>/spec.md` | không có | 6 |

Mọi loại có công cụ đều: viết JSON trước, `--check-only`, sinh, xem ảnh, nhúng ảnh (mục 1). Mọi tên và con số trong JSON phải có nguồn (mục 4.9).

**BỘ MẪU VÀNG để bắt chước (một UC đủ năm sơ đồ):** `doc/features/UC-04-advanced-filter/hinh/` gồm `UC-04.spec.json` (bundle ERD, Class, Sequence, Activity), `UC-04-activity.spec.json`, `UC-04-class.spec.json`, `UC-04-erd.spec.json`, `UC-04-sequence-loc.spec.json` và `UC-04-use-case.spec.json` (use case, ra file `UC-04-use-case-chuan.drawio`). Xem JSON để biết cách đặt tên, chia làn, đặt hàng, ghi nhãn; KHÔNG chép nội dung UC-04 sang UC khác.

**Sau khi vẽ xong cả bộ: chạy `python3 ~/Documents/agent-base/scripts/kiem-bo-so-do.py doc/features/<UC>/hinh` (vòng lặp vẽ, kiểm, sửa, xem ở `mau-phan-tich/00-quy-trinh-mot-uc.md` mục 7).**

## 1. Tám bước bắt buộc (không đảo, không bỏ)

| # | Bước | Làm gì | Bằng chứng |
|---|---|---|---|
| 1 | Đọc mẫu chuẩn | Đọc mục 4 của file này cho đúng loại sơ đồ; mở ảnh mẫu của loại đó | Nêu loại sơ đồ và mẫu đã đọc |
| 2 | Lập bảng sự thật | Mọi tên lớp, hàm, bảng, cột, bước, thông điệp lấy từ code hoặc tài liệu qua công cụ tra cứu (XERJ, project-graph, đọc file). **Cấm bịa tên** | Danh sách nguồn từng tên |
| 3 | **Viết JSON TRƯỚC** | Tạo `<tên>.spec.json` cạnh nơi đặt sơ đồ (ví dụ `doc/features/<UC>/hinh/`). JSON là nguồn sự thật. Chưa có `.drawio` ở bước này | File `.spec.json` |
| 4 | Kiểm JSON | `python3 ~/Documents/agent-base/scripts/ve-so-do.py <spec> --check-only`. Sửa hết `LỖI`; mỗi `CẢNH BÁO` sửa hoặc ghi lý do chấp nhận | Dòng `KIỂM: đạt` |
| 5 | Sinh draw.io và ảnh | Chạy lại không có `--check-only` để ra `.drawio` và `.png` | File ra |
| 6 | Xem ảnh | Xem được ảnh: mở ảnh xem từng hộp, đường, nhãn; sai thì **sửa JSON rồi chạy lại** (không sửa `.drawio` do script sinh). Không xem được ảnh: ghi **"chưa xem ảnh, mới kiểm bằng script"** | Ghi chú đã xem hay chưa |
| 7 | Nhúng vào tài liệu | Ảnh kèm mô tả (bảng hoặc các bước đánh số ngay dưới ảnh) và dòng "Sơ đồ nguồn" trỏ tới `.drawio` | Link trong md |
| 8 | Báo cáo | Đường dẫn spec, kết quả `KIỂM`, số cảnh báo còn lại, đã hay chưa xem ảnh | 3 dòng (mục 7) |

**Cấm:** viết XML `.drawio` hoặc tính tọa độ bằng tay; dùng Mermaid hoặc PlantUML cho sơ đồ nộp vào tài liệu; báo "xong" khi chưa chạy script; bỏ bước kiểm; vẽ sai mẫu chuẩn của loại sơ đồ.

**Ngoại lệ duy nhất:** người dùng đã tự chỉnh `.drawio` bằng tay. Khi đó `.drawio` thắng; sửa tại chỗ theo `huong-dan-ve-so-do.md` mục 5 của dự án và ghi rõ spec JSON đã lệch. Không sinh lại để ghi đè.

## 2. Công cụ

```bash
python3 ~/Documents/agent-base/scripts/ve-so-do.py --mau class      # in JSON mẫu (class | flow | swimlane | sequence | erd)
python3 ~/Documents/agent-base/scripts/ve-so-do.py spec.json --check-only   # chỉ kiểm, không ghi file
python3 ~/Documents/agent-base/scripts/ve-so-do.py spec.json                # ghi .drawio, xuất .png, kiểm
```

- Trường chung: `type` (`class`, `flow`, `swimlane`, `sequence`, `erd`), `title`, `note`, `out` (tên `.drawio`), `png` (tên ảnh), `page` (tên trang). File ra nằm cạnh file spec.
- Xuất ảnh cần draw.io Desktop (`brew install --cask drawio`, hoặc đặt biến `DRAWIO_CLI`). Không có thì script vẫn ghi `.drawio` và kiểm lỗi; báo rõ "chưa xuất ảnh".
- **Quy ước tên file:** file spec đặt cạnh ảnh và **cùng tên gốc với ảnh**: ảnh `hinh/UC-04-erd.png` thì spec là `hinh/UC-04-erd.spec.json` (và `out` là `UC-04-erd.drawio`). `srs-check.py` dựa vào quy ước này để báo ảnh sơ đồ thiếu spec.
- Ảnh quá lớn (trên khoảng 4000 điểm mỗi chiều) bị draw.io cắt cụt khi xuất; công cụ tự giảm tỉ lệ xuất để tránh.
- `ve-so-do-lop.py` là tên cũ, vẫn chạy (mặc định `type: class`).
- Mã thoát 0 là đạt, 1 là có `LỖI`.

## 3. Cách bố trí bằng JSON (không dùng tọa độ)

- **Lớp, bảng, lưu đồ:** gán `col` (cột 0, 1, 2... từ trái sang phải); lưu đồ thêm `row` (hàng). Trong cột, lớp và bảng xếp từ trên xuống theo thứ tự khai báo. Đặt các phần tử có quan hệ **ở cột kề nhau**.
- **Quan hệ không kề nhau:** thêm `via` (hoành độ của đường chạy dọc vòng ngoài) để đường không cắt qua hộp khác.
- **Nút nhánh phụ gộp vào luồng chính** (lưu đồ): thêm `"first": "v"` vào cạnh để đường đi dọc trước rồi mới rẽ ngang vào cạnh bên của nút đích; dùng với nút gộp `junc`.
- **Dòng quá dài:** tăng `w` của lớp hoặc bảng, hoặc rút gọn dòng.
- **Ép vị trí:** `x`, `y` chỉ dùng khi bắt buộc.
- Mỗi `CẢNH BÁO: đường ... cắt qua ...` xử lý theo thứ tự: đổi cột, thêm `via`, dời phần tử.

## 4. Chuẩn từng loại sơ đồ

### 4.1. Sơ đồ lớp (`type: class`)

Mẫu chuẩn (người dùng xác nhận): ảnh `assets/uml/class-diagram/images/uml-class-mau-thu-vien-sach.png` (IMG-0712). Ảnh do công cụ sinh: `assets/uml/class-diagram/images/mau-lop-tu-script.png` (IMG-0714), JSON mẫu `mau/class.json`.

- Hộp trắng ba ngăn: tên in đậm giữa hộp (dòng 2 nhỏ: nghĩa tiếng Việt), thuộc tính `- tên : kiểu`, hàm `+ tên(kiểu tham số) : kiểu`. Không biểu tượng C, I, E.
- `stereo`: `interface`, `enumeration`, `Abstract` (in `<<...>>`); `abstract: true` in nghiêng tên.
- `relations[].kind`: `ext` (Extends, implements: đường liền, tam giác rỗng, `label` ghi `Extends` hoặc `implements`), `agg` (thoi rỗng, `from` là phía chứa), `comp` (thoi đặc), `assoc` (mũi tên đặc), `dep` (đứt, mũi tên mở). **Không ghi số lượng** 1, 0..*.
- Kiểm tự động: hộp chồng nhau, quan hệ trỏ lớp không có, `kind` sai, đường cắt hộp, dòng quá dài.

### 4.2. Lưu đồ và sơ đồ hoạt động một làn (`type: flow`)

Ảnh: `assets/uml/activity-diagram/images/mau-flow-tu-script.png` (IMG-0715), JSON mẫu `mau/flow.json`.

- `nodes[]`: `id`, `kind`, `col`, `row`, `label`. `kind`: `start` (chấm đen), `end` (chấm kết thúc), `proc` (việc làm), `dec` (quyết định, hình thoi), `ok` (nhánh phụ thành công, xanh nhạt), `err` và `ex` (lỗi, đỏ), `junc` (điểm gộp, **hình tròn nhỏ**, không dùng hình thoi vì `srs-check` coi mọi hình thoi là quyết định).
- `edges[]`: `from`, `to`, `label`, `color` (`green`, `red`, `blue`, `black`), `via` (đường vòng), `dashed`.
- Quy tắc nội dung (loại `flow`; loại `activity` ở mục 4.6 được nhiều điểm đầu và cuối): **đúng 1 điểm bắt đầu, đúng 1 điểm kết thúc**; mọi nhánh, kể cả lỗi, đều về điểm kết thúc; nhánh lỗi tô đỏ, đi vòng bên phải rồi về điểm kết thúc; nhãn bằng lời thường, tên hàm hoặc mã lỗi trong ngoặc.
- Kiểm tự động: số điểm đầu, cuối; nút quyết định có ít nhất 2 nhánh ra và **mỗi nhánh có nhãn**; nút nào cũng có đường đi ra (trừ điểm kết thúc); mọi nút với tới được từ điểm bắt đầu; thiếu `label`; đường cắt nút; nút chồng nhau.
- Nhiều làn bơi: dùng `type: swimlane` (mục 4.5).

### 4.3. Sơ đồ tuần tự (`type: sequence`)

Ảnh: `assets/uml/sequence-diagram/images/mau-seq-tu-script.png` (IMG-0716), JSON mẫu `mau/sequence.json`.

- `participants[]`: `id`, `name` (xuống dòng bằng `\n`, ghi nghĩa trước, tên kỹ thuật trong ngoặc), `color` (`blue`, `green`, `purple`, `amber`, `red`, `gray`).
- `messages[]` theo đúng thứ tự thời gian: `from`, `to`, `label`, `kind` (`call` mặc định, `return` nét đứt, `self` gọi chính mình).
- Quy tắc: **chỉ đánh số lời gọi**, không đánh số dòng trả về (script tự đánh số); nhãn nằm phía trên đường.
- Kiểm tự động: thông điệp trỏ đối tượng không có; gọi chính mình mà không dùng `self`; nhãn quá dài so với khoảng cách; số dòng trả về nhiều hơn số lời gọi.


**Kiểu thông điệp (UML 2.5, đã đối chiếu `assets/uml/sequence-diagram/messages.md`, 10/11/2026) và `kind` trong JSON:**

| Thông điệp | Hình vẽ | `kind` |
|---|---|---|
| Gọi đồng bộ (gửi và chờ kết quả) | Nét liền, đầu mũi tên đặc | `call` (mặc định) |
| Gọi bất đồng bộ (gửi rồi chạy tiếp, không chờ) | Nét liền, đầu mũi tên hở | `async` |
| Trả về (reply) | Nét đứt, đầu mũi tên hở | `return` |
| Tự gọi chính nó | Mũi tên vòng lại lifeline | `self` |
| Tạo đối tượng (create), hủy (delete, dấu X cuối lifeline), mất thông điệp (lost), tìm thấy (found) | Có trong nguồn | CHƯA có trong công cụ; ghi vào mô tả |

Khung `alt` (rẽ nhánh), `opt` (tùy chọn), `loop`, `par` (song song)... là "combined fragment" (`assets/uml/sequence-diagram/fragments.md`); công cụ chưa vẽ khung, thể hiện nhánh bằng thông điệp có nhãn "[điều kiện]" và ghi rõ trong mô tả.

### 4.4. ERD, sơ đồ bảng dữ liệu (`type: erd`)

Ảnh: `assets/uml/class-diagram/images/mau-erd-tu-script.png` (IMG-0717), JSON mẫu `mau/erd.json`.

- `tables[]`: `id`, `name`, `col`, `color` (`green` bảng chính, `blue` bảng liên quan), `columns` là danh sách `[tên cột, kiểu, khóa]` với khóa `PK`, `FK`, `UQ` hoặc rỗng, `hot` là các cột nằm trong chỉ mục (tô cam).
- Quy tắc: mỗi bảng là lưới 3 cột (Tên cột, Kiểu, Khóa), **không có dòng tiêu đề cột**; chỉ liệt kê cột liên quan; kiểu lấy từ `@Column` hoặc migration, không đoán.
- `relations[]` **nối đúng cột với cột**, không nối bảng với bảng: `from` và `from_col` là bảng và cột khóa chính (phía một), `to` và `to_col` là bảng và cột khóa ngoại (phía nhiều, ký hiệu chân chim), `label` là tên cột hoặc ghi chú. `to_col` có thể là **danh sách** khi nhiều cột khóa ngoại cùng trỏ về một khóa chính (ví dụ 6 cột `staff_*_id` về `staff.id`): mỗi cột một đường. Công cụ báo `LỖI` khi thiếu `from_col`/`to_col` hoặc tên cột không có trong bảng; hai bảng phải ở hai cột (`col`) khác nhau; các quan hệ cùng đổ vào một bảng được dàn thành các đường dọc riêng, không chồng nhau.

### 4.5. Sơ đồ hoạt động nhiều làn bơi (`type: swimlane`)

Ảnh: `assets/uml/activity-diagram/images/mau-swimlane-tu-script.png` (IMG-0718), JSON mẫu `mau/swimlane.json`.

- Giống `flow` (cùng `kind` nút, cùng `edges`) và thêm:
  - `lanes[]`: `id`, `name` (tên tác nhân, ghi nghĩa trước), `color` (`gray`, `blue`, `purple`, `amber`, `green`, `red`). Thứ tự khai báo là thứ tự làn từ trái sang phải; mỗi làn là một tác nhân (người dùng, giao diện, API Gateway, dịch vụ, cơ sở dữ liệu...).
  - mỗi nút có `lane` (mã làn) thay cho `col`, và `row` (hàng, từ trên xuống).
- (Loại cũ theo VAI; sơ đồ hoạt động mặc định nay là `activity`, mục 4.6.) Quy tắc nội dung: như lưu đồ (một điểm bắt đầu, một điểm kết thúc, nhánh quyết định có nhãn, lỗi đỏ về điểm kết thúc); thêm: **mỗi nút nằm đúng làn của tác nhân thực hiện việc đó**; mũi tên băng qua làn là một lời gọi hoặc một lần chuyển việc, ghi nhãn nếu mang dữ liệu.
- Kiểm tự động: như `flow`, thêm lỗi nút thiếu `lane` hoặc `lane` không có trong `lanes`.
- Dùng cho: sơ đồ hoạt động theo luồng nghiệp vụ nhiều tác nhân (ví dụ lọc đơn từ người dùng tới cơ sở dữ liệu).

### 4.6. Sơ đồ hoạt động theo làn LỚP (`type: activity`), MẪU CHUẨN MỚI, dùng mặc định

Nguồn mẫu: bốn trang của anhbv ở `agents/knowledge/diagrams/mau-anhbv/` (xem ảnh `mau-activity.png`, `mau-class.png`, `mau-sequence.png`, `mau-erd.png`; file `.drawio` gốc cùng thư mục). Người dùng chốt 09/11/2026: **vẽ giống mẫu này, đen trắng, không màu mè**. Mẫu JSON: `python3 ~/Documents/agent-base/scripts/ve-so-do.py --mau activity` (file `mau/activity.json`).

Luật của loại này (khác `swimlane` theo vai):
- **Mỗi làn là MỘT LỚP hoặc THÀNH PHẦN chạy mã** (Controller, Service, ScreenFilterSchema, PostgreSQL, RabbitMQ...). Làn "Người dùng" và "Giao diện" được phép làm làn đầu. Không phân làn theo chức danh (Kế toán, CSKH...).
- **Nhiều điểm bắt đầu và nhiều điểm kết thúc được phép** (mỗi làn chạy độc lập có điểm vào riêng; mỗi nhánh lỗi có thể có điểm kết thúc riêng kèm `note` in nghiêng). Cạnh này khác luật cũ "đúng 1 kết thúc" của `flow` và `swimlane`; luật cũ vẫn đúng cho hai loại đó.
- Mũi tên liền = luồng trong một làn; **nét đứt = lời gọi hoặc message sang làn khác** (công cụ tự đặt khi hai nút khác làn), cạnh liên làn phải có nhãn ngắn ("gọi validate", "danh sách mã đơn", "HTTP GET").
- Nhánh quyết định ghi điều kiện trong ngoặc vuông `[Có]`, `[Không]` (công cụ tự thêm ngoặc). Nhánh lỗi: nút `kind: "err"` viền đậm, KHÔNG tô đỏ.
- Có hộp **Chú giải (UML Activity)** dưới sơ đồ (mặc định bật).
- Bố trí không tọa độ: `lane` (làn), `row` (hàng, số thực được, 1 hàng khoảng 115 điểm), `sub` (cột con trong làn; làn có `sub` lớn nhất bằng bao nhiêu thì rộng bấy nhiêu cột). Nhánh phụ (lỗi, ngoại lệ) đặt ở `sub: 1` cùng hàng với nút rẽ.
- Cạnh nối nút khác cột và hàng: mặc định đi ngang ở hàng nguồn rồi xuống đầu đích. `first: "v"` đi xuống trước rồi rẽ ngang vào cạnh bên đích (dùng khi nhánh phụ gộp về luồng chính). `via: <x>` vòng lại qua đường dọc tại x (vòng lặp, ví dụ `via` nằm sát mép trái của làn).
- Nhãn nút `proc` tối đa khoảng 120 ký tự, `dec` tối đa khoảng 60 ký tự; dài hơn thì tách bước (công cụ cảnh báo).
- Kiểm tự động: mọi nút có đường ra (trừ kết thúc), mọi nút với tới được từ một điểm bắt đầu, mỗi điểm bắt đầu tới được một điểm kết thúc, quyết định có từ 2 nhánh có nhãn, hộp chồng nhau, đường cắt hộp, cạnh liên làn thiếu nhãn.

### 4.7. Gộp nhiều sơ đồ thành các tab của MỘT file (`type: bundle`)

Mẫu của anhbv: một file `.drawio` bốn tab, **mỗi loại sơ đồ đúng một tab** (ERD, Class, Sequence, Activity). Một chức năng (UC) làm theo đó: `doc/features/<UC>/hinh/<UC>.spec.json` loại `bundle` liệt kê các tab, mỗi tab trỏ tới một spec con (`<UC>-erd.spec.json`, `<UC>-class.spec.json`, `<UC>-sequence.spec.json`, `<UC>-activity.spec.json`). Mẫu: `ve-so-do.py --mau bundle`. Một lệnh `ve-so-do.py <UC>.spec.json` kiểm cả bốn spec, ghi một `.drawio` bốn tab và xuất từng ảnh `.png` (tên theo trường `png` của spec con). File `.drawio` riêng của spec con KHÔNG ghi.

Cấm tách mỗi lưu đồ nhỏ thành một tab: lỗi đã mắc ở UC-04 (12 tab, năm lưu đồ rời) và phải gộp lại. Thuật toán chi tiết (validate, toPredicate...) thành các làn và nhánh của MỘT sơ đồ hoạt động; phần cần giải thích dài thì viết lời trong tài liệu, không vẽ thêm lưu đồ.

Các loại chưa có công cụ JSON (use case, user story map, mockup) không vào bundle; để file riêng (`<UC>-use-case.drawio`).

### 4.8. Phong cách đen trắng (mặc định)

ERD (`erd`) và tuần tự (`sequence`) mặc định đen trắng: tiêu đề bảng và hộp đối tượng nền xám nhạt `#f2f2f2`, cột nằm trong chỉ mục nền xám đậm hơn và chữ đậm. Muốn có màu thì ghi `"plain": false` trong spec, chỉ khi người dùng yêu cầu.

### 4.9. Luật NỘI DUNG cho bộ sơ đồ một UC (rút ra từ lần Gemini vẽ thử UC-04, 10/11/2026)

Công cụ chỉ kiểm hình thức. Các luật sau do agent tự giữ; người duyệt dùng chúng làm danh sách soát:
1. **Nguồn sự thật cho mọi tên và con số.** Tên lớp, hàm, bảng, cột, toán tử, mã lỗi, con số (kích thước trang, giới hạn) phải lấy từ mã nguồn (XERJ), CSDL hoặc tài liệu UC đã duyệt. Không có nguồn thì KHÔNG vẽ; hoặc ghi rõ "giả định" ngay trên hình. Lỗi đã mắc: Gemini thêm toán tử `TODAY, THIS_WEEK, THIS_MONTH` (không tồn tại, thật là 18 toán tử khác) và hàm `getSourceOrders` (thật là `findRows`).
2. **Làn activity là MỘT lớp hoặc thành phần.** Không gộp "Người dùng & Trình duyệt"; tách làn Người dùng và làn Giao diện. Khi hai lớp cùng làn (ví dụ Controller và Advice) phải là hai cột con (`sub`) hoặc ghi cả hai tên có chủ đích.
3. **Mỗi nhánh lỗi phải đi tới nơi trả lỗi thật** (lớp bắt lỗi, mã HTTP, mã lỗi), không dừng ở "Ném lỗi" rồi kết thúc. Nhánh lỗi hệ thống (HTTP 500) cũng phải có nếu mã nguồn có.
4. **Không rút gọn quá tay.** Một bước kiểm có nhiều điều kiện (số điều kiện, thiếu cột, trùng cột, ngoài danh mục, sai kiểu so sánh) thì mỗi điều kiện một nút quyết định hoặc gom có chủ đích kèm nhãn nêu đủ; không thay bằng một ô "hợp lệ?". Bước chọn cột cần bộ xử lý riêng, vòng lặp theo điều kiện cũng phải có.
5. **Sequence: người gọi phải đúng.** Xác định lớp thực sự gọi (ví dụ dịch vụ `GetListOrderSourceServiceImpl` gọi `OrderScreenRows.page`), không rút lớp trung gian làm mũi tên đi sai nguồn.
6. **Class: hai nửa tách thật.** Nếu ghi chú nói "nửa trên là thư viện, nửa dưới là service" thì đặt đúng như vậy (`y` khác nhau). Mỗi lớp có thật trong luồng phải có hộp (đủ lớp ở bảng mục 9 của tài liệu UC), dùng đúng loại quan hệ: thoi rỗng khi lớp này CHỨA lớp kia, mũi tên đứt khi chỉ phụ thuộc, tam giác rỗng khi implements. Không đổi mọi quan hệ thành mũi tên đứt.
7. **ERD: nhãn quan hệ là tên cột thật hoặc "N khóa: ...".** Không đặt nhãn kiểu `staff_id`, `area_id` nếu không phải tên cột. Cột ràng buộc (UQ, chỉ mục) lấy từ Liquibase, không đoán.
8. **Sau khi sinh phải mở ảnh.** Công cụ nay cảnh báo nhãn chồng nhau, nhãn đè lên hộp, hai quan hệ dùng chung một đoạn; sửa hết hoặc ghi lý do. Cảnh báo bằng 0 chưa có nghĩa là đẹp: vẫn phải xem ảnh.
9. **Không ghi đè bộ đã duyệt.** Vẽ thử hoặc vẽ lại đặt vào thư mục riêng (ví dụ `hinh/thu-<tên>/`), so sánh rồi mới thay.

### 4.10. Use case (`type: usecase`)

Mẫu: `ve-so-do.py --mau usecase`; ảnh: `assets/uml/use-case-diagram/template.png`. JSON cùng dạng file `.usecase.json` cũ của workspace (`usecases`, `actors`, `links`, `relations`), thêm `type: usecase` và `system` (tên khung hệ thống). Khái niệm gốc (đã đối chiếu uml-diagrams.org, 10/11/2026): `assets/uml/use-case-diagram/{how-to,subject,actor,use-case,actor-association,include,extend}.md`.

**Cách phân tích để vẽ use case chuẩn (4 bước, theo `how-to.md`):**
1. **Xác định hệ thống (subject).** Hệ thống đang thiết kế và RANH GIỚI của nó: cái gì nằm trong, cái gì nằm ngoài. Đặt tên đúng (ví dụ "Hệ thống đơn hàng"). Vẽ thành hình chữ nhật, use case nằm trong, tác nhân nằm ngoài.
2. **Xác định tác nhân (actor).** Tác nhân là thực thể BÊN NGOÀI hệ thống cần dịch vụ của nó: người dùng, hoặc hệ thống, thiết bị khác. Đặt tên theo VAI họ đóng với hệ thống (Kế toán, CSKH, Telesale, Nhân viên kho, Quản trị viên; hệ thống ngoài như J&T, Pancake). Người làm việc BÊN TRONG nghiệp vụ không phải tác nhân của hệ thống nghiệp vụ đó. Tên chung "User" bị cảnh báo.
3. **Xác định use case.** Mỗi use case là một đơn vị chức năng HOÀN CHỈNH và HỮU ÍCH mà hệ thống cung cấp cho tác nhân, do tác nhân khởi động, phản ánh mục tiêu của họ. Tên dạng "động từ + danh từ" (Chia đơn CSKH, Lọc đơn nâng cao), không phải một thao tác nhỏ hay một nút bấm. Tác nhân nối với use case bằng đường liền (association), không mũi tên.
4. **Mô tả hành vi của từng use case** bằng văn bản và, khi cần, bằng sơ đồ hoạt động, trạng thái hoặc tuần tự (đó là các sơ đồ khác của bộ UC).

**Quan hệ giữa các use case (bảng so sánh của nguồn):**

| | `include` | `extend` | generalization (tam giác rỗng) |
|---|---|---|---|
| Ý nghĩa | Hành vi của use case được gọi (phần bổ sung) CHÈN vào use case gốc; như gọi hàm con | Use case mở rộng, tùy chọn, chèn vào use case gốc tại một điểm mở rộng | Use case con chuyên biệt hóa use case cha |
| Use case gốc | Chưa hoàn chỉnh một mình (cần phần được gọi) | Hoàn chỉnh, có nghĩa độc lập | Có thể trừu tượng hoặc cụ thể |
| Phần được thêm | BẮT BUỘC, luôn chạy, không điều kiện | TÙY CHỌN, có điều kiện, có điểm mở rộng (extension point) | Bắt buộc nếu cha trừu tượng |
| Mũi tên | Nét đứt, đầu hở, TỪ use case gốc TỚI use case được gọi, nhãn «include» | Nét đứt, đầu hở, TỪ use case mở rộng TỚI use case gốc, nhãn «extend» | Nét liền, tam giác rỗng |
| Dùng khi | Tách use case lớn thành các use case nhỏ; rút phần dùng chung của hai use case trở lên | Có nhánh tùy chọn hoặc điều kiện đặc biệt | Có các biến thể thay thế nhau |

Điều kiện của `extend` và điểm mở rộng ghi trong ghi chú gắn với đường `extend`; điểm mở rộng cũng có thể ghi trong một ngăn của hình elip với tiêu đề "extension points". `include` KHÔNG có điều kiện và không có điểm chèn. Công cụ hiện chưa vẽ điều kiện và điểm mở rộng: ghi chúng vào mô tả use case trong tài liệu.

**Quy tắc của công cụ:**
- `generalizations`: `[[tác_nhân_con, tác_nhân_cha], ...]` (tác nhân con kế thừa tác nhân cha: nét liền, tam giác rỗng ở phía cha; ví dụ 5 vai kế thừa "Người dùng hệ thống"). Tác nhân con xếp thành cột bên trái, tác nhân cha ở giữa.
- `links`: tác nhân nối với use case. `relations`: `include` (from là use case gốc, mũi tên đi từ gốc tới phần được gọi) và `extend` (from là use case mở rộng, mũi tên đi từ use case mở rộng tới use case gốc); đường nét đứt, mỗi quan hệ một đường dọc riêng.
- Kiểm tự động: tác nhân không nối use case nào là LỖI; use case mồ côi, tên tác nhân chung chung là cảnh báo; `include`/`extend` tạo vòng là LỖI.
- Use case vẽ ra file riêng `<UC>-use-case.drawio`, không nằm trong bốn tab của `bundle` (có thể thêm vào `bundle` nếu muốn, nhưng chuẩn hiện tại là bốn tab).

### 4.11. Trạng thái, thành phần, triển khai, gói (`statemachine`, `component`, `deployment`, `package`)

Bốn loại thêm 10/11/2026, cùng phong cách đen trắng, cùng quy trình JSON trước. Mỗi loại có mẫu phân tích riêng (ký hiệu và nghĩa, phiếu, khung JSON, lỗi hay gặp): `agents/knowledge/diagrams/mau-phan-tich/{state-machine,component,deployment,package}.md`; mẫu JSON `ve-so-do.py --mau <type>`. Danh sách đầy đủ mọi loại sơ đồ và quyết định chưa làm công cụ: `agents/knowledge/diagrams/ma-tran-loai-so-do.md`. Tóm tắt luật của công cụ:
- **statemachine:** đúng một `initial` mỗi vùng (không chuyển vào, đúng một chuyển ra); `final` không chuyển ra; `choice` có ít nhất 2 chuyển ra với `[điều kiện]`; mọi trạng thái với tới được từ `initial`; trạng thái cụt chưa phải `final` bị cảnh báo; hai chuyển cùng nhãn từ một trạng thái bị cảnh báo; trạng thái ghép dùng `parent`.
- **component:** giao diện cung cấp là chấm tròn (`provides`); thành phần cần giao diện dùng `connections` `kind: uses` cộng `interface`, `to` phải `provides` giao diện đó (nếu không là LỖI); giao diện không ai dùng và thành phần cô lập bị cảnh báo; chấm tròn tự đặt phía thành phần dùng nó.
- **deployment:** `stereo` là `device`, `executionEnvironment` hoặc `node`; artifact nằm trong nút (`artifacts`), nút lồng nhau dùng `children`; một nút chỉ có một nút cha; nút không có đường nối bị cảnh báo.
- **package:** `kind` là `use`, `import`, `access`, `merge`; phụ thuộc VÒNG giữa các gói bị cảnh báo; gói không có phụ thuộc bị cảnh báo.
Quy tắc nội dung dùng chung: mọi tên (trạng thái, thành phần, nút, gói) lấy từ nguồn thật; mẫu `mau/*.json` là ví dụ minh họa, KHÔNG chép nội dung.

### 4.12. Luật KHÔNG ĐÈ (mọi loại sơ đồ, bắt buộc)

Người xem phải đọc được từng nét và từng chữ. Công cụ `ve-so-do.py --check-only` báo CẢNH BÁO cho các lỗi sau; mỗi cảnh báo phải sửa trong JSON (hoặc ghi lý do) trước khi xuất ảnh:
1. **Nét không đè nét:** hai đường nối khác nguồn và khác đích không được có đoạn thẳng nằm chồng lên nhau (người xem tưởng là một quan hệ). Nhiều đường cùng ĐÍCH chỉ được gộp ở đoạn cuối ngắn (tối đa 40px); muốn tách thì cho mỗi đường một `via` riêng (cách nhau 14 đến 16px) và `yin` (dời điểm vào dọc cạnh của đích, activity). Thứ tự rãnh: nguồn nằm trên dùng rãnh bên trái, điểm vào thấp hơn; nếu không các đường sẽ cắt nhau.
2. **Nét không xuyên hộp:** đường nối không đi xuyên qua hộp, ghi chú hay nút khác (kể cả ghi chú đặt dưới nút kết thúc). Đổi cột, thêm `via`, hoặc dời hộp.
3. **Chữ không đè chữ, không đè hộp, không bị nét lạ cắt qua:** nhãn cạnh không chồng nhãn khác, không nằm lên hộp không phải đầu mút, không bị đường của cạnh khác gạch ngang. Nhãn dài phải RÚT NGẮN (chi tiết đã có trong hộp) hoặc dời bằng `lab_x`. Nhãn cạnh quyết định ngắn gọn (`Có: lỗi`), không chép cả điều kiện.
4. **Sequence:** nhãn thông điệp tự xuống dòng cho vừa khoảng cách hai đường đời và có nền trắng để đường đời của đối tượng ở giữa không gạch qua chữ. Không nối chữ dài một dòng tràn sang cột khác.
5. **ERD:** đường có nhãn được vẽ sau cùng; nhãn ngắn (`3 khóa FK`) để không bị đường quan hệ khác cắt.
Quy trình: vẽ, `--check-only`, sửa hết cảnh báo đè, xuất ảnh, MỞ ẢNH nhìn lại; công cụ chỉ kiểm hình chữ nhật và đoạn thẳng nên mắt người vẫn là lớp kiểm cuối. Bài học UC-04 (11/2026): nhiều đường lỗi dồn một trục dọc và nhãn dài là lỗi hay gặp nhất; ghi chú đặt dưới nút kết thúc bị đường đi qua.

## 5. Phần chung cho mọi loại

- Màu và nhãn: đỏ là lỗi, xanh lá là thành công hoặc bảng chính, xanh dương là tham chiếu; mọi tên kỹ thuật kèm nghĩa (xem bài học mục 7).
- Chữ Việt có dấu, tên mã (lớp, hàm, bảng) giữ nguyên.
- Một file `.drawio` có thể gom nhiều trang cho một chức năng; mỗi sơ đồ một spec riêng, tên trang ổn định.

## 6. Loại sơ đồ chưa có công cụ `ve-so-do.py`

Vòng đời và trạng thái, kiến trúc, thành phần, triển khai: dùng archify (`quy-uoc-draw-io-va-archify.md`). Mockup: script riêng của workspace. Communication, timing, interaction overview, profile, user story map: chưa có công cụ.
- Vẫn bắt buộc các bước 1, 2, 6, 7, 8 (đọc mẫu, bảng sự thật, xem ảnh, nhúng, báo cáo).
- Ghi rõ trong báo cáo: **"không qua spec JSON, chưa có công cụ"**.
- Lần thứ hai gặp cùng loại thì đề xuất thêm `type` mới vào `ve-so-do.py` thay vì viết thêm script riêng.

## 7. Mẫu báo cáo ba dòng

```
Sơ đồ: <tên> (<loại>), spec: <đường dẫn .spec.json>
KIỂM: đạt (0 cảnh báo) / còn N cảnh báo: <lý do chấp nhận>
Ảnh: đã xem từng hộp, đường / CHƯA xem ảnh, mới kiểm bằng script
```

## 8. Khi người dùng sửa tay file `.drawio`

JSON và `.drawio` phải luôn khớp nhau. Công cụ bảo vệ như sau:

- **Mỗi lần sinh**, công cụ ghi thêm file `<tên>.drawio.sha` (mã băm của file vừa sinh). Lần chạy sau, nếu `.drawio` khác mã băm đó (người dùng đã mở và lưu trong draw.io), công cụ **dừng với mã thoát 2 và KHÔNG ghi đè**, rồi nêu hai lối:
  1. Giữ chỉnh sửa tay, cập nhật JSON: `python3 ~/Documents/agent-base/scripts/ve-so-do.py <spec> --lay-tu-drawio`
  2. Bỏ chỉnh sửa tay, dựng lại từ JSON: chạy lại với `--ghi-de`
- **`--lay-tu-drawio`** so file `.drawio` đã sửa với bản vừa dựng từ JSON và ghi phần khác biệt ngược vào JSON:

| Người dùng sửa trong draw.io | Có đồng bộ về JSON không |
|---|---|
| Dời hộp lớp, nút, bảng | Có (ghi `x`, `y`, và `w` với lớp; dùng vị trí ép cứng) |
| Sửa chữ: tên lớp, thuộc tính, hàm, nhãn nút, tên bảng, tên đối tượng, nhãn thông điệp | Có |
| Thêm, xóa, nối lại **đường nối** | **Không** (công cụ in cảnh báo; sửa `relations`, `edges`, `messages` trong JSON bằng tay) |
| Thêm ô mới, đổi màu, đổi kiểu | **Không** (cảnh báo nếu thêm ô; màu và kiểu mất khi dựng lại với `--ghi-de`) |
| Sửa cột trong bảng ERD, đổi thứ tự thông điệp tuần tự | **Không** (sửa JSON) |

- Công cụ đọc được `.drawio` ở dạng văn bản. Nếu draw.io lưu dạng nén thì báo lỗi; nhờ người dùng bỏ chọn "Nén" (Tệp, Thuộc tính).
- Các ô có mã cố định theo mã trong JSON (`cls_<id>`, `node_<id>`, `tbl_<id>`, `par_<id>`, `msg_<k>`); **không đổi mã ô** khi sửa tay, nếu không đồng bộ ngược không nhận ra.
- Đường nối của lưu đồ, sơ đồ nhiều làn và sơ đồ lớp **gắn vào ô**: người dùng kéo ô thì đường đi theo.
- Quy trình khi người dùng nói "tôi vừa sửa sơ đồ": chạy `--lay-tu-drawio`, đọc các dòng `ĐỒNG BỘ` và `CẢNH BÁO`, báo lại người dùng điều nào đã vào JSON, điều nào chưa; không chạy `--ghi-de` khi chưa được đồng ý.

## 8b. Bài học khi dựng bộ sơ đồ UC-04 theo mẫu anhbv (09/11/2026)

1. **Học từ mẫu trước khi vẽ:** mở ảnh mẫu, ghi các điểm khác với luật hiện có (số điểm kết thúc, cách phân làn, ERD nối bảng hay cột) và hỏi người dùng chốt, đừng tự giữ luật cũ hay tự theo mẫu.
2. **Một loại sơ đồ một tab.** Đếm tab trước khi nộp: ERD, Class, Sequence, Activity là đủ. Nhiều tab nhỏ là dấu hiệu chia sai.
3. **Phân làn theo lớp, không theo vai**, và đặt làn theo thứ tự gọi (Controller, validate, truy vấn, toPredicate, CSDL). Hai lớp gọi nhau liên tục thì đặt kề nhau để mũi tên ngắn.
4. **Đặt hàng (`row`) theo thời gian chạy**, rồi kiểm cảnh báo "đường cắt qua hộp": sửa bằng `sub`, `first: "v"`, `via`, hoặc thêm nút nối (`junc`), không để cảnh báo tồn đọng.
5. **Nhãn lỗi ngắn trên cạnh, mã lỗi chi tiết để trong tài liệu**; nhiều cạnh lỗi cùng đổ về một nút lỗi chung thì ngắn gọn hơn một nút lỗi cho mỗi nhánh.
6. **Mỗi lần đổi công cụ phải chạy lại `srs-check.py --full` và `diagram-describe.py --check`**: kiểm cũ đòi đúng một điểm kết thúc nên đã báo lỗi giả; đã sửa để nhận ra sơ đồ activity theo làn lớp qua hộp chú giải.
7. **Công cụ có lỗi riêng, không chỉ agent có lỗi.** Lần Gemini vẽ thử lộ ra: ERD cho hai quan hệ khác nhau dùng chung một đoạn đường (đã sửa: mỗi quan hệ một đường dọc riêng, quan hệ có khóa chính ở bên trái lấy đường bên trái) và công cụ không bắt nhãn chồng nhau (đã thêm kiểm nhãn, kiểm đoạn chung). Mỗi lần có agent khác vẽ thử, đối chiếu ảnh với danh sách mục 4.9 rồi vá cả công cụ lẫn tri thức.
8. **Xem ảnh sau mỗi lần sinh.** Lần đầu cạnh [Có] đi xuyên qua hộp lỗi và nhãn dồn giữa đường dài; chỉ thấy khi xem ảnh.

## 9. Giới hạn đã biết

- Kiểm bằng chữ phát hiện hộp chồng nhau, đường cắt hộp, thiếu nhãn và lỗi cấu trúc; **không phát hiện** nhãn đè nhãn hay chữ tràn do phông. Nó không thay việc xem ảnh.
- Chưa kiểm chứng bằng agent Gemini; quy trình viết để agent không xem được ảnh vẫn làm được và báo trung thực.
- Bố trí theo cột đơn giản; sơ đồ rất dày cần chỉnh `col`, `via`, `w` vài lượt.
