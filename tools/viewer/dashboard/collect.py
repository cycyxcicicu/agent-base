"""
tools/viewer/dashboard/collect.py
Thu thập dữ liệu cho bảng điều khiển: thông tin dự án, epic/phase, task card, tài liệu docs/, cổng chất lượng,
nhật ký git, và đổi Markdown sang HTML. Không ghi file; phần ghi nằm ở render.py.
Tự thích ứng với bất kỳ dự án nào theo khung AGENTS.md (đọc PROJECT.md, tasks/EPICS.md, tasks/**/T-*.md, docs/).
"""

import os
import re
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Mặc định: tools/viewer/dashboard/collect.py -> gốc dự án là 3 cấp trên thư mục chứa file này.
# Biến môi trường VIEWER_ROOT cho phép quét một dự án khác (dùng để thử, không ghi vào dự án đó).
ROOT = Path(os.environ['VIEWER_ROOT']).resolve() if os.environ.get('VIEWER_ROOT') else Path(__file__).resolve().parents[3]
TASKS_DIR = ROOT / 'tasks'
DOCS_DIR = ROOT / 'docs'

STATUS_META = {
    'done': {'label': 'Hoàn thành', 'icon': '✅', 'color': '#10b981', 'bg': 'rgba(16, 185, 129, 0.12)', 'border': 'rgba(16, 185, 129, 0.3)'},
    'doing': {'label': 'Đang làm', 'icon': '🔄', 'color': '#3b82f6', 'bg': 'rgba(59, 130, 246, 0.12)', 'border': 'rgba(59, 130, 246, 0.3)'},
    'todo': {'label': 'Chờ làm', 'icon': '⬜', 'color': '#94a3b8', 'bg': 'rgba(148, 163, 184, 0.12)', 'border': 'rgba(148, 163, 184, 0.25)'},
    'review': {'label': 'Đang duyệt', 'icon': '👀', 'color': '#f59e0b', 'bg': 'rgba(245, 158, 11, 0.12)', 'border': 'rgba(245, 158, 11, 0.3)'},
    'blocked': {'label': 'Bị chặn', 'icon': '⛔', 'color': '#ef4444', 'bg': 'rgba(239, 68, 68, 0.12)', 'border': 'rgba(239, 68, 68, 0.3)'},
    'cancelled': {'label': 'Đã hủy', 'icon': '🚫', 'color': '#64748b', 'bg': 'rgba(100, 116, 139, 0.12)', 'border': 'rgba(100, 116, 139, 0.2)'}
}


def load_project_info():
    """Tự động đọc thông tin dự án từ PROJECT.md hoặc thư mục gốc."""
    info = {
        'name': ROOT.name,
        'desc': 'Bảng Điều Khiển Tổng Quan • Sơ Đồ Lộ Trình Task • Thư Viện Tài Liệu Hệ Thống',
        'stack': 'Không xác định',
        'main_branch': 'main',
        'develop_branch': 'develop'
    }
    p_file = ROOT / 'PROJECT.md'
    if p_file.exists():
        try:
            txt = p_file.read_text(encoding='utf-8')
            m_name = re.search(r'\|\s*Tên dự án\s*\|\s*([^|]+)\|', txt, re.I)
            m_desc = re.search(r'\|\s*Mô tả[^\n|]*\|\s*([^|]+)\|', txt, re.I)
            m_stack = re.search(r'\|\s*Stack\s*\|\s*([^|]+)\|', txt, re.I)
            m_main = re.search(r'\|\s*Nhánh chính\s*\|\s*([^|]+)\|', txt, re.I)
            m_dev = re.search(r'\|\s*Nhánh tích hợp\s*\|\s*([^|]+)\|', txt, re.I)

            if m_name and m_name.group(1).strip():
                info['name'] = m_name.group(1).strip()
            if m_desc and m_desc.group(1).strip():
                info['desc'] = m_desc.group(1).strip()
            if m_stack and m_stack.group(1).strip():
                info['stack'] = m_stack.group(1).strip()
            if m_main and m_main.group(1).strip():
                info['main_branch'] = m_main.group(1).strip()
            if m_dev and m_dev.group(1).strip():
                info['develop_branch'] = m_dev.group(1).strip()
        except Exception as e:
            print(f"Lỗi đọc PROJECT.md: {e}")
    return info


def load_epics_and_phases():
    """Tự động đọc danh sách Epic và Phase từ tasks/EPICS.md."""
    epics = {}
    phases = {}
    epics_file = TASKS_DIR / 'EPICS.md'
    if epics_file.exists():
        try:
            txt = epics_file.read_text(encoding='utf-8')
            for line in txt.splitlines():
                if line.strip().startswith('|---'):
                    continue
                # Bảng Epics: | Epic | Thư mục | Tên | Mã yêu cầu | Phase |
                m_ep = re.match(r'^\|\s*([A-Za-z0-9_]+)\s*\|\s*`?([^|`]+?)`?\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', line)
                if m_ep and m_ep.group(1).lower() != 'epic':
                    c_epic = m_ep.group(1).strip()
                    c_folder = m_ep.group(2).strip().rstrip('/')
                    c_name = m_ep.group(3).strip()
                    c_req = m_ep.group(4).strip()
                    c_phase = m_ep.group(5).strip()
                    epics[c_epic] = {
                        'code': c_epic,
                        'folder': c_folder,
                        'name': c_name,
                        'requirements': c_req,
                        'phase': c_phase,
                        'badge': c_phase,
                        'desc': f"{c_name}" + (f" ({c_req})" if c_req and c_req != '—' else "")
                    }
                # Bảng Phase: | Phase | Nghĩa | Mốc |
                m_ph = re.match(r'^\|\s*([A-Za-z0-9_]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', line)
                if m_ph and m_ph.group(1).lower() != 'phase' and m_ph.group(1) not in epics:
                    p_code = m_ph.group(1).strip()
                    p_name = m_ph.group(2).strip()
                    p_milestone = m_ph.group(3).strip()
                    phases[p_code] = {
                        'code': p_code,
                        'name': p_name,
                        'milestone': p_milestone
                    }
        except Exception as e:
            print(f"Lỗi đọc tasks/EPICS.md: {e}")
    return epics, phases


def inline_format(text: str) -> str:
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" class="md-link">\1 ↗</a>', text)
    return text


def markdown_to_html(md: str) -> str:
    """Chuyển đổi cú pháp Markdown đầy đủ (Headings, Tables, Code Blocks, Checklists, Quotes) thành HTML."""
    lines = md.splitlines()
    html_lines = []
    in_code = False
    code_lang = ''
    code_buf = []
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows, html_lines
        if not table_rows:
            in_table = False
            return
        t_html = ['<div class="md-table-wrap"><table class="md-table">']
        has_sep = len(table_rows) > 1 and re.match(r'^[\|\s\-:]+$', table_rows[1])
        start_idx = 0
        if has_sep:
            header_cols = [c.strip() for c in table_rows[0].split('|')[1:-1]]
            t_html.append('<thead><tr>' + ''.join(f'<th>{inline_format(c)}</th>' for c in header_cols) + '</tr></thead>')
            start_idx = 2
            t_html.append('<tbody>')
        else:
            t_html.append('<tbody>')

        for r in table_rows[start_idx:]:
            cols = [c.strip() for c in r.split('|')[1:-1]]
            t_html.append('<tr>' + ''.join(f'<td>{inline_format(c)}</td>' for c in cols) + '</tr>')

        t_html.append('</tbody></table></div>')
        html_lines.append('\n'.join(t_html))
        table_rows = []
        in_table = False

    for line in lines:
        if line.startswith('```'):
            if in_table:
                flush_table()
            if not in_code:
                in_code = True
                code_lang = line[3:].strip()
                code_buf = []
            else:
                in_code = False
                escaped_code = '\n'.join(code_buf).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_lines.append(f'<div class="code-block-wrap"><div class="code-header"><span>{code_lang or "code"}</span><button class="copy-btn" onclick="copyCode(this)">Sao chép</button></div><pre><code>{escaped_code}</code></pre></div>')
            continue

        if in_code:
            code_buf.append(line)
            continue

        # Xử lý bảng markdown (table)
        if line.strip().startswith('|') and line.strip().endswith('|'):
            in_table = True
            table_rows.append(line.strip())
            continue
        elif in_table:
            flush_table()

        if line.startswith('#### '):
            html_lines.append(f'<h4 class="md-h4">{inline_format(line[5:])}</h4>')
        elif line.startswith('### '):
            html_lines.append(f'<h3 class="md-h3">{inline_format(line[4:])}</h3>')
        elif line.startswith('## '):
            html_lines.append(f'<h2 class="md-h2">{inline_format(line[3:])}</h2>')
        elif line.startswith('# '):
            html_lines.append(f'<h1 class="md-h1">{inline_format(line[2:])}</h1>')
        elif line.startswith('> '):
            html_lines.append(f'<blockquote class="md-quote">{inline_format(line[2:])}</blockquote>')
        elif line.startswith('- [x] ') or line.startswith('- [X] '):
            html_lines.append(f'<div class="chk-item chk-done"><span class="chk-box">✔</span><span>{inline_format(line[6:])}</span></div>')
        elif line.startswith('- [ ] '):
            html_lines.append(f'<div class="chk-item chk-pending"><span class="chk-box">○</span><span>{inline_format(line[6:])}</span></div>')
        elif line.startswith('- '):
            html_lines.append(f'<li class="md-li">{inline_format(line[2:])}</li>')
        elif re.match(r'^\d+\.\s+', line):
            m = re.match(r'^\d+\.\s+(.*)$', line)
            html_lines.append(f'<li class="md-li-num">{inline_format(m.group(1))}</li>')
        elif line.strip() == '':
            html_lines.append('<div class="md-spacer"></div>')
        else:
            html_lines.append(f'<p class="md-p">{inline_format(line)}</p>')

    if in_table:
        flush_table()

    return '\n'.join(html_lines)


def parse_front_and_body(text: str):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n(.*)$', text, re.S)
    if not m:
        return {}, text
    front_str = m.group(1)
    body_str = m.group(2)
    meta = {}
    cur_key = None
    for line in front_str.splitlines():
        if re.match(r'^\s+-\s+', line) and cur_key:
            val = re.sub(r'^\s+-\s+', '', line).strip().strip('"\'')
            if not isinstance(meta.get(cur_key), list):
                meta[cur_key] = []
            meta[cur_key].append(val)
            continue
        kv = re.match(r'^([A-Za-z0-9_]+):\s*(.*)$', line)
        if kv:
            cur_key = kv.group(1).lower()
            raw_val = kv.group(2).strip()
            if raw_val == '' or raw_val == '[]':
                meta[cur_key] = []
            elif raw_val.startswith('[') and raw_val.endswith(']'):
                items = [x.strip().strip('"\'') for x in raw_val[1:-1].split(',') if x.strip()]
                meta[cur_key] = items
            else:
                meta[cur_key] = raw_val.strip('"\'')
    return meta, body_str


def discover_system_docs(link_prefix: str = ''):
    """Tự động quét toàn bộ thư mục docs/ và sinh HTML hoàn chỉnh để đọc trực tiếp trên giao diện.

    link_prefix: tiền tố đường dẫn từ nơi đặt trang dashboard về gốc dự án (ví dụ '../../' khi dashboard nằm ở build/viewer/),
    dùng cho href/iframe trỏ tới file gốc. Trường `path` luôn là đường dẫn từ gốc dự án để hiển thị."""
    docs = []
    if not DOCS_DIR.exists():
        return docs

    FOLDER_META = {
        'diagrams': {'category': 'Sơ đồ Kiến trúc & Luồng', 'badge': 'Architecture'},
        'spec': {'category': 'Đặc tả Kỹ thuật & Ranh giới', 'badge': 'Spec'},
        'requirements': {'category': 'Yêu cầu Nghiệp vụ', 'badge': 'Requirements'},
        'adr': {'category': 'Quyết định Kiến trúc', 'badge': 'ADR'},
        'db': {'category': 'Cơ sở Dữ liệu & Migration', 'badge': 'Database'},
        'design': {'category': 'Thiết kế Giao diện (UI/UX)', 'badge': 'UI/UX'},
        'qa': {'category': 'Báo cáo Kiểm thử & QA', 'badge': 'QA Report'},
        'security': {'category': 'Kiểm toán An ninh & CSO', 'badge': 'Security'},
        'risk': {'category': 'Cổng Rủi ro & An toàn', 'badge': 'Risk Gate'},
        'ai': {'category': 'Mô hình & Chiến lược AI', 'badge': 'AI/LLM'},
        'research': {'category': 'Nghiên cứu Công nghệ', 'badge': 'Research'},
        'analysis': {'category': 'Phân tích Hệ thống', 'badge': 'Analysis'},
        'runbooks': {'category': 'Sổ tay Vận hành', 'badge': 'Runbook'},
    }

    # 1. Kiểm tra trung tâm sơ đồ trực quan (Archify / HTML / SVG)
    diag_index = DOCS_DIR / 'diagrams' / 'index.html'
    if diag_index.exists():
        diag_files = [p for p in (DOCS_DIR / 'diagrams').glob('*.*') if p.suffix.lower() in ('.html', '.svg') and p.name != 'index.html']
        diag_count = len(diag_files)
        rel_diag = 'docs/diagrams/index.html'
        docs.append({
            'id': 'doc_0',
            'category': 'Sơ đồ Kiến trúc & Luồng',
            'title': f"Bản đồ {diag_count} Sơ đồ Kiến trúc & Luồng Nghiệp vụ (Archify)" if diag_count else "Bản đồ Sơ đồ Kiến trúc Archify",
            'path': rel_diag,
            'href': link_prefix + rel_diag,
            'desc': f"Tổng hợp {diag_count} sơ đồ trực quan tương tác SVG: Luồng nghiệp vụ, Module, RBAC và Mô hình ERD." if diag_count else "Tổng hợp sơ đồ trực quan tương tác kiến trúc hệ thống.",
            'badge': f"{diag_count} Diagrams" if diag_count else "Diagrams",
            'html_body': f'<div style="margin-bottom: 14px;"><a href="{link_prefix + rel_diag}" target="_blank" class="btn btn-primary" style="display: inline-flex;">Mở bản đồ sơ đồ Archify toàn màn hình ↗</a></div><iframe src="{link_prefix + rel_diag}" style="width: 100%; height: 80vh; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); background: #0b0f19;"></iframe>',
            'is_diagram': True
        })

    # 2. Quét đệ quy các thư mục con trong docs/
    skip_folders = {'source', 'converted', 'notes', '__pycache__', 'screens'}
    for sub in sorted(DOCS_DIR.iterdir()):
        if not sub.is_dir() or sub.name in skip_folders:
            continue
        cat_info = FOLDER_META.get(sub.name, {'category': sub.name.replace('-', ' ').title(), 'badge': sub.name.upper()})
        
        for f in sorted(sub.glob('**/*')):
            if not f.is_file():
                continue
            if f.suffix.lower() not in ('.md', '.html') or f.name.lower() in ('index.html', 'readme.md'):
                continue
            if 'screens' in f.parts:
                continue

            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                title = None
                if f.suffix.lower() == '.html':
                    m_t = re.search(r'<title>(.*?)</title>', content, re.I)
                    if m_t:
                        title = m_t.group(1).strip()
                else:
                    m_t = re.search(r'^#\s+(.+)$', content, re.M)
                    if m_t:
                        title = m_t.group(1).strip()
                if not title:
                    title = f.stem.replace('-', ' ').replace('_', ' ').title()

                # Tóm tắt dòng mô tả đầu tiên
                desc = ""
                for line in content.splitlines():
                    line_s = line.strip()
                    if not line_s or line_s.startswith('#') or line_s.startswith('|') or line_s.startswith('---') or line_s.startswith('```') or line_s.startswith('<!--'):
                        continue
                    desc = re.sub(r'[*_`\[\]]', '', line_s)
                    if len(desc) > 160:
                        desc = desc[:157] + '...'
                    break
                if not desc:
                    desc = f"Tài liệu kỹ thuật tại {f.name}"

                rel_path = f.relative_to(ROOT).as_posix()
                badge = cat_info['badge']
                if 'adr' in sub.name.lower():
                    badge = f.stem.split('-')[0].upper() if '-' in f.stem else 'ADR'
                elif 'rk' in f.stem.lower():
                    badge = f.stem.split('-')[0].upper()

                doc_id = f"doc_{len(docs)}"
                if f.suffix.lower() == '.html':
                    html_body = f'<div style="margin-bottom: 14px;"><a href="{link_prefix + rel_path}" target="_blank" class="btn btn-primary" style="display: inline-flex;">Mở toàn màn hình tab mới ↗</a></div><iframe src="{link_prefix + rel_path}" style="width: 100%; height: 75vh; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); background: #0b0f19;"></iframe>'
                    is_diagram = True
                else:
                    html_body = markdown_to_html(content)
                    is_diagram = False

                docs.append({
                    'id': doc_id,
                    'category': cat_info['category'],
                    'title': title,
                    'path': rel_path,
                    'href': link_prefix + rel_path,
                    'desc': desc,
                    'badge': badge,
                    'html_body': html_body,
                    'is_diagram': is_diagram
                })
            except Exception:
                pass

    return docs


def load_all_cards(epics, phases):
    """Đọc toàn bộ thẻ task cards và tự động bổ sung Epic/Phase nếu chưa khai báo."""
    cards = []
    if not TASKS_DIR.exists():
        return cards

    for path in TASKS_DIR.rglob('T-*.md'):
        try:
            raw = path.read_text(encoding='utf-8')
            meta, body = parse_front_and_body(raw)
            card_id = meta.get('id', path.stem)
            title = meta.get('title', '')
            if not title:
                t_match = re.search(r'^#\s+(?:T-[A-Za-z0-9_-]+:\s*)?(.+)$', body, re.M)
                title = t_match.group(1).strip() if t_match else path.stem

            status = meta.get('status', 'todo').lower()
            owner = meta.get('owner', 'lead').lower()
            epic = meta.get('epic', 'E0').upper()
            phase = meta.get('phase', 'PT')
            branch = meta.get('branch', '')
            scope_edit = meta.get('scope_edit', [])
            if isinstance(scope_edit, str):
                scope_edit = [scope_edit]
            outputs = meta.get('outputs', [])
            if isinstance(outputs, str):
                outputs = [outputs]
            requirements = meta.get('requirements', [])
            if isinstance(requirements, str):
                requirements = [requirements]
            blocked_by = meta.get('blocked_by', [])
            if isinstance(blocked_by, str):
                blocked_by = [blocked_by]

            is_code_task = any(
                'frontend' in str(s) or 'backend' in str(s) or '.py' in str(s) or '.ts' in str(s) or '.tsx' in str(s)
                for s in (scope_edit + outputs)
            )

            # Tự động đồng bộ epic/phase vào danh mục nếu chưa có
            if epic not in epics:
                epics[epic] = {
                    'code': epic,
                    'folder': path.parent.name,
                    'name': f"Epic {epic}",
                    'requirements': '—',
                    'phase': phase,
                    'badge': phase,
                    'desc': f"Tập hợp các task thuộc {epic}"
                }
            if phase not in phases:
                phases[phase] = {
                    'code': phase,
                    'name': f"Giai đoạn {phase}",
                    'milestone': ''
                }

            html_body = markdown_to_html(body)

            cards.append({
                'id': card_id,
                'title': title,
                'status': status,
                'owner': owner,
                'epic': epic,
                'phase': phase,
                'branch': branch,
                'scope_edit': scope_edit,
                'outputs': outputs,
                'requirements': requirements,
                'blocked_by': blocked_by,
                'is_code_task': is_code_task,
                'rel_path': str(path.relative_to(ROOT)).replace('\\', '/'),
                'html_body': html_body,
                'raw_md': body
            })
        except Exception as e:
            print(f"Lỗi đọc card {path}: {e}")

    def sort_key(c):
        m = re.search(r'\d+', c['id'])
        return (c['epic'], int(m.group(0)) if m else 9999, c['id'])

    cards.sort(key=sort_key)
    return cards


def load_gates():
    gates_file = TASKS_DIR / 'GATES.json'
    if gates_file.exists():
        try:
            return json.loads(gates_file.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}


def load_code_commits():
    try:
        out = subprocess.check_output(
            ['git', 'log', '-n', '25', '--oneline', '--stat'],
            cwd=str(ROOT),
            text=True,
            encoding='utf-8',
            stderr=subprocess.DEVNULL  # dự án chưa git init thì không in "fatal: not a git repository"
        )
        return out
    except Exception:
        return "Chưa có log git."


def build_dynamic_roadmap_stages(phases, epics, cards):
    """Tự động xây dựng các chặng Lộ trình từ danh sách Phase & Epic thực tế."""
    stages = []
    phase_keys = list(phases.keys())
    if not phase_keys:
        phase_keys = sorted(list({c['phase'] for c in cards if c.get('phase')}))
        if not phase_keys:
            phase_keys = ['DEV']

    # Gom các epics theo phase
    phase_epics = {p: [] for p in phase_keys}
    for ep_code, ep_data in epics.items():
        ph = ep_data.get('phase', phase_keys[0])
        if ph not in phase_epics:
            phase_epics[ph] = []
        phase_epics[ph].append(ep_code)

    has_found_frontier = False

    for idx, p_code in enumerate(phase_keys):
        p_info = phases.get(p_code, {'name': f"Giai đoạn {p_code}", 'milestone': ''})
        assigned_epics = phase_epics.get(p_code, [])
        p_cards = [c for c in cards if c.get('phase') == p_code or (c.get('epic') in assigned_epics)]

        stage_total = len(p_cards)
        stage_done = sum(1 for c in p_cards if c['status'] == 'done')
        stage_doing = sum(1 for c in p_cards if c['status'] in ('doing', 'review'))
        stage_blocked = sum(1 for c in p_cards if c['status'] == 'blocked')

        is_complete = stage_total > 0 and stage_done == stage_total
        is_active = False
        if not is_complete and not has_found_frontier:
            is_active = True
            has_found_frontier = True

        epic_nodes = []
        for ep_code in assigned_epics:
            ep_meta = epics.get(ep_code, {'name': f"Epic {ep_code}", 'desc': ''})
            e_cards = [c for c in p_cards if c.get('epic') == ep_code]
            e_total = len(e_cards)
            e_done = sum(1 for c in e_cards if c['status'] == 'done')
            e_doing = [c for c in e_cards if c['status'] in ('doing', 'review')]

            is_epic_frontier = is_active and (len(e_doing) > 0 or (e_done < e_total and len(epic_nodes) == 0))
            epic_nodes.append({
                'code': ep_code,
                'name': ep_meta.get('name', f"Epic {ep_code}"),
                'desc': ep_meta.get('desc', ''),
                'total': e_total,
                'done': e_done,
                'doing_count': len(e_doing),
                'doing_tasks': e_doing,
                'is_frontier': is_epic_frontier
            })

        stages.append({
            'stage_num': idx + 1,
            'phase_code': p_code,
            'title': p_info.get('name', f"Giai đoạn {p_code}"),
            'milestone': p_info.get('milestone', ''),
            'total': stage_total,
            'done': stage_done,
            'doing': stage_doing,
            'blocked': stage_blocked,
            'is_complete': is_complete,
            'is_active': is_active,
            'epics': epic_nodes,
            'active_tasks': [c for c in p_cards if c['status'] in ('doing', 'review')][:4]
        })

    return stages


