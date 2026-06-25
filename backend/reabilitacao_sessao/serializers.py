from rest_framework import serializers

from .models import ReabilitacaoSessao


class ReabilitacaoSessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReabilitacaoSessao
        fields = [
            "id", "id_reabilitacao", "data_sessao", "hora_sessao",
            "passos_realizados", "proximos_passos_planejamento",
            "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
