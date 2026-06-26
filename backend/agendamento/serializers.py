from rest_framework import serializers

from .models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    profissional_nome = serializers.CharField(
        source="id_profissional.nome_completo", read_only=True, default=None
    )
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )

    class Meta:
        model = Agendamento
        fields = [
            "id", "id_profissional", "profissional_nome",
            "id_paciente", "paciente_nome",
            "sala", "data", "hora_inicio", "hora_fim", "tipo",
            "observacoes", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]

    def validate(self, data):
        hora_inicio = data.get("hora_inicio", getattr(self.instance, "hora_inicio", None))
        hora_fim = data.get("hora_fim", getattr(self.instance, "hora_fim", None))
        sala = data.get("sala", getattr(self.instance, "sala", None))
        dia = data.get("data", getattr(self.instance, "data", None))

        if hora_inicio and hora_fim and hora_inicio >= hora_fim:
            raise serializers.ValidationError({"hora_fim": "Hora fim deve ser maior que hora inicio."})

        if sala and dia and hora_inicio and hora_fim:
            qs = Agendamento.objects.filter(
                sala=sala, data=dia,
                hora_inicio__lt=hora_fim,
                hora_fim__gt=hora_inicio,
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                conflito = qs.first()
                raise serializers.ValidationError({
                    "sala": f"Sala {sala} ja ocupada neste horario ({conflito.hora_inicio}-{conflito.hora_fim})."
                })

        return data
