# Admin (Usuários e Permissões) — NeuroCare

Este arquivo explica como usar e habilitar o Django Admin para criar/gerenciar usuários, grupos e permissões na aplicação NeuroCare.

Ele cobre:
- habilitar acesso ao `admin/` (já habilitado por padrão no projeto)
- criar superuser (interativo e não interativo via PowerShell)
- criar grupos e atribuir permissões no admin
- registrar modelos no admin.py (exemplos)
- exemplos de script para criar usuários e atribuir grupos/permissions via `manage.py shell`

---

Pré-requisitos
- Python e virtualenv ativos (se estiver usando `psico` env, ative com `.\\psico\\Scripts\\Activate.ps1` no PowerShell)
- banco de dados conectado (veja `neurocare_project/settings.py`)
- o projeto pode já ter o Admin habilitado — confirme que `django.contrib.admin` está em `INSTALLED_APPS` e que `neurocare_project/urls.py` tem uma rota para `admin/`.

Verificações rápidas
1. Confirme que Admin está habilitado:
   - Abra `neurocare_project/settings.py` e verifique `INSTALLED_APPS` contém `django.contrib.admin`.
   - Abra `neurocare_project/urls.py` e confirme que existe `path('admin/', admin.site.urls)`.

Criar um superuser (interativo)
No PowerShell (na raiz do projeto):

```powershell
# Ative o virtualenv se necessário
.\psico\Scripts\Activate.ps1

# Cria um superuser interativo
python manage.py createsuperuser
```

Criar um superuser não-interativamente (script)
Use quando quiser automatizar em scripts CI/CD ou em provisionamento. Exemplo (PowerShell):

```powershell
$env:DJANGO_SUPERUSER_USERNAME = "admin"
$env:DJANGO_SUPERUSER_EMAIL = "admin@example.com"
$env:DJANGO_SUPERUSER_PASSWORD = "ChangeMe123!"
python manage.py createsuperuser --noinput
```

Observação: O `createsuperuser --noinput` exige que você defina as variáveis de ambiente acima. Em ambientes de produção prefira criar usuários com senhas seguras e processos controlados.

Acessando o Admin
- Inicie o servidor: `python manage.py runserver`
- Vá para: `http://127.0.0.1:8000/admin/`
- Faça login com o superuser criado.

Gerenciar usuários, grupos e permissões pelo Admin
- Users: crie e edite usuários, defina `is_staff` e `is_superuser`.
- Groups: crie grupos (por exemplo "Recepção", "Profissional") e adicione permissões desejadas.
- Permissions: associe permissões de models (ex.: `add_paciente`, `view_paciente`) a grupos ou usuários diretamente.

Dica: para que usuários acessem o Admin a conta precisa ter `is_staff=True`.

Registrar modelos no Admin (exemplos)
Se quiser listar modelos específicos no Admin para gerenciamento (ex.: `pacientes.Paciente`), adicione um `admin.py` no app correspondente e registre o modelo.

Exemplo `pacientes/admin.py`:

```python
from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'telefone')
    search_fields = ('nome', 'cpf')
```

Depois reinicie o servidor; o modelo deverá aparecer em Admin.

Criar grupos e permissões via script (manage.py shell)
Às vezes é útil criar grupos e atribuir permissões por script (útil em provisioning):

```powershell
# Abra o shell
python manage.py shell

# No shell Python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Exemplo: criar um grupo 'Recepcao' e dar permissão de ver/Adicionar Paciente
g, _ = Group.objects.get_or_create(name='Recepcao')
# permissões já existem se o model Paciente estiver migrado: 'add_paciente', 'view_paciente'
from django.contrib.auth.models import Permission
p_view = Permission.objects.get(codename='view_paciente')
p_add = Permission.objects.get(codename='add_paciente')
g.permissions.add(p_view, p_add)

# adicionar um usuário ao grupo
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username='someuser')
u.groups.add(g)
```

Script automatizado (exemplo em PowerShell) para criar grupo e permissões:

```powershell
python - <<'PY'
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

g, _ = Group.objects.get_or_create(name='Recepcao')
perm = Permission.objects.get(codename='view_paciente')
g.permissions.add(perm)

User = get_user_model()
user = User.objects.create_user('reception1', password='Pass123!')
user.is_staff = True
user.save()
user.groups.add(g)
print('created')
PY
```

Controle de acesso na UI (menu)
O projeto já possui uma lógica de menu que usa `permissions` strings no `menu_config.py` e filtra com `user.has_perms(...)` no `neurocare_project/context_processors.py`.

Isso significa que, depois de atribuir permissões via Admin ou script, os itens do menu aparecerão automaticamente para usuários que têm essas permissões.

Boa prática: criar grupos com o conjunto de permissões e atribuir usuários a esses grupos. Assim o menu e as permissões da aplicação serão coerentes.

Exemplo rápido: permissões úteis para o domínio Pacientes
- `accounts.view_paciente` ou `pacientes.view_paciente` (dependendo do app_label) — ver a lista
- `accounts.add_paciente` — criar
- `accounts.change_paciente` — editar
- `accounts.delete_paciente` — remover

(Substitua `accounts` acima pelo `app_label` correto do model Paciente, provavelmente `pacientes`.)

Como verificar permissões de um usuário no shell

```powershell
python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='someuser')
print(user.has_perm('pacientes.view_paciente'))
print(user.has_perms(['pacientes.view_paciente','pacientes.add_paciente']))
```

Notas de segurança e recomendações
- Nunca exponha contas de superuser em produção sem controle (use credenciais fortes, 2FA, etc.).
- Prefira criar contas de administração com `is_staff=True` e permissões/grupos limitados.
- Mantenha um conjunto mínimo de permissões necessárias para cada role.

Próximos passos (opcionais que eu posso implementar)
- Adicionar link no menu para `/admin/` visível apenas para `is_staff`.
- Scaffold de UI integrado no app `accounts` para criar/editar usuários e atribuir grupos (se preferir não usar Admin).
- Script de inicialização (data migration ou management command) para criar grupos e permissões padrão.

---

Arquivo criado automaticamente pelo assistente. Se quiser, atualizo com exemplos específicos (nomes de grupos que você usa) ou crio um management command para provisionamento automático dos grupos/permissions.
