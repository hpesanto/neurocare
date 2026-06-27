# Serviços do Paciente

## Objetivo
Registrar quais **serviços** o paciente está utilizando ao longo do tempo (ex.:
psicoterapia, reabilitação, avaliação), com período de início e fim.

## Como acessar
Rota `/cadastro/paciente-servico`.

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Paciente | Sim | A quem o serviço pertence. |
| Tipo de Serviço | Sim | Qual serviço está sendo prestado. |
| Data Início | Não | Quando o serviço começou. |
| Data Fim | Não | Quando terminou (deixe vazio se ainda ativo). |
| Observações | Não | Anotações livres. |

## Dependências com outras telas
- **Paciente** → deve estar cadastrado na tela **Pacientes**.
- **Tipo de Serviço** → deve estar cadastrado na tela **Tipos de Serviço**
  (`/cadastro/tipos-servico`).

## Regras e observações
- A coluna **Ativo** indica se o serviço está em andamento.
- Permite manter um histórico de quais serviços cada paciente já utilizou.
