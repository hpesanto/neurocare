from rest_framework import serializers

from .models import VendaGeral, VendaGeralItem


class VendaGeralItemSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(
        source="id_produto.nome", read_only=True, default=None
    )

    class Meta:
        model = VendaGeralItem
        fields = [
            "id", "id_venda_geral", "id_produto", "produto_nome",
            "quantidade", "valor_unitario", "valor_total_item", "data_criacao",
        ]
        read_only_fields = ["id", "data_criacao"]


class VendaGeralSerializer(serializers.ModelSerializer):
    itens = VendaGeralItemSerializer(source="vendageralitem_set", many=True, read_only=True)

    class Meta:
        model = VendaGeral
        fields = [
            "id", "id_psicologo", "data_venda", "nome_comprador",
            "contato_comprador", "valor_total_transacao", "id_forma_pagamento",
            "observacoes", "data_criacao", "data_atualizacao", "itens",
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
            id_psicologo_id=venda.id_psicologo_id if hasattr(venda, "id_psicologo_id") else None,
            id_tipo_transacao=tipo,
            data_transacao=venda.data_venda,
            valor=venda.valor_total_transacao,
            id_forma_pagamento=venda.id_forma_pagamento,
            id_status_pagamento=status,
            descricao=f"Venda geral: {venda.nome_comprador or 'Avulsa'} - R${venda.valor_total_transacao}",
            id_venda_geral=venda,
        )
