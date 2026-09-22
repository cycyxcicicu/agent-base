import os
import json
import asyncio
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import time
import sys

# Thiết lập UTF-8 trên terminal Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Định vị thư mục gốc agent-base và nạp thư viện gemini_webapi nội bộ
AGENT_BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(AGENT_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_BASE_DIR))
_gemini_src = str(AGENT_BASE_DIR / "tools" / "gemini-api" / "src")
if _gemini_src not in sys.path:
    sys.path.insert(0, _gemini_src)

# Kích hoạt lớp bảo vệ orjson trong RAM để gemini_webapi không bị crash bởi byte lỗi
from agent_core.core.json_safe import patch_orjson_globally
patch_orjson_globally()

from gemini_webapi import GeminiClient
try:
    from .cookie_rotator import rotate_and_save_1psidts
except ImportError:
    from cookie_rotator import rotate_and_save_1psidts


class GeminiAccount:
    """Đại diện cho một tài khoản Gemini với trạng thái hoạt động, hạn mức và cooldown."""
    def __init__(self, account_id: int, secure_1psid: str, secure_1psidts: str, name: str = "", is_active: bool = True):
        self.account_id = account_id
        self.name = name or f"Account {account_id}"
        self.secure_1psid = secure_1psid
        self.secure_1psidts = secure_1psidts
        self.is_active = is_active
        self.client: Optional[GeminiClient] = None
        self.last_used_time: float = 0.0
        self.is_quota_exhausted: bool = False
        self.quota_reset_time: float = 0.0
        self.consecutive_errors: int = 0

    def is_available(self) -> bool:
        """Kiểm tra xem tài khoản có đang khỏe mạnh và không bị hạn chế/cooldown không."""
        if not self.is_active or not self.client:
            return False
        if self.is_quota_exhausted:
            if time.time() >= self.quota_reset_time:
                # Đã hết thời gian cooldown, khôi phục lại tài khoản vào pool
                self.is_quota_exhausted = False
                self.consecutive_errors = 0
                print(f"🔄 [{self.name}] Hết thời gian cooldown. Đã khôi phục vào pool hoạt động.", flush=True)
                return True
            return False
        return True

    def mark_exhausted(self, cooldown_seconds: float = 300.0):
        """Đánh dấu tài khoản tạm nghỉ khi chạm hạn mức quota hoặc rate limit 429."""
        self.is_quota_exhausted = True
        self.quota_reset_time = time.time() + cooldown_seconds
        print(f"⏳ [{self.name}] Chạm hạn mức/rate-limit. Tạm nghỉ cooldown trong {cooldown_seconds}s.", flush=True)

    def mark_active(self):
        """Đặt lại bộ đếm lỗi khi gọi thành công."""
        self.is_quota_exhausted = False
        self.consecutive_errors = 0
        self.last_used_time = time.time()

    async def initialize(self) -> bool:
        try:
            self.client = GeminiClient(
                secure_1psid=self.secure_1psid,
                secure_1psidts=self.secure_1psidts or ""
            )
            await self.client.init(auto_refresh=False)
            if self.client and getattr(self.client, "_running", False):
                print(f"✅ [{self.name}] Khởi tạo thành công & sẵn sàng trong pool.", flush=True)
                self.is_active = True
                self.is_quota_exhausted = False
                return True
            else:
                print(f"⚠️ [{self.name}] Không thể kích hoạt session. Tạm vô hiệu hóa.", flush=True)
                self.is_active = False
                return False
        except Exception as e:
            print(f"⚠️ [{self.name}] Lỗi khởi tạo: {e}", flush=True)
            self.is_active = False
            return False

    async def refresh_and_persist_cookies(self) -> Optional[str]:
        """Tự động làm mới token __Secure-1PSIDTS qua Google RPC, cập nhật client và lưu lại."""
        if not self.secure_1psid:
            return None
        new_ts = await rotate_and_save_1psidts(self.account_id, self.secure_1psid)
        if new_ts:
            self.secure_1psidts = new_ts
            # Nếu client đang tồn tại, cập nhật cookie và kết nối lại nếu cần
            if self.client:
                try:
                    self.client.cookies.set("__Secure-1PSIDTS", new_ts, domain=".google.com")
                except Exception:
                    pass
                # Nếu client đang lỗi hoặc cần refresh sâu
                try:
                    await self.client.close()
                except Exception:
                    pass
                self.client = None
                await self.initialize()
        return new_ts

    async def close(self):
        if self.client:
            try:
                await self.client.close()
            except Exception:
                pass


class AccountPool:
    """Bể chứa đa tài khoản với cơ chế xoay vòng tự động (Round-Robin & Fallback)."""
    def __init__(self, cookies_dir: Optional[Path] = None, env_path: Optional[Path] = None):
        self.cookies_dir = cookies_dir or self._detect_cookies_dir()
        self.env_path = env_path or self._detect_env_path()
        self.accounts: List[GeminiAccount] = []
        self.current_idx: int = 0
        self._load_all_accounts()

    def _detect_cookies_dir(self) -> Path:
        user_home_cookies = Path.home() / ".gemini" / "cookies"
        if os.environ.get("GEMINI_COOKIES_DIR"):
            return Path(os.environ["GEMINI_COOKIES_DIR"])
        if user_home_cookies.exists():
            return user_home_cookies
        for p in [AGENT_BASE_DIR / "cookies", AGENT_BASE_DIR.parent / "cookies"]:
            if p.exists():
                return p
        return user_home_cookies

    def _detect_env_path(self) -> Path:
        if os.environ.get("GEMINI_ENV_FILE"):
            return Path(os.environ["GEMINI_ENV_FILE"])
        user_home_env = Path.home() / ".gemini" / ".env"
        if user_home_env.exists():
            return user_home_env
        for p in [AGENT_BASE_DIR / ".env", AGENT_BASE_DIR.parent / ".env"]:
            if p.exists():
                return p
        return user_home_env

    def _load_all_accounts(self):
        # 1. Nạp từ all_accounts.json nếu có
        all_acc_file = self.cookies_dir / "all_accounts.json"
        if all_acc_file.exists():
            try:
                data = json.loads(all_acc_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    for item in data:
                        psid = item.get("__Secure-1PSID") or item.get("1psid")
                        psidts = item.get("__Secure-1PSIDTS") or item.get("1psidts") or ""
                        acc_id = item.get("id", len(self.accounts) + 1)
                        name = item.get("name", f"Account {acc_id}")
                        if psid:
                            self.accounts.append(GeminiAccount(
                                account_id=acc_id,
                                secure_1psid=psid.strip(),
                                secure_1psidts=psidts.strip() if psidts else "",
                                name=name
                            ))
                    if self.accounts:
                        return
            except Exception as e:
                print(f"⚠️ Lỗi đọc all_accounts.json: {e}", flush=True)

        # 2. Nạp từ file .env nếu có
        if self.env_path.exists():
            lines = self.env_path.read_text(encoding="utf-8").splitlines()
            env_dict = {}
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_dict[k.strip()] = v.strip().strip('"').strip("'")

            for i in range(1, 10):
                suffix = f"_{i}" if i > 1 else ""
                psid_key = f"GEMINI_SECURE_1PSID{suffix}"
                ts_key = f"GEMINI_SECURE_1PSIDTS{suffix}"
                psid = env_dict.get(psid_key)
                ts = env_dict.get(ts_key, "")
                if psid:
                    self.accounts.append(GeminiAccount(
                        account_id=i,
                        secure_1psid=psid.strip(),
                        secure_1psidts=ts.strip() if ts else "",
                        name=f"Account {i}"
                    ))

    async def init_all(self):
        if not self.accounts:
            print("⚠️ Không tìm thấy tài khoản nào trong pool!", flush=True)
            return
        print(f"🔄 Đang khởi tạo bể {len(self.accounts)} tài khoản Gemini...", flush=True)
        init_tasks = [acc.initialize() for acc in self.accounts]
        await asyncio.gather(*init_tasks)
        active_count = sum(1 for a in self.accounts if a.is_active)
        print(f"🚀 Bể tài khoản đã sẵn sàng: {active_count}/{len(self.accounts)} tài khoản hoạt động.", flush=True)

    def get_available_accounts(self) -> List[GeminiAccount]:
        return [a for a in self.accounts if a.is_available()]

    def get_next_account(self) -> Optional[GeminiAccount]:
        """Lấy tài khoản khả dụng kế tiếp theo thuật toán Round-Robin."""
        avail = self.get_available_accounts()
        if not avail:
            # Khôi phục nếu các tài khoản hết hạn cooldown
            for a in self.accounts:
                if a.is_active and a.client:
                    a.is_quota_exhausted = False
            avail = [a for a in self.accounts if a.is_active and a.client]
            if not avail:
                return None

        acc = avail[self.current_idx % len(avail)]
        self.current_idx += 1
        return acc

    async def execute_with_rotation(self, operation_func, max_attempts: Optional[int] = None) -> Any:
        """
        Thực thi hàm tác vụ với cơ chế xoay vòng tài khoản tự động:
        - Nếu gặp lỗi 1016 / unauthenticated: Tự động làm mới token __Secure-1PSIDTS.
        - Nếu gặp lỗi 429 / quota limit: Đưa tài khoản vào trạng thái cooldown và chuyển sang tài khoản tiếp theo.
        """
        attempts = max_attempts or (len(self.accounts) * 2 or 4)
        last_error = None

        for attempt in range(attempts):
            acc = self.get_next_account()
            if not acc or not acc.client:
                await asyncio.sleep(1.0)
                continue

            try:
                result = await operation_func(acc)
                acc.mark_active()
                return result
            except Exception as e:
                err_str = str(e).lower()
                last_error = e
                acc.consecutive_errors += 1
                print(f"⚠️ [{acc.name} | Lần thử {attempt + 1}] Lỗi: {e}", flush=True)

                if any(w in err_str for w in ["quota", "429", "resource_exhausted", "limit"]):
                    acc.mark_exhausted(cooldown_seconds=300.0)
                elif any(w in err_str for w in ["1016", "unauthenticated", "auth", "permission denied"]):
                    print(f"🔄 [{acc.name}] Token hết hạn. Đang kích hoạt làm mới tự động...", flush=True)
                    await acc.refresh_and_persist_cookies()
                else:
                    if acc.consecutive_errors >= 3:
                        acc.mark_exhausted(cooldown_seconds=120.0)

        raise RuntimeError(f"Tất cả tài khoản trong pool đều gặp sự cố hoặc cạn hạn mức. Lỗi cuối cùng: {last_error}")

    async def generate_content_with_rotation(self, prompt: str, files: Optional[List[Any]] = None) -> Any:
        """
        Helper cấp cao để sinh nội dung với cơ chế tự động xoay vòng tài khoản thông minh.
        """
        async def _gen(acc: GeminiAccount):
            return await acc.client.generate_content(prompt=prompt, files=files)

        return await self.execute_with_rotation(_gen)

    async def close_all(self):
        for acc in self.accounts:
            await acc.close()

    async def sync_all(self):
        """Làm mới token RPC cho toàn bộ tài khoản."""
        print("🔄 Đang làm mới và đồng bộ token cho toàn bộ tài khoản...", flush=True)
        for acc in self.accounts:
            new_ts = await acc.refresh_and_persist_cookies()
            status = f"Thành công: {new_ts[:25]}..." if new_ts else "Giữ nguyên token hiện tại"
            print(f"  {acc.name}: {status}", flush=True)


class ConcurrentWorkerPool:
    """
    Bể xử lý song song đa luồng (Multi-Worker Pool), gán mỗi tài khoản Gemini vào một worker độc lập.
    Cho phép xử lý đồng thời nhiều yêu cầu mà không gây nghẽn chéo giữa các tài khoản.
    """
    def __init__(self, account_pool: AccountPool, max_workers: Optional[int] = None):
        self.pool = account_pool
        self.max_workers = max_workers
        self.queue: asyncio.Queue = asyncio.Queue()
        self.results: List[Any] = []

    async def run_batch(self, items: List[Any], worker_coro) -> List[Any]:
        """
        Thực thi worker_coro(account, item) song song cho danh sách items.
        Tự động chuyển đổi tài khoản (failover rotation) nếu gặp lỗi 429 hoặc token hết hạn.
        """
        active_accounts = [a for a in self.pool.accounts if a.is_active and a.client]
        if not active_accounts:
            raise RuntimeError("Không có tài khoản Gemini nào đang hoạt động trong pool!")

        num_workers = min(len(active_accounts), self.max_workers or len(active_accounts))
        print(f"🚀 [ConcurrentWorkerPool] Bắt đầu {num_workers} worker song song cho {len(items)} tác vụ.", flush=True)

        for item in items:
            await self.queue.put(item)

        results_dict = {}

        async def worker_loop(worker_id: int, initial_account: GeminiAccount):
            current_account = initial_account
            while not self.queue.empty():
                try:
                    item = self.queue.get_nowait()
                except asyncio.QueueEmpty:
                    break

                item_id = getattr(item, "item_id", None) or getattr(item, "id", None) or str(item)
                success = False

                for attempt in range(len(self.pool.accounts) + 1):
                    if not current_account.is_available():
                        next_acc = self.pool.get_next_account()
                        if next_acc:
                            current_account = next_acc

                    try:
                        res = await worker_coro(current_account, item)
                        results_dict[item_id] = res
                        current_account.mark_active()
                        success = True
                        break
                    except Exception as e:
                        err_str = str(e).lower()
                        print(f"⚠️ [Worker {worker_id} - {current_account.name}] Lỗi trên {item_id}: {e}", flush=True)
                        if any(w in err_str for w in ["quota", "429", "resource_exhausted"]):
                            current_account.mark_exhausted(cooldown_seconds=300.0)
                        elif any(w in err_str for w in ["1016", "auth", "unauthenticated"]):
                            print(f"🔄 [Worker {worker_id}] Kích hoạt làm mới token hết hạn...", flush=True)
                            await current_account.refresh_and_persist_cookies()

                        next_acc = self.pool.get_next_account()
                        if next_acc and next_acc != current_account:
                            current_account = next_acc
                        else:
                            await asyncio.sleep(1.0)

                if not success:
                    results_dict[item_id] = {"error": "Thất bại sau khi thử tất cả tài khoản", "item": item}

                self.queue.task_done()

        workers = [
            asyncio.create_task(worker_loop(i + 1, active_accounts[i % len(active_accounts)]))
            for i in range(num_workers)
        ]

        await asyncio.gather(*workers)
        return [results_dict.get(getattr(it, "item_id", None) or getattr(it, "id", None) or str(it)) for it in items]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quản Lý & Xoay Vòng Cookie Tài Khoản Gemini")
    parser.add_argument("--sync", action="store_true", help="Tự động gọi Google RPC để làm mới token __Secure-1PSIDTS")
    parser.add_argument("--status", action="store_true", help="Xem danh sách tài khoản được nạp vào pool")
    parser.add_argument("--test", action="store_true", help="Kiểm tra kết nối và gửi prompt thử nghiệm tới từng tài khoản")
    args = parser.parse_args()

    async def run_cli():
        pool = AccountPool()
        if not pool.accounts:
            print("📋 Bể tài khoản phát hiện: 0 tài khoản.")
            print("⚠️ CHƯA PHÁT HIỆN TÀI KHOẢN NÀO TRONG BỂ (POOL).")
            print("  👉 Nếu bạn muốn kích hoạt tính năng Live Gemini Deep Research / Multi-Account:")
            print("     1. Khuyến nghị an toàn: Lưu cấu hình tại '~/.gemini/.env' hoặc điền token GEMINI_SECURE_1PSID vào '.env'")
            print("     2. Hoặc lưu cookies tại '~/.gemini/cookies/all_accounts.json' (ngoài thư mục đồng bộ OneDrive)")
            print("  💡 Nếu bạn KHÔNG điền tài khoản (Chế độ Offline / Tự do):")
            print("     - Toàn bộ hệ thống kỹ nghệ Agent-Base (DAG Frontier, Red-team Scanner, Design Tokens,")
            print("       WCAG Linter, Sổ cái nợ DebtLedger, Ingest XLSX/Web, Simulator Đa Agent) vẫn chạy 100% hoàn hảo!")
            print("     - Không bắt buộc phải điền nếu dự án của bạn chỉ dùng mô hình Agent nội bộ.\n")
            return

        print(f"📋 Bể tài khoản phát hiện: {len(pool.accounts)} tài khoản.")
        for a in pool.accounts:
            print(f"  - [{a.account_id}] {a.name} (PSID: {a.secure_1psid[:20]}...)")

        if args.sync:
            await pool.sync_all()
            return

        if args.test:
            print("\n--- KIỂM TRA KẾT NỐI & KHỞI TẠO CÁC TÀI KHOẢN ---", flush=True)
            await pool.init_all()
            print("\n--- GỬI PROMPT TEST TỚI TỪNG TÀI KHOẢN ---", flush=True)
            for acc in pool.accounts:
                if acc.client and acc.is_active:
                    try:
                        resp = await acc.client.generate_content("Trả lời 1 từ: OK")
                        ans = resp.text.strip() if resp and resp.text else "(Trống)"
                        print(f"✅ {acc.name}: Phản hồi '{ans}'", flush=True)
                    except Exception as e:
                        print(f"❌ {acc.name}: Lỗi {e}", flush=True)
            await pool.close_all()

    asyncio.run(run_cli())
