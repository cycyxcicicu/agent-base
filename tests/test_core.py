import unittest
import time
from agent_core.core.resilience import calculate_backoff, CircuitBreaker, retry_with_backoff
from agent_core.core.condition_wait import wait_until
from agent_core.core.json_safe import SafeJsonWrapper
from agent_core.core.telemetry import ProofValidator, verify_iron_law


class TestCoreModules(unittest.TestCase):
    def test_calculate_backoff(self):
        delay = calculate_backoff(attempt=2, base_delay=1.0, max_delay=10.0, jitter=False)
        self.assertEqual(delay, 4.0)

    def test_circuit_breaker(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.2)
        self.assertTrue(cb.allow_request())
        cb.record_failure()
        self.assertTrue(cb.allow_request())
        cb.record_failure()
        # Chạm ngưỡng: Phải ngắt mạch (OPEN)
        self.assertFalse(cb.allow_request())
        time.sleep(0.25)
        # Hết timeout: Phải chuyển sang HALF_OPEN và cho phép thử
        self.assertTrue(cb.allow_request())

    def test_condition_wait(self):
        flag = {"done": False}
        def mark():
            flag["done"] = True
        import threading
        threading.Timer(0.1, mark).start()
        # Chờ điều kiện không dùng sleep tĩnh
        res = wait_until(lambda: flag["done"], timeout=1.0, interval=0.02)
        self.assertTrue(res)

    def test_safe_json(self):
        sample = {"name": "Antigravity", "value": 100, "unicode": "Tiếng Việt có dấu"}
        encoded = SafeJsonWrapper.dumps(sample)
        decoded = SafeJsonWrapper.loads(encoded)
        self.assertEqual(decoded["unicode"], "Tiếng Việt có dấu")

    def test_proof_validator(self):
        proof = ProofValidator.execute_and_prove("python -c \"print('OK')\"")
        self.assertTrue(verify_iron_law(proof))
        self.assertEqual(proof["stdout"], "OK")

    def test_patch_orjson_globally(self):
        from agent_core.core.json_safe import patch_orjson_globally, HAS_ORJSON
        if not HAS_ORJSON:
            return
        import orjson
        self.assertTrue(patch_orjson_globally())
        # Test giải mã byte chuỗi dị thường không bị văng lỗi
        bad_bytes = b'{"status": "ok", "bad": "hello \xff world"}'
        res = orjson.loads(bad_bytes)
        self.assertEqual(res["status"], "ok")
        self.assertIn("hello", res["bad"])


if __name__ == "__main__":
    unittest.main()
