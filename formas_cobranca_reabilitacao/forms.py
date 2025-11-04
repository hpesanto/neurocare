from django import forms

from .models import FormaCobrancaReabilitacao


class FormaCobrancaReabilitacaoForm(forms.ModelForm):
    class Meta:
        model = FormaCobrancaReabilitacao
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "maxlength": 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "nome" in self.fields:
            self.fields["nome"].label = "Nome da forma de cobrança"
