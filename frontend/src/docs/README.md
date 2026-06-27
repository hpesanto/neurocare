# Documentação de Telas — NeuroCare

Esta pasta contém um arquivo de ajuda (`.md`) para **cada tela** do sistema.
O objetivo é alimentar o **botão de Ajuda** presente em cada tela: ao clicar,
o usuário vê a explicação correspondente, escrita em linguagem simples para
qualquer pessoa entender a funcionalidade.

## Como usar no botão de ajuda

Cada arquivo abaixo corresponde a uma rota da aplicação. O nome do arquivo seque
o padrão do caminho da tela (com `-` no lugar de `/`). Basta importar o conteúdo
do `.md` correspondente à rota atual e exibi-lo em um modal/painel de ajuda.

## Índice de telas

| Tela | Rota | Arquivo |
|------|------|---------|
| Login | `/login` | [login.md](./login.md) |
| Agenda / Calendário | `/agendamento` | [agendamento.md](./agendamento.md) |
| Pacientes (lista/cadastro) | `/cadastro/pacientes` | [cadastro-pacientes.md](./cadastro-pacientes.md) |
| Detalhe do Paciente | `/cadastro/pacientes/:id` | [cadastro-paciente-detalhe.md](./cadastro-paciente-detalhe.md) |
| Profissionais | `/cadastro/profissionais` | [cadastro-profissionais.md](./cadastro-profissionais.md) |
| Convênios | `/cadastro/convenios` | [cadastro-convenios.md](./cadastro-convenios.md) |
| Formas de Pagamento | `/cadastro/formas-pagamento` | [cadastro-formas-pagamento.md](./cadastro-formas-pagamento.md) |
| Tipos de Produto | `/cadastro/tipos-produto` | [cadastro-tipos-produto.md](./cadastro-tipos-produto.md) |
| Produtos | `/cadastro/produtos` | [cadastro-produtos.md](./cadastro-produtos.md) |
| Faixas Etárias | `/cadastro/faixas-etarias` | [cadastro-faixas-etarias.md](./cadastro-faixas-etarias.md) |
| Tipos de Serviço | `/cadastro/tipos-servico` | [cadastro-tipos-servico.md](./cadastro-tipos-servico.md) |
| Contatos de Emergência | `/cadastro/contatos-emergencia` | [cadastro-contatos-emergencia.md](./cadastro-contatos-emergencia.md) |
| Serviços do Paciente | `/cadastro/paciente-servico` | [cadastro-paciente-servico.md](./cadastro-paciente-servico.md) |
| Evolução Clínica | `/atendimento/evolucao-clinica` | [atendimento-evolucao-clinica.md](./atendimento-evolucao-clinica.md) |
| Avaliação Neuropsicológica | `/atendimento/avaliacao-neuropsicologica` | [atendimento-avaliacao-neuropsicologica.md](./atendimento-avaliacao-neuropsicologica.md) |
| Objetivos de Reabilitação | `/atendimento/objetivos-reabilitacao` | [atendimento-objetivos-reabilitacao.md](./atendimento-objetivos-reabilitacao.md) |
| Sessões de Reabilitação | `/atendimento/sessoes-reabilitacao` | [atendimento-sessoes-reabilitacao.md](./atendimento-sessoes-reabilitacao.md) |
| Reabilitação (programa) | `/financeiro/reabilitacao` | [financeiro-reabilitacao.md](./financeiro-reabilitacao.md) |
| Transações Financeiras | `/financeiro/transacoes` | [financeiro-transacoes.md](./financeiro-transacoes.md) |
| Tipos de Transação | `/financeiro/tipos-transacao` | [financeiro-tipos-transacao.md](./financeiro-tipos-transacao.md) |
| Status de Pagamento | `/financeiro/status-pagamento` | [financeiro-status-pagamento.md](./financeiro-status-pagamento.md) |
| Formas de Cobrança | `/financeiro/formas-cobranca` | [financeiro-formas-cobranca.md](./financeiro-formas-cobranca.md) |
| Status de Objetivo | `/financeiro/status-objetivo` | [financeiro-status-objetivo.md](./financeiro-status-objetivo.md) |
| Vendas Vinculadas | `/vendas/vinculadas` | [vendas-vinculadas.md](./vendas-vinculadas.md) |
| Vendas Gerais | `/vendas/geral` | [vendas-geral.md](./vendas-geral.md) |

## Conceitos gerais (válidos para todas as telas)

- **Tela de cadastro padrão**: a maioria das telas mostra uma **tabela** com os
  registros existentes e um botão **"+ Adicionar"**. Ao clicar em Adicionar ou
  Editar, abre-se um formulário (modal). Campos com **asterisco (\*)** são
  **obrigatórios**.
- **Campos de seleção (dropdowns)**: vários formulários têm campos que buscam
  dados de **outra tela** (ex.: escolher o Paciente, o Profissional, o Convênio).
  Esses itens precisam **já estar cadastrados** para aparecerem na lista. Essa é
  a principal **dependência entre telas**.
- **Perfis de acesso**: o sistema possui perfis (ex.: **Administrador**,
  **Psicólogo**, **Secretária**). Telas clínicas e financeiras podem ser
  restritas por perfil, e um Psicólogo normalmente só enxerga **os seus próprios
  pacientes** e registros. Em caso de dúvida sobre o que você pode ver/editar,
  fale com o Administrador.
- **Tabelas auxiliares (listas de apoio)**: telas como Convênios, Formas de
  Pagamento, Tipos de Produto/Serviço/Transação, Status, etc. são **listas
  simples** usadas para preencher os dropdowns das telas principais. Mantê-las
  atualizadas é o que garante boas opções nos formulários.
