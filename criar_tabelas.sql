-- ============================================================================
-- NeuroCare - Script de Criação de Tabelas
-- ============================================================================
-- Este script cria todas as tabelas da aplicação NeuroCare no PostgreSQL.
-- 
-- Uso:
--   psql -U postgres -d neurocare -f criar_tabelas.sql
--
-- Pré-requisitos:
--   - PostgreSQL 12+ instalado e rodando
--   - Banco de dados 'neurocare' já criado
--   - Schema 'neurocare' deve existir (use setup_database.sql antes)
-- ============================================================================

-- Define o schema neurocare como padrão para as operações seguintes
SET search_path TO neurocare;

-- Extensão necessária para gerar UUIDs aleatórios
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 1. TABELAS DE LOOKUP (Valores padrão do sistema)
-- ============================================================================

-- Tabela de Perfis de Acesso
CREATE TABLE IF NOT EXISTS tb_perfil_acesso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Convênios
CREATE TABLE IF NOT EXISTS tb_convenio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Faixas Etárias
CREATE TABLE IF NOT EXISTS tb_faixa_etaria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Tipos de Serviço
CREATE TABLE IF NOT EXISTS tb_tipo_servico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Formas de Cobrança da Reabilitação
CREATE TABLE IF NOT EXISTS tb_forma_cobranca_reabilitacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Status do Objetivo da Reabilitação
CREATE TABLE IF NOT EXISTS tb_status_objetivo_reabilitacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Tipos de Transação Financeira
CREATE TABLE IF NOT EXISTS tb_tipo_transacao_financeira (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Formas de Pagamento
CREATE TABLE IF NOT EXISTS tb_forma_pagamento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Status de Pagamento
CREATE TABLE IF NOT EXISTS tb_status_pagamento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Tipos de Produto
CREATE TABLE IF NOT EXISTS tb_tipo_produto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 2. TABELAS PRINCIPAIS
-- ============================================================================

-- Tabela de Usuários (Profissionais)
CREATE TABLE IF NOT EXISTS tb_usuario (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_perfil_acesso UUID NOT NULL REFERENCES tb_perfil_acesso(id),
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    login VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usuario_email ON tb_usuario (email);
CREATE INDEX IF NOT EXISTS idx_usuario_login ON tb_usuario (login);
CREATE INDEX IF NOT EXISTS idx_usuario_id_perfil_acesso ON tb_usuario (id_perfil_acesso);

-- Tabela de Pacientes
CREATE TABLE IF NOT EXISTS tb_paciente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    rg VARCHAR(20),
    genero VARCHAR(50) NOT NULL CHECK (genero IN ('Masculino', 'Feminino', 'Outro', 'Não Informar')),
    estado_civil VARCHAR(50) NOT NULL CHECK (estado_civil IN ('Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'União Estável')),
    profissao VARCHAR(100),
    telefone_principal VARCHAR(20) NOT NULL,
    telefone_secundario VARCHAR(20),
    email VARCHAR(255),
    endereco_rua VARCHAR(255),
    endereco_numero VARCHAR(50),
    endereco_complemento VARCHAR(100),
    endereco_bairro VARCHAR(100),
    endereco_cidade VARCHAR(100),
    endereco_estado VARCHAR(50),
    endereco_cep VARCHAR(10),
    id_psicologo_responsavel UUID REFERENCES tb_usuario(id),
    quem_encaminhou VARCHAR(255),
    motivo_encaminhamento TEXT,
    id_convenio UUID REFERENCES tb_convenio(id),
    numero_carteirinha_convenio VARCHAR(100),
    validade_carteirinha_convenio DATE,
    id_faixa_etaria UUID REFERENCES tb_faixa_etaria(id),
    status_paciente VARCHAR(50) NOT NULL CHECK (status_paciente IN ('Ativo', 'Inativo', 'Alta', 'Em Espera')),
    observacoes_gerais TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_paciente_cpf ON tb_paciente (cpf);
CREATE INDEX IF NOT EXISTS idx_paciente_nome_completo ON tb_paciente (nome_completo);
CREATE INDEX IF NOT EXISTS idx_paciente_psicologo_responsavel ON tb_paciente (id_psicologo_responsavel);

-- Tabela de Contatos de Emergência
CREATE TABLE IF NOT EXISTS tb_contato_emergencia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    nome_contato VARCHAR(255) NOT NULL,
    telefone_contato VARCHAR(20) NOT NULL,
    parentesco VARCHAR(100) NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Paciente x Serviço
CREATE TABLE IF NOT EXISTS tb_paciente_servico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_tipo_servico UUID NOT NULL REFERENCES tb_tipo_servico(id),
    psicologo_responsavel_servico UUID REFERENCES tb_usuario(id),
    data_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    data_fim DATE,
    ativo BOOLEAN DEFAULT TRUE,
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_paciente, id_tipo_servico)
);

-- ============================================================================
-- 3. TABELAS DE EVOLUÇÃO CLÍNICA E AVALIAÇÕES
-- ============================================================================

-- Tabela de Evolução Clínica
CREATE TABLE IF NOT EXISTS tb_evolucao_clinica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id),
    data_sessao DATE NOT NULL,
    hora_sessao TIME,
    evolucao_texto TEXT NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evolucao_clinica_paciente_data ON tb_evolucao_clinica (id_paciente, data_sessao);

-- Tabela de Avaliação Neuropsicológica
CREATE TABLE IF NOT EXISTS tb_avaliacao_neuropsicologica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id),
    data_avaliacao DATE NOT NULL,
    motivo_avaliacao TEXT NOT NULL,
    instrumentos_utilizados TEXT,
    valor_avaliacao NUMERIC(10, 2),
    hipoteses_diagnosticas TEXT,
    resultados_principais TEXT,
    conclusao_recomendacoes TEXT,
    caminho_laudo_pdf VARCHAR(255),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_avaliacao_neuropsicologica_paciente ON tb_avaliacao_neuropsicologica (id_paciente);

-- ============================================================================
-- 4. TABELAS DE REABILITAÇÃO
-- ============================================================================

-- Tabela de Reabilitação Neuropsicológica
CREATE TABLE IF NOT EXISTS tb_reabilitacao_neuropsicologica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id),
    data_inicio DATE NOT NULL,
    data_fim_prevista DATE,
    programa_descricao TEXT NOT NULL,
    num_sessoes_planejadas INTEGER,
    frequencia VARCHAR(100),
    materiais_atividades_desc TEXT,
    id_forma_cobranca UUID REFERENCES tb_forma_cobranca_reabilitacao(id),
    valor_por_sessao NUMERIC(10, 2),
    valor_total_pacote NUMERIC(10, 2),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reabilitacao_neuropsicologica_paciente ON tb_reabilitacao_neuropsicologica (id_paciente);

-- Tabela de Objetivos da Reabilitação
CREATE TABLE IF NOT EXISTS tb_reabilitacao_objetivo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_reabilitacao UUID NOT NULL REFERENCES tb_reabilitacao_neuropsicologica(id),
    descricao TEXT NOT NULL,
    id_status_objetivo UUID REFERENCES tb_status_objetivo_reabilitacao(id),
    comentario_status TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Sessões de Reabilitação
CREATE TABLE IF NOT EXISTS tb_reabilitacao_sessao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_reabilitacao UUID NOT NULL REFERENCES tb_reabilitacao_neuropsicologica(id),
    data_sessao DATE NOT NULL,
    hora_sessao TIME,
    passos_realizados TEXT NOT NULL,
    proximos_passos_planejamento TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 5. TABELAS DE VENDAS E PRODUTOS
-- ============================================================================

-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS tb_produto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_tipo_produto UUID REFERENCES tb_tipo_produto(id),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    valor_unitario NUMERIC(10, 2) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_produto_nome ON tb_produto (nome);

-- Tabela de Vendas Vinculadas ao Paciente
CREATE TABLE IF NOT EXISTS tb_venda_vinculada_paciente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_psicologo UUID REFERENCES tb_usuario(id),
    id_produto UUID NOT NULL REFERENCES tb_produto(id),
    data_venda DATE NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario NUMERIC(10, 2) NOT NULL,
    valor_total_produto NUMERIC(10, 2) NOT NULL,
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id),
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_venda_vinculada_paciente ON tb_venda_vinculada_paciente (id_paciente);

-- Tabela de Vendas Gerais
CREATE TABLE IF NOT EXISTS tb_venda_geral (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_psicologo UUID REFERENCES tb_usuario(id),
    data_venda DATE NOT NULL,
    nome_comprador VARCHAR(255),
    contato_comprador VARCHAR(255),
    valor_total_transacao NUMERIC(10, 2) NOT NULL,
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id),
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_venda_geral_data ON tb_venda_geral (data_venda);

-- Tabela de Itens de Venda Geral
CREATE TABLE IF NOT EXISTS tb_venda_geral_item (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_venda_geral UUID NOT NULL REFERENCES tb_venda_geral(id),
    id_produto UUID NOT NULL REFERENCES tb_produto(id),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario NUMERIC(10, 2) NOT NULL,
    valor_total_item NUMERIC(10, 2) NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 6. TABELAS DE TRANSAÇÕES FINANCEIRAS
-- ============================================================================

-- Tabela de Transações Financeiras
CREATE TABLE IF NOT EXISTS tb_transacao_financeira (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID REFERENCES tb_paciente(id),
    id_psicologo UUID REFERENCES tb_usuario(id),
    id_tipo_transacao UUID NOT NULL REFERENCES tb_tipo_transacao_financeira(id),
    data_transacao DATE NOT NULL,
    valor NUMERIC(10, 2) NOT NULL CHECK (valor >= 0),
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id),
    id_status_pagamento UUID NOT NULL REFERENCES tb_status_pagamento(id),
    descricao TEXT NOT NULL,
    cpf_pagador VARCHAR(14),
    endereco_pagador TEXT,
    email_pagador VARCHAR(255),
    observacoes TEXT,
    id_evolucao_clinica UUID REFERENCES tb_evolucao_clinica(id),
    id_avaliacao_neuropsicologica UUID REFERENCES tb_avaliacao_neuropsicologica(id),
    id_reabilitacao_neuropsicologica UUID REFERENCES tb_reabilitacao_neuropsicologica(id),
    id_reabilitacao_sessao UUID REFERENCES tb_reabilitacao_sessao(id),
    id_venda_vinculada_paciente UUID REFERENCES tb_venda_vinculada_paciente(id),
    id_venda_geral UUID REFERENCES tb_venda_geral(id),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_transacao_financeira_paciente ON tb_transacao_financeira (id_paciente);
CREATE INDEX IF NOT EXISTS idx_transacao_financeira_data ON tb_transacao_financeira (data_transacao);
CREATE INDEX IF NOT EXISTS idx_transacao_financeira_psicologo ON tb_transacao_financeira (id_psicologo);

-- ============================================================================
-- 7. INSERÇÃO DE DADOS INICIAIS (LOOKUP TABLES)
-- ============================================================================

-- Perfis de Acesso
INSERT INTO tb_perfil_acesso (nome, descricao) VALUES
('Administrador', 'Acesso total ao sistema e gestão de usuários.'),
('Psicologa', 'Acesso aos dados de seus próprios pacientes e gestão financeira vinculada.'),
('Secretaria', 'Acesso básico a cadastros de pacientes e início de registros de vendas.')
ON CONFLICT (nome) DO NOTHING;

-- Faixas Etárias
INSERT INTO tb_faixa_etaria (nome, descricao) VALUES
('Crianca (0-12 anos)', 'Pacientes com idade entre 0 e 12 anos.'),
('Adolescente (13-18 anos)', 'Pacientes com idade entre 13 e 18 anos.'),
('Adulto (19-59 anos)', 'Pacientes com idade entre 19 e 59 anos.'),
('Idoso (60+ anos)', 'Pacientes com idade igual ou superior a 60 anos.')
ON CONFLICT (nome) DO NOTHING;

-- Tipos de Serviço
INSERT INTO tb_tipo_servico (nome) VALUES
('Psicoterapia Clinica'),
('Avaliacao Neuropsicologica'),
('Reabilitacao Neuropsicologica'),
('Orientacao Profissional'),
('Outro')
ON CONFLICT (nome) DO NOTHING;

-- Formas de Cobrança de Reabilitação
INSERT INTO tb_forma_cobranca_reabilitacao (nome) VALUES
('Por Sessao'),
('Pacote Total'),
('Parcelado'),
('Por Etapa/Modulo'),
('Outro')
ON CONFLICT (nome) DO NOTHING;

-- Status do Objetivo de Reabilitação
INSERT INTO tb_status_objetivo_reabilitacao (nome) VALUES
('Objetivo Alcançado'),
('Parcialmente Alcançado'),
('Nao Alcançado'),
('Em Andamento')
ON CONFLICT (nome) DO NOTHING;

-- Tipos de Transação Financeira
INSERT INTO tb_tipo_transacao_financeira (nome) VALUES
('Pagamento de Servico'),
('Venda de Produto Vinculada ao Paciente'),
('Venda de Material Geral')
ON CONFLICT (nome) DO NOTHING;

-- Formas de Pagamento
INSERT INTO tb_forma_pagamento (nome) VALUES
('Debito'),
('Credito'),
('Dinheiro'),
('Pix'),
('Transferencia'),
('Convenio')
ON CONFLICT (nome) DO NOTHING;

-- Status de Pagamento
INSERT INTO tb_status_pagamento (nome) VALUES
('Pago'),
('Pendente'),
('Cancelado')
ON CONFLICT (nome) DO NOTHING;

-- Tipos de Produto
INSERT INTO tb_tipo_produto (nome) VALUES
('Jogo'),
('Manual'),
('Licenca Software'),
('E-book'),
('Curso Online'),
('Video Aula'),
('Material Didatico'),
('Brinde'),
('Papelaria'),
('Outro')
ON CONFLICT (nome) DO NOTHING;

-- ============================================================================
-- Confirmação de sucesso
-- ============================================================================
SELECT 'Tabelas criadas com sucesso!' AS mensagem;
