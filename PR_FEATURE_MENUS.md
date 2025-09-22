Title: feat: menus — Add configurable menu with subitems

This PR implements the new menu system and related templates/context processor.

Summary of changes:
- Add `neurocare_project/menu_config.py` for declarative menu items and subitems
- Add `neurocare_project/context_processors.py` to expose filtered `MENU_ITEMS` to templates
- Add templates `templates/includes/menu.html` and `templates/includes/menu_item.html` for recursive rendering
- Wire menu into base template and update menus where needed

Notes:
- The repo uses UUID PKs for `Paciente` and some URL patterns were adjusted accordingly in `pacientes/urls.py`.
- Development branch is the base for this feature (branch: `development`).

Please review menu structure and permission handling for items that require specific Django permissions.
