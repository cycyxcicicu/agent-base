# Cài agent-base vào dự án và đồng bộ ngược

`agent-base` là **nguồn** của bộ khung. Mỗi dự án chỉ là một bản cài. Cải tiến dùng chung phát hiện ở dự án nào cũng phải quay về `agent-base`, nếu không dự án sau lại gặp lại lỗi cũ.

## 1. Cái gì là "khung", cái gì là "của dự án"

Danh sách chính thức: **`agents/manifest.txt`**. Chỉ những gì có trong đó mới được mang sang dự án và mới cần đồng bộ ngược.

| Loại | Ví dụ | Sửa ở dự án thì |
|---|---|---|
| Khung dùng chung (`copy` trong manifest) | `scripts/*.py`, `agents/protocols/*`, `agents/roles/*`, `agents/stacks/*`, `tasks/_template.md`, `.githooks/*` | **đưa ngược về agent-base** nếu không gắn với riêng dự án |
| File sinh ra (`generated`) | `.kilo/agents/*`, `.agents/rules/*`, `GEMINI.md`, `CODEX.md` | không sửa tay; sửa nguồn rồi chạy `sync-adapters` |
| Mẫu của dự án | `PROJECT.md`, `tasks/EPICS.md`, `agents/models.txt` | **giữ ở dự án**. Chỉ đưa ngược khi đổi *cấu trúc hoặc hướng dẫn* của mẫu, không đưa *nội dung* dự án |
| Của riêng dự án | `tasks/T-*`, `docs/*`, code | không bao giờ đưa ngược |

## 2. Cài vào dự án mới

Người dùng (hoặc AI được người dùng giao, đưa đường dẫn agent-base) chạy **từ thư mục agent-base**:

```
python scripts/bootstrap-project.py --target <thư mục dự án> --mode hidden   # agent-base chỉ nằm trên máy
python scripts/bootstrap-project.py --target <thư mục dự án> --mode git      # agent-base lên git của dự án
```

- Luôn chạy `--dry-run` trước nếu dự án đã có file.
- `--mode hidden` cần `git init` ở dự án trước; script tự ghi `.git/info/exclude`.
- Script không ghi đè file đã có, và ghi `.agent-base.json` (nguồn + băm từng file) làm mốc đồng bộ.
- Sau đó làm theo `agents/protocols/onboarding.md`.

## 3. Quy định đồng bộ ngược (bắt buộc)

1. **Agent sửa file khung** trong dự án (bất kể lý do) phải ghi vào ghi chú bàn giao, mục **"Thay đổi dùng chung cho agent-base"**: file nào, sửa gì, vì sao, có dùng chung được không.
2. **Writer**, khi gộp ghi chú sau merge, chép các mục đó vào `docs/PROJECT-NOTES.md`, phần "Chờ đưa về agent-base".
3. **Định kỳ** (cuối mỗi giai đoạn, hoặc ngay khi sửa lỗi của chính bộ khung), người dùng hoặc Lead chạy **ở dự án**:
   ```
   python scripts/agent-base-diff.py
   ```
   Script chia file khung thành: dự án đã sửa (cần đưa ngược), agent-base đã cập nhật (cần kéo về), cả hai cùng sửa (gộp tay).
4. Đưa ngược **từng file đã xem diff**: `python scripts/agent-base-diff.py --push <file>...`. Không đẩy file gắn với riêng dự án.
5. Ở **agent-base**: chạy `python scripts/sync-adapters.py`, chạy test, cập nhật `README.md` / `onboarding.md` nếu cách dùng đổi, rồi người dùng commit qua nhánh riêng và Merge Request (không commit thẳng `main`).
6. Thêm file khung **mới** thì thêm luôn vào `agents/manifest.txt`, nếu không `bootstrap-project.py` sẽ không mang sang dự án sau.
7. Hai bên đã khớp thì chạy ở dự án: `python scripts/agent-base-diff.py --mark-synced`.

Sửa `AGENTS.md` hoặc `agents/roles/` vẫn theo quy tắc chung: **chỉ người dùng** sửa hoặc cho phép rõ ràng, ở cả dự án lẫn agent-base.

## 4. Kéo cập nhật từ agent-base về dự án đang chạy

```
python scripts/agent-base-diff.py            # xem mục "agent-base đã cập nhật"
python scripts/agent-base-diff.py --pull <file>...
python scripts/sync-adapters.py
```

Mở phiên agent mới sau khi kéo về: phiên cũ vẫn giữ quy tắc cũ trong ngữ cảnh.
