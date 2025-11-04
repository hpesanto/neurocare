document.addEventListener('DOMContentLoaded', function () {
  const modalContainer = document.getElementById('modal-container');
  const btnNew = document.getElementById('btnNew');

  function openModal(html, mode) {
    modalContainer.innerHTML = html;
    const modal = modalContainer.querySelector('form');
    const btnCancel = modalContainer.querySelector('#btnCancel');
    if (btnCancel) btnCancel.addEventListener('click', () => (modalContainer.innerHTML = ''));
    if (modal) modal.addEventListener('submit', submitForm);
    if (mode === 'view' && modal) {
      try {
        modal.querySelectorAll('input,select,textarea').forEach(n => { try { n.setAttribute('disabled', 'disabled'); } catch (e) { } });
        modal.querySelectorAll('button, input[type=submit]').forEach(n => {
          try {
            if (n.tagName.toLowerCase() === 'button') {
              if ((n.type || '').toLowerCase() === 'submit') { n.style.display = 'none'; n.setAttribute('disabled', 'disabled'); }
            } else { n.style.display = 'none'; n.setAttribute('disabled', 'disabled'); }
          } catch (e) { }
        });
      } catch (e) { console.error('convenios.openModal view-mode error', e); }
    }
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
        const tbody = document.querySelector('#convenios-table tbody');
        const temp = document.createElement('tbody');
        temp.innerHTML = json.row_html;
        const newRow = temp.firstElementChild;
        const existing = document.getElementById('convenio-row-' + json.id);
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
    root.querySelectorAll('.btn-view').forEach((b) =>
      b.addEventListener('click', (e) => fetchForm(e.currentTarget.dataset.url, 'view'))
    );
  }

  attachEditHandlers();
  const observer = new MutationObserver(() => attachEditHandlers());
  observer.observe(document.querySelector('#convenios-table tbody'), { childList: true, subtree: true });
});
