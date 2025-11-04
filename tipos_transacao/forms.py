from django import forms

from .models import TipoTransacaoFinanceira


class TipoTransacaoForm(forms.ModelForm):
    class Meta:
        model = TipoTransacaoFinanceira
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "maxlength": 100})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "nome" in self.fields:
            self.fields["nome"].label = "Nome do tipo de transação"
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
