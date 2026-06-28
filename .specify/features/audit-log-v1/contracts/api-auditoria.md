# API Contract — Auditoria (audit-log-v1)

Base: `/api/`. Autenticação JWT (Bearer). Salvo indicado, **consulta exige perfil Administrador**.

---

## 1. Captura automática (comportamento, sem endpoint próprio)
Toda operação de escrita/leitura pela API gera um `AuditLog` de forma transparente:

| Operação API | Ação registrada |
|--------------|-----------------|
| `POST /api/<entidade>/` | `CREATE` |
| `PUT/PATCH /api/<entidade>/{id}/` | `UPDATE` (com diff) |
| `DELETE /api/<entidade>/{id}/` | `DELETE` |
| `GET /api/<entidade sensível>/{id}/` | `LEITURA` |

Regras: best-effort (falha não quebra a operação), após commit, sem campos sensíveis.

---

## 2. Autenticação

### `POST /api/token/` (substitui a view padrão)
- **200**: login válido → `{ access, refresh }` **e** registra `LOGIN`.
- **401**: credenciais inválidas → registra `LOGIN_FALHA` (`usuario_login` = username tentado, `ip`).
- Nunca registra a senha.

### `POST /api/auth/logout/`
- **Body**: `{ "refresh": "<refresh_token>" }`
- **205/200**: invalida (blacklist) o refresh e registra `LOGOUT`.
- **400**: refresh ausente/ inválido.
- Requer estar autenticado.

---

## 3. Consulta de logs (Administrador)

### `GET /api/auditoria/`
Lista paginada, ordenada por `data_hora` desc.

**Query params (filtros)**:
| Param | Exemplo | Efeito |
|-------|---------|--------|
| `data_hora__gte` | `2026-06-01` | A partir de |
| `data_hora__lte` | `2026-06-30` | Até |
| `id_usuario` | `5` | Por usuário (auth_user id) |
| `acao` | `UPDATE` | Por ação |
| `entidade` | `Paciente` | Por entidade |
| `objeto_id` | `1a2b...` | Histórico de um registro |
| `search` | `texto` | Busca em `objeto_repr`/`usuario_login` |
| `page`, `page_size` | `1`, `25` | Paginação |

**200** → `{ count, next, previous, results: [AuditLog] }`
**403** → usuário sem perfil Administrador.

### `GET /api/auditoria/{id}/`
Detalhe de um evento (inclui `alteracoes`). **403** se não-Admin.

### `GET /api/auditoria/exportar/?formato=csv|xlsx&<mesmos filtros>`
Exporta os eventos filtrados.
- **200** → arquivo `auditoria.csv` ou `auditoria.xlsx` (colunas: Data/Hora, Usuário, Perfil, Ação,
  Entidade, Objeto, Alterações, IP).
- **403** se não-Admin.

### Imutabilidade
`POST/PUT/PATCH/DELETE` em `/api/auditoria/` → **405 Method Not Allowed** (ReadOnly).

---

## Forma do objeto `AuditLog` (resposta)
```json
{
  "id": 123,
  "data_hora": "2026-06-28T14:32:10Z",
  "usuario_login": "psicologa1",
  "perfil": "Psicologo",
  "acao": "UPDATE",
  "entidade": "Paciente",
  "objeto_id": "9f1c...",
  "objeto_repr": "João da Silva",
  "alteracoes": { "telefone_principal": { "de": "1199990000", "para": "1188887777" } },
  "ip": "187.127.37.57",
  "user_agent": "Mozilla/5.0 ...",
  "metodo_http": "PATCH",
  "caminho": "/api/pacientes/9f1c.../"
}
```
</content>
