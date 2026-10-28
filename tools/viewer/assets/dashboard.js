    // Dữ liệu do generate-dashboard.py ghi vào data.js (window.DASH). Nội dung từng tài liệu nằm ở docs/<id>.js, nạp khi mở.
    const DASH = window.DASH || {};
    let ALL_CARDS = DASH.cards || [];
    const GATES = DASH.gates || [];
    const STATUS_META = DASH.statusMeta || {};
    let EPIC_META = DASH.epicMeta || {};
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
    window.__setCardMulti = function (projId, id, html) {
      if (MULTI_PROJECTS[projId] && MULTI_PROJECTS[projId].cards) {
        setBody('cards', MULTI_PROJECTS[projId].cards, id, html);
      }
    };

    function loadBody(kind, item, label, cb) {
      if (item.html_body !== undefined) { cb(item.html_body); return; }
      const key = bodyKey(kind, item.id);
      BODY_CALLBACKS[key] = cb;
      const s = document.createElement('script');
      if (CURRENT_PROJECT_ID && MULTI_PROJECTS[CURRENT_PROJECT_ID]) {
        s.src = kind + '/' + bodyFileName(CURRENT_PROJECT_ID) + '_' + bodyFileName(item.id) + '.js';
      } else {
        s.src = kind + '/' + bodyFileName(item.id) + '.js';
      }
      s.onerror = function () {
        // Fallback: thử tìm file không có tiền tố dự án
        const s2 = document.createElement('script');
        s2.src = kind + '/' + bodyFileName(item.id) + '.js';
        s2.onerror = function () {
          delete BODY_CALLBACKS[key];
          cb('<p>Không tải được nội dung (' + label + '). Chạy lại python scripts/generate-dashboard.py.</p>');
        };
        document.head.appendChild(s2);
      };
      document.head.appendChild(s);
    }
    function loadDocBody(doc, cb) { loadBody('docs', doc, doc.path, cb); }
    function loadCardBody(card, cb) { loadBody('cards', card, card.id, cb); }

    let currentStatusFilter = 'ALL';
    let currentViewMode = 'cards';
    let currentDocCategoryFilter = 'ALL';

    function updateProjectHeader(proj) {
      if (!proj) return;
      const titleElem = document.querySelector('.brand-text h1');
      if (titleElem) {
        titleElem.innerHTML = `${proj.name} <span class="badge-phase">Cockpit & Roadmap</span>`;
      }
      const descElem = document.querySelector('.brand-text p');
      if (descElem) {
        descElem.innerHTML = `${proj.desc || 'Hệ thống Quản trị & Điều phối'} • Cập nhật: ${new Date().toLocaleDateString('vi-VN')} ${new Date().toLocaleTimeString('vi-VN')}`;
      }
      const iconElem = document.querySelector('.brand-icon');
      if (iconElem && proj.name) {
        iconElem.textContent = proj.name.charAt(0).toUpperCase();
      }
    }

    function updateKPIAndBadges() {
      const total = ALL_CARDS.length;
      const done = ALL_CARDS.filter(c => c.status === 'done').length;
      const doing = ALL_CARDS.filter(c => c.status === 'doing').length;
      const todo = ALL_CARDS.filter(c => c.status === 'todo').length;
      const code = ALL_CARDS.filter(c => c.is_code_task).length;
      const pct = total > 0 ? Math.round((done / total) * 100) : 0;

      // Cập nhật KPI Overview
      const pctElem = document.getElementById('kpi-pct-val');
      if (pctElem) pctElem.innerHTML = `${pct}% <span class="kpi-sub">(${done}/${total} task)</span>`;
      const barElem = document.getElementById('kpi-pct-bar');
      if (barElem) barElem.style.width = `${pct}%`;
      const doneElem = document.getElementById('kpi-done-val');
      if (doneElem) doneElem.innerHTML = `${done} <span class="kpi-sub">tasks</span>`;
      const doingElem = document.getElementById('kpi-doing-val');
      if (doingElem) doingElem.innerHTML = `${doing} <span class="kpi-sub">tasks</span>`;
      const todoElem = document.getElementById('kpi-todo-val');
      if (todoElem) todoElem.innerHTML = `${todo} <span class="kpi-sub">tasks</span>`;
      const codeElem = document.getElementById('kpi-code-val');
      if (codeElem) codeElem.innerHTML = `${code} <span class="kpi-sub">code tasks</span>`;

      // Cập nhật Radar Summary
      const radarElem = document.getElementById('radar-progress-summary');
      if (radarElem) {
        radarElem.innerHTML = `📍 TRẠNG THÁI TIẾN ĐỘ: Đã xong ${done}/${total} task (${pct}%) • Đang thực hiện ${doing} task`;
      }

      // Cập nhật badges tab
      const tasksBadge = document.getElementById('badge-tasks-count');
      if (tasksBadge) tasksBadge.textContent = total;
      const docBadge = document.getElementById('badge-docs-count');
      if (docBadge) docBadge.textContent = SYSTEM_DOCS.length + ' Mục';
      const mantisBadge = document.getElementById('badge-mantis-count');
      if (mantisBadge) mantisBadge.textContent = CURRENT_MANTIS.total || 0;
      const diagBadge = document.getElementById('badge-diagrams-count');
      if (diagBadge) diagBadge.textContent = CURRENT_DIAGRAMS.length || 0;
      const codeBadge = document.getElementById('badge-code-count');
      if (codeBadge) codeBadge.textContent = code;

      // Cập nhật số đếm trên Task chips
      const chipTotal = document.getElementById('chip-total-cnt');
      if (chipTotal) chipTotal.textContent = total;
      const chipDone = document.getElementById('chip-done-cnt');
      if (chipDone) chipDone.textContent = done;
      const chipDoing = document.getElementById('chip-doing-cnt');
      if (chipDoing) chipDoing.textContent = doing;
      const chipTodo = document.getElementById('chip-todo-cnt');
      if (chipTodo) chipTodo.textContent = todo;
      const chipCode = document.getElementById('chip-code-cnt');
      if (chipCode) chipCode.textContent = code;
    }

    function renderEpicOptions() {
      const select = document.getElementById('epicSelect');
      if (!select) return;
      const epicCounts = {};
      ALL_CARDS.forEach(c => {
        const ep = c.epic || 'GENERAL';
        epicCounts[ep] = (epicCounts[ep] || 0) + 1;
      });
      const epKeys = Object.keys(epicCounts).sort();
      let html = `<option value="ALL">📁 Tất cả Epic (${ALL_CARDS.length})</option>`;
      epKeys.forEach(code => {
        const meta = EPIC_META[code] || {};
        const name = meta.name || `Epic ${code}`;
        html += `<option value="${code}">${code}: ${name} (${epicCounts[code]})</option>`;
      });
      select.innerHTML = html;
    }

    function renderDocCategoryChips() {
      const container = document.getElementById('docCategoryChips');
      if (!container) return;
      const catCounts = {};
      SYSTEM_DOCS.forEach(d => {
        const c = d.category || 'Tài liệu chung';
        catCounts[c] = (catCounts[c] || 0) + 1;
      });
      const cats = Object.keys(catCounts).sort();
      let html = `<button class="chip-btn ${currentDocCategoryFilter === 'ALL' ? 'active' : ''}" data-cat="ALL" onclick="setDocCategoryFilter('ALL', this)">Tất cả (${SYSTEM_DOCS.length})</button>`;
      cats.forEach(c => {
        const act = currentDocCategoryFilter === c ? 'active' : '';
        html += `<button class="chip-btn ${act}" data-cat="${c}" onclick="setDocCategoryFilter('${c}', this)">${c} (${catCounts[c]})</button>`;
      });
      container.innerHTML = html;
    }

    function init() {
      // Khởi tạo dự án mặc định từ MULTI_PROJECTS nếu có
      if (CURRENT_PROJECT_ID && MULTI_PROJECTS[CURRENT_PROJECT_ID]) {
        const p = MULTI_PROJECTS[CURRENT_PROJECT_ID];
        if (p.docs && p.docs.length > 0) SYSTEM_DOCS = p.docs;
        if (p.cards && p.cards.length > 0) ALL_CARDS = p.cards;
        if (p.epics) EPIC_META = p.epics;
        CURRENT_MANTIS = p.mantis || { total: 0, bugs: [] };
        CURRENT_DIAGRAMS = p.diagrams || [];
        updateProjectHeader(p);
      } else {
        // Dự án hiện tại
        CURRENT_MANTIS = (DASH.mantis) || { total: 0, bugs: [] };
        CURRENT_DIAGRAMS = (DASH.diagrams) || [];
      }

      updateKPIAndBadges();
      renderEpicOptions();
      renderDocCategoryChips();
      renderCards();
      renderDocs();
      renderCodeTasks();
      renderGates();
      renderMantisBugs();
      renderDiagrams();
      
      // Phục hồi tab đang đứng từ hash hoặc storage
      let initialTab = 'roadmap';
      const hash = window.location.hash ? window.location.hash.substring(1) : '';
      const storedTab = sessionStorage.getItem('dash_active_tab') || localStorage.getItem('dash_last_tab');
      const validTabs = ['roadmap', 'tasks', 'docs', 'diagrams', 'mantis', 'code', 'gates'];
      if (validTabs.includes(hash)) {
        initialTab = hash;
      } else if (validTabs.includes(storedTab)) {
        initialTab = storedTab;
      }
      switchMainTab(initialTab);

      // Phục hồi tài liệu hoặc task card đang mở nếu có
      try {
        const lastDoc = sessionStorage.getItem('dash_open_doc');
        if (lastDoc && SYSTEM_DOCS.some(d => d.id === lastDoc)) {
          openDocDrawer(lastDoc);
        } else {
          const lastCard = sessionStorage.getItem('dash_open_card');
          if (lastCard && ALL_CARDS.some(c => c.id === lastCard)) {
            openDrawer(lastCard);
          }
        }
      } catch(e) {}

      window.addEventListener('hashchange', () => {
        const h = window.location.hash ? window.location.hash.substring(1) : '';
        if (validTabs.includes(h)) {
          switchMainTab(h);
        }
      });

      window.addEventListener('keydown', (e) => {
        const modal = document.getElementById('imageLightboxModal');
        const isModalOpen = modal && modal.style.display === 'flex';

        if (e.key === 'Escape') {
          if (isModalOpen) {
            closeImageLightbox();
          } else {
            closeDrawer();
          }
        } else if (isModalOpen) {
          if (e.key === '+' || e.key === '=') {
            e.preventDefault();
            zoomLightboxImage(0.25);
          } else if (e.key === '-' || e.key === '_') {
            e.preventDefault();
            zoomLightboxImage(-0.25);
          } else if (e.key === '0') {
            e.preventDefault();
            resetLightboxZoom();
          }
        }
      });
    }

    function switchProject(projId) {
      CURRENT_PROJECT_ID = projId;
      if (MULTI_PROJECTS[projId]) {
        const p = MULTI_PROJECTS[projId];
        SYSTEM_DOCS = p.docs || [];
        ALL_CARDS = (p.cards && p.cards.length > 0) ? p.cards : (DASH.cards || []);
        EPIC_META = p.epics || DASH.epicMeta || {};
        CURRENT_MANTIS = p.mantis || { total: 0, bugs: [] };
        CURRENT_DIAGRAMS = p.diagrams || [];
        updateProjectHeader(p);
      }
      currentDocCategoryFilter = 'ALL';
      currentStatusFilter = 'ALL';
      updateKPIAndBadges();
      renderEpicOptions();
      renderDocCategoryChips();
      renderCards();
      renderDocs();
      renderCodeTasks();
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
        try {
          sessionStorage.setItem('dash_active_tab', tab);
          localStorage.setItem('dash_last_tab', tab);
          if (window.location.hash !== '#' + tab) {
            history.replaceState(null, '', '#' + tab);
          }
        } catch(e) {}
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
              <a href="${d.href || d.path}" class="btn btn-ghost" style="padding: 5px 10px; font-size: 12px;" onclick="event.stopPropagation();" title="Mở trực tiếp">
                ➔
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

      try {
        sessionStorage.setItem('dash_open_doc', docId);
        sessionStorage.removeItem('dash_open_card');
      } catch(e) {}

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

      try {
        sessionStorage.setItem('dash_open_card', taskId);
        sessionStorage.removeItem('dash_open_doc');
      } catch(e) {}

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
      try {
        sessionStorage.removeItem('dash_open_doc');
        sessionStorage.removeItem('dash_open_card');
      } catch(e) {}
      document.getElementById('drawerOverlay').classList.remove('open');
      document.getElementById('drawerPanel').classList.remove('open');
      document.body.style.overflow = 'auto';
    }

    /* ==========================================================================
       IMAGE LIGHTBOX (XEM ẢNH PHÓNG TO VỚI ZOOM & PAN)
       ========================================================================== */
    let lightboxScale = 1;
    let lightboxTranslateX = 0;
    let lightboxTranslateY = 0;
    let isLightboxDragging = false;
    let lightboxStartX = 0;
    let lightboxStartY = 0;
    let lightboxEventsBound = false;

    function updateLightboxTransform() {
      const img = document.getElementById('lightboxImg');
      const percentElem = document.getElementById('lightboxZoomPercent');
      const viewport = document.getElementById('lightboxViewport');
      if (img) {
        img.style.transform = `translate(${lightboxTranslateX}px, ${lightboxTranslateY}px) scale(${lightboxScale})`;
      }
      if (percentElem) {
        percentElem.textContent = Math.round(lightboxScale * 100) + '%';
      }
      if (viewport && !isLightboxDragging) {
        viewport.style.cursor = lightboxScale > 1.05 ? 'grab' : 'zoom-in';
      }
    }

    function zoomLightboxImage(delta, clientX, clientY) {
      const oldScale = lightboxScale;
      let newScale = Math.min(Math.max(lightboxScale + delta, 0.25), 5.0);
      newScale = Math.round(newScale * 100) / 100;
      if (newScale === oldScale) return;

      const viewport = document.getElementById('lightboxViewport');
      if (viewport && Number.isFinite(clientX) && Number.isFinite(clientY)) {
        const rect = viewport.getBoundingClientRect();
        const originX = clientX - (rect.left + rect.width / 2);
        const originY = clientY - (rect.top + rect.height / 2);
        const ratio = newScale / oldScale;
        lightboxTranslateX = originX - (originX - lightboxTranslateX) * ratio;
        lightboxTranslateY = originY - (originY - lightboxTranslateY) * ratio;
      }
      lightboxScale = newScale;
      updateLightboxTransform();
    }

    function resetLightboxZoom() {
      lightboxScale = 1;
      lightboxTranslateX = 0;
      lightboxTranslateY = 0;
      updateLightboxTransform();
    }

    function initLightboxEventListeners() {
      if (lightboxEventsBound) return;
      const viewport = document.getElementById('lightboxViewport');
      if (!viewport) return;

      // Lăn chuột phóng to / thu nhỏ theo tâm trỏ chuột
      viewport.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY < 0 ? 0.2 : -0.2;
        zoomLightboxImage(delta, e.clientX, e.clientY);
      }, { passive: false });

      // Nhấp đúp phóng to 2x hoặc reset về 1x
      viewport.addEventListener('dblclick', (e) => {
        if (e.target.tagName === 'BUTTON') return;
        if (lightboxScale > 1.2) {
          resetLightboxZoom();
        } else {
          zoomLightboxImage(1.0, e.clientX, e.clientY);
        }
      });

      // Nhấp giữ chuột để kéo xem ảnh (Pan / Drag)
      viewport.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        if (e.target.tagName === 'BUTTON') return;
        isLightboxDragging = true;
        lightboxStartX = e.clientX - lightboxTranslateX;
        lightboxStartY = e.clientY - lightboxTranslateY;
        viewport.style.cursor = 'grabbing';
      });

      window.addEventListener('mousemove', (e) => {
        if (!isLightboxDragging) return;
        lightboxTranslateX = e.clientX - lightboxStartX;
        lightboxTranslateY = e.clientY - lightboxStartY;
        updateLightboxTransform();
      });

      window.addEventListener('mouseup', () => {
        if (isLightboxDragging) {
          isLightboxDragging = false;
          updateLightboxTransform();
        }
      });

      lightboxEventsBound = true;
    }

    function openImageLightbox(src, caption) {
      const modal = document.getElementById('imageLightboxModal');
      const img = document.getElementById('lightboxImg');
      const cap = document.getElementById('lightboxCaption');
      if (!modal || !img) return;

      initLightboxEventListeners();
      resetLightboxZoom();

      img.src = src;
      img.alt = caption || 'Hình ảnh';
      if (cap) cap.textContent = caption || '';
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }

    function closeImageLightbox() {
      const modal = document.getElementById('imageLightboxModal');
      if (modal) modal.style.display = 'none';
      resetLightboxZoom();
      const drawer = document.getElementById('drawerPanel');
      document.body.style.overflow = (drawer && drawer.classList.contains('open')) ? 'hidden' : 'auto';
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
        
        const isHtml = d.href && d.href.endsWith('.html');
        const isImg = !isHtml && !d.is_drawio;
        const targetUrl = isHtml ? d.href : (d.preview_img || d.href);
        const escapedName = (d.name || '').replace(/'/g, "\\'");

        let openAction = '';
        let clickHandler = '';

        if (d.is_drawio) {
          openAction = `<a href="${d.href}" download class="btn btn-ghost" style="padding: 4px 8px; font-size: 11px; color: #f59e0b; border-color: rgba(245, 158, 11, 0.4);">Tải Draw.io 📥</a>`;
          clickHandler = `window.location.href='${d.href}'`;
        } else if (isImg) {
          openAction = `<button class="btn btn-ghost" onclick="event.stopPropagation(); openImageLightbox('${targetUrl}', '${escapedName}')" style="padding: 4px 8px; font-size: 11px; color: #38bdf8; border-color: rgba(56, 189, 248, 0.4);">Phóng to ảnh 🔍</button>`;
          clickHandler = `openImageLightbox('${targetUrl}', '${escapedName}')`;
        } else {
          openAction = `<a href="${targetUrl}" class="btn btn-ghost" style="padding: 4px 8px; font-size: 11px; color: #38bdf8; border-color: rgba(56, 189, 248, 0.4);">Xem sơ đồ ➔</a>`;
          clickHandler = `window.location.href='${targetUrl}'`;
        }

        return `
          <div class="diagram-card">
            <div class="diagram-thumb-wrap" onclick="${clickHandler}" style="cursor: pointer;" title="${isImg ? 'Nhấp để xem phóng to tại chỗ' : 'Nhấp để xem sơ đồ'}">
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

    async function refreshDashboardData() {
      const btn = document.getElementById('btnRefreshData');
      if (btn) {
        btn.innerHTML = '🔄 Đang quét & nạp dữ liệu...';
        btn.disabled = true;
      }
      try {
        await fetch('/api/refresh');
      } catch(e) {}
      window.location.reload();
    }

    /* ==========================================================================
       REALTIME AUTO-SYNC (TỰ ĐỘNG ĐỒNG BỘ DỮ LIỆU KHI FILE TRÊN Ổ ĐĨA THAY ĐỔI)
       ========================================================================== */
    let lastKnownVersion = null;
    let isCheckingVersion = false;

    function showRealtimeToast(msg) {
      let toast = document.getElementById('realtimeSyncToast');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'realtimeSyncToast';
        toast.style.cssText = 'position: fixed; bottom: 24px; right: 24px; z-index: 999999; background: rgba(15, 23, 42, 0.95); border: 1px solid #10b981; color: #f8fafc; padding: 10px 18px; border-radius: 8px; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); backdrop-filter: blur(12px); transition: all 0.3s ease;';
        document.body.appendChild(toast);
      }
      toast.innerHTML = `<span style="color: #10b981; font-size: 16px;">⚡</span> ${msg}`;
      toast.style.opacity = '1';
      toast.style.transform = 'translateY(0)';
      setTimeout(() => {
        if (toast) {
          toast.style.opacity = '0';
          toast.style.transform = 'translateY(10px)';
        }
      }, 3500);
    }

    async function checkRealtimeUpdate() {
      if (isCheckingVersion) return;
      isCheckingVersion = true;
      try {
        const res = await fetch('/api/version?t=' + Date.now());
        if (res.ok) {
          const data = await res.json();
          if (lastKnownVersion === null) {
            lastKnownVersion = data.version;
          } else if (data.version && data.version !== lastKnownVersion) {
            lastKnownVersion = data.version;
            showRealtimeToast('Phát hiện tài liệu/task thay đổi! Đang tự động cập nhật Realtime...');
            setTimeout(() => {
              window.location.reload();
            }, 600);
          }
        }
      } catch(e) {}
      isCheckingVersion = false;
    }

    // Tự động kiểm tra thay đổi mỗi 2 giây
    setInterval(checkRealtimeUpdate, 2000);

    window.onload = init;
  
