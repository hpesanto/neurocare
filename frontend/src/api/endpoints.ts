export const ENDPOINTS = {
  // Auth
  token: "/token/",
  tokenRefresh: "/token/refresh/",

  // Cadastro
  pacientes: "/pacientes/",
  profissionais: "/profissionais/",
  usuarios: "/usuarios/",
  convenios: "/convenios/",
  formasPagamento: "/formas-pagamento/",
  tiposProduto: "/tipos-produto/",
  produtos: "/produtos/",
  faixasEtarias: "/faixas-etarias/",
  tiposServico: "/tipos-servico/",
  contatosEmergencia: "/contatos-emergencia/",
  pacienteServico: "/paciente-servico/",
  perfisAcesso: "/perfis-acesso/",

  // Atendimento
  evolucaoClinica: "/evolucao-clinica/",
  avaliacaoNeuropsicologica: "/avaliacao-neuropsicologica/",
  statusObjetivoReabilitacao: "/status-objetivo-reabilitacao/",
  reabilitacaoObjetivo: "/reabilitacao-objetivo/",
  reabilitacaoSessao: "/reabilitacao-sessao/",

  // Financeiro
  reabilitacaoNeuropsicologica: "/reabilitacao-neuropsicologica/",
  formasCobrancaReabilitacao: "/formas-cobranca-reabilitacao/",
  tiposTransacao: "/tipos-transacao/",
  statusPagamento: "/status-pagamento/",
  transacoes: "/transacoes/",

  // Vendas
  vendasVinculadas: "/vendas-vinculadas/",
  vendasGeral: "/vendas-geral/",
  vendasGeralItens: "/vendas-geral-itens/",
} as const;
