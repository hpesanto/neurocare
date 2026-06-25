from rest_framework import serializers

from .models import EvolucaoClinica


class EvolucaoClinicaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )
    psicologo_nome = serializers.CharField(
        source="id_psicologo.nome_completo", read_only=True, default=None
    )

    class Meta:
        model = EvolucaoClinica
        fields = [
            "id", "id_paciente", "paciente_nome", "id_psicologo", "psicologo_nome",
            "data_sessao", "hora_sessao", "evolucao_texto",
            "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
