from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from .models import Agendamento
from .serializers import AgendamentoSerializer


class AgendamentoViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = Agendamento.objects.select_related(
        "id_profissional", "id_paciente"
    ).order_by("data", "hora_inicio")
    serializer_class = AgendamentoSerializer
    filterset_fields = {
        "data": ["exact", "gte", "lte"],
        "sala": ["exact"],
        "id_profissional": ["exact"],
        "id_paciente": ["exact"],
    }
    search_fields = ["observacoes"]
