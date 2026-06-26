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

    def create(self, validated_data):
        venda = super().create(validated_data)
        self._create_transacao(venda)
        return venda

    def _create_transacao(self, venda):
        from status_pagamento.models import StatusPagamento
        from tipos_transacao.models import TipoTransacaoFinanceira
        from transacoes.models import TransacaoFinanceira

        tipo = TipoTransacaoFinanceira.objects.filter(nome__icontains="produto").first()
        if not tipo:
            tipo = TipoTransacaoFinanceira.objects.first()
        status = StatusPagamento.objects.filter(nome__icontains="pago").exclude(nome__icontains="parcial").first()
        if not status:
            status = StatusPagamento.objects.first()
        if not tipo or not status:
            return

        TransacaoFinanceira.objects.create(
            id_paciente=venda.id_paciente,
            id_psicologo_id=venda.id_psicologo_id if hasattr(venda, "id_psicologo_id") else None,
            id_tipo_transacao=tipo,
            data_transacao=venda.data_venda,
            valor=venda.valor_total_produto,
            id_forma_pagamento=venda.id_forma_pagamento,
            id_status_pagamento=status,
            descricao=f"Venda: {venda.id_produto} x{venda.quantidade}",
            id_venda_vinculada_paciente=venda,
        )
