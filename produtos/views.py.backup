from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pacientes.models import Produto

from .forms import ProdutoForm


def list_produtos(request):
    produtos = Produto.objects.select_related("id_tipo_produto").all().order_by("nome")
    form = ProdutoForm()
    return render(request, "produtos/list.html", {"produtos": produtos, "form": form})


def create_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "produtos/row.html", {"produto": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("produtos:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "produtos/_form_partial.html",
                    {"form": form, "title": "Novo Produto"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = ProdutoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "produtos/_form_partial.html",
            {"form": form, "title": "Novo Produto"},
        )

    return render(
        request, "produtos/form.html", {"form": form, "title": "Novo Produto"}
    )


def update_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "produtos/row.html", {"produto": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("produtos:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "produtos/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar {produto.nome}",
                        "instance": produto,
                    },
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = ProdutoForm(instance=produto)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "produtos/_form_partial.html",
            {"form": form, "title": f"Editar {produto.nome}", "instance": produto},
        )

    return render(
        request, "produtos/form.html", {"form": form, "title": f"Editar {produto.nome}"}
    )
