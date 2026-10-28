"""
tools/viewer/dashboard/render.py
Dựng bảng điều khiển dạng nhiều file nhẹ trong build/viewer/ (không còn một file HTML nặng hàng MB):

  index.html        khung trang (đổ số liệu tóm tắt và sơ đồ lộ trình)
  dashboard.css     giao diện (nguồn: tools/viewer/assets/dashboard.css)
  dashboard.js      logic giao diện (nguồn: tools/viewer/assets/dashboard.js)
  data.js           window.DASH: task card, cổng, epic, chỉ mục tài liệu (không kèm nội dung tài liệu)
  docs/<id>.js      nội dung HTML của từng tài liệu, chỉ nạp khi người dùng mở (chạy được cả khi mở file:// trực tiếp)
  monitor.html      trang giám sát agent (nguồn: tools/viewer/assets/monitor.html, cần scripts/watch-swarm.py chạy)
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

from .collect import (
    DOCS_DIR, ROOT, STATUS_META, build_dynamic_roadmap_stages, discover_system_docs, load_all_cards,
    load_code_commits, load_epics_and_phases, load_gates, load_project_info,
)

ASSETS_DIR = Path(__file__).resolve().parent.parent / 'assets'
OUTPUT_DIR = Path(os.environ['VIEWER_OUT']).resolve() if os.environ.get('VIEWER_OUT') else ROOT / 'build' / 'viewer'
# Từ build/viewer/ về gốc dự án: dùng cho liên kết tới file gốc trong docs/.
LINK_PREFIX = '../../'


def _js_json(obj) -> str:
    """JSON an toàn khi nhúng trong thẻ <script>: không để '</' đóng script sớm."""
    return json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


def build_context():
    print("🚀 Đang tự động quét và phân tích toàn bộ dự án...")
    proj_info = load_project_info()
    epics, phases = load_epics_and_phases()
    cards = load_all_cards(epics, phases)
    gates = load_gates()
    git_stat = load_code_commits()
    system_docs = discover_system_docs(LINK_PREFIX)
    roadmap_stages = build_dynamic_roadmap_stages(phases, epics, cards)

    total_tasks = len(cards)
    done_tasks = sum(1 for c in cards if c['status'] == 'done')
    doing_tasks = sum(1 for c in cards if c['status'] == 'doing')
    todo_tasks = sum(1 for c in cards if c['status'] == 'todo')
    code_tasks_count = sum(1 for c in cards if c['is_code_task'])
    pct_complete = round((done_tasks / total_tasks * 100), 1) if total_tasks else 0

    # Đếm số task theo từng epic
    epic_counts = {}
    for c in cards:
        ep = c['epic']
        epic_counts[ep] = epic_counts.get(ep, 0) + 1

    # Thu thập danh sách các danh mục tài liệu độc nhất
    doc_categories = sorted(list({d['category'] for d in system_docs}))
    doc_chips_html = []
    for cat in doc_categories:
        doc_chips_html.append(f'<button class="chip-btn" data-cat="{cat}" onclick="setDocCategoryFilter(\'{cat}\', this)">{cat}</button>')
    doc_category_chips_str = ''.join(doc_chips_html)

    # Tạo JSON nhúng vào HTML
    cards_json = json.dumps(cards, ensure_ascii=False)
    gates_json = json.dumps(gates, ensure_ascii=False)
    status_meta_json = json.dumps(STATUS_META, ensure_ascii=False)
    epic_meta_json = json.dumps(epics, ensure_ascii=False)
    system_docs_json = json.dumps(system_docs, ensure_ascii=False)
    project_info_json = json.dumps(proj_info, ensure_ascii=False)
    doc_categories_json = json.dumps(doc_categories, ensure_ascii=False)

    now_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    brand_letter = proj_info['name'][0].upper() if proj_info['name'] else 'P'

    # Tạo HTML Options cho Epic Dropdown Filter
    epic_options_html = ['<option value="ALL">📁 Tất cả Epic ({})</option>'.format(total_tasks)]
    for ep_code in sorted(epics.keys()):
        ep_name = epics[ep_code].get('name', f"Epic {ep_code}")
        ep_cnt = epic_counts.get(ep_code, 0)
        epic_options_html.append(f'<option value="{ep_code}">{ep_code}: {ep_name} ({ep_cnt})</option>')
    epic_options_str = '\n            '.join(epic_options_html)

    # Tạo HTML cho Roadmap Pipeline Stages
    roadmap_stages_html = []
    for s_idx, st in enumerate(roadmap_stages):
        if st['is_complete']:
            border_color = "var(--success)"
            badge_bg = "rgba(16, 185, 129, 0.2)"
            badge_color = "var(--success)"
            status_label = f"✅ ĐÃ HOÀN TẤT 100% ({st['done']}/{st['total']} task)"
            status_style = "color: var(--success);"
        elif st['is_active']:
            border_color = "#38bdf8"
            badge_bg = "rgba(56, 189, 248, 0.2)"
            badge_color = "#38bdf8"
            status_label = f"🚀 ĐANG TRIỂN KHAI ({st['done']}/{st['total']} task)"
            status_style = "color: #38bdf8;"
        else:
            border_color = "var(--text-subtle)"
            badge_bg = "rgba(148, 163, 184, 0.15)"
            badge_color = "var(--text-muted)"
            status_label = f"⏳ CHỜ THỰC HIỆN ({st['done']}/{st['total']} task)"
            status_style = "color: var(--text-muted);"

        # Render Epic Node Cards trong stage
        nodes_html = []
        for ep in st['epics']:
            is_frontier_class = "active-frontier" if ep['is_frontier'] else ""
            frontier_label = "👉 ĐANG LÀM" if ep['doing_count'] > 0 else "SẴN SÀNG"
            frontier_badge = f'<div style="font-size: 11px; color: #38bdf8; font-weight: 700;">{frontier_label} ➔ Nhấp để xem</div>' if ep['is_frontier'] else ''
            
            nodes_html.append(f"""
              <div class="node-card {is_frontier_class}" onclick="filterByEpicFromRoadmap('{ep['code']}')">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span class="task-id-badge">{ep['code']}</span>
                  <span style="font-size: 12px; font-weight: 700; color: {'var(--success)' if ep['total'] > 0 and ep['done'] == ep['total'] else ('#38bdf8' if ep['doing_count'] > 0 else 'var(--text-muted)')};">
                    {ep['done']}/{ep['total']} Đạt
                  </span>
                </div>
                <div style="font-weight: 700; color: #fff; margin-bottom: 4px; font-size: 13px;">{ep['name']}</div>
                <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">{ep['desc']}</div>
                {frontier_badge}
              </div>
            """)

        # Thêm các thẻ task đang làm (nếu có)
        for act in st['active_tasks']:
            nodes_html.append(f"""
              <div class="node-card active-frontier" onclick="openDrawer('{act['id']}')">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span class="task-id-badge" style="background: rgba(56, 189, 248, 0.25); color: #38bdf8;">TASK TIÊN PHONG</span>
                  <span style="color: #38bdf8; font-weight: 700; font-size: 12px;">ĐANG CHẠY</span>
                </div>
                <div style="font-weight: 700; color: #fff; margin-bottom: 4px; font-size: 13px;">{act['id']}: {act['title']}</div>
                <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px;">Nhánh: <code>{act['branch'] or 'main'}</code> • Vai trò: <code>{act['owner']}</code></div>
                <div style="font-size: 11px; color: #38bdf8; font-weight: 600;">➔ Nhấp vào đây để xem chi tiết task!</div>
              </div>
            """)

        stage_box_html = f"""
        <div class="pipeline-stage" style="border-left: 5px solid {border_color};">
          <div class="stage-header">
            <div class="stage-title">
              <span style="background: {badge_bg}; color: {badge_color}; padding: 4px 10px; border-radius: 6px; font-size: 13px;">CHẶNG {st['stage_num']}</span>
              <span>{st['title']}</span>
            </div>
            <span style="font-size: 13px; font-weight: 700; {status_style}">{status_label}</span>
          </div>
          <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 14px;">
            Mốc mục tiêu: <strong>{st['milestone'] or 'Hoàn tất các chức năng'}</strong> • Tổng cộng: <strong>{st['total']} task cards</strong>.
          </div>
          <div class="stage-nodes-grid">
            {''.join(nodes_html)}
          </div>
        </div>
        """
        roadmap_stages_html.append(stage_box_html)

        # Connector giữa các chặng
        if s_idx < len(roadmap_stages) - 1:
            next_st = roadmap_stages[s_idx + 1]
            gate_divider = f"""
            <div style="display: flex; align-items: center; justify-content: center; gap: 16px; padding: 6px 0;">
              <div style="height: 2px; flex: 1; background: linear-gradient(90deg, transparent, var(--border-accent));"></div>
              <div style="background: var(--bg-card); border: 1px solid var(--border-accent); padding: 8px 18px; border-radius: 20px; font-size: 12px; font-weight: 700; color: var(--primary-light);">
                ⚡ CỔNG CHUYỂN GIAI ĐOẠN: {st['phase_code']} ➔ {next_st['phase_code']}
              </div>
              <div style="height: 2px; flex: 1; background: linear-gradient(90deg, var(--border-accent), transparent);"></div>
            </div>
            """
            roadmap_stages_html.append(gate_divider)

    roadmap_stages_rendered_str = '\n'.join(roadmap_stages_html)

    return {
        'proj_info': proj_info, 'epics': epics, 'cards': cards, 'gates': gates, 'git_stat': git_stat,
        'system_docs': system_docs, 'total_tasks': total_tasks, 'done_tasks': done_tasks,
        'doing_tasks': doing_tasks, 'todo_tasks': todo_tasks, 'code_tasks_count': code_tasks_count,
        'pct_complete': pct_complete, 'now_str': now_str, 'brand_letter': brand_letter,
        'doc_category_chips_str': doc_category_chips_str, 'epic_options_str': epic_options_str,
        'roadmap_stages_rendered_str': roadmap_stages_rendered_str, 'doc_categories': doc_categories,
    }


def _diagram_link(ctx) -> str:
    """Nút mở bản đồ sơ đồ; số sơ đồ đếm thật từ docs/diagrams, không ghi cứng."""
    diag_dir = DOCS_DIR / 'diagrams'
    if not (diag_dir / 'index.html').exists():
        return ''
    count = sum(1 for p in diag_dir.glob('*.html') if p.name != 'index.html')
    label = f'{count} Sơ Đồ Hệ Thống' if count else 'Sơ Đồ Hệ Thống'
    return (f'<a href="{LINK_PREFIX}docs/diagrams/index.html" target="_blank" class="btn btn-ghost" '
            f'style="border-color: rgba(168, 85, 247, 0.5); color: #c084fc;">🗺️ {label} (Archify) ↗</a>')


def write_site(ctx, out_dir: Path = OUTPUT_DIR) -> dict:
    """Ghi toàn bộ site vào out_dir. Trả về số liệu kích thước để kiểm tra."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for sub in ('docs', 'cards'):
        if (out_dir / sub).exists():
            shutil.rmtree(out_dir / sub)
        (out_dir / sub).mkdir()

    def split_bodies(items, sub, setter):
        """Mỗi mục có html_body ghi ra <sub>/<id>.js; trả về danh sách mục đã bỏ html_body (để vào data.js)."""
        slim = []
        for it in items:
            fname = re.sub(r'[^A-Za-z0-9_.-]', '_', str(it['id']))
            body = it.get('html_body', '')
            (out_dir / sub / f"{fname}.js").write_text(f"{setter}({json.dumps(it['id'])}, {_js_json(body)});\n", encoding='utf-8')
            slim.append({k: v for k, v in it.items() if k != 'html_body'})
        return slim

    # 1. Nội dung từng tài liệu / task card ra file riêng, chỉ mục (không kèm nội dung) vào data.js
    index_docs = split_bodies(ctx['system_docs'], 'docs', 'window.__setDoc')
    index_cards = split_bodies(ctx['cards'], 'cards', 'window.__setCard')
    # Chỉ mục tìm toàn văn: nội dung thô của card (chữ thường) gom vào một file, chỉ nạp khi người dùng tìm kiếm
    search_idx = {str(c['id']): str(c.get('raw_md', '')).lower() for c in ctx['cards']}
    (out_dir / 'cards' / '_search.js').write_text('window.__setSearch(' + _js_json(search_idx) + ');\n', encoding='utf-8')
    for c in index_cards:
        c.pop('raw_md', None)

    data = {
        'cards': index_cards, 'gates': ctx['gates'], 'statusMeta': STATUS_META, 'epicMeta': ctx['epics'],
        'projectInfo': ctx['proj_info'], 'docs': index_docs,
    }
    (out_dir / 'data.js').write_text('window.DASH = ' + _js_json(data) + ';\n', encoding='utf-8')

    # 2. Khung trang: thay các thẻ @@TOKEN@@ bằng số liệu
    proj = ctx['proj_info']
    tokens = {
        'NAME': proj['name'], 'DESC': proj['desc'], 'BRAND_LETTER': ctx['brand_letter'], 'NOW_STR': ctx['now_str'],
        'TOTAL_TASKS': ctx['total_tasks'], 'DONE_TASKS': ctx['done_tasks'], 'DOING_TASKS': ctx['doing_tasks'],
        'TODO_TASKS': ctx['todo_tasks'], 'CODE_TASKS_COUNT': ctx['code_tasks_count'], 'PCT_COMPLETE': ctx['pct_complete'],
        'LEN_GATES': len(ctx['gates']), 'LEN_DOCS': len(ctx['system_docs']), 'GIT_STAT': ctx['git_stat'],
        'DOC_CATEGORY_CHIPS_STR': ctx['doc_category_chips_str'], 'EPIC_OPTIONS_STR': ctx['epic_options_str'],
        'ROADMAP_STAGES_RENDERED_STR': ctx['roadmap_stages_rendered_str'], 'DIAGRAM_LINK': _diagram_link(ctx),
    }
    html = (ASSETS_DIR / 'index.template.html').read_text(encoding='utf-8')
    # Thay một lượt bằng regex để giá trị chứa '@@' (nếu có) không bị thay lần hai
    html = re.sub(r'@@([A-Z_]+)@@', lambda m: str(tokens.get(m.group(1), m.group(0))), html)
    (out_dir / 'index.html').write_text(html, encoding='utf-8')

    # 3. Tài nguyên tĩnh
    for name in ('dashboard.css', 'dashboard.js', 'monitor.html'):
        shutil.copyfile(ASSETS_DIR / name, out_dir / name)

    total = sum(p.stat().st_size for p in out_dir.rglob('*') if p.is_file())
    return {'files': sum(1 for p in out_dir.rglob('*') if p.is_file()), 'bytes': total,
            'index_bytes': (out_dir / 'index.html').stat().st_size, 'data_bytes': (out_dir / 'data.js').stat().st_size}


def main():
    ctx = build_context()
    stats = write_site(ctx)
    print(f"✅ Đã tạo Bảng điều khiển: {OUTPUT_DIR / 'index.html'} "
          f"({len(ctx['cards'])} task cards, {len(ctx['system_docs'])} tài liệu, {stats['files']} file, "
          f"tổng {stats['bytes'] // 1024} KB; trang đầu {stats['index_bytes'] // 1024} KB + data {stats['data_bytes'] // 1024} KB)")
    return 0
