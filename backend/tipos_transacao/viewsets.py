from rest_framework import viewsets

from .models import TipoTransacaoFinanceira
from .serializers import TipoTransacaoFinanceiraSerializer


class TipoTransacaoFinanceiraViewSet(viewsets.ModelViewSet):
    queryset = TipoTransacaoFinanceira.objects.all().order_by("nome")
    serializer_class = TipoTransacaoFinanceiraSerializer
    search_fields = ["nome"]
