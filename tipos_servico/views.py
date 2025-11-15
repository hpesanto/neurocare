from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pacientes.models import TipoServico

from .forms import TipoServicoForm


@login_required
def list_tipos_servico(request):
    tipos = TipoServico.objects.all().order_by("nome")
    form = TipoServicoForm()
    return render(request, "tipos_servico/list.html", {"tipos": tipos, "form": form})


@login_required
def create_tipo_servico(request):
    if request.method == "POST":
        form = TipoServicoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "tipos_servico/row.html", {"tipo": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("tipos_servico:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "tipos_servico/_form_partial.html",
                    {"form": form, "title": "Novo Tipo de Servico"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = TipoServicoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "tipos_servico/_form_partial.html",
            {"form": form, "title": "Novo Tipo de Servico"},
        )

    return render(
        request,
        "tipos_servico/form.html",
        {"form": form, "title": "Novo Tipo de Servico"},
    )


@login_required
def update_tipo_servico(request, pk):
    tipo = get_object_or_404(TipoServico, pk=pk)
    if request.method == "POST":
        form = TipoServicoForm(request.POST, instance=tipo)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "tipos_servico/row.html", {"tipo": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("tipos_servico:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "tipos_servico/_form_partial.html",
                    {"form": form, "title": f"Editar {tipo.nome}", "instance": tipo},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = TipoServicoForm(instance=tipo)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "tipos_servico/_form_partial.html",
            {"form": form, "title": f"Editar {tipo.nome}", "instance": tipo},
        )

    return render(
        request,
        "tipos_servico/form.html",
        {"form": form, "title": f"Editar {tipo.nome}"},
    )
