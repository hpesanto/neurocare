from django.contrib.auth.decorators import login_required

import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AvaliacaoNeuropsicologicaForm
from .models import AvaliacaoNeuropsicologica

logger = logging.getLogger(__name__)


@login_required
def list_avaliacao(request):
    qs = AvaliacaoNeuropsicologica.objects.all().order_by("-data_avaliacao")
    form = AvaliacaoNeuropsicologicaForm()
    return render(
        request,
        "avaliacao_neuropsicologica/list.html",
        {"items": list(qs), "form": form},
    )


@login_required
def create_avaliacao(request):
    if request.method == "POST":
        form = AvaliacaoNeuropsicologicaForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "avaliacao_neuropsicologica/row.html",
                    {"item": saved},
                    request=request,
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("avaliacao:list"))
        else:
            logger.warning("Avaliacao create form invalid: %s", form.errors.as_json())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "avaliacao_neuropsicologica/_form_partial.html",
                    {
                        "form": form,
                        "title": "Nova Avaliação Neuropsicológica",
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
        form = AvaliacaoNeuropsicologicaForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "avaliacao_neuropsicologica/_form_partial.html",
            {
                "form": form,
                "title": "Nova Avaliação Neuropsicológica",
                "action": request.path,
            },
        )

    return render(
        request,
        "avaliacao_neuropsicologica/form.html",
        {
            "form": form,
            "title": "Nova Avaliação Neuropsicológica",
            "action": request.path,
        },
    )


@login_required
def update_avaliacao(request, pk):
    item = get_object_or_404(AvaliacaoNeuropsicologica, pk=pk)
    if request.method == "POST":
        form = AvaliacaoNeuropsicologicaForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "avaliacao_neuropsicologica/row.html",
                    {"item": saved},
                    request=request,
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("avaliacao:list"))
        else:
            logger.warning(
                "Avaliacao update invalid (pk=%s): %s", pk, form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "avaliacao_neuropsicologica/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar Avaliação",
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
        form = AvaliacaoNeuropsicologicaForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "avaliacao_neuropsicologica/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Avaliação",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "avaliacao_neuropsicologica/form.html",
        {"form": form, "title": f"Editar Avaliação"},
    )
