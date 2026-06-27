# Vendas Vinculadas ao Paciente

## Objetivo
Registrar a **venda de produtos a um paciente específico**, mantendo o histórico de
compras vinculado ao prontuário do paciente.

## Como acessar
Menu **Vendas → Vendas Vinculadas** (`/vendas/vinculadas`).

## Como usar
- A **barra de filtros** permite filtrar por **período**, **paciente** e **produto**.
- Botão **+ Adicionar** abre o formulário de nova venda.

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Paciente | Sim | A quem a venda está vinculada. |
| Produto | Sim | Produto vendido. |
| Data | Sim | Data da venda. |
| Quantidade | Sim | Quantidade vendida. |
| Valor Unitário | Sim | Preço de uma unidade. |
| Valor Total | Sim | Total da venda. |
| Forma de Pagamento | Sim | Como foi pago. |

## Dependências com outras telas (importante)
- **Só é possível vender para pacientes já cadastrados** na tela **Pacientes**.
- **Só é possível vender produtos já cadastrados** na tela **Produtos**.
- **Forma de Pagamento** → tela **Formas de Pagamento**.

## Relação com Finanças
- Ao salvar, o sistema pode **criar automaticamente uma Transação Financeira**
  correspondente a esta venda, evitando lançamento manual no Financeiro.

## Onde mais aparece
- As vendas aparecem na aba **Vendas** do **Perfil do Paciente**.
