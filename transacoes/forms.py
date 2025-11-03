from django import forms

from .models import TransacaoFinanceira


class TransacaoFinanceiraForm(forms.ModelForm):
    class Meta:
        model = TransacaoFinanceira
        fields = [
            "id_paciente",
            "id_psicologo",
            "id_tipo_transacao",
            "data_transacao",
            "valor",
            "id_forma_pagamento",
            "id_status_pagamento",
            "descricao",
            "cpf_pagador",
            "endereco_pagador",
            "email_pagador",
            "observacoes",
            "id_evolucao_clinica",
            "id_avaliacao_neuropsicologica",
            "id_reabilitacao_neuropsicologica",
            "id_reabilitacao_sessao",
            "id_venda_vinculada_paciente",
            "id_venda_geral",
        ]
        widgets = {
            "id_paciente": forms.Select(attrs={"class": "form-control"}),
            "id_psicologo": forms.Select(attrs={"class": "form-control"}),
            "id_tipo_transacao": forms.Select(attrs={"class": "form-control"}),
            "data_transacao": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "id_forma_pagamento": forms.Select(attrs={"class": "form-control"}),
            "id_status_pagamento": forms.Select(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "cpf_pagador": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_pagador": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "email_pagador": forms.EmailInput(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "id_evolucao_clinica": forms.Select(attrs={"class": "form-control"}),
            "id_avaliacao_neuropsicologica": forms.Select(
                attrs={"class": "form-control"}
            ),
            "id_reabilitacao_neuropsicologica": forms.Select(
                attrs={"class": "form-control"}
            ),
            "id_reabilitacao_sessao": forms.Select(attrs={"class": "form-control"}),
            "id_venda_vinculada_paciente": forms.Select(
                attrs={"class": "form-control"}
            ),
            "id_venda_geral": forms.Select(attrs={"class": "form-control"}),
        }
