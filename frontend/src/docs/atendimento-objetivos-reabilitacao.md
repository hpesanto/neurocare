# Objetivos de Reabilitação

## Objetivo
Definir os **objetivos terapêuticos** de um programa de reabilitação e acompanhar o
**status** de cada um (ex.: em andamento, concluído).

## Como acessar
Menu **Atendimento → Objetivos Reab.** (`/atendimento/objetivos-reabilitacao`).

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Reabilitação | Sim | A qual programa de reabilitação o objetivo pertence. |
| Status | Não | Situação atual do objetivo. |
| Descrição | Sim | O que se pretende alcançar. |
| Comentário | Não | Observações sobre o andamento. |

## Dependências com outras telas (importante)
- **Reabilitação** → o objetivo só pode ser criado se já existir um **programa de
  reabilitação** cadastrado na tela **Reabilitação** (`/financeiro/reabilitacao`).
  O programa carrega automaticamente o paciente e o profissional associados.
- **Status** → usa a lista da tela **Status de Objetivo** (`/financeiro/status-objetivo`).

## Regras e observações
- As colunas **Paciente** e **Profissional** vêm do programa de reabilitação vinculado.
