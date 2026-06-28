from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from neurocare_project.mixins import OwnPsicologoQuerysetMixin
from neurocare_project.permissions import IsPsicologaOrAdmin

from .models import TransacaoFinanceira
from .serializers import TransacaoFinanceiraSerializer


class TransacaoFinanceiraViewSet(OwnPsicologoQuerysetMixin, viewsets.ModelViewSet):
    queryset = TransacaoFinanceira.objects.select_related(
        "id_paciente", "id_psicologo", "id_tipo_transacao",
        "id_forma_pagamento", "id_status_pagamento",
    ).order_by("-data_transacao")
    serializer_class = TransacaoFinanceiraSerializer
    permission_classes = [IsPsicologaOrAdmin]
    filterset_fields = {
        "id_paciente": ["exact"],
        "id_psicologo": ["exact"],
        "id_tipo_transacao": ["exact"],
        "id_status_pagamento": ["exact"],
        "data_transacao": ["exact", "gte", "lte"],
    }
    search_fields = ["descricao"]
