from django import forms

from .models import ReabilitacaoSessao


class ReabilitacaoSessaoForm(forms.ModelForm):
    class Meta:
        model = ReabilitacaoSessao
        fields = [
            "id_reabilitacao",
            "data_sessao",
            "hora_sessao",
            "passos_realizados",
            "proximos_passos_planejamento",
        ]
        widgets = {
            "id_reabilitacao": forms.Select(attrs={"class": "form-control"}),
            "data_sessao": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "hora_sessao": forms.TimeInput(
                format="%H:%M", attrs={"class": "form-control", "type": "time"}
            ),
            "passos_realizados": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "proximos_passos_planejamento": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # helpful empty label
        self.fields["id_reabilitacao"].empty_label = (
            "Selecione um plano de reabilitação"
        )
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
