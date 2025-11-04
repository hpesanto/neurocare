import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import StatusPagamentoForm
from .models import StatusPagamento

logger = logging.getLogger(__name__)


def list_status_pagamento(request):
    qs = StatusPagamento.objects.all().order_by("nome")
    form = StatusPagamentoForm()
    return render(
        request, "status_pagamento/list.html", {"items": list(qs), "form": form}
    )


def _render_row(obj, request=None):
    from django.template.loader import render_to_string

    return render_to_string("status_pagamento/row.html", {"item": obj}, request=request)


def create_status(request):
    if request.method == "POST":
        form = StatusPagamentoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "ok": True,
                        "row_html": _render_row(saved, request=request),
                        "id": str(saved.id),
                    }
                )
            return redirect(reverse("status_pagamento:list"))
        else:
            logger.warning("Status create form invalid: %s", form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "status_pagamento/_form_partial.html",
                    {
                        "form": form,
                        "title": "Novo Status de Pagamento",
                        "action": request.path,
                    },
                    request=request,
                )
                return JsonResponse(
                    {
                        "ok": False,
                        "form_html": form_html,
                        "errors": form.errors.get_json_data(),
                    },
                    status=400,
                )
    else:
        form = StatusPagamentoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "status_pagamento/_form_partial.html",
            {"form": form, "title": "Novo Status de Pagamento", "action": request.path},
        )

    return render(
        request,
        "status_pagamento/form.html",
        {"form": form, "title": "Novo Status de Pagamento", "action": request.path},
    )


def update_status(request, pk):
    item = get_object_or_404(StatusPagamento, pk=pk)
    if request.method == "POST":
        form = StatusPagamentoForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                row_html = _render_row(saved, request=request)
                return JsonResponse(
                    {"ok": True, "row_html": row_html, "id": str(saved.id)}
                )
            return redirect(reverse("status_pagamento:list"))
        else:
            logger.warning(
                "Status update invalid (pk=%s): %s", pk, form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "status_pagamento/_form_partial.html",
                    {"form": form, "title": f"Editar Status", "action": request.path},
                    request=request,
                )
                return JsonResponse(
                    {
                        "ok": False,
                        "form_html": form_html,
                        "errors": form.errors.get_json_data(),
                    },
                    status=400,
                )
    else:
        form = StatusPagamentoForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "status_pagamento/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Status",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "status_pagamento/form.html",
        {
            "form": form,
            "title": f"Editar Status",
            "action": request.path,
            "instance": item,
        },
    )


def delete_status(request, pk):
    """Handle deletion of a StatusPagamento. Accepts POST (AJAX or normal).

    Returns JSON {ok: True, id: <pk>} for AJAX POST, otherwise redirects to list.
    """
    item = get_object_or_404(StatusPagamento, pk=pk)
    if request.method == "POST":
        item.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "id": str(pk)})
        return redirect(reverse("status_pagamento:list"))

    # For non-POST, prefer redirecting to list (or could render a confirmation partial)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": False}, status=405)
    return redirect(reverse("status_pagamento:list"))
