    // Dữ liệu do generate-dashboard.py ghi vào data.js (window.DASH). Nội dung từng tài liệu nằm ở docs/<id>.js, nạp khi mở.
    const DASH = window.DASH || {};
    let ALL_CARDS = DASH.cards || [];
    let GROUPED_CARDS = DASH.groupedCards || [];
    let isGroupingMode = true; // Mặc định gom nhóm Use Case
    const GATES = DASH.gates || [];
    const STATUS_META = DASH.statusMeta || {};
    let EPIC_META = DASH.epicMeta || {};
    const PROJECT_INFO = DASH.projectInfo || {};
    let SYSTEM_DOCS = DASH.docs || [];
    const MULTI_PROJECTS = DASH.multiProjects || {};
    let CURRENT_PROJECT_ID = DASH.defaultProject || (DASH.projectList && DASH.projectList[0] ? DASH.projectList[0].id : null);
    let CURRENT_MANTIS = { total: 0, bugs: [] };
    let CURRENT_DIAGRAMS = [];
    let CURRENT_KNOWLEDGE = DASH.knowledgeGraph || { nodes_count: 0, nodes: [], categories: {} };
    let currentKgKindFilter = 'ALL';
    let currentMantisStatusFilter = 'ALL';

    function toggleGroupingMode(enableGroup) {
      isGroupingMode = enableGroup;
      const grpBtn = document.getElementById('viewGroupedBtn');
      const crdBtn = document.getElementById('viewCardsBtn');
      if (grpBtn) grpBtn.classList.toggle('active', isGroupingMode);
      if (crdBtn) crdBtn.classList.toggle('active', !isGroupingMode);
      renderCards();
    }

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
      const cacheBust = '?t=' + Date.now();
      if (CURRENT_PROJECT_ID && MULTI_PROJECTS[CURRENT_PROJECT_ID]) {
        s.src = kind + '/' + bodyFileName(CURRENT_PROJECT_ID) + '_' + bodyFileName(item.id) + '.js' + cacheBust;
      } else {
        s.src = kind + '/' + bodyFileName(item.id) + '.js' + cacheBust;
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
      const kgBadge = document.getElementById('badge-knowledge-count');
      if (kgBadge) kgBadge.textContent = CURRENT_KNOWLEDGE.nodes_count || (CURRENT_KNOWLEDGE.nodes ? CURRENT_KNOWLEDGE.nodes.length : 0);
      const kgTotalElem = document.getElementById('kg-total-nodes');
      if (kgTotalElem) kgTotalElem.textContent = CURRENT_KNOWLEDGE.nodes_count || (CURRENT_KNOWLEDGE.nodes ? CURRENT_KNOWLEDGE.nodes.length : 0);
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
        if (p.grouped_cards && p.grouped_cards.length > 0) GROUPED_CARDS = p.grouped_cards;
        if (p.epics) EPIC_META = p.epics;
        CURRENT_MANTIS = p.mantis || { total: 0, bugs: [] };
        CURRENT_DIAGRAMS = p.diagrams || [];
        updateProjectHeader(p);
      } else {
        // Dự án hiện tại
        if (DASH.groupedCards && DASH.groupedCards.length > 0) GROUPED_CARDS = DASH.groupedCards;
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
      renderKnowledgeGraph();
      
      // Phục hồi tab đang đứng từ hash hoặc storage
      let initialTab = 'roadmap';
      const hash = window.location.hash ? window.location.hash.substring(1) : '';
      const storedTab = sessionStorage.getItem('dash_active_tab') || localStorage.getItem('dash_last_tab');
      const validTabs = ['roadmap', 'tasks', 'docs', 'diagrams', 'mantis', 'knowledge', 'code', 'gates'];
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
        GROUPED_CARDS = (p.grouped_cards && p.grouped_cards.length > 0) ? p.grouped_cards : (DASH.groupedCards || []);
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
      renderKnowledgeGraph();
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
        'knowledge': 'tab-knowledge',
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
        if (tab === 'knowledge') {
          setTimeout(() => {
            if (typeof initOrUpdate3DGraph === 'function' && currentKgViewMode === '3d') {
              initOrUpdate3DGraph();
            }
          }, 80);
        }
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
      const sourceList = (isGroupingMode && GROUPED_CARDS && GROUPED_CARDS.length > 0) ? GROUPED_CARDS : ALL_CARDS;
      const query = (document.getElementById('searchInput').value || '').toLowerCase().trim();
      const epic = document.getElementById('epicSelect').value;
      if (query) ensureSearchIndex();

      return sourceList.filter(c => {
        if (epic !== 'ALL' && c.epic !== epic) return false;
        
        if (currentStatusFilter === 'code_only') {
          if (!c.is_code_task) return false;
        } else if (currentStatusFilter !== 'ALL') {
          if (c.status !== currentStatusFilter) return false;
        }

        if (query) {
          const matchId = (c.id || '').toLowerCase().includes(query);
          const matchTitle = (c.title || '').toLowerCase().includes(query);
          const matchGroup = (c.group_key || '').toLowerCase().includes(query);
          const matchRaw = !!(SEARCH_INDEX && (SEARCH_INDEX[c.id] || '').includes(query));
          if (!matchId && !matchTitle && !matchGroup && !matchRaw) return false;
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
        const bundle = c.bundle || {};
        let bundleBadgesHtml = '';
        if (bundle.total_resources > 0 || c.is_group) {
          const parts = [];
          if (c.is_group && c.sub_cards_count) {
            parts.push(`<span class="bundle-badge highlight">🗂️ ${c.sub_cards_count} thẻ con</span>`);
          }
          if (bundle.progress_docs && bundle.progress_docs.length > 0) {
            parts.push(`<span class="bundle-badge">📋 ${bundle.progress_docs.length} Tiến độ</span>`);
          }
          if (bundle.srs_docs && bundle.srs_docs.length > 0) {
            parts.push(`<span class="bundle-badge">📚 ${bundle.srs_docs.length} SRS & Thiết kế</span>`);
          }
          if (bundle.diagrams && bundle.diagrams.length > 0) {
            parts.push(`<span class="bundle-badge">📊 ${bundle.diagrams.length} Sơ đồ</span>`);
          }
          if (bundle.mantis_bugs && bundle.mantis_bugs.length > 0) {
            parts.push(`<span class="bundle-badge" style="color: #f87171;">🐞 ${bundle.mantis_bugs.length} Bug</span>`);
          }
          bundleBadgesHtml = `<div class="bundle-badge-row">${parts.join('')}</div>`;
        }
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
              ${bundleBadgesHtml}
            </div>
            <div class="task-item-meta">
              <div style="display: flex; gap: 6px; align-items: center;">
                <span class="task-tag">${c.epic}</span>
                <span class="task-tag">${c.owner}</span>
                ${isCodeBadge}
              </div>
              <span style="color: var(--primary-light); font-weight: 600;">Hồ sơ 360° ↗</span>
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

    let currentDrawer360Tab = 'progress';

    function switchDrawer360Tab(tabName) {
      currentDrawer360Tab = tabName;
      ['progress', 'srs', 'diagrams', 'mantis'].forEach(t => {
        const btn = document.getElementById('dTabBtn-' + t);
        const pane = document.getElementById('drawerPane' + t.charAt(0).toUpperCase() + t.slice(1));
        if (btn) btn.classList.toggle('active', t === tabName);
        if (pane) pane.style.display = (t === tabName) ? 'block' : 'none';
      });
    }

    function openDrawer(taskId) {
      let card = ALL_CARDS.find(c => c.id === taskId) || GROUPED_CARDS.find(c => c.id === taskId);
      if (!card) {
        card = ALL_CARDS.find(c => String(c.id).toLowerCase() === String(taskId).toLowerCase()) ||
               GROUPED_CARDS.find(c => String(c.id).toLowerCase() === String(taskId).toLowerCase());
      }
      if (!card) return;

      try {
        sessionStorage.setItem('dash_open_card', taskId);
        sessionStorage.removeItem('dash_open_doc');
      } catch(e) {}

      document.getElementById('drawerTaskId').textContent = card.group_key || card.id;
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

      document.getElementById('drawerBranch').textContent = card.branch || 'develop';
      document.getElementById('drawerRelPath').textContent = card.rel_path || '';
      document.getElementById('drawerRawLink').href = card.rel_path || '#';
      document.getElementById('drawerRawLink').style.display = card.rel_path ? 'inline-flex' : 'none';
      
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

      // ==========================================
      // THIẾT LẬP HỒ SƠ 360° THEO 4 TABS
      // ==========================================
      const bundle = card.bundle || {};
      const pDocs = bundle.progress_docs || [];
      const sDocs = bundle.srs_docs || [];
      const diags = bundle.diagrams || [];
      const bugs = bundle.mantis_bugs || [];

      // 1. Cập nhật số đếm badge
      const hasSubCards = card.is_group && card.sub_cards && card.sub_cards.length > 0;
      const pCount = hasSubCards ? card.sub_cards.length : (pDocs.length > 0 ? pDocs.length : 1);
      document.getElementById('tabBadgeProgress').textContent = pCount;
      document.getElementById('tabBadgeSrs').textContent = sDocs.length;
      document.getElementById('tabBadgeDiagrams').textContent = diags.length;
      document.getElementById('tabBadgeMantis').textContent = bugs.length;

      // 2. Tab 1: Tiến độ & Nhiệm vụ
      const pSubNav = document.getElementById('drawerProgressSubNav');
      const cardBox = document.getElementById('drawerMdContent');
      if (hasSubCards && card.sub_cards.length > 1) {
        // ƯU TIÊN 1: Hiển thị danh sách các thẻ kỹ thuật con (T-04.1 -> T-04.7)
        const sortedSubCards = card.sub_cards.slice().sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true, sensitivity: 'base' }));
        pSubNav.style.display = 'flex';
        pSubNav.innerHTML = sortedSubCards.map((sc, idx) => `
          <button class="drawer-subnav-btn ${idx === 0 ? 'active' : ''}" onclick="selectDrawerCardItem('${sc.id}', this)">
            📋 ${sc.title}
          </button>
        `).join('');
        const firstCard = ALL_CARDS.find(c => c.id === sortedSubCards[0].id) || sortedSubCards[0];
        if (firstCard) {
          document.getElementById('drawerTitle').textContent = firstCard.title;
          document.getElementById('drawerRelPath').textContent = firstCard.rel_path || '';
          document.getElementById('drawerRawLink').href = firstCard.rel_path || '#';
        }
        cardBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải nội dung…</p>';
        loadCardBody(firstCard, function (html) { cardBox.innerHTML = html; });
      } else if (pDocs.length > 1) {
        // ƯU TIÊN 2: Nếu không có thẻ con mà có nhiều văn bản tiến độ
        const sortedPDocs = pDocs.slice().sort((a, b) => a.title.localeCompare(b.title, undefined, { numeric: true, sensitivity: 'base' }));
        pSubNav.style.display = 'flex';
        pSubNav.innerHTML = sortedPDocs.map((pd, idx) => `
          <button class="drawer-subnav-btn ${idx === 0 ? 'active' : ''}" onclick="selectDrawerProgressDoc('${pd.id}', this)">
            📋 ${pd.title}
          </button>
        `).join('');
        cardBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải nội dung…</p>';
        const firstDoc = SYSTEM_DOCS.find(d => d.id === sortedPDocs[0].id) || sortedPDocs[0];
        loadDocBody(firstDoc, function (html) { cardBox.innerHTML = html; });
      } else {
        pSubNav.style.display = 'none';
        pSubNav.innerHTML = '';
        cardBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải nội dung…</p>';
        loadCardBody(card, function (html) { cardBox.innerHTML = html; });
      }

      // 3. Tab 2: SRS & Thiết kế kỹ thuật
      const sSubNav = document.getElementById('drawerSrsSubNav');
      const srsBox = document.getElementById('drawerSrsContent');
      if (sDocs.length > 0) {
        const sortedSDocs = sDocs.slice().sort((a, b) => {
          const rank = (str) => {
            const s = (str || '').toLowerCase();
            if (s.includes('srs') && !s.includes('thiet-ke') && !s.includes('doi-chieu') && !s.includes('happy') && !s.includes('testlink')) return 1;
            if (s.includes('thiet-ke')) return 2;
            if (s.includes('happy')) return 3;
            if (s.includes('testlink') || s.endsWith('.xml')) return 4;
            if (s.includes('man-hinh')) return 5;
            if (s.includes('so-do') || s.includes('quy-trinh')) return 6;
            if (s.includes('doi-chieu')) return 7;
            return 8;
          };
          const rA = rank(a.path || a.title);
          const rB = rank(b.path || b.title);
          if (rA !== rB) return rA - rB;
          return a.title.localeCompare(b.title, undefined, { numeric: true, sensitivity: 'base' });
        });
        sSubNav.style.display = 'flex';
        sSubNav.innerHTML = sortedSDocs.map((sd, idx) => {
          const isTestLink = (sd.badge === 'TestLink') || (sd.title && sd.title.toLowerCase().includes('testlink')) || (sd.path && sd.path.endsWith('.xml'));
          let icon = '📚';
          let label = sd.title;
          let extraStyle = '';
          if (isTestLink) {
            icon = '🧪';
            label = 'TestLink XML (20 Test Cases)';
            extraStyle = 'background: rgba(16, 185, 129, 0.15) !important; color: #10b981 !important; border: 1px solid rgba(16, 185, 129, 0.5) !important; font-weight: 700 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);';
          } else if (sd.title.toLowerCase().includes('happy cases') || sd.title.toLowerCase().includes('kịch bản kiểm thử')) {
            icon = '✅';
            label = 'Kịch bản Happy Cases (20 cases)';
          } else if (sd.title.toLowerCase().includes('thiết kế kỹ thuật')) {
            icon = '⚙️';
            label = 'Thiết kế kỹ thuật';
          } else if (sd.title.toLowerCase().includes('mô tả màn hình')) {
            icon = '🖥️';
            label = 'Mô tả 10 màn hình';
          } else if (sd.title.toLowerCase().includes('sơ đồ')) {
            icon = '📊';
            label = 'Đặc tả Sơ đồ & Kiến trúc';
          } else if (sd.title.toLowerCase().includes('srs')) {
            icon = '📑';
            label = 'SRS Đặc tả chức năng';
          }
          return `
            <button class="drawer-subnav-btn ${idx === 0 ? 'active' : ''}" style="${extraStyle}" onclick="selectDrawerSrsDoc('${sd.id}', this)" title="${sd.title}">
              ${icon} ${label}
            </button>
          `;
        }).join('');
        srsBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải tài liệu đặc tả…</p>';
        const firstDoc = SYSTEM_DOCS.find(d => d.id === sortedSDocs[0].id) || sortedSDocs[0];
        loadDocBody(firstDoc, function (html) { srsBox.innerHTML = html; });
      } else {
        sSubNav.style.display = 'none';
        sSubNav.innerHTML = '';
        srsBox.innerHTML = `
          <div style="text-align: center; padding: 48px 24px; color: var(--text-muted); background: rgba(15,23,42,0.4); border-radius: 8px; border: 1px dashed var(--border-subtle);">
            <div style="font-size: 32px; margin-bottom: 10px;">📚</div>
            <div style="font-weight: 700; color: #fff; margin-bottom: 6px;">Chưa có tài liệu SRS gắn riêng cho mã này</div>
            <div style="font-size: 13px;">Các yêu cầu kỹ thuật hiện được mô tả trực tiếp trong thẻ tiến độ.</div>
          </div>
        `;
      }

      // 4. Tab 3: Sơ đồ & Mockup
      const diagsBox = document.getElementById('drawerDiagramsGallery');
      if (diags.length > 0) {
        diagsBox.innerHTML = diags.map(dg => {
          const isDrawio = dg.is_drawio || (dg.filename && dg.filename.endsWith('.drawio'));
          const isHtml = dg.href && dg.href.endsWith('.html');
          const isImg = !isDrawio && !isHtml;
          const escapedName = (dg.name || '').replace(/'/g, "\\'");
          const imgUrl = dg.preview_img || (isImg ? dg.href : '');

          let thumbHtml = '';
          let clickHandler = '';
          let actionsHtml = '';

          if (isDrawio) {
            thumbHtml = `
              <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 110px; background: rgba(245, 158, 11, 0.08); border-radius: 6px;">
                <div style="font-size: 32px; margin-bottom: 4px;">📐</div>
                <span style="font-size: 11px; font-weight: 700; color: #f59e0b; text-transform: uppercase;">Draw.io Nguồn</span>
              </div>
            `;
            clickHandler = `window.location.href='${dg.href}'`;
            actionsHtml = `
              <a href="${dg.href}" download class="btn btn-ghost" style="flex: 1; padding: 4px 8px; font-size: 11px; color: #f59e0b; border-color: rgba(245, 158, 11, 0.4); text-align: center;">Tải Draw.io 📥</a>
            `;
          } else if (isHtml) {
            thumbHtml = imgUrl ? `
              <img src="${imgUrl}" alt="${escapedName}" class="diagram-thumb" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" />
              <div style="display: none; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 110px; background: rgba(56, 189, 248, 0.08); border-radius: 6px;">
                <div style="font-size: 32px; margin-bottom: 4px;">⚡</div>
                <span style="font-size: 11px; font-weight: 700; color: #38bdf8;">Sơ đồ tương tác</span>
              </div>
            ` : `
              <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 110px; background: rgba(56, 189, 248, 0.08); border-radius: 6px;">
                <div style="font-size: 32px; margin-bottom: 4px;">⚡</div>
                <span style="font-size: 11px; font-weight: 700; color: #38bdf8;">Sơ đồ tương tác</span>
              </div>
            `;
            clickHandler = `window.open('${dg.href}?present=true', '_blank')`;
            actionsHtml = `
              <a href="${dg.href}?present=true" target="_blank" class="btn btn-ghost" style="flex: 1; padding: 4px 8px; font-size: 11px; color: #38bdf8; border-color: rgba(56, 189, 248, 0.4); text-align: center;">Xem tương tác ⚡</a>
            `;
          } else {
            thumbHtml = `
              <img src="${imgUrl}" alt="${escapedName}" class="diagram-thumb" onerror="this.onerror=null;this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'200\\' height=\\'120\\'><text x=\\'50%\\' y=\\'50%\\' dominant-baseline=\\'middle\\' text-anchor=\\'middle\\' fill=\\'%2394a3b8\\' font-size=\\'12\\'>Sơ đồ</text></svg>';" />
            `;
            clickHandler = `openImageLightbox('${imgUrl}', '${escapedName}')`;
            actionsHtml = `
              <button onclick="event.stopPropagation(); openImageLightbox('${imgUrl}', '${escapedName}')" class="btn btn-ghost" style="flex: 1; font-size: 11px;">🔍 Phóng to</button>
              <a href="${dg.href}" target="_blank" class="btn btn-ghost" style="padding: 4px 8px; font-size: 11px;">Mở gốc ➔</a>
            `;
          }

          return `
            <div class="diagram-card" style="margin: 0;">
              <div class="diagram-thumb-wrap" onclick="${clickHandler}" style="cursor: pointer;" title="${isImg ? 'Nhấp để xem phóng to (Zoom & Pan)' : (isHtml ? 'Nhấp để mở sơ đồ tương tác' : 'Nhấp để tải file .drawio')}">
                ${thumbHtml}
              </div>
              <div class="diagram-info">
                <div>
                  <div class="diagram-title">${dg.name}</div>
                  <div class="diagram-meta">${dg.filename} • ${dg.size_kb} KB</div>
                </div>
                <div class="diagram-actions">
                  ${actionsHtml}
                </div>
              </div>
            </div>
          `;
        }).join('');
      } else {
        diagsBox.innerHTML = `
          <div style="grid-column: 1/-1; text-align: center; padding: 48px 24px; color: var(--text-muted); background: rgba(15,23,42,0.4); border-radius: 8px; border: 1px dashed var(--border-subtle);">
            <div style="font-size: 32px; margin-bottom: 10px;">📊</div>
            <div style="font-weight: 700; color: #fff; margin-bottom: 6px;">Chưa có sơ đồ hoặc mockup đính kèm</div>
            <div style="font-size: 13px;">Mọi sơ đồ sequence, kiến trúc hoặc ảnh giao diện thuộc task này sẽ hiển thị tại đây.</div>
          </div>
        `;
      }

      // 5. Tab 4: Mantis & Bug
      const mantisBox = document.getElementById('drawerMantisContent');
      if (bugs.length > 0) {
        mantisBox.innerHTML = `
          <div class="mantis-table-wrap">
            <table class="mantis-table">
              <thead>
                <tr>
                  <th style="width: 75px;">ID</th>
                  <th style="width: 120px;">TRẠNG THÁI</th>
                  <th style="width: 100px;">MỨC ĐỘ</th>
                  <th>TÓM TẮT BUG</th>
                  <th style="width: 110px;">GÁN CHO</th>
                </tr>
              </thead>
              <tbody>
                ${bugs.map(b => {
                  const bId = b.id || '';
                  const bStatus = b.status || 'open';
                  const bSev = b.severity || 'normal';
                  let statusColor = '#94a3b8';
                  if (['resolved', 'closed', 'đã giải quyết', 'đã đóng'].includes(bStatus.toLowerCase())) statusColor = '#10b981';
                  else if (['assigned', 'feedback', 'đang xử lý'].includes(bStatus.toLowerCase())) statusColor = '#3b82f6';
                  else if (['acknowledged', 'confirmed', 'tiếp nhận'].includes(bStatus.toLowerCase())) statusColor = '#f59e0b';
                  return `
                    <tr>
                      <td><span class="mantis-id-badge">#${bId}</span></td>
                      <td><span style="color: ${statusColor}; font-weight: 700; font-size: 12px;">● ${bStatus.toUpperCase()}</span></td>
                      <td><span style="font-size: 12px; color: ${bSev === 'block' || bSev === 'crash' ? '#ef4444' : 'var(--text-muted)'};">${bSev}</span></td>
                      <td><strong>${b.summary || ''}</strong></td>
                      <td><span style="font-size: 12px; color: #94a3b8;">${b.assigned_to || '—'}</span></td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        `;
      } else {
        mantisBox.innerHTML = `
          <div style="text-align: center; padding: 48px 24px; color: var(--text-muted); background: rgba(15,23,42,0.4); border-radius: 8px; border: 1px dashed var(--border-subtle);">
            <div style="font-size: 32px; margin-bottom: 10px;">🐞</div>
            <div style="font-weight: 700; color: #fff; margin-bottom: 6px;">Không có lỗi Mantis nào gắn với task này</div>
            <div style="font-size: 13px;">Dự án hiện không ghi nhận bug nào liên quan trực tiếp đến mã công việc này.</div>
          </div>
        `;
      }

      // Mặc định mở Tab 1
      switchDrawer360Tab('progress');

      document.getElementById('drawerOverlay').classList.add('open');
      document.getElementById('drawerPanel').classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function selectDrawerProgressDoc(docId, btn) {
      document.querySelectorAll('#drawerProgressSubNav .drawer-subnav-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      const doc = SYSTEM_DOCS.find(d => d.id === docId);
      const cardBox = document.getElementById('drawerMdContent');
      if (doc) {
        cardBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải nội dung…</p>';
        loadDocBody(doc, function (html) { cardBox.innerHTML = html; });
      }
    }

    function selectDrawerCardItem(cardId, btn) {
      document.querySelectorAll('#drawerProgressSubNav .drawer-subnav-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      const card = ALL_CARDS.find(c => c.id === cardId);
      const cardBox = document.getElementById('drawerMdContent');
      if (card) {
        document.getElementById('drawerTitle').textContent = card.title;
        document.getElementById('drawerRelPath').textContent = card.rel_path || '';
        document.getElementById('drawerRawLink').href = card.rel_path || '#';
        const sm = STATUS_META[card.status] || STATUS_META['todo'];
        const pill = document.getElementById('drawerStatusPill');
        pill.textContent = sm.icon + ' ' + sm.label;
        pill.style.background = sm.bg;
        pill.style.color = sm.color;
        pill.style.border = '1px solid ' + sm.border;

        cardBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải nội dung…</p>';
        loadCardBody(card, function (html) { cardBox.innerHTML = html; });
      }
    }

    function selectDrawerSrsDoc(docId, btn) {
      document.querySelectorAll('#drawerSrsSubNav .drawer-subnav-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      const doc = SYSTEM_DOCS.find(d => d.id === docId);
      const srsBox = document.getElementById('drawerSrsContent');
      if (doc) {
        srsBox.innerHTML = '<p style="color: var(--text-subtle);">Đang tải tài liệu đặc tả…</p>';
        loadDocBody(doc, function (html) { srsBox.innerHTML = html; });
      }
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
      if (!src) return;
      // Phòng vệ: Nếu vô tình mở file không phải ảnh (drawio, html, xml, json)
      if (src.endsWith('.drawio') || src.endsWith('.xml') || src.endsWith('.json')) {
        const a = document.createElement('a');
        a.href = src;
        a.download = '';
        a.click();
        return;
      }
      if (src.endsWith('.html')) {
        window.open(src + (src.includes('?') ? '&' : '?') + 'present=true', '_blank');
        return;
      }

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
        await reloadDashboardDataInPlace();
      } catch(e) {}
      if (btn) {
        btn.innerHTML = '🔄 Cập nhật';
        btn.disabled = false;
      }
    }

    /* ==========================================================================
       KNOWLEDGE GRAPH (VŨ TRỤ TRI THỨC 3D & DANH SÁCH THẺ)
       ========================================================================== */
    let currentKgViewMode = '3d'; // '3d' | 'cards'
    let kg3DGraphInstance = null;
    let selected3DNode = null;
    let is3DAutoRotating = true;

    function getNodeHexColor(kind) {
      switch ((kind || '').toLowerCase()) {
        case 'role': return '#38bdf8';
        case 'skill': return '#c084fc';
        case 'rule': return '#fb7185';
        case 'design': return '#34d399';
        case 'requirement': return '#fbbf24';
        case 'source': return '#2dd4bf';
        default: return '#818cf8';
      }
    }

    function getKindBadgeStyle(kind) {
      switch ((kind || '').toLowerCase()) {
        case 'role': return { bg: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8', border: 'rgba(56, 189, 248, 0.3)' };
        case 'skill': return { bg: 'rgba(168, 85, 247, 0.15)', color: '#c084fc', border: 'rgba(168, 85, 247, 0.3)' };
        case 'rule': return { bg: 'rgba(244, 63, 94, 0.15)', color: '#fb7185', border: 'rgba(244, 63, 94, 0.3)' };
        case 'design': return { bg: 'rgba(16, 185, 129, 0.15)', color: '#34d399', border: 'rgba(16, 185, 129, 0.3)' };
        case 'requirement': return { bg: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24', border: 'rgba(245, 158, 11, 0.3)' };
        case 'source': return { bg: 'rgba(20, 184, 166, 0.15)', color: '#2dd4bf', border: 'rgba(20, 184, 166, 0.3)' };
        default: return { bg: 'rgba(99, 102, 241, 0.15)', color: '#818cf8', border: 'rgba(99, 102, 241, 0.3)' };
      }
    }

    function setKnowledgeViewMode(mode) {
      currentKgViewMode = mode;
      const btn3D = document.getElementById('btnKgView3D');
      const btnCards = document.getElementById('btnKgViewCards');
      const wrap3D = document.getElementById('kg3DWrapper');
      const gridCards = document.getElementById('kgGrid');

      if (btn3D) btn3D.classList.toggle('active', mode === '3d');
      if (btnCards) btnCards.classList.toggle('active', mode === 'cards');
      if (wrap3D) wrap3D.style.display = mode === '3d' ? 'block' : 'none';
      if (gridCards) gridCards.style.display = mode === 'cards' ? 'grid' : 'none';

      if (mode === '3d') {
        setTimeout(initOrUpdate3DGraph, 60);
      } else {
        renderKnowledgeCards();
      }
    }

    function renderKgKindChips() {
      const container = document.getElementById('kgKindChips');
      if (!container) return;

      const nodes = CURRENT_KNOWLEDGE.nodes || [];
      const cats = {};
      nodes.forEach(n => {
        const k = n.kind || 'Other';
        cats[k] = (cats[k] || 0) + 1;
      });

      let html = `<button class="chip-btn ${currentKgKindFilter === 'ALL' ? 'active' : ''}" data-kind="ALL" onclick="setKnowledgeKindFilter('ALL', this)">Tất cả (${nodes.length})</button>`;
      
      const kindOrder = ['Role', 'Skill', 'Rule', 'Design', 'Requirement', 'Source'];
      kindOrder.forEach(k => {
        if (cats[k]) {
          html += `<button class="chip-btn ${currentKgKindFilter === k ? 'active' : ''}" data-kind="${k}" onclick="setKnowledgeKindFilter('${k}', this)">${k} (${cats[k]})</button>`;
        }
      });
      Object.keys(cats).forEach(k => {
        if (!kindOrder.includes(k)) {
          html += `<button class="chip-btn ${currentKgKindFilter === k ? 'active' : ''}" data-kind="${k}" onclick="setKnowledgeKindFilter('${k}', this)">${k} (${cats[k]})</button>`;
        }
      });

      container.innerHTML = html;
    }

    function setKnowledgeKindFilter(kind, elem) {
      currentKgKindFilter = kind;
      if (elem && elem.parentElement) {
        elem.parentElement.querySelectorAll('.chip-btn').forEach(btn => btn.classList.remove('active'));
        elem.classList.add('active');
      }
      renderKnowledgeGraph();
    }

    function filterKnowledgeGraph() {
      renderKnowledgeGraph();
    }

    function filterByKnowledgeTarget(targetId) {
      const input = document.getElementById('kgSearchInput');
      if (input) {
        input.value = targetId;
        currentKgKindFilter = 'ALL';
        renderKgKindChips();
        renderKnowledgeGraph();
      }
    }

    function copyNodeId(id, btn) {
      navigator.clipboard.writeText(id).then(() => {
        const orig = btn.innerHTML;
        btn.innerHTML = '✓ Đã chép';
        btn.style.color = '#34d399';
        setTimeout(() => {
          btn.innerHTML = orig;
          btn.style.color = '';
        }, 1500);
      });
    }

    function prepareGraphData() {
      const rawNodes = CURRENT_KNOWLEDGE.nodes || [];
      const nodeMap = new Map();
      const query = (document.getElementById('kgSearchInput')?.value || '').toLowerCase().trim();

      const nodes = rawNodes.map(n => {
        const relCount = (n.relations || []).length;
        const color = getNodeHexColor(n.kind);
        
        let match = true;
        if (currentKgKindFilter !== 'ALL' && n.kind !== currentKgKindFilter) {
          match = false;
        }
        if (query) {
          const matchId = (n.id || '').toLowerCase().includes(query);
          const matchTitle = (n.title || '').toLowerCase().includes(query);
          const matchRef = (n.content_ref || '').toLowerCase().includes(query);
          const matchOwner = (n.owner_role || '').toLowerCase().includes(query);
          const matchRel = (n.relations || []).some(r => (r.target || '').toLowerCase().includes(query) || (r.type || '').toLowerCase().includes(query));
          if (!matchId && !matchTitle && !matchRef && !matchOwner && !matchRel) {
            match = false;
          }
        }

        const nodeObj = {
          id: n.id,
          name: n.title || n.id,
          title: n.title || n.id,
          kind: n.kind,
          owner_role: n.owner_role,
          content_ref: n.content_ref,
          version: n.version,
          state: n.state,
          relations: n.relations || [],
          relations_count: relCount,
          val: Math.max(3.5, Math.min(22, 3.5 + relCount * 1.6)),
          color: match ? color : 'rgba(51, 65, 85, 0.2)',
          isDimmed: !match
        };
        nodeMap.set(n.id, nodeObj);
        return nodeObj;
      });

      const links = [];
      const linkSet = new Set();
      rawNodes.forEach(n => {
        (n.relations || []).forEach(r => {
          if (r.target && nodeMap.has(r.target)) {
            const key = n.id < r.target ? `${n.id}---${r.target}` : `${r.target}---${n.id}`;
            if (!linkSet.has(key)) {
              linkSet.add(key);
              const sourceNode = nodeMap.get(n.id);
              const targetNode = nodeMap.get(r.target);
              const isLinkActive = (!sourceNode.isDimmed && !targetNode.isDimmed);
              links.push({
                source: n.id,
                target: r.target,
                type: r.type || 'related_to',
                color: isLinkActive ? 'rgba(56, 189, 248, 0.4)' : 'rgba(30, 41, 59, 0.1)',
                particles: isLinkActive ? 2 : 0
              });
            }
          }
        });
      });

      return { nodes, links };
    }

    function initOrUpdate3DGraph() {
      const container = document.getElementById('kg3dContainer');
      if (!container || typeof ForceGraph3D === 'undefined') return;

      const gData = prepareGraphData();

      if (kg3DGraphInstance) {
        kg3DGraphInstance.graphData(gData);
        return;
      }

      // Khởi tạo 3D Force-Directed Graph với Three.js
      kg3DGraphInstance = ForceGraph3D({ controlType: 'orbit' })(container)
        .graphData(gData)
        .backgroundColor('rgba(0,0,0,0)')
        .showNavInfo(false)
        .enableNodeDrag(true)
        .nodeId('id')
        .nodeLabel(node => `
          <div style="background: rgba(15,23,42,0.95); border: 1px solid rgba(56,189,248,0.5); border-radius: 8px; padding: 8px 12px; font-family: sans-serif; box-shadow: 0 4px 25px rgba(0,0,0,0.7); pointer-events: none;">
            <div style="font-weight: 700; color: #fff; font-size: 13px; margin-bottom: 2px;">${node.title}</div>
            <div style="color: #94a3b8; font-size: 11px;">[${node.kind}] ID: <code style="color: #818cf8;">${node.id}</code></div>
            <div style="color: #38bdf8; font-size: 11px; margin-top: 3px;">🔗 ${node.relations_count} liên kết kiến trúc • Kéo để di chuyển</div>
          </div>
        `)
        .nodeColor(node => node.color)
        .nodeVal(node => node.val)
        .nodeResolution(24)
        .nodeOpacity(0.94)
        .linkColor(link => link.color)
        .linkWidth(link => link.particles > 0 ? 1.4 : 0.8)
        .linkDirectionalParticles(link => link.particles)
        .linkDirectionalParticleWidth(2.5)
        .linkDirectionalParticleSpeed(0.005)
        .linkDirectionalParticleColor(() => '#38bdf8')
        .onNodeHover(node => {
          container.style.cursor = node ? 'grab' : null;
          // Tạm dừng tự xoay khi rê vào node để người dùng dễ dàng bấm và nắm kéo
          if (kg3DGraphInstance && kg3DGraphInstance.controls()) {
            kg3DGraphInstance.controls().autoRotate = (node || !is3DAutoRotating) ? false : true;
          }
        })
        .onNodeDrag((node, translate) => {
          container.style.cursor = 'grabbing';
          if (kg3DGraphInstance && kg3DGraphInstance.controls()) {
            kg3DGraphInstance.controls().autoRotate = false;
          }
        })
        .onNodeDragEnd(node => {
          container.style.cursor = 'grab';
          // Khóa cố định vị trí node sau khi người dùng kéo thả
          node.fx = node.x;
          node.fy = node.y;
          node.fz = node.z;
          if (kg3DGraphInstance && kg3DGraphInstance.controls() && is3DAutoRotating) {
            kg3DGraphInstance.controls().autoRotate = true;
          }
        })
        .onNodeRightClick(node => {
          // Bấm chuột phải lên node để giải phóng ghim vị trí (unpin)
          delete node.fx;
          delete node.fy;
          delete node.fz;
          if (kg3DGraphInstance) kg3DGraphInstance.d3ReheatSimulation();
          showRealtimeToast('Đã nhả ghim tự do cho node: ' + node.id);
        })
        .onNodeClick(node => {
          selected3DNode = node;
          show3dNodeCard(node);
          
          // Hiệu ứng Fly-To camera bay tới áp sát quả cầu tri thức
          const distance = 90;
          const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);
          kg3DGraphInstance.cameraPosition(
            { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
            node,
            1200
          );
        })
        .onBackgroundClick(() => {
          const card = document.getElementById('kg3dNodeCard');
          if (card) card.style.display = 'none';
        });

      // Cấu hình lực đẩy dãn rộng không gian để nhìn rõ vào bên trong lòng cụm
      if (kg3DGraphInstance.d3Force('charge')) {
        kg3DGraphInstance.d3Force('charge').strength(-320);
      }
      if (kg3DGraphInstance.d3Force('link')) {
        kg3DGraphInstance.d3Force('link').distance(65);
      }
      kg3DGraphInstance.d3VelocityDecay(0.25);

      // Bật chế độ tự động xoay thiên hà quanh trục
      if (kg3DGraphInstance.controls()) {
        kg3DGraphInstance.controls().autoRotate = is3DAutoRotating;
        kg3DGraphInstance.controls().autoRotateSpeed = 0.6;
      }

      setup3DKeyboardNavigation();
    }

    function setup3DKeyboardNavigation() {
      if (window.__kgKeyNavSetup) return;
      window.__kgKeyNavSetup = true;
      window.addEventListener('keydown', (e) => {
        if (currentKgViewMode !== '3d' || !kg3DGraphInstance) return;
        if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

        const pos = kg3DGraphInstance.cameraPosition();
        const step = 25;
        let moved = false;

        if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') {
          const dist = Math.hypot(pos.x, pos.y, pos.z);
          if (dist > 35) {
            const factor = Math.max(0.2, (dist - step) / dist);
            kg3DGraphInstance.cameraPosition({ x: pos.x * factor, y: pos.y * factor, z: pos.z * factor }, null, 150);
            moved = true;
          }
        } else if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') {
          const dist = Math.hypot(pos.x, pos.y, pos.z);
          const factor = (dist + step) / dist;
          kg3DGraphInstance.cameraPosition({ x: pos.x * factor, y: pos.y * factor, z: pos.z * factor }, null, 150);
          moved = true;
        }

        if (moved) e.preventDefault();
      });
    }

    function kg3DDiveInside() {
      if (!kg3DGraphInstance) return;
      kg3DGraphInstance.cameraPosition(
        { x: 0, y: 0, z: 25 },
        { x: 0, y: 0, z: -80 },
        1400
      );
      showRealtimeToast('🚀 Đã bay vào lòng thiên hà! Dùng chuột trái để ngắm 360° từ bên trong.');
    }

    let isKgSpread = true;
    function kg3DToggleSpread() {
      if (!kg3DGraphInstance) return;
      isKgSpread = !isKgSpread;
      const charge = isKgSpread ? -320 : -130;
      const dist = isKgSpread ? 65 : 35;
      if (kg3DGraphInstance.d3Force('charge')) kg3DGraphInstance.d3Force('charge').strength(charge);
      if (kg3DGraphInstance.d3Force('link')) kg3DGraphInstance.d3Force('link').distance(dist);
      kg3DGraphInstance.d3ReheatSimulation();
      const btn = document.getElementById('btnKg3DSpread');
      if (btn) {
        btn.innerHTML = isKgSpread ? '🌌 Cụm: DÃN RỘNG' : '📦 Cụm: THU GỌN';
      }
      showRealtimeToast(isKgSpread ? '🌌 Đã dãn rộng cụm để nhìn rõ bên trong!' : '📦 Đã thu gọn cụm.');
    }
    }

    function kg3DZoom(ratio) {
      if (!kg3DGraphInstance) return;
      const currentPos = kg3DGraphInstance.cameraPosition();
      kg3DGraphInstance.cameraPosition({
        x: currentPos.x * ratio,
        y: currentPos.y * ratio,
        z: currentPos.z * ratio
      }, null, 600);
    }

    function kg3DResetCamera() {
      if (!kg3DGraphInstance) return;
      kg3DGraphInstance.zoomToFit(1000, 50);
    }

    function kg3DToggleRotate() {
      if (!kg3DGraphInstance || !kg3DGraphInstance.controls()) return;
      is3DAutoRotating = !is3DAutoRotating;
      kg3DGraphInstance.controls().autoRotate = is3DAutoRotating;
      const btn = document.getElementById('btnKg3DAutoRotate');
      if (btn) {
        btn.innerHTML = is3DAutoRotating ? '🔄 Tự Xoay: BẬT' : '⏸️ Tự Xoay: TẮT';
      }
    }

    function show3dNodeCard(node) {
      const card = document.getElementById('kg3dNodeCard');
      if (!card) return;
      
      const style = getKindBadgeStyle(node.kind);
      const pill = document.getElementById('kg3dCardKind');
      if (pill) {
        pill.textContent = node.kind;
        pill.style.background = style.bg;
        pill.style.color = style.color;
        pill.style.border = '1px solid ' + style.border;
      }

      document.getElementById('kg3dCardId').textContent = node.id;
      document.getElementById('kg3dCardTitle').textContent = node.title;
      
      const refElem = document.getElementById('kg3dCardRef');
      if (refElem) {
        refElem.innerHTML = node.content_ref ? `📄 <code>${node.content_ref}</code>` : '';
      }

      const relsElem = document.getElementById('kg3dCardRelations');
      if (relsElem) {
        const rels = node.relations || [];
        if (rels.length === 0) {
          relsElem.innerHTML = '<span style="font-size: 11px; color: var(--text-subtle);">Không có liên kết quan hệ trực tiếp.</span>';
        } else {
          relsElem.innerHTML = `
            <div style="font-size: 10px; color: var(--text-subtle); margin-bottom: 4px; font-weight: 600; text-transform: uppercase;">
              Liên kết quan hệ (${rels.length}):
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
              ${rels.map(r => `
                <span onclick="focus3dNode('${r.target}')" style="font-size: 10px; cursor: pointer; background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px; color: #93c5fd; border: 1px solid rgba(255,255,255,0.08);" title="${r.type}: Click để bay tới node này">
                  🔗 ${r.target}
                </span>
              `).join('')}
            </div>
          `;
        }
      }

      card.style.display = 'block';
    }

    function focus3dNode(targetId) {
      if (!kg3DGraphInstance) return;
      const gData = kg3DGraphInstance.graphData();
      const target = (gData.nodes || []).find(n => n.id === targetId);
      if (target) {
        selected3DNode = target;
        show3dNodeCard(target);
        const distance = 90;
        const distRatio = 1 + distance / Math.hypot(target.x, target.y, target.z);
        kg3DGraphInstance.cameraPosition(
          { x: target.x * distRatio, y: target.y * distRatio, z: target.z * distRatio },
          target,
          1200
        );
      }
    }

    function readDocFrom3dCard() {
      if (!selected3DNode) return;
      const ref = selected3DNode.content_ref;
      if (!ref) {
        alert('Node này chưa có file tài liệu tham chiếu.');
        return;
      }
      const doc = SYSTEM_DOCS.find(d => (d.path && (d.path.includes(ref) || ref.includes(d.path))));
      if (doc) {
        openDocDrawer(doc.id);
      } else {
        const virtualDoc = {
          id: selected3DNode.id,
          title: selected3DNode.title,
          badge: selected3DNode.kind,
          category: 'Tri thức: ' + selected3DNode.kind,
          path: ref,
          href: ref,
          is_diagram: false
        };
        openDocDrawerDirect(virtualDoc);
      }
    }

    function copy3dNodeId() {
      if (!selected3DNode) return;
      navigator.clipboard.writeText(selected3DNode.id).then(() => {
        showRealtimeToast('✓ Đã sao chép ID: ' + selected3DNode.id);
      });
    }

    function openDocDrawerDirect(doc) {
      document.getElementById('drawerTaskId').textContent = doc.badge;
      document.getElementById('drawerTitle').textContent = doc.title;
      
      const pill = document.getElementById('drawerStatusPill');
      pill.textContent = '📚 ' + doc.category;
      pill.style.background = 'rgba(99, 102, 241, 0.15)';
      pill.style.color = '#818cf8';
      pill.style.border = '1px solid rgba(99, 102, 241, 0.3)';

      document.getElementById('drawerEpicBadge').textContent = 'Chuyên mục: ' + doc.category;
      document.getElementById('drawerPhaseBadge').textContent = 'Tri thức Knowledge Graph';
      document.getElementById('drawerOwnerBadge').textContent = 'Living Docs';

      document.getElementById('drawerBranch').textContent = doc.category;
      document.getElementById('drawerRelPath').textContent = doc.path;
      document.getElementById('drawerRawLink').href = doc.href || doc.path;
      document.getElementById('drawerRawLink').style.display = 'inline-flex';

      document.getElementById('drawerScopeWrap').style.display = 'none';
      document.getElementById('drawerBlockedWrap').style.display = 'none';

      document.getElementById('drawerBodyTitle').textContent = '📄 NỘI DUNG TÀI LIỆU KỸ THUẬT';
      const mdBox = document.getElementById('drawerMdContent');
      mdBox.innerHTML = '<p style="color: var(--text-subtle);">Đang nạp tài liệu từ máy chủ…</p>';
      
      fetch('/' + doc.path + '?t=' + Date.now())
        .then(res => res.ok ? res.text() : Promise.reject('Không thể đọc file: ' + doc.path))
        .then(text => {
          const escaped = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
          mdBox.innerHTML = `<pre style="white-space: pre-wrap; font-family: var(--font-mono); font-size: 13px; line-height: 1.6; color: #cbd5e1; background: var(--bg-card); padding: 18px; border-radius: 8px;">${escaped}</pre>`;
        })
        .catch(err => {
          mdBox.innerHTML = `<p style="color: #f87171;">${err}</p>`;
        });

      document.getElementById('drawerOverlay').classList.add('open');
      document.getElementById('drawerPanel').classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function renderKnowledgeCards() {
      const container = document.getElementById('kgGrid');
      if (!container) return;

      const nodes = CURRENT_KNOWLEDGE.nodes || [];
      const query = (document.getElementById('kgSearchInput') ? document.getElementById('kgSearchInput').value : '').toLowerCase().trim();

      const filtered = nodes.filter(n => {
        if (currentKgKindFilter !== 'ALL' && n.kind !== currentKgKindFilter) return false;
        if (query) {
          const matchId = (n.id || '').toLowerCase().includes(query);
          const matchTitle = (n.title || '').toLowerCase().includes(query);
          const matchRef = (n.content_ref || '').toLowerCase().includes(query);
          const matchOwner = (n.owner_role || '').toLowerCase().includes(query);
          const matchRel = (n.relations || []).some(r => (r.target || '').toLowerCase().includes(query) || (r.type || '').toLowerCase().includes(query));
          if (!matchId && !matchTitle && !matchRef && !matchOwner && !matchRel) return false;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `
          <div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-muted); background: var(--bg-surface); border: 1px dashed var(--border-subtle); border-radius: var(--radius-md);">
            <div style="font-size: 32px; margin-bottom: 8px;">🔍</div>
            <div>Không tìm thấy node tri thức nào khớp với bộ lọc hoặc từ khóa "${query}".</div>
          </div>
        `;
        return;
      }

      container.innerHTML = filtered.map(n => {
        const style = getKindBadgeStyle(n.kind);
        const rels = n.relations || [];
        const relationsHtml = rels.length > 0 ? `
          <div style="margin-top: 10px;">
            <div style="font-size: 10px; color: var(--text-subtle); margin-bottom: 5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
              Kết nối quan hệ (${rels.length}):
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
              ${rels.slice(0, 6).map(r => `
                <span onclick="filterByKnowledgeTarget('${r.target}')" style="font-size: 10px; cursor: pointer; background: rgba(255,255,255,0.05); padding: 2px 7px; border-radius: 4px; color: #93c5fd; border: 1px solid rgba(255,255,255,0.08); transition: all 0.2s;" onmouseover="this.style.background='rgba(59,130,246,0.2)'; this.style.borderColor='#3b82f6';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.borderColor='rgba(255,255,255,0.08)';" title="${r.type}: Click để tìm kiếm node này">
                  🔗 ${r.target.length > 28 ? r.target.substring(0, 26) + '…' : r.target}
                </span>
              `).join('')}
              ${rels.length > 6 ? `<span style="font-size: 10px; color: var(--text-subtle); align-self: center;">+${rels.length - 6} nữa</span>` : ''}
            </div>
          </div>
        ` : '';

        return `
          <div class="doc-card" style="display: flex; flex-direction: column; justify-content: space-between; padding: 16px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); transition: transform 0.2s, border-color 0.2s;">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span class="status-pill" style="background: ${style.bg}; color: ${style.color}; border: 1px solid ${style.border}; font-weight: 700; text-transform: uppercase;">
                  ${n.kind}
                </span>
                <span style="font-size: 11px; color: var(--text-subtle);">Owner: <strong style="color: #cbd5e1;">${n.owner_role || 'system'}</strong></span>
              </div>
              <div style="font-size: 11px; font-family: var(--font-mono); color: #818cf8; margin-bottom: 6px; word-break: break-all;">
                ${n.id}
              </div>
              <h3 style="font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 6px; line-height: 1.4;">${n.title || n.id}</h3>
              ${n.content_ref ? `
                <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 8px; word-break: break-all;">
                  📄 <code style="font-size: 10px; color: #94a3b8; background: rgba(0,0,0,0.3); padding: 2px 4px; border-radius: 3px;">${n.content_ref}</code>
                </div>
              ` : ''}
              ${relationsHtml}
            </div>
            <div style="border-top: 1px solid var(--border-subtle); padding-top: 10px; margin-top: 12px; display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 11px; color: var(--text-subtle);">v${n.version || 1} • <span style="text-transform: capitalize;">${n.state || 'active'}</span></span>
              <button class="btn btn-ghost" style="padding: 3px 8px; font-size: 11px;" onclick="copyNodeId('${n.id}', this)" title="Sao chép Node ID">
                📋 Copy
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderKnowledgeGraph() {
      renderKgKindChips();
      if (currentKgViewMode === '3d') {
        initOrUpdate3DGraph();
      } else {
        renderKnowledgeCards();
      }
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

    async function reloadDashboardDataInPlace() {
      try {
        const res = await fetch('/data.js?t=' + Date.now());
        if (!res.ok) return;
        const text = await res.text();
        const jsonMatch = text.match(/window\.DASH\s*=\s*(\{[\s\S]*\});?\s*$/);
        if (!jsonMatch) return;
        const newDash = JSON.parse(jsonMatch[1]);
        window.DASH = newDash;

        if (newDash.multiProjects) {
          Object.assign(MULTI_PROJECTS, newDash.multiProjects);
        }

        if (CURRENT_PROJECT_ID && newDash.multiProjects && newDash.multiProjects[CURRENT_PROJECT_ID]) {
          const p = newDash.multiProjects[CURRENT_PROJECT_ID];
          SYSTEM_DOCS = p.docs || [];
          ALL_CARDS = (p.cards && p.cards.length > 0) ? p.cards : (newDash.cards || []);
          GROUPED_CARDS = (p.grouped_cards && p.grouped_cards.length > 0) ? p.grouped_cards : (newDash.groupedCards || []);
          EPIC_META = p.epics || newDash.epicMeta || {};
          CURRENT_MANTIS = p.mantis || { total: 0, bugs: [] };
          CURRENT_DIAGRAMS = p.diagrams || [];
          updateProjectHeader(p);
        } else {
          SYSTEM_DOCS = newDash.docs || [];
          ALL_CARDS = newDash.cards || [];
          GROUPED_CARDS = newDash.groupedCards || [];
          EPIC_META = newDash.epicMeta || {};
          CURRENT_MANTIS = newDash.mantis || { total: 0, bugs: [] };
          CURRENT_DIAGRAMS = newDash.diagrams || [];
        }
        CURRENT_KNOWLEDGE = newDash.knowledgeGraph || { nodes_count: 0, nodes: [], categories: {} };

        // Cập nhật ngầm lại toàn bộ DOM (không reload, không chớp trang)
        updateKPIAndBadges();
        renderEpicOptions();
        renderDocCategoryChips();
        renderCards();
        renderDocs();
        renderCodeTasks();
        renderGates();
        renderMantisBugs();
        renderDiagrams();
        renderKnowledgeGraph();

        // Nếu người dùng đang mở Drawer tài liệu, cập nhật ngầm ngay nội dung mới
        const openDocId = sessionStorage.getItem('dash_open_doc');
        const drawerPanel = document.getElementById('drawerPanel');
        if (openDocId && drawerPanel && drawerPanel.classList.contains('open')) {
          const doc = SYSTEM_DOCS.find(d => d.id === openDocId);
          if (doc) {
            doc.html_body = undefined;
            loadDocBody(doc, html => {
              const bodyElem = document.getElementById('drawerDocBody');
              if (bodyElem) bodyElem.innerHTML = html;
            });
          }
        }

        // Tương tự cho task card đang mở
        const openCardId = sessionStorage.getItem('dash_open_card');
        if (openCardId && drawerPanel && drawerPanel.classList.contains('open')) {
          const card = ALL_CARDS.find(c => c.id === openCardId);
          if (card) {
            card.html_body = undefined;
            loadCardBody(card, html => {
              const bodyElem = document.getElementById('drawerTaskBody');
              if (bodyElem) bodyElem.innerHTML = html;
            });
          }
        }

        showRealtimeToast('Đã tự động cập nhật ngầm dữ liệu mới nhất (không gián đoạn trang)!');
      } catch (e) {
        console.warn('Lỗi cập nhật ngầm:', e);
      }
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
            await reloadDashboardDataInPlace();
          }
        }
      } catch(e) {}
      isCheckingVersion = false;
    }

    // Tự động kiểm tra thay đổi mỗi 2 giây
    setInterval(checkRealtimeUpdate, 2000);

    window.onload = init;
  
