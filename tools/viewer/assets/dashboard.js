    // Dữ liệu do generate-dashboard.py ghi vào data.js (window.DASH). Nội dung từng tài liệu nằm ở docs/<id>.js, nạp khi mở.
    const DASH = window.DASH || {};
    const ALL_CARDS = DASH.cards || [];
    const GATES = DASH.gates || [];
    const STATUS_META = DASH.statusMeta || {};
    const EPIC_META = DASH.epicMeta || {};
    const PROJECT_INFO = DASH.projectInfo || {};
    const SYSTEM_DOCS = DASH.docs || [];

    // Nạp nội dung theo yêu cầu: kind = 'docs' (tài liệu) hoặc 'cards' (task card); file nằm ở <kind>/<id>.js
    const BODY_CALLBACKS = {};
    function bodyKey(kind, id) { return kind + ':' + id; }
    function bodyFileName(id) { return String(id).replace(/[^A-Za-z0-9_.-]/g, '_'); }
    function setBody(kind, list, id, html) {
      const item = list.find(x => x.id === id);
      if (item) item.html_body = html;
      const key = bodyKey(kind, id);
      const cb = BODY_CALLBACKS[key];
      delete BODY_CALLBACKS[key];
      if (cb) cb(html);
    }
    window.__setDoc = function (id, html) { setBody('docs', SYSTEM_DOCS, id, html); };
    window.__setCard = function (id, html) { setBody('cards', ALL_CARDS, id, html); };
    function loadBody(kind, item, label, cb) {
      if (item.html_body !== undefined) { cb(item.html_body); return; }
      const key = bodyKey(kind, item.id);
      BODY_CALLBACKS[key] = cb;
      const s = document.createElement('script');
      s.src = kind + '/' + bodyFileName(item.id) + '.js';
      s.onerror = function () { delete BODY_CALLBACKS[key]; cb('<p>Không tải được nội dung (' + label + '). Chạy lại python scripts/generate-dashboard.py.</p>'); };
      document.head.appendChild(s);
    }
    function loadDocBody(doc, cb) { loadBody('docs', doc, doc.path, cb); }
    function loadCardBody(card, cb) { loadBody('cards', card, card.id, cb); }

    let currentStatusFilter = 'ALL';
    let currentViewMode = 'cards';
    let currentDocCategoryFilter = 'ALL';

    function init() {
      renderCards();
      renderDocs();
      renderCodeTasks();
      renderGates();
      
      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeDrawer();
      });
    }

    function switchMainTab(tab) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content-pane').forEach(pane => pane.style.display = 'none');
      
      const tabMap = {
        'roadmap': [0, 'tab-roadmap'],
        'tasks': [1, 'tab-tasks'],
        'docs': [2, 'tab-docs'],
        'code': [3, 'tab-code'],
        'gates': [4, 'tab-gates']
      };

      if (tabMap[tab]) {
        document.querySelectorAll('.tab-btn')[tabMap[tab][0]].classList.add('active');
        document.getElementById(tabMap[tab][1]).style.display = 'block';
      }
    }

    function filterByEpicFromRoadmap(epic) {
      const select = document.getElementById('epicSelect');
      if (select) {
        select.value = epic;
      }
      switchMainTab('tasks');
      applyFilters();
    }

    function setStatusFilter(status, elem) {
      currentStatusFilter = status;
      document.querySelectorAll('.chip-btn').forEach(btn => {
        if (btn.parentElement.classList.contains('chip-group') && !btn.hasAttribute('data-cat')) {
          btn.classList.remove('active');
        }
      });
      elem.classList.add('active');
      applyFilters();
    }

    function setDocCategoryFilter(cat, elem) {
      currentDocCategoryFilter = cat;
      document.querySelectorAll('#docCategoryChips .chip-btn').forEach(btn => btn.classList.remove('active'));
      elem.classList.add('active');
      renderDocs();
    }

    function setViewMode(mode) {
      currentViewMode = mode;
      document.getElementById('viewCardsBtn').classList.toggle('active', mode === 'cards');
      document.getElementById('viewTableBtn').classList.toggle('active', mode === 'table');
      document.getElementById('tasksCardsContainer').style.display = mode === 'cards' ? 'grid' : 'none';
      document.getElementById('tasksTableContainer').style.display = mode === 'table' ? 'block' : 'none';
      applyFilters();
    }

    function getFilteredCards() {
      const query = (document.getElementById('searchInput').value || '').toLowerCase().trim();
      const epic = document.getElementById('epicSelect').value;
      if (query) ensureSearchIndex();

      return ALL_CARDS.filter(c => {
        if (epic !== 'ALL' && c.epic !== epic) return false;
        
        if (currentStatusFilter === 'code_only') {
          if (!c.is_code_task) return false;
        } else if (currentStatusFilter !== 'ALL') {
          if (c.status !== currentStatusFilter) return false;
        }

        if (query) {
          const matchId = c.id.toLowerCase().includes(query);
          const matchTitle = c.title.toLowerCase().includes(query);
          const matchRaw = !!(SEARCH_INDEX && (SEARCH_INDEX[c.id] || '').includes(query));
          if (!matchId && !matchTitle && !matchRaw) return false;
        }
        return true;
      });
    }

    // Chỉ mục tìm toàn văn trong nội dung card (chữ thường) nằm ở cards/_search.js, nạp lần đầu khi người dùng gõ tìm kiếm.
    let SEARCH_INDEX = null;
    let SEARCH_LOADING = false;
    window.__setSearch = function (idx) { SEARCH_INDEX = idx; SEARCH_LOADING = false; applyFilters(); };
    function ensureSearchIndex() {
      if (SEARCH_INDEX || SEARCH_LOADING) return;
      SEARCH_LOADING = true;
      const s = document.createElement('script');
      s.src = 'cards/_search.js';
      s.onerror = function () { SEARCH_INDEX = {}; SEARCH_LOADING = false; };
      document.head.appendChild(s);
    }

    function renderCards() {
      const filtered = getFilteredCards();
      const container = document.getElementById('tasksCardsContainer');
      const tableContainer = document.getElementById('tasksTableContainer');

      if (filtered.length === 0) {
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-subtle);">Không tìm thấy task nào phù hợp với bộ lọc.</div>';
        tableContainer.innerHTML = '<div style="text-align: center; padding: 48px; color: var(--text-subtle);">Không tìm thấy task nào.</div>';
        return;
      }

      container.innerHTML = filtered.map(c => {
        const sm = STATUS_META[c.status] || STATUS_META['todo'];
        const isCodeBadge = c.is_code_task ? '<span class="task-tag task-code-badge">💻 Code</span>' : '';
        return `
          <div class="task-card-item status-${c.status}" onclick="openDrawer('${c.id}')">
            <div>
              <div class="task-item-top">
                <span class="task-id-badge">${c.id}</span>
                <span class="status-pill" style="background: ${sm.bg}; color: ${sm.color}; border: 1px solid ${sm.border};">
                  ${sm.icon} ${sm.label}
                </span>
              </div>
              <div class="task-item-title">${c.title}</div>
            </div>
            <div class="task-item-meta">
              <div style="display: flex; gap: 6px; align-items: center;">
                <span class="task-tag">${c.epic}</span>
                <span class="task-tag">${c.owner}</span>
                ${isCodeBadge}
              </div>
              <span style="color: var(--primary-light); font-weight: 600;">Xem chi tiết ↗</span>
            </div>
          </div>
        `;
      }).join('');

      tableContainer.innerHTML = `
        <table class="task-table">
          <thead>
            <tr>
              <th style="width: 100px;">Mã Task</th>
              <th style="width: 130px;">Trạng Thái</th>
              <th>Tên Công Việc</th>
              <th style="width: 80px;">Epic</th>
              <th style="width: 80px;">Vai Trò</th>
              <th style="width: 100px;">Loại</th>
              <th style="width: 100px;">Thao Tác</th>
            </tr>
          </thead>
          <tbody>
            ${filtered.map(c => {
              const sm = STATUS_META[c.status] || STATUS_META['todo'];
              return `
                <tr onclick="openDrawer('${c.id}')">
                  <td><span class="task-id-badge">${c.id}</span></td>
                  <td>
                    <span class="status-pill" style="background: ${sm.bg}; color: ${sm.color}; border: 1px solid ${sm.border};">
                      ${sm.icon} ${sm.label}
                    </span>
                  </td>
                  <td><strong>${c.title}</strong></td>
                  <td><span class="task-tag">${c.epic}</span></td>
                  <td><span class="task-tag">${c.owner}</span></td>
                  <td>${c.is_code_task ? '<span class="task-tag task-code-badge">💻 Code</span>' : '<span class="task-tag">Tài liệu</span>'}</td>
                  <td><span style="color: var(--primary-light); font-weight: 600;">Đọc tài liệu ↗</span></td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      `;
    }

    /* SYSTEM DOCS RENDERING & FILTERING */
    function getFilteredDocs() {
      const query = (document.getElementById('docSearchInput') ? document.getElementById('docSearchInput').value : '').toLowerCase().trim();

      return SYSTEM_DOCS.filter(d => {
        if (currentDocCategoryFilter !== 'ALL' && d.category !== currentDocCategoryFilter) return false;

        if (query) {
          const matchTitle = (d.title || '').toLowerCase().includes(query);
          const matchDesc = (d.desc || '').toLowerCase().includes(query);
          const matchPath = (d.path || '').toLowerCase().includes(query);
          const matchBadge = (d.badge || '').toLowerCase().includes(query);
          if (!matchTitle && !matchDesc && !matchPath && !matchBadge) return false;
        }
        return true;
      });
    }

    function renderDocs() {
      const filtered = getFilteredDocs();
      const container = document.getElementById('docsCatalogGrid');
      const countElem = document.getElementById('docFilteredCount');
      if (countElem) {
        countElem.innerHTML = `Hiển thị <strong>${filtered.length}</strong>/${SYSTEM_DOCS.length} tài liệu`;
      }
      if (!container) return;

      if (filtered.length === 0) {
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-subtle);">Không tìm thấy tài liệu nào phù hợp với từ khóa tìm kiếm.</div>';
        return;
      }

      container.innerHTML = filtered.map(d => `
        <div class="doc-card" onclick="openDocDrawer('${d.id}')">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
              <span class="doc-badge">${d.badge}</span>
              <span style="font-size: 11px; color: var(--text-subtle);">${d.category}</span>
            </div>
            <h3 style="font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 8px; line-height: 1.4;">${d.title}</h3>
            <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px;">${d.desc}</p>
          </div>
          <div style="border-top: 1px solid var(--border-subtle); padding-top: 14px; display: flex; justify-content: space-between; align-items: center; gap: 8px;">
            <code style="font-size: 11px; color: #818cf8; word-break: break-all; max-width: 60%;">${d.path}</code>
            <div style="display: flex; gap: 6px; align-items: center;">
              <button class="btn btn-primary" style="padding: 5px 12px; font-size: 12px;" onclick="event.stopPropagation(); openDocDrawer('${d.id}')">
                📖 Đọc tài liệu
              </button>
              <a href="${d.href || d.path}" target="_blank" class="btn btn-ghost" style="padding: 5px 10px; font-size: 12px;" onclick="event.stopPropagation();" title="Mở file gốc">
                ↗
              </a>
            </div>
          </div>
        </div>
      `).join('');
    }

    function applyDocFilters() {
      renderDocs();
    }

    function openDocDrawer(docId) {
      const doc = SYSTEM_DOCS.find(d => d.id === docId);
      if (!doc) return;

      document.getElementById('drawerTaskId').textContent = doc.badge;
      document.getElementById('drawerTitle').textContent = doc.title;
      
      const pill = document.getElementById('drawerStatusPill');
      pill.textContent = '📚 ' + doc.category;
      pill.style.background = 'rgba(99, 102, 241, 0.15)';
      pill.style.color = '#818cf8';
      pill.style.border = '1px solid rgba(99, 102, 241, 0.3)';

      document.getElementById('drawerEpicBadge').textContent = 'Chuyên mục: ' + doc.category;
      document.getElementById('drawerPhaseBadge').textContent = 'Định dạng: ' + (doc.is_diagram ? 'Interactive HTML/SVG' : 'Markdown HTML');
      document.getElementById('drawerOwnerBadge').textContent = 'Living Docs';

      document.getElementById('drawerBranch').textContent = doc.category;
      document.getElementById('drawerRelPath').textContent = doc.path;
      document.getElementById('drawerRawLink').href = doc.href || doc.path;
      document.getElementById('drawerRawLink').style.display = 'inline-flex';

      document.getElementById('drawerScopeWrap').style.display = 'none';
      document.getElementById('drawerBlockedWrap').style.display = 'none';

      document.getElementById('drawerBodyTitle').textContent = '📄 NỘI DUNG TÀI LIỆU KỸ THUẬT (HTML RENDERED)';
      const mdBox = document.getElementById('drawerMdContent');
      mdBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải nội dung…</p>';
      loadDocBody(doc, function (html) { mdBox.innerHTML = html; });

      document.getElementById('drawerOverlay').classList.add('open');
      document.getElementById('drawerPanel').classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function renderCodeTasks() {
      const codeTasks = ALL_CARDS.filter(c => c.is_code_task && c.status === 'done');
      const container = document.getElementById('codeTasksGrid');
      if (codeTasks.length === 0) {
        container.innerHTML = '<div style="color: var(--text-subtle);">Chưa có task code nào hoàn thành.</div>';
        return;
      }
      container.innerHTML = codeTasks.map(c => `
        <div class="task-card-item status-done" onclick="openDrawer('${c.id}')">
          <div class="task-item-top">
            <span class="task-id-badge">${c.id}</span>
            <span class="badge-code-change">✅ Đã Merge Code</span>
          </div>
          <div class="task-item-title">${c.title}</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;">
            <strong>Nhánh:</strong> <code>${c.branch || 'main'}</code>
          </div>
          <div class="task-item-meta">
            <span class="task-tag task-code-badge">File: ${c.scope_edit.join(', ') || 'Xem chi tiết'}</span>
            <span style="color: var(--primary-light);">Xem diff ↗</span>
          </div>
        </div>
      `).join('');
    }

    function renderGates() {
      const container = document.getElementById('gatesListContainer');
      const gateKeys = Object.keys(GATES);
      if (gateKeys.length === 0) {
        container.innerHTML = '<div style="color: var(--text-subtle);">Chưa có dữ liệu Quality Gate trong tasks/GATES.json.</div>';
        return;
      }
      container.innerHTML = gateKeys.map(k => {
        const g = GATES[k];
        const isApproved = g.approved;
        return `
          <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-weight: 700; font-size: 15px; color: #fff; margin-bottom: 4px;">
                Cổng ${k}: ${isApproved ? '<span style="color: var(--success);">✔ ĐÃ THÔNG QUA</span>' : '<span style="color: var(--danger);">⛔ ĐANG CHẶN</span>'}
              </div>
              <div style="font-size: 13px; color: var(--text-muted);">${g.note || ''}</div>
              <div style="font-size: 12px; color: var(--text-subtle); margin-top: 4px;">Chặn các task: ${g.blocks ? g.blocks.join(', ') : 'Không có'}</div>
            </div>
          </div>
        `;
      }).join('');
    }

    function applyFilters() {
      renderCards();
    }

    function openDrawer(taskId) {
      const card = ALL_CARDS.find(c => c.id === taskId);
      if (!card) return;

      document.getElementById('drawerTaskId').textContent = card.id;
      document.getElementById('drawerTitle').textContent = card.title;
      
      const sm = STATUS_META[card.status] || STATUS_META['todo'];
      const pill = document.getElementById('drawerStatusPill');
      pill.textContent = sm.icon + ' ' + sm.label;
      pill.style.background = sm.bg;
      pill.style.color = sm.color;
      pill.style.border = '1px solid ' + sm.border;

      document.getElementById('drawerEpicBadge').textContent = 'Epic: ' + card.epic;
      document.getElementById('drawerPhaseBadge').textContent = 'Phase: ' + card.phase;
      document.getElementById('drawerOwnerBadge').textContent = 'Owner: ' + card.owner;

      document.getElementById('drawerBranch').textContent = card.branch || 'main';
      document.getElementById('drawerRelPath').textContent = card.rel_path;
      document.getElementById('drawerRawLink').href = card.rel_path;
      document.getElementById('drawerRawLink').style.display = 'inline-flex';
      
      const scopeWrap = document.getElementById('drawerScopeWrap');
      if (card.scope_edit && card.scope_edit.length > 0) {
        scopeWrap.style.display = 'block';
        document.getElementById('drawerScope').textContent = card.scope_edit.join(', ');
      } else {
        scopeWrap.style.display = 'none';
      }

      const blockedWrap = document.getElementById('drawerBlockedWrap');
      if (card.blocked_by && card.blocked_by.length > 0) {
        blockedWrap.style.display = 'block';
        document.getElementById('drawerBlocked').textContent = card.blocked_by.join(', ');
      } else {
        blockedWrap.style.display = 'none';
      }

      document.getElementById('drawerBodyTitle').textContent = '📄 Chi Tiết & Toàn Bộ Tài Liệu Công Việc';
      const cardBox = document.getElementById('drawerMdContent');
      cardBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải nội dung…</p>';
      loadCardBody(card, function (html) { cardBox.innerHTML = html; });

      document.getElementById('drawerOverlay').classList.add('open');
      document.getElementById('drawerPanel').classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
      document.getElementById('drawerOverlay').classList.remove('open');
      document.getElementById('drawerPanel').classList.remove('open');
      document.body.style.overflow = 'auto';
    }

    function copyCode(btn) {
      const code = btn.closest('.code-block-wrap').querySelector('code').innerText;
      navigator.clipboard.writeText(code).then(() => {
        const orig = btn.innerText;
        btn.innerText = 'Đã chép!';
        setTimeout(() => btn.innerText = orig, 1500);
      });
    }

    window.onload = init;
  
