# Contrato: Permissoes da API

## Endpoints e permissoes por perfil

### Secretaria
| Endpoint | GET | POST | PATCH | DELETE |
|----------|-----|------|-------|--------|
| `/api/pacientes/` | Todos | Sim | Sim (dados basicos) | Nao |
| `/api/contatos-emergencia/` | Todos | Sim | Sim | Nao |
| `/api/convenios/` | Sim | Nao | Nao | Nao |
| `/api/formas-pagamento/` | Sim | Nao | Nao | Nao |
| `/api/vendas-geral/` | Sem valores | Sim (sem valor) | Nao | Nao |
| `/api/transacoes/` | Nao | Nao | Nao | Nao |
| `/api/evolucao-clinica/` | Nao | Nao | Nao | Nao |
| `/api/avaliacao-*` | Nao | Nao | Nao | Nao |
| `/api/reabilitacao-*` | Nao | Nao | Nao | Nao |

### Psicologa
| Endpoint | GET | POST | PATCH | DELETE |
|----------|-----|------|-------|--------|
| `/api/pacientes/` | Seus pacientes | Sim | Sim | Nao |
| `/api/evolucao-clinica/` | Seus pacientes | Sim | Sim | Sim |
| `/api/avaliacao-*` | Seus pacientes | Sim | Sim | Sim |
| `/api/reabilitacao-*` | Seus pacientes | Sim | Sim | Sim |
| `/api/transacoes/` | Seus pacientes | Sim | Sim | Nao |
| `/api/vendas-vinculadas/` | Seus pacientes | Sim | Sim | Sim |
| `/api/vendas-geral/` | Suas vendas | Sim | Sim | Sim |

### Admin
Acesso total a todos os endpoints, todos os dados.

## Endpoint novo: Exportacao

```
GET /api/transacoes/exportar/
  ?formato=csv|xlsx
  &data_inicio=YYYY-MM-DD
  &data_fim=YYYY-MM-DD
  &id_psicologo=UUID
  &id_tipo_transacao=UUID
Response: arquivo CSV ou XLSX
```
