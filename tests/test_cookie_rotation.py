import os
import sys
import time
import asyncio
import unittest
from pathlib import Path

# Thêm đường dẫn thư mục agent-base vào sys.path
AGENT_BASE_DIR = Path(__file__).resolve().parent.parent
if str(AGENT_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_BASE_DIR))

# Đảm bảo import được gói nội bộ tools/gemini-api/src
_gemini_src = str(AGENT_BASE_DIR / "tools" / "gemini-api" / "src")
if _gemini_src not in sys.path:
    sys.path.insert(0, _gemini_src)

from tools.cookie_rotation.account_manager import GeminiAccount, AccountPool, ConcurrentWorkerPool

class TestCookieRotation(unittest.TestCase):
    def setUp(self):
        self.acc1 = GeminiAccount(account_id=1, secure_1psid="mock_psid_1", secure_1psidts="mock_ts_1", name="TestAcc 1")
        self.acc2 = GeminiAccount(account_id=2, secure_1psid="mock_psid_2", secure_1psidts="mock_ts_2", name="TestAcc 2")

        # Gắn mock client để kiểm thử logic xoay vòng mà không gọi mạng thực tế
        class MockClient:
            def __init__(self, acc_id):
                self.acc_id = acc_id
                self._running = True

            async def generate_content(self, prompt, files=None):
                return type("Resp", (), {"text": f"Response from {self.acc_id}", "images": []})()

            async def close(self):
                self._running = False

        self.acc1.client = MockClient(1)
        self.acc2.client = MockClient(2)

    def test_account_cooldown_and_restore(self):
        """Kiểm tra cơ chế cooldown khi chạm quota và tự động khôi phục sau khi hết thời gian."""
        self.assertTrue(self.acc1.is_available())
        
        # Đánh dấu chạm hạn ngạch (cooldown ngắn 0.3 giây để test)
        self.acc1.mark_exhausted(cooldown_seconds=0.3)
        self.assertTrue(self.acc1.is_quota_exhausted)
        self.assertFalse(self.acc1.is_available())

        # Chờ cooldown kết thúc
        time.sleep(0.4)
        self.assertTrue(self.acc1.is_available())
        self.assertFalse(self.acc1.is_quota_exhausted)

    def test_account_pool_round_robin(self):
        """Kiểm tra thuật toán luân chuyển Round-Robin giữa các tài khoản khỏe mạnh."""
        pool = AccountPool()
        pool.accounts = [self.acc1, self.acc2]
        
        first = pool.get_next_account()
        second = pool.get_next_account()
        third = pool.get_next_account()

        self.assertEqual(first.account_id, 1)
        self.assertEqual(second.account_id, 2)
        self.assertEqual(third.account_id, 1)

    def test_execute_with_rotation_failover(self):
        """Kiểm tra khi tài khoản 1 gặp lỗi 429 quota, hệ thống tự động xoay sang tài khoản 2."""
        pool = AccountPool()
        pool.accounts = [self.acc1, self.acc2]

        call_log = []

        async def failing_op(account: GeminiAccount):
            call_log.append(account.account_id)
            if account.account_id == 1:
                raise RuntimeError("429 Resource has been exhausted (quota exceeded)")
            return f"Success on Acc {account.account_id}"

        result = asyncio.run(pool.execute_with_rotation(failing_op))
        
        # Kết quả phải trả về thành công từ tài khoản 2
        self.assertEqual(result, "Success on Acc 2")
        self.assertIn(1, call_log)
        self.assertIn(2, call_log)
        self.assertTrue(self.acc1.is_quota_exhausted)
        self.assertFalse(self.acc2.is_quota_exhausted)

    def test_concurrent_worker_pool_execution(self):
        """Kiểm tra bể worker xử lý đồng thời với nhiều tài khoản."""
        pool = AccountPool()
        pool.accounts = [self.acc1, self.acc2]
        worker_pool = ConcurrentWorkerPool(pool, max_workers=2)

        items = ["item_a", "item_b", "item_c", "item_d"]

        async def sample_task(account: GeminiAccount, item: str):
            await asyncio.sleep(0.01)
            return f"{item}_processed_by_{account.account_id}"

        results = asyncio.run(worker_pool.run_batch(items, sample_task))
        self.assertEqual(len(results), 4)
        for i, it in enumerate(items):
            self.assertTrue(results[i].startswith(f"{it}_processed_by_"))

if __name__ == "__main__":
    unittest.main()
