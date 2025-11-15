import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import StatusObjetivoReabilitacaoForm
from .models import StatusObjetivoReabilitacao

logger = logging.getLogger(__name__)


def list_status(request):
    qs = StatusObjetivoReabilitacao.objects.all().order_by("nome")
    form = StatusObjetivoReabilitacaoForm()
    return render(
        request,
        "status_objetivo_reabilitacao/list.html",
        {"items": list(qs), "form": form},
    )


def create_status(request):
    if request.method == "POST":
        form = StatusObjetivoReabilitacaoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "status_objetivo_reabilitacao/row.html",
                    {"item": saved},
                    request=request,
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("status:list"))
        else:
            logger.warning("Status create form invalid: %s", form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "status_objetivo_reabilitacao/_form_partial.html",
                    {"form": form, "title": "Novo Status", "action": request.path},
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
        form = StatusObjetivoReabilitacaoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "status_objetivo_reabilitacao/_form_partial.html",
            {"form": form, "title": "Novo Status", "action": request.path},
        )

    return render(
        request,
        "status_objetivo_reabilitacao/form.html",
        {"form": form, "title": "Novo Status", "action": request.path},
    )


def update_status(request, pk):
    item = get_object_or_404(StatusObjetivoReabilitacao, pk=pk)
    if request.method == "POST":
        form = StatusObjetivoReabilitacaoForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "status_objetivo_reabilitacao/row.html",
                    {"item": saved},
                    request=request,
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("status:list"))
        else:
            logger.warning(
                "Status update invalid (pk=%s): %s", pk, form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "status_objetivo_reabilitacao/_form_partial.html",
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
        form = StatusObjetivoReabilitacaoForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "status_objetivo_reabilitacao/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Status",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "status_objetivo_reabilitacao/form.html",
        {"form": form, "title": f"Editar Status"},
    )
