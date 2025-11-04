from django import forms

from pacientes.models import FormaPagamento


class FormaPagamentoForm(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
        }
