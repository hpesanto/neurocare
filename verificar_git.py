#!/usr/bin/env python3
"""
Script para comparar repositório local com remoto e verificar status.
"""

import subprocess
import sys
from datetime import datetime

def run_cmd(cmd, description=""):
    """Execute comando git e retorne resultado."""
    print(f"\n{'='*80}")
    if description:
        print(f"🔍 {description}")
    print(f"{'='*80}")
    print(f"$ {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=".")
        if result.stdout:
            print(result.stdout)
        if result.stderr and "fatal" in result.stderr.lower():
            print("❌ ERRO:", result.stderr)
            return False, result.stdout, result.stderr
        return True, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False, "", str(e)

def main():
    print("\n" + "="*80)
    print("🔍 COMPARAÇÃO: REPOSITÓRIO LOCAL vs REMOTO")
    print("="*80)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. Status geral
    print("\n1️⃣  STATUS GERAL DO REPOSITÓRIO")
    run_cmd("git status", "Verificando status local...")
    
    # 2. Configuração remoto
    print("\n2️⃣  CONFIGURAÇÃO DO REMOTO")
    run_cmd("git remote -v", "Remotes configurados...")
    
    # 3. Branch atual
    print("\n3️⃣  BRANCH ATUAL")
    success, branch_output, _ = run_cmd("git rev-parse --abbrev-ref HEAD", "Branch atual...")
    branch = branch_output.strip() if success else "unknown"
    
    # 4. Últimos commits locais
    print("\n4️⃣  ÚLTIMOS 5 COMMITS LOCAIS")
    run_cmd("git log --oneline -5", "Histórico local...")
    
    # 5. Últimos commits remotos
    print("\n5️⃣  ÚLTIMOS 5 COMMITS REMOTOS")
    run_cmd(f"git log origin/{branch} --oneline -5 2>/dev/null || echo 'Branch não existe no remoto'", 
            "Histórico remoto...")
    
    # 6. Diferenças entre local e remoto
    print("\n6️⃣  DIFERENÇAS: LOCAL vs REMOTO")
    print(f"Commits locais não sincronizados (local ahead of remote):")
    run_cmd(f"git log origin/{branch}..{branch} --oneline 2>/dev/null || echo 'Nenhuma diferença'", 
            "Commits a fazer push...")
    
    print(f"\nCommits remotos não sincronizados (remote ahead of local):")
    run_cmd(f"git log {branch}..origin/{branch} --oneline 2>/dev/null || echo 'Nenhuma diferença'", 
            "Commits a fazer pull...")
    
    # 7. Arquivos não sincronizados
    print("\n7️⃣  ARQUIVOS COM DIFERENÇAS")
    run_cmd("git diff --name-status", "Arquivos modificados (não staged)...")
    run_cmd("git diff --cached --name-status", "Arquivos staged...")
    run_cmd("git status --short", "Status resumido...")
    
    # 8. Verificar arquivo .gitignore
    print("\n8️⃣  ARQUIVOS IGNORADOS")
    run_cmd("git check-ignore -v .*", "Padrões .gitignore ativo...")
    
    # 9. Untracked files
    print("\n9️⃣  ARQUIVOS NÃO RASTREADOS")
    success, untracked, _ = run_cmd("git ls-files --others --exclude-standard", 
                                     "Arquivos não rastreados...")
    
    # 10. Comparação detalhada
    print("\n🔟 RESUMO COMPARATIVO")
    print("="*80)
    
    success_local, local_count, _ = run_cmd(
        "git rev-list --count HEAD", 
        "Contando commits locais..."
    )
    
    success_remote, remote_count, _ = run_cmd(
        f"git rev-list --count origin/{branch} 2>/dev/null || echo '0'", 
        "Contando commits remotos..."
    )
    
    if success_local and success_remote:
        local_num = int(local_count.strip()) if local_count.strip().isdigit() else 0
        remote_num = int(remote_count.strip()) if remote_count.strip().isdigit() else 0
        
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   Commits locais:  {local_num}")
        print(f"   Commits remotos: {remote_num}")
        print(f"   Diferença:       {abs(local_num - remote_num)}")
    
    # 11. Status final
    print("\n" + "="*80)
    print("📋 RESUMO FINAL")
    print("="*80)
    
    # Verificar se há mudanças para fazer commit
    success, status, _ = run_cmd("git status --porcelain", "Verificando mudanças...")
    
    if not status.strip():
        print("\n✅ Repositório limpo (nenhuma mudança local)")
    else:
        print(f"\n⚠️  Há {len(status.strip().split(chr(10)))} arquivo(s) com mudanças")
        print("Use 'git add .' para staged ou 'git push' para sincronizar")
    
    # Mostrar recomendações
    print("\n" + "="*80)
    print("💡 RECOMENDAÇÕES")
    print("="*80)
    
    if not status.strip():
        print("\n✅ TUDO OK!")
        print("   - Repositório está sincronizado")
        print("   - Não há mudanças pendentes")
        print("   - Pronto para novos desenvolvimentos")
    else:
        print("\n⚠️  AÇÕES RECOMENDADAS:")
        print("   1. git add . (ou git add <arquivo>)")
        print("   2. git commit -m 'message'")
        print("   3. git push origin " + branch)
    
    print("\n" + "="*80)
    print("✅ VERIFICAÇÃO CONCLUÍDA")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
