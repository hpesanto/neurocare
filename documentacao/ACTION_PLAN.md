# 🚨 LISTA DE AÇÕES URGENTES - Correção de Autenticação

**Data**: 2025-11-12  
**Prioridade**: 🔴 CRÍTICA  
**Tempo Estimado**: 2-3 horas

---

## ⚠️ PROBLEMA

**Você consegue acessar o menu e todas as páginas sem fazer login.**

Isso significa que QUALQUER PESSOA pode:
- ✅ Ver dados de pacientes (CPF, RG, endereço, etc.)
- ✅ Ver dados clínicos (evoluções, avaliações)
- ✅ Criar, editar e deletar registros
- ✅ Acessar dados financeiros

**Risco**: Violação de LGPD e dados sensíveis expostos!

---

## ✅ SOLUÇÃO RÁPIDA (2-3 horas)

### **OPÇÃO 1: Script Automatizado (RECOMENDADO)**

Execute o script Python que criamos:

```bash
# 1. Ver o que será alterado (sem modificar)
python add_login_required.py --dry-run

# 2. Criar backups e aplicar correções
python add_login_required.py --backup

# 3. Verificar mudanças
git diff

# 4. Testar
python manage.py runserver
```

### **OPÇÃO 2: Manual (se preferir)**

Siga os passos abaixo manualmente.

---

## 📋 PASSOS DETALHADOS (Manual)

### **PASSO 1: Corrigir Context Processor do Menu** (5 min)

Edite: `neurocare_project/context_processors.py`

**Linha 38**, MUDE DE:
```python
if parent_allowed or new_item.get("children") or new_item.get("url"):
    visible.append(new_item)
```

**PARA:**
```python
# Só mostra menu se usuário estiver autenticado
if user and user.is_authenticated:
    if parent_allowed or new_item.get("children"):
        visible.append(new_item)
```

---

### **PASSO 2: Proteger Home Page** (2 min)

Edite: `neurocare_project/urls.py`

**Linha 14**, MUDE DE:
```python
path("", TemplateView.as_view(template_name="home.html"), name="home"),
```

**PARA:**
```python
from django.contrib.auth.decorators import login_required

path("", login_required(TemplateView.as_view(template_name="home.html")), name="home"),
```

---

### **PASSO 3: Adicionar @login_required em Pacientes** (10 min)

Edite: `pacientes/views.py`

**No início do arquivo**, adicione o import:
```python
from django.contrib.auth.decorators import login_required
```

**Antes de CADA função**, adicione `@login_required`:
```python
@login_required
def list_pacientes(request):
    # código existente...

@login_required
def create_paciente(request):
    # código existente...

@login_required
def update_paciente(request, pk):
    # código existente...
```

---

### **PASSO 4: Repetir para TODOS os Apps** (1-2 horas)

Aplique o mesmo padrão do PASSO 3 em TODOS estes apps:

#### Apps CRÍTICOS (fazer primeiro):
- ✅ `evolucao_clinica/views.py`
- ✅ `avaliacao_neuropsicologica/views.py`
- ✅ `reabilitacao_neuropsicologica/views.py`
- ✅ `reabilitacao_sessao/views.py`
- ✅ `transacoes/views.py`
- ✅ `vendas/views.py`
- ✅ `vendas_geral/views.py`

#### Apps IMPORTANTES:
- ✅ `profissionais/views.py`
- ✅ `usuarios/views.py`
- ✅ `convenios/views.py`
- ✅ `contatos_emergencia/views.py`
- ✅ `paciente_servico/views.py`

#### Apps Cadastro:
- ✅ `faixas/views.py`
- ✅ `tipos_produto/views.py`
- ✅ `tipos_servico/views.py`
- ✅ `produtos/views.py`
- ✅ `formas_pagamento/views.py`
- ✅ `formas_cobranca_reabilitacao/views.py`
- ✅ `tipos_transacao/views.py`
- ✅ `status_pagamento/views.py`
- ✅ `status_objetivo_reabilitacao/views.py`
- ✅ `reabilitacao_objetivo/views.py`

**Padrão para TODOS:**
```python
# No início do arquivo
from django.contrib.auth.decorators import login_required

# Antes de cada função view
@login_required
def nome_da_funcao(request):
    # código...
```

---

### **PASSO 5: Testar** (10 min)

```bash
# 1. Inicie o servidor
python manage.py runserver

# 2. Abra navegador em modo anônimo/privado

# 3. Acesse http://127.0.0.1:8000/

# 4. ESPERADO: Deve redirecionar para /login/

# 5. Tente acessar /cadastro/pacientes/

# 6. ESPERADO: Deve redirecionar para /login/

# 7. Faça login com usuário válido

# 8. ESPERADO: Deve conseguir acessar as páginas
```

---

## 🧪 CHECKLIST DE VALIDAÇÃO

Após aplicar as correções, verifique:

### ✅ **Sem Login (Janela Anônima)**
- [ ] Acessar `/` redireciona para `/login/`
- [ ] Acessar `/cadastro/pacientes/` redireciona para `/login/`
- [ ] Acessar `/atendimento/evolucao-clinica/` redireciona para `/login/`
- [ ] Menu NÃO aparece no cabeçalho
- [ ] Só aparece link "Entrar"

### ✅ **Com Login**
- [ ] Consegue acessar home `/`
- [ ] Menu aparece baseado em permissões
- [ ] Consegue acessar páginas permitidas
- [ ] Link "Sair" funciona
- [ ] Após logout, redireciona para login

---

## 📊 ARQUIVOS MODIFICADOS

| Arquivo | Mudança | Impacto |
|---------|---------|---------|
| `context_processors.py` | Filtro de menu | Menu só para autenticados |
| `urls.py` | Home protegida | Home requer login |
| `pacientes/views.py` | +@login_required | Protege dados sensíveis |
| `evolucao_clinica/views.py` | +@login_required | Protege dados clínicos |
| `transacoes/views.py` | +@login_required | Protege dados financeiros |
| ... + ~20 arquivos | +@login_required | Proteção completa |

**Total**: ~23 arquivos modificados

---

## 🆘 TROUBLESHOOTING

### Problema: "No module named 'django.contrib.auth.decorators'"
**Solução**: Django está instalado? Execute:
```bash
pip install -r requirements.txt
```

### Problema: Erro de syntax após adicionar @login_required
**Solução**: Verifique se adicionou o import no início do arquivo:
```python
from django.contrib.auth.decorators import login_required
```

### Problema: Redirect loop (redireciona infinitamente)
**Solução**: Verifique se `LOGIN_URL` está configurado em `settings.py`:
```python
LOGIN_URL = "login"
```

### Problema: Login existe mas não consigo criar usuário
**Solução**: Crie superuser via terminal:
```bash
python manage.py createsuperuser
```

---

## 🎯 RESULTADOS ESPERADOS

### Antes (VULNERÁVEL ❌)
```
┌─────────────────────────┐
│  Navegador Anônimo      │
│  ↓                      │
│  http://localhost:8000/ │
│  ↓                      │
│  ✅ Home carregada       │
│  ✅ Menu visível         │
│  ✅ Dados acessíveis     │
└─────────────────────────┘
```

### Depois (PROTEGIDO ✅)
```
┌─────────────────────────┐
│  Navegador Anônimo      │
│  ↓                      │
│  http://localhost:8000/ │
│  ↓                      │
│  🔒 Redirect → /login/   │
│  ❌ Menu oculto          │
│  ❌ Dados protegidos     │
└─────────────────────────┘
```

---

## ⏱️ TEMPO ESTIMADO POR OPÇÃO

| Método | Tempo | Dificuldade |
|--------|-------|-------------|
| **Script Automatizado** | 15 min | ⭐ Fácil |
| **Manual - Apps Críticos** | 30 min | ⭐⭐ Médio |
| **Manual - Completo** | 2-3h | ⭐⭐⭐ Trabalhoso |

---

## 📞 PRECISA DE AJUDA?

Se encontrar problemas:

1. **Reverta mudanças**:
   ```bash
   git checkout .
   ```

2. **Tente o script automatizado** (mais seguro)

3. **Documente o erro** e peça ajuda da equipe

---

## 🎉 APÓS CONCLUIR

1. ✅ Commit das mudanças:
   ```bash
   git add .
   git commit -m "🔒 Add authentication to all views - Critical security fix"
   ```

2. ✅ Documente no CHANGELOG

3. ✅ Notifique a equipe

4. ✅ Planeje Fase 2 (permissões granulares)

---

**Documento**: Lista de Ações - Correção de Autenticação  
**Versão**: 1.0  
**Criado em**: 2025-11-12  
**Autor**: GitHub Copilot CLI  

**⚠️ ATENÇÃO**: Este é um problema CRÍTICO de segurança. Priorize esta correção!
