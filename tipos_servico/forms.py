from django import forms

from pacientes.models import TipoServico


class TipoServicoForm(forms.ModelForm):
    class Meta:
        model = TipoServico
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
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
