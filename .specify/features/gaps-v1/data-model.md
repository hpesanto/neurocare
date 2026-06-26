# Data Model — Gaps

## Modelos existentes (sem alteracao)
Todos os 23 modelos ja existem e estao corretos. Nenhuma alteracao de schema.

## Novas entidades/campos necessarios

### Mapeamento Usuario Django <-> tb_usuario
Para o controle de acesso funcionar, precisamos vincular `auth_user` a `tb_usuario`:
- Opcao A: Campo `tb_usuario_id` no profile do Django User
- Opcao B: Lookup por email (auth_user.email == tb_usuario.email)
- **Escolha**: Opcao B — nao requer alteracao no banco

### Permissoes por Perfil
| Perfil | tb_perfil_acesso.nome | Acesso |
|--------|----------------------|--------|
| Secretaria | "Secretaria" | Cadastro pacientes (CRUD), Vendas material (sem valores) |
| Psicologa | "Psicologo" | Tudo de seus proprios pacientes |
| Admin | "Administrador" | Acesso total |

### Upload de laudos
- Storage: `backend/media/laudos/`
- Campo existente: `AvaliacaoNeuropsicologica.caminho_laudo_pdf` (CharField 255)
- Alterar para: FileField ou manter CharField e salvar o path do upload

## Relacionamentos novos
Nenhum — todos os FKs ja existem no schema.
