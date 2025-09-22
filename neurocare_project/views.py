from django.shortcuts import render


def under_construction(request, title=None):
    """Render a simple 'Em construção!' page. Accepts an optional title."""
    context = {"title": title or "Em construção"}
    return render(request, "under_construction.html", context)
