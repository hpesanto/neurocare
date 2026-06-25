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
