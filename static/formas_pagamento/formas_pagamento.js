document.addEventListener('DOMContentLoaded', function () {
    const modalContainer = document.getElementById('modal-container');
    const btnNew = document.getElementById('btnNew');

    function openModal(html) {
        modalContainer.innerHTML = html;
        const modal = modalContainer.querySelector('form');
        const btnCancel = modalContainer.querySelector('#btnCancel');
        if (btnCancel) btnCancel.addEventListener('click', () => (modalContainer.innerHTML = ''));
        modal.addEventListener('submit', submitForm);
    }

    async function fetchForm(url) {
        const res = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
        if (res.ok) {
            const html = await res.text();
            openModal(html);
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
                const tbody = document.querySelector('#formas-table tbody');
                const temp = document.createElement('tbody');
                temp.innerHTML = json.row_html;
                const newRow = temp.firstElementChild;
                const existing = document.getElementById('forma-row-' + json.id);
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

    function attachEditHandlers(root = document) {
        root.querySelectorAll('.btn-edit').forEach((b) =>
            b.addEventListener('click', (e) => fetchForm(e.currentTarget.dataset.url))
        );
    }

    attachEditHandlers();
    const observer = new MutationObserver(() => attachEditHandlers());
    observer.observe(document.querySelector('#formas-table tbody'), { childList: true, subtree: true });
});
qs('#modalContent').innerHTML = qs('#modalSpinner').outerHTML || '';
