from rest_framework import serializers

from .models import VendaVinculada


class VendaVinculadaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )
    produto_nome = serializers.CharField(
        source="id_produto.nome", read_only=True, default=None
    )

    class Meta:
        model = VendaVinculada
        fields = [
            "id", "id_paciente", "paciente_nome", "id_psicologo",
            "id_produto", "produto_nome", "data_venda", "quantidade",
            "valor_unitario", "valor_total_produto", "id_forma_pagamento",
            "observacoes", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
