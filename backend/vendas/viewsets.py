from rest_framework import viewsets

from .models import VendaVinculada
from .serializers import VendaVinculadaSerializer


class VendaVinculadaViewSet(viewsets.ModelViewSet):
    queryset = VendaVinculada.objects.select_related(
        "id_paciente", "id_produto"
    ).order_by("-data_venda")
    serializer_class = VendaVinculadaSerializer
    filterset_fields = ["id_paciente", "id_produto"]
