from django import forms

from .models import ReabilitacaoNeuropsicologica


class ReabilitacaoNeuropsicologicaForm(forms.ModelForm):
    class Meta:
        model = ReabilitacaoNeuropsicologica
        fields = [
            "id_paciente",
            "id_psicologo",
            "data_inicio",
            "data_fim_prevista",
            "programa_descricao",
            "num_sessoes_planejadas",
            "frequencia",
            "materiais_atividades_desc",
            "id_forma_cobranca",
            "valor_por_sessao",
            "valor_total_pacote",
        ]
        widgets = {
            "id_paciente": forms.Select(attrs={"class": "form-control"}),
            "id_psicologo": forms.Select(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim_prevista": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "programa_descricao": forms.Textarea(
                attrs={"class": "form-control large-textarea", "rows": 8}
            ),
            "num_sessoes_planejadas": forms.NumberInput(
                attrs={"class": "form-control", "type": "number"}
            ),
            "frequencia": forms.TextInput(attrs={"class": "form-control"}),
            "materiais_atividades_desc": forms.Textarea(
                attrs={"class": "form-control large-textarea", "rows": 8}
            ),
            "id_forma_cobranca": forms.Select(attrs={"class": "form-control"}),
            "valor_por_sessao": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "type": "number"}
            ),
            "valor_total_pacote": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "type": "number"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # friendly labels
        if "id_paciente" in self.fields:
            self.fields["id_paciente"].empty_label = "Selecione um paciente"
        if "id_psicologo" in self.fields:
            self.fields["id_psicologo"].empty_label = "Selecione um psicólogo"
        for fname, fld in self.fields.items():
            lname = fname.lower()
            if any(
                p in lname
                for p in (
                    "motivo",
                    "observ",
                    "resultado",
                    "conclus",
                    "instrument",
                    "hipotes",
                    "recomend",
                )
            ):
                attrs = getattr(fld.widget, "attrs", {})
                classes = attrs.get("class", "")
                if "large-textarea" not in classes:
                    attrs["class"] = (classes + " large-textarea").strip()
                attrs.setdefault("rows", "8")
