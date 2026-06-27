# Detalhe do Paciente (Perfil)

## Objetivo
Mostrar, em um só lugar, todo o **histórico de um paciente** organizado em abas:
seus dados cadastrais e os registros relacionados a ele em outras áreas do sistema.

## Como acessar
Na tela **Pacientes** (`/cadastro/pacientes`), clique no **nome** de um paciente.
A rota é `/cadastro/pacientes/:id`.

## O que cada aba mostra
| Aba | Conteúdo | Origem dos dados |
|-----|----------|------------------|
| **Dados** | Dados pessoais, contato, endereço, convênio e encaminhamento. | Cadastro do paciente |
| **Evolução** | Sessões clínicas registradas. | Tela **Evolução Clínica** |
| **Avaliação** | Avaliações neuropsicológicas. | Tela **Avaliação Neuropsicológica** |
| **Reabilitação** | Programas de reabilitação. | Tela **Reabilitação** |
| **Vendas** | Produtos vendidos a este paciente. | Tela **Vendas Vinculadas** |

## Dependências com outras telas
- Esta tela é **somente leitura** (consulta). Os registros exibidos nas abas são
  criados nas telas correspondentes. Se uma aba estiver vazia (*"Nenhum registro"*),
  é porque ainda não há lançamentos para aquele paciente naquela área.

## Regras e observações
- Use o botão **Voltar** para retornar à lista de pacientes.
- O **status** do paciente (ex.: Ativo) aparece como etiqueta ao lado do nome.
- Esta tela é ideal para uma **visão 360°** do paciente antes de um atendimento.
