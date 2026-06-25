# NeuroCare

Sistema de gestao clinica para neuropsicologia — controle de pacientes, avaliacoes, reabilitacao, financeiro e vendas.

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | Django 5.2 + Django REST Framework + SimpleJWT |
| Frontend | React 18 + TypeScript + Vite + React Bootstrap 5 |
| Banco | PostgreSQL 16 (schema `neurocare`) |
| Infra | Docker Compose (3 servicos) |

## Quick Start (Docker)

```bash
git clone https://github.com/hpesanto/neurocare.git
cd neurocare
docker compose up --build
```

Acesse:
- **App:** http://localhost:3000
- **API:** http://localhost:8000/api/
- **Admin Django:** http://localhost:8000/admin/
- **Login:** `admin` / `admin123`

O Docker cria automaticamente o banco, schema, tabelas, dados de referencia e o superusuario.

## Quick Start (Dev local)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

O Vite faz proxy de `/api` para `localhost:8000` automaticamente.

## Estrutura do Projeto

```
neurocare/
├── docker-compose.yml          # Orquestracao dos 3 servicos
├── docker/postgres/init.sql    # DDL + seed data
├── .env.example                # Variaveis de ambiente
│
├── backend/                    # Django REST API
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── neurocare_project/      # Settings, URLs, WSGI
│   ├── pacientes/              # Models principais + serializers + viewsets
│   ├── profissionais/          # Profissionais (tb_usuario)
│   ├── evolucao_clinica/       # Evolucao clinica
│   ├── avaliacao_neuropsicologica/
│   ├── reabilitacao_neuropsicologica/
│   ├── reabilitacao_objetivo/
│   ├── reabilitacao_sessao/
│   ├── transacoes/             # Transacoes financeiras
│   ├── vendas/                 # Vendas vinculadas ao paciente
│   ├── vendas_geral/           # Vendas gerais do consultorio
│   └── ...                     # Lookup tables (convenios, formas_pagamento, etc.)
│
└── frontend/                   # React SPA
    ├── Dockerfile
    ├── nginx.conf              # Proxy /api/ -> backend
    └── src/
        ├── api/                # Axios client + endpoints
        ├── auth/               # JWT login, context, protected routes
        ├── components/         # DataTable, FormModal, FkSelect, Layout
        ├── hooks/              # useCrud, useOptions
        ├── pages/              # Paginas organizadas por modulo
        └── types/              # Interfaces TypeScript
```

## API

Todos os endpoints estao sob `/api/` e requerem autenticacao JWT.

### Autenticacao

```bash
# Obter token
POST /api/token/
{"username": "admin", "password": "admin123"}
# Retorna: {"access": "...", "refresh": "..."}

# Refresh
POST /api/token/refresh/
{"refresh": "..."}

# Usuario atual
GET /api/auth/me/
Authorization: Bearer <access_token>
```

### Endpoints REST (CRUD completo)

| Grupo | Endpoint | Model |
|-------|----------|-------|
| **Cadastro** | `/api/pacientes/` | Paciente |
| | `/api/profissionais/` | Profissional |
| | `/api/convenios/` | Convenio |
| | `/api/formas-pagamento/` | FormaPagamento |
| | `/api/tipos-produto/` | TipoProduto |
| | `/api/produtos/` | Produto |
| | `/api/faixas-etarias/` | FaixaEtaria |
| | `/api/tipos-servico/` | TipoServico |
| | `/api/contatos-emergencia/` | ContatoEmergencia |
| | `/api/paciente-servico/` | PacienteServico |
| | `/api/perfis-acesso/` | PerfilAcesso |
| | `/api/usuarios/` | Usuario |
| **Atendimento** | `/api/evolucao-clinica/` | EvolucaoClinica |
| | `/api/avaliacao-neuropsicologica/` | AvaliacaoNeuropsicologica |
| | `/api/reabilitacao-neuropsicologica/` | ReabilitacaoNeuropsicologica |
| | `/api/reabilitacao-objetivo/` | ReabilitacaoObjetivo |
| | `/api/reabilitacao-sessao/` | ReabilitacaoSessao |
| | `/api/status-objetivo-reabilitacao/` | StatusObjetivoReabilitacao |
| **Financeiro** | `/api/transacoes/` | TransacaoFinanceira |
| | `/api/tipos-transacao/` | TipoTransacaoFinanceira |
| | `/api/status-pagamento/` | StatusPagamento |
| | `/api/formas-cobranca-reabilitacao/` | FormaCobrancaReabilitacao |
| **Vendas** | `/api/vendas-vinculadas/` | VendaVinculada |
| | `/api/vendas-geral/` | VendaGeral |
| | `/api/vendas-geral-itens/` | VendaGeralItem |

Todos suportam: `GET` (list/detail), `POST`, `PATCH`, `DELETE`.

Paginacao: `?page=1&page_size=25` (max 1000).
Busca: `?search=termo`.
Filtros: `?campo=valor` (varia por endpoint).

## Variaveis de Ambiente

| Variavel | Default | Descricao |
|----------|---------|-----------|
| `NEUROCARE_SECRET_KEY` | `please-change-me...` | Django SECRET_KEY |
| `NEUROCARE_DEBUG` | `false` | Debug mode |
| `NEUROCARE_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hosts permitidos |
| `POSTGRES_DB` | `postgres` | Nome do banco |
| `POSTGRES_USER` | `postgres` | Usuario do banco |
| `POSTGRES_PASSWORD` | `postgres` | Senha do banco |
| `POSTGRES_HOST` | `localhost` | Host do banco |
| `POSTGRES_PORT` | `5432` | Porta do banco |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,...` | Origens CORS permitidas |

## Banco de Dados

O sistema usa PostgreSQL com schema `neurocare`. Todos os models Django sao `managed=False` — as tabelas sao criadas pelo script `docker/postgres/init.sql`, nao pelas migrations.

As migrations do Django criam apenas as tabelas internas (`auth_user`, `django_session`, etc.).

## Docker

```bash
# Subir tudo
docker compose up --build -d

# Ver logs
docker compose logs -f backend

# Parar
docker compose down

# Reset completo (apaga dados)
docker compose down -v
docker compose up --build
```

Servicos:
- **postgres** (porta 5432) — banco com schema e seed data
- **backend** (porta 8000) — Django/Gunicorn com 3 workers
- **frontend** (porta 3000) — nginx servindo React + proxy para API
