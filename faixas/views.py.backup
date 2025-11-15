from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pacientes.models import FaixaEtaria

from .forms import FaixaEtariaForm


def list_faixas(request):
    faixas = FaixaEtaria.objects.all().order_by("nome")
    form = FaixaEtariaForm()
    return render(request, "faixas/list.html", {"faixas": faixas, "form": form})


def create_faixa(request):
    if request.method == "POST":
        form = FaixaEtariaForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "faixas/row.html", {"faixa": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("faixas:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "faixas/_form_partial.html",
                    {"form": form, "title": "Nova Faixa Etária"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = FaixaEtariaForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "faixas/_form_partial.html",
            {"form": form, "title": "Nova Faixa Etária"},
        )

    return render(
        request, "faixas/form.html", {"form": form, "title": "Nova Faixa Etária"}
    )


def update_faixa(request, pk):
    faixa = get_object_or_404(FaixaEtaria, pk=pk)
    if request.method == "POST":
        form = FaixaEtariaForm(request.POST, instance=faixa)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "faixas/row.html", {"faixa": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("faixas:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "faixas/_form_partial.html",
                    {"form": form, "title": f"Editar {faixa.nome}", "instance": faixa},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = FaixaEtariaForm(instance=faixa)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "faixas/_form_partial.html",
            {"form": form, "title": f"Editar {faixa.nome}", "instance": faixa},
        )

    return render(
        request, "faixas/form.html", {"form": form, "title": f"Editar {faixa.nome}"}
    )
    return render(
        request, "faixas/form.html", {"form": form, "title": f"Editar {faixa.nome}"}
    )
