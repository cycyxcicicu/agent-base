# Sổ tay vận hành (Runbook): CLI Kiểm chứng Thực thi & Tái hiện lỗi

Runbook cung cấp hướng dẫn từng bước vận hành công cụ `scripts/verify.py` và `scripts/proof-check.py` kèm các bằng chứng chạy thật trên môi trường máy chủ.

---

## 1. Chuẩn bị môi trường
- Python 3.11+ stdlib (không cần cài thêm dependency).
- Thư mục lưu bằng chứng kiểm chứng: `build/evidence/` (mặc định đã được `.gitignore` bỏ qua).

---

## 2. Quy trình kiểm chứng cài đặt mới (Bootstrap Verification)

### Lệnh thực thi:
```bash
python scripts/verify.py bootstrap --evidence-root build/evidence
```

### Bằng chứng chạy thật (Output):
```text
🚀 Bắt đầu kiểm chứng thực tế recipe: BOOTSTRAP...

=======================================================
KẾT QUẢ KIỂM CHỨNG [BOOTSTRAP]: ✅ PASS
=======================================================
📄 Tệp proof bundle: build\evidence\bootstrap-20261028-013745\proof.json
📊 Run ID: bootstrap-20261028-013745
🎯 Assertions:
  * [PASS] assert-exit-code-0: exit 0
  * [PASS] assert-agent-base-metadata: Tồn tại
  * [PASS] assert-fresh-templates-generated: Tồn tại
🧹 Cleanup performed: True
```

---

## 3. Quy trình kiểm chứng nâng cấp dự án (Upgrade Verification)

### Lệnh thực thi:
```bash
python scripts/verify.py upgrade --evidence-root build/evidence
```

### Bằng chứng chạy thật (Output):
```text
🚀 Bắt đầu kiểm chứng thực tế recipe: UPGRADE...

=======================================================
KẾT QUẢ KIỂM CHỨNG [UPGRADE]: ✅ PASS
=======================================================
📄 Tệp proof bundle: build\evidence\upgrade-20261028-013747\proof.json
📊 Run ID: upgrade-20261028-013747
🎯 Assertions:
  * [PASS] assert-dry-run-safe: Hash trước=..., sau=...
  * [PASS] assert-report-conflicts: Đã phát hiện và liệt kê khác biệt
  * [PASS] assert-preserve-customization: Bảo toàn thành công
  * [PASS] assert-idempotent-rerun: Khớp 100% băm cấu trúc
🧹 Cleanup performed: True
```

---

## 4. Quy trình tái hiện lỗi 2 lần có reset (Bug Repro)

### Chuẩn bị file recipe mẫu `build/recipe-sample.json`:
```json
{
  "name": "sample-cli-repro",
  "command": ["python", "-c", "import sys; sys.exit(1)"],
  "expected_bug_exit_code": 1,
  "reset_action": "noop"
}
```

### Lệnh thực thi:
```bash
python scripts/verify.py repro --recipe build/recipe-sample.json --evidence-root build/evidence
```

### Bằng chứng chạy thật (Output):
```text
🚀 Bắt đầu tái hiện lỗi hai lần có reset theo recipe: sample-cli-repro...

=======================================================
KẾT QUẢ KIỂM CHỨNG [REPRO]: ✅ PASS
=======================================================
📄 Tệp proof bundle: build\evidence\repro-sample-cli-repro-20261028-014030\proof.json
📊 Run ID: repro-sample-cli-repro-20261028-014030
🎯 Assertions:
  * [PASS] assert-repro-consistency: Lần 1: exit 1, Lần 2: exit 1 -> reproduced
🧹 Cleanup performed: True
```

---

## 5. Thẩm định độc lập bằng chứng (Proof Check)

### Lệnh thực thi:
```bash
python scripts/proof-check.py --bundle build/evidence/bootstrap-20261028-013745/proof.json
```

### Kết quả mong đợi:
```text
✅ Bằng chứng hợp lệ 100%: proof.json
```
*(Nếu tệp artifact bị sửa đổi hoặc thiếu sót, lệnh sẽ trả về mã thoát 1 và chỉ rõ tên tệp sai lệch).*
