from rest_framework import serializers

from .models import ReabilitacaoObjetivo


class ReabilitacaoObjetivoSerializer(serializers.ModelSerializer):
    status_nome = serializers.CharField(
        source="id_status_objetivo.nome", read_only=True, default=None
    )

    class Meta:
        model = ReabilitacaoObjetivo
        fields = [
            "id", "id_reabilitacao", "descricao", "id_status_objetivo",
            "status_nome", "comentario_status", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
