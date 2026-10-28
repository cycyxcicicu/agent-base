    // Dữ liệu do generate-dashboard.py ghi vào data.js (window.DASH). Nội dung từng tài liệu nằm ở docs/<id>.js, nạp khi mở.
    const DASH = window.DASH || {};
    const ALL_CARDS = DASH.cards || [];
    const GATES = DASH.gates || [];
    const STATUS_META = DASH.statusMeta || {};
    const EPIC_META = DASH.epicMeta || {};
    const PROJECT_INFO = DASH.projectInfo || {};
    let SYSTEM_DOCS = DASH.docs || [];
    const MULTI_PROJECTS = DASH.multiProjects || {};
    let CURRENT_PROJECT_ID = DASH.defaultProject || (DASH.projectList && DASH.projectList[0] ? DASH.projectList[0].id : null);
    let CURRENT_MANTIS = { total: 0, bugs: [] };
    let CURRENT_DIAGRAMS = [];
    let currentMantisStatusFilter = 'ALL';

    // Nạp nội dung theo yêu cầu: kind = 'docs' (tài liệu) hoặc 'cards' (task card); file nằm ở <kind>/<id>.js
    const BODY_CALLBACKS = {};
    function bodyKey(kind, id) { return kind + ':' + id; }
    function bodyFileName(id) { return String(id).replace(/[^A-Za-z0-9_.-]/g, '_'); }
    function setBody(kind, list, id, html) {
      const item = list.find(x => String(x.id) === String(id));
      if (item) item.html_body = html;
      const key = bodyKey(kind, id);
      const cb = BODY_CALLBACKS[key];
      delete BODY_CALLBACKS[key];
      if (cb) cb(html);
    }
    window.__setDoc = function (id, html) { setBody('docs', SYSTEM_DOCS, id, html); };
    window.__setCard = function (id, html) { setBody('cards', ALL_CARDS, id, html); };
    window.__setDocMulti = function (projId, id, html) {
      if (MULTI_PROJECTS[projId] && MULTI_PROJECTS[projId].docs) {
        setBody('docs', MULTI_PROJECTS[projId].docs, id, html);
      }
    };

    function loadBody(kind, item, label, cb) {
      if (item.html_body !== undefined) { cb(item.html_body); return; }
      const key = bodyKey(kind, item.id);
      BODY_CALLBACKS[key] = cb;
      const s = document.createElement('script');
      if (kind === 'docs' && CURRENT_PROJECT_ID && MULTI_PROJECTS[CURRENT_PROJECT_ID]) {
        s.src = kind + '/' + bodyFileName(CURRENT_PROJECT_ID) + '_' + bodyFileName(item.id) + '.js';
      } else {
        s.src = kind + '/' + bodyFileName(item.id) + '.js';
      }
      s.onerror = function () { delete BODY_CALLBACKS[key]; cb('<p>Không tải được nội dung (' + label + '). Chạy lại python scripts/generate-dashboard.py.</p>'); };
      document.head.appendChild(s);
    }
    function loadDocBody(doc, cb) { loadBody('docs', doc, doc.path, cb); }
    function loadCardBody(card, cb) { loadBody('cards', card, card.id, cb); }

    let currentStatusFilter = 'ALL';
    let currentViewMode = 'cards';
    let currentDocCategoryFilter = 'ALL';

    function init() {
      // Khởi tạo dự án mặc định từ MULTI_PROJECTS nếu có
      if (CURRENT_PROJECT_ID && MULTI_PROJECTS[CURRENT_PROJECT_ID]) {
        const p = MULTI_PROJECTS[CURRENT_PROJECT_ID];
        if (p.docs && p.docs.length > 0) SYSTEM_DOCS = p.docs;
        CURRENT_MANTIS = p.mantis || { total: 0, bugs: [] };
        CURRENT_DIAGRAMS = p.diagrams || [];
      } else {
        // Dự án hiện tại
        CURRENT_MANTIS = (DASH.mantis) || { total: 0, bugs: [] };
        CURRENT_DIAGRAMS = (DASH.diagrams) || [];
      }

      updateBadges();
      renderCards();
      renderDocs();
      renderCodeTasks();
      renderGates();
      renderMantisBugs();
      renderDiagrams();
      
      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeDrawer();
      });
    }

    function updateBadges() {
      const docBadge = document.getElementById('badge-docs-count');
      if (docBadge) docBadge.textContent = SYSTEM_DOCS.length + ' Mục';
      const mantisBadge = document.getElementById('badge-mantis-count');
      if (mantisBadge) mantisBadge.textContent = CURRENT_MANTIS.total || 0;
      const diagBadge = document.getElementById('badge-diagrams-count');
      if (diagBadge) diagBadge.textContent = CURRENT_DIAGRAMS.length || 0;
    }

    function switchProject(projId) {
      CURRENT_PROJECT_ID = projId;
      if (MULTI_PROJECTS[projId]) {
        const p = MULTI_PROJECTS[projId];
        SYSTEM_DOCS = p.docs || [];
        CURRENT_MANTIS = p.mantis || { total: 0, bugs: [] };
        CURRENT_DIAGRAMS = p.diagrams || [];
      }
      updateBadges();
      currentDocCategoryFilter = 'ALL';
      renderDocs();
      renderMantisBugs();
      renderDiagrams();
    }

    function switchMainTab(tab) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content-pane').forEach(pane => pane.style.display = 'none');
      
      const tabMap = {
        'roadmap': 'tab-roadmap',
        'tasks': 'tab-tasks',
        'docs': 'tab-docs',
        'diagrams': 'tab-diagrams',
        'mantis': 'tab-mantis',
        'code': 'tab-code',
        'gates': 'tab-gates'
      };

      if (tabMap[tab]) {
        const pane = document.getElementById(tabMap[tab]);
        if (pane) pane.style.display = 'block';
        // Active đúng button
        document.querySelectorAll('.tab-btn').forEach(btn => {
          if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes("'" + tab + "'")) {
            btn.classList.add('active');
          }
        });
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

    /* ==========================================================================
       MANTISBT BUGS / ISSUES TRACKER
       ========================================================================== */
    function setMantisStatusFilter(status, elem) {
      currentMantisStatusFilter = status;
      document.querySelectorAll('#mantisStatusChips .chip-btn').forEach(btn => btn.classList.remove('active'));
      elem.classList.add('active');
      renderMantisBugs();
    }

    function filterMantisBugs() {
      renderMantisBugs();
    }

    function renderMantisBugs() {
      const tbody = document.getElementById('mantisTableBody');
      if (!tbody) return;

      const bugs = CURRENT_MANTIS.bugs || [];
      const query = (document.getElementById('mantisSearchInput') ? document.getElementById('mantisSearchInput').value : '').toLowerCase().trim();

      const filtered = bugs.filter(b => {
        if (currentMantisStatusFilter !== 'ALL' && b.status.toLowerCase() !== currentMantisStatusFilter.toLowerCase()) return false;
        if (query) {
          const matchId = (b.id || '').toLowerCase().includes(query);
          const matchSummary = (b.summary || '').toLowerCase().includes(query);
          const matchReporter = (b.reporter || '').toLowerCase().includes(query);
          const matchAssigned = (b.assigned_to || '').toLowerCase().includes(query);
          if (!matchId && !matchSummary && !matchReporter && !matchAssigned) return false;
        }
        return true;
      });

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 48px; color: var(--text-subtle);">Không có bug nào phù hợp (Dự án có tổng cộng ${bugs.length} bug).</td></tr>`;
        return;
      }

      tbody.innerHTML = filtered.map(b => {
        const statusClass = `mantis-status-${(b.status || 'new').toLowerCase()}`;
        const sevClass = `mantis-sev-${(b.severity || 'normal').toLowerCase()}`;
        return `
          <tr>
            <td><code class="task-id-badge">${b.id}</code></td>
            <td><span class="${sevClass}">${b.severity}</span></td>
            <td><span class="mantis-badge ${statusClass}">${b.status}</span></td>
            <td>
              <div style="font-weight: 600; color: #fff; margin-bottom: 2px;">${b.summary}</div>
              <div style="font-size: 11px; color: var(--text-muted);">${b.category} • Nghị quyết: ${b.resolution}</div>
            </td>
            <td><span class="task-tag">${b.reporter}</span></td>
            <td>${b.assigned_to ? `<span class="task-tag" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">${b.assigned_to}</span>` : '<span style="color: #64748b;">(chưa gán)</span>'}</td>
            <td style="font-size: 12px; color: var(--text-muted); font-family: var(--font-mono);">${b.updated}</td>
          </tr>
        `;
      }).join('');
    }

    /* ==========================================================================
       DIAGRAMS GALLERY (SƠ ĐỒ DỰ ÁN)
       ========================================================================== */
    function filterDiagrams() {
      renderDiagrams();
    }

    function renderDiagrams() {
      const container = document.getElementById('diagramsListContainer');
      if (!container) return;

      const diagrams = CURRENT_DIAGRAMS || [];
      const query = (document.getElementById('diagramSearchInput') ? document.getElementById('diagramSearchInput').value : '').toLowerCase().trim();

      const filtered = diagrams.filter(d => {
        if (query && !(d.name || '').toLowerCase().includes(query)) return false;
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-subtle);">Không tìm thấy sơ đồ nào (Dự án có ${diagrams.length} sơ đồ).</div>`;
        return;
      }

      container.innerHTML = filtered.map(d => {
        const thumbHtml = d.preview_img 
          ? `<img src="${d.preview_img}" alt="${d.name}" class="diagram-thumb" loading="lazy" />`
          : `<div style="font-size: 32px; color: #64748b;">📊</div>`;
        
        const openAction = d.is_drawio
          ? `<a href="${d.href}" download class="btn btn-ghost" style="padding: 4px 8px; font-size: 11px; color: #f59e0b; border-color: rgba(245, 158, 11, 0.4);">Tải Draw.io 📥</a>`
          : `<a href="${d.href}" target="_blank" class="btn btn-ghost" style="padding: 4px 8px; font-size: 11px; color: #38bdf8; border-color: rgba(56, 189, 248, 0.4);">Xem ảnh to ↗</a>`;

        return `
          <div class="diagram-card">
            <div class="diagram-thumb-wrap" onclick="window.open('${d.preview_img || d.href}', '_blank')" style="cursor: pointer;">
              ${thumbHtml}
            </div>
            <div class="diagram-info">
              <div>
                <div class="diagram-title" title="${d.name}">${d.name}</div>
                <div class="diagram-meta">${d.ext.toUpperCase()} • ${d.size_kb} KB • ${d.rel_path}</div>
              </div>
              <div class="diagram-actions">
                ${openAction}
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    window.onload = init;
  
