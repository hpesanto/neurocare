// Copy of pacientes.js adapted for usuarios
(function () {
    function qs(sel, root = document) { return root.querySelector(sel); }
    function qsa(sel, root = document) { return Array.from(root.querySelectorAll(sel)); }

    // Mark buttons handled by this page so the global modal handler (modal_ajax.js)
    // does not also process the same click and inject a second modal.
    try {
        qsa('#btnNew, .btn-edit, .btn-view').forEach(el => {
            try { el._spAttached = true; } catch (e) { }
            try { if (el.dataset) el.dataset.pageHandled = 'true'; } catch (e) { }
        });
    } catch (e) { /* ignore */ }
    function getCookie(name) {
        const v = document.cookie.split(';').map(c => c.trim()).find(c => c.startsWith(name + '='));
        if (!v) return null; return decodeURIComponent(v.split('=')[1]);
    }

    function showModal(html) {
        const modal = qs('#usuarioModal');
        qs('#modalContent').innerHTML = html;
        modal.style.display = 'block';
        bindForm();
        // if modal was opened in view-only mode, disable inputs and hide submit
        if (modal.dataset && modal.dataset.mode === 'view') {
            const form = qs('#modalContent form');
            if (form) {
                form.querySelectorAll('input,select,textarea').forEach(n => { try { n.setAttribute('disabled', 'disabled'); } catch (e) { } });
                form.querySelectorAll('button, input[type=submit]').forEach(n => {
                    try {
                        if (n.tagName.toLowerCase() === 'button') {
                            if ((n.type || '').toLowerCase() === 'submit') { n.style.display = 'none'; n.setAttribute('disabled', 'disabled'); }
                        } else { n.style.display = 'none'; n.setAttribute('disabled', 'disabled'); }
                    } catch (e) { }
                });
            }
        }
        const cancel = qs('#btnCancel');
        if (cancel) cancel.addEventListener('click', hideModal);
        qs('#modalOverlay').addEventListener('click', hideModal);
        setTimeout(() => {
            const first = qs('#modalContent form input, #modalContent form select, #modalContent form textarea');
            if (first) first.focus();
        }, 50);
    }

    function hideModal() {
        const modal = qs('#usuarioModal');
        modal.style.display = 'none';
        qs('#modalContent').innerHTML = '';
    }

    function loadForm(url) {
        const modal = qs('#usuarioModal');
        qs('#modalContent').innerHTML = qs('#modalSpinner').outerHTML || '';
        modal.style.display = 'block';
        fetch(url, { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.text())
            .then(html => showModal(html))
            .catch(err => { console.error('Erro ao carregar form', err); hideModal(); });
    }

    function bindForm() {
        const form = qs('#modalContent form');
        if (!form) return;
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const url = form.getAttribute('action') || window.location.href;
            const data = new FormData(form);
            fetch(url, {
                method: 'POST',
                body: data,
                credentials: 'same-origin',
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') }
            }).then(r => {
                const ct = r.headers.get('content-type') || '';
                if (ct.includes('application/json')) return r.json();
                return r.text();
            }).then(resp => {
                if (typeof resp === 'object') {
                    if (resp.ok) {
                        if (resp.row_html) {
                            const tmp = document.createElement('tbody');
                            tmp.innerHTML = resp.row_html;
                            const newRow = tmp.firstElementChild;
                            const existing = qs('#usuario-row-' + resp.id);
                            if (existing) existing.replaceWith(newRow);
                            else qs('#usersTable tbody').appendChild(newRow);
                        } else {
                            window.location.reload();
                        }
                        hideModal();
                    } else {
                        if (resp.form_html) qs('#modalContent').innerHTML = resp.form_html;
                        else if (resp.errors) qs('#modalContent').innerHTML = JSON.stringify(resp.errors);
                        bindForm();
                    }
                } else {
                    qs('#modalContent').innerHTML = resp;
                    bindForm();
                }
            }).catch(err => { console.error(err); });
        });
    }

    document.addEventListener('click', function (e) {
        const btn = e.target.closest('#btnNew, .btn-edit, .btn-view');
        if (!btn) return;
        e.preventDefault();
        const url = btn.dataset && btn.dataset.url;
        if (!url) return;
        const mode = btn.dataset && btn.dataset.mode;
        const modal = qs('#usuarioModal');
        if (mode) modal.dataset.mode = mode; else delete modal.dataset.mode;
        loadForm(url);
    });

    const viewTable = qs('#viewTable');
    const viewCards = qs('#viewCards');
    const search = qs('#usersSearch');
    const listContainer = qs('.list-container');
    const cardsContainer = qs('.cards-container');
    let tbodyListenerAdded = false;
    const tbody = qs('#usersTable tbody');

    function showTable() { listContainer.style.display = ''; cardsContainer.style.display = 'none'; }
    function showCards() { listContainer.style.display = 'none'; cardsContainer.style.display = 'flex'; cardsContainer.style.flexWrap = 'wrap'; }

    if (viewTable) viewTable.addEventListener('click', showTable);
    if (viewCards) viewCards.addEventListener('click', showCards);

    if (search) search.addEventListener('input', function (e) {
        const q = (e.target.value || '').toLowerCase();
        document.querySelectorAll('#usersTable tbody tr[id^="usuario-row-"]').forEach(r => {
            const name = (r.querySelector('td') || {}).textContent || '';
            r.style.display = name.toLowerCase().includes(q) ? '' : 'none';
        });
        document.querySelectorAll('.usuario-card').forEach(c => {
            const name = (c.querySelector('h4') || {}).textContent || '';
            c.style.display = name.toLowerCase().includes(q) ? 'inline-block' : 'none';
        });
    });

    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { const modal = qs('#usuarioModal'); if (modal && modal.style.display === 'block') hideModal(); } });

})();
