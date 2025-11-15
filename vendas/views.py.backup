import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import VendaVinculadaForm
from .models import VendaVinculada

logger = logging.getLogger(__name__)


def list_vendas(request):
    qs = VendaVinculada.objects.all().order_by("-data_venda")
    form = VendaVinculadaForm()
    return render(
        request, "vendas_vinculadas/list.html", {"items": list(qs), "form": form}
    )


def create_venda(request):
    if request.method == "POST":
        form = VendaVinculadaForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "vendas_vinculadas/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("vendas:list"))
        else:
            logger.warning(
                "VendaVinculada create form invalid: %s", form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "vendas_vinculadas/_form_partial.html",
                    {
                        "form": form,
                        "title": "Nova Venda Vinculada",
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
        form = VendaVinculadaForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "vendas_vinculadas/_form_partial.html",
            {"form": form, "title": "Nova Venda Vinculada", "action": request.path},
        )

    return render(
        request,
        "vendas_vinculadas/form.html",
        {"form": form, "title": "Nova Venda Vinculada", "action": request.path},
    )


def update_venda(request, pk):
    item = get_object_or_404(VendaVinculada, pk=pk)
    if request.method == "POST":
        form = VendaVinculadaForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "vendas_vinculadas/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("vendas:list"))
        else:
            logger.warning(
                "VendaVinculada update form invalid (pk=%s): %s",
                pk,
                form.errors.as_json(),
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "vendas_vinculadas/_form_partial.html",
                    {"form": form, "title": f"Editar Venda", "action": request.path},
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
        form = VendaVinculadaForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "vendas_vinculadas/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Venda",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request, "vendas_vinculadas/form.html", {"form": form, "title": f"Editar Venda"}
    )
