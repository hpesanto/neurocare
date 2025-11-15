from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pacientes.models import TipoProduto

from .forms import TipoProdutoForm


@login_required
def list_tipos(request):
    tipos = TipoProduto.objects.all().order_by("nome")
    form = TipoProdutoForm()
    return render(request, "tipos_produto/list.html", {"tipos": tipos, "form": form})


@login_required
def create_tipo(request):
    if request.method == "POST":
        form = TipoProdutoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "tipos_produto/row.html", {"tipo": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("tipos_produto:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "tipos_produto/_form_partial.html",
                    {"form": form, "title": "Novo Tipo de Produto"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = TipoProdutoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "tipos_produto/_form_partial.html",
            {"form": form, "title": "Novo Tipo de Produto"},
        )

    return render(
        request,
        "tipos_produto/form.html",
        {"form": form, "title": "Novo Tipo de Produto"},
    )


@login_required
def update_tipo(request, pk):
    tipo = get_object_or_404(TipoProduto, pk=pk)
    if request.method == "POST":
        form = TipoProdutoForm(request.POST, instance=tipo)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "tipos_produto/row.html", {"tipo": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("tipos_produto:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "tipos_produto/_form_partial.html",
                    {"form": form, "title": f"Editar {tipo.nome}", "instance": tipo},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = TipoProdutoForm(instance=tipo)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "tipos_produto/_form_partial.html",
            {"form": form, "title": f"Editar {tipo.nome}", "instance": tipo},
        )

    return render(
        request,
        "tipos_produto/form.html",
        {"form": form, "title": f"Editar {tipo.nome}"},
    )
