// Minimal JS to open modal, load form via fetch, submit via AJAX and update table row
(function () {
    console.log('pacientes.js loaded');
    function qs(sel, root = document) { return root.querySelector(sel); }
    function qsa(sel, root = document) { return Array.from(root.querySelectorAll(sel)); }

    function getCookie(name) {
        const v = document.cookie.split(';').map(c => c.trim()).find(c => c.startsWith(name + '='));
        if (!v) return null; return decodeURIComponent(v.split('=')[1]);
    }

    function showModal(html) {
        const modal = qs('#pacienteModal');
        qs('#modalContent').innerHTML = html;
        modal.style.display = 'block';
        bindForm();
        // if modal was opened in view-only mode, disable inputs and hide submit
        if (modal.dataset && modal.dataset.mode === 'view') {
            const nodes = qs('#modalContent').querySelectorAll('input,select,textarea,button');
            nodes.forEach(n => {
                if (n.tagName.toLowerCase() === 'button' && n.type !== 'submit') return; // leave action buttons
                try { n.setAttribute('disabled', 'disabled'); } catch (e) { }
            });
            const submit = qs('#modalContent form button[type=submit]');
            if (submit) submit.style.display = 'none';
        }
        // cancel button
        const cancel = qs('#btnCancel');
        if (cancel) cancel.addEventListener('click', hideModal);
        qs('#modalOverlay').addEventListener('click', hideModal);
        // focus first input
        setTimeout(() => {
            const first = qs('#modalContent form input, #modalContent form select, #modalContent form textarea');
            if (first) first.focus();
        }, 50);
    }

    function hideModal() {
        const modal = qs('#pacienteModal');
        modal.style.display = 'none';
        qs('#modalContent').innerHTML = '';
    }

    function loadForm(url) {
        // show spinner
        const modal = qs('#pacienteModal');
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
                    // expect {ok: true, row_html: ..., id: ...} or {ok: false, form_html: ...}
                    if (resp.ok) {
                        if (resp.row_html) {
                            const tmp = document.createElement('tbody');
                            tmp.innerHTML = resp.row_html;
                            const newRow = tmp.firstElementChild;
                            const existing = qs('#paciente-row-' + resp.id);
                            if (existing) existing.replaceWith(newRow);
                            else qs('#patientsTable tbody').appendChild(newRow);
                        } else {
                            // fallback: reload page
                            window.location.reload();
                        }
                        hideModal();
                    } else {
                        // render form errors
                        if (resp.form_html) qs('#modalContent').innerHTML = resp.form_html;
                        else if (resp.errors) qs('#modalContent').innerHTML = JSON.stringify(resp.errors);
                        bindForm();
                    }
                } else {
                    // server returned HTML (possibly the form partial)
                    qs('#modalContent').innerHTML = resp;
                    bindForm();
                }
            }).catch(err => { console.error(err); });
        });
    }

    // clicks for open/create/edit/view
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('#btnNew, .btn-edit, .btn-view');
        if (!btn) return;
        e.preventDefault();
        console.log('pacientes: click on', btn);
        const url = btn.dataset && btn.dataset.url;
        if (!url) {
            console.warn('pacientes: no data-url on button', btn);
            return;
        }
        // if button has data-mode=view, open modal in view-only mode
        const mode = btn.dataset && btn.dataset.mode;
        const modal = qs('#pacienteModal');
        if (mode) modal.dataset.mode = mode; else delete modal.dataset.mode;
        loadForm(url);
    });

    // view toggles and search
    const viewTable = qs('#viewTable');
    const viewCards = qs('#viewCards');
    const viewAdvanced = qs('#viewAdvanced');
    const search = qs('#patientsSearch');
    const listContainer = qs('.list-container');
    const cardsContainer = qs('.cards-container');
    let advancedMode = false;
    let tbodyListenerAdded = false;
    const tbody = qs('#patientsTable tbody');

    function showTable() {
        listContainer.style.display = '';
        cardsContainer.style.display = 'none';
        listContainer.classList.add('table-mode');
        // exit advanced mode and close any open details
        advancedMode = false;
        document.querySelectorAll('.paciente-details').forEach(d => d.style.display = 'none');
    }

    function showCards() {
        listContainer.style.display = 'none';
        cardsContainer.style.display = 'flex';
        cardsContainer.style.flexWrap = 'wrap';
    }

    function showAdvanced() {
        showTable();
        // advanced mode: rows clickable to toggle details using delegation (accordion)
        advancedMode = true;
        // add one delegated listener to tbody (idempotent)
        if (!tbodyListenerAdded && tbody) {
            tbody.addEventListener('click', function (ev) {
                if (!advancedMode) return;
                // find the clicked row (ignore clicks on the details row itself)
                const tr = ev.target.closest('tr[id^="paciente-row-"]');
                if (!tr) return;
                // avoid toggling when clicking action buttons
                if (ev.target.closest('.icon-btn')) return;
                const id = tr.id.replace('paciente-row-', '');
                const details = qs('#paciente-details-' + id);
                if (!details) return;
                const isOpen = window.getComputedStyle(details).display !== 'none';
                // close all other details (accordion behavior)
                document.querySelectorAll('.paciente-details').forEach(d => {
                    if (d !== details) d.style.display = 'none';
                });
                // toggle the clicked one
                details.style.display = isOpen ? 'none' : '';
            });
            tbodyListenerAdded = true;
        }
    }

    if (viewTable) viewTable.addEventListener('click', showTable);
    if (viewCards) viewCards.addEventListener('click', showCards);
    if (viewAdvanced) viewAdvanced.addEventListener('click', showAdvanced);

    if (search) search.addEventListener('input', function (e) {
        const q = (e.target.value || '').toLowerCase();
        document.querySelectorAll('#patientsTable tbody tr[id^="paciente-row-"]').forEach(r => {
            const name = (r.querySelector('td') || {}).textContent || '';
            r.style.display = name.toLowerCase().includes(q) ? '' : 'none';
        });
        // also filter cards
        document.querySelectorAll('.paciente-card').forEach(c => {
            const name = (c.querySelector('h4') || {}).textContent || '';
            c.style.display = name.toLowerCase().includes(q) ? 'inline-block' : 'none';
        });
    });

    // close on ESC
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            const modal = qs('#pacienteModal');
            if (modal && modal.style.display === 'block') hideModal();
        }
    });

})();
