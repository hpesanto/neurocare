from django import forms

from pacientes.models import TipoProduto


class TipoProdutoForm(forms.ModelForm):
    class Meta:
        model = TipoProduto
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
        }
