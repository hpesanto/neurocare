-- Criação do schema neurocare
CREATE SCHEMA IF NOT EXISTS neurocare;

-- Define o schema neurocare como padrão para as operações seguintes
SET search_path TO neurocare;

-- Extensão necessária para gerar UUIDs aleatórios
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Tabela de Perfis de Acesso (tb_perfil_acesso)
-- Armazena os diferentes tipos de perfis de usuário no sistema (Administrador, Psicóloga, Secretária).
CREATE TABLE tb_perfil_acesso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) UNIQUE NOT NULL, -- Ex: 'Administrador', 'Psicologa', 'Secretaria'
    descricao TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Usuários (tb_usuario)
-- Contém as informações de login e perfil de cada usuário do sistema.
CREATE TABLE tb_usuario (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_perfil_acesso UUID NOT NULL REFERENCES tb_perfil_acesso(id),
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    login VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL, -- Armazenar o hash da senha (nunca a senha em texto claro)
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhor performance na busca de usuários
CREATE INDEX idx_usuario_email ON tb_usuario (email);
CREATE INDEX idx_usuario_login ON tb_usuario (login);
CREATE INDEX idx_usuario_id_perfil_acesso ON tb_usuario (id_perfil_acesso);


-- Tabela de Convênios (tb_convenio)
-- Tabela de lookup para os convênios que os pacientes podem ter.
CREATE TABLE tb_convenio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Faixas Etárias (tb_faixa_etaria)
-- Tabela de lookup para categorizar os pacientes por faixa etária.
CREATE TABLE tb_faixa_etaria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) UNIQUE NOT NULL, -- Ex: 'Crianca (0-12 anos)', 'Adulto (19-59 anos)'
    descricao TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


-- Tabela de Pacientes (tb_paciente)
-- Armazena todas as informações cadastrais dos pacientes de psicologia.
CREATE TABLE tb_paciente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    cpf VARCHAR(14) UNIQUE, -- Formato: XXX.XXX.XXX-XX
    rg VARCHAR(20),
    genero VARCHAR(50) NOT NULL CHECK (genero IN ('Masculino', 'Feminino', 'Outro', 'Não Informar')), -- Substitui tb_genero
    estado_civil VARCHAR(50) NOT NULL CHECK (estado_civil IN ('Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'União Estável')), -- Substitui tb_estado_civil
    profissao VARCHAR(100),
    telefone_principal VARCHAR(20) NOT NULL, -- Formato: (XX) XXXXX-XXXX
    telefone_secundario VARCHAR(20),
    email VARCHAR(255),
    endereco_rua VARCHAR(255),
    endereco_numero VARCHAR(50),
    endereco_complemento VARCHAR(100),
    endereco_bairro VARCHAR(100),
    endereco_cidade VARCHAR(100),
    endereco_estado VARCHAR(50),
    endereco_cep VARCHAR(10), -- Formato: XXXXX-XXX
    id_psicologo_responsavel UUID REFERENCES tb_usuario(id), -- FK para o psicólogo principal (deve ser do perfil 'Psicologa')
    quem_encaminhou VARCHAR(255),
    motivo_encaminhamento TEXT,
    id_convenio UUID REFERENCES tb_convenio(id),
    numero_carteirinha_convenio VARCHAR(100),
    validade_carteirinha_convenio DATE,
    id_faixa_etaria UUID REFERENCES tb_faixa_etaria(id),
    status_paciente VARCHAR(50) NOT NULL CHECK (status_paciente IN ('Ativo', 'Inativo', 'Alta', 'Em Espera')), -- Substitui tb_status_paciente
    observacoes_gerais TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Contatos de Emergência (tb_contato_emergencia)
-- Armazena os contatos de emergência para cada paciente.
CREATE TABLE tb_contato_emergencia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    nome_contato VARCHAR(255) NOT NULL,
    telefone_contato VARCHAR(20) NOT NULL,
    parentesco VARCHAR(100) NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para busca de pacientes
CREATE INDEX idx_paciente_cpf ON tb_paciente (cpf);
CREATE INDEX idx_paciente_nome_completo ON tb_paciente (nome_completo);
CREATE INDEX idx_paciente_psicologo_responsavel ON tb_paciente (id_psicologo_responsavel);


-- Tabela de Tipos de Serviço (tb_tipo_servico)
-- Tabela de lookup para todos os tipos de serviço oferecidos (Clínica, Avaliação, Reabilitação, etc.).
CREATE TABLE tb_tipo_servico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL, -- Ex: 'Psicoterapia Clinica', 'Avaliacao Neuropsicologica', 'Reabilitacao Neuropsicologica'
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Paciente x Serviço Ativo (tb_paciente_servico)
-- Gerencia quais serviços um paciente está ativamente recebendo, permitindo flexibilidade de ativação.
CREATE TABLE tb_paciente_servico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_tipo_servico UUID NOT NULL REFERENCES tb_tipo_servico(id),
    psicologo_responsavel_servico UUID REFERENCES tb_usuario(id), -- O psicólogo que está conduzindo este serviço específico
    data_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    data_fim DATE,
    ativo BOOLEAN DEFAULT TRUE,
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_paciente, id_tipo_servico) -- Garante que um paciente só pode ter um tipo de serviço ativo por vez para este tipo
);

-- Tabela de Evolução Clínica (tb_evolucao_clinica)
-- Registra as notas e observações de cada sessão de atendimento clínico do paciente.
CREATE TABLE tb_evolucao_clinica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id), -- Psicólogo que registrou a evolução
    data_sessao DATE NOT NULL,
    hora_sessao TIME,
    evolucao_texto TEXT NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para buscar evoluções por paciente e data
CREATE INDEX idx_evolucao_clinica_paciente_data ON tb_evolucao_clinica (id_paciente, data_sessao);


-- Tabela de Avaliação Neuropsicológica (tb_avaliacao_neuropsicologica)
-- Armazena os dados específicos de avaliações neuropsicológicas realizadas.
CREATE TABLE tb_avaliacao_neuropsicologica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id), -- Psicólogo que realizou a avaliação
    data_avaliacao DATE NOT NULL,
    motivo_avaliacao TEXT NOT NULL,
    instrumentos_utilizados TEXT,
    valor_avaliacao NUMERIC(10, 2), -- Valor total da avaliação
    hipoteses_diagnosticas TEXT,
    resultados_principais TEXT,
    conclusao_recomendacoes TEXT,
    caminho_laudo_pdf VARCHAR(255), -- Caminho ou URL para o arquivo PDF do laudo
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para buscar avaliações por paciente
CREATE INDEX idx_avaliacao_neuropsicologica_paciente ON tb_avaliacao_neuropsicologica (id_paciente);


-- Tabela de Formas de Cobrança da Reabilitação (tb_forma_cobranca_reabilitacao)
-- Tabela de lookup para as opções de cobrança de programas de reabilitação.
CREATE TABLE tb_forma_cobranca_reabilitacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL, -- Ex: 'Por Sessao', 'Pacote Total', 'Parcelado', 'Por Etapa/Modulo'
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Status do Objetivo da Reabilitação (tb_status_objetivo_reabilitacao)
-- Tabela de lookup para o status dos objetivos de reabilitação.
CREATE TABLE tb_status_objetivo_reabilitacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL, -- Ex: 'Objetivo Alcançado', 'Parcialmente Alcançado', 'Em Andamento'
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Reabilitação Neuropsicológica (tb_reabilitacao_neuropsicologica)
-- Armazena os detalhes do programa de reabilitação neuropsicológica para um paciente.
CREATE TABLE tb_reabilitacao_neuropsicologica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_psicologo UUID NOT NULL REFERENCES tb_usuario(id), -- Psicólogo responsável pelo programa de reabilitação
    data_inicio DATE NOT NULL,
    data_fim_prevista DATE,
    programa_descricao TEXT NOT NULL,
    num_sessoes_planejadas INTEGER,
    frequencia VARCHAR(100), -- Ex: '2x semana', '1x semana'
    materiais_atividades_desc TEXT,
    id_forma_cobranca UUID REFERENCES tb_forma_cobranca_reabilitacao(id),
    valor_por_sessao NUMERIC(10, 2),
    valor_total_pacote NUMERIC(10, 2),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para buscar reabilitações por paciente
CREATE INDEX idx_reabilitacao_neuropsicologica_paciente ON tb_reabilitacao_neuropsicologica (id_paciente);


-- Tabela de Objetivos da Reabilitação (tb_reabilitacao_objetivo)
-- Lista os objetivos específicos de um programa de reabilitação.
CREATE TABLE tb_reabilitacao_objetivo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_reabilitacao UUID NOT NULL REFERENCES tb_reabilitacao_neuropsicologica(id),
    descricao TEXT NOT NULL,
    id_status_objetivo UUID REFERENCES tb_status_objetivo_reabilitacao(id),
    comentario_status TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Sessões de Reabilitação (tb_reabilitacao_sessao)
-- Registra cada sessão individual dentro de um programa de reabilitação.
CREATE TABLE tb_reabilitacao_sessao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_reabilitacao UUID NOT NULL REFERENCES tb_reabilitacao_neuropsicologica(id),
    data_sessao DATE NOT NULL,
    hora_sessao TIME,
    passos_realizados TEXT NOT NULL,
    proximos_passos_planejamento TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Tipos de Transação Financeira (tb_tipo_transacao_financeira)
-- Tabela de lookup para categorizar as transações financeiras.
CREATE TABLE tb_tipo_transacao_financeira (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL, -- Ex: 'Pagamento de Servico', 'Venda de Produto Vinculada ao Paciente', 'Venda de Material Geral'
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Formas de Pagamento (tb_forma_pagamento)
-- Tabela de lookup para as formas como os pagamentos são realizados.
CREATE TABLE tb_forma_pagamento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL, -- Ex: 'Debito', 'Credito', 'Dinheiro', 'Pix', 'Transferencia', 'Convenio'
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Status de Pagamento (tb_status_pagamento)
-- Tabela de lookup para o status de uma transação financeira.
CREATE TABLE tb_status_pagamento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(50) UNIQUE NOT NULL, -- Ex: 'Pago', 'Pendente', 'Cancelado'
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Tipos de Produto (tb_tipo_produto)
-- Tabela de lookup para categorizar os produtos que podem ser vendidos.
CREATE TABLE tb_tipo_produto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL, -- Ex: 'Jogo', 'Manual', 'Curso Online', 'Material Didatico'
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Produtos (tb_produto)
-- Armazena os detalhes dos produtos físicos ou digitais disponíveis para venda.
CREATE TABLE tb_produto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_tipo_produto UUID REFERENCES tb_tipo_produto(id),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    valor_unitario NUMERIC(10, 2) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para buscar produtos por nome
CREATE INDEX idx_produto_nome ON tb_produto (nome);


-- Tabela de Vendas Vinculadas ao Paciente (tb_venda_vinculada_paciente)
-- Registra as vendas de produtos que são diretamente ligadas ao tratamento de um paciente específico.
CREATE TABLE tb_venda_vinculada_paciente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES tb_paciente(id),
    id_psicologo UUID REFERENCES tb_usuario(id), -- Psicólogo que registrou/finalizou a venda (pode ser secretaria que iniciou)
    id_produto UUID NOT NULL REFERENCES tb_produto(id),
    data_venda DATE NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario NUMERIC(10, 2) NOT NULL, -- Pode ser um valor promocional, diferente do padrão do produto
    valor_total_produto NUMERIC(10, 2) NOT NULL, -- Calculado: quantidade * valor_unitario
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id),
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para buscar vendas vinculadas por paciente
CREATE INDEX idx_venda_vinculada_paciente ON tb_venda_vinculada_paciente (id_paciente);


-- Tabela de Vendas de Material do Consultório Geral (tb_venda_geral)
-- Registra vendas de produtos que não estão vinculadas a um paciente específico.
CREATE TABLE tb_venda_geral (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_psicologo UUID REFERENCES tb_usuario(id), -- Psicólogo/Administrador que finalizou a venda (secretaria pode iniciar)
    data_venda DATE NOT NULL,
    nome_comprador VARCHAR(255), -- Opcional, se o comprador não for um paciente cadastrado
    contato_comprador VARCHAR(255), -- Opcional
    valor_total_transacao NUMERIC(10, 2) NOT NULL, -- Soma de todos os itens da venda
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id),
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para buscar vendas gerais por data
CREATE INDEX idx_venda_geral_data ON tb_venda_geral (data_venda);


-- Tabela de Itens de Venda Geral (tb_venda_geral_item)
-- Detalha os produtos incluídos em uma venda geral.
CREATE TABLE tb_venda_geral_item (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_venda_geral UUID NOT NULL REFERENCES tb_venda_geral(id),
    id_produto UUID NOT NULL REFERENCES tb_produto(id),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario NUMERIC(10, 2) NOT NULL,
    valor_total_item NUMERIC(10, 2) NOT NULL, -- Calculado: quantidade * valor_unitario
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


-- Tabela de Transações Financeiras (tb_transacao_financeira)
-- Centraliza todos os registros financeiros do sistema, vinculando-os às suas origens.
CREATE TABLE tb_transacao_financeira (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID REFERENCES tb_paciente(id), -- Opcional, para vendas gerais ou pagadores que não são o paciente
    id_psicologo UUID REFERENCES tb_usuario(id), -- Psicólogo envolvido na transação (se aplicável)
    id_tipo_transacao UUID NOT NULL REFERENCES tb_tipo_transacao_financeira(id),
    data_transacao DATE NOT NULL,
    valor NUMERIC(10, 2) NOT NULL CHECK (valor >= 0),
    id_forma_pagamento UUID NOT NULL REFERENCES tb_forma_pagamento(id),
    id_status_pagamento UUID NOT NULL REFERENCES tb_status_pagamento(id),
    descricao TEXT NOT NULL, -- Detalhes do item/serviço para nota fiscal
    cpf_pagador VARCHAR(14),
    endereco_pagador TEXT, -- Se o pagador for diferente do paciente e precisar de detalhes
    email_pagador VARCHAR(255),
    observacoes TEXT,
    -- Chaves estrangeiras opcionais para vincular a transação à sua origem específica
    id_evolucao_clinica UUID REFERENCES tb_evolucao_clinica(id), -- Para pagamentos de sessão de psicoterapia
    id_avaliacao_neuropsicologica UUID REFERENCES tb_avaliacao_neuropsicologica(id),
    id_reabilitacao_neuropsicologica UUID REFERENCES tb_reabilitacao_neuropsicologica(id), -- Para pacotes/parcelados de reabilitação
    id_reabilitacao_sessao UUID REFERENCES tb_reabilitacao_sessao(id), -- Para sessões individuais de reabilitação
    id_venda_vinculada_paciente UUID REFERENCES tb_venda_vinculada_paciente(id),
    id_venda_geral UUID REFERENCES tb_venda_geral(id),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para busca de transações financeiras
CREATE INDEX idx_transacao_financeira_paciente ON tb_transacao_financeira (id_paciente);
CREATE INDEX idx_transacao_financeira_data ON tb_transacao_financeira (data_transacao);
CREATE INDEX idx_transacao_financeira_psicologo ON tb_transacao_financeira (id_psicologo);

-- Preenchimento inicial de tabelas de lookup (exemplos)
-- Estes INSERTs devem ser executados após a criação das tabelas para popular as opções iniciais.

INSERT INTO tb_perfil_acesso (nome, descricao) VALUES
('Administrador', 'Acesso total ao sistema e gestão de usuários.'),
('Psicologa', 'Acesso aos dados de seus próprios pacientes e gestão financeira vinculada.'),
('Secretaria', 'Acesso básico a cadastros de pacientes e início de registros de vendas.');

INSERT INTO tb_faixa_etaria (nome, descricao) VALUES
('Crianca (0-12 anos)', 'Pacientes com idade entre 0 e 12 anos.'),
('Adolescente (13-18 anos)', 'Pacientes com idade entre 13 e 18 anos.'),
('Adulto (19-59 anos)', 'Pacientes com idade entre 19 e 59 anos.'),
('Idoso (60+ anos)', 'Pacientes com idade igual ou superior a 60 anos.');

INSERT INTO tb_tipo_servico (nome) VALUES
('Psicoterapia Clinica'),
('Avaliacao Neuropsicologica'),
('Reabilitacao Neuropsicologica'),
('Orientacao Profissional'),
('Outro');

INSERT INTO tb_forma_cobranca_reabilitacao (nome) VALUES
('Por Sessao'), ('Pacote Total'), ('Parcelado'), ('Por Etapa/Modulo'), ('Outro');

INSERT INTO tb_status_objetivo_reabilitacao (nome) VALUES
('Objetivo Alcançado'), ('Parcialmente Alcançado'), ('Nao Alcançado'), ('Em Andamento');

INSERT INTO tb_tipo_transacao_financeira (nome) VALUES
('Pagamento de Servico'),
('Venda de Produto Vinculada ao Paciente'),
('Venda de Material Geral');

INSERT INTO tb_forma_pagamento (nome) VALUES
('Debito'), ('Credito'), ('Dinheiro'), ('Pix'), ('Transferencia'), ('Convenio');

INSERT INTO tb_status_pagamento (nome) VALUES
('Pago'), ('Pendente'), ('Cancelado');

INSERT INTO tb_tipo_produto (nome) VALUES
('Jogo'), ('Manual'), ('Licenca Software'), ('E-book'), ('Curso Online'), ('Video Aula'), ('Material Didatico'), ('Brinde'), ('Papelaria'), ('Outro');

