# Reabilitação (Programa)

## Objetivo
Cadastrar o **programa de reabilitação neuropsicológica** de um paciente: o plano
geral, com data de início, previsão de término e frequência. É o "guarda-chuva" ao
qual se ligam os **Objetivos** e as **Sessões** de reabilitação.

## Como acessar
Menu **Financeiro → Reabilitação** (`/financeiro/reabilitacao`).

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Paciente | Sim | Paciente em reabilitação. |
| Psicólogo | Sim | Profissional responsável pelo programa. |
| Data Início | Sim | Início do programa. |
| Fim Previsto | Não | Previsão de término. |
| Frequência | Não | Ex.: semanal, 2x por semana. |
| Descrição do Programa | Sim | Detalhamento do plano de reabilitação. |

## Dependências com outras telas
- **Paciente** → cadastrado na tela **Pacientes**.
- **Psicólogo** → cadastrado na tela **Profissionais**.

## Esta tela é pré-requisito para
- **Objetivos de Reabilitação** e **Sessões de Reabilitação**: ambos precisam
  apontar para um programa de reabilitação criado **aqui**. Sem cadastrar o programa
  primeiro, não é possível registrar objetivos nem sessões.

## Onde mais aparece
- Os programas aparecem na aba **Reabilitação** do **Perfil do Paciente**.
