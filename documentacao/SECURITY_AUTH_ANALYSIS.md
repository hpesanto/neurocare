# 🔒 ANÁLISE DE SEGURANÇA: Problema de Autenticação

**Data**: 2025-11-12  
**Severidade**: 🔴 **CRÍTICA**  
**Status**: ⚠️ Vulnerável

---

## 🐛 PROBLEMA IDENTIFICADO

### Acesso sem login permitido em TODAS as views

**Sintoma**: Usuários conseguem acessar o menu e todas as páginas sem fazer login.

**Causa Raiz**: Nenhuma view do sistema usa `@login_required` ou verificações de autenticação.

---

## 🔍 ANÁLISE DETALHADA

### 1. Views SEM proteção de autenticação

Todos os apps têm views completamente desprotegidas:

#### ❌ **pacientes/views.py**
```python
def list_pacientes(request):  # SEM @login_required
    # Qualquer pessoa pode ver lista de pacientes
    
def create_paciente(request):  # SEM @login_required
    # Qualquer pessoa pode criar pacientes
    
def update_paciente(request, pk):  # SEM @login_required
    # Qualquer pessoa pode editar pacientes
```

#### ❌ **evolucao_clinica/views.py**
```python
def list_evolucao(request):  # SEM @login_required
    # Dados clínicos sensíveis acessíveis sem login!
    
def create_evolucao(request):  # SEM @login_required
def update_evolucao(request, pk):  # SEM @login_required
```

#### ❌ **profissionais/views.py**
```python
def list_profissionais(request):  # SEM @login_required
def create_profissional(request):  # SEM @login_required
def update_profissional(request, pk):  # SEM @login_required
```

#### ❌ **vendas/views.py**
```python
def list_vendas(request):  # SEM @login_required
def create_venda(request):  # SEM @login_required
def update_venda(request, pk):  # SEM @login_required
```

**E todos os outros apps seguem o mesmo padrão!**

---

### 2. Menu visível sem autenticação

O `context_processors.py` filtra menu por permissões, mas tem uma falha:

```python
# Linha 38 em context_processors.py
if parent_allowed or new_item.get("children") or new_item.get("url"):
    visible.append(new_item)
```

**Problema**: Se o item tem `url`, ele é exibido mesmo se usuário não estiver autenticado!

**Resultado**: Menu aparece para usuários não autenticados.

---

### 3. Home page acessível sem login

```python
# urls.py linha 14
path("", TemplateView.as_view(template_name="home.html"), name="home"),
```

**Problema**: Não exige autenticação.

---

### 4. Template base.html não força login

O template mostra o menu independentemente de autenticação:

```html
<!-- base.html linha 22 -->
{% include 'includes/menu.html' %}
```

Não há verificação `{% if user.is_authenticated %}` antes do menu.

---

## 🔥 IMPACTO DE SEGURANÇA

### **GRAVÍSSIMO** - Violações de Privacidade e Conformidade

1. ✅ **Dados de Pacientes Expostos (LGPD/HIPAA)**
   - Qualquer pessoa pode ver lista de pacientes
   - Acesso a dados pessoais sensíveis (CPF, RG, endereço, telefone)
   - Acesso a dados clínicos (evoluções, avaliações neuropsicológicas)

2. ✅ **Manipulação de Dados**
   - Qualquer pessoa pode criar/editar/deletar registros
   - Risco de sabotagem ou alteração maliciosa

3. ✅ **Dados Financeiros Expostos**
   - Transações financeiras visíveis
   - Informações de pagamento acessíveis

4. ✅ **Não Conformidade Legal**
   - Violação da LGPD (Lei Geral de Proteção de Dados)
   - Se aplicável: Violação de HIPAA (dados de saúde)
   - Passível de multas pesadas

---

## ✅ PLANO DE CORREÇÃO

### 🔴 **PRIORIDADE CRÍTICA - Implementar IMEDIATAMENTE**

### **Fase 1: Proteção Básica (1-2 horas)**

#### 1.1 Adicionar `@login_required` em TODAS as views

**Apps a corrigir** (em ordem de prioridade):
1. ✅ **pacientes** (dados mais sensíveis)
2. ✅ **evolucao_clinica** (dados clínicos)
3. ✅ **avaliacao_neuropsicologica** (dados clínicos)
4. ✅ **reabilitacao_neuropsicologica**
5. ✅ **reabilitacao_sessao**
6. ✅ **profissionais**
7. ✅ **transacoes** (dados financeiros)
8. ✅ **vendas** (dados financeiros)
9. ✅ **vendas_geral** (dados financeiros)
10. ✅ Todos os outros apps restantes

**Exemplo de correção**:

```python
# ANTES (VULNERÁVEL)
def list_pacientes(request):
    # código...

# DEPOIS (PROTEGIDO)
from django.contrib.auth.decorators import login_required

@login_required
def list_pacientes(request):
    # código...
```

#### 1.2 Proteger home page

```python
# urls.py
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_required(TemplateView.as_view(template_name="home.html")), name="home"),
    path("", include("accounts.urls")),
]
```

#### 1.3 Corrigir filtro do menu

```python
# context_processors.py linha 38
# ANTES:
if parent_allowed or new_item.get("children") or new_item.get("url"):
    visible.append(new_item)

# DEPOIS:
# Só inclui se usuário autenticado E (permissões OK OU tem children)
if user and user.is_authenticated:
    if parent_allowed or new_item.get("children"):
        visible.append(new_item)
```

---

### **Fase 2: Proteção Avançada (2-4 horas)**

#### 2.1 Adicionar verificação de permissões nas views

```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('pacientes.view_paciente', raise_exception=True)
def list_pacientes(request):
    # código...

@login_required
@permission_required('pacientes.add_paciente', raise_exception=True)
def create_paciente(request):
    # código...

@login_required
@permission_required('pacientes.change_paciente', raise_exception=True)
def update_paciente(request, pk):
    # código...
```

#### 2.2 Criar template de erro 403

```html
<!-- templates/403.html -->
<!DOCTYPE html>
<html>
<head><title>Acesso Negado</title></head>
<body>
    <h1>🚫 Acesso Negado</h1>
    <p>Você não tem permissão para acessar esta página.</p>
    <a href="{% url 'home' %}">Voltar à Home</a>
</body>
</html>
```

#### 2.3 Adicionar middleware de sessão segura

```python
# settings.py
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Em produção com HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True  # Em produção com HTTPS
```

#### 2.4 Configurar timeout de sessão

```python
# settings.py
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True  # Renova a cada requisição
```

---

### **Fase 3: Auditoria e Monitoramento (4-8 horas)**

#### 3.1 Adicionar logging de acessos

```python
# Criar middleware custom para log de acessos
# neurocare_project/middleware.py

import logging

logger = logging.getLogger('security')

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        username = user.username if user and user.is_authenticated else 'anonymous'
        
        logger.info(
            f"Access: {request.method} {request.path} by {username} from {request.META.get('REMOTE_ADDR')}"
        )
        
        response = self.get_response(request)
        return response
```

#### 3.2 Configurar logging detalhado

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'security_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
        },
    },
    'loggers': {
        'security': {
            'handlers': ['security_file'],
            'level': 'INFO',
        },
    },
}
```

#### 3.3 Adicionar auditoria no banco

```python
# Criar app de auditoria
# auditoria/models.py

from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # CREATE, UPDATE, DELETE, VIEW
    model_name = models.CharField(max_length=100)
    object_id = models.UUIDField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    changes = models.JSONField(null=True)
    
    class Meta:
        db_table = 'tb_audit_log'
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1 (URGENTE - Fazer AGORA)
- [ ] Adicionar `@login_required` em pacientes/views.py
- [ ] Adicionar `@login_required` em evolucao_clinica/views.py
- [ ] Adicionar `@login_required` em avaliacao_neuropsicologica/views.py
- [ ] Adicionar `@login_required` em reabilitacao_neuropsicologica/views.py
- [ ] Adicionar `@login_required` em reabilitacao_sessao/views.py
- [ ] Adicionar `@login_required` em profissionais/views.py
- [ ] Adicionar `@login_required` em transacoes/views.py
- [ ] Adicionar `@login_required` em vendas/views.py
- [ ] Adicionar `@login_required` em vendas_geral/views.py
- [ ] Adicionar `@login_required` em todos os outros apps
- [ ] Proteger home page com `login_required`
- [ ] Corrigir filtro do menu em `context_processors.py`
- [ ] Testar login/logout
- [ ] Verificar que páginas exigem autenticação

### Fase 2 (Importante - 24-48h)
- [ ] Adicionar verificação de permissões nas views críticas
- [ ] Criar template 403.html
- [ ] Configurar cookies de sessão seguros
- [ ] Configurar timeout de sessão
- [ ] Testar permissões

### Fase 3 (Recomendado - 1 semana)
- [ ] Criar middleware de logging
- [ ] Configurar logs de segurança
- [ ] Criar sistema de auditoria
- [ ] Revisar todos os acessos
- [ ] Documentar políticas de acesso

---

## 🧪 TESTES NECESSÁRIOS

### Testes Manuais (Após Fase 1)

1. **Teste de Acesso Sem Login**
   ```
   1. Abrir janela anônima/incógnita
   2. Acessar http://localhost:8000/
   3. ESPERADO: Redirecionar para /login/
   4. Tentar acessar /cadastro/pacientes/
   5. ESPERADO: Redirecionar para /login/
   ```

2. **Teste de Menu**
   ```
   1. Visitar site sem login
   2. ESPERADO: Menu não deve aparecer
   3. Fazer login
   4. ESPERADO: Menu aparece baseado em permissões
   ```

3. **Teste de Logout**
   ```
   1. Fazer login
   2. Acessar página qualquer
   3. Fazer logout
   4. Tentar acessar página novamente
   5. ESPERADO: Redirecionar para /login/
   ```

### Testes Automatizados (Criar depois)

```python
# tests/test_security.py

from django.test import TestCase, Client
from django.urls import reverse

class SecurityTests(TestCase):
    def test_home_requires_login(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/login/', response.url)
    
    def test_pacientes_list_requires_login(self):
        c = Client()
        response = c.get('/cadastro/pacientes/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
```

---

## 🚨 AÇÕES IMEDIATAS (FAZER AGORA!)

### Se sistema está em PRODUÇÃO:

1. **DESLIGAR O SERVIDOR IMEDIATAMENTE**
   ```bash
   # Pare o servidor Django
   pkill -f "python manage.py runserver"
   ```

2. **Notificar stakeholders**
   - Informar equipe técnica
   - Notificar responsável legal/compliance
   - Preparar comunicado (se necessário por LGPD)

3. **Verificar logs de acesso**
   ```bash
   # Verificar acessos suspeitos
   grep "GET /cadastro/pacientes/" logs/access.log
   ```

4. **Aplicar correções da Fase 1**
   - Prioridade máxima
   - Testar em ambiente de teste primeiro

5. **Fazer deploy das correções**
   - Deploy urgente em produção
   - Testar acesso

6. **Documentar incidente**
   - Data/hora da descoberta
   - Período de exposição
   - Dados potencialmente comprometidos
   - Ações tomadas

### Se sistema está em DESENVOLVIMENTO:

1. **Aplicar correções da Fase 1**
2. **Testar completamente**
3. **NÃO colocar em produção até corrigir**

---

## 📊 RESUMO EXECUTIVO

| Item | Status Atual | Risco | Ação |
|------|-------------|-------|------|
| Autenticação em views | ❌ Ausente | 🔴 CRÍTICO | Adicionar `@login_required` |
| Filtro de menu | ⚠️ Falho | 🔴 CRÍTICO | Corrigir lógica |
| Home protegida | ❌ Não | 🔴 CRÍTICO | Adicionar autenticação |
| Permissões granulares | ❌ Ausente | 🟡 ALTO | Implementar |
| Auditoria | ❌ Ausente | 🟡 ALTO | Criar sistema |
| Logs de segurança | ⚠️ Parcial | 🟡 ALTO | Melhorar |

---

## 📞 CONTATOS EMERGENCIAIS

Em caso de violação de dados confirmada:
- **ANPD** (Autoridade Nacional de Proteção de Dados): https://www.gov.br/anpd/
- **Prazo para notificação LGPD**: Até 72 horas após ciência
- **Documentação necessária**: Logs, impacto, medidas tomadas

---

**Preparado por**: GitHub Copilot CLI  
**Última atualização**: 2025-11-12  
**Versão**: 1.0  
**Classificação**: 🔴 CRÍTICO - CONFIDENCIAL
