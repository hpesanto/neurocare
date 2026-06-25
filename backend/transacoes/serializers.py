from rest_framework import serializers

from .models import TransacaoFinanceira


class TransacaoFinanceiraSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )
    psicologo_nome = serializers.CharField(
        source="id_psicologo.nome_completo", read_only=True, default=None
    )
    tipo_transacao_nome = serializers.CharField(
        source="id_tipo_transacao.nome", read_only=True, default=None
    )
    forma_pagamento_nome = serializers.CharField(
        source="id_forma_pagamento.nome", read_only=True, default=None
    )
    status_pagamento_nome = serializers.CharField(
        source="id_status_pagamento.nome", read_only=True, default=None
    )

    class Meta:
        model = TransacaoFinanceira
        fields = "__all__"
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
