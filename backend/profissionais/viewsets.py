from rest_framework import viewsets

from .models import PerfilAcesso, Profissional
from .serializers import PerfilAcessoSerializer, ProfissionalSerializer


class PerfilAcessoViewSet(viewsets.ModelViewSet):
    queryset = PerfilAcesso.objects.all().order_by("nome")
    serializer_class = PerfilAcessoSerializer
    search_fields = ["nome"]


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.select_related("id_perfil_acesso").order_by("nome")
    serializer_class = ProfissionalSerializer
    search_fields = ["nome", "email"]
    filterset_fields = ["ativo"]
