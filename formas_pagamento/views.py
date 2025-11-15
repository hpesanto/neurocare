from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pacientes.models import FormaPagamento

from .forms import FormaPagamentoForm


@login_required
def list_formas(request):
    formas = FormaPagamento.objects.all().order_by("nome")
    form = FormaPagamentoForm()
    return render(
        request, "formas_pagamento/list.html", {"formas": formas, "form": form}
    )


@login_required
def create_forma(request):
    if request.method == "POST":
        form = FormaPagamentoForm(request.POST)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "formas_pagamento/row.html", {"forma": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("formas_pagamento:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "formas_pagamento/_form_partial.html",
                    {"form": form, "title": "Nova Forma de Pagamento"},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = FormaPagamentoForm()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "formas_pagamento/_form_partial.html",
            {"form": form, "title": "Nova Forma de Pagamento"},
        )

    return render(
        request,
        "formas_pagamento/form.html",
        {"form": form, "title": "Nova Forma de Pagamento"},
    )


@login_required
def update_forma(request, pk):
    forma = get_object_or_404(FormaPagamento, pk=pk)
    if request.method == "POST":
        form = FormaPagamentoForm(request.POST, instance=forma)
        if form.is_valid():
            saved = form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                row_html = render_to_string(
                    "formas_pagamento/row.html", {"forma": saved}, request=request
                )
                return JsonResponse({"ok": True, "row_html": row_html, "id": saved.id})
            return redirect(reverse("formas_pagamento:list"))
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                from django.http import JsonResponse
                from django.template.loader import render_to_string

                form_html = render_to_string(
                    "formas_pagamento/_form_partial.html",
                    {"form": form, "title": f"Editar {forma.nome}", "instance": forma},
                    request=request,
                )
                return JsonResponse({"ok": False, "form_html": form_html}, status=400)
    else:
        form = FormaPagamentoForm(instance=forma)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.accepts(
        "text/html"
    ):
        return render(
            request,
            "formas_pagamento/_form_partial.html",
            {"form": form, "title": f"Editar {forma.nome}", "instance": forma},
        )

    return render(
        request,
        "formas_pagamento/form.html",
        {"form": form, "title": f"Editar {forma.nome}"},
    )
