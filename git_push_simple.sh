#!/bin/bash
# Script simples para verificar e fazer push de alterações

cd "$(dirname "$0")" 2>/dev/null || cd .

echo "=================================="
echo "Git Status"
echo "=================================="
git status

echo ""
echo "=================================="
echo "Adicionando alterações..."
echo "=================================="
git add .

echo ""
echo "=================================="
echo "Fazendo commit..."
echo "=================================="
git commit -m "chore: clean up diagnostic documents and update documentation"

echo ""
echo "=================================="
echo "Fazendo push..."
echo "=================================="
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git push origin $BRANCH

echo ""
echo "=================================="
echo "Status final"
echo "=================================="
git status
