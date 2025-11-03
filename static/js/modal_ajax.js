// Shared modal + AJAX helper used by list pages and modal partials
(function () {
    function qs(sel, root) { return (root || document).querySelector(sel); }

    function getCookie(name) {
        const v = document.cookie.split(';').map(c => c.trim()).find(c => c.startsWith(name + '='));
        if (!v) return null; return decodeURIComponent(v.split('=')[1]);
    }

    function closeModal() { const m = qs('#modal'); if (m) { m.style.display = 'none'; m.innerHTML = ''; } }

    // Delegate click for opening forms (data-url) and for delete buttons (data-delete-url)
    document.addEventListener('click', function (e) {
        const openBtn = e.target.closest && e.target.closest('[data-url]');
        if (openBtn) {
            // If this button is handled by a page-specific modal script (e.g. page-level handlers), skip
            try {
                if (openBtn.matches && openBtn.matches('#btnNew, .btn-edit, .btn-view')) return;
            } catch (err) { /* ignore match errors */ }
            e.preventDefault();
            const url = openBtn.getAttribute('data-url');
            fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' }, credentials: 'same-origin' })
                .then(r => { if (!r.ok) throw new Error('Network response was not ok: ' + r.status); return r.text(); })
                .then(html => {
                    const modal = qs('#modal'); if (!modal) throw new Error('Modal container #modal not found');
                    modal.innerHTML = html; modal.style.display = 'block';
                })
                .catch(err => { console.error('modal_ajax: error loading form', err); alert('Erro ao carregar o formulário. Veja o console para detalhes.'); });
            return;
        }

        const delBtn = e.target.closest && e.target.closest('[data-delete-url]');
        if (delBtn) {
            e.preventDefault();
            const url = delBtn.getAttribute('data-delete-url');
            if (!confirm('Confirma exclusão?')) return;
            fetch(url, { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') }, credentials: 'same-origin' })
                .then(r => { if (!r.ok) throw new Error('Network response was not ok: ' + r.status); return r.json(); })
                .then(resp => {
                    if (resp && resp.ok) {
                        const tbody = qs('.list-container table tbody');
                        const row = tbody && tbody.querySelector(`tr[data-id="${resp.id}"]`);
                        if (row) row.remove();
                    } else {
                        alert('Não foi possível excluir.');
                    }
                })
                .catch(err => { console.error('modal_ajax: delete error', err); alert('Erro ao excluir. Veja o console para detalhes.'); });
            return;
        }
    });

    // Delegate form submits inside modal
    document.addEventListener('submit', function (e) {
        const form = e.target.closest && e.target.closest('form');
        if (!form) return;
        // Only handle forms that are inside the modal (modal partials)
        if (!form.closest('#modal')) return;
        e.preventDefault();
        const url = form.getAttribute('action') || window.location.href;
        const data = new FormData(form);
        fetch(url, { method: 'POST', body: data, credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') } })
            .then(r => {
                const ct = r.headers.get('content-type') || '';
                if (ct.includes('application/json')) return r.json();
                return r.text();
            })
            .then(resp => {
                const modal = qs('#modal');
                if (typeof resp === 'object') {
                    if (resp.ok) {
                        if (resp.row_html) {
                            const tmp = document.createElement('tbody'); tmp.innerHTML = resp.row_html; const newRow = tmp.firstElementChild;
                            const tbody = qs('.list-container table tbody');
                            if (tbody && newRow) {
                                const existing = tbody.querySelector(`tr[data-id="${resp.id}"]`);
                                if (existing) existing.replaceWith(newRow); else tbody.insertAdjacentElement('afterbegin', newRow);
                            }
                        }
                        closeModal();
                    } else {
                        if (resp.form_html && modal) modal.innerHTML = resp.form_html;
                    }
                } else {
                    if (modal) modal.innerHTML = resp;
                }
            })
            .catch(err => { console.error('modal_ajax: submit error', err); alert('Erro ao salvar. Veja o console.'); });
    });

    // small focus helper for dynamically inserted modal content
    const obs = new MutationObserver(function (records) {
        for (const r of records) {
            for (const n of r.addedNodes) {
                if (!(n instanceof HTMLElement)) continue;
                const first = n.querySelector && n.querySelector('form input, form select, form textarea');
                if (first) { setTimeout(() => first.focus(), 40); return; }
            }
        }
    });
    const modal = qs('#modal'); if (modal) obs.observe(modal, { childList: true, subtree: true });
})();
