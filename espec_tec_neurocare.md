
hoes -> hpEkIq1029##

--acesse sua vps usando 
ssh root@187.127.37.57

ssh neurocare@187.127.37.57


admin / NeuroCare@Admin2026

NeuroCare@Admin2026

#NeuroCare — Descrição Técnica  
Arquitetura  
Aplicação web com arquitetura SPA + REST API, composta por 3 serviços independentes orquestrados via Docker Compose.  

Browser → nginx (porta 80/3000) → React SPA → proxy /api/ → Django/Gunicorn (porta 8000) → PostgreSQL (porta 5432)  

##Frontend
Item	Valor
Framework	React 18 com TypeScript
Build tool	Vite 8.1
UI framework	React Bootstrap 2.10 (Bootstrap 5)
Icones	Bootstrap Icons
HTTP client	Axios
State/cache	TanStack React Query (server state)
Roteamento	React Router DOM 7
Servidor producao	nginx:alpine (serve SPA + proxy reverso para API)

##Backend
Item	Valor
Linguagem	Python 3.12
Framework	Django 5.2.5
API	Django REST Framework 3.16
Autenticacao	JWT via djangorestframework-simplejwt 5.5
CORS	django-cors-headers 4.7
Filtros	django-filter 25.1
Excel export	openpyxl 3.1.5
WSGI server	Gunicorn 23.0 (3 workers)
ORM	Django ORM com models managed=False (tabelas pre-existentes)

##Banco de Dados
Item	Valor
SGBD	PostgreSQL 16
Schema	neurocare (via search_path)
PKs	UUID v4 em todas as tabelas
Tabelas de negocio	24 (todas managed=False)
Tabelas Django	6 (auth_user, sessions, migrations, etc. — managed=True)

##API
Tipo: REST (JSON) com paginação, filtros e busca
Base URL: /api/
Autenticação: JWT Bearer token (access 30min, refresh 7 dias)
Endpoints: 26 ViewSets (CRUD completo) + 1 export + 1 auth/me
Permissões: 3 perfis (Administrador, Psicólogo, Secretária) com isolamento de dados por profissional

##Infraestrutura
Item	Valor
Containerização	Docker + Docker Compose
Imagem backend	python:3.12-slim
Imagem frontend	node:20-alpine (build) → nginx:alpine (serve)
Imagem banco	postgres:16
Volumes	pgdata (banco), media_data (uploads PDF)

##Dependências (versões exatas)
###Backend (requirements.txt):
django==5.2.5
psycopg2-binary==2.9.10
python-dotenv==1.0.0
djangorestframework==3.16.0
djangorestframework-simplejwt==5.5.0
django-cors-headers==4.7.0
django-filter==25.1
gunicorn==23.0.0
openpyxl==3.1.5

###Frontend (package.json):
react: ^18.x
react-dom: ^18.x
react-router-dom: ^7.x
react-bootstrap: ^2.10.x
bootstrap: ^5.3.x
bootstrap-icons: ^1.x
axios: ^1.x
@tanstack/react-query: ^5.x
typescript: ^5.x
vite: ^8.1.x