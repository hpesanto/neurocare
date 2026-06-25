from rest_framework import serializers

from .models import FormaCobrancaReabilitacao


class FormaCobrancaReabilitacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaCobrancaReabilitacao
        fields = ["id", "nome", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
