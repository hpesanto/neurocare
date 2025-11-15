# 👥 GUIA: Gestão de Usuários com Django Admin

**Data**: 2025-11-12  
**Status**: ✅ IMPLEMENTADO

---

## 🎉 O QUE FOI IMPLEMENTADO

### ✅ Django Admin Configurado
- Interface administrativa completa para gerenciar usuários
- Criar, editar, desativar usuários
- Senhas armazenadas com hash seguro (pbkdf2_sha256)
- Busca e filtros avançados

---

## 🚀 COMO USAR

### **1. Criar Superuser (apenas primeira vez)**

Se ainda não criou, execute:

```bash
python manage.py createsuperuser

# Preencha:
Username: admin
Email: admin@neurocare.com
Password: [senha forte]
```

---

### **2. Acessar Django Admin**

1. Inicie servidor: `python manage.py runserver`
2. Acesse: **http://127.0.0.1:8000/admin/**
3. Faça login com o superuser criado

---

### **3. Criar Novo Usuário**

#### Via Django Admin (RECOMENDADO):

1. No admin, clique em **"Usuarios"** (no grupo Pacientes)
2. Clique em **"Adicionar Usuario +"** (canto superior direito)
3. Preencha os campos:
   - **Nome completo**: Nome do usuário
   - **Email**: email@exemplo.com
   - **Login**: username (será usado para login)
   - **Ativo**: ✅ Marcado
   - **Senha**: Digite a senha
   - **Confirmar Senha**: Digite novamente
4. Clique em **"Salvar"**

✅ **Pronto!** O usuário pode fazer login imediatamente.

---

### **4. Editar Usuário Existente**

1. No admin, clique em **"Usuarios"**
2. Clique no usuário que deseja editar
3. Modifique os campos desejados
4. Para mudar a senha:
   - Digite nova senha em **"Senha"**
   - Confirme em **"Confirmar Senha"**
   - (Deixe em branco para não alterar senha)
5. Clique em **"Salvar"**

---

### **5. Desativar Usuário**

1. No admin, clique em **"Usuarios"**
2. Clique no usuário
3. **Desmarque** a caixa **"Ativo"**
4. Clique em **"Salvar"**

⚠️ Usuário desativado **não consegue fazer login**.

---

### **6. Buscar Usuários**

Na lista de usuários, use a caixa de busca para procurar por:
- Login
- Nome completo
- Email

Você também pode filtrar por:
- Status (Ativo/Inativo)
- Data de criação

---

## 🔐 SEGURANÇA

### ✅ **Hash de Senhas**

**Novos usuários** criados pelo admin usam **hash Django (pbkdf2_sha256)**:
- ✅ Extremamente seguro
- ✅ Salt automático
- ✅ 260.000 iterações (padrão Django 5.x)
- ✅ Impossível reverter para texto plano

**Usuários antigos** (MD5/SHA256) continuam funcionando:
- ⚠️ O backend suporta os dois formatos
- 💡 Recomendado: Pedir usuários para redefinir senha

---

### 🔄 **Migrar Usuários Antigos para Hash Seguro**

#### Opção 1: Manual (via admin)
1. Acesse cada usuário no admin
2. Digite nova senha
3. Salve

#### Opção 2: Script (todos de uma vez)
```python
python manage.py shell
```

```python
from pacientes.models import Usuario
from django.contrib.auth.hashers import make_password

# Listar usuários com hash antigo
usuarios_antigos = Usuario.objects.exclude(senha_hash__startswith='pbkdf2_')

print(f"Encontrados {usuarios_antigos.count()} usuários com hash antigo")

# ATENÇÃO: Isso vai resetar todas as senhas para uma senha padrão!
# Os usuários precisarão redefini-la depois.
senha_temporaria = "Mudar123!"

for u in usuarios_antigos:
    u.senha_hash = make_password(senha_temporaria)
    u.save()
    print(f"✅ {u.login} atualizado (senha temp: {senha_temporaria})")

print("\n⚠️  Notifique os usuários para mudarem a senha!")
```

---

## 📊 RECURSOS DO ADMIN

### ✅ Lista de Usuários
- Ver todos os usuários de relance
- Status ativo/inativo visível
- Data de criação e última atualização
- Ordenação por qualquer coluna

### ✅ Busca e Filtros
- Busca por login, nome, email
- Filtro por status (ativo/inativo)
- Filtro por data de criação

### ✅ Segurança
- Senhas nunca visíveis
- Hash automático ao salvar
- Validação de senha duplicada
- ID não editável

### ✅ Auditoria
- Data de criação registrada
- Data de última atualização
- Histórico de mudanças (log do Django)

---

## 🧪 TESTES

### **Teste 1: Criar usuário**
```
1. Admin → Usuarios → Adicionar
2. Nome: Teste Silva
3. Email: teste@email.com
4. Login: teste
5. Senha: Teste123!
6. Confirmar: Teste123!
7. Ativo: ✅
8. Salvar
```

### **Teste 2: Login com novo usuário**
```
1. Logout do admin
2. Acesse: /login/
3. Username: teste
4. Password: Teste123!
5. ✅ Deve funcionar!
```

### **Teste 3: Editar usuário**
```
1. Admin → Usuarios → teste
2. Mude email para: teste2@email.com
3. Salvar
4. ✅ Email atualizado
```

### **Teste 4: Mudar senha**
```
1. Admin → Usuarios → teste
2. Senha: NovaSenha456!
3. Confirmar: NovaSenha456!
4. Salvar
5. Logout e login com nova senha
6. ✅ Deve funcionar!
```

---

## 🎯 PERMISSÕES E GRUPOS (PRÓXIMO PASSO)

### Criar Grupos de Permissões

1. No admin, vá em **"Grupos"**
2. Crie grupos como:
   - **Psicólogos**: Permissões de atendimento
   - **Administrativo**: Permissões de cadastro
   - **Financeiro**: Permissões financeiras
   - **Recepção**: Permissões limitadas

3. Atribua permissões específicas a cada grupo

4. Adicione usuários aos grupos apropriados

### Exemplo de Permissões:

**Grupo "Psicólogos"**:
- ✅ `pacientes.view_paciente`
- ✅ `pacientes.add_paciente`
- ✅ `pacientes.change_paciente`
- ✅ `evolucao_clinica.add_evolucaoclinica`
- ✅ `evolucao_clinica.change_evolucaoclinica`
- ✅ `evolucao_clinica.view_evolucaoclinica`

**Grupo "Recepção"**:
- ✅ `pacientes.view_paciente`
- ❌ Sem acesso a dados clínicos

---

## 📋 CHECKLIST DE CONFIGURAÇÃO

- [x] Django Admin configurado
- [x] UsuarioAdmin criado
- [x] Backend de autenticação suporta hash Django
- [ ] Superuser criado
- [ ] Testado criar usuário via admin
- [ ] Testado login com novo usuário
- [ ] Grupos de permissões criados (opcional)
- [ ] Usuários antigos migrados para hash seguro (opcional)

---

## 🆘 TROUBLESHOOTING

### Problema: Não aparece "Usuarios" no admin

**Solução**: 
1. Verifique se `pacientes/admin.py` existe
2. Reinicie o servidor Django
3. Limpe cache do navegador (Ctrl+Shift+R)

### Problema: Erro ao salvar usuário

**Sintoma**: `DatabaseError` ou `IntegrityError`

**Solução**: Verifique se:
- Login é único (não existe outro com mesmo login)
- Email é único (não existe outro com mesmo email)
- Todos os campos obrigatórios estão preenchidos

### Problema: Senhas não coincidem

**Sintoma**: Formulário não salva e mostra erro

**Solução**: 
- Digite exatamente a mesma senha nos dois campos
- Cuidado com caps lock
- Não use espaços no início/fim da senha

---

## 💡 COMANDOS ÚTEIS

### Ver todos os usuários no shell
```python
python manage.py shell

from pacientes.models import Usuario

# Listar todos
for u in Usuario.objects.all():
    print(f"{u.login} - {u.nome_completo} - {'Ativo' if u.ativo else 'Inativo'}")
```

### Criar usuário via shell (alternativa)
```python
from pacientes.models import Usuario
from django.contrib.auth.hashers import make_password
import uuid

u = Usuario.objects.create(
    id=uuid.uuid4(),
    nome_completo="João Silva",
    email="joao@email.com",
    login="joao",
    senha_hash=make_password("Joao123!"),
    ativo=True
)
print(f"✅ Usuário {u.login} criado!")
```

### Resetar senha de usuário
```python
from pacientes.models import Usuario
from django.contrib.auth.hashers import make_password

u = Usuario.objects.get(login='psico')
u.senha_hash = make_password('NovaSenha123!')
u.save()
print(f"✅ Senha de {u.login} atualizada!")
```

---

## 🎨 CUSTOMIZAÇÕES FUTURAS

### Adicionar mais campos ao admin:
```python
# Em pacientes/admin.py
list_display = [
    'login',
    'nome_completo',
    'email',
    'ativo',
    'ultimo_acesso',  # Novo campo
    'data_criacao',
]
```

### Adicionar ações em massa:
```python
@admin.action(description='Desativar usuários selecionados')
def desativar_usuarios(modeladmin, request, queryset):
    queryset.update(ativo=False)

class UsuarioAdmin(admin.ModelAdmin):
    actions = [desativar_usuarios]
```

---

## 📚 RECURSOS ADICIONAIS

- **Django Admin Docs**: https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
- **User Permissions**: https://docs.djangoproject.com/en/5.0/topics/auth/default/#permissions-and-authorization
- **Password Hashing**: https://docs.djangoproject.com/en/5.0/topics/auth/passwords/

---

**Status**: ✅ Pronto para uso  
**Próximo passo**: Criar superuser e testar criação de usuário  
**Suporte**: Me avise se encontrar algum problema!
