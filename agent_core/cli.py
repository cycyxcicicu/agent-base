"""
Agent-Base Unified CLI.
Giao diện dòng lệnh tập trung điều khiển toàn bộ các module kỹ nghệ trong src/.
"""

import sys
import argparse
from pathlib import Path

# Đảm bảo UTF-8 cho Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent_core.debt.ledger import DebtLedger
from agent_core.workflow.tracer_bullet import TicketParser, DependencyGraph
from agent_core.eval.redteam import RedTeamScanner
from agent_core.ingest.doc_converter import DocumentConverter
from agent_core.ingest.web_cleaner import WebCleaner


def main():
    parser = argparse.ArgumentParser(description="Agent-Base Engineering Core CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Lệnh 1: Thu hoạch nợ kỹ thuật (debt)
    p_debt = subparsers.add_parser("debt", help="Thu hoạch toàn bộ nợ kỹ thuật và cập nhật docs/DEBT.md")
    p_debt.add_argument("-o", "--output", help="Đường dẫn lưu file markdown (mặc định docs/DEBT.md)")

    # Lệnh 2: Tìm đường biên tác vụ khả thi (frontier)
    p_frontier = subparsers.add_parser("frontier", help="Quét thư mục tasks/ và tìm các ticket sẵn sàng thực thi trên Frontier")
    p_frontier.add_argument("-d", "--dir", default="tasks", help="Thư mục chứa ticket (mặc định: tasks)")

    # Lệnh 3: Quét bảo mật Red-team cho prompt hoặc text (scan)
    p_scan = subparsers.add_parser("scan", help="Quét rà soát Prompt Injection, PII, rò rỉ dữ liệu hoặc mã độc")
    p_scan.add_argument("text", help="Chuỗi văn bản hoặc prompt cần quét")

    # Lệnh 4: Chuyển đổi tài liệu sang Markdown sạch (convert)
    p_conv = subparsers.add_parser("convert", help="Chuyển đổi CSV/JSON hoặc HTML sang Markdown sạch")
    p_conv.add_argument("file", help="Đường dẫn file cần chuyển đổi")

    args = parser.parse_args()

    if args.command == "debt":
        ledger = DebtLedger(ROOT_DIR)
        items = ledger.harvest()
        out_file = Path(args.output) if args.output else (ROOT_DIR / "docs" / "DEBT.md")
        ledger.write_to_file(out_file)
        print(f"✅ Đã thu hoạch {len(items)} khoản nợ kỹ thuật và cập nhật vào: {out_file}")

    elif args.command == "frontier":
        task_dir = ROOT_DIR / args.dir
        if not task_dir.exists():
            print(f"⚠️ Thư mục không tồn tại: {task_dir}")
            sys.exit(1)

        tickets = []
        for p in task_dir.glob("*.md"):
            if p.name.startswith("_"):
                continue
            ticket = TicketParser.parse_markdown(p.read_text(encoding="utf-8", errors="replace"), str(p))
            if ticket:
                tickets.append(ticket)

        graph = DependencyGraph(tickets)
        frontier = graph.get_frontier()
        print(f"\n🚀 TÌM THẤY {len(frontier)}/{len(tickets)} TICKET SẴN SÀNG TRÊN ĐƯỜNG BIÊN (FRONTIER):")
        for t in frontier:
            print(f"  👉 [{t.ticket_id}] {t.title} (Status: {t.status})")

    elif args.command == "scan":
        issues = RedTeamScanner.scan_text(args.text)
        if not issues:
            print("✅ An toàn tuyệt đối: Không phát hiện lỗi bảo mật hay prompt injection.")
        else:
            print(f"⚠️ CẢNH BÁO: Phát hiện {len(issues)} vấn đề an ninh:")
            for iss in issues:
                print(f"  - [{iss.severity}] {iss.category}: {iss.description} ('{iss.matched_content}')")

    elif args.command == "convert":
        target = Path(args.file)
        if not target.exists():
            print(f"❌ Không tìm thấy file: {target}")
            sys.exit(1)

        content = target.read_text(encoding="utf-8", errors="replace")
        ext = target.suffix.lower()

        if ext == ".csv":
            print(DocumentConverter.csv_to_markdown(content))
        elif ext == ".json":
            print(DocumentConverter.json_to_markdown(content))
        elif ext in [".html", ".htm"]:
            print(WebCleaner.clean_html(content))
        else:
            print(content)


if __name__ == "__main__":
    main()
