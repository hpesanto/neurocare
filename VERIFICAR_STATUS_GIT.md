# 🔍 Como Verificar Status: Local vs Remoto

Para verificar se tudo está sincronizado entre seu repositório local e o remoto:

---

## 🚀 Executar Verificação

### Opção 1: Script Python (Recomendado)
```bash
python verificar_git.py
```

### Opção 2: Script Batch (Windows)
```bash
verificar_git.bat
```

### Opção 3: Comandos Manuais

```bash
# Ver status geral
git status

# Ver remotes
git remote -v

# Ver últimos commits locais
git log --oneline -5

# Ver últimos commits remotos
git log origin/main --oneline -5

# Ver commits não sincronizados
git log origin/main..main --oneline

# Ver diferenças
git diff
```

---

## 📊 O Que a Verificação Mostra

### ✅ Status Local
- Branch atual
- Últimos commits locais
- Arquivos modificados
- Arquivos staged
- Arquivos untracked

### ✅ Status Remoto
- Últimos commits no remoto
- Diferenças entre local e remoto
- Commits a fazer push
- Commits a fazer pull

### ✅ Comparação
- Commits não sincronizados
- Arquivos com diferenças
- Estatísticas completas

---

## 🎯 O Que Você Verá

Exemplo de saída:

```
✅ STATUS GERAL DO REPOSITÓRIO
   [mostra status do git]

✅ CONFIGURAÇÃO DO REMOTO
   origin  https://github.com/usuario/neurocare.git (fetch)
   origin  https://github.com/usuario/neurocare.git (push)

✅ BRANCH ATUAL
   main

✅ ÚLTIMOS COMMITS LOCAIS
   abc1234 chore: clean up files
   def5678 docs: add documentation

✅ DIFERENÇAS
   [mostra se há commits a sincronizar]

✅ RESUMO FINAL
   ✅ Tudo OK!
   - Repositório sincronizado
   - Nenhuma mudança pendente
```

---

## 📌 Possíveis Resultados

### ✅ Cenário 1: Tudo Sincronizado
```
✅ Repositório limpo (nenhuma mudança local)
✅ TUDO OK!
   - Repositório está sincronizado
   - Não há mudanças pendentes
```
**Ação**: Nenhuma necessária

### ⚠️ Cenário 2: Há Mudanças Locais
```
⚠️ Há N arquivo(s) com mudanças
```
**Ação**: Execute `git add .` seguido de `git commit` e `git push`

### 📤 Cenário 3: Commits a Fazer Push
```
Commits a fazer push:
abc1234 chore: clean up files
def5678 docs: add documentation
```
**Ação**: Execute `git push origin main`

### 📥 Cenário 4: Commits a Fazer Pull
```
Commits a fazer pull:
xyz9999 fix: bug fix from team
```
**Ação**: Execute `git pull origin main`

---

## 🔧 Interpretando o Output

### Status Porcelain Codes
```
M  = Modified (modificado)
A  = Added (adicionado)
D  = Deleted (deletado)
R  = Renamed (renomeado)
C  = Copied (copiado)
?? = Untracked (não rastreado)
```

### Exemplos
```
 M arquivo.py          → Modificado, não staged
M  arquivo.py          → Modificado, staged
?? novo_arquivo.txt    → Arquivo novo, não rastreado
```

---

## 📋 Checklist de Verificação

- [ ] Status local limpo (nenhuma mudança)
- [ ] Remotes corretos
- [ ] Branch correto (main/develop)
- [ ] Nenhum commit não sincronizado
- [ ] Nenhum arquivo untracked importante
- [ ] .gitignore funcionando

---

## 🆘 Se Tiver Problemas

### "fatal: not a git repository"
```bash
# Você não está em um repositório git
cd seu-repositorio
```

### "fatal: 'origin' does not appear to be a 'git' repository"
```bash
# Remoto não está configurado
git remote add origin https://github.com/usuario/repo.git
```

### "Your branch is ahead/behind of origin/main"
```bash
# Tem commits não sincronizados
git push origin main    # Para push
git pull origin main    # Para pull
```

---

## 📊 Comparação Rápida

| Situação | Comando | Ação |
|----------|---------|------|
| Ver status | `git status` | Nenhuma |
| Ver commits pendentes | `git log origin/main..main --oneline` | Push |
| Ver mudanças | `git diff` | Add + Commit |
| Sincronizar | `git push origin main` | Push |
| Ver histórico | `git log --oneline` | Consulta |

---

## ✅ Próximos Passos

1. **Execute a verificação**: `python verificar_git.py`
2. **Verifique o resultado**
3. **Se tiver mudanças**:
   ```bash
   git add .
   git commit -m "message"
   git push origin main
   ```
4. **Crie Pull Request** se necessário

---

**Data**: 2025-11-15  
**Status**: Script pronto para executar

