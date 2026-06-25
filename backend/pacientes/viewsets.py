from rest_framework import viewsets

from .models import (
    Convenio,
    ContatoEmergencia,
    FaixaEtaria,
    FormaPagamento,
    Paciente,
    PacienteServico,
    Produto,
    TipoProduto,
    TipoServico,
    Usuario,
)
from .serializers import (
    ContatoEmergenciaSerializer,
    ConvenioSerializer,
    FaixaEtariaSerializer,
    FormaPagamentoSerializer,
    PacienteSerializer,
    PacienteServicoSerializer,
    ProdutoSerializer,
    TipoProdutoSerializer,
    TipoServicoSerializer,
    UsuarioSerializer,
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by("nome_completo")
    serializer_class = UsuarioSerializer
    search_fields = ["nome_completo", "email"]


class ConvenioViewSet(viewsets.ModelViewSet):
    queryset = Convenio.objects.all().order_by("nome")
    serializer_class = ConvenioSerializer
    search_fields = ["nome"]


class FormaPagamentoViewSet(viewsets.ModelViewSet):
    queryset = FormaPagamento.objects.all().order_by("nome")
    serializer_class = FormaPagamentoSerializer
    search_fields = ["nome"]


class TipoProdutoViewSet(viewsets.ModelViewSet):
    queryset = TipoProduto.objects.all().order_by("nome")
    serializer_class = TipoProdutoSerializer
    search_fields = ["nome"]


class TipoServicoViewSet(viewsets.ModelViewSet):
    queryset = TipoServico.objects.all().order_by("nome")
    serializer_class = TipoServicoSerializer
    search_fields = ["nome"]


class FaixaEtariaViewSet(viewsets.ModelViewSet):
    queryset = FaixaEtaria.objects.all().order_by("nome")
    serializer_class = FaixaEtariaSerializer
    search_fields = ["nome"]


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related("id_tipo_produto").order_by("nome")
    serializer_class = ProdutoSerializer
    search_fields = ["nome"]
    filterset_fields = ["ativo", "id_tipo_produto"]


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.select_related(
        "id_psicologo_responsavel", "id_convenio", "id_faixa_etaria"
    ).order_by("nome_completo")
    serializer_class = PacienteSerializer
    search_fields = ["nome_completo", "cpf", "email"]
    filterset_fields = ["status_paciente", "genero", "id_convenio"]


class ContatoEmergenciaViewSet(viewsets.ModelViewSet):
    queryset = ContatoEmergencia.objects.select_related("id_paciente").order_by("nome_contato")
    serializer_class = ContatoEmergenciaSerializer
    filterset_fields = ["id_paciente"]
    search_fields = ["nome_contato"]


class PacienteServicoViewSet(viewsets.ModelViewSet):
    queryset = PacienteServico.objects.select_related(
        "id_paciente", "id_tipo_servico"
    ).order_by("-data_inicio")
    serializer_class = PacienteServicoSerializer
    filterset_fields = ["id_paciente", "id_tipo_servico", "ativo"]
