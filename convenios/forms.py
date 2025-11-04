from django import forms

from pacientes.models import Convenio


class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
        }
