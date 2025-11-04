# Menu configuration: edit this file to add menu items.
# Each item is a dict with: 'title', 'url' and optional 'permissions' (list of permission strings)

# This is a draft menu generated from the proposed evolution. Each database table
# described in the proposal was mapped to one menu item. URLs and permission
# strings follow a reasonable convention but may need to be adjusted to match
# actual view names and app labels in the project.

MENU = [
    {"title": "Home", "url": "/"},
    # CADASTRO group (lookup and master data)
    {
        "title": "Cadastro",
        "url": "#",
        "permissions": ["accounts.view_paciente"],
        "children": [
            {
                "title": "Formas de Pagamento",
                "url": "/cadastro/formas-pagamento/",
                "permissions": ["financeiro.view_formapagamento"],
            },
            {
                "title": "Tipos de Produto",
                "url": "/cadastro/tipos-produto/",
                "permissions": ["vendas.view_tipoproduto"],
            },
            {
                "title": "Produtos",
                "url": "/cadastro/produtos/",
                "permissions": ["vendas.view_produto"],
            },
            {
                "title": "Usuários",
                "url": "/cadastro/usuarios/",
                "permissions": ["auth.view_user"],
            },
            {
                "title": "Convênios",
                "url": "/cadastro/convenios/",
                "permissions": ["pacientes.view_convenio"],
            },
            {
                "title": "Faixas Etárias",
                "url": "/cadastro/faixas-etarias/",
                "permissions": ["pacientes.view_faixaetaria"],
            },
            {
                "title": "Pacientes",
                "url": "/cadastro/pacientes/",
                "permissions": ["pacientes.view_paciente"],
            },
            {
                "title": "Contatos de Emergência",
                "url": "/cadastro/contatos-emergencia/",
                "permissions": ["pacientes.view_contatoemergencia"],
            },
            {
                "title": "Tipos de Serviço",
                "url": "/cadastro/tipos-servico/",
                "permissions": ["atendimento.view_tiposervico"],
            },
            {
                "title": "Paciente x Serviço (Ativo)",
                "url": "/cadastro/paciente-servico/",
                "permissions": ["pacientes.view_pacienteservico"],
            },
        ],
    },
    # ATENDIMENTO group (clinical records and rehabilitation)
    {
        "title": "Atendimento",
        "url": "#",
        "permissions": ["atendimento.view_evolucao_clinica"],
        "children": [
            {
                "title": "Evolução Clínica",
                "url": "/atendimento/evolucao-clinica/",
                "permissions": ["atendimento.view_evolucaoclinica"],
            },
            {
                "title": "Avaliação Neuropsicológica",
                "url": "/atendimento/avaliacao-neuropsicologica/",
                "permissions": ["atendimento.view_avaliacaoneuropsicologica"],
            },
            {
                "title": "Status Objetivo Reabilitação",
                "url": "/atendimento/status-objetivo-reabilitacao/",
                "permissions": ["reabilitacao.view_statusobjetivo"],
            },
            {
                "title": "Objetivos da Reabilitação",
                "url": "/atendimento/objetivos-reabilitacao/",
                "permissions": ["reabilitacao_objetivo.view_reabilitacaoobjetivo"],
            },
            {
                "title": "Sessões de Reabilitação",
                "url": "/atendimento/sessoes-reabilitacao/",
                # permission corrected to match app label and model name
                # model: ReabilitacaoSessao in app reabilitacao_sessao => permission codename: view_reabilitacaosessao
                "permissions": ["reabilitacao_sessao.view_reabilitacaosessao"],
            },
        ],
    },
    # FINANCEIRO group
    {
        "title": "Financeiro",
        "url": "#",
        "permissions": ["financeiro.view_transacao_financeira"],
        "children": [
            {
                "title": "Formas de Cobrança (Reabilitação)",
                "url": "/financeiro/formas-cobranca-reabilitacao/",
                "permissions": ["financeiro.view_formacobranca"],
            },
            {
                "title": "Reabilitação Neuropsicológica",
                "url": "/financeiro/reabilitacao-neuropsicologica/",
                "permissions": ["financeiro.view_reabilitacao"],
            },
            {
                "title": "Tipos de Transação",
                "url": "/financeiro/tipos-transacao/",
                "permissions": ["financeiro.view_tipotransacao"],
            },
            {
                "title": "Status de Pagamento",
                "url": "/financeiro/status-pagamento/",
                "permissions": ["financeiro.view_statuspagamento"],
            },
            {
                "title": "Transações Financeiras",
                "url": "/financeiro/transacoes/",
                "permissions": ["financeiro.view_transacao_financeira"],
            },
        ],
    },
    # VENDAS group
    {
        "title": "Vendas",
        "url": "#",
        "permissions": ["vendas.view_venda"],
        "children": [
            {
                "title": "Vendas Vinculadas ao Paciente",
                "url": "/vendas/vinculadas-paciente/",
                # permission adjusted to match model class name VendaVinculada -> permission codename 'view_vendavinculada'
                "permissions": ["vendas.view_vendavinculada"],
            },
            {
                "title": "Vendas Gerais (Consultório)",
                "url": "/vendas/geral/",
                # model: VendaGeral in app vendas_geral => permission codename view_vendageral
                "permissions": ["vendas_geral.view_vendageral"],
            },
            {
                "title": "Itens de Venda Geral",
                "url": "/vendas/geral/itens/",
                "permissions": ["vendas_geral.view_vendageralitem"],
            },
        ],
    },
    # keep Agendamentos if present in system
    {
        "title": "Agendamentos",
        "url": "/agendamentos/",
        "permissions": ["accounts.view_agendamento"],
    },
]
