#!/usr/bin/env python3
"""
Wrapper điều phối Gemini-API từ agent-base
Tích hợp cổng kiểm tra Ask-Before-Search và tự động định vị cookies.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Đảm bảo UTF-8 cho Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
# 1. Ưu tiên đường dẫn nội bộ bên trong chính agent-base (Đảm bảo tính độc lập khi copy sang dự án khác)
INTERNAL_CLI = ROOT_DIR / "tools" / "gemini-api" / "cli.py"
EXTERNAL_CLI = ROOT_DIR.parent / "Gemini-API" / "cli.py"

INTERNAL_COOKIES = ROOT_DIR / "gemini_cookies.json"
EXTERNAL_COOKIES = ROOT_DIR.parent / "gemini_cookies.json"
USER_HOME_COOKIES = Path.home() / ".gemini" / "gemini_cookies.json"

def get_cli_path():
    if INTERNAL_CLI.exists():
        return str(INTERNAL_CLI)
    if EXTERNAL_CLI.exists():
        return str(EXTERNAL_CLI)
    print(f"❌ Không tìm thấy Gemini-API CLI tại: {INTERNAL_CLI} hoặc {EXTERNAL_CLI}")
    print("Vui lòng kiểm tra thư mục tools/gemini-api bên trong agent-base.")
    sys.exit(1)

def get_cookies_path(custom_path=None):
    if custom_path:
        target = Path(custom_path)
    elif os.environ.get("GEMINI_COOKIES_FILE") and Path(os.environ["GEMINI_COOKIES_FILE"]).exists():
        target = Path(os.environ["GEMINI_COOKIES_FILE"])
    elif USER_HOME_COOKIES.exists():
        target = USER_HOME_COOKIES
    elif INTERNAL_COOKIES.exists():
        target = INTERNAL_COOKIES
    elif EXTERNAL_COOKIES.exists():
        target = EXTERNAL_COOKIES
    else:
        target = USER_HOME_COOKIES
        print(f"⚠️ Cảnh báo: Chưa tìm thấy file cookies tại {USER_HOME_COOKIES} hoặc {INTERNAL_COOKIES}")
        print(f"Khuyến nghị bảo mật: Lưu cookies tại ngoài OneDrive ({USER_HOME_COOKIES}) hoặc fteck/gemini_cookies.json.")
    return str(target)

def run_gemini_cli(cli_args):
    cmd = [sys.executable, get_cli_path()] + cli_args
    try:
        proc = subprocess.run(cmd, text=True, encoding='utf-8', errors='replace')
        return proc.returncode
    except Exception as e:
        print(f"💥 Lỗi khi gọi Gemini-API: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Điều phối Gemini-API & Deep Research với cổng an toàn Ask-Before-Search")
    parser.add_argument("--cookies", help="Đường dẫn file cookies (Mặc định: fteck/gemini_cookies.json)")
    parser.add_argument("--confirm", "-y", action="store_true", help="Xác nhận người dùng đã phê duyệt gửi request ra ngoài")
    
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Subcommand: pool-status
    subparsers.add_parser("pool-status", help="Xem trạng thái các tài khoản trong bể xoay vòng")

    # Subcommand: sync-all
    subparsers.add_parser("sync-all", help="Làm mới token __Secure-1PSIDTS cho toàn bộ tài khoản qua Google RPC")

    # Subcommand: pool-test
    subparsers.add_parser("pool-test", help="Kiểm tra kết nối và gửi prompt test tới từng tài khoản trong pool")

    # Subcommand: inspect
    subparsers.add_parser("inspect", help="Kiểm tra thông tin tài khoản, hạn ngạch và model khả dụng")

    # Subcommand: models
    subparsers.add_parser("models", help="Liệt kê danh sách các mô hình Gemini được hỗ trợ")

    # Subcommand: ask
    ask_parser = subparsers.add_parser("ask", help="Tra cứu thông tin có trích dẫn Google Grounding")
    ask_parser.add_argument("prompt", help="Nội dung câu hỏi cần tra cứu")
    ask_parser.add_argument("--model", default="gemini-flash", help="Mô hình sử dụng (mặc định: gemini-flash)")
    ask_parser.add_argument("--rotate", action="store_true", help="Tự động xoay vòng tài khoản nếu gặp lỗi/hết hạn")
    ask_parser.add_argument("--confirm", "-y", action="store_true", help="Xác nhận người dùng đã phê duyệt")

    # Subcommand: research-send
    r_send = subparsers.add_parser("research-send", help="Khởi tạo tiến trình Gemini Deep Research")
    r_send.add_argument("prompt", help="Chủ đề cần nghiên cứu sâu")
    r_send.add_argument("--model", default="gemini-pro", help="Mô hình nghiên cứu (mặc định: gemini-pro)")
    r_send.add_argument("--confirm", "-y", action="store_true", help="Xác nhận người dùng đã phê duyệt")

    # Subcommand: research-check
    r_check = subparsers.add_parser("research-check", help="Kiểm tra trạng thái tiến trình Deep Research")
    r_check.add_argument("chat_id", help="Chat ID của tác vụ nghiên cứu")

    # Subcommand: research-get
    r_get = subparsers.add_parser("research-get", help="Tải báo cáo Deep Research hoàn chỉnh")
    r_get.add_argument("chat_id", help="Chat ID của tác vụ nghiên cứu")
    r_get.add_argument("-o", "--output", help="Đường dẫn file markdown lưu kết quả (ví dụ: docs/research/bao-cao.md)")

    args = parser.parse_args()

    # Xử lý các lệnh quản lý bể tài khoản (Không cần confirm ra ngoài)
    if args.subcommand in ["pool-status", "sync-all", "pool-test"]:
        pool_script = ROOT_DIR / "tools" / "cookie_rotation" / "account_manager.py"
        if not pool_script.exists():
            print(f"❌ Không tìm thấy module account_manager tại: {pool_script}")
            sys.exit(1)
        sub_arg_map = {
            "sync-all": ["--sync"],
            "pool-status": ["--status"],
            "pool-test": ["--test"]
        }
        sys.exit(subprocess.run([sys.executable, str(pool_script)] + sub_arg_map[args.subcommand]).returncode)

    cookies_path = get_cookies_path(args.cookies)

    # Kiểm tra cổng an toàn: Ask-Before-Search Gate
    requires_confirmation = args.subcommand in ["ask", "research-send"]
    if requires_confirmation:
        # Nếu đang chạy trong terminal tương tác (có con người ngồi trước máy)
        if sys.stdin.isatty():
            print("\n🛑 [CỔNG BẢO VỆ TRA CỨU WEB: ASK-BEFORE-SEARCH]")
            print(f"👉 Thao tác: Gửi truy vấn ra ngoài qua Gemini-API ({args.subcommand})")
            print(f"👉 Nội dung: \"{args.prompt}\"")
            print(f"👉 Model: {args.model}")
            try:
                user_choice = input("\n❓ Bạn có đồng ý cho phép gửi yêu cầu tra cứu này ra Internet không? [y/N]: ").strip().lower()
                if user_choice not in ["y", "yes"]:
                    print("❌ Đã hủy truy vấn theo yêu cầu của người dùng.\n")
                    sys.exit(2)
            except (EOFError, KeyboardInterrupt):
                print("\n❌ Đã hủy truy vấn.\n")
                sys.exit(2)
        else:
            # Chạy phi tương tác (subagent, automated pipeline)
            # Yêu cầu biến môi trường CONFIRM_WEB_SEARCH=1 hoặc cờ --confirm từ người điều hành
            env_confirmed = os.environ.get("CONFIRM_WEB_SEARCH") == "1"
            if not args.confirm and not env_confirmed:
                print("\n🛑 [CỔNG BẢO VỆ TRA CỨU WEB: ASK-BEFORE-SEARCH]")
                print(f"👉 Thao tác: Gửi truy vấn ra ngoài qua Gemini-API ({args.subcommand})")
                print(f"👉 Nội dung: \"{args.prompt}\"")
                print(f"👉 Model: {args.model}")
                print("\n⚠️  Cảnh báo: Tác vụ phi tương tác chưa có xác nhận từ con người (--confirm hoặc CONFIRM_WEB_SEARCH=1).")
                print("Vui lòng hỏi ý kiến người dùng trước khi thực thi.\n")
                sys.exit(2)

    # Xây dựng lệnh chuyển tiếp đến cli.py
    cli_base = ["--cookies-json", cookies_path]

    if args.subcommand == "inspect":
        sys.exit(run_gemini_cli(cli_base + ["inspect"]))
    elif args.subcommand == "models":
        sys.exit(run_gemini_cli(cli_base + ["models"]))
    elif args.subcommand == "ask":
        ret = run_gemini_cli(cli_base + ["--model", args.model, "ask", args.prompt])
        # Nếu gặp lỗi và có cờ --rotate: Thử kích hoạt xoay vòng tài khoản
        if ret != 0 and getattr(args, "rotate", False):
            print("\n🔄 [TỰ ĐỘNG XOAY VÒNG] Tài khoản hiện tại gặp lỗi. Đang đồng bộ và thử lại tài khoản tiếp theo trong pool...", flush=True)
            pool_script = ROOT_DIR / "tools" / "cookie_rotation" / "account_manager.py"
            subprocess.run([sys.executable, str(pool_script), "--sync"])
        sys.exit(ret)
    elif args.subcommand == "research-send":
        sys.exit(run_gemini_cli(cli_base + ["--model", args.model, "research", "send", args.prompt]))
    elif args.subcommand == "research-check":
        sys.exit(run_gemini_cli(cli_base + ["research", "check", args.chat_id]))
    elif args.subcommand == "research-get":
        if args.output:
            cmd = [sys.executable, get_cli_path()] + cli_base + ["research", "get", args.chat_id]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
            if res.returncode == 0:
                out_path = Path(args.output)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(res.stdout, encoding='utf-8')
                print(f"✅ Đã lưu báo cáo nghiên cứu thành công vào: {out_path}")
                sys.exit(0)
            else:
                sys.exit(res.returncode)
        else:
            sys.exit(run_gemini_cli(cli_base + ["research", "get", args.chat_id]))

if __name__ == "__main__":
    main()
