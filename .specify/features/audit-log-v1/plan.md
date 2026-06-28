# Implementation Plan: Log de Auditoria

**Branch**: `audit-log-v1` | **Date**: 2026-06-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `.specify/features/audit-log-v1/spec.md`

## Summary

Registrar, de forma imutável e consultável, os eventos do sistema: autenticação (login com
sucesso, login com falha, logout), operações de dados (criação, alteração com diff, exclusão) e
leitura de prontuários (LGPD). A captura ocorre **somente pela API**, via um mixin do DRF para as
escritas/leituras e uma subclasse da view de obtenção de token para o login; o logout usa blacklist
de refresh token. Os eventos ficam em uma tabela imutável, com retenção de 12 meses e consulta
restrita ao Administrador (com filtros e exportação CSV/XLSX).

## Technical Context

**Language/Version**: Python 3.12, Django 5.2, DRF 3.16; TypeScript/React 19 (frontend)

**Primary Dependencies**: djangorestframework-simplejwt 5.5 (+ `token_blacklist`), django-filter,
openpyxl (export XLSX), React-Bootstrap (frontend)

**Storage**: PostgreSQL 16 (schema `neurocare`); nova tabela `tb_log_auditoria`

**Testing**: Django `TestCase`/DRF `APITestCase` (backend)

**Target Platform**: Backend em container Docker (gunicorn); frontend SPA servido por nginx

**Project Type**: Web application (backend Django REST + frontend React)

**Performance Goals**: Gravação de auditoria não pode adicionar latência perceptível à operação do
usuário; escrita best-effort e após commit. `LEITURA` é a ação de maior volume.

**Constraints**: Registro imutável (sem update/delete via app); nunca persistir campos sensíveis;
captura apenas via API; IP real atrás de proxy nginx; logout best-effort (JWT stateless).

**Scale/Scope**: ~25 telas / ~20 entidades auditáveis; volume dominado por LEITURA e por escrita
de evolução/agenda; retenção 12 meses com purga agendada.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

A constituição do projeto (`.specify/memory/constitution.md`) está como template (sem princípios
personalizados), portanto **não há gates específicos** a violar. Princípios gerais aplicados por
prudência:

- **Simplicidade**: reuso dos padrões existentes (ViewSets, `permissions.py`, exportação do
  financeiro) em vez de framework de auditoria externo.
- **Segurança/Privacidade**: exclusão de campos sensíveis e imutabilidade do log — alinhado ao
  domínio (dados de saúde / LGPD).
- **Observabilidade**: o recurso, por natureza, aumenta a rastreabilidade do sistema.

Resultado: **PASS** (inicial e pós-design).

## Project Structure

### Documentation (this feature)

```text
.specify/features/audit-log-v1/
├── plan.md              # Este arquivo
├── spec.md              # Especificação
├── research.md          # Decisões de design (Fase 0)
├── data-model.md        # Modelo de dados (Fase 1)
├── quickstart.md        # Guia de validação (Fase 1)
├── contracts/
│   └── api-auditoria.md  # Contrato dos endpoints (Fase 1)
└── checklists/
    └── requirements.md   # Checklist de qualidade da spec
```

### Source Code (repository root)

```text
backend/
├── auditoria/                     # NOVO app
│   ├── models.py                  # AuditLog (tb_log_auditoria)
│   ├── services.py                # registrar_log(...) — gravação best-effort/on_commit
│   ├── utils.py                   # IP/user-agent, diff, remoção de campos sensíveis
│   ├── mixins.py                  # AuditLogMixin (perform_create/update/destroy/retrieve)
│   ├── auth_views.py              # AuditTokenObtainPairView, LogoutView
│   ├── serializers.py             # AuditLogSerializer (read-only)
│   ├── viewsets.py                # AuditLogViewSet (ReadOnly, IsAdmin)
│   ├── export_view.py             # exportar_auditoria (CSV/XLSX)
│   ├── permissions.py?            # reusa neurocare_project/permissions.IsAdmin
│   └── management/commands/purge_audit_logs.py
├── neurocare_project/
│   ├── settings.py                # + app token_blacklist + auditoria
│   └── urls.py                    # troca api/token/; + api/auth/logout/; + api/auditoria/
└── <apps existentes>/viewsets.py  # passam a herdar o AuditLogMixin

frontend/
├── src/pages/admin/AuditoriaPage.tsx   # tela de consulta (Admin)
├── src/components/Layout/Sidebar.tsx   # item de menu (visível só p/ Admin)
├── src/App.tsx                         # rota /admin/auditoria
├── src/auth/AuthContext.tsx            # logout() chama /api/auth/logout/
└── src/docs/admin-auditoria.md         # doc de ajuda da tela
```

## Implementation Phases

> Detalhamento por fase; a quebra em tarefas executáveis é gerada pelo `/speckit-tasks`.

### Fase 1 — App e modelo (Backend)
Criar app `auditoria` + model `AuditLog` (schema `neurocare`) + migração com índices. Registrar em
`INSTALLED_APPS`. Registro imutável (sem expor update/delete).

### Fase 2 — Serviço de registro + helpers
`registrar_log(...)` (best-effort, `transaction.on_commit`); helpers de IP (atrás do nginx via
`X-Forwarded-For`), user-agent, mapeamento usuário→profissional/perfil (reusa
`permissions.get_profissional`/`get_perfil_nome`), função de diff e remoção de campos sensíveis.

### Fase 3 — Captura de CREATE/UPDATE/DELETE
`AuditLogMixin` sobrescreve `perform_create/perform_update/perform_destroy`. Aplicar a todos os
`ModelViewSet` (via base comum). UPDATE captura instância antiga para diff.

### Fase 3B — Captura de LEITURA (LGPD)
`AuditLogMixin.retrieve` grava `LEITURA` nas entidades sensíveis (Paciente, Evolução, Avaliação,
Reabilitação/Sessão/Objetivo). Não loga `list`. Cuidar do volume (índices, on_commit, dedupe
opcional em janela curta).

### Fase 4 — Login (sucesso e falha)
`AuditTokenObtainPairView` registra `LOGIN`/`LOGIN_FALHA` (usuário tentado + IP; nunca a senha).
Apontar `api/token/` para a nova view.

### Fase 5 — Logout
Adicionar `rest_framework_simplejwt.token_blacklist` (+ migração) e endpoint
`POST /api/auth/logout/` (blacklist do refresh + `LOGOUT`). Frontend chama no `logout()`.

### Fase 6 — API de consulta (Admin)
`AuditLogViewSet(ReadOnlyModelViewSet)` com `IsAdmin`; filtros por período/usuário/ação/entidade;
exportação CSV/XLSX reusando o padrão de `transacoes/export_view.py`. Registrar `/api/auditoria/`.

### Fase 7 — Tela de Auditoria (Frontend)
`AuditoriaPage` (FilterBar + DataTable + modal de diff); item de menu só p/ Admin; doc de ajuda.

### Fase 8 — Retenção, índices e testes
Comando `purge_audit_logs --days 365` (padrão 12 meses) + cron no deploy; testes por ação,
não-vazamento de sensíveis e resiliência (falha de log não quebra operação).

## Complexity Tracking

Sem desvios que exijam justificativa. Nenhuma dependência nova além do app de blacklist do
SimpleJWT (já presente como pacote) e reuso do `openpyxl` já instalado.
</content>
