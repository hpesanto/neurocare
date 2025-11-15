#!/bin/bash

echo ""
echo "======================================================================"
echo ""
echo "🚀 PUSH DE ALTERAÇÕES LOCAIS PARA REPOSITÓRIO REMOTO"
echo ""
echo "======================================================================"
echo ""

# Verificar se está em um repositório git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Este diretório não é um repositório git!"
    exit 1
fi

# 1. Ver status atual
echo "📊 STATUS ATUAL DO REPOSITÓRIO"
echo "======================================================================"
git status
echo ""

# 2. Ver branch atual
echo "🌿 BRANCH ATUAL"
echo "======================================================================"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Branch: $BRANCH"
echo ""

# 3. Ver commits não sincronizados
echo "📈 COMMITS LOCAIS NÃO SINCRONIZADOS"
echo "======================================================================"
git log "$BRANCH@{u}..$BRANCH" --oneline 2>/dev/null || echo "Nenhum commit pendente (ou branch não tem upstream)"
echo ""

# 4. Adicionar todas as mudanças
echo "➕ ADICIONANDO TODAS AS ALTERAÇÕES"
echo "======================================================================"
git add .
echo "✅ Mudanças adicionadas ao staging"
echo ""

# 5. Verificar se há mudanças para commitar
CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
    echo "⚠️  Nenhuma alteração local para commit!"
    echo "Seu repositório está atualizado."
    exit 0
fi

# 6. Criar mensagem de commit
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
COMMIT_MESSAGE="chore: clean up diagnostic documents and update documentation ($TIMESTAMP)"

# 7. Fazer commit
echo "💾 CRIANDO COMMIT"
echo "======================================================================"
git commit -m "$COMMIT_MESSAGE"
if [ $? -ne 0 ]; then
    echo "❌ Erro ao fazer commit!"
    exit 1
fi
echo ""

# 8. Fazer push
echo "🚀 FAZENDO PUSH PARA REPOSITÓRIO REMOTO"
echo "======================================================================"
git push origin "$BRANCH"
if [ $? -ne 0 ]; then
    echo "❌ Erro ao fazer push!"
    echo "⚠️  Verifique sua conexão e credenciais git"
    exit 1
fi
echo ""

# 9. Ver resultado
echo "✅ STATUS PÓS-PUSH"
echo "======================================================================"
git status
echo ""

# 10. Resumo
echo "======================================================================"
echo "📋 RESUMO DA OPERAÇÃO"
echo "======================================================================"
echo "✅ Alterações commitadas com sucesso!"
echo "✅ Push realizado para: origin/$BRANCH"
echo "✅ Mensagem do commit: $COMMIT_MESSAGE"
echo ""
echo "📌 Para criar uma Pull Request:"
echo "   1. Acesse seu repositório no GitHub/GitLab"
echo "   2. Você verá um botão 'Compare & pull request'"
echo "   3. Configure título, descrição e reviewers"
echo "   4. Clique em 'Create Pull Request'"
echo "======================================================================"
echo ""
