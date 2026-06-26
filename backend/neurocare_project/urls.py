from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .permissions import get_perfil_nome, get_profissional


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    prof = get_profissional(user)
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "perfil": get_perfil_nome(user),
        "profissional_id": str(prof.id) if prof else None,
    })

from avaliacao_neuropsicologica.viewsets import AvaliacaoNeuropsicologicaViewSet
from evolucao_clinica.viewsets import EvolucaoClinicaViewSet
from formas_cobranca_reabilitacao.viewsets import FormaCobrancaReabilitacaoViewSet
from pacientes.viewsets import (
    ContatoEmergenciaViewSet,
    ConvenioViewSet,
    FaixaEtariaViewSet,
    FormaPagamentoViewSet,
    PacienteServicoViewSet,
    PacienteViewSet,
    ProdutoViewSet,
    TipoProdutoViewSet,
    TipoServicoViewSet,
    UsuarioViewSet,
)
from profissionais.viewsets import PerfilAcessoViewSet, ProfissionalViewSet
from reabilitacao_neuropsicologica.viewsets import ReabilitacaoNeuropsicologicaViewSet
from reabilitacao_objetivo.viewsets import ReabilitacaoObjetivoViewSet
from reabilitacao_sessao.viewsets import ReabilitacaoSessaoViewSet
from status_objetivo_reabilitacao.viewsets import StatusObjetivoReabilitacaoViewSet
from status_pagamento.viewsets import StatusPagamentoViewSet
from tipos_transacao.viewsets import TipoTransacaoFinanceiraViewSet
from transacoes.viewsets import TransacaoFinanceiraViewSet
from vendas.viewsets import VendaVinculadaViewSet
from transacoes.export_view import exportar_transacoes
from vendas_geral.viewsets import VendaGeralItemViewSet, VendaGeralViewSet

router = DefaultRouter()

# Cadastro
router.register(r"pacientes", PacienteViewSet)
router.register(r"profissionais", ProfissionalViewSet)
router.register(r"usuarios", UsuarioViewSet)
router.register(r"convenios", ConvenioViewSet)
router.register(r"formas-pagamento", FormaPagamentoViewSet)
router.register(r"tipos-produto", TipoProdutoViewSet)
router.register(r"produtos", ProdutoViewSet)
router.register(r"faixas-etarias", FaixaEtariaViewSet)
router.register(r"tipos-servico", TipoServicoViewSet)
router.register(r"contatos-emergencia", ContatoEmergenciaViewSet)
router.register(r"paciente-servico", PacienteServicoViewSet)
router.register(r"perfis-acesso", PerfilAcessoViewSet)

# Atendimento
router.register(r"evolucao-clinica", EvolucaoClinicaViewSet)
router.register(r"avaliacao-neuropsicologica", AvaliacaoNeuropsicologicaViewSet)
router.register(r"status-objetivo-reabilitacao", StatusObjetivoReabilitacaoViewSet)
router.register(r"reabilitacao-objetivo", ReabilitacaoObjetivoViewSet)
router.register(r"reabilitacao-sessao", ReabilitacaoSessaoViewSet)

# Financeiro
router.register(r"reabilitacao-neuropsicologica", ReabilitacaoNeuropsicologicaViewSet)
router.register(r"formas-cobranca-reabilitacao", FormaCobrancaReabilitacaoViewSet)
router.register(r"tipos-transacao", TipoTransacaoFinanceiraViewSet)
router.register(r"status-pagamento", StatusPagamentoViewSet)
router.register(r"transacoes", TransacaoFinanceiraViewSet)

# Vendas
router.register(r"vendas-vinculadas", VendaVinculadaViewSet)
router.register(r"vendas-geral", VendaGeralViewSet)
router.register(r"vendas-geral-itens", VendaGeralItemViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/me/", current_user, name="current_user"),
    path("api/transacoes/exportar/", exportar_transacoes, name="exportar_transacoes"),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
