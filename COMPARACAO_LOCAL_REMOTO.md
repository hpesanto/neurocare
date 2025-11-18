# 📊 Comparação Local vs Remoto - Guia de Verificação

---

## 🚀 Como Verificar Status

### Opção 1: Script Automático (Recomendado)
```bash
python verificar_git.py      # Python
verificar_git.bat            # Windows
bash verificar_status.sh     # Bash/Linux
```

### Opção 2: Comandos Git Manuais

```bash
# 1. Ver status geral
git status

# 2. Ver remotes
git remote -v

# 3. Ver branch atual
git branch
git rev-parse --abbrev-ref HEAD

# 4. Ver commits locais
git log --oneline -10

# 5. Ver commits remotos
git log origin/main --oneline -10

# 6. Ver commits não sincronizados (para push)
git log origin/main..main --oneline
git rev-list origin/main..main --count

# 7. Ver commits não sincronizados (para pull)
git log main..origin/main --oneline
git rev-list main..origin/main --count

# 8. Ver diferenças de arquivos
git diff
git diff --staged

# 9. Ver arquivos não rastreados
git ls-files --others --exclude-standard

# 10. Ver status resumido
git status --short
```

---

## 📋 O Que Esperar Ver

### ✅ Repositório Sincronizado
```
$ git status
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

### ⚠️ Com Mudanças Locais
```
$ git status
On branch main
Your branch is ahead of 'origin/main' by 2 commits.

Changes not staged for commit:
  modified: arquivo.py

Untracked files:
  novo_arquivo.txt
```

### 📤 Commits Pendentes (Push)
```
$ git log origin/main..main --oneline
abc1234 chore: clean up files
def5678 docs: add documentation
```

### 📥 Commits Pendentes (Pull)
```
$ git log main..origin/main --oneline
xyz9999 fix: bug from team
```

---

## 🔍 Interpretação de Resultados

| Output | Significado | Ação |
|--------|------------|------|
| `up to date with 'origin/main'` | Tudo sincronizado | Nenhuma |
| `ahead by N commits` | Tem commits para fazer push | `git push` |
| `behind by N commits` | Tem commits para fazer pull | `git pull` |
| `Changes not staged` | Arquivos modificados | `git add .` |
| `Untracked files` | Arquivos novos | `git add .` |

---

## 📊 Status Porcelain (Resumido)

Comando: `git status --short`

Output:
```
 M arquivo.py          ← Modificado (não staged)
M  arquivo.py          ← Modificado (staged)
A  novo.py             ← Adicionado
D  deletado.py         ← Deletado
R  renomeado.py        ← Renomeado
?? ignorado.pyc        ← Não rastreado
```

---

## 🎯 Cenários Comuns

### Cenário 1: Tudo OK
```bash
git status
# Output: "nothing to commit, working tree clean"
```
✅ **Ação**: Nenhuma

### Cenário 2: Tem Mudanças Locais
```bash
git status
# Output: "Changes not staged for commit"
git diff                 # Ver mudanças
git add .                # Adicionar
git commit -m "msg"      # Commit
git push origin main     # Push
```
✅ **Ação**: `git add . && git commit -m "msg" && git push`

### Cenário 3: Commits Não Sincronizados
```bash
git log origin/main..main --oneline
# Mostra commits locais não sincronizados
git push origin main
```
✅ **Ação**: `git push origin main`

### Cenário 4: Conflitos
```bash
git status
# Output: "both modified: arquivo.py"
# Resolver manualmente
git add arquivo.py
git commit -m "resolve conflict"
git push origin main
```
✅ **Ação**: Resolver conflito + commit + push

---

## 📈 Workflow Típico

```
1. Ver status
   $ git status

2. Se houver mudanças:
   $ git add .
   $ git commit -m "descriptive message"

3. Se houver commits não sincronizados:
   $ git push origin main

4. Se precisar de atualizações remotas:
   $ git pull origin main

5. Criar Pull Request (se necessário)
   Via GitHub ou GitHub CLI
```

---

## 🔗 Comandos Úteis

```bash
# Ver diferenças
git diff                           # Working vs Staged
git diff --staged                  # Staged vs HEAD
git diff main origin/main          # Local vs Remoto

# Ver histórico
git log --oneline                  # Resumido
git log --graph --oneline --all    # Com gráfico
git log --stat                     # Com estatísticas

# Ver branches
git branch                         # Local
git branch -a                      # Tudo
git branch -v                      # Com info

# Verificar remote
git remote -v                      # URLs
git remote show origin             # Info completa
git ls-remote origin               # Refs remotas

# Sincronizar
git fetch                          # Baixar sem mergear
git pull                           # Fetch + Merge
git push                           # Enviar
```

---

## ⚠️ Erros Comuns

### "Not a git repository"
```bash
cd /caminho/para/repositorio
git status
```

### "fatal: origin does not appear to be a git repository"
```bash
git remote add origin https://github.com/usuario/repo.git
git remote -v
```

### "Permission denied"
```bash
# Configure SSH keys ou use HTTPS com token
git config credential.helper cache
git push
```

### "Your branch diverged"
```bash
git pull origin main
# Resolver conflitos se houver
git push origin main
```

---

## 🎯 Recomendação

**Sempre execute antes de fazer mudanças:**
```bash
git status              # Ver status local
git log -1 --oneline    # Ver último commit
git remote -v           # Verificar remotes
```

**Sempre sincronize antes de novos desenvolvimentos:**
```bash
git fetch               # Atualizar info
git status              # Verificar status
git pull               # Se houver novidades
```

---

## 📝 Exemplo Completo

```bash
# 1. Verificar status
$ git status
On branch main
Your branch is ahead of 'origin/main' by 2 commits.

# 2. Ver commits não sincronizados
$ git log origin/main..main --oneline
abc1234 chore: clean up files
def5678 docs: add documentation

# 3. Ver diferenças
$ git diff origin/main

# 4. Fazer push
$ git push origin main
Enumerating objects: 5, done.
...
Your branch is up to date with 'origin/main'.

# 5. Verificar novamente
$ git status
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean

✅ Sincronizado!
```

---

## 📊 Comparação Rápida

```bash
# Local vs Remoto
git diff main origin/main              # Diferenças
git log main..origin/main --oneline    # Commits remotos
git log origin/main..main --oneline    # Commits locais

# Status resumido
git status -s                          # Muito resumido
git status -b                          # Com branch info
```

---

**Data**: 2025-11-15  
**Status**: Pronto para verificação

