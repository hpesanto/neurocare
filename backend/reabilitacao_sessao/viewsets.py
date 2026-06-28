from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from .models import ReabilitacaoSessao
from .serializers import ReabilitacaoSessaoSerializer


class ReabilitacaoSessaoViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = ReabilitacaoSessao.objects.select_related(
        "id_reabilitacao__id_paciente", "id_reabilitacao__id_psicologo"
    ).order_by("-data_sessao", "-hora_sessao")
    serializer_class = ReabilitacaoSessaoSerializer
    filterset_fields = ["id_reabilitacao"]
