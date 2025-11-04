from django import forms

from .models import ReabilitacaoObjetivo


class ReabilitacaoObjetivoForm(forms.ModelForm):
    class Meta:
        model = ReabilitacaoObjetivo
        fields = [
            "id_reabilitacao",
            "descricao",
            "id_status_objetivo",
            "comentario_status",
        ]
        widgets = {
            "id_reabilitacao": forms.Select(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "id_status_objetivo": forms.Select(attrs={"class": "form-control"}),
            "comentario_status": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
