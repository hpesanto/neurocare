from django.shortcuts import render


def placeholder(request, title=None, description=None, mode="list", template=None):
    """Generic placeholder page used for menu items that don't have views yet.

    Args:
        request: HttpRequest
        title: optional title to show on the page
        description: optional description
        mode: 'list' or 'form' (controls which template to render)
        template: optional explicit template path to use (overrides mode)

    By default renders `templates/placeholders/list.html`. Use mode='form' to
    render `templates/placeholders/form.html`.
    """
    context = {
        "title": title or "Em construção",
        "description": description,
        "mode": mode,
    }
    if template:
        return render(request, template, context)

    if mode == "form":
        tpl = "placeholders/form.html"
    else:
        tpl = "placeholders/list.html"

    return render(request, tpl, context)
