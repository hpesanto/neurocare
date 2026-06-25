from rest_framework import viewsets

from .models import VendaGeral, VendaGeralItem
from .serializers import VendaGeralItemSerializer, VendaGeralSerializer


class VendaGeralViewSet(viewsets.ModelViewSet):
    queryset = VendaGeral.objects.all().order_by("-data_venda")
    serializer_class = VendaGeralSerializer
    search_fields = ["nome_comprador"]


class VendaGeralItemViewSet(viewsets.ModelViewSet):
    queryset = VendaGeralItem.objects.select_related("id_produto").order_by("-data_criacao")
    serializer_class = VendaGeralItemSerializer
    filterset_fields = ["id_venda_geral"]
