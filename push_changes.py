#!/usr/bin/env python3
"""
Script para criar um commit com todas as alterações locais
e fazer push para o repositório remoto.

Uso: python push_changes.py
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(cmd, description=""):
    """Execute um comando e retorne o resultado."""
    print(f"\n{'='*70}")
    if description:
        print(f"🔄 {description}")
    print(f"{'='*70}")
    print(f"$ {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("⚠️  Mensagens:", result.stderr)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False, "", str(e)

def main():
    print("\n" + "="*70)
    print("🚀 PUSH DE ALTERAÇÕES LOCAIS PARA REPOSITÓRIO REMOTO")
    print("="*70)
    
    # Verificar se está em um repositório git
    success, _, _ = run_command("git rev-parse --git-dir", "Verificando repositório git...")
    if not success:
        print("❌ Este diretório não é um repositório git!")
        sys.exit(1)
    
    # 1. Ver status atual
    print("\n📊 STATUS ATUAL DO REPOSITÓRIO")
    run_command("git status", "Verificando mudanças...")
    
    # 2. Ver branch atual
    print("\n🌿 BRANCH ATUAL")
    success, branch, _ = run_command("git rev-parse --abbrev-ref HEAD", "Identificando branch...")
    branch = branch.strip()
    
    # 3. Ver commits não sincronizados
    print("\n📈 COMMITS LOCAIS NÃO SINCRONIZADOS")
    run_command(f"git log {branch}@{{u}}..{branch} --oneline", "Commits pendentes...")
    
    # 4. Adicionar todas as mudanças
    print("\n➕ ADICIONANDO TODAS AS ALTERAÇÕES")
    success, _, _ = run_command("git add .", "Staging de todas as mudanças...")
    if not success:
        print("❌ Erro ao adicionar arquivos!")
        sys.exit(1)
    
    # 5. Verificar se há mudanças para commitar
    success, status_output, _ = run_command("git status --porcelain", "Verificando mudanças após staging...")
    
    if not status_output.strip():
        print("\n⚠️  Nenhuma alteração local para commit!")
        print("Seu repositório está atualizado.")
        sys.exit(0)
    
    # 6. Criar mensagem de commit
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"chore: clean up diagnostic documents and update documentation ({timestamp})"
    
    # 7. Fazer commit
    print("\n💾 CRIANDO COMMIT")
    success, _, _ = run_command(
        f'git commit -m "{commit_message}"',
        f"Commitando alterações: '{commit_message}'"
    )
    if not success:
        print("❌ Erro ao fazer commit!")
        sys.exit(1)
    
    # 8. Fazer push
    print("\n🚀 FAZENDO PUSH PARA REPOSITÓRIO REMOTO")
    success, _, _ = run_command(
        f"git push origin {branch}",
        f"Enviando commits para branch '{branch}'..."
    )
    if not success:
        print("❌ Erro ao fazer push!")
        print("⚠️  Verifique sua conexão e credenciais git")
        sys.exit(1)
    
    # 9. Ver resultado
    print("\n✅ STATUS PÓS-PUSH")
    run_command("git status", "Verificando status final...")
    
    # 10. Resumo
    print("\n" + "="*70)
    print("📋 RESUMO DA OPERAÇÃO")
    print("="*70)
    print(f"✅ Alterações commitadas com sucesso!")
    print(f"✅ Push realizado para: origin/{branch}")
    print(f"✅ Mensagem do commit: {commit_message}")
    print(f"\n📌 Para criar uma Pull Request:")
    print(f"   1. Acesse seu repositório no GitHub/GitLab")
    print(f"   2. Você verá um botão 'Compare & pull request'")
    print(f"   3. Configure título, descrição e reviewers")
    print(f"   4. Clique em 'Create Pull Request'")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
