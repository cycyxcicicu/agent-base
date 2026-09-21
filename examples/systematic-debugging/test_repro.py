"""
Test Harness Tái Hiện Lỗi (Feedback Loop) - Chuẩn pocock-skills / diagnosing-bugs
Đặc tính:
1. Red-capable: Gây lỗi chính xác trên BuggyTokenBucket và xanh trên FixedTokenBucket.
2. Deterministic: Pin mốc thời gian ảo (Virtual Time), không phụ thuộc vào time.sleep ngẫu nhiên.
3. Fast: Chạy hoàn tất trong dưới 0.05 giây.
"""

import sys
import argparse

# Thiết lập UTF-8 cho terminal Windows chống lỗi mã hóa
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from rate_limiter import BuggyTokenBucket, FixedTokenBucket

def run_feedback_loop(bucket_cls, verbose=True):
    # Kịch bản: Dung lượng 5 tokens, tốc độ nạp 2 tokens / giây
    # Sau khi dùng hết 5 tokens tại t=0, gửi 5 requests cách nhau 0.6 giây.
    # Tại mỗi 0.6s, với tốc độ 2 tokens/s, lượng nạp là 1.2 tokens -> Mỗi request đều PHẢI ĐƯỢC CHẤP NHẬN.
    bucket = bucket_cls(capacity=5.0, refill_rate_per_sec=2.0)
    
    virtual_time = 1000.0
    # Bước 1: Tiêu thụ toàn bộ 5 tokens ban đầu
    for i in range(5):
        allowed = bucket.allow_request(1.0, current_time=virtual_time)
        assert allowed, f"Lỗi khởi tạo: Request khởi đầu {i+1} phải thành công!"

    if verbose:
        print(f"[{bucket_cls.__name__}] Đã dùng hết 5 tokens ban đầu tại t={virtual_time:.1f}s.")

    # Bước 2: Gửi liên tiếp 5 requests, mỗi request cách nhau 0.6 giây
    # Kỳ vọng: Mọi request đều được chấp nhận vì 0.6s * 2 tokens/s = 1.2 tokens > 1.0 needed.
    success_count = 0
    failure_count = 0

    for step in range(1, 6):
        virtual_time += 0.6
        allowed = bucket.allow_request(1.0, current_time=virtual_time)
        if allowed:
            success_count += 1
            if verbose:
                print(f"  t={virtual_time:.1f}s: Request {step} -> ✅ CHẤP NHẬN (Tokens còn: {bucket.tokens:.2f})")
        else:
            failure_count += 1
            if verbose:
                print(f"  t={virtual_time:.1f}s: Request {step} -> ❌ BỊ CHẶN SAI LẦM (Tokens còn: {bucket.tokens:.2f})")

    # Đánh giá kết quả
    if failure_count > 0:
        raise AssertionError(
            f"BẮT ĐƯỢC LỖI TÁI HIỆN (RED SIGNAL): Có {failure_count}/5 requests bị chặn oan uổng do lỗi làm tròn số nguyên!"
        )
    
    if verbose:
        print(f"[{bucket_cls.__name__}] 🎉 TẤT CẢ 5 REQUESTS ĐỀU ĐƯỢC PHÊ DUYỆT THÀNH CÔNG (GREEN SIGNAL)!\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Chạy Feedback Loop kiểm thử lỗi Rate Limiter")
    parser.add_argument("--mode", choices=["buggy", "fixed", "all"], default="buggy", help="Chọn phiên bản cần test")
    args = parser.parse_args()

    print(f"--- BẮT ĐẦU CHẠY FEEDBACK LOOP ĐIỀU TRA LỖI (Mode: {args.mode}) ---")

    if args.mode in ["buggy", "all"]:
        print("\n🧪 [Pha 1 & Pha 2] Chạy Feedback Loop trên phiên bản lỗi (Buggy)...")
        try:
            run_feedback_loop(BuggyTokenBucket)
            print("❌ Lỗi: Test không bắt được bug (Test chưa đủ chặt chẽ)!")
            sys.exit(1)
        except AssertionError as e:
            print(f"🔴 TÍN HIỆU ĐỎ THÀNH CÔNG: {e}")
            if args.mode == "buggy":
                print("\n-> Chu trình chẩn đoán: Pha 1 hoàn tất (Đã có test deterministic đỏ đúng bug).")
                sys.exit(1)

    if args.mode in ["fixed", "all"]:
        print("\n🧪 [Pha 5] Chạy lại Feedback Loop trên phiên bản đã sửa (Fixed)...")
        try:
            run_feedback_loop(FixedTokenBucket)
            print("🟢 TÍN HIỆU XANH: Test vượt qua 100%, bug đã được dập tắt triệt để!")
            sys.exit(0)
        except AssertionError as e:
            print(f"❌ Sửa lỗi thất bại: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
