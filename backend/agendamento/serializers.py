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

        if dia and hora_inicio and hora_fim:
            import datetime
            is_saturday = dia.weekday() == 5
            is_sunday = dia.weekday() == 6
            min_hour = datetime.time(7, 0)
            max_hour = datetime.time(12, 0) if is_saturday else datetime.time(20, 0)

            if is_sunday:
                raise serializers.ValidationError({"data": "Nao ha atendimento aos domingos."})
            if hora_inicio < min_hour:
                raise serializers.ValidationError({"hora_inicio": "Horario minimo: 07:00."})
            if hora_fim > max_hour:
                limit = "12:00" if is_saturday else "20:00"
                raise serializers.ValidationError({"hora_fim": f"Horario maximo {'no sabado' if is_saturday else ''}: {limit}."})

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
