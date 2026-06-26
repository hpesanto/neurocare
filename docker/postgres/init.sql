CREATE SCHEMA IF NOT EXISTS neurocare;
SET search_path TO neurocare;

-- Lookup tables
CREATE TABLE IF NOT EXISTS tb_usuario (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    login VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    id_perfil_acesso UUID,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_perfil_acesso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_convenio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_forma_pagamento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_tipo_produto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_tipo_servico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_faixa_etaria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_status_objetivo_reabilitacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_forma_cobranca_reabilitacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_tipo_transacao_financeira (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_status_pagamento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Main tables
CREATE TABLE IF NOT EXISTS tb_paciente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    rg VARCHAR(20),
    genero VARCHAR(50),
    estado_civil VARCHAR(50),
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
    id_psicologo_responsavel UUID REFERENCES tb_usuario(id) ON DELETE SET NULL,
    quem_encaminhou VARCHAR(255),
    motivo_encaminhamento TEXT,
    id_convenio UUID REFERENCES tb_convenio(id) ON DELETE SET NULL,
    numero_carteirinha_convenio VARCHAR(100),
    validade_carteirinha_convenio DATE,
    id_faixa_etaria UUID REFERENCES tb_faixa_etaria(id) ON DELETE SET NULL,
    status_paciente VARCHAR(50),
    observacoes_gerais TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_produto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_tipo_produto UUID REFERENCES tb_tipo_produto(id) ON DELETE SET NULL,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    valor_unitario DECIMAL(10,2) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_contato_emergencia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id) ON DELETE CASCADE,
    nome_contato VARCHAR(255) NOT NULL,
    telefone_contato VARCHAR(20) NOT NULL,
    parentesco VARCHAR(100) NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_paciente_servico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id) ON DELETE CASCADE,
    id_tipo_servico UUID NOT NULL REFERENCES tb_tipo_servico(id) ON DELETE CASCADE,
    id_psicologo_responsavel_servico UUID REFERENCES tb_usuario(id) ON DELETE SET NULL,
    data_inicio DATE DEFAULT CURRENT_DATE,
    data_fim DATE,
    ativo BOOLEAN DEFAULT TRUE,
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(id_paciente, id_tipo_servico)
);

CREATE TABLE IF NOT EXISTS tb_evolucao_clinica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id) ON DELETE CASCADE,
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id) ON DELETE CASCADE,
    data_sessao DATE NOT NULL,
    hora_sessao TIME,
    evolucao_texto TEXT NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_avaliacao_neuropsicologica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id) ON DELETE CASCADE,
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id) ON DELETE CASCADE,
    data_avaliacao DATE NOT NULL,
    motivo_avaliacao TEXT NOT NULL,
    instrumentos_utilizados TEXT,
    valor_avaliacao DECIMAL(10,2),
    hipoteses_diagnosticas TEXT,
    resultados_principais TEXT,
    conclusao_recomendacoes TEXT,
    caminho_laudo_pdf VARCHAR(255),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_reabilitacao_neuropsicologica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id) ON DELETE CASCADE,
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id) ON DELETE CASCADE,
    data_inicio DATE NOT NULL,
    data_fim_prevista DATE,
    programa_descricao TEXT NOT NULL,
    num_sessoes_planejadas INTEGER,
    frequencia VARCHAR(100),
    materiais_atividades_desc TEXT,
    id_forma_cobranca UUID REFERENCES tb_forma_cobranca_reabilitacao(id) ON DELETE SET NULL,
    valor_por_sessao DECIMAL(10,2),
    valor_total_pacote DECIMAL(10,2),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_reabilitacao_objetivo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_reabilitacao UUID NOT NULL REFERENCES tb_reabilitacao_neuropsicologica(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    id_status_objetivo UUID REFERENCES tb_status_objetivo_reabilitacao(id) ON DELETE SET NULL,
    comentario_status TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_reabilitacao_sessao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_reabilitacao UUID NOT NULL REFERENCES tb_reabilitacao_neuropsicologica(id) ON DELETE CASCADE,
    data_sessao DATE NOT NULL,
    hora_sessao TIME,
    passos_realizados TEXT NOT NULL,
    proximos_passos_planejamento TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_venda_vinculada_paciente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id) ON DELETE CASCADE,
    id_psicologo UUID REFERENCES tb_usuario(id) ON DELETE SET NULL,
    id_produto UUID NOT NULL REFERENCES tb_produto(id) ON DELETE CASCADE,
    data_venda DATE NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    valor_total_produto DECIMAL(10,2) NOT NULL,
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id) ON DELETE CASCADE,
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_venda_geral (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_psicologo UUID REFERENCES tb_usuario(id) ON DELETE SET NULL,
    data_venda DATE NOT NULL,
    nome_comprador VARCHAR(255),
    contato_comprador VARCHAR(255),
    valor_total_transacao DECIMAL(10,2) NOT NULL,
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id) ON DELETE CASCADE,
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_venda_geral_item (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_venda_geral UUID NOT NULL REFERENCES tb_venda_geral(id) ON DELETE CASCADE,
    id_produto UUID NOT NULL REFERENCES tb_produto(id) ON DELETE CASCADE,
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    valor_total_item DECIMAL(10,2) NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_transacao_financeira (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID REFERENCES tb_paciente(id) ON DELETE SET NULL,
    id_psicologo UUID REFERENCES tb_usuario(id) ON DELETE SET NULL,
    id_tipo_transacao UUID NOT NULL REFERENCES tb_tipo_transacao_financeira(id) ON DELETE CASCADE,
    data_transacao DATE NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id) ON DELETE CASCADE,
    id_status_pagamento UUID NOT NULL REFERENCES tb_status_pagamento(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    cpf_pagador VARCHAR(14),
    endereco_pagador TEXT,
    email_pagador VARCHAR(255),
    observacoes TEXT,
    id_evolucao_clinica UUID REFERENCES tb_evolucao_clinica(id) ON DELETE SET NULL,
    id_avaliacao_neuropsicologica UUID REFERENCES tb_avaliacao_neuropsicologica(id) ON DELETE SET NULL,
    id_reabilitacao_neuropsicologica UUID REFERENCES tb_reabilitacao_neuropsicologica(id) ON DELETE SET NULL,
    id_reabilitacao_sessao UUID REFERENCES tb_reabilitacao_sessao(id) ON DELETE SET NULL,
    id_venda_vinculada_paciente UUID REFERENCES tb_venda_vinculada_paciente(id) ON DELETE SET NULL,
    id_venda_geral UUID REFERENCES tb_venda_geral(id) ON DELETE SET NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add FK from tb_usuario to tb_perfil_acesso (added after both tables exist)
ALTER TABLE tb_usuario ADD CONSTRAINT fk_usuario_perfil
    FOREIGN KEY (id_perfil_acesso) REFERENCES tb_perfil_acesso(id) ON DELETE SET NULL;

-- Seed data for testing
INSERT INTO tb_perfil_acesso (nome, descricao) VALUES ('Administrador', 'Acesso total ao sistema') ON CONFLICT DO NOTHING;
INSERT INTO tb_perfil_acesso (nome, descricao) VALUES ('Psicologo', 'Acesso aos proprios pacientes') ON CONFLICT DO NOTHING;
INSERT INTO tb_perfil_acesso (nome, descricao) VALUES ('Secretaria', 'Acesso ao cadastro de pacientes') ON CONFLICT DO NOTHING;
INSERT INTO tb_convenio (nome) VALUES ('Particular'), ('Unimed'), ('SulAmérica') ON CONFLICT DO NOTHING;
INSERT INTO tb_forma_pagamento (nome) VALUES ('Dinheiro'), ('Cartão de Crédito'), ('PIX'), ('Boleto') ON CONFLICT DO NOTHING;
INSERT INTO tb_faixa_etaria (nome, descricao) VALUES ('Criança', '0-12 anos'), ('Adolescente', '13-17 anos'), ('Adulto', '18-59 anos'), ('Idoso', '60+ anos') ON CONFLICT DO NOTHING;
INSERT INTO tb_tipo_servico (nome) VALUES ('Avaliação Neuropsicológica'), ('Reabilitação'), ('Psicoterapia') ON CONFLICT DO NOTHING;
INSERT INTO tb_tipo_produto (nome) VALUES ('Material Terapêutico'), ('Livro'), ('Kit de Avaliação') ON CONFLICT DO NOTHING;
INSERT INTO tb_status_pagamento (nome) VALUES ('Pendente'), ('Pago'), ('Cancelado') ON CONFLICT DO NOTHING;
INSERT INTO tb_tipo_transacao_financeira (nome) VALUES ('Consulta'), ('Avaliação'), ('Produto') ON CONFLICT DO NOTHING;
INSERT INTO tb_status_objetivo_reabilitacao (nome) VALUES ('Em Andamento'), ('Concluído'), ('Cancelado') ON CONFLICT DO NOTHING;
INSERT INTO tb_forma_cobranca_reabilitacao (nome) VALUES ('Por Sessão'), ('Pacote Mensal'), ('Pacote Trimestral') ON CONFLICT DO NOTHING;
