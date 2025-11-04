from django import forms

from pacientes.models import ContatoEmergencia


class ContatoEmergenciaForm(forms.ModelForm):
    class Meta:
        model = ContatoEmergencia
        fields = ["id_paciente", "nome_contato", "telefone_contato", "parentesco"]
        widgets = {
            "id_paciente": forms.Select(attrs={"class": "form-control"}),
            "nome_contato": forms.TextInput(attrs={"class": "form-control"}),
            "telefone_contato": forms.TextInput(attrs={"class": "form-control"}),
            "parentesco": forms.TextInput(attrs={"class": "form-control"}),
        }
