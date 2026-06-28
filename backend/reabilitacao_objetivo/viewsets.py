from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from .models import ReabilitacaoObjetivo
from .serializers import ReabilitacaoObjetivoSerializer


class ReabilitacaoObjetivoViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = ReabilitacaoObjetivo.objects.select_related(
        "id_status_objetivo", "id_reabilitacao__id_paciente", "id_reabilitacao__id_psicologo"
    ).order_by("-data_criacao")
    serializer_class = ReabilitacaoObjetivoSerializer
    filterset_fields = ["id_reabilitacao", "id_status_objetivo"]
    audit_read = True  # Auditar leitura (LGPD)
