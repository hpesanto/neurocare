#!/bin/bash
# Script simples para verificar git status

echo ""
echo "======================================================================"
echo "GIT STATUS - LOCAL vs REMOTO"
echo "======================================================================"
echo ""

echo "1. Status Local"
echo "======================================================================"
git status
echo ""

echo "2. Remotes Configurados"
echo "======================================================================"
git remote -v
echo ""

echo "3. Branch Atual"
echo "======================================================================"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Branch: $BRANCH"
echo ""

echo "4. Últimos Commits Locais"
echo "======================================================================"
git log --oneline -5
echo ""

echo "5. Últimos Commits Remotos"
echo "======================================================================"
git log origin/$BRANCH --oneline -5 2>/dev/null || echo "Branch não existe no remoto"
echo ""

echo "6. Commits NÃO Sincronizados (Local → Remoto)"
echo "======================================================================"
git log origin/$BRANCH..$BRANCH --oneline 2>/dev/null || echo "Tudo sincronizado"
echo ""

echo "7. Commits NÃO Sincronizados (Remoto → Local)"
echo "======================================================================"
git log $BRANCH..origin/$BRANCH --oneline 2>/dev/null || echo "Tudo sincronizado"
echo ""

echo "8. Diferenças (Untracked + Modified)"
echo "======================================================================"
git status --short
if [ -z "$(git status --porcelain)" ]; then
    echo "Nenhuma mudança pendente"
fi
echo ""

echo "======================================================================"
echo "RESUMO"
echo "======================================================================"

UNTRACKED=$(git ls-files --others --exclude-standard | wc -l)
MODIFIED=$(git status --porcelain | grep "^ M" | wc -l)
STAGED=$(git status --porcelain | grep "^M" | wc -l)
AHEAD=$(git rev-list origin/$BRANCH..$BRANCH --count 2>/dev/null || echo 0)
BEHIND=$(git rev-list $BRANCH..origin/$BRANCH --count 2>/dev/null || echo 0)

echo "Arquivos não rastreados: $UNTRACKED"
echo "Arquivos modificados: $MODIFIED"
echo "Arquivos staged: $STAGED"
echo "Commits ahead (para push): $AHEAD"
echo "Commits behind (para pull): $BEHIND"
echo ""

if [ "$UNTRACKED" -eq 0 ] && [ "$MODIFIED" -eq 0 ] && [ "$STAGED" -eq 0 ] && [ "$AHEAD" -eq 0 ] && [ "$BEHIND" -eq 0 ]; then
    echo "✅ TUDO SINCRONIZADO!"
else
    echo "⚠️  Há mudanças pendentes. Execute:"
    if [ "$AHEAD" -gt 0 ]; then
        echo "   git push origin $BRANCH"
    fi
    if [ "$BEHIND" -gt 0 ]; then
        echo "   git pull origin $BRANCH"
    fi
    if [ "$MODIFIED" -gt 0 ] || [ "$UNTRACKED" -gt 0 ]; then
        echo "   git add ."
        echo "   git commit -m 'message'"
    fi
fi

echo ""
