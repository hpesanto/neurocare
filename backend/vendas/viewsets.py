from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from neurocare_project.mixins import OwnPsicologoQuerysetMixin
from neurocare_project.permissions import IsPsicologaOrAdmin

from .models import VendaVinculada
from .serializers import VendaVinculadaSerializer


class VendaVinculadaViewSet(OwnPsicologoQuerysetMixin, viewsets.ModelViewSet):
    queryset = VendaVinculada.objects.select_related(
        "id_paciente", "id_produto"
    ).order_by("-data_venda")
    serializer_class = VendaVinculadaSerializer
    permission_classes = [IsPsicologaOrAdmin]
    filterset_fields = {
        "id_paciente": ["exact"],
        "id_produto": ["exact"],
        "data_venda": ["exact", "gte", "lte"],
    }
    psicologo_fk_field = "id_psicologo"
