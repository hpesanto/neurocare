from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def prepare_field_items(form):
    """Return a list of simple dicts for template consumption.

    Each item contains pre-rendered safe HTML strings for label, widget,
    errors and help text. This avoids deep attribute lookups inside
    included templates and prevents accidental recursion during template
    variable resolution.
    """
    items = []
    for field in form.visible_fields():
        label_html = field.label_tag() or ""
        widget_html = str(field)
        errors_html = ""
        if field.errors:
            errors_html = "".join(
                [f"<div class='field-error'>{e}</div>" for e in field.errors]
            )
        help_html = (
            f"<div class='field-help'>{field.help_text}</div>"
            if field.help_text
            else ""
        )
        items.append(
            {
                "label_html": mark_safe(label_html),
                "widget_html": mark_safe(widget_html),
                "errors_html": mark_safe(errors_html),
                "help_html": mark_safe(help_html),
            }
        )
    return items
