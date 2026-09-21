"""
Resilience & Retry Policies with Exponential Backoff and Full Jitter.
Học hỏi từ: google-skills & superpowers
"""

import time
import random
import asyncio
from typing import Callable, Type, Tuple, Optional, Any
from functools import wraps


def calculate_backoff(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: bool = True
) -> float:
    """Tính toán thời gian chờ lũy thừa kèm full jitter theo chuẩn Google Cloud."""
    delay = min(max_delay, base_delay * (2 ** attempt))
    if jitter:
        return random.uniform(0, delay)
    return delay


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retry_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True
):
    """Decorator tự động thử lại tác vụ đồng bộ/bất đồng bộ với exponential backoff."""
    def decorator(func: Callable):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                last_err = None
                for attempt in range(max_attempts):
                    try:
                        return await func(*args, **kwargs)
                    except retry_exceptions as e:
                        last_err = e
                        if attempt == max_attempts - 1:
                            raise
                        delay = calculate_backoff(attempt, base_delay, max_delay, jitter)
                        await asyncio.sleep(delay)
                raise last_err
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                last_err = None
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except retry_exceptions as e:
                        last_err = e
                        if attempt == max_attempts - 1:
                            raise
                        delay = calculate_backoff(attempt, base_delay, max_delay, jitter)
                        time.sleep(delay)
                raise last_err
            return sync_wrapper
    return decorator


class CircuitBreaker:
    """
    Circuit Breaker Pattern: Tự động ngắt kết nối tạm thời khi phát hiện tỷ lệ lỗi vượt ngưỡng.
    Trạng thái: CLOSED (bình thường) -> OPEN (ngắt mạch) -> HALF_OPEN (thử nghiệm hồi phục).
    """
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = self.CLOSED
        self.last_state_change = time.time()

    def record_success(self):
        self.failure_count = 0
        self.state = self.CLOSED

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = self.OPEN
            self.last_state_change = time.time()

    def allow_request(self) -> bool:
        if self.state == self.CLOSED:
            return True
        if self.state == self.OPEN:
            if time.time() - self.last_state_change >= self.recovery_timeout:
                self.state = self.HALF_OPEN
                return True
            return False
        if self.state == self.HALF_OPEN:
            return True
        return True
