from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProfissionalForm
from .models import Profissional


def list_profissionais(request):
    profissionais = Profissional.objects.all().order_by("nome")
    form = ProfissionalForm()
    return render(
        request,
        "profissionais/list.html",
        {"profissionais": profissionais, "form": form},
    )


def create_profissional(request):
    if request.method == "POST":
        form = ProfissionalForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "profissionais/row.html", {"profissional": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("profissionais:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "profissionais/_form_partial.html",
                    {"form": form, "title": "Novo Profissional"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = ProfissionalForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "profissionais/_form_partial.html",
            {"form": form, "title": "Novo Profissional"},
        )

    return render(
        request, "profissionais/form.html", {"form": form, "title": "Novo Profissional"}
    )


def update_profissional(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    if request.method == "POST":
        form = ProfissionalForm(request.POST, instance=profissional)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "profissionais/row.html", {"profissional": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("profissionais:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "profissionais/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar {profissional.nome}",
                        "instance": profissional,
                    },
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = ProfissionalForm(instance=profissional)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "profissionais/_form_partial.html",
            {
                "form": form,
                "title": f"Editar {profissional.nome}",
                "instance": profissional,
            },
        )

    return render(
        request,
        "profissionais/form.html",
        {"form": form, "title": f"Editar {profissional.nome}"},
    )
