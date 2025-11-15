# 🔐 DIAGNÓSTICO: Problema de Login

**Data**: 2025-11-12  
**Status**: 🔴 IDENTIFICADO

---

## 🐛 PROBLEMA IDENTIFICADO

### O sistema NÃO consegue fazer login porque:

1. **Model Usuario customizado** existe em `pacientes/models.py` (tabela `tb_usuario`)
2. **Django Auth** está configurado para usar tabela padrão `auth_user`
3. **Incompatibilidade**: O usuário "psico" está na tabela `tb_usuario`, mas o Django procura em `auth_user`

---

## 🔍 ANÁLISE TÉCNICA

### Tabela Atual (tb_usuario)
```python
class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=100, unique=True)  # ← Campo customizado!
    senha_hash = models.CharField(max_length=255)           # ← Não é hash Django!
    ativo = models.BooleanField(default=True)
```

### Tabela Esperada pelo Django (auth_user)
```sql
-- Estrutura padrão do Django
id, username, password, email, first_name, last_name, is_staff, is_active, ...
```

**Incompatível!** 😱

---

## ✅ SOLUÇÕES POSSÍVEIS

### **SOLUÇÃO 1: Criar usuário na tabela auth_user (RÁPIDO)** ⚡

Crie um superuser que o Django reconhece:

```bash
python manage.py createsuperuser

# Preencha:
# Username: admin
# Email: admin@neurocare.com
# Password: [escolha uma senha forte]
```

**Prós**: 
- ✅ Rápido (2 minutos)
- ✅ Funciona imediatamente
- ✅ Não modifica código

**Contras**:
- ❌ Cria sistema de usuários paralelo
- ❌ Usuário "psico" da tb_usuario não funciona
- ❌ Não é solução definitiva

---

### **SOLUÇÃO 2: Backend de Autenticação Customizado (RECOMENDADO)** 🎯

Crie um backend que autentica na tabela `tb_usuario`:

#### Passo 1: Criar backend customizado

Crie arquivo `pacientes/auth_backends.py`:

```python
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Usuario
import hashlib


class UsuarioBackend(BaseBackend):
    """
    Autentica usando a tabela tb_usuario customizada.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Busca usuário na tabela tb_usuario
            usuario = Usuario.objects.get(login=username, ativo=True)
            
            # Verifica senha (ajuste conforme seu hash)
            # Se for MD5:
            password_hash = hashlib.md5(password.encode()).hexdigest()
            # Se for SHA256:
            # password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if usuario.senha_hash == password_hash:
                # Cria/atualiza usuário Django paralelo
                django_user, created = User.objects.get_or_create(
                    username=usuario.login,
                    defaults={
                        'email': usuario.email,
                        'first_name': usuario.nome_completo.split()[0] if usuario.nome_completo else '',
                        'is_active': usuario.ativo,
                    }
                )
                return django_user
                
        except Usuario.DoesNotExist:
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```

#### Passo 2: Configurar em settings.py

Adicione ao `settings.py`:

```python
AUTHENTICATION_BACKENDS = [
    'pacientes.auth_backends.UsuarioBackend',  # Seu backend customizado
    'django.contrib.auth.backends.ModelBackend',  # Fallback padrão
]
```

**Prós**:
- ✅ Usuário "psico" funciona
- ✅ Mantém tabela tb_usuario
- ✅ Compatível com Django Auth

**Contras**:
- ⚠️ Requer configuração (15 min)
- ⚠️ Precisa saber qual algoritmo de hash usado

---

### **SOLUÇÃO 3: Migrar para AbstractUser do Django (IDEAL)** 🏆

Refatore o sistema para usar autenticação Django nativa:

**Prós**:
- ✅ Solução definitiva e profissional
- ✅ Usa todas as features do Django
- ✅ Mais seguro (hash bcrypt/argon2)
- ✅ Integração completa com admin

**Contras**:
- ❌ Requer mais tempo (2-4 horas)
- ❌ Precisa migração de dados
- ❌ Requer testes extensivos

---

## 🚀 AÇÃO IMEDIATA (AGORA!)

### Opção A: Login Rápido (2 min)

```bash
# Criar superuser Django
python manage.py createsuperuser

# Quando pedir:
Username: admin
Email: admin@neurocare.com  
Password: [senha forte]
Password (again): [repita a senha]

# Testar login
python manage.py runserver
# Acesse: http://127.0.0.1:8000/login/
# Use: admin / [sua senha]
```

### Opção B: Descobrir hash do usuário "psico" (5 min)

```bash
# Conecte ao PostgreSQL
psql -U postgres -d postgres

# Veja o usuário psico
SELECT login, senha_hash FROM neurocare.tb_usuario WHERE login = 'psico';

# Anote o hash e compare com:
# - MD5 de "psico10!": [resultado]
# - SHA256 de "psico10!": [resultado]
```

Depois me diga:
1. Qual o valor de `senha_hash`?
2. Qual a senha do usuário "psico"?

---

## 🧪 TESTES

### Verificar se auth_user tem dados

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Ver usuários Django
print(User.objects.all())

# Ver usuários customizados
from pacientes.models import Usuario
print(Usuario.objects.filter(ativo=True))
```

---

## 📋 PERGUNTAS PARA DIAGNÓSTICO

Para te ajudar melhor, me diga:

1. **Qual a mensagem de erro exata** quando tenta fazer login?
   - [ ] "Please enter a correct username and password"
   - [ ] "This account is inactive"
   - [ ] Outro erro?

2. **Como a senha está armazenada** em `tb_usuario.senha_hash`?
   - [ ] Texto plano (ex: "psico10!")
   - [ ] MD5 (32 caracteres)
   - [ ] SHA256 (64 caracteres)
   - [ ] Hash Django (começa com "pbkdf2_sha256$")
   - [ ] Não sei

3. **Onde está o usuário "psico"**?
   - [ ] Na tabela `neurocare.tb_usuario`
   - [ ] Na tabela `auth_user`
   - [ ] Não sei

4. **Qual erro aparece no console** do servidor Django?
   - [ ] Nenhum erro
   - [ ] Erro de SQL
   - [ ] Outro?

---

## 🔧 SCRIPT DE DIAGNÓSTICO

Execute este script para coletar informações:

```python
# diagnostico_login.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neurocare_project.settings')
django.setup()

from django.contrib.auth.models import User
from pacientes.models import Usuario

print("=" * 70)
print("🔍 DIAGNÓSTICO DO SISTEMA DE LOGIN")
print("=" * 70)

print("\n1️⃣ Usuários Django (auth_user):")
django_users = User.objects.all()
if django_users:
    for u in django_users:
        print(f"   - {u.username} | Active: {u.is_active} | Staff: {u.is_staff}")
else:
    print("   ❌ Nenhum usuário Django encontrado!")

print("\n2️⃣ Usuários Customizados (tb_usuario):")
custom_users = Usuario.objects.filter(ativo=True)
if custom_users:
    for u in custom_users:
        hash_preview = u.senha_hash[:20] + "..." if len(u.senha_hash) > 20 else u.senha_hash
        print(f"   - {u.login} | Email: {u.email} | Hash: {hash_preview}")
else:
    print("   ❌ Nenhum usuário customizado encontrado!")

print("\n3️⃣ Configuração de Autenticação:")
from django.conf import settings
backends = getattr(settings, 'AUTHENTICATION_BACKENDS', ['django.contrib.auth.backends.ModelBackend'])
for backend in backends:
    print(f"   - {backend}")

print("\n" + "=" * 70)
print("✅ Diagnóstico concluído!")
print("=" * 70)
```

Execute:
```bash
python diagnostico_login.py
```

---

## 💡 PRÓXIMOS PASSOS

**Me envie**:
1. A mensagem de erro completa do login
2. Resultado do script `diagnostico_login.py`
3. Como está armazenada a senha (texto plano, MD5, etc)?

Com essas informações, vou criar a solução exata para o seu caso!

---

**Criado por**: GitHub Copilot CLI  
**Data**: 2025-11-12  
**Status**: Aguardando informações do usuário
