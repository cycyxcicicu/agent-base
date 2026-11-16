#!/usr/bin/env python3
"""agy-queue: chia việc kiểm thử cho nhiều lượt agy chạy song song, có hàng đợi, thử lại và theo dõi.

Dùng cùng `agy-acp-bridge.py`. Hướng dẫn: docs/agy-queue.md. Cấu hình mẫu: examples/agy-queue.config.json.

  agy-queue.py plan   --config C --workdir W     # tính phần còn lại, sinh brief và queue-<lane>.txt
  agy-queue.py run    --config C --workdir W --lane A   # chạy hàng đợi của một lượt (chạy nền, mỗi lượt một tiến trình)
  agy-queue.py status --config C --workdir W     # số case đã chạy / còn lại theo đơn vị
  agy-queue.py watch  --config C --workdir W     # mỗi dòng in ra là một sự kiện (dùng với Monitor)

Quy ước: "đơn vị" = một file case (vd một màn hình). Mỗi dòng case có cột mã (id_regex) ở cột 1 và cột tên
(không rỗng) ở cột 2; dòng bước có cột tên rỗng. Kết quả ghi `<result_dir>/<đơn vị>.<phần>.md`, mỗi case một
dòng bảng có cột trạng thái ở cột 2.
"""
import argparse, glob, json, os, re, subprocess, sys, time

BRIDGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agy-acp-bridge.py")
DEFAULTS = {
    "chunk": 12,                       # tối đa case mỗi phần (phiên agy tối đa ~60 phút)
    "part_prefix": "x",
    "statuses": ["Pass", "Fail", "Blocked", "Chờ duyệt ghi"],
    "not_done_regex": "chrome|quota|devtools|kết nối",  # dòng Blocked khớp mẫu này coi là chưa chạy
    "model": "claude-sonnet-5-5-medium",
    "retries": 12,
    "retry_sleep": 30,
    "timeout": 3300,
    "skip_ids_file": None,             # file md liệt kê mã case không chạy (vd case ghi dữ liệu)
    "extra_rules": [],
    "lanes": {},                       # {"A": "<thư mục --dir>", ...}; mỗi lượt một thư mục khác nhau (khóa theo --dir)
    "report_dir": None,
}


def load(path):
    cfg = dict(DEFAULTS)
    cfg.update(json.load(open(path)))
    for k in ("case_glob", "result_dir", "guide", "id_regex", "lanes"):
        if not cfg.get(k):
            sys.exit(f"thiếu khóa cấu hình: {k}")
    return cfg


def cols(line):
    return [x.strip() for x in line.split("|")]


def units(cfg):
    for path in sorted(glob.glob(cfg["case_glob"])):
        yield re.match(r"[^\W\d_]+-\d+|[^.]+", os.path.basename(path)).group(0), path


def case_ids(cfg, path):
    ids = []
    for line in open(path, encoding="utf-8"):
        c = cols(line)
        if len(c) > 3 and re.fullmatch(cfg["id_regex"], c[1]) and c[2] and c[1] not in ids:
            ids.append(c[1])
    return ids


def done_ids(cfg, unit):
    done, bad = set(), re.compile(cfg["not_done_regex"], re.I)
    for f in glob.glob(os.path.join(cfg["result_dir"], unit + ".*md")) + glob.glob(os.path.join(cfg["result_dir"], unit + ".md")):
        for line in open(f, encoding="utf-8"):
            c = cols(line)
            if len(c) > 4 and re.fullmatch(cfg["id_regex"], c[1]) and c[2] in cfg["statuses"]:
                if c[2] == "Blocked" and bad.search(line):
                    continue
                done.add(c[1])
    return done


def remaining(cfg):
    skip = set()
    if cfg["skip_ids_file"]:
        skip = set(re.findall(cfg["id_regex"], open(cfg["skip_ids_file"], encoding="utf-8").read()))
    out = {}
    for unit, path in units(cfg):
        ids = case_ids(cfg, path)
        d = done_ids(cfg, unit)
        out[unit] = (path, ids, [i for i in ids if i not in d and i not in skip])
    return out


def brief_text(cfg, unit, part, path, chunk, out):
    rules = "\n".join(f"- {r}" for r in cfg["extra_rules"])
    return f"""# Nhiệm vụ: chạy kiểm thử {unit}, phần {part}
Đọc kỹ `{cfg['guide']}`, rồi chạy ĐÚNG các case sau trong file `{path}`:
{', '.join(chunk)}

Ghi kết quả vào `{out}`. Ghi file sau mỗi 5 case. Mỗi case một dòng bảng, trạng thái ở cột 2: {' / '.join(cfg['statuses'])}.

Quy tắc bổ sung (bắt buộc):
- KHÔNG hỏi lại, KHÔNG nói "đang chờ". Công cụ trình duyệt không kết nối thì thử lại ngay, tối đa 6 lần.
- Chỉ mở MỘT tab cho lượt này, dùng lại cho mọi case, cuối lượt đóng đúng tab đã mở.
{rules}
"""


def cmd_plan(cfg, wd):
    os.makedirs(os.path.join(wd, "briefs"), exist_ok=True)
    parts = []
    for unit, (path, ids, todo) in remaining(cfg).items():
        print(f"{unit}: tổng {len(ids)}, còn {len(todo)}")
        for k in range(0, len(todo), cfg["chunk"]):
            parts.append((unit, f"{cfg['part_prefix']}{k // cfg['chunk'] + 1}", path, todo[k:k + cfg["chunk"]]))
    loads = {lane: 0 for lane in cfg["lanes"]}
    queues = {lane: [] for lane in cfg["lanes"]}
    for unit, part, path, chunk in sorted(parts, key=lambda p: -len(p[3])):  # cân tải tham lam
        lane = min(loads, key=loads.get)
        loads[lane] += len(chunk)
        queues[lane].append(f"{unit}:{part}")
        out = os.path.join(cfg["result_dir"], f"{unit}.{part}.md")
        open(os.path.join(wd, "briefs", f"{lane}-{unit}-{part}.md"), "w", encoding="utf-8").write(brief_text(cfg, unit, part, path, chunk, out))
    for lane, q in queues.items():
        open(os.path.join(wd, f"queue-{lane}.txt"), "w").write("".join(x + "\n" for x in q))
        print(f"lượt {lane}: {loads[lane]} case, {len(q)} phần")


def log(wd, lane, msg):
    with open(os.path.join(wd, f"lane-{lane}.log"), "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")


def cmd_run(cfg, wd, lane):
    qf = os.path.join(wd, f"queue-{lane}.txt")
    while True:
        lines = [x for x in open(qf).read().split("\n") if x]
        if not lines:
            log(wd, lane, "HET HANG DOI")
            return
        item = lines[0]
        open(qf, "w").write("".join(x + "\n" for x in lines[1:]))
        unit, part = item.split(":")
        out = os.path.join(cfg["result_dir"], f"{unit}.{part}.md")
        brief = os.path.join(wd, "briefs", f"{lane}-{unit}-{part}.md")
        if os.path.exists(out):
            log(wd, lane, f"bỏ qua {item} (đã có file)")
            continue
        for attempt in range(1, cfg["retries"] + 1):
            log(wd, lane, f"{item} lần {attempt}")
            cmd = [sys.executable, BRIDGE, "run", "--dir", cfg["lanes"][lane], "--task-file", brief, "--model", cfg["model"],
                   "--allow-write", cfg["result_dir"], "--timeout", str(cfg["timeout"])]
            if cfg["report_dir"]:
                cmd += ["--report-dir", cfg["report_dir"]]
            r = subprocess.run(cmd, capture_output=True, text=True)
            txt = r.stdout + r.stderr
            if re.search(r"Individual quota reached|quota", txt, re.I) and not os.path.exists(out):
                log(wd, lane, f"QUOTA {item}: dừng lượt, báo người dùng")
                open(qf, "w").write(item + "\n" + "".join(x + "\n" for x in lines[1:]))
                return
            if os.path.exists(out):
                break
            log(wd, lane, f"{item} KHONG CO FILE (mã thoát {r.returncode}), thử lại")
            time.sleep(cfg["retry_sleep"])
        else:
            log(wd, lane, f"LOI {item}: hết {cfg['retries']} lần vẫn không có file")


def cmd_status(cfg, wd):
    tot = 0
    for unit, (path, ids, todo) in remaining(cfg).items():
        print(f"{unit}: đã chạy {len(ids) - len(todo)}/{len(ids)}, còn {len(todo)}")
        tot += len(todo)
    print(f"Còn lại tổng: {tot}")


def cmd_watch(cfg, wd):
    seen_files, offs = set(glob.glob(os.path.join(cfg["result_dir"], "*.md"))), {}
    while True:
        for f in glob.glob(os.path.join(cfg["result_dir"], "*.md")):
            if f not in seen_files:
                seen_files.add(f)
                print(f"file mới: {os.path.basename(f)}", flush=True)
        for lane in cfg["lanes"]:
            p = os.path.join(wd, f"lane-{lane}.log")
            if os.path.exists(p):
                with open(p, encoding="utf-8") as fh:
                    fh.seek(offs.get(p, 0))
                    for line in fh:
                        if re.search(r"KHONG CO FILE|LOI|HET HANG DOI|QUOTA", line):
                            print(f"[{lane}] {line.strip()}", flush=True)
                    offs[p] = fh.tell()
        time.sleep(60)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["plan", "run", "status", "watch"])
    ap.add_argument("--config", required=True)
    ap.add_argument("--workdir", required=True, help="thư mục tạm chứa brief, hàng đợi, log (ngoài repo)")
    ap.add_argument("--lane")
    a = ap.parse_args()
    cfg = load(a.config)
    os.makedirs(a.workdir, exist_ok=True)
    if a.cmd == "plan":
        cmd_plan(cfg, a.workdir)
    elif a.cmd == "run":
        if not a.lane or a.lane not in cfg["lanes"]:
            sys.exit("cần --lane khớp khóa trong cấu hình lanes")
        cmd_run(cfg, a.workdir, a.lane)
    elif a.cmd == "status":
        cmd_status(cfg, a.workdir)
    else:
        cmd_watch(cfg, a.workdir)


if __name__ == "__main__":
    main()
