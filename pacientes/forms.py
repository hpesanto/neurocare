from django import forms

from .models import Paciente, Usuario


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nome_completo",
            "data_nascimento",
            "cpf",
            "rg",
            "genero",
            "estado_civil",
            "profissao",
            "telefone_principal",
            "telefone_secundario",
            "email",
            "endereco_rua",
            "endereco_numero",
            "endereco_complemento",
            "endereco_bairro",
            "endereco_cidade",
            "endereco_estado",
            "endereco_cep",
            "id_psicologo_responsavel",
            "quem_encaminhou",
            "motivo_encaminhamento",
            "id_convenio",
            "numero_carteirinha_convenio",
            "validade_carteirinha_convenio",
            "id_faixa_etaria",
            "status_paciente",
            "observacoes_gerais",
        ]
        widgets = {
            "nome_completo": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "rg": forms.TextInput(attrs={"class": "form-control"}),
            "genero": forms.Select(attrs={"class": "form-control"}),
            "estado_civil": forms.Select(attrs={"class": "form-control"}),
            "profissao": forms.TextInput(attrs={"class": "form-control"}),
            "telefone_principal": forms.TextInput(attrs={"class": "form-control"}),
            "telefone_secundario": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "endereco_rua": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_numero": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_complemento": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_bairro": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_cidade": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_estado": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_cep": forms.TextInput(attrs={"class": "form-control"}),
            "id_psicologo_responsavel": forms.Select(attrs={"class": "form-control"}),
            "quem_encaminhou": forms.TextInput(attrs={"class": "form-control"}),
            "motivo_encaminhamento": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "id_convenio": forms.Select(attrs={"class": "form-control"}),
            "numero_carteirinha_convenio": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "validade_carteirinha_convenio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "id_faixa_etaria": forms.Select(attrs={"class": "form-control"}),
            "status_paciente": forms.Select(attrs={"class": "form-control"}),
            "observacoes_gerais": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit psicologo_responsavel to active users (assuming Usuario has ativo field)
        self.fields["id_psicologo_responsavel"].queryset = Usuario.objects.filter(
            ativo=True
        )
        # Add empty choices for foreign keys
        self.fields["id_psicologo_responsavel"].empty_label = "Selecione um psicólogo"
        self.fields["id_convenio"].empty_label = "Selecione um convênio"
        self.fields["id_faixa_etaria"].empty_label = "Selecione uma faixa etária"
        # Ensure date inputs render in ISO format (YYYY-MM-DD) so
        # <input type="date"> displays the value correctly when editing.
        if "data_nascimento" in self.fields:
            self.fields["data_nascimento"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        if "validade_carteirinha_convenio" in self.fields:
            self.fields["validade_carteirinha_convenio"].input_formats = [
                "%Y-%m-%d",
                "%d/%m/%Y",
            ]
