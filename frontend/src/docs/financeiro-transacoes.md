# Transações Financeiras

## Objetivo
Registrar e acompanhar todas as **movimentações financeiras** do consultório
(recebimentos, pagamentos, etc.), com filtros e **exportação** para CSV/Excel.

## Como acessar
Menu **Financeiro → Transações** (`/financeiro/transacoes`).

## Como usar
- A **barra de filtros** permite filtrar por **período** (data início/fim), **tipo de
  transação** e **status de pagamento**. Clique em **Aplicar** / **Limpar**.
- Botões **Exportar CSV** e **Exportar Excel** geram um arquivo com as transações
  **respeitando os filtros aplicados**.

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Data | Sim | Data da transação. |
| Valor | Sim | Valor em R$. |
| Tipo de Transação | Sim | Categoria da movimentação. |
| Forma de Pagamento | Sim | Como foi pago/recebido. |
| Status Pagamento | Sim | Situação (ex.: pago, pendente). |
| Paciente | Não | Paciente relacionado (quando aplicável). |
| Descrição | Sim | Detalhe da transação. |

## Dependências com outras telas
- **Tipo de Transação** → tela **Tipos de Transação**.
- **Forma de Pagamento** → tela **Formas de Pagamento**.
- **Status Pagamento** → tela **Status de Pagamento**.
- **Paciente** (opcional) → tela **Pacientes**.

## Relação com Vendas
- Ao registrar uma **venda** (Vendas Vinculadas ou Vendas Gerais), o sistema pode
  **gerar automaticamente** uma transação financeira correspondente. Por isso, parte
  das transações pode ter origem nas telas de Vendas.

## Regras e observações
- Acesso normalmente restrito a perfis com permissão financeira (ex.: Administrador).
