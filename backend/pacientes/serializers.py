from rest_framework import serializers

from .models import (
    Convenio,
    ContatoEmergencia,
    FaixaEtaria,
    FormaPagamento,
    Paciente,
    PacienteServico,
    Produto,
    TipoProduto,
    TipoServico,
    Usuario,
)


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nome_completo", "email", "login", "ativo", "data_criacao"]
        read_only_fields = ["id", "data_criacao"]


class ConvenioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convenio
        fields = ["id", "nome", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class FormaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = ["id", "nome", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class TipoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProduto
        fields = ["id", "nome", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class TipoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = ["id", "nome", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class FaixaEtariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaixaEtaria
        fields = ["id", "nome", "descricao", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class ProdutoSerializer(serializers.ModelSerializer):
    tipo_produto_nome = serializers.CharField(
        source="id_tipo_produto.nome", read_only=True, default=None
    )

    class Meta:
        model = Produto
        fields = [
            "id", "id_tipo_produto", "tipo_produto_nome", "nome", "descricao",
            "valor_unitario", "ativo", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class PacienteSerializer(serializers.ModelSerializer):
    psicologo_nome = serializers.CharField(
        source="id_psicologo_responsavel.nome_completo", read_only=True, default=None
    )
    convenio_nome = serializers.CharField(
        source="id_convenio.nome", read_only=True, default=None
    )
    faixa_etaria_nome = serializers.CharField(
        source="id_faixa_etaria.nome", read_only=True, default=None
    )

    class Meta:
        model = Paciente
        fields = "__all__"
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class ContatoEmergenciaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )

    class Meta:
        model = ContatoEmergencia
        fields = [
            "id", "id_paciente", "paciente_nome", "nome_contato",
            "telefone_contato", "parentesco", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class PacienteServicoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )
    servico_nome = serializers.CharField(
        source="id_tipo_servico.nome", read_only=True, default=None
    )

    class Meta:
        model = PacienteServico
        fields = [
            "id", "id_paciente", "paciente_nome", "id_tipo_servico", "servico_nome",
            "psicologo_responsavel_servico", "data_inicio", "data_fim", "ativo",
            "observacoes", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
