from django import forms

from .models import VendaVinculada


class VendaVinculadaForm(forms.ModelForm):
    class Meta:
        model = VendaVinculada
        fields = [
            "id_paciente",
            "id_psicologo",
            "id_produto",
            "data_venda",
            "quantidade",
            "valor_unitario",
            "valor_total_produto",
            "id_forma_pagamento",
            "observacoes",
        ]
        widgets = {
            "id_paciente": forms.Select(attrs={"class": "form-control"}),
            "id_psicologo": forms.Select(attrs={"class": "form-control"}),
            "id_produto": forms.Select(attrs={"class": "form-control"}),
            "data_venda": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "quantidade": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "valor_unitario": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "valor_total_produto": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "id_forma_pagamento": forms.Select(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id_paciente"].empty_label = "Selecione um paciente"
        self.fields["id_psicologo"].empty_label = "Selecione um psicólogo"
        self.fields["id_produto"].empty_label = "Selecione um produto"
        self.fields["id_forma_pagamento"].empty_label = (
            "Selecione uma forma de pagamento"
        )
