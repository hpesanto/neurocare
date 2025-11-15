from django.contrib.auth.decorators import login_required

# ...existing code...
import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PacienteForm
from .models import Paciente


@login_required
def list_pacientes(request):
    # Some DB rows may have malformed values for array columns (e.g. `genero`) which raise
    # django.db.utils.DataError when Django tries to load them. We attempt the normal ORM
    # query first and fallback to a safe raw read that excludes the problematic column.
    from django.db import DataError, connection

    logger = logging.getLogger(__name__)

    # Debug: log search_path and whether tb_paciente exists in any schema using the
    # same DB connection that the server uses. This helps reproduce intermittent
    # "relation ... does not exist" errors.
    try:
        with connection.cursor() as debug_cursor:
            debug_cursor.execute("SHOW search_path;")
            sp = debug_cursor.fetchone()
            logger.info("DEBUG search_path: %s", sp)
            print("DEBUG search_path:", sp)
            debug_cursor.execute(
                "SELECT table_schema, table_name FROM information_schema.tables WHERE table_name = 'tb_paciente';"
            )
            tables = debug_cursor.fetchall()
            logger.info("DEBUG tables tb_paciente: %s", tables)
            print("DEBUG tables tb_paciente:", tables)
    except Exception as e:
        logger.exception("DEBUG error while checking search_path/tables: %s", e)

    try:
        # Use getattr to avoid static analyzers complaining that Paciente may lack 'objects'.
        # If getattr yields None (unexpected), fetch the model via apps.get_model and use its manager.
        objects_attr = getattr(Paciente, "objects", None)
        if objects_attr is None:
            from django.apps import apps

            objects_attr = apps.get_model("pacientes", "Paciente").objects

        qs = objects_attr.all().order_by("nome_completo")
        # Log the SQL that will be executed (lazy, but .query builds it)
        logger.info("DEBUG Paciente Query SQL: %s", str(qs.query))
        pacientes = list(qs)
    except DataError:
        # Fallback: read only safe columns via raw SQL and construct minimal model instances.
        # This avoids parsing the problematic array column.
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, nome_completo, cpf, telefone_principal, email FROM tb_paciente ORDER BY nome_completo"
            )
            rows = cursor.fetchall()

        pacientes = []
        for row in rows:
            # Create a lightweight Paciente instance without hitting DB for other fields
            p = Paciente()
            p.id = row[0]
            p.nome_completo = row[1]
            p.cpf = row[2]
            p.telefone_principal = row[3]
            p.email = row[4]
            # Ensure attributes accessed by templates exist to avoid AttributeError
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
            # If AJAX request, return JSON with rendered row HTML so client can insert it
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "pacientes/row.html", {"paciente": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("pacientes:list"))
        else:
            # Return JSON errors when AJAX
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "pacientes/_form_partial.html",
                    {"form": form, "title": "Novo Paciente"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = PacienteForm()
    # If AJAX GET (fetch) return the form partial so it can be rendered inside the modal
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "pacientes/_form_partial.html",
            {"form": form, "title": "Novo Paciente"},
        )

    return render(
        request, "pacientes/form.html", {"form": form, "title": "Novo Paciente"}
    )


@login_required
def update_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "pacientes/row.html", {"paciente": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("pacientes:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "pacientes/_form_partial.html",
                    {
                        "form": form,
                        "title": f"Editar {paciente.nome_completo}",
                        "instance": paciente,
                    },
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = PacienteForm(instance=paciente)
    # If this is an AJAX/fetch load request, return only the form partial
    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "pacientes/_form_partial.html",
            {
                "form": form,
                "title": f"Editar {paciente.nome_completo}",
                "instance": paciente,
            },
        )

    return render(
        request,
        "pacientes/form.html",
        {"form": form, "title": f"Editar {paciente.nome_completo}"},
    )
