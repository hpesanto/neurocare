from django import forms

from .models import StatusPagamento


class StatusPagamentoForm(forms.ModelForm):
    class Meta:
        model = StatusPagamento
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "maxlength": 50}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        if nome:
            return nome.strip()
        return nome
        return nome

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
