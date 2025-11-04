document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modal');
    const btnNew = document.getElementById('btnNewStatus');

    function disableViewMode(modalEl) {
        try {
            const form = modalEl.querySelector('form');
            if (!form) return;
            form.querySelectorAll('input,select,textarea').forEach(n => { try { n.setAttribute('disabled', 'disabled'); } catch (e) { } });
            form.querySelectorAll('button, input[type=submit]').forEach(n => {
                try {
                    const tag = n.tagName.toLowerCase();
                    if (tag === 'button') {
                        if ((n.type || '').toLowerCase() === 'submit') { n.style.display = 'none'; n.setAttribute('disabled', 'disabled'); }
                    } else {
                        n.style.display = 'none'; n.setAttribute('disabled', 'disabled');
                    }
                } catch (e) { }
            });
        } catch (e) { console.error('status_pagamento: disableViewMode error', e); }
    }

    async function fetchForm(url, mode) {
        try {
            const res = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' }, credentials: 'same-origin' });
            if (!res.ok) { console.error('status_pagamento: fetch failed', res.status); return; }
            const html = await res.text();
            if (!modal) { console.error('status_pagamento: modal container #modal not found'); return; }
            // set mode on modal for potential consumers
            if (mode) modal.dataset.mode = mode; else delete modal.dataset.mode;
            modal.innerHTML = html; modal.style.display = 'block';
            if (mode === 'view') disableViewMode(modal);
        } catch (err) { console.error('status_pagamento: fetchForm error', err); alert('Erro ao carregar o formulário. Veja o console para detalhes.'); }
    }

    if (btnNew) btnNew.addEventListener('click', (e) => {
        const url = btnNew.dataset.url || btnNew.getAttribute('data-url') || btnNew.dataset.createUrl;
        if (url) fetchForm(url);
    });

    function attachHandlers(root = document) {
        root.querySelectorAll('.btn-edit').forEach((b) => {
            // avoid double-binding
            if (b._spAttached) return; b._spAttached = true;
            b.addEventListener('click', (e) => { e.preventDefault(); fetchForm(e.currentTarget.dataset.url); });
        });
        root.querySelectorAll('.btn-view').forEach((b) => {
            if (b._spAttached) return; b._spAttached = true;
            b.addEventListener('click', (e) => { e.preventDefault(); fetchForm(e.currentTarget.dataset.url, 'view'); });
        });
    }

    attachHandlers();
    const tbody = document.querySelector('.list-container table tbody');
    if (tbody) {
        const obs = new MutationObserver(() => attachHandlers(tbody));
        obs.observe(tbody, { childList: true, subtree: true });
    }
});
