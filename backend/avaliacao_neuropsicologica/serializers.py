from rest_framework import serializers

from .models import AvaliacaoNeuropsicologica


class AvaliacaoNeuropsicologicaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )
    psicologo_nome = serializers.CharField(
        source="id_psicologo.nome_completo", read_only=True, default=None
    )

    class Meta:
        model = AvaliacaoNeuropsicologica
        fields = [
            "id", "id_paciente", "paciente_nome", "id_psicologo", "psicologo_nome",
            "data_avaliacao", "motivo_avaliacao", "instrumentos_utilizados",
            "valor_avaliacao", "hipoteses_diagnosticas", "resultados_principais",
            "conclusao_recomendacoes", "caminho_laudo_pdf",
            "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
