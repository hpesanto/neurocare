# Tasks: Log de Auditoria

**Input**: Design documents from `.specify/features/audit-log-v1/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-auditoria.md

**Tests**: incluídos (a spec define cenários de aceitação e o plano prevê testes na Fase 8).

**Organização**: por user story (P1→P3), para implementação/entrega incremental.

## Path Conventions
Web app: `backend/` (Django REST) e `frontend/` (React). Schema do banco: `neurocare`.

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Criar app Django `auditoria` (`backend/auditoria/`) e registrá-lo em `INSTALLED_APPS` em `backend/neurocare_project/settings.py`
- [ ] T002 Adicionar `rest_framework_simplejwt.token_blacklist` em `INSTALLED_APPS` em `backend/neurocare_project/settings.py` (necessário para o logout)
- [ ] T003 [P] Definir a denylist de campos sensíveis (`password`, `senha`, `senha_hash`, `token`, `access`, `refresh`) em `backend/auditoria/utils.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: modelo + serviço de registro + helpers. Bloqueia todas as user stories.

- [ ] T004 Criar o model `AuditLog` (tabela `tb_log_auditoria`, schema `neurocare`) com campos, `choices` de `acao` e índices, conforme `data-model.md`, em `backend/auditoria/models.py`
- [ ] T005 Gerar e aplicar a migração do `AuditLog` em `backend/auditoria/migrations/`
- [ ] T006 Implementar helpers de request (IP real via `X-Forwarded-For`, user-agent, mapeamento usuário→`Profissional`/perfil reusando `neurocare_project/permissions.get_profissional`) em `backend/auditoria/utils.py`
- [ ] T007 Implementar função de diff (`{campo:{de,para}}`) e remoção de campos sensíveis em `backend/auditoria/utils.py`
- [ ] T008 Implementar `registrar_log(...)` best-effort (`try/except` + `transaction.on_commit`) em `backend/auditoria/services.py`

---

## Phase 3: User Story 1 — Rastrear alterações de dados (P1) 🎯 MVP

**Goal**: toda criação/alteração/exclusão pela API gera evento com autor, data/hora, entidade, id e diff.
**Independent Test**: criar, editar e excluir um registro e confirmar 3 eventos (CREATE/UPDATE/DELETE), com diff no UPDATE e sem campos sensíveis.

- [ ] T009 [US1] Implementar `AuditLogMixin.perform_create` (registra `CREATE` com snapshot sem sensíveis) em `backend/auditoria/mixins.py`
- [ ] T010 [US1] Implementar `AuditLogMixin.perform_update` (lê instância antiga e registra `UPDATE` com diff) em `backend/auditoria/mixins.py`
- [ ] T011 [US1] Implementar `AuditLogMixin.perform_destroy` (registra `DELETE` com `objeto_repr`) em `backend/auditoria/mixins.py`
- [ ] T012 [US1] Aplicar o `AuditLogMixin` a todos os `ModelViewSet` (via classe base comum) em `backend/*/viewsets.py`
- [ ] T013 [P] [US1] Testes de auditoria de CREATE/UPDATE/DELETE (incl. não-vazamento de sensíveis) em `backend/auditoria/tests/test_writes.py`

**Checkpoint**: escrita auditável ponta a ponta — MVP entregue.

---

## Phase 4: User Story 2 — Auditar autenticação (P1)

**Goal**: registrar login (sucesso/falha) e logout.
**Independent Test**: login errado + login certo + logout geram `LOGIN_FALHA`, `LOGIN`, `LOGOUT`.

- [ ] T014 [US2] Implementar `AuditTokenObtainPairView` (registra `LOGIN`; em `AuthenticationFailed`, `LOGIN_FALHA` com usuário tentado + IP, nunca a senha) em `backend/auditoria/auth_views.py`
- [ ] T015 [US2] Implementar `LogoutView` (`POST /api/auth/logout/`: blacklist do refresh + `LOGOUT`) em `backend/auditoria/auth_views.py`
- [ ] T016 [US2] Apontar `api/token/` para a nova view e registrar `api/auth/logout/` em `backend/neurocare_project/urls.py`
- [ ] T017 [US2] Gerar/aplicar a migração do `token_blacklist`
- [ ] T018 [US2] Ajustar `logout()` no frontend para chamar `POST /api/auth/logout/` (com fallback) em `frontend/src/auth/AuthContext.tsx`
- [ ] T019 [P] [US2] Testes de login sucesso/falha e logout em `backend/auditoria/tests/test_auth.py`

**Checkpoint**: autenticação auditável.

---

## Phase 5: User Story 3 — Consultar e exportar (P2)

**Goal**: Administrador consulta/filtra/exporta os logs; não-Admin é bloqueado.
**Independent Test**: como Admin, filtrar e exportar CSV/XLSX; como não-Admin, receber 403.

- [ ] T020 [US3] Criar `AuditLogSerializer` (somente leitura) em `backend/auditoria/serializers.py`
- [ ] T021 [US3] Criar `AuditLogViewSet` (`ReadOnlyModelViewSet`, `IsAdmin`, filtros período/usuário/ação/entidade/objeto_id) em `backend/auditoria/viewsets.py`
- [ ] T022 [US3] Criar `exportar_auditoria` (CSV/XLSX) reusando o padrão de `backend/transacoes/export_view.py` em `backend/auditoria/export_view.py`
- [ ] T023 [US3] Registrar `/api/auditoria/` (router) e `/api/auditoria/exportar/` em `backend/neurocare_project/urls.py`
- [ ] T024 [US3] Criar a tela `AuditoriaPage` (FilterBar + DataTable + modal de diff) em `frontend/src/pages/admin/AuditoriaPage.tsx`
- [ ] T025 [US3] Adicionar a rota `/admin/auditoria` em `frontend/src/App.tsx`
- [ ] T026 [US3] Adicionar item de menu visível só para Admin em `frontend/src/components/Layout/Sidebar.tsx`
- [ ] T027 [P] [US3] Criar doc de ajuda da tela em `frontend/src/docs/admin-auditoria.md`
- [ ] T028 [P] [US3] Testes de acesso (Admin 200 / não-Admin 403) e filtros em `backend/auditoria/tests/test_query.py`

**Checkpoint**: logs consultáveis e exportáveis.

---

## Phase 6: User Story 4 — Auditar leitura de prontuário / LGPD (P3)

**Goal**: registrar `LEITURA` ao abrir prontuário individual; listagens não geram leitura.
**Independent Test**: abrir detalhe de paciente gera `LEITURA`; listar não.

- [ ] T029 [US4] Implementar `AuditLogMixin.retrieve` (registra `LEITURA`) em `backend/auditoria/mixins.py`
- [ ] T030 [US4] Habilitar captura de `LEITURA` nos viewsets sensíveis (Paciente, Evolução, Avaliação, Reabilitação, Sessão, Objetivo) em `backend/*/viewsets.py`
- [ ] T031 [P] [US4] Testes: `retrieve` gera `LEITURA`; `list` não em `backend/auditoria/tests/test_read.py`

**Checkpoint**: conformidade LGPD de leitura.

---

## Phase 7: User Story 5 — Retenção e limpeza (P3)

**Goal**: manter 12 meses e expurgar o resto automaticamente.
**Independent Test**: rodar a purga remove >12 meses e preserva recentes.

- [ ] T032 [US5] Criar comando `purge_audit_logs --days 365` em `backend/auditoria/management/commands/purge_audit_logs.py`
- [ ] T033 [US5] Adicionar cron diário de purga no deploy (documentar em `DEPLOY_VPS.md` e/ou `deploy.sh`)
- [ ] T034 [P] [US5] Teste de retenção (remove >12 meses, mantém recentes) em `backend/auditoria/tests/test_retention.py`

**Checkpoint**: crescimento da base controlado.

---

## Phase 8: Polish & Cross-Cutting

- [ ] T035 [P] Validar índices e desempenho da listagem/filtros de auditoria
- [ ] T036 [P] (Opcional) Deduplicar `LEITURA` repetida do mesmo usuário em janela curta em `backend/auditoria/mixins.py`
- [ ] T037 [P] Atualizar `README.md`/`DEPLOY_VPS.md` mencionando o log de auditoria e a purga
- [ ] T038 Executar todos os cenários de `quickstart.md` ponta a ponta

---

## Dependencies & Execution Order

- **Setup (Fase 1)** → **Foundational (Fase 2)** bloqueiam tudo.
- **US1 (Fase 3)** depende de Foundational. É o **MVP**.
- **US2 (Fase 4)** depende de Foundational (independente de US1).
- **US3 (Fase 5)** depende de existirem eventos (Foundational + idealmente US1/US2) e do modelo.
- **US4 (Fase 6)** depende do `AuditLogMixin` (US1).
- **US5 (Fase 7)** depende do modelo (Foundational).
- **Polish (Fase 8)** por último.

## Parallel Opportunities

- Fase 2: T006 e T007 tocam `utils.py` (sequenciais); T008 depende de T006/T007.
- Após Foundational, **US1 e US2 podem ser tocadas em paralelo** (arquivos distintos).
- Testes marcados `[P]` (T013, T019, T028, T031, T034) rodam em paralelo ao restante de cada fase.
- Na US3, T027 (doc) e T028 (testes) são `[P]`.

## Implementation Strategy

- **MVP**: Fase 1 + Fase 2 + **US1** (escrita auditável). Entrega valor sozinho.
- **Incremento 2**: US2 (autenticação).
- **Incremento 3**: US3 (consulta/exportação — torna o recurso utilizável pelo Admin).
- **Incremento 4**: US4 (LGPD) e US5 (retenção).
- **Fechamento**: Fase 8 (polish + validação do quickstart).

## Resumo
- **Total de tarefas**: 38 (T001–T038)
- **Por story**: US1=5, US2=6, US3=9, US4=3, US5=3; Setup=3, Foundational=5, Polish=4
- **MVP sugerido**: US1 (+ Setup/Foundational)
</content>
