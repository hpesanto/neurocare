from django.contrib.auth.decorators import login_required

import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import TransacaoFinanceiraForm
from .models import TransacaoFinanceira

logger = logging.getLogger(__name__)


@login_required
def list_transacoes(request):
    qs = TransacaoFinanceira.objects.all().order_by("-data_transacao")
    form = TransacaoFinanceiraForm()
    return render(request, "transacoes/list.html", {"items": list(qs), "form": form})


@login_required
def create_transacao(request):
    if request.method == "POST":
        form = TransacaoFinanceiraForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "transacoes/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("transacoes:list"))
        else:
            logger.warning("Transacao create form invalid: %s", form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "transacoes/_form_partial.html",
                    {"form": form, "title": "Nova Transação", "action": request.path},
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
        form = TransacaoFinanceiraForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "transacoes/_form_partial.html",
            {"form": form, "title": "Nova Transação", "action": request.path},
        )

    return render(
        request,
        "transacoes/form.html",
        {"form": form, "title": "Nova Transação", "action": request.path},
    )


@login_required
def update_transacao(request, pk):
    item = get_object_or_404(TransacaoFinanceira, pk=pk)
    if request.method == "POST":
        form = TransacaoFinanceiraForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "transacoes/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("transacoes:list"))
        else:
            logger.warning(
                "Transacao update form invalid (pk=%s): %s", pk, form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "transacoes/_form_partial.html",
                    {"form": form, "title": "Editar Transação", "action": request.path},
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
        form = TransacaoFinanceiraForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "transacoes/_form_partial.html",
            {
                "form": form,
                "title": "Editar Transação",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request, "transacoes/form.html", {"form": form, "title": "Editar Transação"}
    )
