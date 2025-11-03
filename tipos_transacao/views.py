import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import TipoTransacaoForm
from .models import TipoTransacaoFinanceira

logger = logging.getLogger(__name__)


def list_tipos(request):
    qs = TipoTransacaoFinanceira.objects.all().order_by("nome")
    form = TipoTransacaoForm()
    return render(
        request, "tipos_transacao/list.html", {"items": list(qs), "form": form}
    )


def create_tipo(request):
    if request.method == "POST":
        form = TipoTransacaoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "tipos_transacao/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("tipos_transacao:list"))
        else:
            logger.warning("Tipo create form invalid: %s", form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "tipos_transacao/_form_partial.html",
                    {
                        "form": form,
                        "title": "Novo Tipo de Transação",
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
        form = TipoTransacaoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "tipos_transacao/_form_partial.html",
            {"form": form, "title": "Novo Tipo de Transação", "action": request.path},
        )

    return render(
        request,
        "tipos_transacao/form.html",
        {"form": form, "title": "Novo Tipo de Transação", "action": request.path},
    )


def update_tipo(request, pk):
    item = get_object_or_404(TipoTransacaoFinanceira, pk=pk)
    if request.method == "POST":
        form = TipoTransacaoForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "tipos_transacao/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("tipos_transacao:list"))
        else:
            logger.warning("Tipo update invalid (pk=%s): %s", pk, form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "tipos_transacao/_form_partial.html",
                    {"form": form, "title": f"Editar Tipo", "action": request.path},
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
        form = TipoTransacaoForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "tipos_transacao/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Tipo",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request, "tipos_transacao/form.html", {"form": form, "title": f"Editar Tipo"}
    )
