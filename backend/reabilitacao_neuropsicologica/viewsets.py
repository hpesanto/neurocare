from rest_framework import viewsets

from .models import ReabilitacaoNeuropsicologica
from .serializers import ReabilitacaoNeuropsicologicaSerializer


class ReabilitacaoNeuropsicologicaViewSet(viewsets.ModelViewSet):
    queryset = ReabilitacaoNeuropsicologica.objects.select_related(
        "id_paciente", "id_psicologo", "id_forma_cobranca"
    ).order_by("-data_inicio")
    serializer_class = ReabilitacaoNeuropsicologicaSerializer
    filterset_fields = ["id_paciente", "id_psicologo"]
