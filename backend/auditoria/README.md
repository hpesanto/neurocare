# Auditoria (Audit Log) — NeuroCare

Sistema de auditoria que rastreia **autenticação** (login, logout, falhas) e **operações de dados** (CREATE, UPDATE, DELETE, LEITURA) no NeuroCare.

## Visão Geral

Todos os eventos são registrados automaticamente na tabela `tb_log_auditoria` com:
- **Quem**: usuário + perfil
- **Quando**: data/hora UTC+3 (America/Sao_Paulo)
- **O quê**: entidade, ID do registro, representação legível
- **O que mudou**: diff (antes/depois) para UPDATE
- **De onde**: IP real + User-Agent

Campos sensíveis (password, tokens, etc.) **nunca** são registrados.

## Recurso MVP

### Fase 1-2: Setup & Foundational ✅
- App Django `auditoria` registrado
- Modelo `AuditLog` com 15 campos + índices
- Helpers de request (IP via X-Forwarded-For, User-Agent)
- Função de diff (só campos alterados)
- Serviço `registrar_log` com best-effort (não quebra operação)

### Fase 3: User Story 1 — Escrita (CREATE/UPDATE/DELETE) ✅
- `AuditLogMixin` aplicado a **todos os 15 viewsets**
- Captura automática de CREATE/UPDATE/DELETE
- Diff disponível para UPDATE
- Campos sensíveis removidos
- Testes: `test_writes.py`

### Fase 4: User Story 2 — Autenticação ✅
- `AuditTokenObtainPairView` registra LOGIN (200) e LOGIN_FALHA (401)
- `logout_view` implementa logout + blacklist de refresh token
- Eventos: LOGIN, LOGIN_FALHA, LOGOUT
- Testes: `test_auth.py`

### Fase 5: User Story 3 — Consulta/Export ✅
- API ReadOnly `/api/auditoria/` (Admin only)
- Filtros: período, usuário, ação, entidade, objeto_id
- Busca: username, objeto_repr
- Exportação: CSV e XLSX
- Django Admin: visualização com cores + JSON formatado
- Testes: `test_query.py`

### Fase 7: User Story 5 — Retenção ✅
- Comando: `python manage.py purge_audit_logs --days 365` (padrão: 12 meses)
- Testes: `test_retention.py`

### Fase 6: User Story 4 — LGPD (Leitura) ⏳
- Não implementado nesta fase (maior volume, tratável como evolução)
- Quando necessário: adicionar `AuditLogMixin.retrieve()` nos viewsets sensíveis

## Como Usar

### Testes de Escrita
```bash
docker compose exec backend python manage.py test auditoria.tests.test_writes -v 2
```

### Testes de Autenticação
```bash
docker compose exec backend python manage.py test auditoria.tests.test_auth -v 2
```

### Testes de Consulta/Export
```bash
docker compose exec backend python manage.py test auditoria.tests.test_query -v 2
```

### Testes de Retenção
```bash
docker compose exec backend python manage.py test auditoria.tests.test_retention -v 2
```

### Executar todos os testes de auditoria
```bash
docker compose exec backend python manage.py test auditoria -v 2
```

### Visualizar logs no Django Admin
```
http://localhost:8000/admin/auditoria/auditlog/
```
- Filtrar por Ação, Data, Entidade
- Buscar por usuário ou representação
- JSON das alterações é formatado para legibilidade

### Consultar logs pela API
```bash
# Listar todos (Admin only)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/auditoria/

# Filtrar por período
curl -H "Authorization: Bearer $TOKEN" \
  'http://localhost:8000/api/auditoria/?data_hora__gte=2026-06-01&data_hora__lte=2026-06-30'

# Filtrar por ação
curl -H "Authorization: Bearer $TOKEN" 'http://localhost:8000/api/auditoria/?acao=UPDATE'

# Filtrar por entidade
curl -H "Authorization: Bearer $TOKEN" 'http://localhost:8000/api/auditoria/?entidade=Paciente'

# Buscar por usuário
curl -H "Authorization: Bearer $TOKEN" 'http://localhost:8000/api/auditoria/?search=testuser'

# Exportar CSV
curl -H "Authorization: Bearer $TOKEN" 'http://localhost:8000/api/auditoria/exportar/?formato=csv' \
  -o auditoria.csv

# Exportar XLSX
curl -H "Authorization: Bearer $TOKEN" 'http://localhost:8000/api/auditoria/exportar/?formato=xlsx' \
  -o auditoria.xlsx
```

### Purgar logs antigos
```bash
# Remover logs com > 365 dias (padrão)
docker compose exec backend python manage.py purge_audit_logs

# Remover logs com > 180 dias
docker compose exec backend python manage.py purge_audit_logs --days 180
```

## Agendar purga com Cron (VPS)

Adicionar ao crontab do usuário Docker/app:
```bash
# Diariamente às 2 AM
0 2 * * * cd /app && python manage.py purge_audit_logs --days 365 >> /var/log/neurocare/audit-purge.log 2>&1
```

Ou via systemd timer no VPS:
```bash
# Criar arquivo /etc/systemd/system/neurocare-audit-purge.service
[Unit]
Description=NeuroCare Audit Log Purge
After=docker.service

[Service]
Type=oneshot
ExecStart=/usr/bin/docker compose -f /app/docker-compose.yml exec -T backend python manage.py purge_audit_logs --days 365
WorkingDirectory=/app

# Criar arquivo /etc/systemd/system/neurocare-audit-purge.timer
[Unit]
Description=NeuroCare Audit Log Purge Timer
Requires=neurocare-audit-purge.service

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

## Validação Ponta-a-Ponta (quickstart.md)

Cenários no arquivo `.specify/features/audit-log-v1/quickstart.md`:
1. CREATE/UPDATE/DELETE geram eventos
2. LOGIN sucesso/falha
3. LOGOUT blacklista refresh
4. Permissão de consulta (Admin only)
5. Filtros e exportação
6. Imutabilidade (ReadOnly)
7. Resiliência (auditoria não quebra operação)
8. Retenção (purga >12 meses)

## Estrutura de Arquivos

```
backend/auditoria/
├── __init__.py
├── admin.py              # Django Admin config
├── apps.py               # App config
├── auth_views.py         # Login/Logout custom views
├── mixins.py             # AuditLogMixin (CREATE/UPDATE/DELETE/RETRIEVE)
├── models.py             # AuditLog model
├── serializers.py        # AuditLogSerializer
├── services.py           # registrar_log()
├── utils.py              # Helpers (IP, diff, sensitive fields)
├── viewsets.py           # AuditLogViewSet (ReadOnly + Admin)
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py   # AuditLog table + indices
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── purge_audit_logs.py  # Retention command
└── tests/
    ├── __init__.py
    ├── test_writes.py    # CREATE/UPDATE/DELETE audit
    ├── test_auth.py      # LOGIN/LOGOUT audit
    ├── test_query.py     # API filtering & export
    └── test_retention.py # Purge logic
```

## Decisões de Design

Veja `.specify/features/audit-log-v1/research.md` para:
- D1: Mecanismo de captura (Mixin vs sinais vs pacotes prontos)
- D2: Login (subclasse TokenObtainPairView)
- D3: Logout (JWT blacklist)
- D4: Diff compacto (só campos alterados)
- D5: IP real (X-Forwarded-For)
- D6: Best-effort (falha não quebra operação)
- D7: LGPD (apenas retrieve, não list)
- D8: Consulta (ReadOnly + IsAdmin)
- D9: Retenção (365 dias + cron)

## Próximas Evoluções

1. **Fase 6**: LGPD — registrar LEITURA em retrieve de Paciente/Evolução/Avaliação/etc.
2. **Dedupe de LEITURA**: evitar logar a mesma leitura N vezes em janela curta
3. **Tela React**: UI própria em `/admin/auditoria` (hoje é Django Admin)
4. **WebSocket alerts**: notificar Admin de eventos em tempo real
5. **Siem/exportação**: integrar com Splunk, ELK, etc.

---

**Especificação completa**: `.specify/features/audit-log-v1/spec.md`
**Plano técnico**: `.specify/features/audit-log-v1/plan.md`
**Validação**: `.specify/features/audit-log-v1/quickstart.md`
