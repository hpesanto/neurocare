from rest_framework import serializers

from .models import ReabilitacaoNeuropsicologica


class ReabilitacaoNeuropsicologicaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )
    psicologo_nome = serializers.CharField(
        source="id_psicologo.nome_completo", read_only=True, default=None
    )
    display_label = serializers.SerializerMethodField()

    class Meta:
        model = ReabilitacaoNeuropsicologica
        fields = [
            "id", "id_paciente", "paciente_nome", "id_psicologo", "psicologo_nome",
            "display_label",
            "data_inicio", "data_fim_prevista", "programa_descricao",
            "num_sessoes_planejadas", "frequencia", "materiais_atividades_desc",
            "id_forma_cobranca", "valor_por_sessao", "valor_total_pacote",
            "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao", "display_label"]

    def get_display_label(self, obj):
        paciente = getattr(obj.id_paciente, "nome_completo", None) if obj.id_paciente else None
        desc = obj.programa_descricao[:40] if obj.programa_descricao else ""
        if paciente:
            return f"{paciente} — {desc}"
        return desc
