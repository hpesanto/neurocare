from django import forms

from .models import VendaGeral, VendaGeralItem


class VendaGeralItemForm(forms.ModelForm):
    class Meta:
        model = VendaGeralItem
        fields = [
            "id_venda_geral",
            "id_produto",
            "quantidade",
            "valor_unitario",
            "valor_total_item",
        ]
        widgets = {
            "id_venda_geral": forms.Select(attrs={"class": "form-control"}),
            "id_produto": forms.Select(attrs={"class": "form-control"}),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
            "valor_unitario": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "valor_total_item": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }

    def clean(self):
        cleaned = super().clean()
        quantidade = cleaned.get("quantidade")
        valor_unitario = cleaned.get("valor_unitario")
        if quantidade is not None and valor_unitario is not None:
            cleaned["valor_total_item"] = quantidade * valor_unitario
        return cleaned


class VendaGeralForm(forms.ModelForm):
    class Meta:
        model = VendaGeral
        fields = [
            "id_psicologo",
            "data_venda",
            "nome_comprador",
            "contato_comprador",
            "valor_total_transacao",
            "id_forma_pagamento",
            "observacoes",
        ]
        widgets = {
            "id_psicologo": forms.Select(attrs={"class": "form-control"}),
            "data_venda": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "nome_comprador": forms.TextInput(attrs={"class": "form-control"}),
            "contato_comprador": forms.TextInput(attrs={"class": "form-control"}),
            "valor_total_transacao": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "id_forma_pagamento": forms.Select(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id_psicologo"].empty_label = "Selecione um psicólogo"
        self.fields["id_forma_pagamento"].empty_label = (
            "Selecione uma forma de pagamento"
        )
        # Ensure descriptive fields use a larger textarea widget visually
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
