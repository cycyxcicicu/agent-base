"""
Module Rate Limiter: Dịch vụ kiểm soát tần suất request theo thuật toán Token Bucket.
Bao gồm phiên bản có lỗi (Buggy) và phiên bản đã khắc phục chuẩn chỉ (Fixed).
"""

import time

class BuggyTokenBucket:
    """
    Phiên bản có lỗi: Lỗi làm tròn số nguyên (Floor Division) và cập nhật timestamp sai thời điểm.
    Hậu quả: Khi các request đến với khoảng cách nhỏ (sub-second), lượng token được nạp
    bị làm tròn về 0, dẫn đến chặn nhầm người dùng hợp lệ trong các chu kỳ request nhanh.
    """
    def __init__(self, capacity: float, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate_per_sec)
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def allow_request(self, tokens_needed: float = 1.0, current_time: float = None) -> bool:
        now = current_time if current_time is not None else time.time()
        elapsed = now - self.last_refill

        # LỖI TẠI ĐÂY: Ép kiểu int làm mất phần thập phân của elapsed time
        # Ví dụ: nếu elapsed = 0.4s và refill_rate = 2 tokens/s -> elapsed * refill_rate = 0.8
        # int(0.8) = 0! Không có token nào được nạp, và last_refill bị reset sai!
        refill_tokens = int(elapsed * self.refill_rate)
        if refill_tokens > 0:
            self.tokens = min(self.capacity, self.tokens + refill_tokens)
            self.last_refill = now  # Cập nhật sai khiến thời gian dư bị mất

        if self.tokens >= tokens_needed:
            self.tokens -= tokens_needed
            return True
        return False


class FixedTokenBucket:
    """
    Phiên bản đã sửa lỗi sau chu trình 4-Phase Systematic Debugging:
    - Giữ độ chính xác dấu phẩy động (float) cho token.
    - Cập nhật last_refill chính xác theo lượng token thực tế đã nạp (không làm mất thời gian dư).
    """
    def __init__(self, capacity: float, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate_per_sec)
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def allow_request(self, tokens_needed: float = 1.0, current_time: float = None) -> bool:
        now = current_time if current_time is not None else time.time()
        elapsed = max(0.0, now - self.last_refill)

        # Tính toán chính xác số token cần nạp dưới dạng float
        refill_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + refill_tokens)
        self.last_refill = now

        if self.tokens >= tokens_needed:
            self.tokens -= tokens_needed
            return True
        return False
