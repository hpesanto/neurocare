from auditoria.mixins import AuditLogMixin
from rest_framework import viewsets

from .models import VendaGeral, VendaGeralItem
from .serializers import VendaGeralItemSerializer, VendaGeralSerializer


class VendaGeralViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = VendaGeral.objects.all().order_by("-data_venda")
    serializer_class = VendaGeralSerializer
    search_fields = ["nome_comprador"]


class VendaGeralItemViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = VendaGeralItem.objects.select_related("id_produto").order_by("-data_criacao")
    serializer_class = VendaGeralItemSerializer
    filterset_fields = ["id_venda_geral"]
