#!/usr/bin/env python3
"""
scripts/watch-swarm.py
Máy chủ Giám sát Đa Agent Thời Gian Thực (Generic Live Swarm Server & File Watcher)
Tự động nhận diện dự án từ PROJECT.md, tasks/EPICS.md, agents/roles/, .kilo/agent-manager.json
Hoàn toàn độc lập, không hardcode tên dự án hay danh sách task riêng lẻ.
Tương thích 100% khi sao chép sang bất kỳ dự án nào sử dụng chuẩn AGENTS.md.

Cách dùng:
  python scripts/watch-swarm.py [--port 4200]
"""

import os
import re
import json
import sys
import time
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse
import subprocess
import sqlite3

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
PROJ_FILE = ROOT / 'PROJECT.md'
EPICS_FILE = ROOT / 'tasks' / 'EPICS.md'
KILO_MGR = ROOT / '.kilo' / 'agent-manager.json'
KILO_DB = Path.home() / '.local' / 'share' / 'kilo' / 'kilo.db'
TASKS_DIR = ROOT / 'tasks'
ROLES_DIR = ROOT / 'agents' / 'roles'
INBOX_DIR = ROOT / 'doc' / 'notes' / 'inbox' if (ROOT / 'doc' / 'notes' / 'inbox').is_dir() else ROOT / 'docs' / 'notes' / 'inbox'
VIEWER_ASSETS = ROOT / 'tools' / 'viewer' / 'assets'
MONITOR_HTML = VIEWER_ASSETS / 'monitor.html'
VIEWER_BUILD = ROOT / 'build' / 'viewer'  # do scripts/generate-dashboard.py sinh ra

# Chỉ phục vụ file tĩnh trong hai thư mục này (không phục vụ cả gốc dự án: tránh lộ .env, mã nguồn, .git).
STATIC_ROOTS = {'/viewer/': VIEWER_BUILD, '/docs/': ROOT / 'docs'}
STATIC_TYPES = {
    '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json',
    '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.md': 'text/plain', '.txt': 'text/plain', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon',
}


def resolve_static(url_path: str):
    """Đổi đường dẫn URL thành file thật trong STATIC_ROOTS; None nếu ngoài phạm vi, sai đuôi hoặc thoát thư mục (..)."""
    url_path = urllib.parse.unquote(url_path)
    for prefix, base in STATIC_ROOTS.items():
        if url_path.startswith(prefix):
            try:
                target = (base / url_path[len(prefix):]).resolve()
                base_resolved = base.resolve()
            except OSError:
                return None
            if base_resolved not in target.parents:
                return None
            if target.is_file() and target.suffix.lower() in STATIC_TYPES:
                return target
    return None

PORT = 4200
CLIENTS = set()
CLIENTS_LOCK = threading.Lock()

ROLE_ICONS = {
    'dev': '💻',
    'dev-frontend': '💻',
    'dev-backend': '⚙️',
    'mobile': '📱',
    'qa': '🧪',
    'reviewer': '👀',
    'lead': '👑',
    'product': '🎯',
    'ba': '📋',
    'analyst': '🔍',
    'architect': '📐',
    'designer': '🎨',
    'dba': '🗄️',
    'ai-eng': '🤖',
    'data-eng': '📊',
    'devops': '🚀',
    'sre': '🚨',
    'security': '🛡️',
    'debt-hunter': '🧹',
    'writer': '✍️',
    'runner': '⚡'
}


def load_project_info():
    """Tự động đọc thông tin dự án từ PROJECT.md hoặc thư mục gốc."""
    info = {
        'name': ROOT.name,
        'description': 'Dự án Phát Triển Phần Mềm Đa Agent Tự Động Hóa',
        'stack': 'TypeScript, Python, Docker',
        'main_branch': 'main',
        'develop_branch': 'develop'
    }
    if PROJ_FILE.exists():
        try:
            txt = PROJ_FILE.read_text(encoding='utf-8')
            m_name = re.search(r'\|\s*Tên dự án\s*\|\s*([^|]+)\|', txt, re.I)
            m_desc = re.search(r'\|\s*Mô tả[^\n|]*\|\s*([^|]+)\|', txt, re.I)
            m_stack = re.search(r'\|\s*Stack\s*\|\s*([^|]+)\|', txt, re.I)
            m_main = re.search(r'\|\s*Nhánh chính\s*\|\s*([^|]+)\|', txt, re.I)
            m_dev = re.search(r'\|\s*Nhánh tích hợp\s*\|\s*([^|]+)\|', txt, re.I)

            if m_name and m_name.group(1).strip():
                info['name'] = m_name.group(1).strip()
            if m_desc and m_desc.group(1).strip():
                info['description'] = m_desc.group(1).strip()
            if m_stack and m_stack.group(1).strip():
                info['stack'] = m_stack.group(1).strip()
            if m_main and m_main.group(1).strip():
                info['main_branch'] = m_main.group(1).strip()
            if m_dev and m_dev.group(1).strip():
                info['develop_branch'] = m_dev.group(1).strip()
        except Exception:
            pass
    return info


_LAST_VALID_KILO_DATA = []


def read_kilo_live_data():
    """Đọc dữ liệu thời gian thực trực tiếp từ SQLite Database của Kilo Code (~/.local/share/kilo/kilo.db)."""
    global _LAST_VALID_KILO_DATA
    if not KILO_DB.exists():
        return _LAST_VALID_KILO_DATA
    try:
        uri = f"file:{KILO_DB}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=5.0)
        c = conn.cursor()

        # Lấy các session cha (parent_id IS NULL) chưa bị archived
        c.execute("""
            SELECT id, title, agent, model, time_created, time_updated, summary_files, cost, tokens_input, tokens_output, tokens_reasoning, directory, metadata
            FROM session
            WHERE parent_id IS NULL AND time_archived IS NULL
            ORDER BY time_updated DESC
            LIMIT 10
        """)
        parent_rows = c.fetchall()
        sessions = []

        for row in parent_rows:
            ses_id = row[0]
            title = row[1] or "Session"
            agent = row[2] or "lead"
            model_raw = row[3]
            time_created = row[4]
            time_updated = row[5]
            summary_files = row[6] or 0
            cost = row[7] or 0.0
            tokens_in = row[8] or 0
            tokens_out = row[9] or 0
            tokens_reasoning = row[10] or 0
            directory = row[11]
            metadata_raw = row[12] if len(row) > 12 else None

            # Model ID
            model_name = "unknown"
            if model_raw:
                try:
                    m_obj = json.loads(model_raw)
                    model_name = m_obj.get("id", model_raw)
                except Exception:
                    model_name = model_raw

            # Todos
            c.execute("SELECT position, status, content, priority FROM todo WHERE session_id=? ORDER BY position", (ses_id,))
            todo_rows = c.fetchall()
            todos_list = []
            done_count = 0
            in_progress_item = None
            for t in todo_rows:
                todos_list.append({
                    "position": t[0],
                    "status": t[1],
                    "content": t[2],
                    "priority": t[3]
                })
                if t[1] == "completed":
                    done_count += 1
                elif t[1] == "in_progress" and not in_progress_item:
                    in_progress_item = t[2]

            # Subagents
            c.execute("""
                SELECT id, title, agent, model, time_created, time_updated
                FROM session
                WHERE parent_id=?
                ORDER BY time_updated DESC
            """, (ses_id,))
            sub_rows = c.fetchall()
            subagents_map = {}
            for s in sub_rows:
                sub_model = "unknown"
                if s[3]:
                    try:
                        sm = json.loads(s[3])
                        sub_model = sm.get("id", s[3])
                    except Exception:
                        sub_model = s[3]
                subagents_map[s[0]] = {
                    "id": s[0],
                    "title": s[1] or "Subagent",
                    "agent": s[2] or "dev",
                    "model": sub_model,
                    "timeCreated": s[4],
                    "timeUpdated": s[5],
                    "lastAction": None,
                    "status": "running"
                }

            # Lấy các part gần nhất bằng session_id IN (...)
            active_sub_keys = [k for k, v in subagents_map.items() if (now_ms - v.get('timeUpdated', 0)) < 600000][:15] if 'now_ms' in locals() else list(subagents_map.keys())[:15]
            rel_ids = [ses_id] + (active_sub_keys if active_sub_keys else list(subagents_map.keys())[:15])
            placeholders = ','.join(['?'] * len(rel_ids))
            c.execute(f"""
                SELECT p.id, p.session_id, s.agent, p.time_created, p.data
                FROM part p
                JOIN session s ON p.session_id = s.id
                WHERE p.session_id IN ({placeholders})
                ORDER BY p.time_created DESC
                LIMIT 25
            """, rel_ids)

            recent_actions = []
            modified_files_set = set()
            latest_part_type = {}

            for pr in c.fetchall():
                try:
                    pd = json.loads(pr[4])
                    ptype = pd.get('type')
                    act_agent = pr[2] or 'agent'
                    act_ses_id = pr[1]
                    act_time = time.strftime('%H:%M:%S', time.localtime(pr[3] / 1000))

                    if act_ses_id not in latest_part_type:
                        latest_part_type[act_ses_id] = ptype
                        if ptype == 'step-finish' and act_ses_id in subagents_map:
                            subagents_map[act_ses_id]['status'] = 'completed'

                    if ptype == 'tool':
                        tool_name = pd.get('tool', 'tool')
                        state = pd.get('state', {})
                        inp = state.get('input', {})
                        status = state.get('status', 'running')

                        target = inp.get('filePath') or inp.get('path') or inp.get('pattern') or ''
                        cmd = inp.get('command') or ''
                        desc = inp.get('description') or inp.get('prompt') or ''

                        if target and ('/' in target or '\\' in target):
                            clean_target = os.path.normpath(target)
                            if tool_name in ('write', 'apply_patch', 'edit', 'replace'):
                                modified_files_set.add(clean_target)

                        action_desc = ''
                        if tool_name == 'write':
                            action_desc = f"Ghi tệp tin: {Path(target).name if target else ''}"
                        elif tool_name in ('apply_patch', 'edit'):
                            action_desc = f"Vá mã nguồn: {Path(target).name if target else ''}"
                        elif tool_name == 'bash':
                            action_desc = f"Chạy lệnh: {cmd[:60]}"
                        elif tool_name == 'read':
                            action_desc = f"Đọc tệp tin: {Path(target).name if target else ''}"
                        elif tool_name == 'glob':
                            action_desc = f"Tìm tệp tin: {target}"
                        elif tool_name == 'task':
                            action_desc = f"Giao việc Subagent: {desc[:60]}"
                        else:
                            action_desc = f"{tool_name}: {target or cmd or desc[:50]}"

                        action_obj = {
                            'time': act_time,
                            'agent': act_agent,
                            'tool': tool_name,
                            'status': status,
                            'target': target,
                            'command': cmd,
                            'description': action_desc
                        }
                        recent_actions.append(action_obj)

                        # Gắn trực tiếp vào subagent tương ứng nếu chưa có
                        if act_ses_id in subagents_map and not subagents_map[act_ses_id]['lastAction']:
                            subagents_map[act_ses_id]['lastAction'] = action_obj
                            subagents_map[act_ses_id]['status'] = 'running' if status == 'running' else 'completed'

                    elif ptype == 'patch':
                        patch_files = pd.get('files', [])
                        for pf in patch_files:
                            modified_files_set.add(os.path.normpath(pf))
                        patch_action = {
                            'time': act_time,
                            'agent': act_agent,
                            'tool': 'patch',
                            'status': 'completed',
                            'target': ', '.join([Path(f).name for f in patch_files]),
                            'command': '',
                            'description': f"Sửa đổi {len(patch_files)} file: {', '.join([Path(f).name for f in patch_files])}"
                        }
                        recent_actions.append(patch_action)
                        if act_ses_id in subagents_map and not subagents_map[act_ses_id]['lastAction']:
                            subagents_map[act_ses_id]['lastAction'] = patch_action
                except Exception:
                    pass

            # Xác định trạng thái thực tế của subagents dựa trên part cuối cùng của chính nó
            now_ms = int(time.time() * 1000)
            for sub_id, sm in subagents_map.items():
                sm_updated = sm.get('timeUpdated', 0)
                diff_sec = (now_ms - sm_updated) / 1000 if sm_updated else 999999

                # Nếu subagent đã không hoạt động hơn 5 phút (300s) -> chắc chắn completed
                if diff_sec >= 300:
                    sm['status'] = 'completed'
                    continue

                # Đọc part mới nhất của subagent này
                try:
                    c.execute("""
                        SELECT data
                        FROM part
                        WHERE session_id = ?
                        ORDER BY time_created DESC
                        LIMIT 1
                    """, (sub_id,))
                    latest_p = c.fetchone()
                    l_type = None
                    l_reason = None
                    l_tool_status = None
                    if latest_p:
                        pd = json.loads(latest_p[0])
                        l_type = pd.get('type')
                        l_reason = pd.get('reason')
                        if l_type == 'tool':
                            l_tool_status = pd.get('state', {}).get('status')

                    is_sub_running = False
                    if latest_p is None:
                        is_sub_running = (diff_sec < 90)
                    elif l_type == 'step-finish' and l_reason in ('stop', 'other', 'end_turn'):
                        is_sub_running = False
                    elif l_type == 'tool' and l_tool_status in ('running', 'pending', None):
                        is_sub_running = True
                    elif l_type == 'step-finish' and l_reason == 'tool-calls':
                        is_sub_running = True
                    elif l_type in ('text', 'reasoning', 'step-start') and diff_sec < 180:
                        is_sub_running = True
                    elif l_type == 'tool' and l_tool_status == 'completed' and diff_sec < 90:
                        is_sub_running = True
                    elif diff_sec < 60:
                        is_sub_running = True

                    sm['status'] = 'running' if is_sub_running else 'completed'
                except Exception:
                    sm['status'] = 'completed'

            # Đồng bộ trạng thái hoàn thành cho subagents nếu toàn bộ to-dos đã xong
            all_todos_finished = (done_count == len(todos_list) and len(todos_list) > 0)
            if all_todos_finished:
                for sm in subagents_map.values():
                    sm['status'] = 'completed'

            total_subs_count = len(subagents_map)
            running_subs_count = sum(1 for sm in subagents_map.values() if sm['status'] == 'running')
            completed_subs_count = sum(1 for sm in subagents_map.values() if sm['status'] == 'completed')

            # Tự động trích xuất tên có ý nghĩa nếu tiêu đề gốc là timestamp New session
            clean_title = title
            is_new_session = title.startswith("New session - ")
            if is_new_session:
                first_prompt_line = ""
                try:
                    c.execute("""
                        SELECT p.data FROM part p
                        JOIN message m ON p.message_id = m.id
                        WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'user' AND json_extract(p.data, '$.type') = 'text'
                        ORDER BY m.time_created ASC LIMIT 1
                    """, (ses_id,))
                    row_p = c.fetchone()
                    if row_p:
                        ptxt = json.loads(row_p[0]).get('text', '').strip()
                        if ptxt and not ptxt.startswith('<'):
                            first_prompt_line = ptxt.split('\n')[0].strip()[:70]
                except Exception:
                    pass

                if first_prompt_line:
                    clean_title = f"Phiên mới: {first_prompt_line}"
                elif in_progress_item and not in_progress_item.startswith("Chưa có") and not in_progress_item.startswith("Tất cả"):
                    clean_title = f"Phiên mới: {in_progress_item}"
                elif running_subs_count > 0:
                    for sm in subagents_map.values():
                        if sm['status'] == 'running':
                            clean_title = f"Phiên mới: {sm['title']}"
                            break
                elif todos_list:
                    clean_title = f"Phiên mới: {todos_list[-1]['content']}"
                elif subagents_map:
                    clean_title = f"Phiên mới: {list(subagents_map.values())[0]['title']}"
                else:
                    clean_title = "Phiên mới (Kilo Code)"

            # Sắp xếp subagents: subagent đang chạy lên đầu, rồi đến gần đây nhất
            sorted_subs = sorted(
                subagents_map.values(),
                key=lambda x: (1 if x['status'] == 'running' else 0, x.get('timeUpdated', 0)),
                reverse=True
            )
            # Gửi đầy đủ danh sách subagents để giao diện hiển thị trọn vẹn dàn agent tự động
            subagents = sorted_subs

            # Xác định thời gian thực tế của đợt làm việc hiện tại (Goal run / Active Prompt cluster)
            active_start_time = time_created
            try:
                goal_text = None
                if metadata_raw:
                    meta = json.loads(metadata_raw)
                    goal_text = meta.get("kilo.goal", {}).get("text")
                if goal_text:
                    c.execute("""
                        SELECT time_created FROM part 
                        WHERE session_id = ? AND data LIKE ?
                        ORDER BY time_created DESC LIMIT 1
                    """, (ses_id, f"%{goal_text[:30]}%"))
                    g_row = c.fetchone()
                    if g_row and g_row[0]:
                        active_start_time = g_row[0]
                else:
                    c.execute("""
                        SELECT time_created FROM message 
                        WHERE session_id = ? AND json_extract(data, '$.role') = 'user'
                        ORDER BY time_created ASC
                    """, (ses_id,))
                    u_pts = [r[0] for r in c.fetchall()]
                    if u_pts:
                        cur_pt = u_pts[-1]
                        for idx_u in range(len(u_pts) - 1, 0, -1):
                            if (u_pts[idx_u] - u_pts[idx_u - 1]) / 60000 <= 15:
                                cur_pt = u_pts[idx_u - 1]
                            else:
                                break
                        active_start_time = cur_pt
            except Exception:
                pass

            last_user_time = time_created
            try:
                c.execute("""
                    SELECT max(time_created) FROM message 
                    WHERE session_id = ? AND json_extract(data, '$.role') = 'user'
                """, (ses_id,))
                lu = c.fetchone()
                if lu and lu[0]:
                    last_user_time = lu[0]
            except Exception:
                pass

            now_ms = int(time.time() * 1000)
            elapsed_sec = max(0, int((now_ms - active_start_time) / 1000))
            h = elapsed_sec // 3600
            m = (elapsed_sec % 3600) // 60
            s_sec = elapsed_sec % 60
            elapsed_text = f"{h}h {m:02d}m {s_sec:02d}s" if h > 0 else f"{m:02d}m {s_sec:02d}s"

            # Trích xuất các lượt prompt (đoạn chat) của người dùng và gán subagents tương ứng
            prompt_turns = []
            try:
                c.execute("""
                    SELECT m.id, m.time_created
                    FROM message m
                    WHERE m.session_id=? AND json_extract(m.data, '$.role') = 'user'
                    ORDER BY m.time_created ASC
                """, (ses_id,))
                user_msgs = c.fetchall()

                for m_id, t_c in user_msgs:
                    c.execute("SELECT data FROM part WHERE message_id=? AND json_extract(data, '$.type') = 'text'", (m_id,))
                    p_rows = c.fetchall()
                    txt = ''.join([json.loads(p[0]).get('text', '') for p in p_rows]).strip()
                    if txt and not txt.startswith('<task id=') and not txt.startswith('Continue if you have') and not txt.startswith('<summary>Background'):
                        t_str = time.strftime('%H:%M:%S', time.localtime(t_c / 1000))
                        prompt_turns.append({
                            'id': m_id,
                            'time': t_c,
                            'timeText': t_str,
                            'prompt': txt,
                            'subagents': []
                        })

                # Gán subagents vào từng đoạn chat tương ứng dựa theo thời gian sinh
                for sm in sorted_subs:
                    s_tc = sm.get('timeCreated', 0)
                    assigned_turn = None
                    for pt in prompt_turns:
                        if pt['time'] <= s_tc + 5000:
                            assigned_turn = pt
                        else:
                            break
                    if assigned_turn:
                        assigned_turn['subagents'].append(sm)
                    elif prompt_turns:
                        prompt_turns[0]['subagents'].append(sm)

                for i, pt in enumerate(prompt_turns):
                    pt['turnIndex'] = i + 1
                    pt['isLatest'] = (i == len(prompt_turns) - 1)
                    pt['runningCount'] = sum(1 for x in pt['subagents'] if x.get('status') == 'running')
                    pt['totalCount'] = len(pt['subagents'])
            except Exception:
                prompt_turns = []

            sessions.append({
                "sessionId": ses_id,
                "title": clean_title,
                "agent": agent,
                "model": model_name,
                "directory": directory,
                "elapsedSeconds": elapsed_sec,
                "elapsedText": elapsed_text,
                "timeCreated": time_created,
                "timeUpdated": time_updated,
                "lastUserTime": last_user_time,
                "totalSubagents": total_subs_count,
                "runningSubagents": running_subs_count,
                "completedSubagents": completed_subs_count,
                "recentActions": recent_actions,
                "lastAction": recent_actions[0] if recent_actions else None,
                "modifiedFiles": list(modified_files_set),
                "todos": {
                    "total": len(todos_list),
                    "done": done_count,
                    "inProgress": in_progress_item or ("Tất cả to-do đã hoàn thành" if done_count == len(todos_list) and len(todos_list) > 0 else "Chưa có to-do đang chạy"),
                    "items": todos_list
                },
                "subagents": subagents,
                "promptTurns": prompt_turns,
                "stats": {
                    "summaryFiles": summary_files,
                    "cost": cost,
                    "tokensInput": tokens_in,
                    "tokensOutput": tokens_out,
                    "tokensReasoning": tokens_reasoning
                }
            })
        conn.close()
        if sessions:
            _LAST_VALID_KILO_DATA = sessions
        return sessions
    except Exception:
        return _LAST_VALID_KILO_DATA


_STATE_LOCK = threading.Lock()
_COMPUTE_LOCK = threading.Lock()
_CACHED_STATE = None
_CACHED_JSON_BYTES = None
_LAST_STATE_TIME = 0.0
_WT_STATUS_CACHE = {}
_WT_STATUS_TIME = {}


def get_current_swarm_state(force_refresh=False):
    global _CACHED_STATE, _LAST_STATE_TIME, _CACHED_JSON_BYTES
    now = time.time()
    with _STATE_LOCK:
        if not force_refresh and _CACHED_STATE is not None and (now - _LAST_STATE_TIME) < 1.2:
            return _CACHED_STATE

    with _COMPUTE_LOCK:
        now = time.time()
        with _STATE_LOCK:
            if not force_refresh and _CACHED_STATE is not None and (now - _LAST_STATE_TIME) < 1.2:
                return _CACHED_STATE

        proj_info = load_project_info()

    # 1. Đọc trạng thái tasks từ tasks/
    all_tasks = []
    doing_tasks = []
    review_tasks = []
    blocked_tasks = []
    done_count = 0
    todo_count = 0
    doing_count = 0
    review_count = 0

    if TASKS_DIR.exists():
        for p in TASKS_DIR.rglob('T-*.md'):
            try:
                txt = p.read_text(encoding='utf-8')
                m_id = re.search(r'^id:\s*(.+)$', txt, re.M)
                m_title = re.search(r'^title:\s*(.+)$', txt, re.M)
                m_status = re.search(r'^status:\s*(.+)$', txt, re.M)
                m_owner = re.search(r'^owner:\s*(.+)$', txt, re.M)
                m_branch = re.search(r'^branch:\s*(.+)$', txt, re.M)
                m_epic = re.search(r'^epic:\s*(.+)$', txt, re.M)

                cid = m_id.group(1).strip() if m_id else p.stem
                st = m_status.group(1).strip().lower() if m_status else 'todo'
                ow = m_owner.group(1).strip().lower() if m_owner else 'dev'
                ti = m_title.group(1).strip() if m_title else cid
                br = m_branch.group(1).strip() if m_branch else ''
                ep = m_epic.group(1).strip() if m_epic else ''

                t_obj = {'id': cid, 'title': ti, 'status': st, 'owner': ow, 'branch': br, 'epic': ep}
                all_tasks.append(t_obj)

                if st == 'done':
                    done_count += 1
                elif st == 'doing':
                    doing_count += 1
                    doing_tasks.append(t_obj)
                elif st == 'review':
                    review_count += 1
                    review_tasks.append(t_obj)
                elif st == 'blocked':
                    blocked_tasks.append(t_obj)
                elif st == 'todo':
                    todo_count += 1
            except Exception:
                pass

    total_tasks = done_count + doing_count + review_count + todo_count + len(blocked_tasks)

    # 2. Đọc Git Worktrees thực tế
    parsed_wts = []
    try:
        git_wt_out = subprocess.check_output(
            ['git', '-C', str(ROOT), 'worktree', 'list', '--porcelain'],
            text=True,
            timeout=3,
            stderr=subprocess.DEVNULL
        )
        cur_wt = {}
        for line in git_wt_out.splitlines():
            line = line.strip()
            if not line:
                if cur_wt:
                    parsed_wts.append(cur_wt)
                    cur_wt = {}
                continue
            if line.startswith('worktree '):
                cur_wt['path'] = line[len('worktree '):].strip()
            elif line.startswith('branch '):
                cur_wt['branch'] = line[len('branch '):].strip().replace('refs/heads/', '')
            elif line.startswith('HEAD '):
                cur_wt['head'] = line[len('HEAD '):].strip()
            elif line.startswith('detached'):
                cur_wt['branch'] = 'detached'
        if cur_wt:
            parsed_wts.append(cur_wt)
    except Exception:
        pass

    # 3. Đọc dữ liệu thực tế 100% từ Kilo Code SQLite Database (kilo.db)
    kilo_raw_sessions = read_kilo_live_data()
    active_sessions = []
    matched_wt_paths = set()

    for ks in kilo_raw_sessions:
        # Nhận diện Ticket ID chính xác: Ưu tiên đường dẫn file đang thao tác thực tế -> Subagent mới nhất -> In-progress todo -> Tiêu đề
        m_ticket = None
        target_check = (ks.get('lastAction') or {}).get('target') or ''
        if target_check:
            m_ticket = re.search(r'\bT-?(\d+)\b', target_check, re.I)
        if not m_ticket and ks.get('modifiedFiles'):
            for mf in ks['modifiedFiles']:
                m_ticket = re.search(r'\bT-?(\d+)\b', mf, re.I)
                if m_ticket:
                    break
        if not m_ticket:
            for sub in ks.get('subagents', []):
                m_ticket = re.search(r'\bT-?(\d+)\b', sub.get('title', ''), re.I)
                if m_ticket:
                    break
        if not m_ticket:
            in_prog_raw = ks['todos'].get('inProgress') or ''
            if in_prog_raw and not in_prog_raw.startswith("Chưa có") and not in_prog_raw.startswith("Tất cả"):
                m_ticket = re.search(r'\bT-?(\d+)\b', in_prog_raw, re.I)
        if not m_ticket:
            m_ticket = re.search(r'\bT-?(\d+)\b', ks['title'], re.I)

        ticket_id = f"T-{m_ticket.group(1)}" if m_ticket else None

        # Cập nhật lại tiêu đề phiên nếu ticket hiện tại mới hơn tiêu đề ban đầu
        display_title = ks['title']
        if display_title.startswith("Phiên mới:"):
            inner = display_title.replace("Phiên mới:", "").strip()
            if ticket_id and ticket_id not in inner:
                display_title = f"Phiên mới: [{ticket_id}] {inner}"
        elif ticket_id and "Backend" in display_title:
            display_title = f"Triển khai Backend {ticket_id}"

        # Khớp với task trong tasks/ để lấy branch chính thức
        matched_task = None
        if ticket_id:
            for t in all_tasks:
                if t['id'].upper() == ticket_id.upper():
                    matched_task = t
                    break

        # Khớp với worktree: Ưu tiên worktree đang thao tác file trực tiếp hoặc subagent đang chạy
        matched_wt = None
        candidates = []
        if ticket_id:
            candidates.append(ticket_id)
        if target_check:
            m_act = re.search(r'\bT-?(\d+)\b', target_check, re.I)
            if m_act:
                candidates.append(f"T-{m_act.group(1)}")
        for sub in ks.get('subagents', []):
            m_s = re.search(r'\bT-?(\d+)\b', sub.get('title', ''), re.I)
            if m_s:
                candidates.append(f"T-{m_s.group(1)}")

        for cid in candidates:
            for wt in parsed_wts:
                wp = wt.get('path', '').lower()
                wb = wt.get('branch', '').lower()
                if cid.lower() in wp or cid.lower() in wb:
                    matched_wt = wt
                    break
            if matched_wt:
                break

        wt_path = matched_wt.get('path') if matched_wt else str(ROOT)
        branch = matched_wt.get('branch') if matched_wt else (matched_task.get('branch') if matched_task and matched_task.get('branch') else 'main')
        is_root = os.path.normpath(wt_path).lower() == os.path.normpath(str(ROOT)).lower()
        if matched_wt:
            matched_wt_paths.add(os.path.normpath(wt_path).lower())

        # Đọc git status file thay đổi trong worktree (có cache 5s)
        now_ts = time.time()
        if wt_path not in _WT_STATUS_CACHE or (now_ts - _WT_STATUS_TIME.get(wt_path, 0)) >= 5.0:
            st_files = []
            if os.path.isdir(wt_path):
                try:
                    git_st = subprocess.check_output(
                        ['git', 'status', '--porcelain'],
                        cwd=wt_path,
                        text=True,
                        timeout=1.5,
                        stderr=subprocess.DEVNULL
                    )
                    st_files = [l.strip() for l in git_st.splitlines() if l.strip()]
                except Exception:
                    st_files = []
            _WT_STATUS_CACHE[wt_path] = st_files
            _WT_STATUS_TIME[wt_path] = now_ts

        changed_files = _WT_STATUS_CACHE[wt_path]

        # Quyết định trạng thái
        all_todos_done = ks['todos']['total'] > 0 and ks['todos']['done'] == ks['todos']['total']
        has_inprogress_todo = (
            ks['todos']['inProgress'] 
            and "Chưa có to-do" not in ks['todos']['inProgress'] 
            and "Tất cả to-do" not in ks['todos']['inProgress']
        )
        running_subagents = [sub for sub in ks['subagents'] if sub['status'] == 'running']
        has_running_sub = len(running_subagents) > 0

        now_ms = int(time.time() * 1000)
        mins_since_update = (now_ms - ks.get('timeUpdated', 0)) / 60000

        # Nếu người dùng vừa chat hoặc agent vừa chạy công cụ trong vòng 4 phút qua -> ĐANG THI CÔNG!
        has_fresh_activity = mins_since_update <= 4.0

        if has_running_sub:
            session_state = 'WORKING'
            active_role = running_subagents[0]['agent']
            status_text = f"Subagent {active_role.upper()} đang thực thi"
        elif has_inprogress_todo:
            session_state = 'WORKING'
            active_role = ks['agent'] or 'lead'
            status_text = f"Lead đang xử lý: {ks['todos']['inProgress']}"
        elif has_fresh_activity:
            session_state = 'WORKING'
            active_role = ks['agent'] or 'lead'
            last_desc = ks['lastAction']['description'] if ks.get('lastAction') else "Đang thực hiện yêu cầu mới..."
            status_text = f"Lead đang xử lý: {last_desc}"
        elif all_todos_done:
            session_state = 'DONE'
            active_role = ks['agent'] or 'lead'
            status_text = f"Đã hoàn thành toàn bộ {ks['todos']['done']}/{ks['todos']['total']} to-dos"
        elif len(changed_files) > 0:
            session_state = 'MODIFIED'
            active_role = ks['agent'] or 'lead'
            status_text = f"Đang chỉnh sửa {len(changed_files)} tệp tin"
        else:
            session_state = 'IDLE'
            active_role = None
            status_text = "Chờ lệnh prompt tiếp theo"


        short_label = ticket_id or ('ROOT' if is_root else ks['sessionId'][:8])

        # Tập hợp tất cả các file bị sửa đổi (kết hợp git status và patch từ kilo.db)
        all_modified = list(dict.fromkeys(changed_files + ks.get('modifiedFiles', [])))

        active_sessions.append({
            'sessionId': ks['sessionId'],
            'shortId': short_label,
            'title': display_title,
            'worktreeId': ticket_id or ('ROOT' if is_root else Path(wt_path).name),
            'branch': branch,
            'worktreePath': wt_path,
            'existsOnDisk': os.path.isdir(wt_path),
            'changedFiles': changed_files,
            'modifiedFiles': all_modified,
            'recentActions': ks.get('recentActions', []),
            'lastAction': ks.get('lastAction'),
            'matchedTask': matched_task,
            'state': session_state,
            'statusText': status_text,
            'activeRole': active_role,
            'agent': ks['agent'],
            'model': ks['model'],
            'elapsedSeconds': ks['elapsedSeconds'],
            'elapsedText': ks['elapsedText'],
            'timeCreated': ks['timeCreated'],
            'timeUpdated': ks['timeUpdated'],
            'lastUserTime': ks.get('lastUserTime', ks['timeCreated']),
            'todos': ks['todos'],
            'totalSubagents': ks.get('totalSubagents', len(ks.get('subagents', []))),
            'runningSubagents': ks.get('runningSubagents', 0),
            'completedSubagents': ks.get('completedSubagents', 0),
            'subagents': ks['subagents'],
            'promptTurns': ks.get('promptTurns', []),
            'stats': ks['stats'],
            'isRoot': is_root
        })

    # LẤY CÁC PHIÊN CHAT CỦA DỰ ÁN (ƯU TIÊN PHIÊN ĐANG CHẠY & CÁC PHIÊN CÓ SUBAGENTS GẦN ĐÂY)
    now_ms = int(time.time() * 1000)
    filtered_sessions = []

    # 1. Các phiên đang thi công hoặc có hoạt động trong 45 phút qua
    for s in active_sessions:
        mins_since_update = (now_ms - s.get('timeUpdated', 0)) / 60000
        has_running_sub = any(sub.get('status') == 'running' for sub in s.get('subagents', []))
        if mins_since_update <= 45.0 or has_running_sub:
            if s not in filtered_sessions:
                filtered_sessions.append(s)

    # 2. Bổ sung các phiên chat gần đây có subagents hoặc to-dos để người dùng có thể duyệt từng đoạn chat
    for s in active_sessions:
        if s not in filtered_sessions and (s.get('totalSubagents', 0) > 0 or s.get('todos', {}).get('total', 0) > 0):
            filtered_sessions.append(s)
            if len(filtered_sessions) >= 6:
                break

    if not filtered_sessions and active_sessions:
        filtered_sessions = active_sessions[:5]

    active_sessions = filtered_sessions

    # Worktrees list
    active_worktrees = [{'path': wt.get('path', ''), 'branch': wt.get('branch', '')} for wt in parsed_wts]

    # 3. Quét động các vai trò Agent từ agents/roles/*.md
    roles_list = []
    if ROLES_DIR.exists():
        for rf in sorted(ROLES_DIR.glob('*.md')):
            try:
                r_id = rf.stem
                rtxt = rf.read_text(encoding='utf-8')
                m_name = re.search(r'^name:\s*(.+)$', rtxt, re.M)
                m_desc = re.search(r'^description:\s*(.+)$', rtxt, re.M)
                m_tier = re.search(r'^model_tier:\s*(.+)$', rtxt, re.M)

                role_name = m_name.group(1).strip() if m_name else r_id.upper()
                role_desc = m_desc.group(1).strip() if m_desc else f'Vai trò chuyên môn {r_id}'
                role_tier = m_tier.group(1).strip() if m_tier else 'standard'

                # Tìm các task thuộc vai trò này
                role_doing = [t for t in doing_tasks if t['owner'] == r_id]
                role_review = [t for t in review_tasks if t['owner'] == r_id]
                role_done_count = sum(1 for t in all_tasks if t['owner'] == r_id and t['status'] == 'done')
                role_todo_count = sum(1 for t in all_tasks if t['owner'] == r_id and t['status'] == 'todo')

                # Xác định trạng thái vai trò
                if role_doing:
                    role_status = 'RUN'
                    current_task_title = f"{role_doing[0]['id']}: {role_doing[0]['title']}"
                    current_branch = role_doing[0]['branch'] or 'feature/branch'
                    progress_pct = 40
                elif role_review:
                    role_status = 'REVIEW'
                    current_task_title = f"{role_review[0]['id']}: {role_review[0]['title']}"
                    current_branch = role_review[0]['branch'] or 'review'
                    progress_pct = 90
                elif role_done_count > 0 and role_todo_count == 0:
                    role_status = 'DONE'
                    current_task_title = f"Lũy kế: {role_done_count} task đã xong"
                    current_branch = 'Đã nghiệm thu'
                    progress_pct = 100
                elif role_todo_count > 0:
                    role_status = 'WAIT'
                    current_task_title = f"Chờ tiếp nhận ({role_todo_count} task trong hàng đợi)"
                    current_branch = 'Chờ tín hiệu'
                    progress_pct = 0
                else:
                    role_status = 'STANDBY'
                    current_task_title = "Sẵn sàng (Chưa có task trong phiên)"
                    current_branch = 'Trực tuyến'
                    progress_pct = 0

                roles_list.append({
                    'id': r_id,
                    'name': role_name,
                    'description': role_desc,
                    'tier': role_tier,
                    'icon': ROLE_ICONS.get(r_id, '🤖'),
                    'status': role_status,
                    'currentTask': current_task_title,
                    'branch': current_branch,
                    'progress': progress_pct,
                    'stats': {
                        'done': role_done_count,
                        'doing': len(role_doing),
                        'review': len(role_review),
                        'todo': role_todo_count
                    }
                })
            except Exception:
                pass

    # 4. Đọc 8 ghi chú mới nhất từ inbox
    recent_notes = []
    if INBOX_DIR.exists():
        note_files = list(INBOX_DIR.rglob('*.md'))
        note_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        for nf in note_files[:8]:
            recent_notes.append({
                'filename': nf.name,
                'time': time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(nf)))
            })

    state = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'project': proj_info,
        'kilo': {
            'totalSessions': len(active_sessions),
            'sessions': active_sessions,
            'totalWorktrees': len(active_worktrees),
            'worktrees': active_worktrees
        },
        'tasks': {
            'total': total_tasks,
            'done': done_count,
            'doing': doing_count,
            'review': review_count,
            'todo': todo_count,
            'blocked': len(blocked_tasks),
            'doingList': doing_tasks,
            'reviewList': review_tasks,
            'blockedList': blocked_tasks
        },
        'roles': roles_list,
        'inbox': recent_notes
    }

    with _STATE_LOCK:
        _CACHED_STATE = state
        _CACHED_JSON_BYTES = json.dumps(state, ensure_ascii=False).encode('utf-8')
        _LAST_STATE_TIME = time.time()

    return state


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        # Bỏ qua lỗi ngắt socket phổ biến trên Windows khi browser reload
        pass


class SwarmHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in ('/', '/monitor.html', '/agent-monitor.html'):
            if (VIEWER_BUILD / 'monitor.html').exists():
                self.redirect('/viewer/monitor.html')
            else:
                self.serve_file(MONITOR_HTML, 'text/html')
        elif path == '/dashboard.html':
            if (VIEWER_BUILD / 'index.html').exists():
                self.redirect('/viewer/index.html')
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write('Chưa có dashboard. Chạy: python scripts/generate-dashboard.py'.encode('utf-8'))
        elif path == '/api/state':
            state = get_current_swarm_state()
            with _STATE_LOCK:
                data = _CACHED_JSON_BYTES or json.dumps(state, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        elif path == '/api/role':
            role_id = query.get('id', [''])[0]
            role_file = ROLES_DIR / f"{role_id}.md"
            content = "Không tìm thấy vai trò này."
            if role_file.exists() and role_file.is_file():
                content = role_file.read_text(encoding='utf-8')
            data = json.dumps({'id': role_id, 'content': content}, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        elif path == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            initial_state = get_current_swarm_state()
            self.wfile.write(f"data: {json.dumps(initial_state, ensure_ascii=False)}\n\n".encode('utf-8'))
            self.wfile.flush()

            with CLIENTS_LOCK:
                CLIENTS.add(self)

            try:
                while True:
                    time.sleep(1)
            except Exception:
                pass
            finally:
                with CLIENTS_LOCK:
                    CLIENTS.discard(self)
        else:
            requested_file = resolve_static(path)
            if requested_file is not None:
                self.serve_file(requested_file, STATIC_TYPES[requested_file.suffix.lower()])
            else:
                self.send_response(404)
                self.end_headers()

    def redirect(self, location: str):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def serve_file(self, file_path: Path, content_type: str):
        try:
            content = file_path.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', f'{content_type}; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(content)
        except Exception:
            self.send_response(500)
            self.end_headers()


def broadcast_state(force_refresh=True):
    state = get_current_swarm_state(force_refresh=force_refresh)
    with _STATE_LOCK:
        payload = b"data: " + (_CACHED_JSON_BYTES or json.dumps(state, ensure_ascii=False).encode('utf-8')) + b"\n\n"
    with CLIENTS_LOCK:
        dead_clients = []
        for client in CLIENTS:
            try:
                client.wfile.write(payload)
                client.wfile.flush()
            except Exception:
                dead_clients.append(client)
        for dc in dead_clients:
            CLIENTS.discard(dc)


def file_watcher_loop():
    last_snapshot = {}

    def get_fs_snapshot():
        snap = {}
        if KILO_MGR.exists():
            snap['kilo'] = os.path.getmtime(KILO_MGR)
        if PROJ_FILE.exists():
            snap['project'] = os.path.getmtime(PROJ_FILE)
        if TASKS_DIR.exists():
            for p in TASKS_DIR.rglob('*.md'):
                snap[str(p)] = os.path.getmtime(p)
        if INBOX_DIR.exists():
            for p in INBOX_DIR.rglob('*.md'):
                snap[str(p)] = os.path.getmtime(p)
        if ROLES_DIR.exists():
            for p in ROLES_DIR.glob('*.md'):
                snap[str(p)] = os.path.getmtime(p)
        if KILO_DB.exists():
            try:
                snap['kilo_db'] = KILO_DB.stat().st_mtime
                snap['kilo_db_size'] = KILO_DB.stat().st_size
            except Exception:
                pass
        wal_file = Path(str(KILO_DB) + '-wal')
        if wal_file.exists():
            try:
                snap['kilo_wal'] = wal_file.stat().st_mtime
                snap['kilo_wal_size'] = wal_file.stat().st_size
            except Exception:
                pass
        return snap

    last_snapshot = get_fs_snapshot()

    while True:
        time.sleep(1.0)
        try:
            current_snapshot = get_fs_snapshot()
            if current_snapshot != last_snapshot:
                last_snapshot = current_snapshot
                broadcast_state(force_refresh=True)
        except Exception:
            pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generic Swarm Live Monitor Server")
    parser.add_argument("--port", type=int, default=4200, help="Cổng chạy server (mặc định 4200)")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Địa chỉ lắng nghe (mặc định 127.0.0.1, chỉ máy này; 0.0.0.0 mở cho cả mạng LAN, không có xác thực)")
    args = parser.parse_args()

    server = ThreadedHTTPServer((args.host, args.port), SwarmHandler)
    print(f"🚀 Máy chủ Giám Sát Đa Agent tự động nhận diện đang chạy tại: http://localhost:{args.port}/")
    print(f"📁 Dự án: {load_project_info()['name']}")
    print(f"📡 Luồng SSE: http://localhost:{args.port}/events")
    print(f"📊 Dashboard: http://localhost:{args.port}/dashboard.html")

    watcher_thread = threading.Thread(target=file_watcher_loop, daemon=True)
    watcher_thread.start()

    while True:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng máy chủ giám sát.")
            break
        except Exception:
            time.sleep(0.5)


if __name__ == '__main__':
    main()
