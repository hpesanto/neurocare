from django import forms
from django.http import JsonResponse
from django.shortcuts import redirect, render


class DummyFormaForm(forms.Form):
    nome = forms.CharField(max_length=100, label="Nome")


def list_formas(request):
    # Minimal safe implementation: provide empty list so template renders
    formas = []
    return render(request, "formas_pagamento/list.html", {"formas": formas})


def create_forma(request):
    form = DummyFormaForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # In this minimal placeholder we don't persist; redirect to list
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {"ok": True, "row_html": "<tr><td>--</td><td></td></tr>", "id": "0"}
                )
            return redirect("formas_pagamento:list")
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "formas_pagamento/_form_partial.html",
            {"form": form, "title": "Nova Forma", "action": request.path},
        )
    return render(
        request,
        "formas_pagamento/form.html",
        {"form": form, "title": "Nova Forma", "action": request.path},
    )


def update_forma(request, pk):
    form = DummyFormaForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "ok": True,
                        "row_html": '<tr data-id="%s"><td>%s</td><td></td></tr>'
                        % (pk, form.cleaned_data.get("nome")),
                        "id": str(pk),
                    }
                )
            return redirect("formas_pagamento:list")
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "formas_pagamento/_form_partial.html",
            {
                "form": form,
                "title": "Editar Forma",
                "action": request.path,
                "instance": None,
            },
        )
    return render(
        request,
        "formas_pagamento/form.html",
        {
            "form": form,
            "title": "Editar Forma",
            "action": request.path,
            "instance": None,
        },
    )
