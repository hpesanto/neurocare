from rest_framework import serializers

from .models import ReabilitacaoSessao


class ReabilitacaoSessaoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_reabilitacao.id_paciente.nome_completo", read_only=True, default=None
    )
    profissional_nome = serializers.CharField(
        source="id_reabilitacao.id_psicologo.nome_completo", read_only=True, default=None
    )

    class Meta:
        model = ReabilitacaoSessao
        fields = [
            "id", "id_reabilitacao", "paciente_nome", "profissional_nome",
            "data_sessao", "hora_sessao",
            "passos_realizados", "proximos_passos_planejamento",
            "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
