from rest_framework import serializers

from .models import StatusObjetivoReabilitacao


class StatusObjetivoReabilitacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusObjetivoReabilitacao
        fields = ["id", "nome", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
