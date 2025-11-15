# 📊 Estrutura Modular de NeuroCare

Sim! **Cada subdiretório dentro de `neurocare/` é um módulo Django (app)** da aplicação.

---

## 🏗️ Arquitetura da Aplicação

A aplicação segue o **padrão modular do Django**, onde cada funcionalidade é organizada em uma aplicação independente com:
- `models.py` - Estrutura de dados
- `views.py` - Lógica de apresentação
- `urls.py` - Roteamento
- `forms.py` - Formulários
- `migrations/` - Histórico de mudanças no banco de dados
- `templates/` - Templates HTML (organizados em subpastas)

---

## 📋 Módulos Registrados em `INSTALLED_APPS`

Estes são os módulos **ativos** (registrados em `neurocare_project/settings.py`):

### 🔐 Autenticação
- **`accounts`** - Login, logout, gerenciamento de sessão

### 👥 Cadastro (Dados Básicos)
- **`pacientes`** - Gestão de pacientes
- **`profissionais`** - Gestão de profissionais
- **`usuarios`** - Usuários do sistema
- **`convenios`** - Convênios e seguradoras
- **`faixas`** - Faixas etárias
- **`contatos_emergencia`** - Contatos de emergência
- **`tipos_produto`** - Tipos de produtos/serviços
- **`tipos_servico`** - Tipos de serviços
- **`formas_pagamento`** - Formas de pagamento
- **`produtos`** - Produtos oferecidos
- **`paciente_servico`** - Vínculo paciente-serviço

### 🏥 Atendimento Clínico
- **`evolucao_clinica`** - Evolução clínica dos pacientes
- **`avaliacao_neuropsicologica`** - Avaliações neuropsicológicas
- **`reabilitacao_neuropsicologica`** - Planos de reabilitação neuropsicológica
- **`reabilitacao_sessao`** - Sessões de reabilitação
- **`reabilitacao_objetivo`** - Objetivos de reabilitação
- **`status_objetivo_reabilitacao`** - Status dos objetivos

### 💰 Financeiro
- **`transacoes`** - Transações financeiras
- **`tipos_transacao`** - Tipos de transações
- **`status_pagamento`** - Status de pagamento
- **`formas_cobranca_reabilitacao`** - Formas de cobrança reabilitação
- **`reabilitacao_neuropsicologica`** - Cobrança de reabilitação
- **`vendas`** - Vendas vinculadas ao paciente
- **`vendas_geral`** - Vendas gerais (consultório)

---

## 🗂️ Outros Diretórios (NÃO são módulos)

### 🔧 Infraestrutura
- **`neurocare_project/`** - Configuração central da aplicação Django
  - `settings.py` - Configurações globais
  - `urls.py` - URLs principais
  - `views.py` - Views genéricas
  - `context_processors.py` - Processadores de contexto
  - `menu_config.py` - Configuração do menu
  - `placeholders.py` - Páginas placeholder

### 📁 Recursos Estáticos
- **`static/`** - Arquivos estáticos (CSS, JS, imagens)
  - `css/` - Folhas de estilo
  - `js/` - JavaScript
  - `images/` - Imagens (logo, ícones, etc)

### 🎨 Templates
- **`templates/`** - Templates HTML compartilhados
  - Subpastas por módulo para organização
  - `base.html` - Template base
  - `home.html` - Página inicial
  - `includes/` - Componentes reutilizáveis
  - `shared/` - Templates compartilhados

### 📚 Documentação
- **`documentacao/`** - Documentação do projeto

### 🐍 Python Virtual Environment
- **`psico/`** - Ambiente virtual Python (não deve estar versionado normalmente)

---

## 🔗 Estrutura de Dependências entre Módulos

```
┌─────────────────────────────────────────────┐
│         neurocare_project (Config)          │
│  - settings.py (INSTALLED_APPS)             │
│  - urls.py (routing)                        │
│  - context_processors.py (menu)             │
└─────────────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
    ┌──────────┐              ┌──────────────┐
    │ accounts │              │ pacientes    │
    │ (Login)  │              │ (Cadastro)   │
    └──────────┘              └──────────────┘
        │                             │
        └──────────────┬──────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌────────┐  ┌──────────┐  ┌──────────┐
   │Atendim.│  │Cadastros │  │Financeiro│
   │Clínico │  │Básicos   │  │          │
   └────────┘  └──────────┘  └──────────┘
```

---

## 📝 Padrão de Cada Módulo

### Estrutura Típica
```
módulo/
├── migrations/          # Histórico de mudanças no DB
├── templatetags/        # Template tags customizadas (opcional)
├── admin.py            # Configuração do admin
├── apps.py             # Configuração da app
├── forms.py            # Formulários
├── models.py           # Modelos de dados
├── urls.py             # URLs do módulo
├── views.py            # Views/Controllers
├── views.py.backup     # Backup (alguns módulos)
└── __init__.py
```

---

## 🔌 Como um Módulo é Integrado

### 1️⃣ **Registrado em `INSTALLED_APPS`** (settings.py)
```python
INSTALLED_APPS = [
    "accounts",
    "pacientes",
    "profissionais",
    # ...
]
```

### 2️⃣ **URLs Incluídas** (neurocare_project/urls.py)
```python
maybe_include("cadastro/pacientes/", "pacientes.urls")
maybe_include("cadastro/profissionais/", "profissionais.urls")
```

### 3️⃣ **Templates Organizados** (templates/)
```
templates/
├── pacientes/           # Templates de pacientes
├── profissionais/       # Templates de profissionais
└── ...
```

### 4️⃣ **Estáticos Organizados** (static/)
```
static/
├── css/
├── js/
└── images/
```

---

## 📊 Módulos Ativos vs Inativos

### ✅ Módulos Instalados (INSTALLED_APPS)
- accounts
- pacientes
- profissionais
- evolucao_clinica
- avaliacao_neuropsicologica
- status_objetivo_reabilitacao
- formas_cobranca_reabilitacao
- reabilitacao_neuropsicologica
- reabilitacao_sessao
- reabilitacao_objetivo
- vendas
- vendas_geral
- transacoes
- tipos_transacao
- status_pagamento

### ⚠️ Módulos de Suporte (não em INSTALLED_APPS)
```
Alguns módulos existem como diretórios mas podem estar
incompletos ou não registrados formalmente.
```

---

## 🎯 Organização Lógica por Negócio

### **Tier 1: Autenticação**
- `accounts` - Acesso à plataforma

### **Tier 2: Dados Mestres (Cadastros)**
- `pacientes` - Dados dos pacientes
- `profissionais` - Dados dos profissionais
- `usuarios` - Usuários do sistema
- `convenios` - Convênios
- `faixas` - Faixas etárias
- E outros (tipos, formas, etc)

### **Tier 3: Operacional (Negócio)**
- `evolucao_clinica` - Acompanhamento clínico
- `avaliacao_neuropsicologica` - Diagnósticos
- `reabilitacao_*` - Planos e sessões

### **Tier 4: Financeiro**
- `transacoes` - Movimentações
- `vendas*` - Vendas
- `status_pagamento` - Controle de pagamentos

---

## 🔄 Fluxo Típico de Uma Requisição

```
1. Usuário acessa http://127.0.0.1:8000/cadastro/pacientes/

2. neurocare_project/urls.py
   ↓
   maybe_include("cadastro/pacientes/", "pacientes.urls")

3. pacientes/urls.py
   ↓
   path("", list_pacientes, name="list")

4. pacientes/views.py
   ↓
   list_pacientes(request) → busca em pacientes/models.py

5. Renderiza templates/pacientes/list.html

6. Retorna HTML ao usuário
```

---

## ✅ Benefícios da Arquitetura Modular

✅ **Isolamento** - Cada módulo é independente  
✅ **Reutilização** - Componentes podem ser compartilhados  
✅ **Escalabilidade** - Fácil adicionar novos módulos  
✅ **Manutenção** - Código organizado e fácil de encontrar  
✅ **Testes** - Cada módulo pode ser testado isoladamente  
✅ **Django Padrão** - Segue convenções do framework  

---

## 🚀 Como Adicionar um Novo Módulo

```bash
# 1. Criar a app
python manage.py startapp novo_modulo

# 2. Registrar em INSTALLED_APPS (settings.py)
INSTALLED_APPS = [
    ...
    "novo_modulo",
]

# 3. Criar models, views, urls, forms
# 4. Criar migrations
python manage.py makemigrations

# 5. Aplicar migrations
python manage.py migrate

# 6. Incluir URLs em neurocare_project/urls.py
maybe_include("caminho/", "novo_modulo.urls")

# 7. Criar templates em templates/novo_modulo/
```

---

## 📌 Resumo

**SIM**, cada subdiretório é um módulo Django completo e independente, organizado por **domínio de negócio** (autenticação, cadastros, atendimento clínico, financeiro).

A aplicação segue a **arquitetura modular recomendada pelo Django**, permitindo escalabilidade e manutenção eficiente.

**Data**: 2025-11-15  
**Versão**: 1.0
