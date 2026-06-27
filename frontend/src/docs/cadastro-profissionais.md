# Profissionais

## Objetivo
Cadastrar os profissionais e usuários do sistema (psicólogos, secretárias,
administradores). Além de representar quem realiza os atendimentos, este cadastro é
o que **permite o login** no sistema.

## Como acessar
Menu **Cadastro → Profissionais** (`/cadastro/profissionais`).

## Campos do formulário
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Nome | Sim | Nome do profissional. |
| E-mail | Sim | E-mail (também usado para identificar o usuário). |
| Login | Sim | Nome de usuário para entrar no sistema. |
| Senha | Sim ao criar / opcional ao editar | Senha de acesso. Ao editar, preencha só se quiser **trocar** a senha. |
| Perfil de Acesso | Não | Define as permissões (ex.: Administrador, Psicólogo, Secretária). |

## Dependências com outras telas
- O campo **Perfil de Acesso** usa a lista de perfis cadastrados no sistema. O perfil
  controla **o que o usuário pode fazer** nas demais telas.

## Esta tela é pré-requisito para
- **Login**: sem um profissional com login/senha, não há como entrar no sistema.
- **Agenda, Evolução, Avaliação, Reabilitação**: o profissional precisa existir aqui
  para ser selecionado como responsável pelo atendimento.

## Regras e observações
- O **Perfil de Acesso** deve ser definido com cuidado: ele determina, por exemplo,
  se o usuário enxerga dados financeiros ou apenas seus próprios pacientes.
- A coluna **Ativo** indica se o profissional está em atividade.
