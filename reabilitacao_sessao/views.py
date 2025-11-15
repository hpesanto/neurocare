from django.contrib.auth.decorators import login_required

import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ReabilitacaoSessaoForm
from .models import ReabilitacaoSessao

logger = logging.getLogger(__name__)


@login_required
def list_sessoes(request):
    qs = ReabilitacaoSessao.objects.all().order_by("-data_sessao", "-hora_sessao")
    form = ReabilitacaoSessaoForm()
    return render(
        request, "reabilitacao_sessao/list.html", {"items": list(qs), "form": form}
    )


@login_required
def create_sessao(request):
    if request.method == "POST":
        form = ReabilitacaoSessaoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "reabilitacao_sessao/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("sessoes:list"))
        else:
            logger.warning(
                "ReabilitacaoSessao create form invalid: %s", form.errors.as_json()
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "reabilitacao_sessao/_form_partial.html",
                    {
                        "form": form,
                        "title": "Nova Sessão de Reabilitação",
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
        form = ReabilitacaoSessaoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "reabilitacao_sessao/_form_partial.html",
            {
                "form": form,
                "title": "Nova Sessão de Reabilitação",
                "action": request.path,
            },
        )

    return render(
        request,
        "reabilitacao_sessao/form.html",
        {"form": form, "title": "Nova Sessão de Reabilitação", "action": request.path},
    )


@login_required
def update_sessao(request, pk):
    item = get_object_or_404(ReabilitacaoSessao, pk=pk)
    if request.method == "POST":
        form = ReabilitacaoSessaoForm(request.POST, instance=item)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "reabilitacao_sessao/row.html", {"item": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("sessoes:list"))
        else:
            logger.warning(
                "ReabilitacaoSessao update form invalid (pk=%s): %s",
                pk,
                form.errors.as_json(),
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "reabilitacao_sessao/_form_partial.html",
                    {"form": form, "title": f"Editar Sessão", "action": request.path},
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
        form = ReabilitacaoSessaoForm(instance=item)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "reabilitacao_sessao/_form_partial.html",
            {
                "form": form,
                "title": f"Editar Sessão",
                "instance": item,
                "action": request.path,
            },
        )

    return render(
        request,
        "reabilitacao_sessao/form.html",
        {"form": form, "title": f"Editar Sessão"},
    )
