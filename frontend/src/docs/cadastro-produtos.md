# Produtos

## Objetivo
Cadastrar os produtos que o consultório vende (ex.: materiais, kits, itens
terapêuticos). Esses produtos são usados nas telas de **Vendas**.

## Como acessar
Menu **Cadastro → Produtos** (`/cadastro/produtos`).

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Nome | Sim | Nome do produto. |
| Valor Unitário (R$) | Sim | Preço de venda de uma unidade. |
| Descrição | Não | Detalhes do produto. |

## Dependências com outras telas
- Opcionalmente, um produto pode estar associado a um **Tipo de Produto** (cadastrado
  na tela **Tipos de Produto**), exibido na coluna *Tipo* da listagem.

## Esta tela é pré-requisito para
- **Vendas Vinculadas** (`/vendas/vinculadas`): só é possível vender produtos que
  estejam cadastrados aqui.

## Regras e observações
- A coluna **Ativo** indica se o produto está disponível para venda.
- O **Valor Unitário** serve de referência ao registrar uma venda.
