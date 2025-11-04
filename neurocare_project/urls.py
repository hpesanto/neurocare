import importlib
import logging

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import placeholders as project_placeholders
from . import views as project_views

# start urlpatterns and always-available routes
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", include("accounts.urls")),
]


def maybe_include(route, module_str, *args, **kwargs):
    """Append a path(route, include(module_str)) to urlpatterns if module is importable."""
    try:
        importlib.import_module(module_str)
    except Exception:
        logger = logging.getLogger(__name__)
        logger.debug("maybe_include: module not present: %s", module_str)
        return
    urlpatterns.append(path(route, include(module_str), *args, **kwargs))


# Conditional includes for app routes (safe to run even if apps are missing)
maybe_include("cadastro/pacientes/", "pacientes.urls")
maybe_include("cadastro/profissionais/", "profissionais.urls")
maybe_include("cadastro/usuarios/", "usuarios.urls")
maybe_include("cadastro/formas-pagamento/", "formas_pagamento.urls")
maybe_include("cadastro/tipos-produto/", "tipos_produto.urls")
maybe_include("cadastro/produtos/", "produtos.urls")
maybe_include("cadastro/convenios/", "convenios.urls")
maybe_include("cadastro/faixas-etarias/", "faixas.urls")
maybe_include("cadastro/contatos-emergencia/", "contatos_emergencia.urls")
maybe_include("cadastro/tipos-servico/", "tipos_servico.urls")
maybe_include("cadastro/paciente-servico/", "paciente_servico.urls")

maybe_include("atendimento/evolucao-clinica/", "evolucao_clinica.urls")
maybe_include(
    "atendimento/avaliacao-neuropsicologica/", "avaliacao_neuropsicologica.urls"
)
maybe_include(
    "atendimento/status-objetivo-reabilitacao/", "status_objetivo_reabilitacao.urls"
)
maybe_include("atendimento/objetivos-reabilitacao/", "reabilitacao_objetivo.urls")
# Sessões de reabilitação (app: reabilitacao_sessao)
maybe_include("atendimento/sessoes-reabilitacao/", "reabilitacao_sessao.urls")

maybe_include(
    "financeiro/reabilitacao-neuropsicologica/", "reabilitacao_neuropsicologica.urls"
)
maybe_include(
    "financeiro/formas-cobranca-reabilitacao/", "formas_cobranca_reabilitacao.urls"
)
maybe_include("financeiro/tipos-transacao/", "tipos_transacao.urls")
maybe_include("financeiro/status-pagamento/", "status_pagamento.urls")
maybe_include("financeiro/transacoes/", "transacoes.urls")

# VENDAS apps (include if present so named routes like vendas:list and vendas_geral:itens_list resolve)
maybe_include("vendas/vinculadas-paciente/", "vendas.urls")
maybe_include("vendas/geral/", "vendas_geral.urls")

# vendas/transacoes placeholders (used when apps are not present)
urlpatterns += [
    path(
        "financeiro/transacoes/",
        project_placeholders.placeholder,
        {"title": "Transações Financeiras"},
        name="financeiro_transacoes",
    ),
    path(
        "vendas/vinculadas-paciente/",
        project_placeholders.placeholder,
        {"title": "Vendas Vinculadas ao Paciente"},
        name="vendas_vinculadas_paciente",
    ),
    path(
        "vendas/geral/",
        project_placeholders.placeholder,
        {"title": "Vendas Gerais (Consultório)"},
        name="vendas_geral",
    ),
    path(
        "vendas/geral/itens/",
        project_placeholders.placeholder,
        {"title": "Itens de Venda Geral"},
        name="vendas_geral_itens",
    ),
    path(
        "agendamentos/",
        project_views.under_construction,
        {"title": "Agendamentos"},
        name="agendamentos",
    ),
]
