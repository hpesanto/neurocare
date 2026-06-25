import logging

from django.contrib.auth.decorators import login_required
from django.db import DataError, connection
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from neurocare_project.crud_views import _is_ajax, _json_error, _json_success

from .forms import PacienteForm
from .models import Paciente

logger = logging.getLogger(__name__)

FORM_PARTIAL = "pacientes/_form_partial.html"
ROW_TEMPLATE = "pacientes/row.html"


@login_required
def list_pacientes(request):
    try:
        pacientes = list(Paciente.objects.all().order_by("nome_completo"))
    except DataError:
        # Fallback for rows with malformed array columns
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, nome_completo, cpf, telefone_principal, email "
                "FROM tb_paciente ORDER BY nome_completo"
            )
            rows = cursor.fetchall()
        pacientes = []
        for row in rows:
            p = Paciente()
            p.id, p.nome_completo, p.cpf, p.telefone_principal, p.email = row
            p.genero = None
            pacientes.append(p)

    form = PacienteForm()
    return render(
        request, "pacientes/list.html", {"pacientes": pacientes, "form": form}
    )


@login_required
def create_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if _is_ajax(request):
                return _json_success(request, saved, ROW_TEMPLATE, "paciente")
            return redirect(reverse("pacientes:list"))
        else:
            if _is_ajax(request):
                return _json_error(request, form, FORM_PARTIAL, "Novo Paciente")
    else:
        form = PacienteForm()

    if _is_ajax(request):
        return render(
            request, FORM_PARTIAL, {"form": form, "title": "Novo Paciente"}
        )
    return render(
        request, "pacientes/form.html", {"form": form, "title": "Novo Paciente"}
    )


@login_required
def update_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    title = f"Editar {paciente.nome_completo}"
    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            saved = form.save()
            if _is_ajax(request):
                return _json_success(request, saved, ROW_TEMPLATE, "paciente")
            return redirect(reverse("pacientes:list"))
        else:
            if _is_ajax(request):
                return _json_error(request, form, FORM_PARTIAL, title)
    else:
        form = PacienteForm(instance=paciente)

    if _is_ajax(request):
        return render(
            request,
            FORM_PARTIAL,
            {"form": form, "title": title, "instance": paciente},
        )
    return render(
        request, "pacientes/form.html", {"form": form, "title": title}
    )
