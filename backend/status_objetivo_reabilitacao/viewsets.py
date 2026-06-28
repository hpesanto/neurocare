from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from .models import StatusObjetivoReabilitacao
from .serializers import StatusObjetivoReabilitacaoSerializer


class StatusObjetivoReabilitacaoViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = StatusObjetivoReabilitacao.objects.all().order_by("nome")
    serializer_class = StatusObjetivoReabilitacaoSerializer
    search_fields = ["nome"]
