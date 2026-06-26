from rest_framework import viewsets

from neurocare_project.mixins import OwnPsicologoQuerysetMixin
from neurocare_project.permissions import IsPsicologaOrAdmin

from .models import ReabilitacaoNeuropsicologica
from .serializers import ReabilitacaoNeuropsicologicaSerializer


class ReabilitacaoNeuropsicologicaViewSet(OwnPsicologoQuerysetMixin, viewsets.ModelViewSet):
    queryset = ReabilitacaoNeuropsicologica.objects.select_related(
        "id_paciente", "id_psicologo", "id_forma_cobranca"
    ).order_by("-data_inicio")
    serializer_class = ReabilitacaoNeuropsicologicaSerializer
    permission_classes = [IsPsicologaOrAdmin]
    filterset_fields = ["id_paciente", "id_psicologo"]
