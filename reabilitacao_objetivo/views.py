import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ReabilitacaoObjetivoForm
from .models import ReabilitacaoObjetivo

logger = logging.getLogger(__name__)


def list_objetivos(request):
    qs = ReabilitacaoObjetivo.objects.all().order_by("-data_criacao")
    form = ReabilitacaoObjetivoForm()
    return render(request, "reabilitacao_objetivo/list.html", {"items": list(qs), "form": form})


def create_objetivo(request):
    if request.method == "POST":
        form = ReabilitacaoObjetivoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "reabilitacao_objetivo/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("reabilitacao_objetivo:list"))
        else:
            logger.warning("Objetivo create form invalid: %s", form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "reabilitacao_objetivo/_form_partial.html",
                    {"form": form, "title": "Novo Objetivo", "action": request.path},
                    request=request,
                )
                return JsonResponse(
                    {"ok": False, "form_html": form_html, "errors": form.errors.get_json_data()},
                    status=400,
                )
    else:
        form = ReabilitacaoObjetivoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "reabilitacao_objetivo/_form_partial.html", {"form": form, "title": "Novo Objetivo", "action": request.path})

    return render(request, "reabilitacao_objetivo/form.html", {"form": form, "title": "Novo Objetivo", "action": request.path})


def update_objetivo(request, pk):
    item = get_object_or_404(ReabilitacaoObjetivo, pk=pk)
    if request.method == "POST":
        form = ReabilitacaoObjetivoForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "reabilitacao_objetivo/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("reabilitacao_objetivo:list"))
        else:
            logger.warning("Objetivo update form invalid (pk=%s): %s", pk, form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "reabilitacao_objetivo/_form_partial.html",
                    {"form": form, "title": "Editar Objetivo", "action": request.path},
                    request=request,
                )
                return JsonResponse(
                    {"ok": False, "form_html": form_html, "errors": form.errors.get_json_data()},
                    status=400,
                )
    else:
        form = ReabilitacaoObjetivoForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "reabilitacao_objetivo/_form_partial.html", {"form": form, "title": "Editar Objetivo", "instance": item, "action": request.path})

    return render(request, "reabilitacao_objetivo/form.html", {"form": form, "title": "Editar Objetivo"})
