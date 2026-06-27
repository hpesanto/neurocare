# Vendas Gerais

## Objetivo
Registrar vendas **avulsas**, feitas para compradores que **não são pacientes**
cadastrados (ex.: venda balcão a um terceiro).

## Como acessar
Menu **Vendas → Vendas Gerais** (`/vendas/geral`).

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Data | Sim | Data da venda. |
| Valor Total | Sim | Total da venda em R$. |
| Forma de Pagamento | Sim | Como foi pago. |
| Comprador | Não | Nome de quem comprou. |
| Contato | Não | Telefone/contato do comprador. |

## Dependências com outras telas
- **Forma de Pagamento** → tela **Formas de Pagamento**.
- Diferente das **Vendas Vinculadas**, esta tela **não exige paciente cadastrado**:
  o comprador é informado livremente em texto.

## Relação com Finanças
- Ao salvar, o sistema pode **criar automaticamente uma Transação Financeira**
  correspondente a esta venda.

## Quando usar Vendas Gerais x Vendas Vinculadas
- Use **Vendas Vinculadas** quando o comprador **é um paciente** (fica no histórico dele).
- Use **Vendas Gerais** quando o comprador **não é paciente** do consultório.
