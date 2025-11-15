import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import EvolucaoClinicaForm
from .models import EvolucaoClinica

logger = logging.getLogger(__name__)


def list_evolucao(request):
    qs = EvolucaoClinica.objects.all().order_by("-data_sessao", "-hora_sessao")
    form = EvolucaoClinicaForm()
    return render(
        request, "evolucao_clinica/list.html", {"items": list(qs), "form": form}
    )


def create_evolucao(request):
    if request.method == "POST":
        form = EvolucaoClinicaForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "evolucao_clinica/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("evolucao:list"))
        else:
            logger.warning(
                "EvolucaoClinica create form invalid: %s", form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "evolucao_clinica/_form_partial.html",
                    {
                        "form": form,
                        "title": "Nova Evolução Clínica",
                        "action": request.path,
                    },
                    request=request,
                )
                # return structured errors (get_json_data returns serializable structure)
                return JsonResponse(
                    {
                        "ok": False,
                        "form_html": form_html,
                        "errors": form.errors.get_json_data(),
                    },
                    status=400,
                )
    else:
        form = EvolucaoClinicaForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "evolucao_clinica/_form_partial.html",
            {"form": form, "title": "Nova Evolução Clínica", "action": request.path},
        )

    return render(
        request,
        "evolucao_clinica/form.html",
        {"form": form, "title": "Nova Evolução Clínica", "action": request.path},
    )


def update_evolucao(request, pk):
    item = get_object_or_404(EvolucaoClinica, pk=pk)
    if request.method == "POST":
        form = EvolucaoClinicaForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "evolucao_clinica/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("evolucao:list"))
        else:
            logger.warning(
                "EvolucaoClinica update form invalid (pk=%s): %s",
                pk,
                form.errors.as_json(),
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "evolucao_clinica/_form_partial.html",
                    {"form": form, "title": f"Editar Evolução", "action": request.path},
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
        form = EvolucaoClinicaForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "evolucao_clinica/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Evolução",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "evolucao_clinica/form.html",
        {"form": form, "title": f"Editar Evolução"},
    )
