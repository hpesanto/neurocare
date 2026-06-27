#!/usr/bin/env bash
#
# Deploy do NeuroCare em um comando.
# Uso no servidor:  bash deploy.sh
#
# Faz: git pull -> build das imagens -> sobe os containers -> espera o
# backend responder -> mostra o status. Idempotente: pode rodar quantas
# vezes quiser. As credenciais/hosts vêm do arquivo .env (não versionado).

set -euo pipefail
cd "$(dirname "$0")"

COMPOSE="docker compose"
# Permite sobrescrever o arquivo de compose:  COMPOSE_FILE=docker-compose.prod.yml bash deploy.sh
if [ -n "${COMPOSE_FILE:-}" ]; then
  COMPOSE="docker compose -f ${COMPOSE_FILE}"
fi

echo "==> 1/4 Atualizando código (git pull)..."
git pull --ff-only origin main

echo "==> 2/4 Build das imagens..."
$COMPOSE build

echo "==> 3/4 Subindo containers..."
$COMPOSE up -d

echo "==> 4/4 Aguardando o backend responder..."
API_PORT="${API_PORT:-8000}"
ok=0
for i in $(seq 1 40); do
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST -H "Content-Type: application/json" \
    -d '{"username":"_healthcheck_","password":"_x_"}' \
    "http://localhost:${API_PORT}/api/token/" 2>/dev/null || echo 000)
  # 2xx/4xx = Django no ar e banco acessível; 5xx/000 = ainda subindo ou com erro
  case "$code" in
    2*|4*) ok=1; break ;;
    *) printf '   ... aguardando (HTTP %s) [%s/40]\r' "$code" "$i"; sleep 3 ;;
  esac
done
echo ""

if [ "$ok" = "1" ]; then
  echo "==> OK: backend respondendo (API e banco no ar)."
else
  echo "!!  Backend não respondeu a tempo. Veja os logs:"
  echo "      $COMPOSE logs --tail=40 backend"
  exit 1
fi

echo ""
echo "==> Status dos containers:"
$COMPOSE ps
echo ""
echo "Deploy concluído."
