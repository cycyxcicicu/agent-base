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
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if predicate():
                return True
        except Exception:
            pass
        time.sleep(interval)
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
    while time.time() - start_time < timeout:
        try:
            res = predicate()
            if asyncio.iscoroutine(res):
                res = await res
            if res:
                return True
        except Exception:
            pass
        await asyncio.sleep(interval)
    raise TimeoutError(f"{error_message} (sau {timeout}s)")
