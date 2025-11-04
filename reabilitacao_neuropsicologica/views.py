import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ReabilitacaoNeuropsicologicaForm
from .models import ReabilitacaoNeuropsicologica

logger = logging.getLogger(__name__)


def list_reabilitacao(request):
    qs = ReabilitacaoNeuropsicologica.objects.all().order_by("-data_inicio")
    form = ReabilitacaoNeuropsicologicaForm()
    return render(
        request,
        "reabilitacao_neuropsicologica/list.html",
        {"items": list(qs), "form": form},
    )


def create_reabilitacao(request):
    if request.method == "POST":
        form = ReabilitacaoNeuropsicologicaForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "reabilitacao_neuropsicologica/row.html",
                    {"item": saved},
                    request=request,
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("reabilitacao:list"))
        else:
            logger.warning(
                "Reabilitacao create form invalid: %s", form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "reabilitacao_neuropsicologica/_form_partial.html",
                    {
                        "form": form,
                        "title": "Nova Reabilitação",
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
        form = ReabilitacaoNeuropsicologicaForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "reabilitacao_neuropsicologica/_form_partial.html",
            {"form": form, "title": "Nova Reabilitação", "action": request.path},
        )

    return render(
        request,
        "reabilitacao_neuropsicologica/form.html",
        {"form": form, "title": "Nova Reabilitação", "action": request.path},
    )


def update_reabilitacao(request, pk):
    item = get_object_or_404(ReabilitacaoNeuropsicologica, pk=pk)
    if request.method == "POST":
        form = ReabilitacaoNeuropsicologicaForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "reabilitacao_neuropsicologica/row.html",
                    {"item": saved},
                    request=request,
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("reabilitacao:list"))
        else:
            logger.warning(
                "Reabilitacao update invalid (pk=%s): %s", pk, form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "reabilitacao_neuropsicologica/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar Reabilitação",
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
        form = ReabilitacaoNeuropsicologicaForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "reabilitacao_neuropsicologica/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Reabilitação",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "reabilitacao_neuropsicologica/form.html",
        {"form": form, "title": f"Editar Reabilitação"},
    )
