from rest_framework import viewsets

from .models import EvolucaoClinica
from .serializers import EvolucaoClinicaSerializer


class EvolucaoClinicaViewSet(viewsets.ModelViewSet):
    queryset = EvolucaoClinica.objects.select_related(
        "id_paciente", "id_psicologo"
    ).order_by("-data_sessao", "-hora_sessao")
    serializer_class = EvolucaoClinicaSerializer
    filterset_fields = ["id_paciente", "id_psicologo"]
    search_fields = ["evolucao_texto"]
