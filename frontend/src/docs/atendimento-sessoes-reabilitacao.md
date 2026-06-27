# Sessões de Reabilitação

## Objetivo
Registrar cada **sessão** realizada dentro de um programa de reabilitação: o que foi
feito e o planejamento dos próximos passos.

## Como acessar
Menu **Atendimento → Sessões Reab.** (`/atendimento/sessoes-reabilitacao`).

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Reabilitação | Sim | A qual programa de reabilitação a sessão pertence. |
| Data | Sim | Data da sessão. |
| Hora | Não | Horário da sessão. |
| Passos Realizados | Sim | O que foi trabalhado na sessão. |
| Próximos Passos | Não | Planejamento para a próxima sessão. |

## Dependências com outras telas (importante)
- **Reabilitação** → a sessão só pode ser registrada se já existir um **programa de
  reabilitação** cadastrado na tela **Reabilitação** (`/financeiro/reabilitacao`).
  O programa define automaticamente o paciente e o profissional.

## Regras e observações
- As colunas **Paciente** e **Profissional** vêm do programa de reabilitação vinculado.
- Use o campo **Próximos Passos** para dar continuidade ao plano na sessão seguinte.
