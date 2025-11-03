import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import VendaGeralForm, VendaGeralItemForm
from .models import VendaGeral, VendaGeralItem

logger = logging.getLogger(__name__)


def list_venda_geral(request):
    qs = VendaGeral.objects.all().order_by("-data_venda")
    form = VendaGeralForm()
    return render(request, "vendas_geral/list.html", {"items": list(qs), "form": form})


def create_venda_geral(request):
    if request.method == "POST":
        form = VendaGeralForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "vendas_geral/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("vendas_geral:list"))
        else:
            logger.warning("VendaGeral create form invalid: %s", form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "vendas_geral/_form_partial.html",
                    {
                        "form": form,
                        "title": "Nova Venda (Geral)",
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
        form = VendaGeralForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "vendas_geral/_form_partial.html",
            {"form": form, "title": "Nova Venda (Geral)", "action": request.path},
        )

    return render(
        request,
        "vendas_geral/form.html",
        {"form": form, "title": "Nova Venda (Geral)", "action": request.path},
    )


def update_venda_geral(request, pk):
    item = get_object_or_404(VendaGeral, pk=pk)
    if request.method == "POST":
        form = VendaGeralForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "vendas_geral/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("vendas_geral:list"))
        else:
            logger.warning(
                "VendaGeral update form invalid (pk=%s): %s", pk, form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "vendas_geral/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar Venda (Geral)",
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
        form = VendaGeralForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "vendas_geral/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Venda (Geral)",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "vendas_geral/form.html",
        {"form": form, "title": "Editar Venda (Geral)"},
    )


def list_venda_geral_itens(request):
    qs = VendaGeralItem.objects.all().order_by("-data_criacao")
    form = VendaGeralItemForm()
    return render(
        request, "vendas_geral/itens_list.html", {"items": list(qs), "form": form}
    )


def create_venda_geral_item(request):
    if request.method == "POST":
        form = VendaGeralItemForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "vendas_geral/itens_row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("vendas_geral:itens_list"))
        else:
            logger.warning(
                "VendaGeralItem create form invalid: %s", form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "vendas_geral/itens_form_partial.html",
                    {
                        "form": form,
                        "title": "Novo Item de Venda",
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
        form = VendaGeralItemForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "vendas_geral/itens_form_partial.html",
            {"form": form, "title": "Novo Item de Venda", "action": request.path},
        )

    return render(
        request,
        "vendas_geral/itens_form.html",
        {"form": form, "title": "Novo Item de Venda", "action": request.path},
    )


def update_venda_geral_item(request, pk):
    item = get_object_or_404(VendaGeralItem, pk=pk)
    if request.method == "POST":
        form = VendaGeralItemForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "vendas_geral/itens_row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("vendas_geral:itens_list"))
        else:
            logger.warning(
                "VendaGeralItem update form invalid (pk=%s): %s",
                pk,
                form.errors.as_json(),
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "vendas_geral/itens_form_partial.html",
                    {
                        "form": form,
                        "title": "Editar Item de Venda",
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
        form = VendaGeralItemForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "vendas_geral/itens_form_partial.html",
            {
                "form": form,
                "title": "Editar Item de Venda",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "vendas_geral/itens_form.html",
        {"form": form, "title": "Editar Item de Venda"},
    )
