import os

from django.conf import settings

from .menu_config import MENU


def _filter_items(items, user):
    """Return a filtered copy of items where:
    - children are always evaluated independently of parent permissions
    - a parent is included if:
        * it itself passes its permissions OR
        * it has at least one visible child OR
        * it has a url
    This implements "bloqueio apenas no nível de filhos" (parent does not block children).
    """
    visible = []
    for item in items:
        # Evaluate children first (children are evaluated independently)
        new_item = item.copy()
        children = item.get("children")
        if children:
            filtered_children = _filter_items(children, user)
            if filtered_children:
                new_item["children"] = filtered_children
            else:
                new_item.pop("children", None)

        # Determine if the parent itself is allowed
        perms = item.get("permissions")
        parent_allowed = True
        if perms:
            parent_allowed = bool(
                user and user.is_authenticated and user.has_perms(perms)
            )

        # Include the parent if it is allowed, has visible children, or has a url
        if parent_allowed or new_item.get("children") or new_item.get("url"):
            visible.append(new_item)

    return visible


def menu(request):
    user = getattr(request, "user", None)
    # try to include a cache-busting version for the logo based on file modification time
    logo_version = ""
    try:
        logo_path = os.path.join(settings.BASE_DIR, "static", "images", "logo.jpg")
        if os.path.exists(logo_path):
            logo_version = str(int(os.path.getmtime(logo_path)))
    except Exception:
        logo_version = ""

    # compute a simple static version based on base.css modification time to bust CSS/JS cache
    static_version = ""
    try:
        css_path = os.path.join(settings.BASE_DIR, "static", "css", "base.css")
        if os.path.exists(css_path):
            static_version = str(int(os.path.getmtime(css_path)))
    except Exception:
        static_version = ""

    return {
        "MENU_ITEMS": _filter_items(MENU, user),
        "logo_version": logo_version,
        "static_version": static_version,
    }
