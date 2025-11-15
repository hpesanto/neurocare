from django.contrib.auth.decorators import login_required

import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from profissionais.models import Profissional

from .forms import UsuarioForm


@login_required
def list_usuarios(request):
    logger = logging.getLogger(__name__)
    qs = Profissional.objects.all().order_by("nome")
    usuarios = list(qs)
    form = UsuarioForm()
    return render(request, "usuarios/list.html", {"usuarios": usuarios, "form": form})


@login_required
def create_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "usuarios/row.html", {"usuario": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("usuarios:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "usuarios/_form_partial.html",
                    {"form": form, "title": "Novo Usuário"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = UsuarioForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "usuarios/_form_partial.html",
            {"form": form, "title": "Novo Usuário"},
        )

    return render(
        request, "usuarios/form.html", {"form": form, "title": "Novo Usuário"}
    )


@login_required
def update_usuario(request, pk):
    usuario = get_object_or_404(Profissional, pk=pk)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "usuarios/row.html", {"usuario": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("usuarios:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "usuarios/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar {usuario.nome}",
                        "instance": usuario,
                    },
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = UsuarioForm(instance=usuario)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "usuarios/_form_partial.html",
            {
                "form": form,
                "title": f"Editar {usuario.nome}",
                "instance": usuario,
            },
        )

    return render(
        request,
        "usuarios/form.html",
        {"form": form, "title": f"Editar {usuario.nome}"},
    )
