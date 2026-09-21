import os
import re
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict
import sys

# Thiết lập UTF-8 trên terminal Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Định vị thư mục gốc agent-base và nạp thư viện gemini_webapi nội bộ
AGENT_BASE_DIR = Path(__file__).resolve().parent.parent.parent
_gemini_src = str(AGENT_BASE_DIR / "tools" / "gemini-api" / "src")
if _gemini_src not in sys.path:
    sys.path.insert(0, _gemini_src)

from curl_cffi.requests import AsyncSession
from gemini_webapi.utils.rotate_1psidts import rotate_1psidts

async def rotate_and_save_1psidts(
    account_id: int,
    secure_1psid: str,
    cookies_dict: Optional[Dict[str, str]] = None,
    cookies_dir: Optional[Path] = None
) -> Optional[str]:
    """
    Gọi endpoint Google RotateCookiesPage qua curl_cffi để lấy token __Secure-1PSIDTS mới
    và tự động lưu đè vào file .env cũng như file cookies json tương ứng.
    """
    if not secure_1psid:
        return None

    # Tìm thư mục cookies (ưu tiên thư mục ngoài OneDrive: ~/.gemini/cookies hoặc GEMINI_COOKIES_DIR)
    user_home_cookies = Path.home() / ".gemini" / "cookies"
    if cookies_dir:
        c_dir = Path(cookies_dir)
    elif os.environ.get("GEMINI_COOKIES_DIR"):
        c_dir = Path(os.environ["GEMINI_COOKIES_DIR"])
    elif user_home_cookies.exists():
        c_dir = user_home_cookies
    elif (AGENT_BASE_DIR / "cookies").exists():
        c_dir = AGENT_BASE_DIR / "cookies"
    elif (AGENT_BASE_DIR.parent / "cookies").exists():
        c_dir = AGENT_BASE_DIR.parent / "cookies"
    else:
        c_dir = user_home_cookies
    
    c_dir.mkdir(parents=True, exist_ok=True)
    acc_file = c_dir / f"account_{account_id}.json"

    # Xây dựng danh sách cookie đầy đủ
    full_cookies: Dict[str, str] = {}
    if acc_file.exists():
        try:
            acc_data = json.loads(acc_file.read_text(encoding="utf-8"))
            if isinstance(acc_data, list):
                for c in acc_data:
                    if isinstance(c, dict) and "name" in c and "value" in c:
                        full_cookies[c["name"]] = c["value"]
            elif isinstance(acc_data, dict):
                full_cookies = acc_data.get("cookies", acc_data)
        except Exception:
            pass

    if cookies_dict:
        full_cookies.update(cookies_dict)

    if "__Secure-1PSID" not in full_cookies:
        full_cookies["__Secure-1PSID"] = secure_1psid

    try:
        async with AsyncSession(impersonate="chrome124") as session:
            for name, val in full_cookies.items():
                if isinstance(val, str):
                    session.cookies.set(name, val, domain=".google.com")

            new_1psidts = await rotate_1psidts(session, verbose=False)
            if not new_1psidts:
                return None

        # 1. Cập nhật file .env (ở agent-base hoặc fteck)
        env_paths = [AGENT_BASE_DIR / ".env", AGENT_BASE_DIR.parent / ".env"]
        for env_path in env_paths:
            if env_path.exists():
                env_content = env_path.read_text(encoding="utf-8")
                suffix = f"_{account_id}" if account_id > 1 else ""
                key = f"GEMINI_SECURE_1PSIDTS{suffix}"
                if f"{key}=" in env_content:
                    env_content = re.sub(
                        rf"{key}=.*",
                        f'{key}="{new_1psidts}"',
                        env_content
                    )
                else:
                    env_content += f'\n{key}="{new_1psidts}"\n'
                env_path.write_text(env_content, encoding="utf-8")
                os.environ[key] = new_1psidts

        # 2. Cập nhật file cookies json (account_X.json và all_accounts.json)
        if acc_file.exists():
            try:
                data = json.loads(acc_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    for c in data:
                        if c.get("name") == "__Secure-1PSIDTS":
                            c["value"] = new_1psidts
                    acc_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
                elif isinstance(data, dict) and "cookies" in data:
                    data["cookies"]["__Secure-1PSIDTS"] = new_1psidts
                    acc_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
            except Exception:
                pass

        all_acc_file = c_dir / "all_accounts.json"
        if all_acc_file.exists():
            try:
                all_data = json.loads(all_acc_file.read_text(encoding="utf-8"))
                if isinstance(all_data, list):
                    for acc in all_data:
                        if acc.get("id") == account_id:
                            acc["__Secure-1PSIDTS"] = new_1psidts
                    all_acc_file.write_text(json.dumps(all_data, indent=2, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass

        print(f"🔄 [CookieRotator] Đã làm mới & lưu token __Secure-1PSIDTS cho Tài khoản {account_id}", flush=True)
        return new_1psidts

    except Exception as e:
        print(f"⚠️ [CookieRotator] Không thể xoay vòng token cho Tài khoản {account_id}: {e}", flush=True)
        return None
