// static/js/menu.js - progressive enhancement for menu toggles and keyboard support
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.has-children > a, .has-children > span').forEach(function (toggle) {
        const parent = toggle.parentElement;
        toggle.setAttribute('aria-haspopup', 'true');
        toggle.setAttribute('aria-expanded', parent.classList.contains('open') ? 'true' : 'false');

        toggle.addEventListener('click', function (ev) {
            // If the parent has children, clicking the parent should toggle the submenu
            // even if the <a> has an href. This matches the expected UX where 'Cadastro'
            // opens its options instead of navigating away.
            if (parent.classList.contains('has-children')) {
                ev.preventDefault();
                const willOpen = !parent.classList.contains('open');
                // Close sibling open menus (accordion behaviour)
                const siblings = Array.from(parent.parentElement.children).filter(function (c) {
                    return c !== parent && c.classList && c.classList.contains('has-children');
                });
                siblings.forEach(function (s) {
                    if (s.classList.contains('open')) {
                        s.classList.remove('open');
                        const t = s.querySelector('a, span');
                        if (t) t.setAttribute('aria-expanded', 'false');
                    }
                });

                // Toggle the clicked parent
                if (willOpen) {
                    parent.classList.add('open');
                    toggle.setAttribute('aria-expanded', 'true');
                } else {
                    parent.classList.remove('open');
                    toggle.setAttribute('aria-expanded', 'false');
                }
                return;
            }

            // Otherwise, if it's a normal link (and not '#'), let it navigate normally.
            const href = toggle.getAttribute('href');
            if (href && href !== '#') return;
            // If no href or href is '#', prevent default to avoid jumping
            ev.preventDefault();
        });

        toggle.addEventListener('keydown', function (ev) {
            if (ev.key === 'Enter' || ev.key === ' ') {
                ev.preventDefault();
                toggle.click();
            } else if (ev.key === 'Escape') {
                parent.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.focus();
            }
        });
    });

    document.addEventListener('click', function (ev) {
        if (!ev.target.closest('.main-menu')) {
            document.querySelectorAll('.has-children.open').forEach(function (el) {
                el.classList.remove('open');
                const t = el.querySelector('a, span');
                if (t) t.setAttribute('aria-expanded', 'false');
            });
        }
    });
});
