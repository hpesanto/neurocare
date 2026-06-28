# Feature Specification: Log de Auditoria

**Feature Branch**: `audit-log-v1`

**Created**: 2026-06-28

**Status**: Draft

**Input**: User description: "Log de auditoria do sistema: registrar autenticação (login com sucesso, login com falha, logout) e operações de dados (criação/INSERT, alteração/UPDATE, exclusão/DELETE) e, para conformidade LGPD, a leitura/visualização de prontuários de pacientes. Cada evento deve registrar quem (usuário e perfil), quando (data/hora), o quê (entidade e identificador do registro), o que mudou (diferença antes/depois nas alterações), e a origem (IP e navegador). Captura somente pelas operações feitas pela API. Login com falha deve ser registrado (usuário tentado e IP). Retenção dos logs por 12 meses com limpeza automática. Consulta dos logs restrita ao perfil Administrador, com filtros (período, usuário, ação, entidade) e exportação CSV/XLSX. Campos sensíveis (senha, hash de senha, tokens) nunca devem ser registrados. O registro de auditoria é imutável."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Rastrear alterações de dados (Priority: P1)

Como **Administrador**, quero ver quem criou, alterou ou excluiu cada registro do sistema
(pacientes, evoluções, avaliações, transações, vendas, etc.) e o que exatamente mudou, para
investigar erros, responsabilizar ações e ter histórico confiável.

**Why this priority**: É o coração da auditoria. Sem o registro de escrita não há rastreabilidade
das operações que mais impactam os dados clínicos e financeiros.

**Independent Test**: Criar, editar e excluir um registro qualquer pela aplicação e confirmar que
cada operação gerou um evento de auditoria com autor, data/hora, entidade, identificador e — na
edição — a diferença "de → para".

**Acceptance Scenarios**:

1. **Given** um usuário autenticado, **When** ele cria um novo paciente, **Then** é registrado um
   evento "CRIAÇÃO" com o autor, a data/hora, a entidade "Paciente", o identificador do registro
   e os dados informados (sem campos sensíveis).
2. **Given** um registro existente, **When** o usuário altera um ou mais campos, **Then** o evento
   "ALTERAÇÃO" registra apenas os campos modificados, com o valor anterior e o novo.
3. **Given** um registro existente, **When** o usuário o exclui, **Then** o evento "EXCLUSÃO"
   registra autor, data/hora, entidade, identificador e um rótulo legível do que foi excluído.

---

### User Story 2 - Auditar autenticação (Priority: P1)

Como **Administrador**, quero registrar entradas e saídas do sistema, incluindo tentativas de
login malsucedidas, para detectar acessos indevidos e investigar incidentes de segurança.

**Why this priority**: Saber quem entrou, quando e de onde — e identificar tentativas falhas — é
requisito básico de segurança e costuma ser o primeiro item exigido em auditorias.

**Independent Test**: Efetuar um login válido, um login com senha errada e um logout, e confirmar
que os três eventos foram registrados com usuário e origem (IP/navegador).

**Acceptance Scenarios**:

1. **Given** credenciais válidas, **When** o usuário faz login, **Then** é registrado um evento
   "LOGIN" com usuário, perfil, data/hora, IP e navegador.
2. **Given** credenciais inválidas, **When** alguém tenta logar, **Then** é registrado um evento
   "LOGIN_FALHA" com o usuário tentado e o IP (sem registrar a senha).
3. **Given** um usuário autenticado, **When** ele faz logout pela aplicação, **Then** é registrado
   um evento "LOGOUT" com usuário e data/hora.

---

### User Story 3 - Consultar e exportar os logs (Priority: P2)

Como **Administrador**, quero consultar os registros de auditoria com filtros e exportá-los, para
analisar atividades e atender solicitações de auditoria/conformidade.

**Why this priority**: O valor da auditoria só se concretiza quando os registros são consultáveis.
Depende de já existirem eventos (P1).

**Independent Test**: Acessar a tela de auditoria como Administrador, filtrar por período, usuário,
ação e entidade, e exportar o resultado em CSV e XLSX.

**Acceptance Scenarios**:

1. **Given** um Administrador autenticado, **When** ele abre a auditoria, **Then** vê a lista de
   eventos ordenada do mais recente para o mais antigo, com paginação.
2. **Given** a lista de eventos, **When** aplica filtros de período, usuário, ação e entidade,
   **Then** vê apenas os eventos que satisfazem os filtros.
3. **Given** um conjunto filtrado, **When** clica em exportar, **Then** baixa um arquivo CSV ou
   XLSX com os mesmos eventos.
4. **Given** um usuário sem perfil Administrador, **When** tenta acessar a auditoria, **Then** o
   acesso é negado.

---

### User Story 4 - Auditar leitura de prontuário (LGPD) (Priority: P3)

Como **Encarregado de dados (DPO)/Administrador**, quero registrar quem visualizou o prontuário de
cada paciente, para atender à LGPD no tratamento de dados sensíveis de saúde.

**Why this priority**: Exigência de conformidade importante, porém de maior volume e construída
sobre a base de captura já criada nas histórias anteriores.

**Independent Test**: Abrir o prontuário/registro detalhado de um paciente e confirmar que foi
gerado um evento "LEITURA" com autor, data/hora e identificação do prontuário acessado.

**Acceptance Scenarios**:

1. **Given** um usuário autenticado, **When** ele abre o detalhe de um prontuário (paciente,
   evolução, avaliação ou reabilitação), **Then** é registrado um evento "LEITURA" com autor,
   data/hora, entidade e identificador.
2. **Given** a navegação por listas, **When** o usuário apenas visualiza uma listagem geral,
   **Then** isso não gera evento de "LEITURA" individual (apenas a abertura de um prontuário
   específico é registrada).

---

### User Story 5 - Retenção e limpeza automática (Priority: P3)

Como **Administrador**, quero que os logs sejam mantidos por 12 meses e expurgados automaticamente
depois disso, para preservar histórico relevante sem crescimento ilimitado da base.

**Why this priority**: Sustentabilidade operacional; relevante após o sistema acumular volume.

**Independent Test**: Executar a rotina de limpeza e confirmar que eventos com mais de 12 meses são
removidos e os mais recentes preservados.

**Acceptance Scenarios**:

1. **Given** eventos com mais de 12 meses, **When** a rotina de limpeza roda, **Then** esses
   eventos são removidos.
2. **Given** eventos com menos de 12 meses, **When** a rotina de limpeza roda, **Then** eles são
   preservados.

---

### Edge Cases

- **Falha ao gravar a auditoria**: se o registro do log falhar, a operação principal do usuário
  **não** pode ser interrompida; a falha é tratada internamente e não afeta o usuário.
- **Operação revertida (rollback)**: se uma alteração não chega a ser persistida, **não** deve
  gerar evento de auditoria.
- **Usuário removido depois**: o log preserva uma cópia do identificador/login do autor, de modo
  que o evento continue legível mesmo se o usuário for excluído.
- **Logout não explícito**: se o usuário apenas fecha o navegador sem deslogar, pode não haver
  evento "LOGOUT" (registro do logout é best-effort).
- **Acesso atrás de proxy**: o IP de origem deve refletir o IP real do cliente, e não o do
  servidor intermediário.
- **Tentativa de adulteração**: não deve existir caminho na aplicação para editar ou apagar
  manualmente um registro de auditoria (apenas a limpeza por retenção remove eventos).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST registrar um evento de auditoria para cada criação, alteração e
  exclusão de registros realizada pela aplicação.
- **FR-002**: Em alterações, o sistema MUST registrar a diferença "valor anterior → novo valor"
  apenas dos campos efetivamente modificados.
- **FR-003**: O sistema MUST registrar login bem-sucedido, login malsucedido e logout.
- **FR-004**: Em login malsucedido, o sistema MUST registrar o usuário tentado e o IP, e MUST NOT
  registrar a senha informada.
- **FR-005**: O sistema MUST registrar, para conformidade LGPD, a visualização individual de
  prontuários de pacientes (dados de saúde).
- **FR-006**: Cada evento MUST conter: quem (usuário e perfil), quando (data/hora), ação,
  entidade e identificador do registro afetado (quando aplicável), origem (IP e navegador) e,
  quando aplicável, as alterações.
- **FR-007**: O sistema MUST NOT registrar campos sensíveis em nenhum evento (senha, hash de
  senha, tokens de acesso/atualização).
- **FR-008**: Os registros de auditoria MUST ser imutáveis — o sistema MUST NOT oferecer meio de
  editá-los ou excluí-los individualmente pela aplicação.
- **FR-009**: A captura MUST ocorrer somente para operações realizadas pela API da aplicação
  (alterações feitas fora da aplicação estão fora do escopo desta versão).
- **FR-010**: A consulta dos registros MUST ser restrita ao perfil Administrador.
- **FR-011**: A consulta MUST permitir filtrar por período (data inicial/final), usuário, ação e
  entidade, e MUST apresentar os eventos do mais recente para o mais antigo, com paginação.
- **FR-012**: O sistema MUST permitir exportar os eventos consultados em CSV e XLSX, respeitando
  os filtros aplicados.
- **FR-013**: O sistema MUST reter os eventos por 12 meses e MUST remover automaticamente os
  eventos mais antigos que esse período.
- **FR-014**: A falha ao registrar um evento de auditoria MUST NOT interromper ou reverter a
  operação principal do usuário.
- **FR-015**: O sistema MUST preservar uma identificação legível do autor no evento mesmo que o
  usuário seja posteriormente removido.
- **FR-016**: O sistema MUST registrar o IP real de origem do cliente quando a aplicação estiver
  atrás de proxy/reverse proxy.

### Key Entities *(include if feature involves data)*

- **Registro de Auditoria**: representa um evento ocorrido no sistema. Atributos principais:
  data/hora; autor (usuário) e perfil; identificação legível do autor (preservada); ação
  (LOGIN, LOGIN_FALHA, LOGOUT, CRIAÇÃO, ALTERAÇÃO, EXCLUSÃO, LEITURA); entidade afetada;
  identificador do registro afetado; rótulo legível do registro; alterações (campo → de/para);
  origem (IP e navegador). Relaciona-se com o usuário autor e, indiretamente, com o registro de
  qualquer entidade auditada.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% das criações, alterações e exclusões feitas pela aplicação geram um evento de
  auditoria correspondente.
- **SC-002**: 100% dos eventos de alteração apresentam a diferença "de → para" dos campos
  modificados.
- **SC-003**: 100% dos logins (com e sem sucesso) e logouts feitos pela aplicação são registrados.
- **SC-004**: 0 eventos contêm dados sensíveis (senha, hash de senha ou tokens) — verificável por
  inspeção dos registros.
- **SC-005**: Um Administrador consegue localizar todos os eventos de um usuário ou de um registro
  específico em menos de 1 minuto usando os filtros.
- **SC-006**: Usuários sem perfil Administrador têm 0% de acesso aos registros de auditoria.
- **SC-007**: Eventos com mais de 12 meses são removidos automaticamente; eventos dentro do período
  são preservados (verificável após a rotina de limpeza).
- **SC-008**: A indisponibilidade do registro de auditoria não causa nenhuma falha perceptível nas
  operações do usuário (as operações continuam concluindo normalmente).

## Assumptions

- A captura ocorre **somente pelas operações da API** da aplicação; alterações feitas diretamente
  no banco, por scripts ou pela área administrativa técnica estão fora do escopo desta versão.
- O logout é **best-effort**: como a sessão é baseada em token, o evento de logout é registrado
  quando o usuário desloga pela aplicação; fechar o navegador sem deslogar pode não gerar evento.
- Os perfis de acesso e o mecanismo de autenticação existentes são reutilizados (Administrador,
  Psicólogo, Secretária).
- Para a leitura LGPD, considera-se "prontuário" o detalhe individual de paciente e seus registros
  clínicos (evolução, avaliação, reabilitação/sessões). Listagens gerais não geram evento de
  leitura individual.
- O período de retenção padrão é de 12 meses; a limpeza é executada por uma rotina agendada.
- A exportação reutiliza o padrão de exportação já existente no sistema (financeiro).
</content>
