# Quickstart / Validação — Log de Auditoria (audit-log-v1)

Cenários executáveis para provar o recurso ponta a ponta. Pré-requisitos: app rodando (Docker),
um usuário Administrador (`admin`) e um usuário não-admin (`psicologa1`).

## 1. Escrita gera auditoria (CREATE/UPDATE/DELETE)
1. Logar como `psicologa1` e **criar** um paciente.
2. **Editar** o telefone desse paciente.
3. **Excluir** o paciente.
- **Esperado**: como `admin`, em `GET /api/auditoria/?entidade=Paciente`, existem 3 eventos
  (`CREATE`, `UPDATE`, `DELETE`); o `UPDATE` mostra `telefone_principal: {de, para}`; nenhum evento
  contém senha/hash.

## 2. Login com sucesso e com falha
1. `POST /api/token/` com senha **errada** para `psicologa1`.
2. `POST /api/token/` com senha **correta**.
- **Esperado**: um `LOGIN_FALHA` (com `usuario_login=psicologa1`, `ip` preenchido, sem senha) e um
  `LOGIN`.

## 3. Logout
1. Estando logado, chamar `POST /api/auth/logout/` com o refresh token.
- **Esperado**: evento `LOGOUT`; reutilizar o mesmo refresh em `/api/token/refresh/` falha
  (blacklisted).

## 4. Leitura de prontuário (LGPD)
1. Como `psicologa1`, abrir o **detalhe** de um paciente (`GET /api/pacientes/{id}/`).
2. Apenas **listar** pacientes (`GET /api/pacientes/`).
- **Esperado**: o passo 1 gera `LEITURA`; o passo 2 **não** gera evento de leitura individual.

## 5. Permissão de consulta (somente Admin)
1. `GET /api/auditoria/` como `psicologa1`.
2. `GET /api/auditoria/` como `admin`.
- **Esperado**: passo 1 → **403**; passo 2 → **200** com a lista paginada.

## 6. Filtros e exportação
1. Como `admin`, filtrar por período + ação + entidade.
2. `GET /api/auditoria/exportar/?formato=xlsx&...` e `?formato=csv&...`.
- **Esperado**: lista coerente com os filtros; download de `auditoria.xlsx` e `auditoria.csv`.

## 7. Imutabilidade
1. `DELETE /api/auditoria/{id}/` e `PATCH /api/auditoria/{id}/` como `admin`.
- **Esperado**: **405 Method Not Allowed** (registro imutável).

## 8. Resiliência (falha de auditoria não quebra operação)
1. Simular falha na gravação do log (ex.: indisponibilidade temporária) e criar um registro normal.
- **Esperado**: a criação do registro **conclui com sucesso**; a falha de auditoria é apenas
  logada internamente.

## 9. Retenção
1. Inserir eventos antigos (> 12 meses) e rodar `python manage.py purge_audit_logs --days 365`.
- **Esperado**: eventos > 12 meses removidos; recentes preservados.
</content>
