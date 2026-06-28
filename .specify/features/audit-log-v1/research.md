# Research — Log de Auditoria (audit-log-v1)

Decisões de design (Fase 0). Todas as incógnitas resolvidas; sem NEEDS CLARIFICATION.

## D1 — Mecanismo de captura de escrita (CREATE/UPDATE/DELETE)
- **Decisão**: Mixin no DRF (`AuditLogMixin`) sobrescrevendo `perform_create`,
  `perform_update`, `perform_destroy` nos ViewSets.
- **Rationale**: acesso direto a `request.user`, IP e user-agent; cobre exatamente as operações da
  API (escopo confirmado); diff de UPDATE feito lendo a instância antiga antes de salvar; aplicável
  de forma central (todos os ViewSets são `ModelViewSet`).
- **Alternativas consideradas**:
  - *Sinais `post_save`/`post_delete`*: pega escritas fora da API (Admin/shell/seed) mas perde
    contexto de request/usuário sem middleware thread-local e dispara em migração/seed. **Rejeitado**
    (escopo é "somente API"); fica como evolução futura se for preciso auditar o Django Admin.
  - *Pacotes prontos (django-auditlog/django-simple-history)*: trariam dependência e modelo de
    dados próprios, com menos controle sobre exclusão de campos sensíveis e formato exigido.
    **Rejeitado** por simplicidade/controle.

## D2 — Login (sucesso e falha)
- **Decisão**: subclasse de `TokenObtainPairView` (`AuditTokenObtainPairView`) que grava `LOGIN`
  no sucesso e `LOGIN_FALHA` quando a validação levanta `AuthenticationFailed`.
- **Rationale**: ponto único por onde todo login passa; captura usuário tentado e IP sem tocar nos
  serializers de cada entidade.
- **Alternativas**: signal `user_logged_in` do Django — não dispara para JWT (não usa sessão).
  **Rejeitado**.

## D3 — Logout (JWT stateless)
- **Decisão**: habilitar `rest_framework_simplejwt.token_blacklist` e endpoint
  `POST /api/auth/logout/` que faz blacklist do refresh token e grava `LOGOUT`; frontend chama no
  `logout()`.
- **Rationale**: dá um logout real (invalida o refresh) e um evento auditável.
- **Limitação aceita**: fechar o navegador sem deslogar não gera `LOGOUT` (best-effort). A
  expiração (access 30 min / refresh 7 dias) limita a janela.
- **Alternativas**: heartbeat/sessão curta — complexidade desproporcional. **Rejeitado**.

## D4 — Diff de alterações
- **Decisão**: comparar o estado serializado antigo x novo e registrar `{campo: {de, para}}` apenas
  dos campos alterados; aplicar lista de exclusão de campos sensíveis antes de persistir.
- **Rationale**: log compacto e legível; evita ruído de campos inalterados.
- **Campos sensíveis (denylist)**: `password`, `senha`, `senha_hash`, `token`, `access`, `refresh`.

## D5 — IP real atrás de proxy
- **Decisão**: extrair o IP do cabeçalho `X-Forwarded-For` (primeiro IP da lista) com fallback para
  `REMOTE_ADDR`. O nginx do frontend já repassa `X-Forwarded-For`/`X-Real-IP`.
- **Rationale**: sem isso, todos os eventos teriam o IP do container nginx.

## D6 — Gravação resiliente
- **Decisão**: `registrar_log` envolto em `try/except` (loga exceção, não propaga) e disparado em
  `transaction.on_commit`.
- **Rationale**: (a) auditoria nunca quebra a operação do usuário; (b) só registra o que foi
  efetivamente persistido (evita logar updates revertidos).

## D7 — Auditoria de leitura (LGPD)
- **Decisão**: registrar `LEITURA` apenas na recuperação individual (`retrieve`) das entidades
  sensíveis (Paciente e registros clínicos); **não** registrar `list`.
- **Rationale**: atende à LGPD (quem viu o prontuário) sem o volume explosivo de logar toda
  listagem. Dedupe opcional (mesma leitura, mesmo usuário, janela curta) se o volume incomodar.

## D8 — Consulta, permissão e exportação
- **Decisão**: `ReadOnlyModelViewSet` com `IsAdmin`; filtros via `django-filter`
  (período/usuário/ação/entidade); exportação CSV/XLSX reusando o padrão de
  `transacoes/export_view.py` (openpyxl).
- **Rationale**: reuso máximo dos padrões já existentes no projeto.

## D9 — Retenção
- **Decisão**: comando `purge_audit_logs --days 365` (padrão 12 meses), agendado por cron no deploy.
- **Rationale**: histórico útil sem crescimento ilimitado; alinhado à decisão do solicitante.
</content>
