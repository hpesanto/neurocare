from rest_framework import serializers

from .models import ReabilitacaoObjetivo


class ReabilitacaoObjetivoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_reabilitacao.id_paciente.nome_completo", read_only=True, default=None
    )
    profissional_nome = serializers.CharField(
        source="id_reabilitacao.id_psicologo.nome_completo", read_only=True, default=None
    )
    status_nome = serializers.CharField(
        source="id_status_objetivo.nome", read_only=True, default=None
    )

    class Meta:
        model = ReabilitacaoObjetivo
        fields = [
            "id", "id_reabilitacao", "paciente_nome", "profissional_nome",
            "descricao", "id_status_objetivo", "status_nome",
            "comentario_status", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
