from rest_framework import viewsets

from .models import ReabilitacaoSessao
from .serializers import ReabilitacaoSessaoSerializer


class ReabilitacaoSessaoViewSet(viewsets.ModelViewSet):
    queryset = ReabilitacaoSessao.objects.all().order_by("-data_sessao", "-hora_sessao")
    serializer_class = ReabilitacaoSessaoSerializer
    filterset_fields = ["id_reabilitacao"]
