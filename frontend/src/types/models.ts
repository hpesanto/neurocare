export interface LookupItem {
  id: string;
  nome: string;
  data_criacao: string;
  data_atualizacao: string;
}

export interface Paciente {
  id: string;
  nome_completo: string;
  data_nascimento: string;
  cpf: string | null;
  rg: string | null;
  genero: string;
  estado_civil: string;
  profissao: string | null;
  telefone_principal: string;
  telefone_secundario: string | null;
  email: string | null;
  endereco_rua: string | null;
  endereco_numero: string | null;
  endereco_complemento: string | null;
  endereco_bairro: string | null;
  endereco_cidade: string | null;
  endereco_estado: string | null;
  endereco_cep: string | null;
  id_psicologo_responsavel: string | null;
  psicologo_nome: string | null;
  quem_encaminhou: string | null;
  motivo_encaminhamento: string | null;
  id_convenio: string | null;
  convenio_nome: string | null;
  numero_carteirinha_convenio: string | null;
  validade_carteirinha_convenio: string | null;
  id_faixa_etaria: string | null;
  faixa_etaria_nome: string | null;
  status_paciente: string;
  observacoes_gerais: string | null;
  data_criacao: string;
  data_atualizacao: string;
}

export interface Profissional {
  id: string;
  id_perfil_acesso: string;
  perfil_acesso_nome: string | null;
  nome: string;
  email: string;
  login: string;
  ativo: boolean;
  data_criacao: string;
  data_atualizacao: string;
}

export interface EvolucaoClinica {
  id: string;
  id_paciente: string;
  paciente_nome: string | null;
  id_psicologo: string;
  psicologo_nome: string | null;
  data_sessao: string;
  hora_sessao: string | null;
  evolucao_texto: string;
  data_criacao: string;
  data_atualizacao: string;
}

export interface TransacaoFinanceira {
  id: string;
  id_paciente: string | null;
  paciente_nome: string | null;
  id_psicologo: string | null;
  psicologo_nome: string | null;
  id_tipo_transacao: string;
  tipo_transacao_nome: string | null;
  data_transacao: string;
  valor: string;
  id_forma_pagamento: string;
  forma_pagamento_nome: string | null;
  id_status_pagamento: string;
  status_pagamento_nome: string | null;
  descricao: string;
  data_criacao: string;
  data_atualizacao: string;
}
