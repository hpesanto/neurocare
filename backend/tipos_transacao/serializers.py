from rest_framework import serializers

from .models import TipoTransacaoFinanceira


class TipoTransacaoFinanceiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTransacaoFinanceira
        fields = ["id", "nome", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
