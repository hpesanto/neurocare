# NeuroCare (inicial)

Quick start (Windows PowerShell)

1. Ative o ambiente virtual (ex.: `psico` já incluído no workspace):

```powershell
.\psico\Scripts\Activate.ps1
```

2. Instale dependências (se necessário):

```powershell
pip install -r requirements.txt
```

3. Banco de dados — Postgres (recomendado) ou SQLite (fallback)

O projeto tenta conectar ao PostgreSQL usando as credenciais definidas em `neurocare_project/settings.py`.

Para usar PostgreSQL localmente:

1. Instale um servidor Postgres (p.ex. PostgreSQL para Windows) e crie um banco/usuário:

```powershell
# Exemplo usando psql (executar no prompt do Postgres ou no PowerShell se psql estiver no PATH)
psql -U postgres
CREATE DATABASE postgres;
CREATE USER psico WITH PASSWORD 'psico10!';
GRANT ALL PRIVILEGES ON DATABASE postgres TO psico;
\q
```

2. Ajuste `neurocare_project/settings.py` (ou use variáveis de ambiente) para apontar para o banco criado.

3. Rode migrações:

```powershell
python manage.py migrate


```

Se a conexão com Postgres falhar por qualquer motivo, o projeto cairá para SQLite automaticamente (arquivo `db.sqlite3` no diretório do projeto).

Variáveis de ambiente (recomendado)

O projeto agora lê as principais configurações (SECRET_KEY, DEBUG e configurações do banco) a partir de variáveis de ambiente. Existe um exemplo de arquivo `.env` chamado `.env.example` no repositório.

Exemplo rápido (PowerShell) — exporte as variáveis antes de executar o servidor:

```powershell
$env:NEUROCARE_SECRET_KEY = "uma_chave_segura_aqui"
$env:NEUROCARE_DEBUG = "false"
$env:NEUROCARE_DB_NAME = "postgres"
$env:NEUROCARE_DB_USER = "postgres"
$env:NEUROCARE_DB_PASSWORD = "postgres"
$env:NEUROCARE_DB_HOST = "localhost"
$env:NEUROCARE_DB_PORT = "5432"
```

Você também pode usar ferramentas como `python-dotenv` (carregar variáveis de um `.env`) em desenvolvimento; não comite um `.env` com segredos reais.

4. Crie um superusuário (interativo):

```powershell
python manage.py createsuperuser
```

5. Inicie o servidor de desenvolvimento:

```powershell
python manage.py runserver

python manage.py runserver --noreload
```

Abra http://127.0.0.1:8000/ no navegador.

Menu e submenus

O menu de navegação é configurado em `neurocare_project/menu_config.py` e agora suporta subitens (children). Cada item pode ter:

- `title`: texto exibido
- `url`: rota do link (opcional)
- `permissions`: lista de permissions Django (opcional)
- `children`: lista de subitens com a mesma estrutura

Comportamento de permissões implementado: "bloqueio apenas no nível de filhos" — isto é, um pai com permissões não impede que filhos apareçam se os filhos tiverem suas próprias permissões e essas forem atendidas. Filhos são avaliados independentemente.

Exemplo:

```python
MENU = [
	{'title': 'Home', 'url': '/'},
	{
		'title': 'Agendamentos',
		'url': '#',
		'permissions': ['accounts.view_agendamento'],
		'children': [
			{'title': 'Novo', 'url': '/agendamentos/novo/', 'permissions': ['appointments.add']},
			{'title': 'Listar', 'url': '/agendamentos/', 'permissions': ['appointments.view']},
		]
	},
]
```

Arquivos principais relacionados ao menu:

- `neurocare_project/menu_config.py` — defina o menu aqui.
- `neurocare_project/context_processors.py` — filtra recursivamente os itens e expõe `MENU_ITEMS` aos templates.
- `templates/includes/menu.html` e `templates/includes/menu_item.html` — templates que renderizam o menu recursivamente.

Notas de segurança e produção

- Troque `SECRET_KEY` em `neurocare_project/settings.py` por um valor seguro antes de colocar em produção.
- Não confie no fallback automático em produção: configure explicitamente o banco e variáveis de ambiente.
- Evite deixar senhas em arquivos; prefira variáveis de ambiente ou um secrets manager.

Se quiser, eu posso adicionar instruções para usar variáveis de ambiente (dotenv) ou mostrar como criar o superuser de forma não interativa em scripts CI/CD.

