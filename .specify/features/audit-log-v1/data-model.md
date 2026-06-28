# Data Model — Log de Auditoria (audit-log-v1)

## Entidade: AuditLog (tabela `tb_log_auditoria`, schema `neurocare`)

Registro imutável de um evento do sistema.

| Campo | Tipo | Nulo | Descrição |
|-------|------|:----:|-----------|
| `id` | BigAutoField (PK) | não | Identificador |
| `data_hora` | DateTimeField (auto_now_add, **index**) | não | Quando ocorreu |
| `id_usuario` | FK → `auth_user` (SET_NULL, **index**) | sim | Autor (nulo em LOGIN_FALHA/anônimo) |
| `usuario_login` | CharField(150) | não | Snapshot do login do autor (preservado) |
| `id_profissional` | FK → `Profissional` (SET_NULL) | sim | Profissional vinculado, se houver |
| `perfil` | CharField(50) | sim | Snapshot do perfil de acesso no momento |
| `acao` | CharField(20, choices) | não | Tipo do evento (ver abaixo) |
| `entidade` | CharField(100, **index** c/ objeto_id) | sim | Nome da entidade afetada |
| `objeto_id` | CharField(64) | sim | Identificador do registro afetado |
| `objeto_repr` | CharField(255) | sim | Rótulo legível (ex.: nome do paciente) |
| `alteracoes` | JSONField | sim | UPDATE: `{campo:{de,para}}`; CREATE: snapshot |
| `ip` | GenericIPAddressField | sim | IP real de origem |
| `user_agent` | CharField(255) | sim | Navegador/cliente |
| `metodo_http` | CharField(10) | sim | GET/POST/PUT/PATCH/DELETE |
| `caminho` | CharField(255) | sim | Rota acessada |

### Choices de `acao`
`LOGIN`, `LOGIN_FALHA`, `LOGOUT`, `CREATE`, `UPDATE`, `DELETE`, `LEITURA`.

### Índices
- `data_hora` (ordenação/consulta por período)
- `id_usuario` (consulta por usuário)
- (`entidade`, `objeto_id`) (histórico de um registro)
- `acao` (filtro por tipo)

### Regras / Invariantes
- **Imutável**: a aplicação não expõe update nem delete individual; apenas a rotina de retenção
  remove eventos (> 12 meses).
- **Campos sensíveis nunca persistidos** em `alteracoes`/snapshot: `password`, `senha`,
  `senha_hash`, `token`, `access`, `refresh`.
- `usuario_login`/`perfil` são **snapshots** (não dependem do usuário continuar existindo).
- Em `LOGIN_FALHA`, `id_usuario` pode ser nulo; `usuario_login` recebe o usuário tentado.

### Conteúdo de `alteracoes` por ação
| Ação | `alteracoes` |
|------|--------------|
| CREATE | snapshot dos campos do registro (sem sensíveis) |
| UPDATE | `{campo: {"de": valor_antigo, "para": valor_novo}}` só dos modificados |
| DELETE | nulo (rótulo vai em `objeto_repr`) |
| LOGIN / LOGOUT / LEITURA | nulo |
| LOGIN_FALHA | nulo (usuário tentado em `usuario_login`) |

## Entidades sensíveis auditadas em LEITURA
Paciente, EvolucaoClinica, AvaliacaoNeuropsicologica, ReabilitacaoNeuropsicologica,
ReabilitacaoSessao, ReabilitacaoObjetivo (recuperação individual / `retrieve`).

## Relacionamentos
- `AuditLog.id_usuario` → `auth_user` (autor).
- `AuditLog.id_profissional` → `Profissional` (quando o autor é um profissional).
- Vínculo lógico (não FK) com o registro auditado via (`entidade`, `objeto_id`).
</content>
