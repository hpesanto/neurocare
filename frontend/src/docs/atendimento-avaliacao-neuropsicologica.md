# Avaliação Neuropsicológica

## Objetivo
Registrar as avaliações neuropsicológicas dos pacientes, incluindo motivo,
instrumentos utilizados, hipóteses, resultados, conclusões e o **anexo do laudo em
PDF**.

## Como acessar
Menu **Atendimento → Avaliação Neuropsi.** (`/atendimento/avaliacao-neuropsicologica`).

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Paciente | Sim | Paciente avaliado. |
| Psicólogo | Sim | Profissional responsável. |
| Data da Avaliação | Sim | Quando foi realizada. |
| Valor (R$) | Não | Valor cobrado pela avaliação. |
| Laudo PDF | Não | Arquivo do laudo (apenas `.pdf`). |
| Motivo da Avaliação | Sim | Por que a avaliação foi solicitada. |
| Instrumentos Utilizados | Não | Testes/escalas aplicados. |
| Hipóteses Diagnósticas | Não | Hipóteses levantadas. |
| Resultados Principais | Não | Principais achados. |
| Conclusão e Recomendações | Não | Encaminhamentos e orientações. |

## Dependências com outras telas
- **Paciente** → cadastrado na tela **Pacientes**.
- **Psicólogo** → cadastrado na tela **Profissionais**.

## Anexo de laudo (PDF)
- No campo **Laudo PDF** é possível anexar o arquivo do laudo. Aceita **somente PDF**.
- Quando já há laudo anexado, a coluna **Laudo** da tabela mostra um botão **PDF**
  para abrir/baixar o documento, e o formulário indica *"Laudo já anexado"*.

## Onde mais aparece
- Esses registros aparecem na aba **Avaliação** do **Perfil do Paciente**.
