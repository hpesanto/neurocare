from django import forms

from pacientes.models import PacienteServico


class PacienteServicoForm(forms.ModelForm):
    class Meta:
        model = PacienteServico
        fields = [
            "id_paciente",
            "id_tipo_servico",
            "psicologo_responsavel_servico",
            "data_inicio",
            "data_fim",
            "ativo",
            "observacoes",
        ]
        widgets = {
            "id_paciente": forms.Select(attrs={"class": "form-control"}),
            "id_tipo_servico": forms.Select(attrs={"class": "form-control"}),
            "psicologo_responsavel_servico": forms.Select(
                attrs={"class": "form-control"}
            ),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
