from rest_framework import viewsets

from .models import TransacaoFinanceira
from .serializers import TransacaoFinanceiraSerializer


class TransacaoFinanceiraViewSet(viewsets.ModelViewSet):
    queryset = TransacaoFinanceira.objects.select_related(
        "id_paciente", "id_psicologo", "id_tipo_transacao",
        "id_forma_pagamento", "id_status_pagamento",
    ).order_by("-data_transacao")
    serializer_class = TransacaoFinanceiraSerializer
    filterset_fields = ["id_paciente", "id_psicologo", "id_tipo_transacao", "id_status_pagamento"]
    search_fields = ["descricao"]
