from django import forms

from pacientes.models import FaixaEtaria


class FaixaEtariaForm(forms.ModelForm):
    class Meta:
        model = FaixaEtaria
        fields = ["nome", "descricao"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
