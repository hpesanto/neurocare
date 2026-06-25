from rest_framework import serializers

from .models import StatusPagamento


class StatusPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusPagamento
        fields = ["id", "nome", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
