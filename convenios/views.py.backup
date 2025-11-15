from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pacientes.models import Convenio

from .forms import ConvenioForm


def list_convenios(request):
    convenios = Convenio.objects.all().order_by("nome")
    form = ConvenioForm()
    return render(
        request, "convenios/list.html", {"convenios": convenios, "form": form}
    )


def create_convenio(request):
    if request.method == "POST":
        form = ConvenioForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "convenios/row.html", {"convenio": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("convenios:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "convenios/_form_partial.html",
                    {"form": form, "title": "Novo Convênio"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = ConvenioForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "convenios/_form_partial.html",
            {"form": form, "title": "Novo Convênio"},
        )

    return render(
        request, "convenios/form.html", {"form": form, "title": "Novo Convênio"}
    )


def update_convenio(request, pk):
    convenio = get_object_or_404(Convenio, pk=pk)
    if request.method == "POST":
        form = ConvenioForm(request.POST, instance=convenio)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "convenios/row.html", {"convenio": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("convenios:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "convenios/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar {convenio.nome}",
                        "instance": convenio,
                    },
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = ConvenioForm(instance=convenio)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "convenios/_form_partial.html",
            {"form": form, "title": f"Editar {convenio.nome}", "instance": convenio},
        )

    return render(
        request,
        "convenios/form.html",
        {"form": form, "title": f"Editar {convenio.nome}"},
    )
    return render(
        request,
        "convenios/form.html",
        {"form": form, "title": f"Editar {convenio.nome}"},
    )
