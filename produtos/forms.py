from django import forms

from pacientes.models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["id_tipo_produto", "nome", "descricao", "valor_unitario", "ativo"]
        widgets = {
            "id_tipo_produto": forms.Select(attrs={"class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "valor_unitario": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
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
