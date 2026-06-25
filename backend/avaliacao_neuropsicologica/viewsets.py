from rest_framework import viewsets

from .models import AvaliacaoNeuropsicologica
from .serializers import AvaliacaoNeuropsicologicaSerializer


class AvaliacaoNeuropsicologicaViewSet(viewsets.ModelViewSet):
    queryset = AvaliacaoNeuropsicologica.objects.select_related(
        "id_paciente", "id_psicologo"
    ).order_by("-data_avaliacao")
    serializer_class = AvaliacaoNeuropsicologicaSerializer
    filterset_fields = ["id_paciente", "id_psicologo"]
