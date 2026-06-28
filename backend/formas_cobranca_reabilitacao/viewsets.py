from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from .models import FormaCobrancaReabilitacao
from .serializers import FormaCobrancaReabilitacaoSerializer


class FormaCobrancaReabilitacaoViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = FormaCobrancaReabilitacao.objects.all().order_by("nome")
    serializer_class = FormaCobrancaReabilitacaoSerializer
    search_fields = ["nome"]
