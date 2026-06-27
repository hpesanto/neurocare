# Pacientes

## Objetivo
Cadastrar e gerenciar os pacientes do consultório. Esta é uma das telas **mais
importantes do sistema**: o paciente cadastrado aqui é usado em praticamente todas
as outras telas (agenda, atendimentos, finanças, vendas).

## Como acessar
Menu **Cadastro → Pacientes** (`/cadastro/pacientes`).

## Como usar
- A tabela lista todos os pacientes. Clique no **nome** do paciente para abrir o
  **perfil completo** (com abas de histórico).
- Botão **+ Adicionar** abre o formulário de novo paciente.
- Use os ícones de **editar** e **excluir** em cada linha.

## Campos do formulário
Campos com **\*** são obrigatórios.

**Dados Pessoais**
| Campo | Obrigatório |
|-------|:----------:|
| Nome Completo | Sim |
| Data de Nascimento | Sim |
| CPF, RG, Gênero, Estado Civil, Profissão | Não |
| Status (Ativo / Inativo / Alta / Em Espera) | Não (padrão: Ativo) |

**Contato**
| Campo | Obrigatório |
|-------|:----------:|
| Telefone Principal | Sim |
| Telefone Secundário, E-mail | Não |

**Endereço** — todos opcionais (Rua, Número, Complemento, Bairro, Cidade, Estado, CEP).

**Encaminhamento e Convênio** — todos opcionais (Psicólogo Responsável, Convênio,
Faixa Etária, Quem Encaminhou, Nº da Carteirinha, Validade, Motivo do
Encaminhamento, Observações Gerais).

## Dependências com outras telas
Os campos de seleção abaixo só mostram opções **se já estiverem cadastradas**:
- **Psicólogo Responsável** → tela **Profissionais**.
- **Convênio** → tela **Convênios**.
- **Faixa Etária** → tela **Faixas Etárias**.

## Esta tela é pré-requisito para
Como o paciente é usado em muitos lugares, **cadastrá-lo aqui é o primeiro passo**
para poder: agendar na **Agenda**, registrar **Evolução Clínica**, **Avaliação**,
**Reabilitação**, **Vendas Vinculadas**, **Contatos de Emergência** e **Transações**.

## Regras e observações
- O **Status** ajuda a separar pacientes ativos dos que tiveram alta ou estão inativos.
- Dependendo do perfil, um **Psicólogo** pode ver apenas os pacientes sob sua
  responsabilidade.
