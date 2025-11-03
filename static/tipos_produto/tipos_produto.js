document.addEventListener('DOMContentLoaded', function () {
    const modalContainer = document.getElementById('modal-container');
    const btnNew = document.getElementById('btnNew');

    function openModal(html, mode) {
        modalContainer.innerHTML = html;
        const modal = modalContainer.querySelector('form');
        // store mode on container so other helpers can read it
        if (mode) modalContainer.dataset.mode = mode; else delete modalContainer.dataset.mode;
        const btnCancel = modalContainer.querySelector('#btnCancel');
        if (btnCancel) btnCancel.addEventListener('click', () => (modalContainer.innerHTML = ''));
        // if view-only mode, disable inputs and hide submit
        if (mode === 'view') {
            const nodes = modalContainer.querySelectorAll('input,select,textarea,button');
            nodes.forEach(n => {
                if (n.tagName.toLowerCase() === 'button' && n.type !== 'submit') return;
                try { n.setAttribute('disabled', 'disabled'); } catch (e) { }
            });
            const submit = modalContainer.querySelector('form button[type=submit]');
            if (submit) submit.style.display = 'none';
        }
        if (modal) modal.addEventListener('submit', submitForm);
    }

    async function fetchForm(url, mode) {
        const res = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
        if (res.ok) {
            const html = await res.text();
            openModal(html, mode);
        } else {
            console.error('Failed to fetch form', res.status);
        }
    }

    async function submitForm(ev) {
        ev.preventDefault();
        const form = ev.target;
        const action = form.getAttribute('action');
        const data = new FormData(form);
        const res = await fetch(action, {
            method: 'POST',
            body: data,
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });
        if (res.ok) {
            const json = await res.json();
            if (json.ok) {
                const tbody = document.querySelector('#tipos-table tbody');
                const temp = document.createElement('tbody');
                temp.innerHTML = json.row_html;
                const newRow = temp.firstElementChild;
                const existing = document.getElementById('tipo-row-' + json.id);
                if (existing) existing.replaceWith(newRow);
                else tbody.appendChild(newRow);
                modalContainer.innerHTML = '';
            } else {
                const jsonErr = await res.json();
                modalContainer.innerHTML = jsonErr.form_html;
                const modalForm = modalContainer.querySelector('form');
                modalForm.addEventListener('submit', submitForm);
                const btnCancel = modalContainer.querySelector('#btnCancel');
                if (btnCancel) btnCancel.addEventListener('click', () => (modalContainer.innerHTML = ''));
            }
        } else {
            console.error('Submit failed', res.status);
        }
    }

    if (btnNew) btnNew.addEventListener('click', () => fetchForm(btnNew.dataset.createUrl));

    function attachHandlers(root = document) {
        root.querySelectorAll('.btn-edit').forEach((b) =>
            b.addEventListener('click', (e) => fetchForm(e.currentTarget.dataset.url))
        );
        root.querySelectorAll('.btn-view').forEach((b) =>
            b.addEventListener('click', (e) => fetchForm(e.currentTarget.dataset.url, 'view'))
        );
    }

    attachHandlers();
    const observer = new MutationObserver(() => attachHandlers());
    const tbodyEl = document.querySelector('#tipos-table tbody');
    if (tbodyEl) observer.observe(tbodyEl, { childList: true, subtree: true });

    // toggle details row on row click (accordion) ignoring clicks on icon buttons
    const table = document.querySelector('#tipos-table');
    if (table) {
        table.addEventListener('click', function (ev) {
            const tr = ev.target.closest('tr[id^="tipo-row-"]');
            if (!tr) return;
            if (ev.target.closest('.icon-btn')) return; // ignore clicks on buttons
            const id = tr.id.replace('tipo-row-', '');
            const details = document.getElementById('tipo-details-' + id);
            if (!details) return;
            const isOpen = window.getComputedStyle(details).display !== 'none';
            document.querySelectorAll('.tipo-details').forEach(d => { if (d !== details) d.style.display = 'none'; });
            details.style.display = isOpen ? 'none' : '';
        });
    }
});
