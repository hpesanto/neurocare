from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from .models import StatusPagamento
from .serializers import StatusPagamentoSerializer


class StatusPagamentoViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = StatusPagamento.objects.all().order_by("nome")
    serializer_class = StatusPagamentoSerializer
    search_fields = ["nome"]
