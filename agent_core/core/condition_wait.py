"""
Condition-Based Waiting.
Học hỏi từ: superpowers (Trừ khử kiểm thử chập chờn Flaky Tests - cấm dùng sleep tĩnh).
"""

import time
import asyncio
from typing import Callable, Any, Optional


def wait_until(
    predicate: Callable[[], bool],
    timeout: float = 10.0,
    interval: float = 0.05,
    error_message: str = "Hết thời gian chờ điều kiện hoàn thành"
) -> bool:
    """
    Chờ đồng bộ cho tới khi điều kiện predicate() trả về True hoặc chạm ngưỡng timeout.
    Loại bỏ hoàn toàn sleep(5) tĩnh gây chậm trễ hoặc thất bại ngẫu nhiên.
    Lưu trữ nguyên nhân lỗi (exception / assertion error) để hỗ trợ debug khi timeout.
    """
    start_time = time.time()
    last_exception: Optional[Exception] = None
    while time.time() - start_time < timeout:
        try:
            if predicate():
                return True
        except Exception as e:
            last_exception = e
        time.sleep(interval)
    
    err_suffix = f" - Lỗi kiểm tra cuối: {type(last_exception).__name__}: {last_exception}" if last_exception else ""
    if last_exception:
        raise TimeoutError(f"{error_message} (sau {timeout}s){err_suffix}") from last_exception
    raise TimeoutError(f"{error_message} (sau {timeout}s)")


async def wait_until_async(
    predicate: Callable[[], Any],
    timeout: float = 10.0,
    interval: float = 0.05,
    error_message: str = "Hết thời gian chờ điều kiện hoàn thành"
) -> bool:
    """
    Chờ bất đồng bộ cho tới khi predicate() trả về True hoặc chạm ngưỡng timeout.
    """
    start_time = time.time()
    last_exception: Optional[Exception] = None
    while time.time() - start_time < timeout:
        try:
            res = predicate()
            if asyncio.iscoroutine(res):
                res = await res
            if res:
                return True
        except Exception as e:
            last_exception = e
        await asyncio.sleep(interval)

    err_suffix = f" - Lỗi kiểm tra cuối: {type(last_exception).__name__}: {last_exception}" if last_exception else ""
    if last_exception:
        raise TimeoutError(f"{error_message} (sau {timeout}s){err_suffix}") from last_exception
    raise TimeoutError(f"{error_message} (sau {timeout}s)")
