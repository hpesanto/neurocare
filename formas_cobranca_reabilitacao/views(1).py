from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms


class DummyFormaCobrancaForm(forms.Form):
    nome = forms.CharField(max_length=100, label="Nome")


def list_formas_cobranca(request):
    items = []
    return render(request, "formas_cobranca_reabilitacao/list.html", {"items": items})


def create_forma_cobranca(request):
    form = DummyFormaCobrancaForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": True, "row_html": "<tr><td>--</td><td></td></tr>", "id": "0"})
            return redirect("formas_cobranca_reabilitacao:list")
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "formas_cobranca_reabilitacao/_form_partial.html", {"form": form, "title": "Nova Forma", "action": request.path})
    return render(request, "formas_cobranca_reabilitacao/form.html", {"form": form, "title": "Nova Forma", "action": request.path})


def update_forma_cobranca(request, pk):
    form = DummyFormaCobrancaForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": True, "row_html": "<tr data-id=\"%s\"><td>%s</td><td></td></tr>" % (pk, form.cleaned_data.get('nome')), "id": str(pk)})
            return redirect("formas_cobranca_reabilitacao:list")
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "formas_cobranca_reabilitacao/_form_partial.html", {"form": form, "title": "Editar Forma", "action": request.path, "instance": None})
    return render(request, "formas_cobranca_reabilitacao/form.html", {"form": form, "title": "Editar Forma", "action": request.path, "instance": None})
