# Evolução Clínica

## Objetivo
Registrar o acompanhamento clínico de cada sessão de um paciente (prontuário de
evolução). Cada registro documenta o que foi observado/trabalhado em uma sessão.

## Como acessar
Menu **Atendimento → Evolução Clínica** (`/atendimento/evolucao-clinica`).

## Como usar
- No topo há uma **barra de filtros** para localizar registros por **período**
  (data início/fim), **paciente** e **psicólogo**. Clique em **Aplicar** para filtrar
  e **Limpar** para remover os filtros.
- Botão **+ Adicionar** abre o formulário de nova evolução.

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Paciente | Sim | Paciente atendido. |
| Psicólogo | Sim | Profissional que conduziu a sessão. |
| Data | Sim | Data da sessão. |
| Hora | Não | Horário da sessão. |
| Evolução | Sim | Texto descritivo da evolução clínica. |

## Dependências com outras telas
- **Paciente** → cadastrado na tela **Pacientes**.
- **Psicólogo** → cadastrado na tela **Profissionais**.

## Onde mais aparece
- Esses registros aparecem na aba **Evolução** do **Perfil do Paciente**.

## Regras e observações
- Conteúdo clínico sensível: o acesso pode ser restrito ao psicólogo responsável,
  conforme o perfil de acesso.
