from django import forms

from .models import AvaliacaoNeuropsicologica


class AvaliacaoNeuropsicologicaForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoNeuropsicologica
        fields = [
            "id_paciente",
            "id_psicologo",
            "data_avaliacao",
            "motivo_avaliacao",
            "instrumentos_utilizados",
            "valor_avaliacao",
            "hipoteses_diagnosticas",
            "resultados_principais",
            "conclusao_recomendacoes",
            "caminho_laudo_pdf",
        ]
        widgets = {
            "id_paciente": forms.Select(attrs={"class": "form-control"}),
            "id_psicologo": forms.Select(attrs={"class": "form-control"}),
            "data_avaliacao": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "motivo_avaliacao": forms.Textarea(
                attrs={"class": "form-control large-textarea", "rows": 8}
            ),
            "instrumentos_utilizados": forms.Textarea(
                attrs={"class": "form-control large-textarea", "rows": 8}
            ),
            "valor_avaliacao": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "type": "number"}
            ),
            "hipoteses_diagnosticas": forms.Textarea(
                attrs={"class": "form-control large-textarea", "rows": 8}
            ),
            "resultados_principais": forms.Textarea(
                attrs={"class": "form-control large-textarea", "rows": 8}
            ),
            "conclusao_recomendacoes": forms.Textarea(
                attrs={"class": "form-control large-textarea", "rows": 8}
            ),
            "caminho_laudo_pdf": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Friendly empty labels
        self.fields["id_paciente"].empty_label = "Selecione um paciente"
        self.fields["id_psicologo"].empty_label = "Selecione um psicólogo"
