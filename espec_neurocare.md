Aqui está o conteúdo completo do documento **Espec_NeuroCare_2025.docx** convertido integralmente para o formato Markdown:

---

# Programa NeuroCare Consultórios Integrados - Especificações 2025

Este programa é dividido em módulos principais: **Cadastro de Pacientes**, **Registro Financeiro**, **Acompanhamento de Pacientes (Evolução)** e **Gestão de Vendas de Produtos**. O sistema conta com um controle de acesso para diferentes perfis (Secretária, Psicólogas e Administradores), garantindo segurança e confidencialidade.

---

## 1. Cadastro de Pacientes de Psicologia
Centraliza as informações básicas essenciais para o acompanhamento.

### 1.1 Dados Necessários no Cadastro
*   **Informações Pessoais:** Nome Completo, Data de Nascimento, CPF, RG, Gênero, Estado Civil, Profissão.
*   **Informações de Contato:** Telefone Principal (com DDD), Telefone Secundário (opcional), E-mail, Endereço Completo (Rua, Número, Complemento, Bairro, Cidade, Estado, CEP).
*   **Contato de Emergência:** Nome, Telefone e Parentesco.
*   **Informações do Convênio:** Nome do Convênio, Número da Carteirinha, Validade.
*   **Informações de Encaminhamento:** Quem encaminhou (Médico, Escola, etc.) e breve motivo.

### 1.2 Funcionalidades e Seleções (Dropdown)
*   **Psicólogo Responsável:** Seleção entre as seis psicólogas do consultório.
*   **Tipo de Atendimento Inicial:** Psicoterapia Clínica, Avaliação Neuropsicológica, Reabilitação Neuropsicológica, Orientação Profissional ou Outro.
*   **Faixa Etária:** Criança (0-12), Adolescente (13-18), Adulto (19-59), Idoso (60+).
*   **Status do Paciente:** Ativo, Inativo, Alta, Em Espera.

### 1.3 Informações Adicionais
*   **Observações Gerais:** Campo de texto livre para particularidades.
*   **Histórico de Atendimentos Anteriores:** Registro de atendimentos psicológicos prévios.

---

## 2. Registro Financeiro
Gestão de pagamentos de serviços e produtos com controle de acesso rigoroso.

### 2.1 Dados do Registro
*   **Vinculação:** Seleção do paciente cadastrado.
*   **Data da Transação:** Campo de data.
*   **Tipo de Transação:** Pagamento de Serviço (Sessão, Laudo, etc.), Venda de Produto (Vinculada ao Paciente), Venda de Material (Geral).
*   **Descrição:** Texto livre (ex: "Sessão de Psicoterapia", "Jogo de Atenção").
*   **Valor:** Campo numérico (moeda).
*   **Forma de Pagamento:** Débito, Crédito, Dinheiro, Pix, Transferência, Convênio.
*   **Status:** Pago, Pendente, Cancelado.
*   **Dados para Contabilidade:** CPF, Endereço e E-mail do Pagador (se diferente do paciente).

### 2.2 Vinculação e Filtragem
*   **Automação:** Preenchimento automático de dados do paciente no financeiro.
*   **Relatórios:** Geração de relatórios por período, psicólogo ou tipo para exportação (CSV/Excel) para o contador.

---

## 3. Acompanhamento e Evolução do Paciente
Acessível apenas aos psicólogos responsáveis e administradores.

### 3.1 Atendimento Clínico (Evolução)
*   **Registro por Data:** Data e Hora da sessão.
*   **Evolução do Paciente:** Campo de texto amplo para detalhes clínicos e intervenções.
*   **Identificação:** Registro associado automaticamente à psicóloga que o inseriu.

### 3.2 Avaliação Neuropsicológica
*   **Campos Específicos:** Motivo, Instrumentos Utilizados, Hipóteses Diagnósticas, Resultados Principais, Conclusão e Recomendações.
*   **Financeiro:** O "Valor da Avaliação" preenchido aqui é enviado ao módulo financeiro.
*   **Anexos:** Opção para anexar laudo final em PDF.

### 3.3 Reabilitação Neuropsicológica
*   **Planejamento:** Programa, Objetivos, Sessões Programadas e Frequência.
*   **Forma de Cobrança:** Por Sessão, Pacote Total, Parcelado, Por Etapa ou Outro.
*   **Acompanhamento:** Campos para "Passos Realizados", "Planejamento Futuro" e "Status do Objetivo" (Alcançado, Em Andamento, etc.).

### 3.4 Vinculação de Áreas (Botões Ativar/Desativar)
*   Permite ativar ou desativar abas (Evolução, Avaliação, Reabilitação) conforme a necessidade do paciente ao longo do tempo.

---

## 4. Gestão de Vendas de Produtos
### 4.1 Vendas Vinculadas ao Paciente
*   Registro de jogos, manuais, cursos e vídeo aulas adquiridos como complemento ao tratamento.
*   Cálculo automático de Valor Total (Quantidade * Unitário).

### 4.2 Vendas de Material do Consultório (Geral)
*   Módulo independente para vendas ao público geral ou familiares (livros, brindes, papelaria).

---

## 5. Gestão de Acessos e Permissões

### 5.1 Secretária
*   **Pode:** Cadastrar pacientes (dados básicos), organizar busca e iniciar registros de vendas (itens/quantidades).
*   **Não Pode:** Ver valores financeiros, acessar evoluções clínicas ou finalizar pagamentos.

### 5.2 Psicólogas
*   **Pode:** Gestão completa de seus **próprios** pacientes (cadastro, clínica e financeiro).
*   **Não Pode:** Acessar dados clínicos ou financeiros de pacientes de outras colegas.

### 5.3 Administradores
*   **Acesso Total:** Visibilidade irrestrita a todos os módulos, pacientes, evoluções e faturamento total da clínica.
*   **Gestão de Sistema:** Adicionar/remover usuários e gerar relatórios gerenciais abrangentes.

---
