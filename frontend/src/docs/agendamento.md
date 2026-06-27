# Agenda / Calendário

## Objetivo
Visualizar e organizar os agendamentos do consultório em uma grade de horários por
**sala** e por **dia/semana**. Cada profissional aparece com uma cor diferente,
facilitando enxergar a ocupação das salas.

## Como acessar
Menu **Agenda → Calendário** (`/agendamento`). É a tela inicial após o login.

## Como usar
- Alterne entre as visões **Dia** e **Semana** pelos botões no topo.
- Use as setas **‹ ›** para navegar entre semanas/dias e o botão **Hoje** para voltar à data atual.
- Clique em um **espaço vazio** da grade para criar um novo agendamento já com a sala,
  data e hora pré-preenchidas.
- Clique em um **agendamento existente** (bloco colorido) para editar ou excluir.
- O botão **+ Novo** cria um agendamento em branco.

## Campos do agendamento
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Profissional | Sim | Quem fará o atendimento. |
| Paciente | Sim | Para quem é o atendimento. |
| Sala | Sim | Sala 1, 2 ou 3. |
| Data | Sim | Dia do atendimento. |
| Tipo | Sim | Avaliação, Reabilitação, Psicoterapia ou Outro. |
| Hora Início | Sim | Horário de início. |
| Hora Fim | Sim | Horário de término (define o tamanho do bloco). |
| Observações | Não | Anotações livres. |

## Dependências com outras telas (importante)
- **Só é possível agendar para pacientes já cadastrados.** O paciente deve existir
  na tela **Pacientes** (`/cadastro/pacientes`) para aparecer na lista.
- **Só é possível escolher profissionais já cadastrados** na tela **Profissionais**
  (`/cadastro/profissionais`).

## Regras e observações
- Horários disponíveis: das **07:00 às 20:00** de segunda a sexta, e das **07:00 às
  12:00** no sábado.
- Há **3 salas**. Um horário/sala já ocupado não fica disponível para um novo
  agendamento naquele intervalo.
- As cores são atribuídas automaticamente por profissional e aparecem na legenda
  abaixo da grade.
