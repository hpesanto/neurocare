from rest_framework import viewsets

from .models import StatusObjetivoReabilitacao
from .serializers import StatusObjetivoReabilitacaoSerializer


class StatusObjetivoReabilitacaoViewSet(viewsets.ModelViewSet):
    queryset = StatusObjetivoReabilitacao.objects.all().order_by("nome")
    serializer_class = StatusObjetivoReabilitacaoSerializer
    search_fields = ["nome"]
