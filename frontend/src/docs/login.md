# Login

## Objetivo
Tela de entrada do sistema. Garante que apenas usuários autorizados (profissionais
e equipe do consultório) acessem os dados de pacientes e finanças.

## Como acessar
É a primeira tela exibida quando você ainda não está autenticado. Qualquer tentativa
de acessar outra página sem login redireciona para cá.

## Campos
| Campo | Obrigatório | Descrição |
|-------|:----------:|-----------|
| Usuário | Sim | O login cadastrado do profissional. |
| Senha | Sim | A senha definida no cadastro do profissional. |

## Dependências com outras telas
- O usuário e a senha vêm do cadastro feito na tela **Profissionais**
  (`/cadastro/profissionais`). Se um profissional ainda não foi cadastrado lá (com
  login e senha), ele **não consegue entrar**.

## Regras e observações
- Em caso de usuário ou senha incorretos, aparece a mensagem *"Usuário ou senha inválidos"*.
- Após entrar, o sistema abre automaticamente na **Agenda**.
- O perfil de acesso do usuário (Administrador, Psicólogo, Secretária) determina o
  que ele poderá ver e editar nas demais telas.
