from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from neurocare_project.mixins import OwnPsicologoQuerysetMixin
from neurocare_project.permissions import IsPsicologaOrAdmin

from .models import AvaliacaoNeuropsicologica
from .serializers import AvaliacaoNeuropsicologicaSerializer


class AvaliacaoNeuropsicologicaViewSet(OwnPsicologoQuerysetMixin, viewsets.ModelViewSet):
    queryset = AvaliacaoNeuropsicologica.objects.select_related(
        "id_paciente", "id_psicologo"
    ).order_by("-data_avaliacao")
    serializer_class = AvaliacaoNeuropsicologicaSerializer
    permission_classes = [IsPsicologaOrAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filterset_fields = ["id_paciente", "id_psicologo"]
