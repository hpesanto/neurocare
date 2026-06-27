# Contatos de Emergência

## Objetivo
Registrar pessoas para contato em caso de emergência relacionadas a um paciente
(familiares, responsáveis, etc.).

## Como acessar
Menu **Cadastro → Contatos Emergência** (`/cadastro/contatos-emergencia`).

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Paciente | Sim | A quem o contato pertence. |
| Nome do Contato | Sim | Nome da pessoa para contato. |
| Telefone | Sim | Telefone da pessoa. |
| Parentesco | Sim | Relação com o paciente (ex.: mãe, cônjuge). |

## Dependências com outras telas
- **É obrigatório vincular a um paciente já cadastrado** na tela **Pacientes**
  (`/cadastro/pacientes`). Sem paciente cadastrado, não é possível criar o contato.

## Regras e observações
- Um mesmo paciente pode ter **vários** contatos de emergência.
