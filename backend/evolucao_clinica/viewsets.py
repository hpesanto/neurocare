from rest_framework import viewsets

from neurocare_project.mixins import OwnPsicologoQuerysetMixin
from neurocare_project.permissions import IsPsicologaOrAdmin

from .models import EvolucaoClinica
from .serializers import EvolucaoClinicaSerializer


class EvolucaoClinicaViewSet(OwnPsicologoQuerysetMixin, viewsets.ModelViewSet):
    queryset = EvolucaoClinica.objects.select_related(
        "id_paciente", "id_psicologo"
    ).order_by("-data_sessao", "-hora_sessao")
    serializer_class = EvolucaoClinicaSerializer
    permission_classes = [IsPsicologaOrAdmin]
    filterset_fields = {
        "id_paciente": ["exact"],
        "id_psicologo": ["exact"],
        "data_sessao": ["exact", "gte", "lte"],
    }
    search_fields = ["evolucao_texto"]
