from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pacientes.models import PacienteServico

from .forms import PacienteServicoForm


@login_required
def list_paciente_servicos(request):
    servicos = (
        PacienteServico.objects.select_related(
            "id_paciente", "id_tipo_servico", "psicologo_responsavel_servico"
        )
        .all()
        .order_by("data_inicio")
    )
    form = PacienteServicoForm()
    return render(
        request, "paciente_servico/list.html", {"servicos": servicos, "form": form}
    )


@login_required
def create_paciente_servico(request):
    if request.method == "POST":
        form = PacienteServicoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "paciente_servico/row.html", {"servico": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("paciente_servico:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "paciente_servico/_form_partial.html",
                    {"form": form, "title": "Novo Paciente x Servico"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = PacienteServicoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "paciente_servico/_form_partial.html",
            {"form": form, "title": "Novo Paciente x Servico"},
        )

    return render(
        request,
        "paciente_servico/form.html",
        {"form": form, "title": "Novo Paciente x Servico"},
    )


@login_required
def update_paciente_servico(request, pk):
    servico = get_object_or_404(PacienteServico, pk=pk)
    if request.method == "POST":
        form = PacienteServicoForm(request.POST, instance=servico)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "paciente_servico/row.html", {"servico": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("paciente_servico:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "paciente_servico/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar {servico.id_paciente}",
                        "instance": servico,
                    },
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = PacienteServicoForm(instance=servico)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "paciente_servico/_form_partial.html",
            {
                "form": form,
                "title": f"Editar {servico.id_paciente}",
                "instance": servico,
            },
        )

    return render(
        request,
        "paciente_servico/form.html",
        {"form": form, "title": f"Editar {servico.id_paciente}"},
    )
