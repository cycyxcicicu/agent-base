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
    # Render cú pháp ảnh Markdown: ![alt](src)
    def _img_sub(m):
        cap = m.group(1).replace("'", "\\'")
        src = m.group(2)
        return (f'<div class="md-img-wrap" style="text-align: center; margin: 18px 0; background: rgba(15,23,42,0.4); padding: 14px; border-radius: 8px; border: 1px solid var(--border-subtle); cursor: pointer;" onclick="openImageLightbox(\'{src}\', \'{cap}\')" title="Nhấp để xem ảnh phóng to tại chỗ">'
                f'<img src="{src}" alt="{cap}" onerror="if(!this.dataset.retried){{this.dataset.retried=1;this.src=this.src.split(\'/\').pop();}}" style="max-width: 100%; height: auto; border-radius: 6px; box-shadow: 0 4px 14px rgba(0,0,0,0.35);" />'
                f'<div style="font-size: 12px; color: var(--text-muted); margin-top: 8px; font-style: italic;">📷 {cap or "Sơ đồ kiến trúc / quy trình"} (Nhấp để xem phóng to)</div>'
                f'</div>')
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', _img_sub, text)
    text = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="md-link">\1 ➔</a>', text)
    return text


def load_mantis_bugs(csv_path: Path) -> dict:
    """Đọc file CSV MantisBT xuất ra và bóc tách thành dữ liệu chuẩn bảng điều khiển."""
    if not csv_path or not csv_path.is_file():
        return {'total': 0, 'bugs': [], 'status_counts': {}, 'severity_counts': {}}

    bugs = []
    status_counts = {}
    severity_counts = {}

    try:
        import csv
        with open(csv_path, encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bug_id = row.get('Id', '').strip()
                if not bug_id:
                    continue
                status = row.get('Status', 'new').strip()
                severity = row.get('Severity', 'normal').strip()
                priority = row.get('Priority', 'normal').strip()
                summary = row.get('Summary', '').strip()
                reporter = row.get('Reporter', '').strip()
                assigned_to = row.get('Assigned To', '').strip()
                updated = row.get('Updated', '').strip()
                category = row.get('Category', 'General').strip()
                resolution = row.get('Resolution', 'open').strip()

                status_counts[status] = status_counts.get(status, 0) + 1
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

                bugs.append({
                    'id': bug_id,
                    'status': status,
                    'severity': severity,
                    'priority': priority,
                    'summary': summary,
                    'reporter': reporter,
                    'assigned_to': assigned_to,
                    'updated': updated,
                    'category': category,
                    'resolution': resolution
                })
    except Exception as e:
        print(f"Lỗi đọc Mantis CSV {csv_path}: {e}")

    return {
        'total': len(bugs),
        'bugs': bugs,
        'status_counts': status_counts,
        'severity_counts': severity_counts
    }


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


def render_testlink_xml_to_html(xml_content: str, rel_path: str, link_prefix: str = '') -> tuple:
    """
    Phân tích file XML TestLink thành giao diện HTML trực quan:
    Trả về: (title, desc, html_body)
    """
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(xml_content)
    except Exception as e:
        escaped = xml_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return "Tệp TestLink XML", "Tệp XML kiểm thử TestLink", f"<pre><code>{escaped}</code></pre>"

    suite_name = root.attrib.get('name', 'Bộ kiểm thử TestLink')
    details_node = root.find('details')
    details_text = details_node.text.strip() if details_node is not None and details_node.text else ''

    testcases = root.findall('.//testcase')
    tc_count = len(testcases)

    file_url = link_prefix + rel_path

    html_parts = [
        f'<div class="testlink-suite-header" style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 18px 20px; margin-bottom: 20px;">',
        f'  <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap;">',
        f'    <div>',
        f'      <div style="font-size: 11px; font-weight: 700; color: #10b981; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 4px;">🧪 TESTLINK XML TEST SUITE</div>',
        f'      <h2 style="font-size: 20px; font-weight: 800; color: #fff; margin: 0 0 6px 0;">{suite_name}</h2>',
        f'      <div style="font-size: 13px; color: var(--text-muted);">{details_text or "Tập hợp các ca kiểm thử tự động nạp vào TestLink"}</div>',
        f'    </div>',
        f'    <div style="display: flex; gap: 8px; align-items: center;">',
        f'      <span class="status-pill" style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); font-weight: 700;">{tc_count} Test Cases</span>',
        f'      <a href="{file_url}" download class="btn btn-primary" style="padding: 6px 14px; font-size: 12px; display: inline-flex; align-items: center; gap: 6px;">📥 Tải file XML</a>',
        f'    </div>',
        f'  </div>',
        f'</div>',
        f'<div style="font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 12px;">Danh Sách {tc_count} Ca Kiểm Thử (Test Cases)</div>',
        f'<div class="testlink-cases-list" style="display: flex; flex-direction: column; gap: 12px;">'
    ]

    for idx, tc in enumerate(testcases):
        tc_name = tc.attrib.get('name', f'Testcase {idx+1}')
        ext_id = tc.findtext('externalid') or f"TC-{idx+1:03d}"
        summary = tc.findtext('summary') or ''
        preconditions = tc.findtext('preconditions') or ''
        importance = tc.findtext('importance') or '2'
        imp_label = {'3': 'Cao (High)', '2': 'Trung bình (Medium)', '1': 'Thấp (Low)'}.get(importance, 'Medium')

        steps = tc.findall('.//step')

        steps_rows = []
        for s in steps:
            s_num = s.findtext('step_number') or ''
            s_action = s.findtext('actions') or ''
            s_result = s.findtext('expectedresults') or ''
            steps_rows.append(f"""
              <tr>
                <td style="width: 45px; text-align: center; font-weight: 700; color: var(--primary-light);">{s_num}</td>
                <td style="font-size: 13px;">{inline_format(s_action)}</td>
                <td style="font-size: 13px; color: #38bdf8;">{inline_format(s_result)}</td>
              </tr>
            """)

        steps_table_html = f"""
          <table class="md-table" style="margin-top: 10px; width: 100%;">
            <thead>
              <tr>
                <th style="width: 45px;">Bước</th>
                <th>Hành động (Action)</th>
                <th>Kết quả mong đợi (Expected Result)</th>
              </tr>
            </thead>
            <tbody>
              {''.join(steps_rows)}
            </tbody>
          </table>
        """ if steps_rows else '<div style="font-size: 12px; color: var(--text-muted); font-style: italic;">Chưa khai báo từng bước chi tiết.</div>'

        preconditions_html = f"""
          <div style="background: rgba(15, 23, 42, 0.4); border-left: 3px solid #f59e0b; padding: 8px 12px; border-radius: 4px; font-size: 12px; color: var(--text-muted); margin: 8px 0;">
            <strong style="color: #f59e0b;">Tiền điều kiện:</strong> {inline_format(preconditions)}
          </div>
        """ if preconditions else ''

        summary_html = f'<div style="font-size: 13px; color: #cbd5e1; margin-bottom: 6px;">{inline_format(summary)}</div>' if summary else ''

        html_parts.append(f"""
          <div class="testlink-card" style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span class="task-id-badge" style="background: rgba(16, 185, 129, 0.2); color: #10b981; font-weight: 700;">{ext_id}</span>
                <span style="font-weight: 700; color: #fff; font-size: 14px;">{tc_name}</span>
              </div>
              <span style="font-size: 11px; color: var(--text-muted);">Ưu tiên: {imp_label}</span>
            </div>
            {summary_html}
            {preconditions_html}
            {steps_table_html}
          </div>
        """)

    html_parts.append('</div>')

    # Mục xem mã XML nguồn
    escaped_raw = xml_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    html_parts.append(f"""
      <details style="margin-top: 24px; background: rgba(15, 23, 42, 0.5); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px 16px;">
        <summary style="font-size: 13px; font-weight: 700; color: var(--primary-light); cursor: pointer;">🔍 Xem mã XML TestLink nguồn</summary>
        <div class="code-block-wrap" style="margin-top: 12px;">
          <pre><code>{escaped_raw}</code></pre>
        </div>
      </details>
    """)

    title = f"TestLink XML: {suite_name}"
    desc = details_text or f"Tệp XML chứa {tc_count} kịch bản kiểm thử TestLink."
    return title, desc, '\n'.join(html_parts)


def discover_system_docs(link_prefix: str = '', root_path: Path = None):
    """Tự động quét toàn bộ thư mục doc/ và docs/ và sinh HTML hoàn chỉnh để đọc trực tiếp trên giao diện."""
    cur_root = root_path if root_path else ROOT
    docs = []

    doc_roots = []
    if (cur_root / 'docs').is_dir():
        doc_roots.append(cur_root / 'docs')
    if (cur_root / 'doc').is_dir():
        doc_roots.append(cur_root / 'doc')

    if not doc_roots:
        return docs

    FOLDER_META = {
        'features': {'category': 'Gói Chức năng & Use Cases (Features)', 'badge': 'Feature'},
        'architecture': {'category': 'Kiến trúc Cốt lõi & Chuẩn hệ thống (Architecture)', 'badge': 'Arch'},
        'references': {'category': 'Tài liệu Tham khảo & Nguồn (References)', 'badge': 'Ref'},
        'governance': {'category': 'Quy trình Tiêu chuẩn & Mẫu biểu (Governance)', 'badge': 'Gov'},
        'delivery': {'category': 'Tiến độ Bàn giao & Bug Mantis (Delivery)', 'badge': 'Delivery'},
        'srs': {'category': 'Đặc tả Chức năng & SRS/FDD', 'badge': 'SRS/FDD'},
        'thiet-ke': {'category': 'Thiết kế Hệ thống & Luồng', 'badge': 'Design'},
        'quy-trinh': {'category': 'Quy trình Nghiệp vụ', 'badge': 'Process'},
        'ky-thuat': {'category': 'Tiêu chuẩn & Kỹ thuật', 'badge': 'Engineering'},
        'bug': {'category': 'Theo dõi & Quản lý Bug', 'badge': 'Bug'},
        'tien-do': {'category': 'Tiến độ & Nhiệm vụ', 'badge': 'Progress'},
        'ban-giao': {'category': 'Bàn giao Dự án', 'badge': 'Handover'},
        'dich-vu': {'category': 'Tài liệu Dịch vụ & Module', 'badge': 'Services'},
        'uat': {'category': 'Kiểm thử Chấp nhận (UAT)', 'badge': 'UAT'},
        'yeu-cau': {'category': 'Yêu cầu Nghiệp vụ', 'badge': 'Requirements'},
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

    for d_dir in doc_roots:
        # 1. Kiểm tra trung tâm sơ đồ trực quan (Archify / HTML / SVG)
        diag_index = d_dir / 'diagrams' / 'index.html'
        if diag_index.exists():
            diag_files = [p for p in (d_dir / 'diagrams').glob('*.*') if p.suffix.lower() in ('.html', '.svg') and p.name != 'index.html']
            diag_count = len(diag_files)
            rel_diag = str(diag_index.relative_to(cur_root)).replace('\\', '/')
            docs.append({
                'id': f'doc_{len(docs)}',
                'category': 'Sơ đồ Kiến trúc & Luồng',
                'title': f"Bản đồ {diag_count} Sơ đồ Kiến trúc & Luồng Nghiệp vụ (Archify)" if diag_count else "Bản đồ Sơ đồ Kiến trúc Archify",
                'path': rel_diag,
                'href': link_prefix + rel_diag,
                'desc': f"Tổng hợp {diag_count} sơ đồ trực quan tương tác SVG: Luồng nghiệp vụ, Module, RBAC và Mô hình ERD." if diag_count else "Tổng hợp sơ đồ trực quan tương tác kiến trúc hệ thống.",
                'badge': f"{diag_count} Diagrams" if diag_count else "Diagrams",
                'html_body': f'<div style="margin-bottom: 14px;"><a href="{link_prefix + rel_diag}?present=true" class="btn btn-primary" style="display: inline-flex;">Mở toàn màn hình ➔</a></div><iframe src="{link_prefix + rel_diag}" style="width: 100%; height: 80vh; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); background: #0b0f19;"></iframe>',
                'is_diagram': True
            })

        # 2. Quét đệ quy các thư mục con trong doc/ hoặc docs/
        skip_folders = {'source', 'converted', 'notes', '__pycache__', 'screens', 'hinh', '_ban-ghi', 'archive'}
        for sub in sorted(d_dir.iterdir()):
            if not sub.is_dir() or sub.name in skip_folders:
                continue
            cat_info = FOLDER_META.get(sub.name.lower(), {'category': sub.name.replace('-', ' ').title(), 'badge': sub.name.upper()})

            for f in sorted(sub.glob('**/*')):
                if not f.is_file():
                    continue
                if f.suffix.lower() not in ('.md', '.html', '.xml') or f.name.lower() in ('index.html', 'readme.md'):
                    continue
                if 'screens' in f.parts or '_ban-ghi' in f.parts:
                    continue

                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    title = None
                    desc = ""
                    is_diagram = False
                    rel_path = f.relative_to(cur_root).as_posix()
                    badge = cat_info['badge']

                    if f.suffix.lower() == '.xml':
                        title, desc, html_body = render_testlink_xml_to_html(content, rel_path, link_prefix)
                        badge = 'TestLink'
                    elif f.suffix.lower() == '.html':
                        m_t = re.search(r'<title>(.*?)</title>', content, re.I)
                        title = m_t.group(1).strip() if m_t else f.stem
                        desc = f"Sơ đồ tương tác hoặc giao diện HTML: {f.name}"
                        html_body = f'<div style="margin-bottom: 14px;"><a href="{link_prefix + rel_path}?present=true" class="btn btn-primary" style="display: inline-flex;">Mở toàn màn hình ➔</a></div><iframe src="{link_prefix + rel_path}" style="width: 100%; height: 75vh; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); background: #0b0f19;"></iframe>'
                        is_diagram = True
                    else:
                        m_t = re.search(r'^#\s+(.+)$', content, re.M)
                        title = m_t.group(1).strip() if m_t else f.stem.replace('-', ' ').replace('_', ' ').title()
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
                        html_body = markdown_to_html(content)
                        is_diagram = False

                    if 'adr' in sub.name.lower():
                        badge = f.stem.split('-')[0].upper() if '-' in f.stem else 'ADR'
                    elif 'rk' in f.stem.lower():
                        badge = f.stem.split('-')[0].upper()

                    doc_id = f"doc_{len(docs)}"
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


def discover_diagrams(proj_root: Path, diagrams_dir_name: str, link_prefix: str = '') -> list:
    """Quét toàn bộ sơ đồ (.drawio, .png, .svg, .html) của một dự án từ kiến trúc chung, tham chiếu và từng Use Case."""
    scan_dirs = []
    
    # 1. Thư mục kiến trúc hệ thống cốt lõi
    for arch_sub in ('doc/architecture/hinh', 'doc/architecture/diagrams', 'docs/architecture/diagrams'):
        arch_cand = proj_root / arch_sub
        if arch_cand.is_dir() and arch_cand not in scan_dirs:
            scan_dirs.append(arch_cand)

    # 2. Thư mục tham chiếu màn hình chuẩn
    for ref_sub in ('doc/references/screens', 'doc/references/diagrams', 'docs/references/screens'):
        ref_cand = proj_root / ref_sub
        if ref_cand.is_dir() and ref_cand not in scan_dirs:
            scan_dirs.append(ref_cand)
        
    # 3. Thư mục hình riêng của từng Use Case trong doc/features/
    features_dir = proj_root / 'doc' / 'features'
    if features_dir.is_dir():
        for uc_dir in sorted(features_dir.iterdir()):
            if uc_dir.is_dir():
                for sub_name in ('hinh', 'diagrams', 'images'):
                    cand = uc_dir / sub_name
                    if cand.is_dir() and cand not in scan_dirs:
                        scan_dirs.append(cand)

    # 4. Thư mục cấu hình ban đầu hoặc fallback
    if diagrams_dir_name:
        custom_cand = proj_root / diagrams_dir_name
        if custom_cand.is_dir() and custom_cand not in scan_dirs:
            scan_dirs.append(custom_cand)

    for fallback_name in ('docs/diagrams', 'doc/srs/hinh', 'doc/hinh'):
        fb = proj_root / fallback_name
        if fb.is_dir() and fb not in scan_dirs:
            scan_dirs.append(fb)

    diagrams = []
    seen_files = set()

    for diag_dir in scan_dirs:
        for p in sorted(diag_dir.glob('*.*')):
            if p.name.startswith('.') or p.name.startswith('_'):
                continue
            ext = p.suffix.lower()
            if ext in ('.png', '.svg', '.drawio', '.html'):
                try:
                    rel_path = str(p.relative_to(proj_root)).replace('\\', '/')
                except Exception:
                    rel_path = p.name

                if rel_path in seen_files:
                    continue
                seen_files.add(rel_path)

                preview_img = None
                if ext == '.drawio':
                    for alt_ext in ('.png', '.svg'):
                        alt_p = diag_dir / (p.stem + alt_ext)
                        if alt_p.is_file():
                            try:
                                preview_img = link_prefix + str(alt_p.relative_to(proj_root)).replace('\\', '/')
                            except Exception:
                                preview_img = None
                            break
                elif ext == '.html':
                    for alt_ext in ('.png', '.svg'):
                        alt_p = diag_dir / (p.stem + alt_ext)
                        if alt_p.is_file():
                            try:
                                preview_img = link_prefix + str(alt_p.relative_to(proj_root)).replace('\\', '/')
                            except Exception:
                                preview_img = None
                            break
                elif ext in ('.png', '.svg'):
                    preview_img = link_prefix + rel_path

                diagrams.append({
                    'name': p.stem,
                    'filename': p.name,
                    'ext': ext,
                    'rel_path': rel_path,
                    'href': link_prefix + rel_path,
                    'preview_img': preview_img,
                    'is_drawio': ext == '.drawio',
                    'size_kb': round(p.stat().st_size / 1024, 1)
                })
    return diagrams


def load_cards_for_project(p_path: Path, epics: dict, phases: dict) -> list:
    """Tự động thu thập toàn bộ Task Cards cho một dự án từ tasks/, doc/tien-do/, doc/srs/."""
    cards = []

    # 1. Quét task cards T-*.md từ doc/delivery/tasks/, doc/features/, và tasks/ (fallback)
    task_search_dirs = [
        p_path / 'doc' / 'delivery' / 'tasks',
        p_path / 'doc' / 'features',
        p_path / 'tasks'
    ]
    seen_card_ids = set()
    for t_dir in task_search_dirs:
        if t_dir.is_dir():
            for path in sorted(t_dir.rglob('T-*.md'), key=lambda p: natural_sort_key(p.name)):
                try:
                    raw = path.read_text(encoding='utf-8')
                    meta, body = parse_front_and_body(raw)
                    card_id = meta.get('id', path.stem)
                    if card_id in seen_card_ids:
                        continue
                    seen_card_ids.add(card_id)
                    title = meta.get('title', '')
                    if not title:
                        t_match = re.search(r'^#\s+(?:T-[A-Za-z0-9_-]+:\s*)?(.+)$', body, re.M)
                        title = t_match.group(1).strip() if t_match else path.stem
                    status = meta.get('status', 'todo').lower()
                    epic = meta.get('epic', 'E0').upper()
                    phase = meta.get('phase', 'DEV')
                    cards.append({
                        'id': card_id,
                        'title': title,
                        'status': status,
                        'owner': meta.get('owner', 'ducnvh'),
                        'epic': epic,
                        'phase': phase,
                        'branch': meta.get('branch', ''),
                        'scope_edit': meta.get('scope_edit', []),
                        'outputs': meta.get('outputs', []),
                        'requirements': meta.get('requirements', []),
                        'blocked_by': meta.get('blocked_by', []),
                        'is_code_task': True,
                        'rel_path': str(path.relative_to(p_path)).replace('\\', '/'),
                        'html_body': markdown_to_html(body),
                        'raw_md': body
                    })
                except Exception:
                    pass

    # 2. Quét doc/tien-do/ để lấy các task tiến độ thực tế của dự án
    tien_do_dir = p_path / 'doc' / 'tien-do'
    if tien_do_dir.is_dir():
        for path in sorted(tien_do_dir.glob('*.md')):
            if path.name.lower() in ('readme.md',) or 'prompt-gemini' in path.name.lower():
                continue

            # Nếu nhóm này đã có các task card con cụ thể trong tasks/ (ví dụ T-04.1 -> T-04.7)
            # thì tài liệu trong doc/tien-do/ là văn bản tiến độ tổng (thuộc progress_docs), không tạo card trùng lặp
            m_td = re.match(r'^(UC|MAN)-?0*(\d+)', path.stem, re.I)
            if m_td:
                num_val = int(m_td.group(2))
                if any(c['id'].startswith(f"T-{num_val:02d}.") or c['id'].startswith(f"T-{num_val}.") for c in cards):
                    continue

            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                title = path.stem
                for line in content.splitlines():
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break

                status = 'doing'
                low = content.lower()
                if 'đã merge' in low or 'hoàn thành' in low or 'exit 0' in low or 'merge commit' in low or 'hoàn công' in low:
                    status = 'done'
                elif 'kế hoạch' in low or 'chưa ghi' in low or 'chờ' in low or 'chưa làm' in low:
                    status = 'todo'

                prefix = path.stem.split('-')[0].upper()
                epic = prefix or 'GENERAL'
                epics[epic] = {'code': epic, 'name': f"Nhóm {epic}", 'desc': f"Các công việc và tiến độ thuộc {epic}"}
                phases['DEV'] = {'code': 'DEV', 'name': 'Phát Triển & Kiểm Thử', 'milestone': ''}

                cards.append({
                    'id': path.stem,
                    'title': title,
                    'status': status,
                    'owner': 'ducnvh',
                    'epic': epic,
                    'phase': 'DEV',
                    'branch': 'develop',
                    'scope_edit': [],
                    'outputs': [],
                    'requirements': [],
                    'blocked_by': [],
                    'is_code_task': True,
                    'rel_path': str(path.relative_to(p_path)).replace('\\', '/'),
                    'html_body': markdown_to_html(content),
                    'raw_md': content
                })
            except Exception:
                pass

    # 3. Quét doc/features/ và doc/srs/ để lấy thêm các chức năng và bug MAN nếu chưa có thẻ task trong tasks/
    for srs_dir in [p_path / 'doc' / 'features', p_path / 'doc' / 'srs']:
        if srs_dir.is_dir():
            for path in sorted(srs_dir.glob('**/*.md')):
                if path.name.lower() in ('readme.md',) or '-doi-chieu' in path.name.lower() or '-thiet-ke-ky-thuat' in path.name.lower() or '-happy-cases' in path.name.lower() or '-mo-ta-man-hinh' in path.name.lower() or '-so-do' in path.name.lower() or '-testlink' in path.name.lower():
                    continue
                if not (path.name.startswith('UC-') or path.name.startswith('MAN-')):
                    continue
                
                # Tránh thêm tài liệu SRS thành card nếu đã có task thực tế (T-xx.* hoặc UC-xx) trong cards
                m_srs = re.match(r'^(UC|MAN)-?0*(\d+)', path.stem, re.I)
                if m_srs:
                    p_code = m_srs.group(1).upper()
                    num_val = int(m_srs.group(2))
                    equiv_keys = [f"{p_code}-{num_val:02d}", f"{p_code}-{num_val}", f"T-{num_val:02d}", f"T-{num_val}"]
                    if any(any(c['id'].startswith(ek) for ek in equiv_keys) for c in cards):
                        continue
    
                # Tránh trùng nếu đã có từ tiến độ
                if any(c['id'] == path.stem for c in cards):
                    continue
                try:
                    content = path.read_text(encoding='utf-8', errors='ignore')
                    title = path.stem
                    for line in content.splitlines():
                        if line.startswith('# '):
                            title = line[2:].strip()
                            break
    
                    prefix = path.stem.split('-')[0].upper()
                    epic = prefix
                    epics[epic] = {'code': epic, 'name': f"Chức năng {epic}", 'desc': f"Đặc tả và thiết kế {epic}"}
    
                    cards.append({
                        'id': path.stem,
                        'title': title,
                        'status': 'done',
                        'owner': 'ducnvh',
                        'epic': epic,
                        'phase': 'DEV',
                        'branch': 'develop',
                        'scope_edit': [],
                        'outputs': [],
                        'requirements': [],
                        'blocked_by': [],
                        'is_code_task': False,
                        'rel_path': str(path.relative_to(p_path)).replace('\\', '/'),
                        'html_body': markdown_to_html(content),
                        'raw_md': content
                })
                except Exception:
                    pass

    return cards


def natural_sort_key(s: str):
    """Sắp xếp tự nhiên theo số và chữ (ví dụ: T-04.1 < T-04.2 < T-04.10, UC-01 < UC-02)."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]


def clean_task_title(title: str, task_id: str = "") -> str:
    """Loại bỏ việc lặp lại mã task trong tiêu đề để hiển thị ngắn gọn, rõ ràng."""
    if not title:
        return task_id or ""
    # Xóa các cụm lặp như 'Task Card: T-04.1 - ', 'T-04: ', 'UC-04: '
    t = re.sub(r'^(?:Task Card:\s*)?(?:(?:UC|T|MAN|BUG)-\d+(?:\.\d+)?(?:\s*-\s*|\s*:\s*))+', '', title, flags=re.I).strip()
    return t or title


def extract_task_key(name: str) -> str:
    """Trích xuất mã task chuẩn (ví dụ: UC-04, UC-03, UC-01, MAN-123, BUG-45, T-01)."""
    if not name:
        return 'GENERAL'
    m = re.search(r'\b(UC-\d+|MAN-\d+|BUG-\d+|T-\d+)\b', name, re.I)
    if m:
        return m.group(1).upper()
    m2 = re.search(r'\b(UC\d+)\b', name, re.I)
    if m2:
        val = m2.group(1).upper()
        return f"{val[:2]}-{val[2:]}"
    parts = name.split('-')
    if len(parts) >= 2 and parts[0].upper() in ('UC', 'MAN', 'BUG', 'T'):
        return f"{parts[0].upper()}-{parts[1]}"
    return parts[0].upper()


def get_task_match_variants(task_key: str) -> list:
    """
    Trả về tất cả các biến thể tương đương của mã task:
    Ví dụ: 'T-04' <-> ['t-04', 't04', 'uc-04', 'uc04', 'uc-4', 't-4']
           'UC-04' <-> ['uc-04', 'uc04', 't-04', 't04', 'uc-4', 't-4']
    """
    variants = [task_key.lower(), task_key.lower().replace('-', '')]
    m = re.match(r'^(T|UC)-(\d+)$', task_key, re.I)
    if m:
        prefix, num_str = m.group(1).upper(), m.group(2)
        num_int = int(num_str)
        alt_prefix = 'UC' if prefix == 'T' else 'T'
        for p in (prefix, alt_prefix):
            variants.extend([
                f"{p}-{num_str}".lower(),
                f"{p}{num_str}".lower(),
                f"{p}-{num_int}".lower(),
                f"{p}{num_int}".lower(),
            ])
    return list(set(variants))


def normalize_group_key(key: str) -> str:
    """Quy chuẩn mã nhóm về UC-xx nếu là cặp T-xx / UC-xx để gom chung các thẻ kỹ thuật và tài liệu nghiệp vụ."""
    m = re.match(r'^T-(\d+)$', key, re.I)
    if m:
        return f"UC-{m.group(1)}"
    return key


def attach_task_360_bundles(cards: list, docs: list, diagrams: list, mantis_data: dict) -> tuple:
    """
    Tự động gom cụm và liên kết Hồ Sơ 360° (Tiến độ, SRS, Sơ đồ, Mantis) cho từng task.
    Trả về: (cards_đã_gắn_bundle, grouped_cards_theo_use_case)
    """
    bugs_list = mantis_data.get('bugs', []) if isinstance(mantis_data, dict) else []

    for c in cards:
        raw_key = extract_task_key(c['id'])
        if raw_key == 'GENERAL':
            raw_key = extract_task_key(c.get('title', ''))
        t_key = normalize_group_key(raw_key)
        c['group_key'] = t_key

        variants = get_task_match_variants(t_key)

        def is_match(text: str) -> bool:
            if not text:
                return False
            # Đối khớp chuẩn xác theo ranh giới token, không cho phép substring lem nhem (ví dụ: 'luot-4' không được khớp 'T-4')
            m = re.match(r'^(UC|T|BUG|MAN)-?0*(\d+)', t_key, re.I)
            if m:
                prefix, num = m.group(1).upper(), int(m.group(2))
                if prefix in ('UC', 'T'):
                    pattern = rf'(?:^|[\s_./\-])(?:UC|T)[-_]?0*{num}(?:[._\-/]|\b)'
                else:
                    pattern = rf'(?:^|[\s_./\-]){prefix}[-_]?0*{num}(?:[._\-/]|\b)'
                return bool(re.search(pattern, text, re.I))
            return t_key.lower() in text.lower()

        # 1. Tiến độ & Nhiệm vụ
        p_docs = []
        for d in docs:
            cat = d.get('category', '').lower()
            path = d.get('path', '').lower()
            if ('tiến độ' in cat or 'tien-do' in path) and (is_match(d.get('path', '')) or is_match(d.get('title', ''))):
                p_docs.append({
                    'id': d['id'],
                    'title': d['title'],
                    'path': d['path'],
                    'href': d['href'],
                    'badge': d.get('badge', 'Tiến độ')
                })

        # 2. SRS & Thiết kế kỹ thuật
        s_docs = []
        for d in docs:
            cat = d.get('category', '').lower()
            path = d.get('path', '').lower()
            # Loại bỏ sơ đồ HTML/ảnh vì đã nằm ở Tab 3 (Sơ đồ & Mockup)
            if d.get('is_diagram') or path.endswith('.html') or '/hinh/' in path:
                continue
            if ('srs' in cat or 'thiết kế' in cat or 'srs' in path) and (is_match(d.get('path', '')) or is_match(d.get('title', ''))):
                s_docs.append({
                    'id': d['id'],
                    'title': d['title'],
                    'path': d['path'],
                    'href': d['href'],
                    'badge': d.get('badge', 'SRS/FDD')
                })

        # 3. Sơ đồ & Mockup
        d_diags = []
        for dg in diagrams:
            fn = dg.get('filename', '')
            rel = dg.get('rel_path', '')
            nm = dg.get('name', '')
            if is_match(fn) or is_match(rel) or is_match(nm):
                d_diags.append({
                    'name': dg.get('name', ''),
                    'filename': dg.get('filename', ''),
                    'href': dg.get('href', ''),
                    'preview_img': dg.get('preview_img'),
                    'size_kb': dg.get('size_kb', 0),
                    'is_drawio': dg.get('is_drawio', False)
                })

        # 4. Mantis & Bug
        m_bugs = []
        for b in bugs_list:
            b_id = str(b.get('id', ''))
            b_sum = b.get('summary', '')
            b_cat = b.get('category', '')
            if is_match(b_id) or is_match(b_sum) or is_match(b_cat):
                m_bugs.append(b)

        c['bundle'] = {
            'task_key': t_key,
            'progress_docs': p_docs,
            'srs_docs': s_docs,
            'diagrams': d_diags,
            'mantis_bugs': m_bugs,
            'total_resources': len(p_docs) + len(s_docs) + len(d_diags) + len(m_bugs)
        }

    # Tạo grouped_cards (Thẻ nhóm Use Case)
    groups = {}
    for c in cards:
        gk = c.get('group_key', 'GENERAL')
        groups.setdefault(gk, []).append(c)

    grouped_cards = []
    for gk, sub_list in sorted(groups.items(), key=lambda x: natural_sort_key(x[0])):
        # Sắp xếp các task con theo thứ tự tự nhiên (T-04.1 < T-04.2 < T-04.3... < T-04.7)
        sub_list = sorted(sub_list, key=lambda s: natural_sort_key(s['id']))
        rep = sub_list[0]
        for it in sub_list:
            t_low = it['title'].lower()
            if 'srs:' in t_low or 'kế hoạch hoàn thiện' in t_low or 'tổng hợp' in t_low:
                rep = it
                break

        st_list = [s['status'] for s in sub_list]
        if any(s in ('doing', 'review') for s in st_list):
            grp_status = 'doing'
        elif any(s == 'blocked' for s in st_list):
            grp_status = 'blocked'
        elif all(s == 'done' for s in st_list):
            grp_status = 'done'
        else:
            grp_status = 'todo'

        # Gom tài nguyên tổng của cả nhóm
        all_p = []
        all_s = []
        all_d = []
        all_b = []
        seen_p = set()
        seen_s = set()
        seen_d = set()
        seen_b = set()

        for sc in sub_list:
            b = sc.get('bundle', {})
            for p in b.get('progress_docs', []):
                if p['id'] not in seen_p:
                    seen_p.add(p['id'])
                    all_p.append(p)
            for s in b.get('srs_docs', []):
                if s['id'] not in seen_s:
                    seen_s.add(s['id'])
                    all_s.append(s)
            for d in b.get('diagrams', []):
                if d['filename'] not in seen_d:
                    seen_d.add(d['filename'])
                    all_d.append(d)
            for bg in b.get('mantis_bugs', []):
                if bg['id'] not in seen_b:
                    seen_b.add(bg['id'])
                    all_b.append(bg)

        # Sắp xếp các tài nguyên theo thứ tự tự nhiên chuẩn
        all_p = sorted(all_p, key=lambda x: natural_sort_key(x.get('title', '')))
        all_s = sorted(all_s, key=lambda x: natural_sort_key(x.get('title', '')))
        all_d = sorted(all_d, key=lambda x: natural_sort_key(x.get('name', '')))
        all_b = sorted(all_b, key=lambda x: natural_sort_key(str(x.get('id', ''))))

        # Ưu tiên lấy tiêu đề nghiệp vụ đại diện từ SRS chính
        best_title = None
        for s in all_s:
            s_t = s.get('title', '')
            if s_t.startswith('SRS —') or s_t.startswith('SRS:') or s_t.startswith('SRS '):
                best_title = s_t
                break

        if not best_title:
            for s in all_s:
                s_t = s.get('title', '')
                if ('bộ lọc' in s_t.lower() or 'xuất excel' in s_t.lower() or 'ẩn/hiện cột' in s_t.lower() or 'hành trình' in s_t.lower()) and not s_t.startswith('Kịch bản') and not s_t.startswith('TestLink'):
                    best_title = s_t
                    break

        if not best_title:
            best_title = rep['title']

        clean_grp_title = clean_task_title(best_title, gk)
        clean_grp_title = re.sub(r'^(?:SRS\s*[—:-]\s*)+', '', clean_grp_title, flags=re.I).strip()
        if not clean_grp_title.upper().startswith(gk):
            clean_grp_title = f"{gk}: {clean_grp_title}"

        sub_cards_data = []
        for s in sub_list:
            c_title = clean_task_title(s['title'], s['id'])
            display_title = f"{s['id']}: {c_title}" if not c_title.startswith(s['id']) else c_title
            sub_cards_data.append({
                'id': s['id'],
                'title': display_title,
                'status': s['status'],
                'rel_path': s.get('rel_path', '')
            })

        grouped_cards.append({
            'id': f"GRP-{gk}",
            'group_key': gk,
            'title': clean_grp_title,
            'status': grp_status,
            'owner': rep.get('owner', 'ducnvh'),
            'epic': gk,
            'phase': rep.get('phase', 'DEV'),
            'branch': rep.get('branch', 'develop'),
            'scope_edit': rep.get('scope_edit', []),
            'outputs': rep.get('outputs', []),
            'requirements': rep.get('requirements', []),
            'blocked_by': rep.get('blocked_by', []),
            'is_code_task': any(s.get('is_code_task', False) for s in sub_list),
            'is_group': True,
            'sub_cards_count': len(sub_list),
            'sub_cards': sub_cards_data,
            'rel_path': rep.get('rel_path', ''),
            'bundle': {
                'task_key': gk,
                'progress_docs': all_p,
                'srs_docs': all_s,
                'diagrams': all_d,
                'mantis_bugs': all_b,
                'total_resources': len(all_p) + len(all_s) + len(all_d) + len(all_b)
            },
            'html_body': rep.get('html_body', ''),
            'raw_md': rep.get('raw_md', '')
        })

    return cards, grouped_cards


def collect_multi_projects(hub_root: Path, link_prefix: str = '../../') -> dict:
    """Thu thập dữ liệu của toàn bộ các dự án đã đăng ký trong projects.json."""
    projects_file = hub_root / 'projects.json'
    registry = {'projects': [], 'default_project': None}
    if projects_file.is_file():
        try:
            registry = json.loads(projects_file.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"Lỗi đọc {projects_file}: {e}")

    projects_data = {}
    project_list = []
    default_id = registry.get('default_project')

    for proj in registry.get('projects', []):
        p_id = proj.get('id', '')
        if not p_id:
            continue
        p_path_str = proj.get('path', '')
        p_path = Path(p_path_str).resolve()
        if not p_path.is_dir():
            continue

        p_name = proj.get('name', p_id)
        p_desc = proj.get('desc', '')
        doc_dir = proj.get('doc_dir', 'doc')
        diagrams_dir = proj.get('diagrams_dir', 'doc/srs/hinh')
        mantis_rel = proj.get('mantis_csv')

        # 1. Thu thập tài liệu
        docs = discover_system_docs(link_prefix, root_path=p_path)

        # 2. Thu thập sơ đồ
        diag_candidates = [
            diagrams_dir,
            'doc/architecture/diagrams',
            'docs/architecture/diagrams',
            'doc/diagrams',
            'docs/diagrams',
            'doc/hinh',
            'doc/srs/hinh'
        ]
        actual_diag_dir = next((d for d in diag_candidates if (p_path / d).is_dir()), diagrams_dir)
        diagrams = discover_diagrams(p_path, actual_diag_dir, link_prefix)

        # 3. Thu thập Mantis bugs
        mantis_file = (p_path / mantis_rel) if mantis_rel else None
        if not mantis_file or not mantis_file.is_file():
            # Thử tự tìm trong doc/bug/mantis/*.csv
            candidates = list((p_path / 'doc' / 'bug' / 'mantis').glob('*.csv')) if (p_path / 'doc' / 'bug' / 'mantis').is_dir() else []
            if candidates:
                mantis_file = sorted(candidates, key=lambda x: x.stat().st_mtime, reverse=True)[0]
        mantis_data = load_mantis_bugs(mantis_file)

        # 4. Thu thập Tasks/Cards
        epics = {}
        phases = {}
        epics_candidates = [
            p_path / 'doc' / 'delivery' / 'tasks' / 'EPICS.md',
            p_path / 'tasks' / 'EPICS.md',
            p_path / 'doc' / 'delivery' / 'roadmap.md'
        ]
        epics_file = next((f for f in epics_candidates if f.is_file()), None)
        if epics_file:
            try:
                # Đọc epics/phases
                txt = epics_file.read_text(encoding='utf-8')
                for line in txt.splitlines():
                    if line.strip().startswith('|---'):
                        continue
                    m_ep = re.match(r'^\|\s*([A-Za-z0-9_]+)\s*\|\s*`?([^|`]+?)`?\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', line)
                    if m_ep and m_ep.group(1).lower() != 'epic':
                        c_epic = m_ep.group(1).strip()
                        epics[c_epic] = {'code': c_epic, 'name': m_ep.group(3).strip(), 'desc': m_ep.group(3).strip()}
            except Exception:
                pass

        cards = load_cards_for_project(p_path, epics, phases)
        cards, grouped_cards = attach_task_360_bundles(cards, docs, diagrams, mantis_data)

        projects_data[p_id] = {
            'id': p_id,
            'name': p_name,
            'desc': p_desc,
            'path': str(p_path),
            'docs': docs,
            'diagrams': diagrams,
            'mantis': mantis_data,
            'epics': epics,
            'phases': phases,
            'cards': cards,
            'grouped_cards': grouped_cards
        }

        project_list.append({
            'id': p_id,
            'name': p_name,
            'desc': p_desc,
            'docs_count': len(docs),
            'diagrams_count': len(diagrams),
            'mantis_count': mantis_data['total']
        })

    if not default_id and project_list:
        default_id = project_list[0]['id']

    # 5. Tải Đồ thị Tri thức (Knowledge Graph) từ agents/knowledge/knowledge-manifest.json
    knowledge_graph = {'nodes_count': 0, 'relations_count': 0, 'nodes': [], 'categories': {}}
    manifest_file = hub_root / 'agents' / 'knowledge' / 'knowledge-manifest.json'
    if manifest_file.is_file():
        try:
            raw_kg = json.loads(manifest_file.read_text(encoding='utf-8'))
            nodes = raw_kg.get('nodes', [])
            categories = {}
            for n in nodes:
                kind = n.get('kind', 'Other')
                categories[kind] = categories.get(kind, 0) + 1
            knowledge_graph = {
                'nodes_count': len(nodes),
                'nodes': nodes,
                'categories': categories
            }
        except Exception as e:
            print(f"Lỗi nạp knowledge-manifest.json: {e}")

    return {
        'all_projects': projects_data,
        'project_list': project_list,
        'default_project': default_id,
        'knowledge_graph': knowledge_graph
    }


