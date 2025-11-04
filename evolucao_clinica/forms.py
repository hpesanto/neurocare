from django import forms

from .models import EvolucaoClinica


class EvolucaoClinicaForm(forms.ModelForm):
    class Meta:
        model = EvolucaoClinica
        fields = [
            "id_paciente",
            "id_psicologo",
            "data_sessao",
            "hora_sessao",
            "evolucao_texto",
        ]
        widgets = {
            "id_paciente": forms.Select(attrs={"class": "form-control"}),
            "id_psicologo": forms.Select(attrs={"class": "form-control"}),
            # ensure HTML5 inputs receive values in the expected formats when editing
            "data_sessao": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"class": "form-control", "type": "date"},
            ),
            "hora_sessao": forms.TimeInput(
                format="%H:%M",
                attrs={"class": "form-control", "type": "time"},
            ),
            "evolucao_texto": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Provide a friendly empty label for selects
        self.fields["id_paciente"].empty_label = "Selecione um paciente"
        self.fields["id_psicologo"].empty_label = "Selecione um psicólogo"
