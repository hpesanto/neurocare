from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pacientes.models import ContatoEmergencia

from .forms import ContatoEmergenciaForm


def list_contatos(request):
    contatos = (
        ContatoEmergencia.objects.select_related("id_paciente")
        .all()
        .order_by("nome_contato")
    )
    form = ContatoEmergenciaForm()
    return render(
        request, "contatos_emergencia/list.html", {"contatos": contatos, "form": form}
    )


def create_contato(request):
    if request.method == "POST":
        form = ContatoEmergenciaForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "contatos_emergencia/row.html", {"contato": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("contatos_emergencia:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "contatos_emergencia/_form_partial.html",
                    {"form": form, "title": "Novo Contato de Emergencia"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = ContatoEmergenciaForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "contatos_emergencia/_form_partial.html",
            {"form": form, "title": "Novo Contato de Emergencia"},
        )

    return render(
        request,
        "contatos_emergencia/form.html",
        {"form": form, "title": "Novo Contato de Emergencia"},
    )


def update_contato(request, pk):
    contato = get_object_or_404(ContatoEmergencia, pk=pk)
    if request.method == "POST":
        form = ContatoEmergenciaForm(request.POST, instance=contato)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "contatos_emergencia/row.html", {"contato": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("contatos_emergencia:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "contatos_emergencia/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar {contato.nome_contato}",
                        "instance": contato,
                    },
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = ContatoEmergenciaForm(instance=contato)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "contatos_emergencia/_form_partial.html",
            {
                "form": form,
                "title": f"Editar {contato.nome_contato}",
                "instance": contato,
            },
        )

    return render(
        request,
        "contatos_emergencia/form.html",
        {"form": form, "title": f"Editar {contato.nome_contato}"},
    )
