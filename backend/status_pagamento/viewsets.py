from rest_framework import viewsets

from .models import StatusPagamento
from .serializers import StatusPagamentoSerializer


class StatusPagamentoViewSet(viewsets.ModelViewSet):
    queryset = StatusPagamento.objects.all().order_by("nome")
    serializer_class = StatusPagamentoSerializer
    search_fields = ["nome"]
