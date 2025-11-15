from django.contrib.auth.decorators import login_required

import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import FormaCobrancaReabilitacaoForm
from .models import FormaCobrancaReabilitacao

logger = logging.getLogger(__name__)


@login_required
def list_formas(request):
    qs = FormaCobrancaReabilitacao.objects.all().order_by("nome")
    form = FormaCobrancaReabilitacaoForm()
    return render(
        request,
        "formas_cobranca_reabilitacao/list.html",
        {"items": list(qs), "form": form},
    )


@login_required
def create_forma(request):
    if request.method == "POST":
        form = FormaCobrancaReabilitacaoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "formas_cobranca_reabilitacao/row.html",
                    {"item": saved},
                    request=request,
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("formas_cobranca:list"))
        else:
            logger.warning("Forma create form invalid: %s", form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "formas_cobranca_reabilitacao/_form_partial.html",
                    {
                        "form": form,
                        "title": "Nova Forma de Cobrança",
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
        form = FormaCobrancaReabilitacaoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "formas_cobranca_reabilitacao/_form_partial.html",
            {"form": form, "title": "Nova Forma de Cobrança", "action": request.path},
        )

    return render(
        request,
        "formas_cobranca_reabilitacao/form.html",
        {"form": form, "title": "Nova Forma de Cobrança", "action": request.path},
    )


@login_required
def update_forma(request, pk):
    item = get_object_or_404(FormaCobrancaReabilitacao, pk=pk)
    if request.method == "POST":
        form = FormaCobrancaReabilitacaoForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "formas_cobranca_reabilitacao/row.html",
                    {"item": saved},
                    request=request,
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("formas_cobranca:list"))
        else:
            logger.warning(
                "Forma update invalid (pk=%s): %s", pk, form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "formas_cobranca_reabilitacao/_form_partial.html",
                    {"form": form, "title": f"Editar Forma", "action": request.path},
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
        form = FormaCobrancaReabilitacaoForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "formas_cobranca_reabilitacao/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Forma",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "formas_cobranca_reabilitacao/form.html",
        {"form": form, "title": f"Editar Forma"},
    )
